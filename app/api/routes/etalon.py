"""A base game's reference description as a described game (T270): the passport of a real Game owned by `<slug>@etalon`,
poured from data/catalog/templates/<slug>.yaml when first asked and again once the file is newer than the pour (Game.poured).
Nobody's game: no user has such an email, so the gallery, the table and «Моя гра» never meet it; the pour leaves no history."""
import asyncio

from fastapi import APIRouter, HTTPException

import templates
from core.models.history import Change
from core.models.user import Status, User
from models.base_game import BaseGame
from models.game import Claim, Game, Part
from models.rule import Rule
from passport import passport

router = APIRouter(prefix="/api/games")
lock = asyncio.Lock()  # two first visitors at once would pour twice


async def etalon(slug: str) -> Game:
    path = templates.DIR / f"{slug}.yaml"
    if not slug or not path.is_file():
        raise HTTPException(404, "Еталона для цієї основи ще нема.")
    author = User(email=f"{slug}@etalon", status=Status.student)  # pours what a student would get: active cards
    async with lock:
        mtime = path.stat().st_mtime
        game = await Game.find_one(Game.owner == author.email)
        if game and game.poured >= mtime:
            return game
        if game:
            for model in (Part, Claim, Rule):
                await model.find(model.game == game.id).delete()
        else:
            base = await BaseGame.find_one(BaseGame.slug == slug)
            game = await Game(owner=author.email, title=base.title if base else slug, base_game=slug).insert()
        await templates.pour(game, author, templates.load(slug))
        await Change.find(Change.actor == author.email).delete()
        await game.set({Game.poured: mtime})
    return game


@router.get("/{slug}/etalon")
async def get_etalon(slug: str):
    """Open to anyone, a guest too: the same shape as a student's game, without the student."""
    return await passport(await etalon(slug))
