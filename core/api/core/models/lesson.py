import re
from datetime import datetime, timezone
from typing import Annotated

from beanie import Document, Indexed
from pydantic import BaseModel, Field

from core.models.history import record, stamp

KINDS = {"pz": "ПЗ", "lab": "Лаба", "lec": "Лекція", "cons": "Консультація", "x": "Зустріч"}  # the old addresses: pz1, lab2
PARTS = {"pz": "ПЗ", "def": "Захист", "lec": "Лекція", "cons": "Додатковий час", "break": "Перерва", "x": "Інше"}
DAY = re.compile(r"\d{4}-\d{2}-\d{2}(-[a-z0-9]+)?")  # a day of one stream; the tag tells a second one on the same date
VIDEO = re.compile(r"//([\w.-]*\.)?(youtube\.com|youtu\.be|zoom\.us|google\.com|t\.me|dropbox\.com)/")


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


class Part(BaseModel):
    """A stretch of the day (T333): a talk, a defense, extra time, a break. With `only` it is those students' and the
    teacher's — its video and texts live here, never in the lesson's shared ones."""
    key: str = ""  # p1, p2… — the anchor #p2 and the name of its recording piece
    kind: str = "pz"
    title: str = ""
    start: str = ""  # by the clock: «HH:MM», a recording piece knows its second — «HH:MM:SS»
    end: str = ""
    note: str = ""  # a line or two on what it was about
    links: list[Link] = []  # this piece's video
    only: list[str] = []  # emails; empty = everyone who reads the lesson
    summary: str = ""
    transcript: str = ""


class Lesson(Document):
    """A day with students (T333): meta, links, parts and the texts (context → transcript → summary) as markdown in the
    format of .claude/skills/lesson. Truth lives here; data/transcripts/<slug>/ is the working copy on disk (bin/lesson)."""
    slug: Annotated[str, Indexed(unique=True)]  # the date, 2026-11-10[-tag] — the folder on disk too; once it was kind + n
    kind: str = ""  # of the old addresses only
    n: int = 0
    date: str = ""  # YYYY-MM-DD; "" = not known yet, never guessed
    time: str = ""  # «18:35–20:10» by the clock
    title: str = ""
    groups: list[str] = []
    links: list[Link] = []  # video, Drive folder, Telegram post… — the icon follows the host
    parts: list[Part] = []
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
        return f"{KINDS.get(self.kind, KINDS['x'])} {self.n}" if self.kind else ".".join(reversed(self.date[5:].split("-")))

    def row(self) -> dict:
        """What every reader of the lesson may see; the parts are the reader's own cut (lesson_view.py)."""
        urls = [l.url for l in self.links] + [l.url for p in self.parts for l in p.links]
        return {"slug": self.slug, "kind": self.kind, "n": self.n, "label": self.label, "date": self.date, "time": self.time,
                "title": self.title, "groups": self.groups, "links": [l.model_dump() for l in self.links], "published": self.published,
                "has": {"summary": bool(self.summary), "transcript": bool(self.transcript), "chat": bool(self.chat),
                        "zoom": bool(self.zoom.uuid), "video": any(VIDEO.search(u) for u in urls)},
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
