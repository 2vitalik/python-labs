from datetime import datetime, timezone

from beanie import Document
from pydantic import Field


class Note(Document):
    """Teacher's note about a student, typed in a chat (T132, T135); for the teacher only, never shown by the bot."""
    user: str = ""  # student's email; "" until the chat is linked
    tg_id: int | None = None  # student's Telegram id, to link later
    text: str
    by: str  # admin's email
    hidden: bool = False  # /hide: taken out of the student's chat, ephemeral in the forum
    source: str = "private"  # private (Chat Automation) · forum · bot (the bot's own chat)
    at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "notes"
        indexes = ["user", "at"]
