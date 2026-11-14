"""Claims the description makes by itself (T270 §6): a window claims its type, an entity its role and its stats, the field
and a level their properties; what is drawn on the site (T276) — a level's map, a scenario of the game's moments.
Nobody adds or removes them by hand: sync() keeps them in step with the parts after each change.
After a catalog import that changes kinds, opts or stats — every game at once: uv run python auto_claims.py"""
import asyncio
from collections import Counter, defaultdict

import moments
import options
import uploads
from core.models.history import record, record_delete, record_new
from db import init_db
from models.game import Claim, Game, Part
from models.task import Task


def wanted(parts: list[Part], cat: dict) -> dict[tuple[str, str], dict]:
    """(card slug, part id) → params, for every card the parts say they are."""
    out = {}
    for p in parts:
        pid = str(p.id)
        if p.kind == "window" and p.task:
            out[(p.task, pid)] = {}
        elif p.kind == "entity":
            if role := cat["role"].get(p.role):
                out[(role.slug, pid)] = {}
            for s in p.stats:
                if stat := cat["stat"].get(s["key"]):
                    out[(stat.slug, pid)] = {"value": s["value"]}
        elif p.kind in ("field", "level"):
            for key, v in p.props.items():
                for x in v if isinstance(v, list) else [v]:
                    if x is not False and (opt := cat["fieldopt"].get(f"{key}:{'on' if x is True else x}")):
                        out[(opt.slug, pid)] = {}
    return out


def drawn(game: Game, parts: list[Part], cards: set[str]) -> list[tuple[str, str]]:
    """(card slug, part id) of what is drawn (T276), a pair per claim: a level with a map — on it; every scenario of three
    frames and more — one more at game level. A card the catalog has not (yet) — nothing."""
    out = [(moments.MAP, str(p.id)) for p in parts if moments.MAP in cards and p.kind == "level" and str(p.props.get("map") or "").strip()]
    return out + [(moments.FRAMES, "")] * (moments.full(game.moments) if moments.FRAMES in cards else 0)


async def sync(game: Game, actor: str) -> Counter:
    """Insert the missing auto-claims, refresh a stat's value, delete what the parts no longer say. A hand-made claim of
    the same card on the same part (the window type before T270) is adopted rather than doubled. A card may be wanted
    on one place several times (a scenario each): the first claims fill those places, the rest go. No alerts: the part's are
    enough. Returns how many claims were added, adopted, updated (a stat's value) and removed."""
    parts = await Part.find(Part.game == game.id).to_list()
    cards = {t.slug for t in await Task.find({"slug": {"$in": [moments.MAP, moments.FRAMES]}, "status": {"$ne": "archived"}}).to_list()}
    want = defaultdict(list)
    for key, params in wanted(parts, await options.catalog(admin=True)).items():
        want[key].append(params)
    for key in drawn(game, parts, cards):
        want[key].append({})
    have, done = defaultdict(list), Counter()
    for c in await Claim.find(Claim.game == game.id).to_list():
        key = (c.task, c.part)
        if c.rule or not (c.auto or key in want):
            continue
        if len(have[key]) >= len(want.get(key, [])):
            uploads.drop_shots(c)
            await record_delete(c, actor=actor)
            done["removed"] += 1
        else:
            have[key].append(c)
    for key, wishes in want.items():
        for i, params in enumerate(wishes):
            if i < len(have[key]):
                if changes := await record(have[key][i], {"auto": True, "params": params}, actor=actor):
                    done["adopted" if "auto" in changes else "updated"] += 1
            else:
                c = Claim(game=game.id, task=key[0], part=key[1], params=params, auto=True)
                await c.insert()
                await record_new(c, actor=actor)
                done["added"] += 1
    return done


async def main():
    await init_db()
    games = await Game.find_all().to_list()
    done = sum([await sync(g, actor="auto-sync") for g in games], Counter())
    print(f"ігор {len(games)} · авто-заявок додано {done['added']} · прийнято {done['adopted']} · "
          f"оновлено {done['updated']} · прибрано {done['removed']}")


if __name__ == "__main__":
    asyncio.run(main())
