"""Alerts about the student's game (T113): claims (kind `claim`); the card, parts and rules (kind `game`)."""
from aiogram import html
from beanie import PydanticObjectId

from bot import notify
from bot.alerts import arrow, event, level
from models.game import Claim, Game, Part
from models.rule import Rule
from models.task import Task
from models.user import User

PART = {"window": "вікно", "menu": "меню", "entity": "сутність"}
CARD = {"title": "🏷 Назва", "base_game": "🕹 Основа", "base_custom": "🕹 Основа (своя)", "description": "📄 Опис"}
CLAIM = {"note": "📝 Нотатка", "link": "🔗 Лінк", "params": "⚙️ Параметри"}
EFFECT = {  # mirrors app/vue/src/rules.js
    "disappear_a": "зникає А", "disappear_b": "зникає Б", "disappear_both": "зникають обидва", "block": "блокує рух",
    "push": "штовхається", "pickup": "підбирається", "teleport": "телепорт", "damage": "шкода", "score": "очки",
    "spawn": "спавн", "transform": "перетворення на", "window": "відкрити вікно", "win": "перемога 🏆", "lose": "поразка 💀",
}
fmt = lambda v: html.quote(str(v)) if v else ""  # noqa: E731
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
    await notify.send("claim", event(lvl, "Заявка", user, rows))


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
                rows.append(f"{label}: {'змінено' if key == 'description' and lvl_k == 1 else arrow(lvl_k, old, new)}")
    if rows:
        await notify.send("game", event(lvl, "Гра", user, rows))


async def part(user: User, p: Part, lvl: int) -> None:
    await notify.send("game", event(lvl, "Гра", user, [f"🧩 {PART[p.kind]} «{html.quote(p.title)}»{gone(lvl)}"]))


def sentence(r: Rule, name: dict[str, str]) -> str:
    """КОЛИ … → ТО … the way the site shows it."""
    w = r.when
    when = f"«{name.get(w.get('a'), '?')}» × «{name.get(w.get('b'), '?')}»" if w["kind"] == "contact" \
        else f"кожні {w['every']} тіків"
    effects = []
    for e in r.then:
        text = EFFECT.get(e["kind"], e["kind"])
        if "n" in e:
            text += f" {e['n']}"
        elif "part" in e:
            text += f" «{name.get(e['part'], '?')}»"
        elif "text" in e:
            text = e["text"]
        effects.append(text)
    return html.quote(f"КОЛИ {when} → ТО {' · '.join(effects)}")


async def rule(user: User, r: Rule, lvl: int) -> None:
    name = {str(p.id): p.title for p in await Part.find(Part.game == r.game).to_list()}
    await notify.send("game", event(lvl, "Гра", user, [f"📜 {sentence(r, name)}{gone(lvl)}"]))
