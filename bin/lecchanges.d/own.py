"""A journal entry that stands on its own (a doubt, a layout case, an A or G that found no edits): its hunk is the block of
now its quotes stand in — before = after = the block (contract §3.3) — or an empty one at the start of its slide."""
from hunks import WHERE
from locate import find, fragments

LIKE = 0.5


def own(e: dict, flat: list[dict], rec: dict) -> tuple[dict, dict]:
    frags, slides = fragments(e["body"]), set(e["slides"]) or {0}
    best, at = (LIKE, None), min((i for i, b in enumerate(flat) if b["slide"] in slides), default=0)
    for i, b in enumerate(flat):
        if b["slide"] in slides and (s := find(frags, b["raw"])[0]) >= best[0] + 0.01 * (best[1] is not None):
            best = (s, i)
    if best[1] is None:
        h = {"slide": min(slides), "before": "", "after": "", "pos": at - 0.4, "first": at, "last": at - 1, "where": "slide"}
    else:
        i, b = best[1], flat[best[1]]
        h = {"slide": b["slide"], "before": b["raw"], "after": b["raw"], "pos": i + 0.6, "first": i, "last": i,
             "where": WHERE.get(b["kind"], "text")}
    return h | {"units": [], "refs": []}, rec | {"ref": e["id"], "id": e["id"]}
