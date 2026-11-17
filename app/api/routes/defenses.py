"""Defenses (T327): the teacher's list, a defense's page, its time, impressions and result. An agent with a token reads
the list and a page without the teacher's own fields; everything that changes a defense is the teacher's."""
from datetime import datetime, timezone

from beanie import PydanticObjectId
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request
from pydantic import BaseModel

import defense_vocab as V
import defenses
from bot import defense_alerts
from core.config import settings
from core.deps import admin_user, agent, editor_user
from core.models.history import record, record_delete, record_new
from core.models.user import User
from models.defense import Defense, Remark, now
from models.game import Game

router = APIRouter(prefix="/api/defenses")


class NewIn(BaseModel):
    nick: str
    labs: list[int] = []
    kind: str = "online"


class PatchIn(BaseModel):
    """The fields sent are the fields set."""
    labs: list[int] | None = None
    kind: str | None = None
    started_at: datetime | None = None
    ended_at: datetime | None = None
    facts: dict | None = None
    rates: dict | None = None
    marks: list[str] | None = None
    note: str | None = None
    result: str | None = None
    rank: float | None = None
    link: str | None = None


def reader(request: Request) -> str:
    return "agent" if agent(request) else "teacher"


def naive(at: datetime) -> datetime:
    return at.astimezone(timezone.utc).replace(tzinfo=None) if at.tzinfo else at


def clean(patch: dict) -> dict:
    """What a defense may hold, or 422 in words."""
    labs = patch.get("labs") or []
    ok = (all(1 <= n <= settings.labs for n in labs) and patch.get("kind", "online") in V.KINDS and patch.get("result", "") in ("", *V.RESULTS)
          and set(patch.get("marks") or []) <= V.MARKS.keys()
          and all(k in V.FACTS and v in V.ANSWERS for k, v in (patch.get("facts") or {}).items())
          and all(k in V.RATES and v in (1, 1.5, 2, 2.5, 3, 3.5, 4) for k, v in (patch.get("rates") or {}).items()))
    if not ok:
        raise HTTPException(422, "Такого значення в захисті нема.")
    for key in ("started_at", "ended_at"):
        if patch.get(key):
            patch[key] = naive(patch[key])
    return patch | ({"labs": sorted(set(labs))} if "labs" in patch else {}) | ({"scale": V.SCALE} if "rates" in patch else {})


async def get(id: PydanticObjectId) -> Defense:
    if d := await Defense.get(id):
        return d
    raise HTTPException(404)


@router.get("/vocab")
async def get_vocab(user: User = Depends(editor_user)):
    return V.vocab() | {"coins": settings.remark_coins, "labs": settings.labs}


@router.get("")
async def get_list(request: Request, nick: str = "", user: User = Depends(editor_user)):
    """The newest first; `nick` — one student's."""
    owner = await User.by_nick(nick) if nick else None
    docs = await Defense.find({"student": owner.email} if owner else {"_id": None} if nick else {}).sort("-created_at").to_list()
    people = {u.email: u for u in await User.find({"email": {"$in": list({d.student for d in docs})}}).to_list()}
    by = {}
    for r in await Remark.find({"defense": {"$in": [d.id for d in docs]}}).to_list():
        by.setdefault(r.defense, []).append(r)
    return [defenses.defense(d, people.get(d.student), by.get(d.id, []), reader(request)) for d in docs]


@router.post("")
async def post_defense(data: NewIn, admin: User = Depends(admin_user)):
    """A new defense starts now."""
    owner = await User.by_nick(data.nick)
    if not owner:
        raise HTTPException(404, "Такого студента нема.")
    patch = clean({"labs": data.labs, "kind": data.kind})
    d = Defense(student=owner.email, by=admin.email, started_at=now(), scale=V.SCALE, **patch)
    await d.insert()
    await record_new(d, actor=admin.email)
    return defenses.defense(d, owner, [])


@router.get("/{id}")
async def get_defense(id: PydanticObjectId, request: Request, user: User = Depends(editor_user)):
    """The page: the defense, its remarks, the student's game and other defenses, what is owed from them."""
    d, who = await get(id), reader(request)
    owner = await User.find_one(User.email == d.student)
    remarks = await Remark.find(Remark.defense == d.id).sort("order", "created_at").to_list()
    game = await Game.find_one(Game.owner == d.student)
    repo = owner.github if owner else ""
    return defenses.defense(d, owner, remarks, who) | {
        "remarks": [defenses.remark(r, who, repo) for r in remarks], "game": game.title if game else "",
        "others": [defenses.defense(o, owner, [], "agent") for o in await defenses.of_student(d.student, d.id)],
        "debts": [defenses.remark(r, who, repo) for r in await defenses.debts(d.student, d.id)],
    }


@router.put("/{id}")
async def put_defense(id: PydanticObjectId, data: PatchIn, admin: User = Depends(admin_user)):
    d = await get(id)
    patch = clean(data.model_dump(exclude_unset=True))
    start, end = patch.get("started_at", d.started_at), patch.get("ended_at", d.ended_at)
    if start and end and end < start:
        raise HTTPException(422, "Кінець раніше за початок.")
    await record(d, patch, actor=admin.email)
    return defenses.defense(d, await User.find_one(User.email == d.student), await Remark.find(Remark.defense == d.id).to_list())


@router.post("/{id}/send")
async def send(id: PydanticObjectId, tasks: BackgroundTasks, admin: User = Depends(admin_user)):
    """The student gets the result and every remark that is still a draft; a later send — the ones added since."""
    d = await get(id)
    drafts = await Remark.find(Remark.defense == d.id, Remark.state == "draft").to_list()
    for r in drafts:
        await record(r, {"state": "open"}, actor=admin.email)
    await record(d, {"sent_at": now()} | ({} if d.ended_at else {"ended_at": now()}), actor=admin.email)
    if owner := await User.find_one(User.email == d.student):
        tasks.add_task(defense_alerts.sent, owner, d, len(drafts))
    return {"sent": len(drafts)}


@router.delete("/{id}", status_code=204)
async def delete_defense(id: PydanticObjectId, admin: User = Depends(admin_user)):
    d = await get(id)
    if d.sent_at:
        raise HTTPException(422, "Захист уже надіслано студентові — його не видалити.")
    for r in await Remark.find(Remark.defense == d.id).to_list():
        await record_delete(r, actor=admin.email)
    await record_delete(d, actor=admin.email)
