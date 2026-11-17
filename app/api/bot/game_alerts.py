"""Alerts about the student's game (T113): claims (kind `claim`); the card, parts and rules (kind `game`);
ideas, words on a card or on the site (kind `idea`, T270, T274 §4); the videos of «Супровід» go with the claims (T318)."""
from aiogram import html
from beanie import PydanticObjectId

import videos
from core.bot import notify
from core.bot.alerts import arrow, event, level
from core.models.user import User
from models.game import Claim, Game, Part
from models.ref import Ref
from models.rule import Rule
from models.task import Task
from models.video import Video
from models.vocab import sentence
from zones import ZONES

PART = {"field": "поле", "window": "вікно", "menu": "переходи", "entity": "сутність", "level": "рівень"}
CARD = {"title": "🏷 Назва", "base_game": "🕹 Основа", "base_custom": "🕹 Основа (своя)", "description": "📄 Опис", "phases": "🔁 Фази"}
CLAIM = {"note": "📝 Нотатка", "why": "🙋 Запит", "link": "🔗 Лінк", "params": "⚙️ Параметри", "part": "🧩 Обʼєкт"}
STATUS = {"claimed": "заявлено", "accepted": "✅ зараховано", "returned": "↩️ повернуто"}
IDEA = {"idea": ("💡", "Ідея"), "fix": ("🛠", "Про картку"), "site": ("🐞", "Про сайт")}  # Ref.kind → icon, subject
NEED = {"must": "обовʼязкове", "skip": "не потрібне", "": "як у всіх"}
fmt = lambda v: html.quote(" → ".join(v) if isinstance(v, list) else str(v)) if v else ""  # noqa: E731 — phases are a list
gone = lambda lvl: " → ✖️" if lvl == 2 else ""  # noqa: E731


async def send(kind: str, text: str, email: str, game: PydanticObjectId | None = None) -> None:
    """`game` — whose game was edited: the teacher's edit in a student's game (X-Game-Of) is no news to the teacher."""
    if email.endswith("@sandbox"):  # the sandbox's author is made up (routes/my_game.py): its edits are nobody's news
        return
    if game and (g := await Game.get(game)) and g.owner != email:
        return
    await notify.send(kind, text, email)


async def claim(user: User, c: Claim, lvl: int, changes: dict | None = None) -> None:
    """0 new · 1 edited (a row per changed field) · 2 deleted."""
    task = await Task.find_one(Task.slug == c.task)
    rows = [f"🎯 {html.quote(task.title if task else c.task)}{gone(lvl)}"]
    if c.part and (part := await Part.get(PydanticObjectId(c.part))):
        rows.append(f"🧩 {PART[part.kind]} «{html.quote(part.title)}»")
    if c.rule and (r := await Rule.get(PydanticObjectId(c.rule))):
        rows.append(f"📜 {await said(r)}")
    if lvl == 0 and c.why:  # a card outside the core: the student's line is the news (T319)
        rows.append(f"🙋 {html.quote(c.why)}")
    for key, label in CLAIM.items():
        if key in (changes or {}):
            old, new = changes[key]["old"], changes[key]["new"]
            rows.append(f"{label}: {arrow(level(old, new), old, new, fmt)}")
    await send("claim", event(lvl, "Заявка", user, rows), user.email, c.game)


async def verdict(owner: User, c: Claim, changes: dict) -> None:
    """The teacher judged a claim: the student's line in the game feed."""
    task = await Task.find_one(Task.slug == c.task)
    rows = [f"🎯 {html.quote(task.title if task else c.task)} — {STATUS.get(c.status, c.status)}"]
    if c.verdict:
        rows.append(f"💬 {html.quote(c.verdict)}")
    await send("claim", event(1, "Заявка", owner, rows), owner.email)


async def video_title(v: Video) -> str:
    slug = v.slot.removeprefix(videos.MARK)
    task = await Task.find_one(Task.slug == slug) if slug != v.slot else None
    return html.quote(videos.title(v.slot, lambda s: task.title if task else s))


async def video(user: User, v: Video) -> None:
    """A link in «Супровід»: the first one, or a new version of it."""
    last, n = v.versions[-1], len(v.versions)
    rows = [f"🎬 {await video_title(v)}{f' · версія {n}' if n > 1 else ''}", f"🔗 {html.quote(last['link'])}"]
    if last.get("note"):
        rows.append(f"📝 {html.quote(last['note'])}")
    await send("claim", event(0 if n == 1 else 1, "Відео", user, rows), user.email, v.game)


async def video_word(owner: User, v: Video, changes: dict) -> None:
    """The teacher's word on a video: the student's line in the game feed."""
    rows = [f"🎬 {await video_title(v)}{f' — {STATUS.get(v.status, v.status)}' if 'status' in changes else ''}"]
    if "need" in changes:
        rows.append(f"📌 {NEED.get(v.need, v.need)}{f': {html.quote(v.why)}' if v.why else ''}")
    if v.verdict and {"status", "verdict"} & changes.keys():
        rows.append(f"💬 {html.quote(v.verdict)}")
    await send("claim", event(1, "Відео", owner, rows), owner.email)


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
        await send("game", event(lvl, "Гра", user, rows), user.email, g.id)


async def part(user: User, p: Part, lvl: int) -> None:
    await send("game", event(lvl, "Гра", user, [f"🧩 {PART[p.kind]} «{html.quote(p.title)}»{gone(lvl)}"]), user.email, p.game)


async def said(r: Rule) -> str:
    """The rule's sentence, quoted for HTML; no icons in Telegram: quotes mark the names."""
    name = {str(p.id): p.title for p in await Part.find(Part.game == r.game).to_list()}
    return html.quote(sentence(r, lambda pid: f"«{name.get(pid, '?')}»"))


async def rule(user: User, r: Rule, lvl: int) -> None:
    await send("game", event(lvl, "Гра", user, [f"📜 {await said(r)}{gone(lvl)}"]), user.email, r.game)


def where(ref: Ref) -> str:
    """«категорія → підкатегорія» by their titles; "" when the ref is about none."""
    zone = ZONES.get(ref.zone)
    sub = zone and zone["subzones"].get(ref.subzone)
    return " → ".join(x for x in (zone and zone["title"], sub and sub[0]) if x)


async def idea(user: User, ref: Ref) -> None:
    icon, subject = IDEA[ref.kind]
    rows = [f"{icon} {html.quote(ref.title)}" if ref.title else f"{icon} {subject.lower()}"]
    if place := where(ref):
        rows.append(f"🗂 {html.quote(place)}")
    if ref.task and (task := await Task.find_one(Task.slug == ref.task)):
        rows.append(f"🎯 {html.quote(task.title)}")
    if ref.note:
        rows.append(f"💬 {html.quote(ref.note)}")
    await send("idea", event(0, subject, user, rows), user.email)
