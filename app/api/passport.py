"""A described game as the pages show it (the passport, T270 §14.5): its parts, claims and rules with the cards they name
and what the claims are worth. A student's game (routes/student_games.py) and a base game's etalon (routes/etalon.py) alike."""
from models.game import Claim, Game, Part
from models.rule import Rule
from models.task import Task
from zones import kind_of


def task_index(tasks: list[Task]) -> dict:
    """Minimal card info for rendering claims/parts, drafts included (viewer may not see them in the catalog)."""
    return {t.slug: {"title": t.title, "coin": t.coin, "amount": t.amount, "slots": t.slots, "tags": t.tags,
                     "zone": t.zone, "subzone": t.subzone, "status": t.status, "kind": kind_of(t), "icon": t.icon,
                     "opt": t.opt, "description": t.description, "max_count": t.max_count, "parent": t.parent,
                     "rule": t.rule, "proof": t.proof} for t in tasks}


def coins_of(claims: list[Claim], tasks: list[Task]) -> dict:
    """What the claims are worth by kind of coin, claimed and accepted apart (T240; informational until grading).
    A card counts at most max_count times a game (0 — no cap): five enemies are one coin for the role «ворог» (T270)."""
    out: dict[str, dict] = {"claimed": {}, "accepted": {}}
    for t in tasks:
        if not t.coin:
            continue
        mine = [c for c in claims if c.task == t.slug]
        for key, n in (("claimed", len(mine)), ("accepted", sum(c.status == "accepted" for c in mine))):
            n = min(n, t.max_count) if t.max_count else n
            if n:
                out[key][t.coin] = out[key].get(t.coin, 0) + n * t.amount
    return out


async def passport(game: Game) -> dict:
    parts = await Part.find(Part.game == game.id).sort("order", "created_at").to_list()
    claims = await Claim.find(Claim.game == game.id).sort("created_at").to_list()
    rules = await Rule.find(Rule.game == game.id).sort("created_at").to_list()
    slugs = {p.task for p in parts if p.task} | {c.task for c in claims} | {i["task"] for p in parts for i in p.items if i.get("task")}
    tasks = await Task.find({"slug": {"$in": list(slugs)}}).to_list()
    return {"game": game.api(), "parts": [p.api() for p in parts], "claims": [c.api() for c in claims],
            "rules": [r.api() for r in rules], "coins": coins_of(claims, tasks), "tasks": task_index(tasks)}
