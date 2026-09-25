from datetime import datetime, timezone

from beanie import Document
from pydantic import Field


class Activity(Document):
    """A student's footprint on the site — sign-ins, page views, API calls; edits live in `history` by actor.
    Later: an activity map per student over the semester."""
    user: str  # email
    kind: str  # login · view · api
    path: str = ""  # page for `view`, path?query for `api`
    method: str = ""  # api
    status: int = 0  # api: HTTP status
    ms: int = 0  # api: server time
    ua: str = ""  # login: user-agent — phone or desktop
    ip: str = ""  # login: whereabouts
    at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "activity"
        indexes = ["user", "at"]
