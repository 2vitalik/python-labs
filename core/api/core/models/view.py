from datetime import datetime, timezone

from beanie import Document
from pydantic import Field
from pymongo import IndexModel

from core.models.history import when


class View(Document):
    """A saved look at the table (T240): the columns, filters, sort and grouping as the URL carries them, under a name."""
    slug: str
    title: str
    emoji: str = ""
    query: dict = {}  # cols · group · sort · q · f.<column> — what /table?… holds
    order: int = 0
    by: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "views"
        indexes = [IndexModel([("slug", 1)], unique=True)]

    def api(self) -> dict:
        return {"slug": self.slug, "title": self.title, "emoji": self.emoji, "query": self.query, "order": self.order,
                "by": self.by.split("@")[0], "created_at": when(self.created_at)}
