from collections import Counter

from fastapi import APIRouter, Depends, HTTPException

from core.deps import editor_user, viewer
from core.models.user import User
from models.ludo_game import LudoGame

router = APIRouter(prefix="/api/ludopedia")
# the corpus is reference material for the teacher while it is v1: the list and the texts — admin and agents;
# «where this mechanic lives» (Д3 on a card) and tag counts — open, like the catalog itself


@router.get("")
async def list_games(user: User = Depends(editor_user)):
    return [g.brief() for g in await LudoGame.find_all().sort("family", "title").to_list()]


@router.get("/stats")
async def stats(user: User = Depends(editor_user)):
    games = await LudoGame.find_all().to_list()
    tags = Counter(t for g in games for t in g.mechanics)
    return {
        "total": len(games), "families": dict(Counter(g.family for g in games).most_common()),
        "klass": dict(Counter(g.klass for g in games).most_common()), "stage": dict(Counter(g.stage for g in games).most_common()),
        "coverage": round(sum(g.coverage for g in games) / len(games)) if games else 0,
        "rules": sum(len(g.rules) for g in games), "entities": sum(len(g.entities) for g in games),
        "tags": len(tags), "new_tags": sum(1 for t in tags if t.startswith("+")),
    }


@router.get("/mechanics")
async def mechanics(user: User | None = Depends(viewer)):
    """tag → how many games carry it; `+tag` is a mechanic the catalog has no card for yet."""
    return dict(Counter(t for g in await LudoGame.find_all().to_list() for t in g.mechanics).most_common())


@router.get("/by-card/{slug}")
async def by_card(slug: str, user: User | None = Depends(viewer)):
    """Games of the corpus where this catalog card is at work — the seed of «Як це буває в іграх» (Д3)."""
    games = await LudoGame.find({"mechanics": {"$in": [slug, f"+{slug}"]}}).sort("title").to_list()
    return [{"slug": g.slug, "title": g.title, "family": g.family, "year": g.year, "klass": g.klass, "url": g.best} for g in games]


@router.get("/{slug}")
async def game(slug: str, user: User = Depends(editor_user)):
    g = await LudoGame.find_one(LudoGame.slug == slug)
    if not g:
        raise HTTPException(404)
    return g.api()
