from datetime import datetime, timezone

from beanie import Document
from pydantic import Field


class Ref(Document):
    """The finds' inbox (T98 Д2-Д3, T274 §4): a link from the web, an idea of a card, a word on a card or on the site."""
    url: str = ""
    kind: str = "link"  # link | idea | fix (about a card) | site
    parent: str = ""  # idea under a find: that ref's id
    title: str = ""
    note: str = ""
    zone: str = ""  # what it is about: a category of the catalog, maybe a subcategory (zones.ZONES)
    subzone: str = ""
    task: str = ""  # the card it is about (a fix), or the card a find became an example of (Д3)
    author: str  # user email
    status: str = "inbox"  # inbox | linked | dropped — нове · взято · ні, the teacher's
    reply: str = ""  # the teacher's line with the status
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "refs"

    def api(self) -> dict:
        return {
            "id": str(self.id), "url": self.url, "title": self.title, "note": self.note,
            "kind": self.kind, "parent": self.parent, "zone": self.zone, "subzone": self.subzone,
            "author": self.author.split("@")[0], "status": self.status, "reply": self.reply, "task": self.task,
            "created_at": self.created_at.isoformat(),
        }
