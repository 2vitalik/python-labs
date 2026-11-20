"""Units → the catalogue's items (contract §3.3): the units of one journal id in a hunk — one item; the machine's units
of one kind in a hunk (and the blocks of a removed or added run) — one item; every other unit — an item of its own.
An item without a class is `todo`."""
import re

from classify import KINDS
from units import units

SITE = ("emph", "markup", "pic2text")  # looks the site asked for: not the lecturer's doing


def records(lec: int, hunks: list[dict], info: dict) -> list[tuple[dict, dict]]:
    out = []
    for h in hunks:
        groups = {}
        for u in units(h):
            ref = u["cls"].get("ref") if u["how"] == "key" else u.get("ref")
            same = u["how"] in ("auto", "set")  # the machine's units of one kind in a hunk make one item
            g = ("ref", ref) if ref else (u["how"], u["cls"]["kind"]) if same else ("one", u["key"])
            groups.setdefault(g, []).append(u)
        for (by, name), us in groups.items():
            out.append((h, record(lec, h, us, info.get(name, {}) if by == "ref" else None, name if by == "ref" else "")))
    return out


def guess(us: list[dict], title: str) -> str:
    """An A entry's kind when no note names it: a missing word when its title says so, else an error in a formula or
    an error of content."""
    if re.search(r"пропущ", title, re.IGNORECASE):
        return "gap"
    return "formula" if us and all(u.get("math") for u in us) else "error"


def record(lec: int, h: dict, us: list[dict], inf: dict | None, ref: str) -> dict:
    keyed = next((u for u in us if u["how"] == "key" and u["cls"].get("kind")), None)
    cls = (keyed or us[0])["cls"] if keyed or inf is None else {}
    how = "key" if keyed else "journal" if inf is not None else us[0]["how"]
    kind = cls.get("kind") if how != "journal" else (inf.get("kind") or guess(us, inf.get("title", "")))
    kind = kind or "todo"
    group, sev = KINDS.get(kind, KINDS["todo"])  # a kind the catalogue does not know stays as written: `check` names it
    spans = [(e["a"], e["b"]) for u in us for e in (u["edits"] if "look" in u else [u])]
    return {
        "id": ref or f"{lec:02}-{us[0]['key']}", "lec": lec, "slide": h["slide"], "group": group, "kind": kind,
        "sev": cls.get("sev", sev) if how in ("key", "rule") else sev, "status": "fixed",
        "where": "formula" if all(u.get("math") for u in us) else h["where"],
        "origin": cls.get("origin") or (inf or {}).get("origin") or ("site" if kind in SITE else "slide"),
        "size": sum(len(u["del"]) + len(u["ins"]) for u in us), "auto": how == "auto",
        "verified": cls.get("verified", True) if how == "key" else how in ("auto", "journal"),
        "title": cls.get("title") or (inf or {}).get("title", ""), "note": cls.get("note", ""), "why": (inf or {}).get("why", ""),
        "ref": ref, "hunk": "", "how": how,  # del / ins — the raw texts at a / b: the page marks what it shows
        "edits": [{"del": h["before"][slice(*a)], "ins": h["after"][slice(*b)], "a": a, "b": b} for a, b in spans],
    }


def alone(lec: int, rec: dict) -> dict:
    """A journal entry standing on its own: a doubt, a layout case, an A or G that found no edits."""
    kind = "gap" if rec["kind"] == "error" and re.search(r"пропущ", rec["title"], re.IGNORECASE) else rec["kind"]
    return {"id": rec["id"], "lec": lec, "slide": 0, "group": KINDS[kind][0], "kind": kind, "sev": KINDS[kind][1],
            "status": rec.get("status", "fixed"), "where": "", "origin": rec.get("origin", "slide"), "size": 0, "auto": False,
            "verified": True, "title": rec["title"], "note": "", "why": rec["why"], "ref": rec["ref"], "hunk": "", "edits": [],
            "how": "journal"}


def override(items: list[dict], ids: dict):
    """The notes' word on a journal entry (`ids`: kind, sev, origin, note, status) — on every item of it."""
    for it in items:
        if o := ids.get(it["ref"]):
            if "kind" in o:
                it["kind"], (it["group"], it["sev"]) = o["kind"], KINDS.get(o["kind"], KINDS["todo"])
            it.update({k: o[k] for k in ("sev", "origin", "note", "status") if k in o})
