from datetime import datetime, timezone
from typing import Annotated

from beanie import Document, Indexed
from pydantic import Field

from models.history import record

DRAFT = "changes-draft"  # admin-only page: «Що змінилось» draft fed by edit notes (T126 §5b)


class Guide(Document):
    """A guide page: markdown after the title line. Truth lives here; data/guide/*.md is the seed and export (guide_io.py)."""
    slug: Annotated[str, Indexed(unique=True)]
    title: str
    body: str
    rev: int = 0  # bumped on every save; PUT carries the rev it saw → 409 on a stale one
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_by: str = ""

    class Settings:
        name = "guide"

    def api(self) -> dict:
        return {"slug": self.slug, "title": self.title, "body": self.body, "rev": self.rev,
                "updated": self.updated_at.isoformat(), "updated_by": self.updated_by.split("@")[0]}


async def save(g: Guide, title: str, body: str, actor: str, note: str = "") -> bool:
    """Record a new version; False when nothing changed."""
    if (g.title, g.body) == (title, body):
        return False
    g.rev, g.updated_at, g.updated_by = g.rev + 1, datetime.now(timezone.utc), actor
    await record(g, {"title": title, "body": body}, actor=actor, note=note)
    return True
