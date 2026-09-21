from datetime import datetime, timezone

from beanie import Document
from pydantic import Field


class Activity(Document):
    """A student's footprint on the site — sign-ins and page views; edits live in `history` by actor.
    Later: an activity map per student over the semester."""
    user: str  # email
    kind: str  # login · view
    path: str = ""  # page for `view`
    at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "activity"
        indexes = ["user", "at"]
