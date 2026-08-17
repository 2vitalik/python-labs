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
    note: str = ""
    link: str = ""


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
    claim = Claim(game=game.id, task=data.task, part=data.part,
                  note=data.note.strip(), link=data.link.strip())
    await claim.insert()
    await record_new(claim, actor=user.email)
    return claim.api()


@router.put("/{id}")
async def update_claim(id: PydanticObjectId, data: ClaimIn, game: Game = Depends(my_game),
                       user: User = Depends(active_user)):
    claim = await get_claim(id, game)
    await record(claim, {"note": data.note.strip(), "link": data.link.strip()}, actor=user.email)
    return claim.api()


@router.delete("/{id}")
async def delete_claim(id: PydanticObjectId, game: Game = Depends(my_game), user: User = Depends(active_user)):
    claim = await get_claim(id, game)
    await record_delete(claim, actor=user.email)
    return {"ok": True}
