from datetime import datetime, timezone
from typing import Annotated

from beanie import Document, Indexed
from pydantic import BaseModel, Field


class Segment(BaseModel):
    join: datetime
    leave: datetime


class Attendance(Document):
    """One person in one lesson's Zoom meeting (T222): the name as Zoom showed it, the joined-left segments merged,
    the seconds in the room. Who the student is gets resolved on read, by User.aliases and ПІБ — an alias added later counts too."""
    lesson: Annotated[str, Indexed()]  # slug
    name: str
    email: str = ""  # user_email — only for those signed in to Zoom
    segments: list[Segment] = []
    seconds: int = 0
    late: int = 0  # seconds from the meeting's start to the first join; 0 = on time
    meeting_uuid: str = ""
    fetched_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "attendance"
