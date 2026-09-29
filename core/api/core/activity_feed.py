"""One feed over every journal (T146): site footprint, edits, Telegram, alerts, errors, notes — newest first."""
from datetime import datetime

from bson.codec_options import CodecOptions

from core.activity_link import tg_id, unlinked
from core.bot.notify import KINDS
from core.config import settings
from core.db import mongo
from core.models.user import User

# feed source → its collection, its rows there, the field with the person's email
SOURCES = {
    "login": ("activity", {"kind": "login"}, "user"),
    "view": ("activity", {"kind": "view"}, "user"),
    "api": ("activity", {"kind": "api"}, "user"),
    "fail": ("activity", {"kind": "api", "status": {"$gte": 400}}, "user"),  # the part of `api` worth seeing unasked
    "edit": ("history", {}, "actor"),
    "tg": ("messages", {}, "user"),  # without the sent alerts — own()
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


def own(src: str) -> dict:
    """The source's rows in its collection. Sent alerts are in `events` already; their kinds are counted here, not at import:
    a site adds its own."""
    return {"kind": {"$nin": list(KINDS)}} if src == "tg" else SOURCES[src][1]


def brief(value) -> str:
    return "" if value is None else str(value)[:200]


def about(src: str, person: User, link: dict[int, str]) -> dict:
    """One person's rows: their own, plus edits of their profile by others and both sides of their Telegram chat."""
    if src == "edit":
        return {"$or": [{"actor": person.email}, {"coll": "users", "doc_id": person.id}]}
    chat = [{"chat_id": person.tg_chat_id}] if src == "tg" and person.tg_chat_id else []
    return {"$or": [{"user": person.email}, *chat, *unlinked(src, [person.email], link)]}


def others(src: str, hide: list[str], link: dict[int, str]) -> dict:
    late = unlinked(src, hide, link)
    return {SOURCES[src][2]: {"$nin": hide}} | ({"$nor": late} if late else {})


def row(src: str, doc: dict, link: dict[int, str]) -> dict:
    out = {"id": str(doc["_id"]), "src": src, "at": doc["at"], "user": doc.get(SOURCES[src][2]) or link.get(tg_id(doc), "")}
    out |= {k: doc.get(k) for k in FIELDS[src]}
    if src == "edit":
        out["doc"] = str(doc["doc_id"])
        out["changes"] = [{"field": k, "old": brief(v.get("old")), "new": brief(v.get("new"))} for k, v in doc["changes"].items()]
    return out


async def feed(sources: list[str], person: User | None, hide: list[str], link: dict[int, str], before: datetime | None,
               limit: int) -> list[dict]:
    """`hide` — emails to leave out (the staff); one person's feed hides nobody. `link` — Telegram id → email, as linked now."""
    rows = []
    for src in sources:
        query = [own(src), about(src, person, link) if person else others(src, hide, link)]
        if before:
            query.append({"at": {"$lt": before}})
        async for doc in journal(SOURCES[src][0]).find({"$and": query}, {"raw": 0}).sort("at", -1).limit(limit):
            rows.append(row(src, doc, link))
    return sorted(rows, key=lambda r: (r["at"], r["id"]), reverse=True)[:limit]  # ids grow with time: same moment — later written first
