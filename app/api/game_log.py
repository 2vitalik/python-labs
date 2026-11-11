"""One student's game in `history` (T278 §12): the game, its parts, rules and claims — the deleted ones too — newest first,
each change with who made it and what it touched, in words (game_log_text.py)."""
from datetime import datetime

import options
from core.config import settings
from core.models.history import Change, stamp
from core.models.user import Status, User
from game_log_names import Names
from game_log_text import HIDDEN, action, fields, title, what
from models.base_game import BaseGame
from models.game import Claim, Game, Part
from models.rule import Rule
from models.task import Task

INSIDES = (Part, Rule, Claim)  # each carries `game`, and record_new / record_delete log it: deleted ones are found by it
COLLS = [m.Settings.name for m in INSIDES]
SCRIPTS = {"auto-sync": "синхронізація каталогу", "import": "імпорт каталогу"}  # actors with no account: scripts the teacher runs
# a change of plumbing alone (order, an auto-claim adopted) is no row: filtered in Mongo, so a page stays `limit` long
SEEN = {"$expr": {"$anyElementTrue": [{"$map": {"input": {"$objectToArray": "$changes"},
                                                "in": {"$not": [{"$in": ["$$this.k", list(HIDDEN)]}]}}}]}}


# an auto-claim comes and goes with its part (a window's type, a stat, a field option): the part's own row tells it
AUTO = {"$nor": [{"coll": "claims", "changes.auto.new": True, "changes.auto.old": None},
                 {"coll": "claims", "changes.auto.old": True, "changes.auto.new": None}]}


async def snapshots(game: Game) -> tuple[dict, set]:
    """doc id → (collection, fields): as it is now, or as it was when deleted; and every id the game's insides ever had."""
    ref = {"$in": [game.id, str(game.id)]}
    snaps = {game.id: ("student_games", game.model_dump())}
    for c in await Change.find({"coll": {"$in": COLLS}, "changes.game.old": ref}).to_list():
        snaps[c.doc_id] = (c.coll, {k: v.get("old") for k, v in c.changes.items()})
    for m in INSIDES:
        for d in await m.find(m.game == game.id).to_list():
            snaps[d.id] = (m.Settings.name, d.model_dump())
    born = await Change.distinct("doc_id", {"coll": {"$in": COLLS}, "changes.game.new": ref})
    return snaps, set(born) | set(snaps)


async def page(query: dict, before: datetime | None, limit: int) -> list[Change]:
    q = query | ({"at": {"$lt": before}} if before else {})
    found = await Change.find(q).sort("-at", "-_id").limit(limit).to_list()
    if len(found) == limit:  # the rest of the page's last moment too: the next page's `before` would skip it
        seen = {c.id for c in found}
        found += [c for c in await Change.find(q | {"at": found[-1].at}).sort("-_id").to_list() if c.id not in seen]
    return found


async def actors(emails: set[str]) -> dict[str, dict]:
    users = {u.email: u for u in await User.find({"email": {"$in": list(emails)}}).to_list()}
    agents = set(settings.agents.values())

    def who(email: str) -> dict:
        nick = email.split("@")[0]
        if email in agents or email.endswith("@agent"):  # deps.agent: a token's edits are signed `<name>@agent`
            return {"nick": nick, "name": nick, "role": "agent"}
        if not (u := users.get(email)):
            return {"nick": nick, "name": SCRIPTS.get(email, email), "role": "system"}
        teacher = u.status == Status.admin or email in settings.admin_list
        return {"nick": nick, "name": u.person()["name"] or nick, "role": "teacher" if teacher else "student"}
    return {e: who(e) for e in emails}


async def names(snaps: dict, found: list[Change]) -> Names:
    kept = lambda coll: {str(i): s for i, (c, s) in snaps.items() if c == coll}  # noqa: E731
    values = [s for _, s in snaps.values()] + [{k: v.get(end) for k, v in c.changes.items()} for c in found for end in ("old", "new")]
    slugs = {d.get("task") for d in values} | {it.get("task") for d in values for it in d.get("items") or []}
    cards = {t.slug: t for t in await Task.find({"slug": {"$in": list(slugs - {None, ""})}}).to_list()}
    bases = {g.slug: g.title for g in await BaseGame.find({"slug": {"$in": [d.get("base_game") for d in values]}}).to_list()}
    cat = await options.catalog(admin=True)
    return Names(kept("game_parts"), kept("rules"), cards, bases, {o: t.title for o, t in cat["role"].items()},
                 {o: t.title for o, t in cat["fieldopt"].items()})


async def rows(game: Game, before: datetime | None, limit: int) -> list[dict]:
    snaps, ids = await snapshots(game)
    query = {"$or": [{"coll": "student_games", "doc_id": game.id}, {"coll": {"$in": COLLS}, "doc_id": {"$in": list(ids)}}]}
    found = await page(query | SEEN | AUTO, before, limit)
    who, nm = await actors({c.actor for c in found}), await names(snaps, found)
    out = []
    for c in found:
        own = {k: v.get("new") if v.get("new") is not None else v.get("old") for k, v in c.changes.items()}
        snap = own | snaps.get(c.doc_id, ("", {}))[1]  # today's name for the object; its own values if nothing else is known
        out.append({"id": str(c.id), "at": stamp(c.at), "actor": who[c.actor], "coll": c.coll, "what": what(c.coll, snap),
                    "title": title(nm, c.coll, snap), "action": action(c.coll, c.changes), "fields": fields(nm, c.coll, c.changes, snap)})
    return out
