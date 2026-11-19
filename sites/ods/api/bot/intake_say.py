"""The bot's one summary of a burst of forwards (T368 §2.2), T109 style: a role emoji opens every line, no periods, HTML;
per talk — who it is, a line per notebook, how many messages, whether they ask for time; then repeats and the link to «Вхідні»."""
from aiogram import html

from core.activity_people import TZ
from core.bot.alerts import who
from core.config import settings
from core.labs import utc
from core.models.user import User
from intake_match import guess
from models.forward import ForwardHead

LIMIT = 4096  # Telegram's longest message
WHY = {"card": "за карткою", "username": "за ніком", "name": "за імʼям"}


def at(r: ForwardHead) -> str:
    return utc(r.sent_at).astimezone(TZ).strftime("%d.%m %H:%M")


def notebook(r: ForwardHead) -> list[str]:
    """📓 Лаба 2 · КН-1-07 · 13/14 ✅ · 14.11 21:03 · на сайті — and the reason in words when it did not go over."""
    state = "на сайті" if r.version else "не перенесено" if r.lab and r.student else ""
    score = f"{r.ok}/{r.total} ✅" if r.total else "" if r.line else "без рядка"
    parts = [f"Лаба {r.lab}" if r.lab else "Лаба ?", html.quote(r.vid), score, at(r), state]
    return [f"📓 {' · '.join(p for p in parts if p)}"] + ([f"⚠️ {html.quote(r.trouble)}"] if r.trouble else [])


def talk(rows: list[ForwardHead], user: User | None, clues: tuple) -> list[str]:
    theirs = [r for r in rows if not r.mine]
    if user:
        head = f"🎓 {who(user)}"
    elif theirs:
        nick = f" · @{html.quote(theirs[-1].username)}" if theirs[-1].username else ""
        g = guess(rows, *clues)
        like = f" · схоже, {html.quote(g['name'] or g['nick'])} ({WHY[g['why']]})" if g else ""
        head = f"❓ {html.quote(theirs[-1].name)}{nick} · не впізнаю{like}"
    else:
        head = "🧑‍🏫 Лише твої повідомлення — не знаю, з чиєї розмови"
    lines = [head]
    for r in rows:
        if r.kind:
            lines += notebook(r)
        elif r.file:
            lines.append(f"📎 {html.quote(r.file.get('name', ''))} · {html.quote(r.why or 'без ноутбука')}")
    lines.append(f"💬 повідомлень: {len(rows)}" + (" · 🙋 просить час" if any(r.asks for r in rows) else ""))
    return lines


def summary(rows: list[ForwardHead], users: dict[str, User], again: int = 0, other: int = 0, clues: tuple = ([], {})) -> str:
    """`rows` — the burst's new forwards, the oldest first; `users` — email → the students they belong to; `clues` — what
    a guess at the unknown goes by (intake_match.clues)."""
    talks: dict[str, list[ForwardHead]] = {}
    for r in rows:
        talks.setdefault(r.key, []).append(r)
    blocks = ["\n".join(talk(rs, users.get(next((r.student for r in rs if r.student), "")), clues)) for rs in talks.values()]
    foot = ([f"♻️ вже були: {again}"] if again else []) + ([f"📢 з груп і каналів не беру: {other}"] if other else [])
    link = f'🌐 <b><a href="{settings.site_url}/intake">Вхідні</a></b>'
    return "\n\n".join([f"📥 Записав повідомлень: {len(rows)}" if rows else "📥 Нового нема", *blocks, "\n".join([*foot, link])])


def pages(text: str) -> list[str]:
    """A long summary as several messages, split between talks."""
    out: list[str] = []
    for block in text.split("\n\n"):
        if out and len(out[-1]) + 2 + len(block) <= LIMIT:
            out[-1] += "\n\n" + block
        else:
            out.append(block)
    return out
