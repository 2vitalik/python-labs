from datetime import datetime, timezone
from typing import Annotated

from beanie import Document, Indexed
from pydantic import BaseModel, Field

from core.models.history import record, stamp

KINDS = {"pz": "ПЗ", "lab": "Лаба", "lec": "Лекція", "cons": "Консультація", "x": "Зустріч"}
SKILL_KINDS = {"pz": "practice", "lab": "lab", "lec": "lecture", "cons": "consult", "x": "other"}  # merge.md's words


class Link(BaseModel):
    label: str = ""
    url: str


class Meeting(BaseModel):
    """What the last pull from Zoom found (T222): the instance and its span — the attendance rows are measured against it."""
    uuid: str = ""
    topic: str = ""
    start: str = ""  # ISO UTC, as Zoom gives it
    end: str = ""
    pulled: str = ""  # ISO UTC of the pull


class Lesson(Document):
    """One meeting with students: meta, links and the texts (context → transcript → summary) as markdown in the format of
    .claude/skills/lesson. Truth lives here; data/transcripts/<slug>/ is the working copy on disk (bin/lesson)."""
    slug: Annotated[str, Indexed(unique=True)]  # kind + n: pz1, lab2 — the folder on disk too
    kind: str = "pz"
    n: int = 1
    date: str = ""  # YYYY-MM-DD; "" = not known yet, never guessed
    time: str = ""  # «18:35–20:10» by the clock
    title: str = ""
    groups: list[str] = []
    links: list[Link] = []  # video, Drive folder, Telegram post… — the icon follows the host
    video_start: str = ""  # «HH:MM:SS» clock time where the recording starts: a line's time → a moment in the video
    context: str = ""  # the teacher's notes for the summary
    transcript: str = ""
    summary: str = ""
    notes: str = ""  # merge notes: clock offsets, unnamed speakers, doubts — the admin's
    chat: str = ""  # Zoom's chat as saved (meeting_saved_chat.txt)
    meeting: str = ""  # Zoom meeting ID (the recurring link's) or one instance's UUID — what «Оновити із Zoom» asks for
    zoom: Meeting = Meeting()
    published: bool = False
    rev: int = 0  # bumped on every save; a PUT carries the rev it saw → 409 on a stale one
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_by: str = ""

    class Settings:
        name = "lessons"

    @property
    def label(self) -> str:
        return f"{KINDS.get(self.kind, KINDS['x'])} {self.n}"

    def row(self) -> dict:
        return {"slug": self.slug, "kind": self.kind, "n": self.n, "label": self.label, "date": self.date, "time": self.time,
                "title": self.title, "groups": self.groups, "links": [l.model_dump() for l in self.links], "published": self.published,
                "has": {"summary": bool(self.summary), "transcript": bool(self.transcript), "chat": bool(self.chat), "zoom": bool(self.zoom.uuid)},
                "updated": stamp(self.updated_at)}

    def api(self, admin: bool) -> dict:
        data = self.row() | {"video_start": self.video_start, "transcript": self.transcript, "summary": self.summary,
                             "chat": self.chat, "zoom": self.zoom.model_dump(), "rev": self.rev, "updated_by": self.updated_by.split("@")[0]}
        return data | ({"context": self.context, "notes": self.notes, "meeting": self.meeting} if admin else {})


async def save(l: Lesson, data: dict, actor: str, note: str = "") -> bool:
    """Record a new version; False when nothing changed."""
    if all(getattr(l, k) == v for k, v in data.items()):
        return False
    l.rev, l.updated_at, l.updated_by = l.rev + 1, datetime.now(timezone.utc), actor
    await record(l, data, actor=actor, note=note)
    return True
