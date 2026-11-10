from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

import templates
from core.models.user import User
from models.game import Game
from routes.my_game import author, in_sandbox, my_game

router = APIRouter()


class TemplateIn(BaseModel):
    slug: str = ""  # a base game's slug; empty = the game's own base


@router.get("/api/templates")
async def list_templates():
    """Which base games have a reference description, with counts — for the «Почати з еталона» button."""
    return templates.all_summaries()


@router.post("/api/my/game/template")
async def apply_template(data: TemplateIn, game: Game = Depends(my_game), user: User = Depends(author)):
    if in_sandbox(user):
        raise HTTPException(403, "Пісочниця — вже копія зразка: щоб почати наново, натисни «Скинути».")
    return await templates.apply(game, user, data.slug or game.base_game)
