"""Which edits of a hunk are a journal entry's: those that are its fix (`locate.fits`) or, when its quotes cannot
be compared, those under its quotes; a note's edits are never taken."""
from locate import find, fits
from units import units


def overlap(x: list[int], span: tuple[int, int] | None) -> bool:
    return bool(span) and x[0] <= span[1] and x[1] >= span[0]


def free(h: dict) -> list[dict]:
    """Units an entry may take: not a change of looks, not taken, not classified by a note."""
    return [u for u in units(h) if "look" not in u and not u.get("ref") and u["how"] != "key"]


def mine(h: dict, fix, fb: list, fa: list) -> list[dict]:
    """The entry's units in the hunk: its fix's words; without them — the units under its quotes, the machine's and the
    rules' ones only when nothing else is there."""
    if fix:
        got = [u for u in free(h) if fits(u, fix)]
    else:
        was, now = find(fb, h["before"])[1], find(fa, h["after"])[1]
        got = [u for u in free(h) if overlap(u["b"], now) or overlap(u["a"], was)]
    return [u for u in got if u["how"] not in ("auto", "rule")] or got


def best(pool: list[dict], fix, fb: list, fa: list, floor: float) -> list[dict]:
    """The entry's units in the hunk that holds its quotes best; a picture's description only when nothing else does."""
    for some in ([h for h in pool if h["where"] != "alt"], [h for h in pool if h["where"] == "alt"]):
        out = (floor, [])
        for h in some:
            score = max(find(fb, h["before"])[0], find(fa, h["after"])[0])
            if score >= out[0] and (got := mine(h, fix, fb, fa)):
                out = (score + 1e-9, got)
        if out[1]:
            return out[1]
    return []
