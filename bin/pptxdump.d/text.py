"""Runs of a paragraph — the look each has as set on the slide itself (nothing inherited); OMML formulas with colour."""
from omml import lin
from ooxml import loc, q

SYMBOL_FONTS = ("Symbol", "Wingdings", "Wingdings 2", "Wingdings 3", "Webdings", "MT Extra")
PLAIN = (False, False, False, 0, None, None, None, None)


def is_pua(ch: str) -> bool:
    return 0xF000 <= ord(ch) <= 0xF0FF


def look(theme, rPr, text: str) -> tuple:
    """(bold, italic, underline, baseline, colour, size pt, glyph font, highlight); equal looks glue neighbour runs."""
    if rPr is None:
        return PLAIN
    face = lambda tag: rPr.find(q(tag)).get("typeface") if rPr.find(q(tag)) is not None else None
    latin, symf = face("a:latin"), face("a:sym")
    # a:sym applies only to private-use symbol chars; a symbol latin font turns every char into a glyph
    sym = latin if latin in SYMBOL_FONTS else (symf or latin) if any(map(is_pua, text)) else None
    hl = rPr.find(q("a:highlight"))
    return (rPr.get("b") == "1", rPr.get("i") == "1", rPr.get("u") not in (None, "none"), int(rPr.get("baseline", "0")),
            theme.color(rPr.find(q("a:solidFill"))), int(rPr.get("sz")) / 100 if rPr.get("sz") else None, sym,
            theme.color(hl) if hl is not None else None)


def formula_look(theme, m) -> tuple:
    """(the colour all its runs share, None) or, when they differ, (None, the linear text with coloured runs marked)."""
    hue = lambda r: theme.color(r.find(q("a:rPr") + "/" + q("a:solidFill")))
    hues = {hue(r) for r in m.iter(q("m:r")) if "".join(r.itertext()).strip()}
    if len(hues) <= 1:
        return next(iter(hues), None), None
    return None, lin(m, lambda r, t: f"[колір {h}]{t}[/]" if (h := hue(r)) and t.strip() else t).strip()


def pieces(theme, p) -> list[tuple]:
    out = []
    for c in p:
        n = loc(c)
        if n == "r":
            t = c.findtext(q("a:t")) or ""
            out.append(("text", t, look(theme, c.find(q("a:rPr")), t)))
        elif n == "br":
            out.append(("br", "\n", None))
        elif n == "fld":
            out.append(("field", c.findtext(q("a:t")) or "", c.get("type")))
        elif c.tag == q("a14:m"):
            out.append(("formula", lin(c).strip(), formula_look(theme, c)))
        elif n == "AlternateContent" and (choice := c.find(q("mc:Choice"))) is not None:
            out.extend(pieces(theme, choice))  # its children are a:r / a14:m
    return out


def run(kind: str, text: str, extra) -> dict:
    if kind == "field":
        return {"kind": kind, "field": extra, "text": text}
    if kind == "formula":
        return {"kind": kind, "text": text, "color": extra[0], "colored": extra[1]}
    if kind != "text":
        return {"kind": kind, "text": text}
    b, i, u, base, color, size, font, hl = extra
    return {"kind": kind, "text": text, "bold": b, "italic": i, "underline": u,
            "script": "sup" if base > 0 else "sub" if base < 0 else None,
            "color": color, "size": size, "font": font, "highlight": hl}
