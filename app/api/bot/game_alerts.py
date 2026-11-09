"""Alerts about the student's game (T113): claims (kind `claim`); the card, parts and rules (kind `game`)."""
from aiogram import html
from beanie import PydanticObjectId

from core.bot import notify
from core.bot.alerts import arrow, event, level
from core.models.user import User
from models.game import Claim, Game, Part
from models.rule import Rule
from models.task import Task
from models.vocab import sentence

PART = {"field": "поле", "window": "вікно", "menu": "меню", "entity": "сутність"}
CARD = {"title": "🏷 Назва", "base_game": "🕹 Основа", "base_custom": "🕹 Основа (своя)", "description": "📄 Опис", "phases": "🔁 Фази"}
CLAIM = {"note": "📝 Нотатка", "link": "🔗 Лінк", "params": "⚙️ Параметри", "part": "🧩 Обʼєкт"}
STATUS = {"claimed": "заявлено", "accepted": "✅ зараховано", "returned": "↩️ повернуто"}
fmt = lambda v: html.quote(" → ".join(v) if isinstance(v, list) else str(v)) if v else ""  # noqa: E731 — phases are a list
gone = lambda lvl: " → ✖️" if lvl == 2 else ""  # noqa: E731


async def claim(user: User, c: Claim, lvl: int, changes: dict | None = None) -> None:
    """0 new · 1 edited (a row per changed field) · 2 deleted."""
    task = await Task.find_one(Task.slug == c.task)
    rows = [f"🎯 {html.quote(task.title if task else c.task)}{gone(lvl)}"]
    if c.part and (part := await Part.get(PydanticObjectId(c.part))):
        rows.append(f"🧩 {PART[part.kind]} «{html.quote(part.title)}»")
    for key, label in CLAIM.items():
        if key in (changes or {}):
            old, new = changes[key]["old"], changes[key]["new"]
            rows.append(f"{label}: {arrow(level(old, new), old, new, fmt)}")
    await notify.send("claim", event(lvl, "Заявка", user, rows), user.email)


async def verdict(owner: User, c: Claim, changes: dict) -> None:
    """The teacher judged a claim: the student's line in the game feed."""
    task = await Task.find_one(Task.slug == c.task)
    rows = [f"🎯 {html.quote(task.title if task else c.task)} — {STATUS.get(c.status, c.status)}"]
    if c.verdict:
        rows.append(f"💬 {html.quote(c.verdict)}")
    await notify.send("claim", event(1, "Заявка", owner, rows), owner.email)


async def game(user: User, g: Game, changes: dict | None = None) -> None:
    """The card: created (no changes) or edited; a long description only says 'змінено'."""
    if changes is None:
        rows, lvl = [f"🏷 {html.quote(g.title)}", f"🕹 {html.quote(g.base_game or g.base_custom)}"], 0
    else:
        rows, lvl = [], 0
        for key, label in CARD.items():
            if key in changes:
                old, new = changes[key]["old"], changes[key]["new"]
                lvl_k = level(old, new)
                lvl = max(lvl, lvl_k)
                rows.append(f"{label}: {'змінено' if key == 'description' and lvl_k == 1 else arrow(lvl_k, old, new, fmt)}")
    if rows:
        await notify.send("game", event(lvl, "Гра", user, rows), user.email)


async def part(user: User, p: Part, lvl: int) -> None:
    await notify.send("game", event(lvl, "Гра", user, [f"🧩 {PART[p.kind]} «{html.quote(p.title)}»{gone(lvl)}"]), user.email)


async def rule(user: User, r: Rule, lvl: int) -> None:
    name = {str(p.id): p.title for p in await Part.find(Part.game == r.game).to_list()}
    text = html.quote(sentence(r, lambda pid: f"«{name.get(pid, '?')}»"))  # no icons in Telegram: quotes mark the names
    await notify.send("game", event(lvl, "Гра", user, [f"📜 {text}{gone(lvl)}"]), user.email)
