from beanie import PydanticObjectId
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, UploadFile
from pydantic import BaseModel

import uploads
from bot import game_alerts
from deps import active_user
from models.game import Claim, Game, Part
from models.history import record, record_delete, record_new
from models.rule import ROLES, Rule
from models.task import Task
from models.user import Status, User
from routes.my_game import my_game

router = APIRouter(prefix="/api/my/game/parts")


class PartIn(BaseModel):
    kind: str = ""  # window | menu | entity; fixed after creation
    title: str
    task: str = ""  # window type: catalog slug tagged "window"
    role: str = ""  # entity role from the ROLES dictionary
    description: str = ""
    window: str = ""  # menu: host window part id
    items: list[dict] = []
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


@router.post("")
async def create_part(data: PartIn, tasks: BackgroundTasks, game: Game = Depends(my_game),
                      user: User = Depends(active_user)):
    if data.kind not in ("window", "menu", "entity"):
        raise HTTPException(422, "Невідомий тип обʼєкта.")
    d = {"game": game.id, "kind": data.kind, "title": data.title.strip(),
         "description": data.description, "order": data.order}
    if not d["title"]:
        raise HTTPException(422, "Назва — обовʼязкова.")
    if data.kind == "window":
        await check_window_type(data.task, user)
        d["task"] = data.task
    elif data.kind == "entity":
        check_role(data.role)
        d["role"] = data.role
    else:
        d |= await clean_menu(data, game)
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
    elif part.kind == "entity":
        check_role(data.role)
        d["role"] = data.role
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
