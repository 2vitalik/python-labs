"""A lecture then and now → hunks in reading order: a pair of blocks (or a group of merged ones) with its edits and its
changes of looks; a run of removed blocks; a run of added ones. A hunk knows its slide, its place among the blocks of
now (`pos`), the raw texts before and after, the journal ids its comments carry."""
from diff import edits, looks
from md import slides
from pair import pairs

WHERE = {"heading": "heading", "table": "table", "image": "alt", "math": "formula", "caption": "caption"}


def lecture(base_text: str, now_text: str) -> tuple[list[dict], list[dict]]:
    """(hunks, the blocks of now in reading order — the context of the hunks and of the journal's entries)."""
    bs, ns = slides(base_text), slides(now_text)
    flat, start, out = [], {}, []
    for s in sorted(ns):
        start[s] = len(flat)
        flat += [dict(b, slide=s) for b in ns[s]]
    for s in sorted(set(bs) | set(ns)):
        base, now, at = bs.get(s, []), ns.get(s, []), start.get(s, 0)
        for bi, ni in runs(order(pairs(base, now))):
            pos = at + (min(ni) if ni else anchor(out, s, at))
            h = {"slide": s, "before": "\n\n".join(base[i]["raw"] for i in bi), "after": "\n\n".join(now[k]["raw"] for k in ni),
                 "parts": [base[i]["raw"] for i in bi] or [now[k]["raw"] for k in ni],
                 "pos": pos, "first": int(pos + 0.5), "last": at + max(ni) if ni else int(pos + 0.5) - 1,
                 "refs": [r for k in ni for r in now[k]["refs"]], "fence": now[ni[0]]["fence"] if ni else "",
                 "where": where([base[i] for i in bi] + [now[k] for k in ni]), "edits": [], "looks": [], "look": "",
                 "tables": any(b["kind"] == "table" for b in now)}
            if bi and ni:
                same = " ".join(base[i]["bare"] for i in bi) == " ".join(now[k]["bare"] for k in ni)
                h["edits"] = [] if same else edits(h["before"], h["after"])
                h["looks"], h["look"] = looks(h["before"], h["after"], not same) if h["before"] != h["after"] else ([], "")
            out.append(h)
    return sorted(out, key=lambda h: h["pos"]), flat


def order(groups: list) -> list:
    """Groups as one reads now; a removed group stands after the pair of the base block before it."""
    def key(g):
        bi, ni = g
        if ni:
            return (min(ni), 0, min(bi) if bi else -1)
        before = [max(n) for b, n in groups if n and b and min(b) < min(bi)]
        return (max(before, default=-1), 1, min(bi))
    return sorted(groups, key=key)


def runs(groups: list) -> list:
    """Neighbouring removed groups — one hunk; so are added ones in the same region of the slide."""
    out = []
    for bi, ni in groups:
        prev = out[-1] if out else None
        if prev and not ni and not prev[1] and prev[0]:
            prev[0].extend(bi)
        elif prev and not bi and not prev[0] and prev[1] and max(prev[1]) + 1 == min(ni):
            prev[1].extend(ni)
        else:
            out.append((list(bi), list(ni)))
    return out


def anchor(done: list[dict], s: int, at: int) -> float:
    """A removed run's place: right after the last block of now already placed on this slide."""
    return max((h["last"] - at for h in done if h["slide"] == s and h["after"]), default=-1) + 0.5


def where(blocks: list[dict]) -> str:
    kinds = {WHERE.get(b["kind"], "text") for b in blocks}
    return kinds.pop() if len(kinds) == 1 else "text"
