from datetime import datetime, timezone
from typing import Annotated

from beanie import Document, Indexed, PydanticObjectId
from pydantic import Field


class Work(Document):
    owner: Annotated[str, Indexed(unique=True)]  # user email; one game per student
    title: str
    base_game: str = ""  # catalog game slug; "" = custom base
    base_custom: str = ""  # free-text base when not from the catalog
    description: str = ""  # markdown
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "works"

    def api(self) -> dict:
        return {
            "id": str(self.id), "owner": self.owner, "title": self.title,
            "base_game": self.base_game, "base_custom": self.base_custom,
            "description": self.description, "created_at": self.created_at.isoformat(),
        }


class WorkObject(Document):
    work: Annotated[PydanticObjectId, Indexed()]
    kind: str  # window | menu
    title: str
    task: str = ""  # window type: catalog task slug tagged "window"
    description: str = ""
    screenshots: list[str] = []  # file names under uploads/<work-id>/
    window: str = ""  # menu: id of the host window object
    items: list[dict] = []  # menu: {title, window: obj id, task: slug, note}
    order: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "work_objects"

    def api(self) -> dict:
        return {
            "id": str(self.id), "work": str(self.work), "kind": self.kind, "title": self.title,
            "task": self.task, "description": self.description, "screenshots": self.screenshots,
            "window": self.window, "items": self.items, "order": self.order,
            "created_at": self.created_at.isoformat(),
        }


class Claim(Document):
    work: Annotated[PydanticObjectId, Indexed()]
    task: str  # catalog task slug
    object: str = ""  # WorkObject id; "" = game-level claim
    note: str = ""
    link: str = ""  # GitHub link (commit-pin normalization — later phase)
    status: str = "claimed"  # lifecycle grows with reports node (T10)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "claims"

    def api(self) -> dict:
        return {
            "id": str(self.id), "work": str(self.work), "task": self.task, "object": self.object,
            "note": self.note, "link": self.link, "status": self.status,
            "created_at": self.created_at.isoformat(),
        }
