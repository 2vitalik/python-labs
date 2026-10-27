from datetime import datetime, timezone

from beanie import Document
from core.models.history import when
from pydantic import Field
from pymongo import IndexModel


class Deadline(Document):
    """When a lab is due (T235): for everyone (`groups` empty) or for the groups named — the narrower one wins."""
    lab: int
    at: datetime
    groups: list[str] = []
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "deadlines"

    def api(self) -> dict:
        return {"id": str(self.id), "lab": self.lab, "at": when(self.at), "groups": self.groups}


class LabMark(Document):
    """The teacher's word on one student and one lab (T235): an extension, a verdict, a note. One document per pair;
    every change is a row of `history`."""
    user: str  # email
    lab: int
    until: datetime | None = None  # extended to this moment
    open: bool = False  # extended, the date not known yet
    reason: str = ""
    met: bool | None = None  # True — on time, False — not; None — as the site counts
    note: str = ""
    asked: bool = False  # the student asked for an extension (T240) — whether or not one was given
    asked_for: str = ""  # …and for how long, in their words: «на тиждень», «до 5.11»
    by: str = ""  # who last touched it
    at: datetime | None = None

    class Settings:
        name = "lab_marks"
        indexes = [IndexModel([("user", 1), ("lab", 1)], unique=True)]

    def api(self) -> dict:
        return {"until": when(self.until), "open": self.open, "reason": self.reason, "met": self.met, "note": self.note, "asked": self.asked, "asked_for": self.asked_for,
                "by": self.by.split("@")[0], "at": when(self.at)}
