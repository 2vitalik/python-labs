from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from deps import admin_user, current_user
from models.game import Game
from models.history import record, record_new
from models.user import Status, User
from zones import KLASSES, STATUSES

router = APIRouter(prefix="/api/games")


class GameIn(BaseModel):
    slug: str
    title: str
    icon: str = ""
    klass: str = ""
    axes: dict = {}
    summary: str = ""
    description: str = ""
    status: str = "draft"
    order: int = 0


def clean(data: GameIn) -> dict:
    d = data.model_dump()
    d["slug"], d["title"] = d["slug"].strip().lower(), d["title"].strip()
    if not d["slug"] or not d["title"]:
        raise HTTPException(422, "Slug і назва — обовʼязкові.")
    if d["klass"] and d["klass"] not in KLASSES:
        raise HTTPException(422, "Невідомий клас гри.")
    if d["status"] not in STATUSES:
        raise HTTPException(422, "Невідомий статус.")
    return d


@router.get("")
async def list_games(user: User | None = Depends(current_user)):
    games = await Game.find_all().sort("order", "slug").to_list()
    if not user or user.status != Status.admin:  # guests see the catalog too, active only
        games = [g for g in games if g.status == "active"]
    return [g.api() for g in games]


@router.post("")
async def create_game(data: GameIn, admin: User = Depends(admin_user)):
    d = clean(data)
    if await Game.find_one(Game.slug == d["slug"]):
        raise HTTPException(422, "Гра з таким slug уже існує.")
    game = Game(**d)
    await game.insert()
    await record_new(game, actor=admin.email)
    return game.api()


@router.put("/{id}")
async def update_game(id: PydanticObjectId, data: GameIn, admin: User = Depends(admin_user)):
    game = await Game.get(id)
    if not game:
        raise HTTPException(404)
    d = clean(data)
    other = await Game.find_one(Game.slug == d["slug"])
    if other and other.id != game.id:
        raise HTTPException(422, "Гра з таким slug уже існує.")
    await record(game, d, actor=admin.email)
    return game.api()
