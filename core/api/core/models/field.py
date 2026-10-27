from datetime import datetime, timezone
from typing import Any, Literal

from beanie import Document
from pydantic import BaseModel, Field as Attr
from pymongo import IndexModel

from core.models.history import when

Type = Literal["bool", "select", "multi", "number", "text", "date"]
Scope = Literal["student", "lab"]  # a value per student, or per student × lab
COLORS = ("gray", "red", "orange", "yellow", "green", "teal", "blue", "purple", "pink")


class Option(BaseModel):
    """One answer of a select: `id` stays when the text changes, so the values written keep their meaning."""
    id: str
    text: str
    emoji: str = ""
    color: str = ""  # one of COLORS; "" — none


class Field(Document):
    """A column the teacher made up (T240): a checkbox, a choice, a number, a note — on every student, or on every student × lab."""
    key: str  # slug of the title, unique; the column's name in a view
    title: str
    emoji: str = ""
    type: Type
    options: list[Option] = []  # select and multi only
    scope: Scope = "student"
    order: int = 0
    by: str = ""
    created_at: datetime = Attr(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "fields"
        indexes = [IndexModel([("key", 1)], unique=True)]

    def api(self) -> dict:
        return {"key": self.key, "title": self.title, "emoji": self.emoji, "type": self.type, "options": [o.model_dump() for o in self.options],
                "scope": self.scope, "order": self.order, "by": self.by.split("@")[0], "created_at": when(self.created_at)}


class FieldValue(Document):
    """What the teacher put in that column for one student — and one lab, for a `lab` field. One document per cell,
    rewritten with history; cleared = deleted."""
    user: str  # email
    field: str  # Field.key
    lab: int = 0  # 0 — a student-wide field
    value: Any = None  # as the field's type says: bool · option id · [option ids] · number · text · ISO date
    by: str = ""
    at: datetime = Attr(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "field_values"
        indexes = [IndexModel([("user", 1), ("field", 1), ("lab", 1)], unique=True), "field"]

    @property
    def column(self) -> str:
        """The row's key of this value: `done` or `quality.2`."""
        return f"{self.field}.{self.lab}" if self.lab else self.field
