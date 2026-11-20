"""changes/notes/rules.json from GLOSSARY.md: the pairs «was → now» of its decisions table (column «Що замінити») and of
its list by lectures, cut to the edits the diff would make of them; what the machine classifies anyway (a dash, a dot)
is left out. The derived rules carry the note «словничок…» and are made anew each time; the others stay as they are."""
import re
from difflib import SequenceMatcher

import store
from classify import auto
from diff import edits

QUOTED = re.compile(r"«((?:[^«»]|«[^«»]*»)*)»|`([^`]+)`")
NOTE = "словничок"


def sides(text: str) -> tuple[str, str] | None:
    """A bullet «…» → «…» · N · сл. …: the two sides of the first arrow outside quotes."""
    depth, at = 0, None
    for i, c in enumerate(text):
        depth += (c == "«") - (c == "»")
        if c == "→" and depth == 0:
            at = i
            break
    return (text[:at], text[at + 1:].split(" · ")[0]) if at is not None else None


def items(side: str, quoted: bool) -> list[str]:
    """«a / b» and «a», «b» are two forms; a trailing «(…)» explains, it is not the text."""
    if quoted:
        found = [re.sub(r"(?<=\S) \([^()]*\)$", "", (a or b).replace("**", "")) for a, b in QUOTED.findall(side)]
        return [s.strip() for f in found for s in f.split(" / ")]
    side = re.sub(r"\([^)]*\)|\*\*|`|«|»", "", side)
    return [s.strip().rstrip("-") for s in re.split(r",| / ", side) if s.strip() and "…" not in s]


def pairs(left: list[str], right: list[str]) -> list[tuple[str, str]]:
    if len(right) == 1 or len(left) == 1:
        return [(a, b) for a in left for b in right]
    return list(zip(left, right))


def full(was: str, now: str) -> str:
    """The right side names only the changed words («…зміни розв'язку»): put them in place of the most alike ones."""
    w, n = was.split(), now.split()
    if len(n) >= len(w):
        return now
    like = lambda k: sum(SequenceMatcher(None, w[k + j].lower(), n[j].lower()).ratio() for j in range(len(n)))
    k = max(range(len(w) - len(n) + 1), key=lambda k: (like(k), -k))
    return " ".join(w[:k] + n + w[k + len(n):])


def cut(was: str, now: str) -> list[tuple[str, str]]:
    was, now = was.replace("…", " ").strip(), now.replace("…", " ").strip()
    return [(e["del"], e["ins"]) for e in edits(was, full(was, now)) if e["del"] and e["ins"] and not auto(e)]


def derive() -> str:
    text, found = (store.LECT / "GLOSSARY.md").read_text(), {}
    for m in re.finditer(r"^\| (\d+) \|[^|]*\|[^|]*\|([^|]*)\|", text, re.MULTILINE):
        for chunk in m.group(2).split(";"):
            if s := sides(chunk):
                for was, now in pairs(items(s[0], False), items(s[1], False)):
                    for d, i in cut(was, now):
                        found.setdefault((d, i), f"{NOTE}, п. {m.group(1)}")
    lec = "?"
    for line in text[text.find("## По лекціях"):].splitlines():
        if m := re.match(r"### Лекція (\d+)", line):
            lec = m.group(1)
        elif line.startswith("- ") and (s := sides(line[2:])):
            for was, now in pairs(items(s[0], True), items(s[1], True)):
                for d, i in cut(was, now):
                    found.setdefault((d, i), f"{NOTE}, лекція {lec}")
    path = store.NOTES / "rules.json"
    kept = [r for r in store.rules() if not r.get("note", "").startswith(NOTE)]
    rules = kept + [{"del": d, "ins": i, "kind": "term", "note": note} for (d, i), note in found.items()]
    store.NOTES.mkdir(parents=True, exist_ok=True)
    path.write_text(store.dump({"rules": rules}))
    return f"rules.json: зі словничка {len(found)} · своїх {len(kept)}"
