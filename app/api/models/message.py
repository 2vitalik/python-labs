from datetime import datetime, timezone

from beanie import Document
from pydantic import Field


class TgMessage(Document):
    """Every Telegram message the bot saw or sent (T129): student chats, the stream forum, admin alerts."""
    dir: str  # in · out
    chat_id: int
    chat_type: str = "private"  # private · group · supergroup
    thread_id: int | None = None  # forum topic
    from_id: int | None = None  # Telegram user id of the sender; None for the bot's own messages
    username: str = ""
    user: str = ""  # email behind from_id (in) or chat_id (out); "" = not linked
    text: str = ""  # text or media caption
    content_type: str = "text"
    file_id: str = ""  # media; the file itself can be fetched later via getFile
    message_id: int = 0
    kind: str = ""  # out: alert kind from KINDS or "reply"; in: "edit" for edited messages
    at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "messages"
        indexes = ["user", "chat_id", "at"]
