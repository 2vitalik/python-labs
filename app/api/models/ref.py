from datetime import datetime, timezone

from beanie import Document
from pydantic import Field


class Ref(Document):
    """Reference inbox item: a game find from YouTube/web, sorted into the corpus later (T98 Д2-Д3)."""
    url: str
    title: str = ""
    note: str = ""
    author: str  # user email
    status: str = "inbox"  # inbox | linked | dropped — lifecycle grows with Д3
    task: str = ""  # Д3: catalog card slug once the find becomes its example
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "refs"

    def api(self) -> dict:
        return {
            "id": str(self.id), "url": self.url, "title": self.title, "note": self.note,
            "author": self.author.split("@")[0], "status": self.status, "task": self.task,
            "created_at": self.created_at.isoformat(),
        }
