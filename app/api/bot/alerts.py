"""Alerts about people (T111, T113) in the T109 style: header = the worst change, one line per changed field."""
from aiogram import html

from bot import notify
from config import settings
from models.user import Status, User

NAMES = ("last_name", "first_name", "patronymic")
MARK = ("🟢", "🟠", "🔴")  # filled · replaced · deleted
BOT = ("привʼязано", "інший Telegram", "відвʼязано")


def who(user: User, page: str = "") -> str:
    name = f"{user.last_name} {user.first_name}".strip() or user.name or user.nick
    link = f'<b><a href="{settings.site_url}/students/{user.nick}{page}">{html.quote(name)}</a></b>'
    return f"{link} · {user.group}" if user.group else link


def level(old, new) -> int:
    return 0 if not old else 2 if not new else 1


def arrow(lvl: int, old, new, fmt=html.quote) -> str:
    return fmt(new) if lvl == 0 else f"{fmt(old)} → {fmt(new) if new else '✖️'}"


def event(lvl: int, subject: str, user: User, rows: list[str]) -> str:
    return "\n".join([f"{MARK[lvl]} {subject} · {who(user)}", *rows])


def gh(url: str) -> str:
    return f'<a href="{url}">{html.quote(url.removeprefix("https://"))}</a>'


def tg(nick: str) -> str:
    return f'<a href="https://t.me/{nick}">@{html.quote(nick)}</a>'


def rows(user: User, changes: dict) -> list[tuple[str, int, str]]:
    """(label, level, text) per changed field; the three name fields collapse into one ПІБ row."""
    old = {k: v["old"] for k, v in changes.items()}
    fio = lambda parts: " ".join(p for p in parts if p)  # noqa: E731
    out = []
    if old.keys() & NAMES:
        lvl = max(level(old[k], getattr(user, k)) for k in NAMES if k in old)
        was, now = fio(old.get(k, getattr(user, k)) for k in NAMES), fio(getattr(user, k) for k in NAMES)
        out.append(("🪪 ПІБ", lvl, arrow(lvl, was, now)))
    for key, label, fmt in (("github", "🐙 GitHub", gh), ("tg_username", "✈️ Telegram", tg)):
        if key in old:
            lvl = level(old[key], getattr(user, key))
            out.append((label, lvl, arrow(lvl, old[key], getattr(user, key), fmt)))
    if "tg_chat_id" in old:
        lvl = level(old["tg_chat_id"], user.tg_chat_id)
        out.append(("🤖 Бот", lvl, BOT[lvl]))
    return out


async def profile(user: User, changes: dict) -> None:
    """One alert per save: 🟢 goes to kind `fill`, 🟠/🔴 — to `change`."""
    if not (out := rows(user, changes)):
        return
    lvl = max(r[1] for r in out)
    await notify.send("fill" if lvl == 0 else "change", event(lvl, "Профіль", user, [f"{k}: {v}" for k, _, v in out]))


async def signed_in(user: User) -> None:
    """First sign-in ever: an imported student showed up, or someone unknown (pending) who needs a look."""
    pending = user.status == Status.pending
    lines = [f"👋 Перший вхід · {who(user, '/edit' if pending else '')}"]
    if pending:
        lines += [f"📧 {html.quote(user.email)}", "☝️ Не було в списках — статус «очікує»"]
    await notify.send("login", "\n".join(lines))
