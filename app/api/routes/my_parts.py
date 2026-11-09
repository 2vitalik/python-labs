from beanie import PydanticObjectId
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, UploadFile
from pydantic import BaseModel

import uploads
from bot import game_alerts
from core.deps import active_user
from core.models.history import record, record_delete, record_new
from core.models.user import Status, User
from models.game import Claim, Game, Part
from models.rule import Rule
from models.task import Task
from models.vocab import FIELD, PART_KINDS, ROLES, STATS
from routes.my_game import my_game

router = APIRouter(prefix="/api/my/game/parts")
KIND_NAMES = {"field": "поле", "entity": "сутність", "window": "вікно", "menu": "меню"}


class PartIn(BaseModel):
    kind: str = ""  # vocab.PART_KINDS; fixed after creation
    title: str = ""
    task: str = ""  # window type: catalog slug tagged "window"
    role: str = ""  # entity role from vocab.ROLES
    description: str = ""
    window: str = ""  # menu: host window part id
    items: list[dict] = []
    props: dict = {}  # field
    stats: list[dict] = []  # entity
    states: list[str] = []  # entity
    order: int = 0


async def part_of(game: Game, pid: str, kind: str = "") -> Part | None:
    try:
        part = await Part.get(PydanticObjectId(pid))
    except Exception:
        return None
    ok = part and part.game == game.id and (not kind or part.kind == kind)
    return part if ok else None


async def get_part(id: PydanticObjectId, game: Game) -> Part:
    part = await part_of(game, str(id))
    if not part:
        raise HTTPException(404)
    return part


async def check_window_type(slug: str, user: User) -> None:
    task = await Task.find_one(Task.slug == slug)
    if not task or "window" not in task.tags or task.status == "archived":
        raise HTTPException(422, "Тип вікна — картка каталогу з тегом window.")
    if task.status != "active" and user.status != Status.admin:
        raise HTTPException(422, "Ця картка-тип ще чернетка.")


async def clean_menu(data: PartIn, game: Game) -> dict:
    if data.window and not await part_of(game, data.window, kind="window"):
        raise HTTPException(422, "Вікно-хост не знайдено.")
    items = []
    for it in data.items:
        item = {k: str(it.get(k) or "").strip() for k in ("title", "window", "task", "note")}
        if not item["title"]:
            continue
        if item["window"] and not await part_of(game, item["window"], kind="window"):
            raise HTTPException(422, f"Пункт «{item['title']}»: цільове вікно не знайдено.")
        if item["task"] and not await Task.find_one(Task.slug == item["task"]):
            raise HTTPException(422, f"Пункт «{item['title']}»: немає такої картки.")
        items.append(item)
    return {"window": data.window, "items": items}


def check_role(role: str) -> None:
    if role not in ROLES:
        raise HTTPException(422, "Роль сутності — зі словника.")


def clean_props(props: dict) -> dict:
    """The field's properties by vocab.FIELD: unknown keys dropped, choices checked, empty values left out."""
    out = {}
    for spec in FIELD:
        v = props.get(spec["key"])
        if v is None or v == "" or v == []:
            continue
        if spec["type"] == "bool":
            v = bool(v)
        elif spec["type"] == "choice":
            if str(v) not in spec["options"]:
                raise HTTPException(422, f"«{spec['label']}» — зі списку.")
        elif spec["type"] == "tags":
            v = [str(x).strip() for x in (v if isinstance(v, list) else str(v).split(",")) if str(x).strip()]
            if not v:
                continue
        else:
            v = str(v).strip()
            if not v:
                continue
        out[spec["key"]] = v
    return out


def clean_stats(stats: list[dict]) -> list[dict]:
    """Entity stats: a key (a known one or the student's own word), a value as text, an optional unit."""
    known = {k: (label, unit) for k, label, _, unit in STATS}
    out, seen = [], set()
    for s in stats:
        key = str(s.get("key") or "").strip()
        value = str(s.get("value") if s.get("value") is not None else "").strip()
        if not key or key.lower() in seen:
            continue
        if not value:
            raise HTTPException(422, f"Параметр «{key}» — без значення.")
        label = str(s.get("label") or "").strip() or known.get(key, (key, ""))[0]
        unit = str(s.get("unit") or "").strip() or (known[key][1] if key in known and not s.get("unit") else "")
        out.append({"key": key, "label": label, "value": value, "unit": unit})
        seen.add(key.lower())
    return out


def clean_states(states: list[str]) -> list[str]:
    out = []
    for s in states:
        s = " ".join(str(s).split())
        if s and s.lower() not in {x.lower() for x in out}:
            out.append(s)
    if len(out) > 12:
        raise HTTPException(422, "Станів забагато — до 12.")
    return out


def kind_fields(part_kind: str, data: PartIn) -> dict:
    if part_kind == "entity":
        check_role(data.role)
        return {"role": data.role, "stats": clean_stats(data.stats), "states": clean_states(data.states)}
    if part_kind == "field":
        return {"props": clean_props(data.props)}
    return {}


@router.post("")
async def create_part(data: PartIn, tasks: BackgroundTasks, game: Game = Depends(my_game),
                      user: User = Depends(active_user)):
    if data.kind not in PART_KINDS:
        raise HTTPException(422, "Невідомий тип обʼєкта.")
    title = data.title.strip() or ("Поле" if data.kind == "field" else "")
    if not title:
        raise HTTPException(422, "Назва — обовʼязкова.")
    d = {"game": game.id, "kind": data.kind, "title": title, "description": data.description, "order": data.order}
    if data.kind == "field":
        if await Part.find_one(Part.game == game.id, Part.kind == "field"):
            raise HTTPException(409, "Поле в грі одне — воно вже є.")
    elif data.kind == "window":
        await check_window_type(data.task, user)
        d["task"] = data.task
    elif data.kind == "menu":
        d |= await clean_menu(data, game)
    d |= kind_fields(data.kind, data)
    part = Part(**d)
    await part.insert()
    await record_new(part, actor=user.email)
    tasks.add_task(game_alerts.part, user, part, 0)
    if data.kind == "window":  # a window claims its type card automatically
        claim = Claim(game=game.id, task=data.task, part=str(part.id))
        await claim.insert()
        await record_new(claim, actor=user.email)
    return part.api()


@router.put("/{id}")
async def update_part(id: PydanticObjectId, data: PartIn, game: Game = Depends(my_game),
                      user: User = Depends(active_user)):
    part = await get_part(id, game)
    d = {"title": data.title.strip(), "description": data.description, "order": data.order}
    if not d["title"]:
        raise HTTPException(422, "Назва — обовʼязкова.")
    if part.kind == "menu":
        d |= await clean_menu(data, game)
    d |= kind_fields(part.kind, data)
    await record(part, d, actor=user.email)
    return part.api()


@router.delete("/{id}")
async def delete_part(id: PydanticObjectId, tasks: BackgroundTasks, game: Game = Depends(my_game),
                      user: User = Depends(active_user)):
    part = await get_part(id, game)
    for claim in await Claim.find(Claim.game == game.id, Claim.part == str(part.id)).to_list():
        await record_delete(claim, actor=user.email)
    for rule in await Rule.find(Rule.game == game.id).to_list():  # a sentence loses its subject
        if rule.uses(str(part.id)):
            await record_delete(rule, actor=user.email)
    for name in part.screenshots:
        uploads.drop_shot(str(game.id), name)
    if part.kind == "window":  # strip dangling references from menus
        pid = str(part.id)
        for menu in await Part.find(Part.game == game.id, Part.kind == "menu").to_list():
            patch = {"window": ""} if menu.window == pid else {}
            items = [it | {"window": ""} if it.get("window") == pid else it for it in menu.items]
            if items != menu.items:
                patch["items"] = items
            if patch:
                await record(menu, patch, actor=user.email)
    await record_delete(part, actor=user.email)
    tasks.add_task(game_alerts.part, user, part, 2)
    return {"ok": True}


@router.post("/{id}/screenshot")
async def add_screenshot(id: PydanticObjectId, file: UploadFile, game: Game = Depends(my_game),
                         user: User = Depends(active_user)):
    part = await get_part(id, game)
    name = await uploads.save_shot(str(game.id), file)
    await record(part, {"screenshots": part.screenshots + [name]}, actor=user.email)
    return part.api()


@router.delete("/{id}/screenshot/{name}")
async def delete_screenshot(id: PydanticObjectId, name: str, game: Game = Depends(my_game),
                            user: User = Depends(active_user)):
    part = await get_part(id, game)
    if name not in part.screenshots:
        raise HTTPException(404)
    uploads.drop_shot(str(game.id), name)
    await record(part, {"screenshots": [s for s in part.screenshots if s != name]}, actor=user.email)
    return part.api()
