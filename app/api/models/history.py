from datetime import datetime, timezone

from beanie import Document, PydanticObjectId
from pydantic import Field


class Change(Document):
    coll: str
    doc_id: PydanticObjectId
    actor: str  # email of who made the change
    at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    changes: dict  # {field: {"old": ..., "new": ...}}

    class Settings:
        name = "history"
        indexes = ["coll", "doc_id"]


async def record(doc: Document, data: dict, actor: str):
    """Apply `data` to `doc`, saving a diff of what actually changed."""
    changes = {k: {"old": getattr(doc, k), "new": v} for k, v in data.items() if getattr(doc, k) != v}
    if not changes:
        return
    for k, v in data.items():
        setattr(doc, k, v)
    await doc.save()
    await Change(coll=doc.Settings.name, doc_id=doc.id, actor=actor, changes=changes).insert()


async def record_new(doc: Document, actor: str):
    """Log document creation: every non-empty field as old=None."""
    data = doc.model_dump(exclude={"id", "created_at"})
    changes = {k: {"old": None, "new": v} for k, v in data.items() if v}
    await Change(coll=doc.Settings.name, doc_id=doc.id, actor=actor, changes=changes).insert()
