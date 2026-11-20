"""Glyphs layout.md spells out: Wingdings private-use chars by code (with a lookalike), a paragraph's level / bullet."""
from text import SYMBOL_FONTS, is_pua

# Wingdings private-use glyphs with a safe Unicode lookalike; others are shown by code only
WINGDINGS = {0xE8: "➔", 0xD8: "➢", 0x76: "❖", 0x7A: "⌘", 0x6C: "●", 0x6E: "■", 0xA7: "▪", 0xFC: "✔", 0x46: "☞", 0x71: "❑"}
ALIGN = {"ctr": "центр", "r": "право"}


def pua(text: str, font: str | None) -> str:
    out = []
    for ch in text:
        look = WINGDINGS.get(ord(ch) - 0xF000) if font == "Wingdings" and is_pua(ch) else None
        out.append(f"U+{ord(ch):04X}" + (f"≈{look}" if look else "") if is_pua(ch) else ch)
    return "".join(out)


def prefix(p: dict) -> str:
    tags = [f"L{p['level']}"] + ([ALIGN[p["align"]]] if p["align"] in ALIGN else [])
    b, mark = p["bullet"], ""
    if b and "char" in b:
        ch, font = b["char"], b["font"]
        look = WINGDINGS.get(ord(ch[0]) & 0xFF) if font == "Wingdings" and ch else None
        mark = f"маркер «{pua(ch, font)}»" + (f" ({font}{' ≈' + look if look else ''})" if font in SYMBOL_FONTS else "") + " "
    elif b:
        mark = f"нумерація {b['autonum']} "
    return f"[{' '.join(tags)}] {mark}"
