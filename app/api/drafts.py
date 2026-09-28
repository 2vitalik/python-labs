"""Drafts in guide text (T157): `<!-- … -->` is what students do not get. The admin sees it marked (drafts.js),
everyone else gets `public()` of the page."""
import re

DRAFT = re.compile(r"<!--.*?(?:-->|\Z)", re.S)  # an unclosed draft runs to the end of the text
BARE = re.compile(r"^[ \t]*(?:(?:[-*+]|\d+\.)[ \t]+)?\0[ \t\0]*(?:\n|\Z)", re.M)  # a line or a list item with nothing but drafts


def public(body: str) -> str:
    text = BARE.sub("", DRAFT.sub("\0", body))
    text = re.sub(r"[ \t]*\0", "", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def closed(body: str) -> str:
    """Every `##` section, and the lead above the first one, as a draft of its own (`bin/guide close`)."""
    parts = re.split(r"^(?=## )", body.replace("<!--", "").replace("-->", ""), flags=re.M)
    return "\n\n".join(f"<!--\n{p.strip()}\n-->" for p in parts if p.strip())
