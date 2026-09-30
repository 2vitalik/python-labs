from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from core.deps import admin_user
from core.models.user import User
from core.models.vote import TgChat

router = APIRouter(prefix="/api/polls/chats")


class ChatIn(BaseModel):
    name: str | None = None
    hidden: bool | None = None


@router.get("")
async def list_chats(admin: User = Depends(admin_user)):
    """Every place the bot has heard in; `me` — the admin's own chat with the bot, to try a poll there first (None — not linked)."""
    chats = sorted(await TgChat.find_all().to_list(), key=lambda c: (c.title.lower(), c.thread_id is not None, c.where.lower()))
    return {"chats": [c.api() for c in chats], "me": admin.tg_chat_id}


@router.put("/{id}")
async def update_chat(id: PydanticObjectId, data: ChatIn, admin: User = Depends(admin_user)):
    chat = await TgChat.get(id)
    if not chat:
        raise HTTPException(404)
    fields = data.model_dump(exclude_none=True)
    if "name" in fields:
        fields["name"] = " ".join(fields["name"].split())
    if fields:
        await chat.set(fields)
    return chat.api()
