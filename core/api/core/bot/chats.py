"""Where polls can go (T174): every group and forum topic the bot hears in, and whether the bot is still there.
Both are outer middlewares: a failure here is logged and never stops the message on its way."""
import logging
from datetime import datetime, timezone

from aiogram.types import ChatMemberUpdated, Message

from core.models.vote import TgChat

GROUPS = ("group", "supergroup")
logger = logging.getLogger(__name__)


def topic_name(message: Message) -> str:
    """Only service messages carry a topic's name; every plain message in a topic replies to the one that created it."""
    for m in (message, message.reply_to_message):
        topic = m and (m.forum_topic_created or m.forum_topic_edited)
        if topic and topic.name:
            return topic.name
    return ""


async def note(chat_id: int, thread_id: int | None, fields: dict) -> None:
    """Upsert one place; the admin's name and choice (`name`, `hidden`) stay as they are."""
    fresh = {"name": "", "hidden": False} | ({} if "topic" in fields else {"topic": ""})
    await TgChat.get_pymongo_collection().update_one(
        {"chat_id": chat_id, "thread_id": thread_id},
        {"$set": fields | {"left": False, "seen_at": datetime.now(timezone.utc)}, "$setOnInsert": fresh}, upsert=True)


async def seen(handler, message: Message, data):
    """dp.message outer middleware: groups only — a guest mention comes from a chat the bot is not in."""
    try:
        if message.chat.type in GROUPS:
            topic = {"topic": name} if (name := topic_name(message)) else {}
            await note(message.chat.id, message.message_thread_id if message.is_topic_message else None,
                       {"title": message.chat.title or "", "type": message.chat.type} | topic)
    except Exception:  # noqa: BLE001 — the message log matters more than the list of places
        logger.exception("chat not noted")
    return await handler(message, data)


async def joined(handler, event: ChatMemberUpdated, data):
    """dp.my_chat_member outer middleware: the bot added to a group, or thrown out of it."""
    try:
        if event.chat.type in GROUPS:
            if event.new_chat_member.status in ("left", "kicked"):
                await TgChat.find(TgChat.chat_id == event.chat.id).set({TgChat.left: True})
            else:
                await note(event.chat.id, None, {"title": event.chat.title or "", "type": event.chat.type})
    except Exception:  # noqa: BLE001
        logger.exception("chat status not noted")
    return await handler(event, data)
