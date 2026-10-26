from datetime import datetime, timezone
from beanie import Document
from pydantic import Field
from pymongo import IndexModel

from core.models.history import when


class LabVariant(Document):
    """A student's variant of a lab (T200): the card the site hands out, the answers it checks a line against, the line and the mark.
    Made on disk by the lab's generator (outside git) and imported by lab_io.py; the answers never leave the server."""
    lab: int
    group: str
    n: int  # number among the group's cards; 0 — the demo, never handed out by the site
    vid: str  # КН-23-1-07; unique together with `lab`: every lab numbers its cards the same way
    card: str  # the python block the student pastes into the notebook
    ask: list[str] = []  # defence questions
    answers: dict = {}  # name → {value, room, traps: [{value, why}]}
    student: str = ""  # email; "" — free
    assigned_at: datetime | None = None
    line: str = ""
    values: dict = {}
    verdict: dict = {}  # name → {ok, why}
    notebook: str = ""
    attempts: int = 0
    checked_at: datetime | None = None
    points: int | None = None
    note: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "variants"
        indexes = ["group", "student", IndexModel([("lab", 1), ("vid", 1)], unique=True)]

    def api(self) -> dict:
        """What the student sees: no answers, no traps."""
        return {"lab": self.lab, "vid": self.vid, "card": self.card, "ask": self.ask, "verdict": self.verdict,
                "ok": sum(v["ok"] for v in self.verdict.values()), "total": len(self.answers), "line": self.line,
                "notebook": self.notebook, "attempts": self.attempts, "checked_at": when(self.checked_at),
                "points": self.points, "note": self.note}

    def row(self) -> dict:
        """A line of the teacher's table."""
        return self.api() | {"group": self.group, "n": self.n, "student": self.student, "assigned_at": when(self.assigned_at)}
