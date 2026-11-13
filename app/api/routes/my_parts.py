from beanie import PydanticObjectId
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel

import auto_claims
import field_claims
import options
import uploads
from bot import game_alerts
from core.models.history import record, record_delete, record_new
from core.models.user import User
from models.game import Claim, Game, Part
from models.rule import Rule
from models.task import Task
from models.vocab import PART_KINDS
from parts_clean import kind_fields
from routes.my_game import author, my_game
from routes.my_rules import drop_rule
from zones import kind_of

router = APIRouter(prefix="/api/my/game/parts")


class PartIn(BaseModel):
    kind: str = ""  # vocab.PART_KINDS; fixed after creation
    title: str = ""
    task: str = ""  # window type: a card of kind window; on PUT "" = leave as is
    role: str = ""  # entity: the opt of a role card
    icon: str = ""  # entity
    description: str = ""
    window: str = ""  # menu: host window part id
    items: list[dict] = []
    props: dict = {}  # field, level
    stats: list[dict] = []  # entity, level
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
    if not task or kind_of(task) != "window" or task.status == "archived":
        raise HTTPException(422, "Тип вікна — картка каталогу з типом «тип вікна».")
    if task.status != "active" and not options.is_admin(user):
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


async def fields(kind: str, data: PartIn, game: Game, user: User) -> dict:
    d = await clean_menu(data, game) if kind == "menu" else {}
    return d | kind_fields(kind, data.model_dump(), await options.catalog(options.is_admin(user)))


@router.post("")
async def create_part(data: PartIn, tasks: BackgroundTasks, game: Game = Depends(my_game),
                      user: User = Depends(author)):
    if data.kind not in PART_KINDS:
        raise HTTPException(422, "Невідомий тип обʼєкта.")
    title = data.title.strip() or ("Поле" if data.kind == "field" else "")
    if not title:
        raise HTTPException(422, "Назва — обовʼязкова.")
    d = {"game": game.id, "kind": data.kind, "title": title, "description": data.description, "order": data.order}
    if data.kind == "field" and await Part.find_one(Part.game == game.id, Part.kind == "field"):
        raise HTTPException(409, "Поле в грі одне — воно вже є.")
    if data.kind == "window":
        await check_window_type(data.task, user)
        d["task"] = data.task
    part = Part(**d | await fields(data.kind, data, game, user))
    await part.insert()
    await record_new(part, actor=user.email)
    await auto_claims.sync(game, user.email)
    if part.kind == "field":
        await field_claims.seat(game, part, user.email)
    tasks.add_task(game_alerts.part, user, part, 0)
    return part.api()


@router.put("/{id}")
async def update_part(id: PydanticObjectId, data: PartIn, game: Game = Depends(my_game),
                      user: User = Depends(author)):
    part = await get_part(id, game)
    d = {"title": data.title.strip(), "description": data.description, "order": data.order}
    if not d["title"]:
        raise HTTPException(422, "Назва — обовʼязкова.")
    if part.kind == "window" and data.task and data.task != part.task:  # a new type: its auto-claim follows
        await check_window_type(data.task, user)
        d["task"] = data.task
    await record(part, d | await fields(part.kind, data, game, user), actor=user.email)
    await auto_claims.sync(game, user.email)
    return part.api()


@router.delete("/{id}")
async def delete_part(id: PydanticObjectId, tasks: BackgroundTasks, game: Game = Depends(my_game),
                      user: User = Depends(author)):
    part = await get_part(id, game)
    pid = str(part.id)
    for claim in await Claim.find(Claim.game == game.id, Claim.part == pid).to_list():
        uploads.drop_shots(claim)
        await record_delete(claim, actor=user.email)
    for rule in await Rule.find(Rule.game == game.id).to_list():  # a sentence loses its subject
        if rule.uses(pid):
            await drop_rule(rule, user.email)
    for name in part.screenshots:
        uploads.drop_shot(str(game.id), name)
    if part.kind == "window":  # strip dangling references from menus
        for menu in await Part.find(Part.game == game.id, Part.kind == "menu").to_list():
            patch = {"window": ""} if menu.window == pid else {}
            items = [it | {"window": ""} if it.get("window") == pid else it for it in menu.items]
            if items != menu.items:
                patch["items"] = items
            if patch:
                await record(menu, patch, actor=user.email)
    await record_delete(part, actor=user.email)
    await auto_claims.sync(game, user.email)
    tasks.add_task(game_alerts.part, user, part, 2)
    return {"ok": True}

