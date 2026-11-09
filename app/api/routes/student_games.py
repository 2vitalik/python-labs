from beanie import PydanticObjectId
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel

from bot import game_alerts
from core.deps import active_user, admin_user
from core.models.history import record
from core.models.user import User
from core.routes import students
from models.game import CLAIM_STATUSES, Claim, Game, Part
from models.rule import Rule
from models.task import Task

router = APIRouter(prefix="/api/students")


async def task_index(slugs: set[str]) -> dict:
    """Minimal card info for rendering claims/parts, drafts included (viewer may not see them in the catalog)."""
    tasks = await Task.find({"slug": {"$in": list(slugs)}}).to_list()
    return {t.slug: {"title": t.title, "coin": t.coin, "amount": t.amount, "slots": t.slots, "tags": t.tags,
                     "zone": t.zone, "subzone": t.subzone, "status": t.status} for t in tasks}


def coins_of(claims: list[Claim], tasks: list[Task]) -> dict:
    """What the claims are worth by kind of coin, claimed and accepted apart (T240; informational until grading)."""
    worth = {t.slug: (t.coin, t.amount) for t in tasks}
    out: dict[str, dict] = {"claimed": {}, "accepted": {}}
    for c in claims:
        coin, amount = worth.get(c.task, ("", 0))
        if not coin:
            continue
        out["claimed"][coin] = out["claimed"].get(coin, 0) + amount
        if c.status == "accepted":
            out["accepted"][coin] = out["accepted"].get(coin, 0) + amount
    return out


async def game_summary(game: Game | None) -> dict:
    if not game:
        return {}
    parts = await Part.find(Part.game == game.id).sort("order", "created_at").to_list()
    shots = [s for p in parts for s in p.screenshots]
    claims = await Claim.find(Claim.game == game.id).to_list()
    tasks = await Task.find({"slug": {"$in": list({c.task for c in claims})}}).to_list()
    coins = coins_of(claims, tasks)
    return game.api() | {
        "windows": sum(p.kind == "window" for p in parts), "menus": sum(p.kind == "menu" for p in parts),
        "entities": sum(p.kind == "entity" for p in parts), "field": any(p.kind == "field" for p in parts),
        "claims": len(claims), "accepted": sum(c.status == "accepted" for c in claims),
        "coins": coins["claimed"], "coins_accepted": coins["accepted"],
        "rules": await Rule.find(Rule.game == game.id).count(),
        "cover": f"/api/uploads/{game.id}/{shots[0]}" if shots else "",
    }


async def games(users: list[User]) -> dict:
    """Every row of the students' list carries the student's game."""
    found = {g.owner: g for g in await Game.find_all().to_list()}
    return {u.email: {"game": await game_summary(found.get(u.email))} for u in users}


students.EXTRAS.append(games)


async def visible_owner(nick: str, user: User) -> User:
    owner = await User.by_nick(nick)
    if not owner or not students.can_see(user, owner):  # whom the list hides, the page hides too
        raise HTTPException(404)
    return owner


@router.get("/{nick}/game")
async def student_game(nick: str, user: User = Depends(active_user)):
    owner = await visible_owner(nick, user)
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


class VerdictIn(BaseModel):
    status: str = "claimed"
    verdict: str = ""


@router.put("/{nick}/claims/{id}")
async def judge_claim(nick: str, id: PydanticObjectId, data: VerdictIn, tasks: BackgroundTasks,
                      admin: User = Depends(admin_user)):
    """The teacher's word on a claim: зараховано / повернуто (with a line why) / back to заявлено."""
    owner = await User.by_nick(nick)
    game = owner and await Game.find_one(Game.owner == owner.email)
    claim = game and await Claim.get(id)
    if not claim or claim.game != game.id:
        raise HTTPException(404)
    if data.status not in CLAIM_STATUSES:
        raise HTTPException(422, "Статус заявки — заявлено, зараховано або повернуто.")
    if changes := await record(claim, {"status": data.status, "verdict": data.verdict.strip()}, actor=admin.email):
        tasks.add_task(game_alerts.verdict, owner, claim, changes)
    return claim.api()
