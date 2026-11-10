"""The etalon's sandbox (T274 §7): the user's own copy of a base game's reference description, poured like the etalon into
a Game of `sandbox_owner()`; «Моя гра»'s routes work over it under `X-Sandbox: <slug>` (routes/my_game.py)."""
import asyncio
from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException

import templates
from core.deps import active_user
from core.models.history import Change
from core.models.user import Status, User
from models.base_game import BaseGame
from models.game import Claim, Game, Part
from models.rule import Rule
from passport import passport
from routes.my_game import sandbox_owner

router = APIRouter(prefix="/api/games")
locks = defaultdict(asyncio.Lock)  # a double click would pour twice


@router.post("/{slug}/sandbox")
async def reset_sandbox(slug: str, user: User = Depends(active_user)):
    """A clean copy of the etalon `slug`, whatever the old copy held or was based on."""
    t = templates.load(slug)
    if not t:
        raise HTTPException(404, "Еталона для цієї основи ще нема.")
    me = User(email=sandbox_owner(user.email), status=Status.student, test=True)  # pours what a student gets: active cards
    base = await BaseGame.find_one(BaseGame.slug == slug)
    async with locks[me.email]:
        if old := await Game.find_one(Game.owner == me.email):
            for model in (Part, Claim, Rule):
                await model.find(model.game == old.id).delete()
            await old.delete()
        game = await Game(owner=me.email, title=base.title if base else slug, base_game=slug).insert()
        await templates.pour(game, me, t)
        await Change.find(Change.actor == me.email).delete()
    return await passport(game)


@router.get("/{slug}/sandbox")
async def get_sandbox(slug: str, user: User = Depends(active_user)):
    game = await Game.find_one(Game.owner == sandbox_owner(user.email))
    if not game or game.base_game != slug:
        raise HTTPException(404, "Пісочницю не відкрито.")
    return await passport(game)
