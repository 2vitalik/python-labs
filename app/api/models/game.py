from datetime import datetime, timezone
from typing import Annotated

from beanie import Document, Indexed
from pydantic import Field


class Game(Document):
    slug: Annotated[str, Indexed(unique=True)]
    title: str
    icon: str = ""
    klass: str = ""  # avatar | cursor | figure | puzzle
    axes: dict = {}  # {field, time, opponent, info, random, goal} — UA labels
    summary: str = ""
    description: str = ""  # markdown
    status: str = "draft"  # draft | active | archived
    order: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "games"

    def api(self) -> dict:
        return {
            "id": str(self.id), "slug": self.slug, "title": self.title, "icon": self.icon,
            "klass": self.klass, "axes": self.axes, "summary": self.summary,
            "description": self.description, "status": self.status, "order": self.order,
        }
