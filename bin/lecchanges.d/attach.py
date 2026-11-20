"""The journal on the hunks (contract §3.2.8–9). An A entry finds its edits — in the block that carries its comment
`<!-- правка NN-An -->`, else on its slides — by its `Стало` / `Було`, and gives them its title, why and origin; a G entry
finds the text it brought back; B and H — and A or G that found nothing — are records of their own, on the block their
quotes stand in (or on none)."""
from journal import importance, origin
from locate import find, fragments
from own import LIKE, own
from units import units


def attach(entries: list[dict], hunks: list[dict], flat: list[dict]) -> tuple[dict, list[tuple]]:
    """(what each journal id tells its records, [(hunk, record) of the entries standing alone]). The comments go first
    for every entry; only then the quotes alone, among the edits nobody took."""
    info, alone, fixes = {}, [], []
    for e in entries:
        f, letter = e["fields"], e["letter"]
        if letter == "A":
            why = f.get("Чому певен", "") + (f"\n\n**За перевіркою:** {f['За перевіркою']}" if f.get("За перевіркою") else "")
            info[e["id"]] = {"title": e["title"], "why": why or e["body"], "origin": origin(f.get("Звідки помилка", ""))}
            fixes.append((e, fragments(f.get("Було", "")), fragments(f.get("Стало", ""))))
        elif letter == "G":
            info[e["id"]] = {"title": e["title"], "why": e["body"], "kind": "restored", "origin": "convert"}
            fixes.append((e, [], fragments(f.get("Стало в тексті", ""))))
        else:
            status = importance(f.get("Важить", "")) if letter == "H" else "open"
            alone.append(own(e, flat, {"title": e["title"], "why": e["body"], "kind": "doubt" if letter == "B" else "layout",
                                       "status": status, "origin": "slide" if letter == "B" else "site"}))
    left = [x for x in fixes if not take(x[0]["id"], marked(hunks, *x))]
    for e, fb, fa in left:
        if not take(e["id"], search(hunks, e, fb, fa)):
            alone.append(own(e, flat, info[e["id"]] | {"kind": info[e["id"]].get("kind") or "error"}))
    return info, alone


def take(ref: str, got: list[dict]) -> bool:
    for u in got:
        u["ref"] = ref
    return bool(got)


def overlap(x: list[int], span: tuple[int, int] | None) -> bool:
    return bool(span) and x[0] <= span[1] and x[1] >= span[0]


def hits(h: dict, was: tuple | None, now: tuple | None) -> list[dict]:
    """The free units under the quotes; the machine's and the rules' ones only when nothing else is there."""
    got = [u for u in units(h) if "look" not in u and not u.get("ref") and (overlap(u["b"], now) or overlap(u["a"], was))]
    return [u for u in got if u["how"] not in ("auto", "rule")] or got


def best(pool: list[dict], fb: list, fa: list, floor: float) -> list[dict]:
    """The units under the quotes in the hunk that holds them best."""
    out = (floor, [])
    for h in pool:
        (sb, spb), (sa, spa) = find(fb, h["before"]), find(fa, h["after"])
        if max(sb, sa) >= out[0] and (got := hits(h, spb, spa)):
            out = (max(sb, sa) + 1e-9, got)
    return out[1]


def marked(hunks: list[dict], e: dict, fb: list, fa: list) -> list[dict]:
    """In the blocks with the entry's comment: the units under its quotes, else the ones nothing classified."""
    got = []
    for h in (h for h in hunks if e["id"] in h["refs"]):
        got += (hits(h, find(fb, h["before"])[1], find(fa, h["after"])[1])
                or [u for u in units(h) if u["how"] in (None, "set") and not u.get("ref")])
    return got


def search(hunks: list[dict], e: dict, fb: list, fa: list) -> list[dict]:
    """A commented block that only kept its place has the fix next to it (a removed copy, an added word); without a
    comment — anywhere on the entry's slides. Blocks with another entry's comment are that entry's."""
    free = lambda h: all(r == e["id"] for r in h["refs"])
    at = [i for i, h in enumerate(hunks) if e["id"] in h["refs"]]
    if at:
        near = {j for i in at for j in range(i - 2, i + 3) if 0 <= j < len(hunks) and hunks[j]["slide"] == hunks[i]["slide"]}
        return best([hunks[j] for j in sorted(near) if free(hunks[j])], fb, fa, 0.2)
    return best([h for h in hunks if h["slide"] in e["slides"] and free(h)], fb, fa, LIKE)

