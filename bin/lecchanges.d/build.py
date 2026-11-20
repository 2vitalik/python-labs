"""One lecture's catalogue (contract §3.2–3.3): the hunks of then and now, their units keyed and classified, the journal
laid on them, the items and the hunks numbered in reading order."""
from collections import Counter

import store
from attach import attach
from hunks import lecture
from journal import entries
from records import alone, override, records
from tok import inside, math
from units import classed, keyed

CONTEXT = 300


def build(n: int) -> tuple[dict, dict]:
    """(the file's data, what made it: `hows` — items by what classified them, `keys` — every unit's key)."""
    base, now = store.text(n)
    hunks, flat = lecture(base, now)
    keyed(hunks)
    classed(hunks, store.rules(), store.notes(n))
    info, lone = attach(entries(store.journal(n)), hunks, flat)
    pairs = records(n, hunks, info) + [(h, alone(n, rec)) for h, rec in lone]
    pairs.sort(key=lambda p: (p[0]["pos"], p[1]["edits"][0]["b"][0] if p[1]["edits"] else -1, p[1]["id"]))
    numbered, items, seen = {}, [], {}
    for h, it in pairs:
        if id(h) not in numbered:
            numbered[id(h)] = f"h{len(numbered) + 1}"
        it |= {"slide": h["slide"], "where": it["where"] or h["where"], "hunk": numbered[id(h)]}
        seen[it["id"]] = seen.get(it["id"], 0) + 1
        it["id"] += f".{seen[it['id']]}" if seen[it["id"]] > 1 else ""
        items.append(it)
    override(items, store.notes(n).get("ids", {}))
    hunks_out = {numbered[id(h)]: hunk(h, flat) for h, _ in pairs if numbered.get(id(h))}
    meta = {"hows": Counter(it.pop("how") for it in items), "keys": {u["key"] for h in hunks for u in h["units"]}}
    return {"lec": n, "slug": f"lec{n:02}", "base": "orig", "head": store.head(n), "built": "", "items": items,
            "hunks": hunks_out, "todo": sum(it["kind"] == "todo" for it in items)}, meta


def hunk(h: dict, flat: list[dict]) -> dict:
    """The blocks before and after, and the blocks of now around them (`first`, `last` — its own blocks of now; a hunk
    with none has last = first - 1), cut to about CONTEXT chars."""
    prev = flat[h["first"] - 1]["raw"] if 0 < h["first"] <= len(flat) else ""
    nxt = flat[h["last"] + 1]["raw"] if 0 <= h["last"] + 1 < len(flat) else ""
    return {"slide": h["slide"], "before": h["before"], "after": h["after"], "prev": cut(prev, tail=True), "next": cut(nxt)}


def cut(raw: str, tail: bool = False) -> str:
    """At most ~CONTEXT chars at a space outside formulas, «…» where cut; prev keeps its end, next its start."""
    if len(raw) <= CONTEXT:
        return raw
    spans = math(raw)
    spaces = [i for i, c in enumerate(raw) if c == " " and not inside(i, spans)]
    if tail:
        at = min((i for i in spaces if i >= len(raw) - CONTEXT), default=None)
        return "…" + raw[at:] if at is not None else raw
    at = max((i for i in spaces if i <= CONTEXT), default=None)
    return raw[:at] + " …" if at is not None else raw
