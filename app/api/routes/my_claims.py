from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from deps import active_user
from models.game import Claim, Game
from models.history import record, record_delete, record_new
from models.task import Task
from models.user import Status, User
from routes.my_game import my_game
from routes.my_parts import part_of

router = APIRouter(prefix="/api/my/claims")


class ClaimIn(BaseModel):
    task: str = ""
    part: str = ""
    params: dict = {}
    note: str = ""
    link: str = ""


def clean_params(task: Task, params: dict) -> dict:
    specs = {s["key"]: s for s in task.slots}
    if unknown := set(params) - set(specs):
        raise HTTPException(422, f"Картка не має параметра «{unknown.pop()}».")
    out = {}
    for key, s in specs.items():
        v = params.get(key)
        if isinstance(v, str):
            v = v.strip()
        if v is None or v == "":
            if s.get("required"):
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


@router.post("")
async def create_claim(data: ClaimIn, game: Game = Depends(my_game), user: User = Depends(active_user)):
    task = await Task.find_one(Task.slug == data.task)
    if not task or task.status == "archived":
        raise HTTPException(422, "Немає такої картки в каталозі.")
    if task.status != "active" and user.status != Status.admin:
        raise HTTPException(422, "Ця картка ще чернетка.")
    if data.part and not await part_of(game, data.part):
        raise HTTPException(422, "Обʼєкт не знайдено.")
    if await Claim.find_one(Claim.game == game.id, Claim.task == data.task, Claim.part == data.part):
        raise HTTPException(409, "Така заявка вже є.")
    claim = Claim(game=game.id, task=data.task, part=data.part, params=clean_params(task, data.params),
                  note=data.note.strip(), link=data.link.strip())
    await claim.insert()
    await record_new(claim, actor=user.email)
    return claim.api()


@router.put("/{id}")
async def update_claim(id: PydanticObjectId, data: ClaimIn, game: Game = Depends(my_game),
                       user: User = Depends(active_user)):
    claim = await get_claim(id, game)
    task = await Task.find_one(Task.slug == claim.task)
    patch = {"note": data.note.strip(), "link": data.link.strip()}
    if task:  # card gone from the catalog → params frozen as claimed
        patch["params"] = clean_params(task, data.params)
    await record(claim, patch, actor=user.email)
    return claim.api()


@router.delete("/{id}")
async def delete_claim(id: PydanticObjectId, game: Game = Depends(my_game), user: User = Depends(active_user)):
    claim = await get_claim(id, game)
    await record_delete(claim, actor=user.email)
    return {"ok": True}
