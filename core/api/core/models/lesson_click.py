from datetime import datetime, timezone
from typing import Annotated

from beanie import Document, Indexed
from pydantic import Field


class LessonClick(Document):
    """A student followed a lesson's link (T333): which hosting the recordings are really watched on."""
    lesson: Annotated[str, Indexed()]  # slug
    url: str
    user: str  # email
    at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "lesson_clicks"
