"""Where a journal's words stand in a block: the quotes «…» and formulas $…$ of `Було` / `Стало` / `Що бачу`, cut at «…»,
looked for token by token (the text may have moved on since the entry was written, so a near match counts)."""
import re
from difflib import SequenceMatcher

from tok import tokens

QUOTE = re.compile(r"«((?:[^«»]|«[^«»]*»)*)»|`([^`]+)`")
FORMULA = re.compile(r"\$[^$]+\$")


def fragments(text: str) -> list[list[str]]:
    """Quotes «…» and code `…` (not the fence lines `:::`), else the formulas, else the whole text."""
    found = [q for a, b in QUOTE.findall(text) if not (q := a or b).startswith(":::")]
    found = found or FORMULA.findall(text) or [text]
    parts = [p for f in found for p in re.split(r"…|\.\.\.", f)]
    return [k for p in parts if len(k := keys(p)) >= 2 or (k and len(k[0]) > 3)]


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
