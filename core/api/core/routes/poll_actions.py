from beanie import PydanticObjectId
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from core.deps import admin_user
from core.models.history import record_new
from core.models.poll import PollTemplate
from core.models.poll_send import PollSend
from core.models.user import User
from core.models.vote import TgChat
from core.polls_send import close, send, stuck
from core.polls_view import results
from core.routes.polls import get_poll

router = APIRouter(prefix="/api/polls")


class SendIn(BaseModel):
    targets: list[str] = []  # TgChat ids; `me` — the admin's own chat with the bot, to try a poll first
    silent: bool = False


async def place(target: str, admin: User) -> tuple[int, int | None, str]:
    if target == "me":
        if not admin.tg_chat_id:
            raise HTTPException(409, "У тебе не привʼязаний бот — привʼяжи його в профілі")
        return admin.tg_chat_id, None, f"особисто · {admin.first_name or admin.name or admin.nick}"
    chat = await TgChat.get(target) if ObjectId.is_valid(target) else None
    if not chat:
        raise HTTPException(404, "Такого місця бот не знає")
    if chat.left:
        raise HTTPException(409, f"Бота вже нема в «{chat.where}»")
    return chat.chat_id, chat.thread_id, chat.where


@router.post("/{id}/send")
async def send_poll(id: PydanticObjectId, data: SendIn, admin: User = Depends(admin_user)):
    """Every place is checked before the first message goes, so a bad one never leaves half of them sent."""
    poll = await get_poll(id)
    if poll.status == "closed":
        raise HTTPException(409, "Опитування закрите — «Повторити» створить нове")
    if not data.targets:
        raise HTTPException(422, "Обери, куди надіслати")
    places = [await place(t, admin) for t in dict.fromkeys(data.targets)]
    sends = {(s.chat_id, s.thread_id): s for s in await PollSend.find(PollSend.poll == poll.id).to_list()}
    out = []
    for chat_id, thread_id, where in places:
        s = sends.get((chat_id, thread_id))
        if s and not stuck(s):
            continue  # it is there already: a second click must not post it twice
        s = s or PollSend(poll=poll.id, chat_id=chat_id, thread_id=thread_id, by=admin.email)
        s.where, s.silent = where, data.silent
        out.append(await send(poll, s))
    return {"sends": [s.api() for s in out]}


@router.post("/{id}/sends/{sid}/retry")
async def retry_send(id: PydanticObjectId, sid: PydanticObjectId, admin: User = Depends(admin_user)):
    poll = await get_poll(id)
    s = await PollSend.get(sid)
    if not s or s.poll != poll.id:
        raise HTTPException(404)
    if poll.status == "closed" or not stuck(s):
        raise HTTPException(409, "Тут опитування вже є — повторювати нема чого")
    return (await send(poll, s)).api()


@router.post("/{id}/close")
async def close_poll(id: PydanticObjectId, admin: User = Depends(admin_user)):
    poll = await get_poll(id)
    if poll.status == "draft":
        raise HTTPException(409, "Чернетку ще нікуди не надіслано")
    await close(poll)
    return await results(poll)


@router.post("/{id}/template")
async def to_template(id: PydanticObjectId, admin: User = Depends(admin_user)):
    """A poll that turned out to be a regular one becomes a template."""
    poll = await get_poll(id)
    template = PollTemplate(title=poll.title, question=poll.question, options=poll.options, multiple=poll.multiple, tags=poll.tags,
                            by=admin.email)
    await template.insert()
    await record_new(template, actor=admin.email)
    return template.api()
