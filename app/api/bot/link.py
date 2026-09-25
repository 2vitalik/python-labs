from datetime import datetime, timezone

from bot import alerts
from models.history import record
from models.user import User


async def by_token(token: str) -> User | None:
    """T58: student behind /start <tg_token>; an empty token must never match anyone."""
    return await User.find_one(User.tg_token == token) if token else None


async def bind(user: User, chat_id: int, username: str) -> None:
    """Remember chat_id + real @username; a repeat /start from another chat re-links (T58)."""
    if user.tg_chat_id != chat_id:
        user.tg_linked_at = datetime.now(timezone.utc)  # saved along by record(): chat_id differs, so there is a diff
    await alerts.profile(user, await record(user, {"tg_chat_id": chat_id, "tg_username": username}, actor="tgbot"))


async def sync(chat_id: int, username: str) -> User | None:
    """Mirror @username from every message of a linked chat: it can change or vanish any time (T107)."""
    user = await User.find_one(User.tg_chat_id == chat_id)
    if user:
        await alerts.profile(user, await record(user, {"tg_username": username}, actor="tgbot"))
    return user
