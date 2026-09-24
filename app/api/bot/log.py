"""Message log (T129): everything the bot receives → `messages`; outgoing ones are caught by notify.outgoing()."""
from datetime import datetime, timezone

from aiogram import Router
from aiogram.types import BusinessMessagesDeleted, Message

from models.message import TgMessage
from models.user import User

router = Router()


def media_id(message: Message) -> str:
    m = message.photo[-1] if message.photo else (message.document or message.video or message.voice or message.audio
                                                 or message.sticker or message.video_note or message.animation)
    return m.file_id if m else ""


async def email(tg_id: int | None) -> str:
    user = await User.find_one(User.tg_chat_id == tg_id) if tg_id else None
    return user.email if user else ""


async def save(message: Message, dir: str, kind: str = "") -> None:
    sender = message.from_user if dir == "in" else None  # outgoing: the sender is the bot itself
    await TgMessage(dir=dir, chat_id=message.chat.id, chat_type=message.chat.type,
                    thread_id=message.message_thread_id if message.is_topic_message else None,
                    from_id=sender.id if sender else None, username=(sender.username if sender else None) or "",
                    user=await email(sender.id if sender else message.chat.id),
                    text=message.text or message.caption or "", content_type=message.content_type,
                    file_id=media_id(message), message_id=message.message_id, kind=kind,
                    at=datetime.fromtimestamp(message.edit_date, timezone.utc) if message.edit_date else message.date).insert()


async def incoming(handler, message: Message, data):
    """dp.message outer middleware: runs before every router, so unhandled messages are logged too."""
    await save(message, "in")
    return await handler(message, data)


@router.edited_message()
@router.edited_business_message()
async def edited(message: Message):
    await save(message, "in", kind="edit")


@router.deleted_business_messages()
async def deleted(event: BusinessMessagesDeleted):
    """Only Chat Automation chats report deletions; groups never do."""
    await TgMessage.insert_many([TgMessage(dir="in", chat_id=event.chat.id, chat_type=event.chat.type, message_id=m, kind="deleted")
                                 for m in event.message_ids])
