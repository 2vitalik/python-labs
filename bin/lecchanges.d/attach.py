"""The journal on the hunks (contract §3.2.8–9). An A entry takes the edits that are its fix — those whose words are
the difference between its own `Було` and `Стало`, in the block with its comment `<!-- правка NN-An -->`, else next to
it, else on its slides; without quotes on both sides — the edits under them. The other edits of the block stay items
of their own. A G entry takes the text it brought back (not a picture's description, when there is more); B and H —
and A or G that found nothing — are records of their own, on the block their quotes stand in (or on none).
An edit a note gives to an entry (`ref`) is that entry's; an edit a note classifies without one is nobody's."""
from journal import importance, origin
from locate import changes, fragments
from own import LIKE, own
from pick import best, free, mine
from units import units


def attach(entries: list[dict], hunks: list[dict], flat: list[dict]) -> tuple[dict, list[tuple]]:
    """(what each journal id tells its records, [(hunk, record) of the entries standing alone]). The comments go first
    for every entry; only then the quotes alone, among the edits nobody took."""
    info, alone, fixes = {}, [], []
    noted = {u["cls"]["ref"] for h in hunks for u in units(h) if u["how"] == "key" and u["cls"].get("ref")}
    for e in entries:
        f, letter = e["fields"], e["letter"]
        if letter == "A":
            why = f.get("Чому певен", "") + (f"\n\n**За перевіркою:** {f['За перевіркою']}" if f.get("За перевіркою") else "")
            info[e["id"]] = {"title": e["title"], "why": why or e["body"], "origin": origin(f.get("Звідки помилка", ""))}
            fixes.append((e, changes(f.get("Було", ""), f.get("Стало", "")), fragments(f.get("Було", "")),
                          fragments(f.get("Стало", ""))))
        elif letter == "G":
            info[e["id"]] = {"title": e["title"], "why": e["body"], "kind": "restored", "origin": "convert"}
            fixes.append((e, None, [], fragments(f.get("Стало в тексті", ""))))
        else:
            status = importance(f.get("Важить", "")) if letter == "H" else "open"
            alone.append(own(e, flat, {"title": e["title"], "why": e["body"], "kind": "doubt" if letter == "B" else "layout",
                                       "status": status, "origin": "slide" if letter == "B" else "site"}))
    for e, fix, fb, fa in [x for x in fixes if not take(x[0]["id"], marked(hunks, *x), noted)]:
        tries = [(search, fix)] + ([(marked, None), (search, None)] if fix else [])  # the journal paraphrased: its quotes
        if not any(take(e["id"], how(hunks, e, f, fb, fa), noted) for how, f in tries) and e["id"] not in noted:
            alone.append(own(e, flat, info[e["id"]] | {"kind": info[e["id"]].get("kind") or "error"}))
    return info, alone


def take(ref: str, got: list[dict], noted: set) -> bool:
    """An entry a note already gave edits to takes only the edits nothing else classifies."""
    got = [u for u in got if ref not in noted or u["how"] in (None, "set")]
    for u in got:
        u["ref"] = ref
    return bool(got)


def marked(hunks: list[dict], e: dict, fix, fb: list, fa: list) -> list[dict]:
    """In the blocks with the entry's comment: its units; without quotes to compare — else the ones nothing classified."""
    got = []
    for h in (h for h in hunks if e["id"] in h["refs"]):
        got += mine(h, fix, fb, fa) or ([] if fix else [u for u in free(h) if u["how"] in (None, "set")])
    return got


def search(hunks: list[dict], e: dict, fix, fb: list, fa: list) -> list[dict]:
    """A commented block that only kept its place has the fix next to it (a removed copy, an added word); without a
    comment — anywhere on the entry's slides. Blocks with another entry's comment are that entry's."""
    own_ = lambda h: all(r == e["id"] for r in h["refs"])
    at = [i for i, h in enumerate(hunks) if e["id"] in h["refs"]]
    if at:
        near = {j for i in at for j in range(i - 2, i + 3) if 0 <= j < len(hunks) and hunks[j]["slide"] == hunks[i]["slide"]}
        return best([hunks[j] for j in sorted(near) if own_(hunks[j])], fix, fb, fa, 0.2)
    return best([h for h in hunks if h["slide"] in e["slides"] and own_(h)], fix, fb, fa, LIKE)
