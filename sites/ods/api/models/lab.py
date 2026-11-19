from datetime import datetime, timezone
from beanie import Document
from pydantic import Field
from pymongo import IndexModel

from core.models.history import when
from labs_grade import grade

# a card as nobody worked on it: freed by the teacher or the demo taken over (history keeps what was)
FRESH = {"line": "", "values": {}, "verdict": {}, "notebook": "", "attempts": 0, "checked_at": None, "points": None, "note": "",
         "way": "", "video": "", "defended": "", "stars": None, "files": 0, "file": {}, "facts": {}, "live": {}, "live_at": None}


class LabVariant(Document):
    """A student's variant of a lab (T200, T354): the card the site hands out, the answers it checks a line against, the line,
    the notebook file, the defence and the mark. Made on disk by the lab's generator (outside git) and imported by lab_io.py;
    the answers never leave the server."""
    lab: int
    group: str
    n: int  # number among the group's cards — the student's number in the stream's list; 0 — the demo
    vid: str  # ПЗПІ-24-07; unique together with `lab`: every lab numbers its cards the same way
    card: str  # the python block the student pastes into the notebook
    ask: list[str] = []  # defence questions
    answers: dict = {}  # name → {value, step, traps: [{value, why}]}
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
    way: str = ""  # how the student means to defend: none · record · live
    video: str = ""  # a link to the recording
    defended: str = ""  # the defence the teacher accepted: record · live
    stars: int | None = None  # the teacher's word on the stars; None — as the file shows
    files: int = 0  # versions of the notebook handed in
    file: dict = {}  # the last one: FILE (models/lab_file.py)
    facts: dict = {}  # FACTS of the last version (labs_facts.py)
    token: str = ""  # check() of the notebook reports to the site with it (routes/lab_live.py)
    live: dict = {}  # name → {ok, value, tries, at}
    live_at: datetime | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "variants"
        indexes = ["group", "student", IndexModel([("lab", 1), ("vid", 1)], unique=True)]

    def right(self) -> int:
        return sum(v["ok"] for v in self.verdict.values())

    def grade(self) -> dict:
        return grade(self.right(), len(self.answers), self.attempts > 0, self.facts, self.stars, self.defended or self.way)

    def base(self) -> dict:
        return {"lab": self.lab, "vid": self.vid, "card": self.card, "ask": self.ask, "verdict": self.verdict, "ok": self.right(),
                "total": len(self.answers), "line": self.line, "notebook": self.notebook, "attempts": self.attempts,
                "checked_at": when(self.checked_at), "points": self.points, "note": self.note, "way": self.way, "video": self.video,
                "defended": self.defended, "stars": self.stars, "file": self.file or None}

    def api(self) -> dict:
        """What the student sees: no answers, no traps."""
        live = {"at": when(self.live_at), "names": self.live} if self.live else None
        return self.base() | {"facts": self.facts, "grade": self.grade(), "live": live}

    def row(self) -> dict:
        """A line of the teacher's table."""
        g = self.grade()
        return self.base() | {"group": self.group, "n": self.n, "student": self.student, "assigned_at": when(self.assigned_at),
                              "files": self.files, "count": self.facts.get("count"), "grade": {k: g[k] for k in ("work", "cap", "hint")}}
