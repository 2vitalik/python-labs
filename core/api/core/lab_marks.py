"""The teacher's word on a lab (T235): set from the site or the bot, recorded, told to the admins; the dates the bot takes."""
import re
from datetime import datetime, time, timezone
from zoneinfo import ZoneInfo

from aiogram import html

from core.bot import notify
from core.bot.alerts import who
from core.labs import naive, utc
from core.models.deadline import LabMark
from core.models.history import record, record_new
from core.models.user import User

TZ = ZoneInfo("Europe/Kyiv")
END = time(23, 59)  # the day's deadline, when only a date is given
DATE = re.compile(r"^(\d{1,2})\.(\d{1,2})(?:\.(\d{2}|\d{4}))?$")
FIELDS = ("until", "open", "reason", "met", "note")
MET = {True: "✅ вклався — слово викладача", False: "❌ не вклався — слово викладача", None: "↩️ вердикт — як рахує сайт"}


def parse_due(text: str, today: datetime | None = None) -> datetime | None:
    """«5.11», «05.11.2026», «5.11.26», «2026-11-05», «2026-11-05 18:35» → that moment in Kyiv, the day's end when no time."""
    today = today or datetime.now(TZ)
    try:
        if m := DATE.match(text):
            year = int(m[3]) if m[3] else today.year
            day = datetime(year + 2000 if year < 100 else year, int(m[2]), int(m[1]))
        else:
            day = datetime.fromisoformat(text)
    except ValueError:
        return None
    at = day if day.time() != time(0, 0) else datetime.combine(day.date(), END)
    return at.replace(tzinfo=TZ).astimezone(timezone.utc)


def kyiv(d: datetime | str) -> str:
    d = datetime.fromisoformat(d) if isinstance(d, str) else d
    return utc(d).astimezone(TZ).strftime("%-d.%m %H:%M")


def lines(mark: LabMark, changed: set[str]) -> list[str]:
    """What changed, a row each, in the T109 style."""
    out = []
    if changed & {"until", "open"}:
        out.append(f"⏳ до {kyiv(mark.until)}" if mark.until else "⏳ подовжено, дата поки невідома" if mark.open else "✖️ подовження знято")
    if "reason" in changed and mark.reason:
        out.append(f"💬 {html.quote(mark.reason)}")
    if "met" in changed:
        out.append(MET[mark.met])
    if "note" in changed and mark.note:
        out.append(f"📝 {html.quote(mark.note)}")
    return out


async def set_mark(student: User, lab: int, data: dict, actor: str) -> tuple[LabMark, set[str]]:
    """Upsert the pair's document with the fields `data` names; a history row and an alert `due` when something changed."""
    patch = {k: v for k, v in data.items() if k in FIELDS}
    if "until" in patch:
        patch["until"] = naive(patch["until"])
        if patch["until"]:
            patch["open"] = False  # a date closes the open-ended extension
    mark = await LabMark.find_one(LabMark.user == student.email, LabMark.lab == lab)
    now = datetime.now(timezone.utc)
    if mark:
        changed = set((await record(mark, patch | {"by": actor, "at": now}, actor)) if any(getattr(mark, k) != v for k, v in patch.items()) else {})
    else:
        mark = await LabMark(user=student.email, lab=lab, **patch, by=actor, at=now).insert()
        await record_new(mark, actor)
        changed = {k for k, v in patch.items() if v not in (None, "", False)}
    changed &= set(FIELDS)
    if changed:
        await notify.send("due", "\n".join([f"📅 Лаба {lab} · {who(student, '/edit')}", *lines(mark, changed)]), student.email)
    return mark, changed
