"""Telegram rows written before the chat was linked carry a Telegram id and no email (T150):
the person is found when the row is read, by `users.tg_chat_id`; the journals stay as written."""
from core.models.user import User

# feed source → filters for the rows of Telegram ids `ids`; `tg` mirrors how bot/log.py picks the person
BY_TG = {
    "tg": lambda ids: [{"from_id": {"$in": ids}}, {"dir": "out", "chat_id": {"$in": ids}}],
    "note": lambda ids: [{"tg_id": {"$in": ids}}],
    "vote": lambda ids: [{"tg_id": {"$in": ids}}],
}


def links(users: list[User]) -> dict[int, str]:
    return {u.tg_chat_id: u.email for u in users if u.tg_chat_id}


def tg_id(doc: dict) -> int | None:
    """A note's student or a voter, the sender of an incoming message, the chat of an outgoing one."""
    return doc.get("tg_id") or doc.get("from_id") or (doc.get("chat_id") if doc.get("dir") == "out" else None)


def unlinked(src: str, emails: list[str], link: dict[int, str]) -> list[dict]:
    """Mongo filters: rows of these people that have no email in them."""
    ids = [tg for tg, email in link.items() if email in emails]
    return [{"user": ""} | f for f in BY_TG[src](ids)] if src in BY_TG and ids else []
