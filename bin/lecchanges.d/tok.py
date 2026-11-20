"""A block's raw text as the diff sees it: the formulas, the markup it steps over, the tokens and the bare form.

A token is (key, raw start, raw end, clean start, clean end); its key carries a leading space when one stands before it,
so a change of spacing alone is a change of a token and a run of changed words stays one opcode."""
import re

MATH = re.compile(r"\$\$.+?\$\$|(?<!\\)\$(?:\\.|[^$\\])+?\$", re.DOTALL)
# what the bare form drops: comments, the lecturer's colour tags, bold and italic stars, a line's indent with its quote and
# list marks, heading hashes (contract §3.2.3)
SKIP = re.compile(r"<!--.*?-->|</?c-[a-z]>|\*\*?|^[ \t]*(?:(?:>|(?:[-+*]|\d+[.)]|#+)(?=[ \t]))[ \t]*)*", re.MULTILINE | re.DOTALL)
TOKEN = re.compile(r"\\[A-Za-z]+|\\.|\d+(?:[.,]\d+)?|\w+(?:['’ʼ]\w+)*|\S")
# the same with the markup kept as tokens: what a change of looks only (bold, colour, list marks) is made of
RAW = re.compile(r"<!--.*?-->|</?c-[a-z]>|\*\*|\\col\{[a-z]\}\{|\\[A-Za-z]+|\\.|\d+(?:[.,]\d+)?|\w+(?:['’ʼ]\w+)*|\S", re.DOTALL)
COL = re.compile(r"\\col\{[a-z]\}\{")  # the lecturer's colour on a part of a formula: `\col{b}{…}` (T381)


def math(raw: str) -> list[tuple[int, int]]:
    return [m.span() for m in MATH.finditer(raw)]


def inside(pos: int, spans: list[tuple[int, int]]) -> bool:
    return any(s <= pos < e for s, e in spans)


def wraps(raw: str, spans: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """In the formulas: the opening `\\col{b}{` of a coloured part and the brace that closes it."""
    out = []
    for start, end in spans:
        for m in COL.finditer(raw, start, end):
            depth, i = 1, m.end()
            while i < end and depth:
                if raw[i - 1] != "\\":
                    depth += (raw[i] == "{") - (raw[i] == "}")
                i += 1
            if not depth:
                out += [m.span(), (i - 1, i)]
    return out


def skipped(raw: str) -> list[tuple[int, int]]:
    """Spans of markup; inside formulas nothing is markup but the colour of a part."""
    spans = math(raw)
    out = [m.span() for m in SKIP.finditer(raw) if m.end() > m.start() and not inside(m.start(), spans)]
    return sorted(out + wraps(raw, spans))


def clean(raw: str) -> tuple[str, list[int]]:
    """The text without the markup, and for every char of it — its place in raw."""
    text, where, at = [], [], 0
    for s, e in skipped(raw):
        text.append(raw[at:s])
        where.extend(range(at, s))
        at = e
    text.append(raw[at:])
    where.extend(range(at, len(raw)))
    return "".join(text), where


def tokens(raw: str) -> list[tuple]:
    text, where = clean(raw)
    out = []
    for m in TOKEN.finditer(text):
        s, e = m.span()
        space = " " if out and (s == 0 or text[s - 1].isspace()) else ""
        out.append((space + m.group(), where[s], where[e - 1] + 1, s, e))
    return out


def raw_tokens(raw: str) -> list[tuple]:
    """Tokens of the raw text itself, markup included (comments left out), each with a flag «it is markup»:
    for the records of looks."""
    skip, out = skipped(raw), []
    for m in RAW.finditer(raw):
        if m.group().startswith("<!--"):
            continue
        s, e = m.span()
        space = " " if out and raw[s - 1].isspace() else ""
        out.append((space + m.group(), s, e, s, e, inside(s, skip)))
    return out


def squeeze(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def bare(raw: str) -> str:
    return squeeze(clean(raw)[0])
