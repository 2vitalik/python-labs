"""Alert: a student has marked their week (T177) — once, as «Готово» is pressed."""
from aiogram import html

from core.bot import notify
from core.bot.alerts import who
from core.config import settings
from core.models.user import User
from core.models.week import Mark, Week
from core.week_marks import EMOJI, by_reason, spans

REASONS = 12  # lines of reasons shown: a week of any length still fits a Telegram message


def lines(marks: list[Mark]) -> list[str]:
    """🔴 — a line per reason, 🟡 and 🟢 — a line each; nothing marked means any time."""
    out = [f"🔴 {html.quote(why or '?')}: {spans(ms)}" for why, ms in by_reason(marks).items()][:REASONS]
    out += [f"{EMOJI[kind]} {spans(ms)}" for kind in ("meh", "ok") if (ms := [m for m in marks if m.kind == kind])]
    return out or ["✅ може будь-коли"]


async def done(user: User, week: Week) -> None:
    head = f'🗓 <a href="{settings.site_url}/week">Тиждень</a> · {who(user)}'
    comment = [f"💬 {html.quote(week.comment[:300])}"] if week.comment else []
    await notify.send("week", "\n".join([head, *lines(week.marks), *comment]), user.email)
