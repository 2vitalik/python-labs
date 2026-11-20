"""The catalogue's words (contract §3.4) and what classifies an edit (§3.2.7): the machine — punctuation, case, apostrophes,
dashes, spacing → `punct`; a decimal comma → a dot, the spacing and wrapping of a formula → `notation`; then a pair
«del → ins» of the course's rules, then of the lecture's notes; a key in the notes is the strongest."""
import re

KINDS = {  # kind: (group, typical sev)
    "error": ("content", 3), "formula": ("content", 3), "number": ("content", 3), "gap": ("content", 2), "ref": ("content", 2),
    "ru": ("lang", 2), "calque": ("lang", 1), "term": ("lang", 1), "typo": ("lang", 1), "grammar": ("lang", 1),
    "style": ("lang", 1), "punct": ("lang", 0),
    "emph": ("look", 0), "markup": ("look", 0), "notation": ("look", 0), "heading": ("look", 0), "caption": ("look", 0),
    "pic2text": ("media", 1), "pic": ("media", 1),
    "removed": ("set", 2), "restored": ("set", 1), "added": ("set", 1),
    "doubt": ("open", 2), "layout": ("open", 1),
    "todo": ("todo", 1),  # most edits nobody named yet are of the language: «дрібно» till a note says
}
STATUS, WHERE, ORIGIN = ("fixed", "open", "noted"), ("text", "formula", "table", "heading", "caption", "alt", "slide"), ("slide", "convert", "site")
APOS = str.maketrans("’ʼ`", "'''")
DECIMAL = re.compile(r"(\d)(?:\{,\}|,)(\d)")
# what a formula may change without changing what it says: spacing, braces, text wrappers, sizes of brackets
LOOSE = re.compile(r"\s+|[{}]|\\(?:text|mathrm|operatorname|left|right|displaystyle|[,;:! ]|q?quad)(?![A-Za-z])|\\(?=\s|$)")


def words(s: str) -> list[str]:
    """Case does not count — but in a formula it does: x and X are two variables."""
    s = s.translate(APOS)
    return re.findall(r"\w+", s if "$" in s else s.lower())


def loose(s: str) -> str:
    for a, b in (("\\dfrac", "\\frac"), ("\\tfrac", "\\frac"), ("\\ldots", "\\dots")):
        s = s.replace(a, b)
    return LOOSE.sub("", s)


def auto(e: dict) -> str | None:
    """A word moved within its block — `style`; the same words in the same order (two words made one is not
    punctuation) — `punct`; inside a formula only its spacing and wrapping may differ, or a number became a formula
    (`-2` → `$-2$`) — `notation`; the sentence's own stops around a formula (`… = 0,$$`) — `punct`."""
    d, i = e["del"], e["ins"]
    if e.get("moved"):
        return "style"
    if d != i and DECIMAL.sub(r"\1.\2", d) == DECIMAL.sub(r"\1.\2", i):
        return "notation"
    if "$" in d + i and loose(d.replace("$", "")) == loose(i.replace("$", "")):
        return "notation"
    if e["math"]:
        return "notation" if loose(d) == loose(i) else "punct" if re.fullmatch(r"[.,;:\s]*", d + i) else None
    return "punct" if words(d) == words(i) else None


def stem(rule: dict, d: str, i: str) -> bool:
    """A one-word rule also takes the word's other endings: «X-а → Y-а» matches «X-ові → Y-ові»."""
    rd, ri = rule["del"], rule["ins"]
    if rd == d and ri == i:
        return True
    if " " in rd + ri + d + i or not rd or not ri:
        return False
    n = 0
    while n < min(len(rd), len(ri)) and rd[-1 - n] == ri[-1 - n]:
        n += 1
    sd, si = rd[:len(rd) - n], ri[:len(ri) - n]
    return d.startswith(sd) and i.startswith(si) and d[len(sd):] == i[len(si):] and abs(len(d) - len(rd)) <= 4


def rule(rules: list[dict], d: str, i: str) -> dict | None:
    return next((r for r in rules if stem(r, d, i)), None)


def problems(entry: dict, where: str) -> list[str]:
    """What is wrong in a note or a rule: an unknown kind, a weight outside 0–3, an unknown origin."""
    out = []
    if ("kind" in entry or "ref" not in entry) and (entry.get("kind") not in KINDS or entry.get("kind") == "todo"):
        out.append(f"{where}: kind «{entry.get('kind')}» нема в довіднику")
    if "sev" in entry and entry["sev"] not in (0, 1, 2, 3):
        out.append(f"{where}: sev {entry['sev']} — лише 0–3")
    if "origin" in entry and entry["origin"] not in ORIGIN:
        out.append(f"{where}: origin «{entry['origin']}» — лише {', '.join(ORIGIN)}")
    return out
