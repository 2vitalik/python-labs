from beanie import PydanticObjectId
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException

from core.deps import admin_user
from core.models.history import record, record_delete, record_new
from core.models.poll import Poll
from core.models.poll_send import PollSend
from core.models.user import User
from core.polls_in import PollIn, clean
from core.polls_read import summary
from core.polls_send import close
from core.polls_view import results

router = APIRouter(prefix="/api/polls")
FROZEN = ("question", "options", "multiple")  # what Telegram already shows once the poll is sent


async def get_poll(id: PydanticObjectId) -> Poll:
    poll = await Poll.get(id)
    if not poll:
        raise HTTPException(404)
    return poll


@router.get("")
async def list_polls(tag: str = "", admin: User = Depends(admin_user)):
    polls = await Poll.find({"tags": tag} if tag else {}).sort("-created_at").to_list()
    lines = await summary(polls)
    tags = await Poll.get_pymongo_collection().distinct("tags")
    return {"polls": [p.api() | lines[str(p.id)] for p in polls], "tags": sorted(tags, key=str.lower)}


@router.post("")
async def create_poll(data: PollIn, admin: User = Depends(admin_user)):
    """A draft: sending is a step of its own, so a failed send never takes what was typed with it."""
    template = PydanticObjectId(data.template) if ObjectId.is_valid(data.template) else None
    poll = Poll(**clean(data), template=template, by=admin.email)
    await poll.insert()
    await record_new(poll, actor=admin.email)
    return poll.api()


@router.put("/{id}")
async def update_poll(id: PydanticObjectId, data: PollIn, admin: User = Depends(admin_user)):
    poll = await get_poll(id)
    fields = clean(data)
    if poll.status != "draft":
        if any(getattr(poll, k) != fields[k] for k in FROZEN):
            raise HTTPException(409, "Опитування вже в Telegram — питання й варіанти там не змінити. «Повторити» створить нове з правками")
        fields = {k: fields[k] for k in ("title", "tags")}
    await record(poll, fields, actor=admin.email)
    return poll.api()


@router.delete("/{id}")
async def delete_poll(id: PydanticObjectId, admin: User = Depends(admin_user)):
    """A draft, or a poll only teachers have tried: students' answers are never deleted. Their votes stay in `votes` anyway."""
    poll = await get_poll(id)
    if not (await results(poll))["can_delete"]:
        raise HTTPException(409, "Тут уже є голоси студентів — видалити не можна, лише закрити")
    if poll.status == "open":
        await close(poll)  # a try left open in a chat would keep taking votes nobody sees
    await PollSend.find(PollSend.poll == poll.id).delete()
    await record_delete(poll, actor=admin.email)
    return {"ok": True}
