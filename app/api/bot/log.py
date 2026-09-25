"""Message log (T129): everything the bot receives → `messages`; outgoing ones are caught by notify.outgoing()."""
from datetime import datetime, timezone

from aiogram import Router
from aiogram.types import BusinessMessagesDeleted, ChatJoinRequest, ChatMemberUpdated, Message, MessageReactionUpdated, ReactionType
from aiogram.types import User as TgUser

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
    await TgMessage(dir=dir, chat_id=message.chat.id, chat_type="business" if message.business_connection_id else message.chat.type,
                    thread_id=message.message_thread_id if message.is_topic_message else None,
                    from_id=sender.id if sender else None, username=(sender.username if sender else None) or "",
                    user=await email(sender.id if sender else message.chat.id),
                    text=message.text or message.caption or "", content_type=message.content_type,
                    file_id=media_id(message), message_id=message.message_id, kind=kind, raw=dump(message) if dir == "in" else {},
                    at=datetime.fromtimestamp(message.edit_date, timezone.utc) if message.edit_date else message.date).insert()


def dump(event) -> dict:
    return event.model_dump(mode="json", exclude_none=True)


async def event_row(event, who: TgUser | None, **fields) -> None:
    """Non-message updates share the journal: the affected user is the sender, the whole update goes to `raw`."""
    await TgMessage(dir="in", chat_id=event.chat.id, chat_type=event.chat.type, from_id=who.id if who else None,
                    username=(who.username if who else None) or "", user=await email(who.id) if who else "", at=event.date,
                    raw=dump(event), **fields).insert()


def emoji(r: ReactionType) -> str:
    return r.emoji if r.type == "emoji" else f"custom:{r.custom_emoji_id}" if r.type == "custom_emoji" else "⭐"


async def incoming(handler, message: Message, data):
    """dp.message outer middleware: runs before every router, so unhandled messages are logged too."""
    await save(message, "in")
    return await handler(message, data)


@router.edited_message()
@router.edited_business_message()
async def edited(message: Message):
    await save(message, "in", kind="edit")


@router.chat_member()
@router.my_chat_member()
async def member(event: ChatMemberUpdated):
    """Joins, leaves, kicks, promotions in the forum (admin bots get them for everyone); my_chat_member — the bot's own status."""
    new = event.new_chat_member
    via = f" · {event.invite_link.name or event.invite_link.invite_link}" if event.invite_link else ""
    by = f" · by {event.from_user.id}" if event.from_user.id != new.user.id else ""
    await event_row(event, new.user, text=f"{event.old_chat_member.status.value} → {new.status.value}{via}{by}", content_type="chat_member",
                    kind="member")


@router.chat_join_request()
async def join_request(event: ChatJoinRequest):
    await event_row(event, event.from_user, text=event.bio or "", content_type="join_request", kind="member")


@router.message_reaction()
async def reaction(event: MessageReactionUpdated):
    """Who reacted with what; empty text = reaction removed; anonymous admins react as actor_chat."""
    await event_row(event, event.user, message_id=event.message_id, text=" ".join(map(emoji, event.new_reaction)), content_type="reaction",
                    kind="reaction")


@router.deleted_business_messages()
async def deleted(event: BusinessMessagesDeleted):
    """Only Chat Automation chats report deletions; groups never do."""
    await TgMessage.insert_many([TgMessage(dir="in", chat_id=event.chat.id, chat_type="business", message_id=m, kind="deleted")
                                 for m in event.message_ids])
