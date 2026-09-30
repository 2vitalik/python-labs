"""Who is active and how much (T146): per person — counts by source over the period and a bar per day for the last two weeks."""
from collections import Counter
from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo

from core.activity_feed import SOURCES, journal
from core.activity_link import links
from core.models.user import Status, User

TZ = ZoneInfo("Europe/Kyiv")  # a day is the teacher's day, not UTC's
SPARK = 14
# what people do themselves; of Telegram — only what they wrote, not the bot's replies
COUNTED = {k: SOURCES[k] for k in ("login", "view", "api", "edit", "vote")} | {"tg": ("messages", {"dir": "in"}, "user")}


def last_days(n: int) -> list[str]:
    today = datetime.now(TZ).date()
    return [(today - timedelta(days=i)).isoformat() for i in range(n - 1, -1, -1)]


def aware(at: datetime | None) -> datetime | None:
    return at.replace(tzinfo=timezone.utc) if at else None


async def tally(days: int, link: dict[int, str]) -> dict[str, dict]:
    """email → n: rows per source over `days` (0 = all time) · days: rows per day · last: the newest row."""
    period = set(last_days(days))
    span = last_days(max(days, SPARK))[0] if days else None
    match = {"at": {"$gte": datetime.combine(date.fromisoformat(span), time(), TZ)}} if span else {}
    day = {"$dateToString": {"format": "%Y-%m-%d", "date": "$at", "timezone": TZ.key}}
    out = {}
    for src, (name, own, who) in COUNTED.items():
        # the Telegram id — messages and votes only: whose they are when written before the chat was linked (T150)
        tg = {"$ifNull": ["$from_id", "$tg_id"]}
        group = {"_id": {"who": f"${who}", "tg": tg, "day": day}, "n": {"$sum": 1}, "last": {"$max": "$at"}}
        async for g in await journal(name).aggregate([{"$match": own | match}, {"$group": group}]):
            email = g["_id"]["who"] or link.get(g["_id"].get("tg"), "")
            p = out.setdefault(email, {"n": Counter(), "days": Counter(), "last": g["last"]})
            if not days or g["_id"]["day"] in period:
                p["n"][src] += g["n"]
            if src != "api":  # a page view is one action; the API calls behind it are not three more
                p["days"][g["_id"]["day"]] += g["n"]
            p["last"] = max(p["last"], g["last"])
    return out


async def people(days: int, staff: bool) -> dict:
    """Everyone who has ever shown up, the most recent first; `total` — how far the students are with signing in."""
    users = await User.find_all().to_list()
    found, spark = await tally(days, links(users)), last_days(SPARK)
    rows = []
    for u in users:
        t = found.get(u.email)
        if (t or u.first_seen_at) and (staff or u.status != Status.admin):
            rows.append(u.person() | {"tg_linked": u.tg_chat_id is not None, "last": t["last"] if t else aware(u.last_seen_at or u.first_seen_at),
                                     "n": dict(t["n"]) if t else {}, "days": [t["days"][d] if t else 0 for d in spark]})
    students = [u for u in users if u.status == Status.student and not u.test]
    return {"rows": sorted(rows, key=lambda r: r["last"], reverse=True), "spark": spark,
            "total": {"students": len(students), "seen": sum(1 for u in students if u.first_seen_at),
                      "linked": sum(1 for u in students if u.tg_chat_id is not None)}}
