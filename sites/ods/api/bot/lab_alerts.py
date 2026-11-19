"""Alerts about labs, kind `lab`: a student handed in an answer line or a notebook."""
from aiogram import html

from core.bot import notify
from core.bot.alerts import event
from core.models.user import User
from models.lab import LabVariant


async def checked(user: User, v: LabVariant) -> None:
    """🟢 every answer is right · 🟠 some are not yet. A test student is the teacher trying the page: no news."""
    if user.test:
        return
    ok = v.right()
    rows = [f"📨 рядок відповідей: {ok} із {len(v.answers)} ✅ · спроба {v.attempts}", f"🎴 варіант {html.quote(v.vid)}"]
    if v.notebook:
        rows.append(f'📓 <a href="{html.quote(v.notebook)}">ноутбук</a>')
    await notify.send("lab", event(0 if ok == len(v.answers) else 1, f"Лаба {v.lab}", user, rows), user.email)


def got(pair, word: str) -> str:
    return f"{word} {'?' if pair[0] is None else pair[0]}/{pair[1]}" if pair and pair[1] else ""


async def uploaded(user: User, v: LabVariant) -> None:
    """📎 ноутбук: 13/13 ✅ · графіків 3/3 · висновків 4/4 · ★ 1 · підказка 16 — what the site read off the file."""
    if user.test:
        return
    ok, c, hint = v.right(), v.facts.get("count") or {}, v.grade()["hint"]
    stars = (c.get("stars") or [None])[0]
    parts = [f"{ok}/{len(v.answers)} ✅" if v.attempts else "без рядка відповідей", got(c.get("plots"), "графіків"),
             got(c.get("conclusions"), "висновків"), f"★ {stars}" if stars else "", f"підказка {hint}" if hint else ""]
    rows = [f"📎 ноутбук: {' · '.join(p for p in parts if p)}", f"🎴 варіант {html.quote(v.vid)} · версія {v.files}"]
    await notify.send("lab", event(0 if ok == len(v.answers) else 1, f"Лаба {v.lab}", user, rows), user.email)
