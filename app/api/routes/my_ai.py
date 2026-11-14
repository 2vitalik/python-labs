"""«Описати словами» in «Моя гра» (T289, T291 §14, AI-CONTRACT §4): the student's text → proposals; adding and rejecting them."""
from typing import Literal

from beanie import PydanticObjectId
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel

from ai import apply, limits
from ai.describe import describe
from core.models.user import User
from models.draft import Draft
from models.game import Game
from routes.my_game import author, my_game

router = APIRouter(prefix="/api/my/game/ai")


class TextIn(BaseModel):
    text: str = ""


class KeysIn(BaseModel):
    keys: list[str] = []


class StateIn(KeysIn):
    state: Literal["rejected", "open"]


async def get_draft(id: PydanticObjectId, game: Game) -> Draft:
    draft = await Draft.get(id)
    if not draft or draft.game != game.id:
        raise HTTPException(404)
    return draft


@router.get("")
async def get_ai(game: Game = Depends(my_game), user: User = Depends(author)):
    """The switch and the limits; the game's drafts, newest first."""
    drafts = await Draft.find(Draft.game == game.id).sort("-created_at").to_list()
    return await limits.state(user) | {"drafts": [d.api() for d in drafts]}


@router.post("")
async def post_text(data: TextIn, tasks: BackgroundTasks, game: Game = Depends(my_game), user: User = Depends(author)):
    text = data.text.strip()
    await limits.check(user, text)
    async with limits.alone(user.email):
        return await describe(game, user, text, tasks)


@router.post("/{id}/apply")
async def apply_items(id: PydanticObjectId, data: KeysIn, game: Game = Depends(my_game), user: User = Depends(author)):
    return await apply.apply(await get_draft(id, game), game, user, data.keys)


@router.post("/{id}/state")
async def set_state(id: PydanticObjectId, data: StateIn, game: Game = Depends(my_game)):
    """Reject or bring back: what is added or in the game already stays as it is."""
    draft = await get_draft(id, game)
    for it in draft.items:
        if it["key"] in data.keys and it["state"] in ("open", "rejected") and it["group"] != "unknown":
            it["state"] = data.state
    await draft.save()
    return draft.api()
