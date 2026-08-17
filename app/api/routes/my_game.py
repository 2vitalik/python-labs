from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from deps import active_user
from models.base_game import BaseGame
from models.game import Game
from models.history import record, record_new
from models.user import User

router = APIRouter(prefix="/api/my/game")


class GameIn(BaseModel):
    title: str
    base_game: str = ""
    base_custom: str = ""
    description: str = ""


async def my_game(user: User = Depends(active_user)) -> Game:
    game = await Game.find_one(Game.owner == user.email)
    if not game:
        raise HTTPException(404, "Спершу створи свою гру.")
    return game


async def clean(data: GameIn) -> dict:
    d = data.model_dump()
    d["title"] = d["title"].strip()
    if not d["title"]:
        raise HTTPException(422, "Назва — обовʼязкова.")
    if d["base_game"]:
        if not await BaseGame.find_one(BaseGame.slug == d["base_game"]):
            raise HTTPException(422, "Немає такої гри-основи в каталозі.")
    elif not d["base_custom"].strip():
        raise HTTPException(422, "Обери гру-основу з каталогу або опиши свою.")
    return d


@router.get("")
async def get_my_game(user: User = Depends(active_user)):
    game = await Game.find_one(Game.owner == user.email)
    return game.api() if game else None


@router.post("")
async def create_game(data: GameIn, user: User = Depends(active_user)):
    if await Game.find_one(Game.owner == user.email):
        raise HTTPException(409, "Гра вже створена — вона в тебе одна.")
    game = Game(owner=user.email, **await clean(data))
    await game.insert()
    await record_new(game, actor=user.email)
    return game.api()


@router.put("")
async def update_game(data: GameIn, game: Game = Depends(my_game), user: User = Depends(active_user)):
    await record(game, await clean(data), actor=user.email)
    return game.api()
