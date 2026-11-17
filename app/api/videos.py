"""The videos a game is asked for (T318), as «Супровід» lists them: rows nobody adds by hand. A demo by the deadline of
each lab in DEMO_LABS, the async defenses of the semester — and a row per gold card the game claims.
What the course asks of whom — data/guide/score.md: a demo for everyone, a defense from 70, gold cards from 85."""
from datetime import datetime

from core.labs import due_for, effective, utc
from core.models.deadline import Deadline, LabMark
from core.models.history import stamp, when
from core.models.user import User
from models.game import Game
from models.video import Video

DEMO_LABS = (3, 4)  # a demo is a condition of these labs' deadlines
DEFENSES = 2  # async defenses a semester: no deadlines of their own, the second may be the only one
GOLD = ("gold", "crown")  # a card of this coin is explained in a video of its own — unless the teacher lets it go
MARK = "gold:"

FIXED = ([{"slot": f"demo{n}", "kind": "demo", "lab": n} for n in DEMO_LABS]
         + [{"slot": f"defense{n}", "kind": "defense", "n": n} for n in range(1, DEFENSES + 1)])


def gold_slugs(claims: list[dict], tasks: dict) -> list[str]:
    """The gold cards among the game's claims, each once, in the claims' order."""
    return list(dict.fromkeys(c["task"] for c in claims if tasks.get(c["task"], {}).get("coin") in GOLD))


def title(slot: str, card=lambda slug: slug) -> str:
    """A slot in words — for the history and the alerts."""
    if slot.startswith(MARK):
        return card(slot[len(MARK):])
    return f"демка до лаби {slot[4:]}" if slot.startswith("demo") else f"асинхронний захист {slot[7:]}"


async def dues(owner: User | None) -> dict[int, datetime | None]:
    """The student's own deadline of each lab that asks for a demo: the group's, or as the teacher moved it."""
    if not owner:
        return {}
    deadlines = await Deadline.find({"lab": {"$in": list(DEMO_LABS)}}).to_list()
    marks = {m.lab: m for m in await LabMark.find({"user": owner.email, "lab": {"$in": list(DEMO_LABS)}}).to_list()}
    return {n: effective(marks.get(n), due_for(deadlines, n, owner.group)) for n in DEMO_LABS}


def row(spec: dict, doc: Video | None, due: datetime | None = None) -> dict:
    """`on_time` — the first link came by the deadline: a later version does not undo it."""
    versions = doc.versions if doc else []
    first = utc(versions[0]["at"]) if versions else None
    return spec | {
        "versions": [{"link": v["link"], "note": v.get("note", ""), "at": stamp(v["at"]), "by": v.get("by", "").split("@")[0]} for v in versions],
        "need": doc.need if doc else "", "why": doc.why if doc else "",
        "status": doc.status if doc else "claimed", "verdict": doc.verdict if doc else "",
        "due": when(due), "on_time": first <= due if first and due else None,
    }


def specs(claims: list[dict], tasks: dict) -> list[dict]:
    return FIXED + [{"slot": MARK + s, "kind": "gold", "task": s} for s in gold_slugs(claims, tasks)]


async def rows(game: Game, owner: User | None, claims: list[dict], tasks: dict) -> list[dict]:
    """Every row of the game, filled or not, in the page's order. `claims`, `tasks` — as the passport gives them."""
    docs = {v.slot: v for v in await Video.find(Video.game == game.id).to_list()}
    due = await dues(owner)
    return [row(s, docs.get(s["slot"]), due.get(s.get("lab"))) for s in specs(claims, tasks)]


async def waiting(game: Game) -> int:
    """The videos with a link the teacher has not spoken on yet."""
    return sum(1 for v in await Video.find(Video.game == game.id, Video.status == "claimed").to_list() if v.versions and v.need != "skip")


async def summary(games: list[Game]) -> dict:
    """game id → {slot: {at, last, n, link, status, need}} of the fixed rows that have a link or the teacher's word — for the
    lists of students. `at` — when the first link came: what a deadline looks at; `last` — the latest version."""
    out: dict = {}
    slots = [s["slot"] for s in FIXED]
    for v in await Video.find({"game": {"$in": [g.id for g in games]}, "slot": {"$in": slots}}).to_list():
        if v.versions or v.need or v.status != "claimed":
            first, last = (v.versions[0], v.versions[-1]) if v.versions else ({}, {})
            out.setdefault(v.game, {})[v.slot] = {"at": when(first.get("at")), "last": when(last.get("at")), "n": len(v.versions),
                                                  "link": last.get("link", ""), "status": v.status, "need": v.need}
    return out
