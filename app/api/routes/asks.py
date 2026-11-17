"""Requests (T319): claims on active cards outside the core, by card — the teacher's page «Запити» and an agent's `bin/catalog asks`.
The teacher answers one with a line, accepts or returns it, or moves it to another card of the same kind."""
from beanie import PydanticObjectId
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel

from claims_clean import clean_params
from core.deps import editor_user
from core.models.user import User
from game_log_names import PARTS
from models.game import Claim, Game, Part
from models.rule import Rule
from models.task import Task
from models.vocab import sentence
from routes.my_claims import check_unique
from routes.student_games import judge
from zones import KINDS, kind_of

router = APIRouter(prefix="/api/asks")
FAKE = ("@etalon", "@sandbox")  # games nobody asks in: a base game's etalon, someone's sandbox
CARD = ("slug", "title", "icon", "zone", "subzone", "kind", "coin", "amount", "description")
ROW = ("task", "why", "auto", "params", "note", "link", "shots", "status", "verdict", "created_at")


class AskIn(BaseModel):
    verdict: str | None = None  # None — as it is
    status: str | None = None
    task: str | None = None  # the card to move the claim to


def where(c: Claim, parts: dict, rules: dict) -> str:
    """The claim's place in the game, in words; "" — the game itself."""
    if p := parts.get(c.part):
        return "поле" if p.kind == "field" else f"{PARTS.get(p.kind, 'обʼєкт')} «{p.title}»"
    if r := rules.get(c.rule):
        return f"правило «{sentence(r, lambda pid: parts[pid].title if pid in parts else '?')}»"
    return "правило" if c.rule else ""


async def rows(claims: list[Claim]) -> list[dict]:
    """The claims of students' games as the page shows them; an etalon's or a sandbox's are left out."""
    games = {g.id: g for g in await Game.find({"_id": {"$in": list({c.game for c in claims})}}).to_list() if not g.owner.endswith(FAKE)}
    owners = {u.email: u for u in await User.find({"email": {"$in": [g.owner for g in games.values()]}}).to_list()}
    parts = {str(p.id): p for p in await Part.find({"game": {"$in": list(games)}}).to_list()}
    rules = {str(r.id): r for r in await Rule.find({"game": {"$in": list(games)}}).to_list()}
    out = []
    for c in claims:
        if (g := games.get(c.game)) and (u := owners.get(g.owner)):
            out.append({"id": str(c.id), "nick": u.nick, "name": u.person()["name"] or u.nick, "game": g.title, "test": u.test,
                        "where": where(c, parts, rules), "anchor": f"c-{c.id}"} | {k: v for k, v in c.api().items() if k in ROW})
    return out


@router.get("")
async def asks(user: User = Depends(editor_user)):
    """By card, the most asked first: a card counts the students' games that ask for it, a test student's not."""
    cards = {t.slug: t for t in await Task.find({"status": "active", "core": {"$ne": True}}).to_list()}
    claims = await Claim.find({"task": {"$in": list(cards)}, "status": {"$ne": "accepted"}}).sort("created_at").to_list()
    by = {}
    for r in await rows(claims):
        by.setdefault(r["task"], []).append(r)
    out = [{"task": {k: v for k, v in cards[slug].api().items() if k in CARD}, "games": len({r["nick"] for r in rs if not r["test"]}),
            "claims": rs} for slug, rs in by.items()]
    return sorted(out, key=lambda g: (-g["games"], g["task"]["title"]))


async def moved(claim: Claim, card: Task, game: Game, slug: str) -> dict:
    """To another active card of the same kind: what the student asked for may be in the catalog already."""
    if claim.auto:
        raise HTTPException(422, "Цю заявку тримає сам опис (тип, параметр, властивість) — її не перенести.")
    new = await Task.find_one(Task.slug == slug, Task.status == "active")
    if not new or kind_of(new) != kind_of(card):
        raise HTTPException(422, f"Перенести можна лише на активну картку того самого типу — {KINDS[kind_of(card)]}.")
    await check_unique(game, slug, claim.part, claim.rule, new, me=claim)
    keys = {s["key"] for s in new.slots}
    return {"task": slug, "params": clean_params(new, {k: v for k, v in claim.params.items() if k in keys}, loose=True)}


@router.put("/{id}")
async def answer(id: PydanticObjectId, data: AskIn, tasks: BackgroundTasks, user: User = Depends(editor_user)):
    claim = await Claim.get(id)
    card = claim and await Task.find_one(Task.slug == claim.task)
    game = card and not card.core and await Game.get(claim.game)
    owner = game and not game.owner.endswith(FAKE) and await User.find_one(User.email == game.owner)
    if not owner:
        raise HTTPException(404, "Такого запиту нема.")
    patch = {} if data.status is None else {"status": data.status}
    if data.verdict is not None:
        patch["verdict"] = data.verdict.strip()
    if data.task not in (None, claim.task):
        patch |= await moved(claim, card, game, data.task)
    await judge(claim, owner, patch, user.email, tasks)
    return (await rows([claim]))[0]
