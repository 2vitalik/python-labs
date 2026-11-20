"""A lecture's text → slides → blocks (contract §3.2.1–2): a paragraph, a list item with its continuation lines, a table,
a formula, a heading, a picture. Fence lines `:::` and comments are not blocks; a journal id in a comment goes to the block
it stands in, a comment on a line of its own — to the block before it."""
import re
import textwrap

from tok import bare, tokens

SLIDE = re.compile(r"^<!-- слайд (\d+) -->\s*$")
REF = re.compile(r"<!--[^>]*?\b(\d{2}-[A-Z]\d+)\b[^>]*?-->")
QUOTE = re.compile(r"^[ \t]*(?:>[ \t]?)*[ \t]*")
ITEM = re.compile(r"(?:[-+*]|\d+[.)])[ \t]")
CAPTION = re.compile(r"(?:Рис|Табл)\.?\s*\d|Рисунок\s+\d|Таблиця\s+\d")


def slides(text: str) -> dict[int, list[dict]]:
    out, n, lines = {}, 0, []
    for line in text.splitlines():
        if m := SLIDE.match(line):
            out[n] = blocks(lines)
            n, lines = int(m.group(1)), []
        else:
            lines.append(line)
    out[n] = blocks(lines)
    return out


def kind(first: str) -> str:
    return ("heading" if first.startswith("#") else "table" if first.startswith("|") else "image" if first.startswith("![")
            else "math" if first.startswith("$$") else "item" if ITEM.match(first) else "para")


def blocks(lines: list[str]) -> list[dict]:
    out, cur, fence, pending = [], None, [], []
    for line in lines:
        inner = QUOTE.sub("", line)
        if line.startswith(":::"):
            name = line[3:].strip()
            if not name:
                fence = fence[:-1]
            elif name != "колонка":  # a column's start inside `::: колонки`, not a region of its own
                fence = fence + [name]
            cur = None
            continue
        if REF.fullmatch(line.strip()):
            (out[-1]["refs"] if out else pending).extend(REF.findall(line))
            cur = None
            continue
        if not inner.strip():
            cur = None
            continue
        k, depth = kind(inner), line[:len(line) - len(inner)].count(">")
        if (cur is None or k in ("heading", "image", "math", "item") or (k == "table") != (cur["kind"] == "table")
                or depth != cur["depth"]):
            cur = {"kind": k, "lines": [], "refs": pending, "fence": " › ".join(fence), "depth": depth}
            pending = []
            out.append(cur)
        cur["lines"].append(line)
        cur["refs"].extend(REF.findall(line))
        if k in ("heading", "image", "math"):
            cur = None
    for b in out:
        b["raw"] = textwrap.dedent("\n".join(b.pop("lines"))).strip("\n")
        b["bare"], b["tokens"] = bare(b["raw"]), tokens(b["raw"])
        if b["kind"] in ("para", "item") and CAPTION.match(b["bare"]):
            b["kind"] = "caption"
    return out
