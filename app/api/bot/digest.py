"""Daily onboarding digest (T113): per group, how many still lack ПІБ / GitHub / bot — kind `digest`, 09:00 Kyiv."""
import asyncio
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from aiogram import html

from bot import notify
from models.user import Status, User

TZ = ZoneInfo("Europe/Kyiv")
HOUR = 9
GAPS = (
    ("🪪", lambda u: not (u.last_name and u.first_name)),
    ("🐙", lambda u: not u.github),
    ("🤖", lambda u: u.tg_chat_id is None),
)


async def text() -> str | None:
    """None when every student is complete — then nothing is sent."""
    students = await User.find(User.status == Status.student).to_list()
    groups: dict[str, list[User]] = {}
    for s in students:
        groups.setdefault(s.group or "без групи", []).append(s)
    rows = []
    for name, members in sorted(groups.items()):
        gaps = [f"{mark} {n}" for mark, miss in GAPS if (n := sum(1 for u in members if miss(u)))]
        if gaps:
            rows.append(f"👥 {html.quote(name)} · " + " · ".join(gaps))
    if not rows:
        return None
    return "\n".join([f"📊 Профілі не заповнені · студентів: {len(students)}", *rows, "☝️ 🪪 ПІБ · 🐙 GitHub · 🤖 бот"])


def seconds_until(hour: int) -> float:
    now = datetime.now(TZ)
    at = now.replace(hour=hour, minute=0, second=0, microsecond=0)
    if at <= now:
        at += timedelta(days=1)
    return (at - now).total_seconds()


async def loop() -> None:
    while True:
        await asyncio.sleep(seconds_until(HOUR))
        if t := await text():
            await notify.send("digest", t)
