"""Alerts about labs, kind `lab`: a student handed in an answer line."""
from aiogram import html

from core.bot import notify
from core.bot.alerts import event
from core.models.user import User
from models.lab import LabVariant


async def checked(user: User, v: LabVariant) -> None:
    """🟢 every answer is right · 🟠 some are not yet."""
    ok = sum(x["ok"] for x in v.verdict.values())
    rows = [f"📨 рядок відповідей: {ok} із {len(v.answers)} ✅ · спроба {v.attempts}", f"🎴 варіант {html.quote(v.vid)}"]
    if v.notebook:
        rows.append(f'📓 <a href="{html.quote(v.notebook)}">ноутбук</a>')
    await notify.send("lab", event(0 if ok == len(v.answers) else 1, f"Лаба {v.lab}", user, rows), user.email)
