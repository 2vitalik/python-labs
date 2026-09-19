from models.history import record
from models.user import User


async def bind(token: str, chat_id: int, username: str) -> User | None:
    """T58: /start <tg_token> → remember chat_id (+ real @username); unknown token → None."""
    user = await User.find_one(User.tg_token == token) if token else None
    if not user:
        return None
    data = {"tg_chat_id": chat_id}
    if username:  # no @username in Telegram → keep what the student typed
        data["tg_username"] = username
    await record(user, data, actor="tgbot")
    return user
