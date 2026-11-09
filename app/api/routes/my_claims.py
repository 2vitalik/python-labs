from beanie import PydanticObjectId
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel

from bot import game_alerts
from core.deps import active_user
from core.models.history import record, record_delete, record_new
from core.models.user import Status, User
from models.game import Claim, Game
from models.task import Task
from routes.my_game import my_game
from routes.my_parts import part_of

router = APIRouter(prefix="/api/my/claims")


class ClaimIn(BaseModel):
    task: str = ""
    part: str | None = None  # None on PUT = leave as is; "" = game level / the drafts pool
    params: dict = {}
    note: str = ""
    link: str = ""


def clean_params(task: Task, params: dict, loose: bool = False) -> dict:
    """Slot values by the card's specs; `loose` lets a draft wait for its required params (the catalog's «＋ у гру»)."""
    specs = {s["key"]: s for s in task.slots}
    if unknown := set(params) - set(specs):
        raise HTTPException(422, f"Картка не має параметра «{unknown.pop()}».")
    out = {}
    for key, s in specs.items():
        v = params.get(key)
        if isinstance(v, str):
            v = v.strip()
        if v is None or v == "":
            if s.get("required") and not loose:
                raise HTTPException(422, f"Потрібен параметр «{s['label']}».")
            continue
        kind = s.get("type", "int")
        if kind == "int" and (not isinstance(v, int) or isinstance(v, bool)):
            raise HTTPException(422, f"«{s['label']}» — число.")
        if kind == "bool" and not isinstance(v, bool):
            raise HTTPException(422, f"«{s['label']}» — так/ні.")
        if kind == "choice" and v not in s.get("options", []):
            raise HTTPException(422, f"«{s['label']}» — зі списку варіантів.")
        if kind == "text" and not isinstance(v, str):
            raise HTTPException(422, f"«{s['label']}» — текст.")
        out[key] = v
    return out


async def get_claim(id: PydanticObjectId, game: Game) -> Claim:
    claim = await Claim.get(id)
    if not claim or claim.game != game.id:
        raise HTTPException(404)
    return claim


async def check_part(game: Game, part: str) -> str:
    if part and not await part_of(game, part):
        raise HTTPException(422, "Обʼєкт не знайдено.")
    return part


async def check_unique(game: Game, task: str, part: str, me: Claim | None = None) -> None:
    other = await Claim.find_one(Claim.game == game.id, Claim.task == task, Claim.part == part)
    if other and (not me or other.id != me.id):
        raise HTTPException(409, "Така заявка вже є." if part else "Така заявка вже є серед заявок гри.")


@router.post("")
async def create_claim(data: ClaimIn, tasks: BackgroundTasks, game: Game = Depends(my_game),
                       user: User = Depends(active_user)):
    task = await Task.find_one(Task.slug == data.task)
    if not task or task.status == "archived":
        raise HTTPException(422, "Немає такої картки в каталозі.")
    if task.status != "active" and user.status != Status.admin:
        raise HTTPException(422, "Ця картка ще чернетка.")
    part = await check_part(game, data.part or "")
    await check_unique(game, data.task, part)
    claim = Claim(game=game.id, task=data.task, part=part, params=clean_params(task, data.params, loose=not part),
                  note=data.note.strip(), link=data.link.strip())
    await claim.insert()
    await record_new(claim, actor=user.email)
    tasks.add_task(game_alerts.claim, user, claim, 0)
    return claim.api()


@router.put("/{id}")
async def update_claim(id: PydanticObjectId, data: ClaimIn, tasks: BackgroundTasks, game: Game = Depends(my_game),
                       user: User = Depends(active_user)):
    claim = await get_claim(id, game)
    task = await Task.find_one(Task.slug == claim.task)
    patch = {"note": data.note.strip(), "link": data.link.strip()}
    if data.part is not None and data.part != claim.part:  # a draft finds its anchor, or moves to another one
        patch["part"] = await check_part(game, data.part)
        await check_unique(game, claim.task, patch["part"], me=claim)
    if task:  # card gone from the catalog → params frozen as claimed
        patch["params"] = clean_params(task, data.params, loose=not (data.part if data.part is not None else claim.part))
    if changes := await record(claim, patch, actor=user.email):
        tasks.add_task(game_alerts.claim, user, claim, 1, changes)
    return claim.api()


@router.delete("/{id}")
async def delete_claim(id: PydanticObjectId, tasks: BackgroundTasks, game: Game = Depends(my_game),
                       user: User = Depends(active_user)):
    claim = await get_claim(id, game)
    await record_delete(claim, actor=user.email)
    tasks.add_task(game_alerts.claim, user, claim, 2)
    return {"ok": True}
