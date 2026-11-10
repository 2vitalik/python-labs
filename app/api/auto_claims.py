"""Claims the description makes by itself (T270 §6): a window claims its type, an entity its role and its stats, the field
and a level their properties. Nobody adds or removes them by hand: sync() keeps them in step with the parts after each change.
After a catalog import that changes kinds, opts or stats — every game at once: uv run python auto_claims.py"""
import asyncio
from collections import Counter

import options
from core.models.history import record, record_delete, record_new
from db import init_db
from models.game import Claim, Game, Part


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


async def sync(game: Game, actor: str) -> Counter:
    """Insert the missing auto-claims, refresh a stat's value, delete what the parts no longer say. A hand-made claim of
    the same card on the same part (the window type before T270) is adopted rather than doubled. No alerts: the part's are enough.
    Returns how many claims were added, adopted, updated (a stat's value) and removed."""
    want = wanted(await Part.find(Part.game == game.id).to_list(), await options.catalog(admin=True))
    have, done = {}, Counter()
    for c in await Claim.find(Claim.game == game.id).to_list():
        key = (c.task, c.part)
        if c.rule or not (c.auto or key in want):
            continue
        if key not in want or key in have:
            await record_delete(c, actor=actor)
            done["removed"] += 1
        else:
            have[key] = c
    for key, params in want.items():
        if c := have.get(key):
            if changes := await record(c, {"auto": True, "params": params}, actor=actor):
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
