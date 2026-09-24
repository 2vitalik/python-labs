from datetime import datetime, timezone

from beanie import Document
from pydantic import Field


class Note(Document):
    """Teacher's note about a student, written from a chat (T132): /note is hidden from the student, «📝 …» was seen."""
    user: str = ""  # student's email; "" until the chat is linked
    tg_id: int | None = None  # student's Telegram id, to link later
    text: str
    by: str  # admin's email
    visible: bool = False
    source: str = "private"  # private (Chat Automation) · forum · bot (the bot's own chat)
    at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "notes"
        indexes = ["user", "at"]
