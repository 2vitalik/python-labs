"""Lecture texts as the search sees them: Markdown → plain words."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LECTURES = ROOT / "sites" / "ods" / "data" / "lectures"
SEARCH = LECTURES / "search"

LETTER = "A-Za-zЀ-ӿ"
WORD = re.compile(rf"[{LETTER}]+(?:['’ʼ-][{LETTER}]+)*")
CYRILLIC = re.compile("[Ѐ-ӿ]")

STRIP = [  # order matters: formulas may hold '<' and ']', so they go before tags and links
    (re.compile(r"^[ \t]*:::.*$", re.M), " "),
    (re.compile(r"<!--.*?-->", re.S), " "),
    (re.compile(r"\$\$.*?\$\$", re.S), " "),
    (re.compile(r"\$[^$\n]*\$"), " "),
    (re.compile(r"`[^`\n]*`"), " "),
    (re.compile(r"!?\[([^\]\n]*)\]\([^)\n]*\)"), r" \1 "),
    (re.compile(r"https?://\S+"), " "),
    (re.compile(r"</?[A-Za-z][^<>\n]*>"), ""),  # colour tags sit flush against words
]


def texts() -> dict[str, str]:
    return {p.stem: p.read_text(encoding="utf-8") for p in sorted(LECTURES.glob("lec[0-9][0-9]/lec[0-9][0-9].md"))}


def plain(md: str) -> str:
    for pattern, repl in STRIP:
        md = pattern.sub(repl, md)
    return md


def norm(word: str) -> str:
    return word.lower().replace("’", "'").replace("ʼ", "'")


def tokens(text: str) -> list[str]:
    """Words as written (case kept), 2+ letters."""
    return [w for w in WORD.findall(text) if len(w) >= 2]


def tally(docs: dict[str, str]) -> dict[str, set[str]]:
    """Lowercase word → how it is written: 'lower', 'title', 'caps'."""
    seen: dict[str, set[str]] = {}
    for text in docs.values():
        for w in tokens(plain(text)):
            letters = [c for c in w if c.isalpha()]
            look = "caps" if all(c.isupper() for c in letters) else "title" if letters[0].isupper() else "lower"
            seen.setdefault(norm(w), set()).add(look)
    return seen
