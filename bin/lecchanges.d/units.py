"""What can be classified in a hunk — a unit: each edit of a pair, the pair's change of looks, a removed or added run.
Each gets its key (contract §3.2.6) and its class: the machine, the rules, the notes (§3.2.7)."""
import hashlib
from collections import Counter

from classify import auto, rule
from tok import bare


def units(h: dict) -> list[dict]:
    if not h.setdefault("units", []):
        h["units"] = list(h["edits"])
        if h["looks"]:
            h["units"].append({"del": " ".join(e["del"] for e in h["looks"]), "ins": " ".join(e["ins"] for e in h["looks"]),
                               "look": h["look"], "edits": h["looks"]})
        if not h["after"] or not h["before"]:  # a removed or added run: a unit per block, so a rule can name one of them
            at, gone = 0, bool(h["before"])
            for raw in h["parts"]:
                span, none = [at, at + len(raw)], [0, 0]
                h["units"].append({"del": bare(raw) if gone else "", "ins": "" if gone else bare(raw),
                                   "a": span if gone else none, "b": none if gone else span, "whole": True})
                at += len(raw) + 2
    return h["units"]


def keyed(hunks: list[dict]):
    """k + 8 hex of sha1(slide|del|ins|which such on the slide): the same while the edit is the same."""
    seen = Counter()
    for h in hunks:
        for u in units(h):
            ident = (h["slide"], u["del"], u["ins"])
            u["key"] = "k" + hashlib.sha1(f"{h['slide']}|{u['del']}|{u['ins']}|{seen[ident]}".encode()).hexdigest()[:8]
            seen[ident] += 1


def classed(hunks: list[dict], course: list[dict], notes: dict):
    """u["cls"]: kind, sev, note, origin, ref — what is known; u["how"]: auto · rule · key · None (still `todo`)."""
    for h in hunks:
        for u in units(h):
            u["cls"], u["how"] = {}, None
            if "look" in u:
                u["cls"], u["how"] = {"kind": u["look"], "origin": "site"}, "auto"
            elif "whole" in u:  # a removed or added run is known for what it is, though not why
                u["cls"]["kind"] = "removed" if not h["after"] else "pic2text" if "у тексті" in h["fence"] else "added"
                u["how"] = "set"
            elif h["where"] == "table" and set(u["del"] + u["ins"]) <= set("|:- "):  # a column's alignment `:-:` → `--:`
                u["cls"], u["how"] = {"kind": "markup", "origin": "site"}, "auto"
            elif k := auto(u):
                u["cls"], u["how"] = {"kind": k}, "auto"
            for rules in (course, notes.get("rules", [])):
                if "look" not in u and (r := rule(rules, u["del"], u["ins"])):
                    u["cls"], u["how"] = {k: v for k, v in r.items() if k not in ("del", "ins")}, "rule"
            if key := notes.get("keys", {}).get(u["key"]):
                u["cls"], u["how"] = dict(key), "key"
