"""Where a journal's words stand in a block: the quotes «…» and formulas $…$ of `Було` / `Стало` / `Що бачу`, cut at «…»,
looked for token by token (the text may have moved on since the entry was written, so a near match counts)."""
import re
from collections import Counter
from difflib import SequenceMatcher

from diff import edits
from tok import TOKEN, tokens

QUOTE = re.compile(r"«((?:[^«»]|«[^«»]*»)*)»|`([^`]+)`")
FORMULA = re.compile(r"\$[^$]+\$")
SIGNS = {".", ",", ";", ":", "$", "{", "}", "(", ")", "^", "\\", "…"}
DOTS = {"\\ldots": "\\dots", "\\cdots": "\\dots"}


def quoted(text: str) -> list[str]:
    """Quotes «…» and code `…` (not the fence lines `:::`), else the formulas."""
    return [q for a, b in QUOTE.findall(text) if not (q := a or b).startswith(":::")] or FORMULA.findall(text)


def fragments(text: str) -> list[list[str]]:
    """The quoted words, cut at «…»; no quotes — the whole text."""
    parts = [p for f in quoted(text) or [text] for p in re.split(r"…|\.\.\.", f)]
    return [k for p in parts if len(k := keys(p)) >= 2 or (k and len(k[0]) > 3)]


def bag(text: str) -> Counter:
    """The tokens of a bare text (no markup left to skip: a leading «-» is a minus, not a list's mark); the dots of
    a formula are one token whichever way written — a fix and `\\dots` → `\\ldots` share an edit often."""
    return Counter(DOTS.get(t, t) for t in TOKEN.findall(text))


def changes(was: str, now: str) -> tuple[Counter, Counter] | None:
    """What the journal's own `Було` → `Стало` takes away and brings, token by token; None — one side quotes nothing."""
    qb, qa = quoted(was), quoted(now)
    if not qb or not qa:
        return None
    found = edits(" … ".join(qb), " … ".join(qa))
    return sum((bag(e["del"]) for e in found), Counter()), sum((bag(e["ins"]) for e in found), Counter())


def stem(t: str) -> str:
    """A word without its ending: the journal quotes «значущим», the text has «значущою»."""
    return t[:max(4, len(t) - 3)] if t.isalpha() and len(t) > 4 else t


def words(b: Counter) -> Counter:
    return Counter(stem(t) for t in b.elements() if t not in SIGNS)


def fits(u: dict, fix: tuple[Counter, Counter]) -> bool:
    """An edit is the journal's fix when what it really takes away and brings (its common words, stops, brackets and
    dollars aside) is in the fix; an edit that only changes endings or order — when its words are in the fix; an edit
    of signs alone — when the fix has those signs."""
    d, i, fd, fi = bag(u["del"]), bag(u["ins"]), *fix
    wd, wi = words(d), words(i)
    if wd - wi or wi - wd:
        return wd - wi <= words(fd) and wi - wd <= words(fi)
    if [t for t in TOKEN.findall(u["del"]) if t not in SIGNS] != [t for t in TOKEN.findall(u["ins"]) if t not in SIGNS]:
        return bool(wd & words(fd) or wi & words(fi))
    return bool(d - i or i - d) and d - i <= fd and i - d <= fi


def keys(raw: str) -> list[str]:
    return [t[0].strip().lower() for t in tokens(raw)]


def find(frags: list[list[str]], raw: str) -> tuple[float, tuple[int, int] | None]:
    """(how well the best fragment is found — its share of tokens, less for a fragment shorter than three tokens;
    the span in raw from the first to the last token of the fragments found at least by half)."""
    toks = tokens(raw)
    hay, score, spans = [t[0].strip().lower() for t in toks], 0.0, []
    for frag in frags:
        blocks = SequenceMatcher(None, frag, hay, autojunk=False).get_matching_blocks()
        got = [b for b in blocks if b.size and (b.size > 1 or len(frag) < 4)]
        n = sum(b.size for b in got)
        if got and n >= 0.5 * len(frag):
            score = max(score, n / len(frag) * min(1.0, len(frag) / 3))
            spans.append((toks[got[0].b][1], toks[got[-1].b + got[-1].size - 1][2]))
    if not spans:
        return 0.0, None
    return score, (min(s for s, _ in spans), max(e for _, e in spans))
