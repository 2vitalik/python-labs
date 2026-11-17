"""Defenses as parts of a lesson's day (T333): the teacher sees every defense of the date on the lessons pages, a student —
own ones, once they are sent. Read only: the defense's own pages are /defenses/<id> and /my/remarks (T327)."""
from collections import defaultdict
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from core.config import settings
from core.lesson_view import SITE_PARTS
from core.models.user import User
from models.defense import Defense


def clock(at: datetime) -> tuple[str, str]:
    """Mongo's UTC → the date and «HH:MM» of the classes' clock."""
    local = at.replace(tzinfo=timezone.utc).astimezone(ZoneInfo(settings.tz))
    return local.strftime("%Y-%m-%d"), local.strftime("%H:%M")


async def parts(user: User, admin: bool) -> dict[str, list[dict]]:
    mine = {} if admin else {"student": user.email, "sent_at": {"$ne": None}}
    found = await Defense.find({"started_at": {"$ne": None}} | mine).sort("started_at").to_list()
    owners = {u.email: u for u in await User.find({"email": {"$in": [d.student for d in found]}}).to_list()}
    out = defaultdict(list)
    for d in found:
        date, start = clock(d.started_at)
        out[date].append({"key": f"d-{d.id}", "kind": "def", "title": "лаби " + ", ".join(map(str, d.labs)) if d.labs else "",
                          "start": start, "end": clock(d.ended_at)[1] if d.ended_at else "", "note": "", "private": True,
                          "links": [{"label": "Запис", "url": d.link}] if d.link else [], "result": d.result, "mode": d.kind,
                          "people": [owners[d.student].person()] if d.student in owners else [],
                          "to": f"/defenses/{d.id}" if admin else "/my/remarks"})
    return out


SITE_PARTS.append(parts)
