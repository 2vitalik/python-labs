"""One feed over every journal (T146): site footprint, edits, Telegram, alerts, errors, notes — newest first."""
from datetime import datetime

from bson.codec_options import CodecOptions

from bot.notify import KINDS
from config import settings
from db import mongo
from models.user import User

# feed source → its collection, its rows there, the field with the person's email
SOURCES = {
    "login": ("activity", {"kind": "login"}, "user"),
    "view": ("activity", {"kind": "view"}, "user"),
    "api": ("activity", {"kind": "api"}, "user"),
    "fail": ("activity", {"kind": "api", "status": {"$gte": 400}}, "user"),  # the part of `api` worth seeing unasked
    "edit": ("history", {}, "actor"),
    "tg": ("messages", {"kind": {"$nin": list(KINDS)}}, "user"),  # sent alerts are in `events` already
    "event": ("events", {}, "user"),
    "error": ("errors", {}, "user"),
    "note": ("notes", {}, "user"),
}
FIELDS = {
    "login": ("ua", "ip"),
    "view": ("path", "ua", "ip"),
    "api": ("method", "path", "status", "ms", "ua", "ip"),
    "fail": ("method", "path", "status", "ms", "ua", "ip"),
    "edit": ("coll", "note"),
    "tg": ("dir", "kind", "chat_type", "thread_id", "from_id", "username", "text", "content_type"),
    "event": ("kind", "text", "sent"),
    "error": ("source", "title", "trace", "method", "path", "where", "ua", "ip"),
    "note": ("text", "by", "hidden", "source", "tg_id"),
}
AWARE = CodecOptions(tz_aware=True)  # Mongo returns UTC without a zone, and the browser would read that as local time


def journal(name: str):
    return mongo[settings.db_name].get_collection(name, codec_options=AWARE)


def brief(value) -> str:
    return "" if value is None else str(value)[:200]


def about(src: str, person: User) -> dict:
    """One person's rows: their own, plus edits of their profile by others and both sides of their Telegram chat."""
    if src == "edit":
        return {"$or": [{"actor": person.email}, {"coll": "users", "doc_id": person.id}]}
    if src == "tg" and person.tg_chat_id:
        return {"$or": [{"user": person.email}, {"chat_id": person.tg_chat_id}]}
    return {"user": person.email}


def row(src: str, doc: dict) -> dict:
    out = {"id": str(doc["_id"]), "src": src, "at": doc["at"], "user": doc.get(SOURCES[src][2], "")}
    out |= {k: doc.get(k) for k in FIELDS[src]}
    if src == "edit":
        out["doc"] = str(doc["doc_id"])
        out["changes"] = [{"field": k, "old": brief(v.get("old")), "new": brief(v.get("new"))} for k, v in doc["changes"].items()]
    return out


async def feed(sources: list[str], person: User | None, hide: list[str], before: datetime | None, limit: int) -> list[dict]:
    """`hide` — emails to leave out (the staff); one person's feed hides nobody."""
    rows = []
    for src in sources:
        name, own, who = SOURCES[src]
        query = [own, about(src, person) if person else {who: {"$nin": hide}}]
        if before:
            query.append({"at": {"$lt": before}})
        async for doc in journal(name).find({"$and": query}, {"raw": 0}).sort("at", -1).limit(limit):
            rows.append(row(src, doc))
    return sorted(rows, key=lambda r: (r["at"], r["id"]), reverse=True)[:limit]  # ids grow with time: same moment — later written first
