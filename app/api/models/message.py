from datetime import datetime, timezone

from beanie import Document
from pydantic import Field


class TgMessage(Document):
    """Every Telegram message the bot saw or sent (T129): student chats, the stream forum, admin alerts —
    plus forum membership and reactions (T138), so one collection holds a student's whole Telegram footprint."""
    dir: str  # in · out
    chat_id: int
    chat_type: str = "private"  # private · business (teacher's chat with a student via Chat Automation) · group · supergroup
    thread_id: int | None = None  # forum topic
    from_id: int | None = None  # sender; None for the bot's own messages. business: chat_id is the student, from_id whoever wrote
    username: str = ""
    user: str = ""  # email behind from_id (in) or chat_id (out); "" = not linked
    text: str = ""  # text or media caption
    content_type: str = "text"  # Telegram's, or chat_member · join_request · reaction for non-message events
    file_id: str = ""  # media; the file itself can be fetched later via getFile
    message_id: int = 0
    kind: str = ""  # out: alert kind from KINDS or "reply"; in: edit · deleted · member · reaction
    raw: dict = {}  # in: the whole Telegram object, for whatever analysis comes later
    at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "messages"
        indexes = ["user", "chat_id", "at"]
