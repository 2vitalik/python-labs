from fastapi import APIRouter, Depends, HTTPException

from core.deps import active_user
from core.models.user import User
from core.routes import students
from models.game import Claim, Game, Part
from models.rule import Rule
from models.task import Task

router = APIRouter(prefix="/api/students")


async def task_index(slugs: set[str]) -> dict:
    """Minimal card info for rendering claims/parts, drafts included (viewer may not see them in the catalog)."""
    tasks = await Task.find({"slug": {"$in": list(slugs)}}).to_list()
    return {t.slug: {"title": t.title, "coin": t.coin, "amount": t.amount, "slots": t.slots,
                     "zone": t.zone, "subzone": t.subzone, "status": t.status} for t in tasks}


async def game_summary(game: Game | None) -> dict:
    if not game:
        return {}
    parts = await Part.find(Part.game == game.id).sort("order", "created_at").to_list()
    shots = [s for p in parts for s in p.screenshots]
    return game.api() | {
        "windows": sum(p.kind == "window" for p in parts), "menus": sum(p.kind == "menu" for p in parts),
        "entities": sum(p.kind == "entity" for p in parts),
        "claims": await Claim.find(Claim.game == game.id).count(),
        "rules": await Rule.find(Rule.game == game.id).count(),
        "cover": f"/api/uploads/{game.id}/{shots[0]}" if shots else "",
    }


async def games(users: list[User]) -> dict:
    """Every row of the students' list carries the student's game."""
    found = {g.owner: g for g in await Game.find_all().to_list()}
    return {u.email: {"game": await game_summary(found.get(u.email))} for u in users}


students.EXTRAS.append(games)


@router.get("/{nick}/game")
async def student_game(nick: str, user: User = Depends(active_user)):
    owner = await User.by_nick(nick)
    if not owner:
        raise HTTPException(404)
    game = await Game.find_one(Game.owner == owner.email)
    if not game:
        return {"student": owner.person(), "game": None}  # the student is there, the game is yet to come
    parts = await Part.find(Part.game == game.id).sort("order", "created_at").to_list()
    claims = await Claim.find(Claim.game == game.id).sort("created_at").to_list()
    rules = await Rule.find(Rule.game == game.id).sort("created_at").to_list()
    slugs = {p.task for p in parts if p.task} | {c.task for c in claims} | \
            {i["task"] for p in parts for i in p.items if i.get("task")}
    return {
        "game": game.api(), "student": owner.person(),
        "parts": [p.api() for p in parts], "claims": [c.api() for c in claims],
        "rules": [r.api() for r in rules],
        "tasks": await task_index(slugs), "mine": game.owner == user.email,
    }
