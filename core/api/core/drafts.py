"""Drafts in guide text (T157): `<!-- … -->` is the admin's notes and unfinished parts, marked on the page (drafts.js).
`public()` is the page without them — what the admin sees with drafts switched off.
`<!-- слайд N -->` is not a draft: a slide's border in a lecture (T166 Q3), invisible on the page."""
import re

DRAFT = re.compile(r"<!--(?!\s*слайд\s).*?(?:-->|\Z)", re.S)  # an unclosed draft runs to the end of the text
BARE = re.compile(r"^[ \t]*(?:(?:[-*+]|\d+\.)[ \t]+)?\0[ \t\0]*(?:\n|\Z)", re.M)  # a line or a list item with nothing but drafts


def public(body: str) -> str:
    text = BARE.sub("", DRAFT.sub("\0", body))
    text = re.sub(r"[ \t]*\0", "", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()
