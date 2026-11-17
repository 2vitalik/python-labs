from beanie import PydanticObjectId
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel

import videos
from bot import game_alerts
from core.deps import active_user, admin_user
from core.models.history import record
from core.models.user import User
from core.routes import students
from grading import wood
from models.game import CLAIM_STATUSES, Claim, Game, Part
from models.rule import Rule
from models.task import Task
from passport import coins_of, passport

router = APIRouter(prefix="/api/students")


async def game_summary(game: Game | None) -> dict:
    if not game:
        return {}
    parts = await Part.find(Part.game == game.id).sort("order", "created_at").to_list()
    shots = [s for p in parts for s in p.screenshots]
    claims = await Claim.find(Claim.game == game.id).to_list()
    tasks = await Task.find({"slug": {"$in": list({c.task for c in claims})}}).to_list()
    coins, asked = coins_of(claims, tasks), {t.slug for t in tasks if not t.core}
    return game.api() | {
        "windows": sum(p.kind == "window" for p in parts), "menus": sum(p.kind == "menu" for p in parts),
        "entities": sum(p.kind == "entity" for p in parts), "levels": sum(p.kind == "level" for p in parts),
        "field": any(p.kind == "field" for p in parts),
        "claims": len(claims), "accepted": sum(c.status == "accepted" for c in claims),
        "coins": coins["claimed"], "coins_accepted": coins["accepted"],
        "wood_claimed": wood(coins["claimed"]), "wood_accepted": wood(coins["accepted"]),
        "waiting": sum(c.status == "claimed" and not c.auto for c in claims) + await videos.waiting(game),  # the teacher's word is due
        "asked": sum(c.task in asked and c.status != "accepted" for c in claims),  # on cards outside the core (T319)
        "rules": await Rule.find(Rule.game == game.id).count(),
        "cover": f"/api/uploads/{game.id}/{shots[0]}" if shots else "",
        "videos": (await videos.summary([game])).get(game.id, {}),  # the demos and defenses handed in (T318)
    }


async def games(users: list[User]) -> dict:
    """Every row of the students' list carries the student's game."""
    found = {g.owner: g for g in await Game.find({"owner": {"$in": [u.email for u in users]}}).to_list()}
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
    p = await passport(game)
    return p | {"student": owner.person(), "mine": game.owner == user.email, "videos": await videos.rows(game, owner, p["claims"], p["tasks"])}


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
    await judge(claim, owner, {"status": data.status, "verdict": data.verdict.strip()}, admin.email, tasks)
    return claim.api()


async def judge(claim: Claim, owner: User, patch: dict, actor: str, tasks: BackgroundTasks) -> None:
    """The teacher's word on a claim (its status, the line, a request moved to another card — routes/asks.py): the student hears it."""
    if patch.get("status", claim.status) not in CLAIM_STATUSES:
        raise HTTPException(422, "Статус заявки — заявлено, зараховано або повернуто.")
    if changes := await record(claim, patch, actor=actor):
        tasks.add_task(game_alerts.verdict, owner, claim, changes)
