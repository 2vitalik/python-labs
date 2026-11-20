"""The edits between two raw texts (contract §3.2.4–5): a token diff, neighbouring tokens merged into one edit; each edit
knows what went (`del`), what came (`ins`) and where both stand in the raw texts (`a`, `b`)."""
from difflib import SequenceMatcher

from cells import moved, split
from tok import clean, inside, math, raw_tokens, squeeze, tokens

EMPH = ("**", "*", "<c-", "</c-", "\\col{", "}")  # `}` as markup is the end of a coloured part of a formula (tok.wraps)
STOPS = (".", ",", ";", ":", "-")  # what one edit may step over, close up: `Рис.1` → `рис. 1`, `П-З` → `причинно-…`


def ops(x: list, y: list, spaced: bool = True) -> list[tuple]:
    key = (lambda t: t[0]) if spaced else (lambda t: t[0].strip())
    sm = SequenceMatcher(None, [key(t) for t in x], [key(t) for t in y], autojunk=False)
    return [o for o in sm.get_opcodes() if o[0] != "equal"]


def at(toks: list, i: int, j: int) -> list[int]:
    if i < j:
        return [toks[i][1], toks[j - 1][2]]
    p = toks[i - 1][2] if i else toks[0][1] if toks else 0
    return [p, p]


def say(text: str, toks: list, i: int, j: int) -> str:
    return squeeze(text[toks[i][3]:toks[j - 1][4]]) if i < j else ""


def joined(x: list, y: list, mx: list, my: list, found: list[tuple]) -> list[tuple]:
    """Edits one stop apart or, inside a formula (then or now: `-2` → `$-2$`), up to three tokens apart — one edit:
    a rebuilt formula reads as one change, not as a scatter of braces."""
    out = []
    for _, i, j, k, l in found:
        if out:
            gap, gap2 = x[out[-1][2]:i], y[out[-1][4]:k]
            formula = (gap and all(inside(t[1], mx) for t in gap)) or (gap2 and all(inside(t[1], my) for t in gap2))
            if (formula and len(gap) <= 3) or (len(gap) == 1 and gap[0][0] in STOPS):
                out[-1] = (None, out[-1][1], j, out[-1][3], l)
                continue
        out.append((None, i, j, k, l))
    return out


def edits(before: str, after: str) -> list[dict]:
    """Word edits; a change of spacing alone takes the token before it along, so the edit shows."""
    x, y, cx, cy = tokens(before), tokens(after), clean(before)[0], clean(after)[0]
    mx, my, out = math(before), math(after), []
    for _, i, j, k, l in joined(x, y, mx, my, split(x, y, mx, my, ops(x, y))):
        if say(cx, x, i, j) == say(cy, y, k, l) and i and k:
            i, k = i - 1, k - 1
        sides = [inside(t[1], mx) for t in x[i:j]] + [inside(t[1], my) for t in y[k:l]]
        out.append({"del": say(cx, x, i, j), "ins": say(cy, y, k, l), "a": at(x, i, j), "b": at(y, k, l), "math": all(sides)})
    return moved(out)


def looks(before: str, after: str, only_markup: bool) -> tuple[list[dict], str]:
    """Edits of the markup (bold, colour, list and quote marks, heading hashes) and the kind of them: `emph` when only
    stars and colour tags changed, else `markup`. only_markup — drop the edits that touch words (they are `edits`).
    Spacing is not compared here: a tag before a word must not take the word along."""
    x, y, out, kinds = raw_tokens(before), raw_tokens(after), [], set()
    for _, i, j, k, l in ops(x, y, spaced=False):
        part = x[i:j] + y[k:l]
        if only_markup and not all(t[5] for t in part):
            continue
        kinds |= {"emph" if t[0].strip().startswith(EMPH) else "markup" for t in part if t[5]}
        out.append({"del": squeeze(before[slice(*at(x, i, j))]), "ins": squeeze(after[slice(*at(y, k, l))]),
                    "a": at(x, i, j), "b": at(y, k, l)})
    return out, "markup" if "markup" in kinds or not kinds else "emph"
