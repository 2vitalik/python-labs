from beanie import PydanticObjectId
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel

from bot import game_alerts
from core.deps import active_user, admin_user
from core.models.history import record, record_delete, record_new
from core.models.user import Status, User
from models.ref import Ref
from refs_clean import RefIn, clean

router = APIRouter(prefix="/api/refs")
STATUSES = ("inbox", "linked", "dropped")  # нове · взято · ні


class VerdictIn(BaseModel):
    status: str
    reply: str = ""


async def own_ref(id: PydanticObjectId, user: User) -> Ref:
    ref = await Ref.get(id)
    if not ref:
        raise HTTPException(404)
    if ref.author != user.email and user.status != Status.admin:
        raise HTTPException(403)
    return ref


def out(ref: Ref, user: User) -> dict:
    return ref.api() | {"mine": ref.author == user.email}


@router.get("")
async def list_refs(user: User = Depends(active_user)):
    return [out(r, user) for r in await Ref.find_all().sort("-created_at").to_list()]


@router.post("")
async def create_ref(data: RefIn, tasks: BackgroundTasks, user: User = Depends(active_user)):
    ref = Ref(author=user.email, **await clean(data))
    await ref.insert()
    await record_new(ref, actor=user.email)
    if ref.kind != "link":  # an idea, a word on a card or on the site — the teacher's to sort (T274 §4)
        tasks.add_task(game_alerts.idea, user, ref)
    return out(ref, user)


@router.put("/{id}")
async def update_ref(id: PydanticObjectId, data: RefIn, user: User = Depends(active_user)):
    ref = await own_ref(id, user)
    await record(ref, await clean(data), actor=user.email)
    return out(ref, user)


@router.put("/{id}/verdict")
async def judge_ref(id: PydanticObjectId, data: VerdictIn, admin: User = Depends(admin_user)):
    """The teacher's word with a line the author sees on the page; no alert to the author (T274 §13)."""
    ref = await Ref.get(id)
    if not ref:
        raise HTTPException(404)
    if data.status not in STATUSES:
        raise HTTPException(422, "Стан — нове, взято або ні")
    await record(ref, {"status": data.status, "reply": data.reply.strip()}, actor=admin.email)
    return out(ref, admin)


@router.delete("/{id}")
async def delete_ref(id: PydanticObjectId, user: User = Depends(active_user)):
    ref = await own_ref(id, user)
    await record_delete(ref, actor=user.email)
    return {"ok": True}
