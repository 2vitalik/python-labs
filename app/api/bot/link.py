from models.history import record
from models.user import User


async def bind(token: str, chat_id: int, username: str) -> User | None:
    """T58: /start <tg_token> → remember chat_id + real @username; unknown token → None."""
    user = await User.find_one(User.tg_token == token) if token else None
    if not user:
        return None
    await record(user, {"tg_chat_id": chat_id, "tg_username": username}, actor="tgbot")
    return user


async def sync(chat_id: int, username: str) -> None:
    """Mirror @username from every message of a linked chat: it can change or vanish any time (T107)."""
    user = await User.find_one(User.tg_chat_id == chat_id)
    if user:
        await record(user, {"tg_username": username}, actor="tgbot")
