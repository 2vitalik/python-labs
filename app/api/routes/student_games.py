from fastapi import APIRouter, Depends, HTTPException

from deps import active_user
from models.game import Claim, Game, Part
from models.rule import Rule
from models.task import Task
from models.user import Status, User

router = APIRouter(prefix="/api/students")


async def task_index(slugs: set[str]) -> dict:
    """Minimal card info for rendering claims/parts, drafts included (viewer may not see them in the catalog)."""
    tasks = await Task.find({"slug": {"$in": list(slugs)}}).to_list()
    return {t.slug: {"title": t.title, "coin": t.coin, "amount": t.amount, "slots": t.slots,
                     "zone": t.zone, "subzone": t.subzone, "status": t.status} for t in tasks}


def person(u: User) -> dict:
    full = " ".join(x for x in (u.last_name, u.first_name) if x)
    return {"nick": u.nick, "name": full or u.name, "group": u.group,
            "picture": u.picture, "status": u.status}


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


@router.get("")
async def list_students(user: User = Depends(active_user)):
    """Gallery for everyone active; admin extras let the same page host the admin table."""
    users = await User.find_all().sort("group", "last_name").to_list()
    if user.status != Status.admin:
        users = [u for u in users if u.status != Status.pending]
    games = {g.owner: g for g in await Game.find_all().to_list()}
    out = []
    for u in users:
        row = person(u) | {"game": await game_summary(games.get(u.email))}
        if user.status == Status.admin:
            row |= {"email": u.email, "github": u.github,
                    "tg_username": u.tg_username, "tg_linked": u.tg_chat_id is not None}
        out.append(row)
    return out


@router.get("/{nick}/game")
async def student_game(nick: str, user: User = Depends(active_user)):
    owner = await User.by_nick(nick)
    game = owner and await Game.find_one(Game.owner == owner.email)
    if not game:
        raise HTTPException(404, "Гра не знайдена.")
    parts = await Part.find(Part.game == game.id).sort("order", "created_at").to_list()
    claims = await Claim.find(Claim.game == game.id).sort("created_at").to_list()
    rules = await Rule.find(Rule.game == game.id).sort("created_at").to_list()
    slugs = {p.task for p in parts if p.task} | {c.task for c in claims} | \
            {i["task"] for p in parts for i in p.items if i.get("task")}
    return {
        "game": game.api(), "student": person(owner),
        "parts": [p.api() for p in parts], "claims": [c.api() for c in claims],
        "rules": [r.api() for r in rules],
        "tasks": await task_index(slugs), "mine": game.owner == user.email,
    }
