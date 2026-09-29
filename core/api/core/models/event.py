from datetime import datetime, timezone

from beanie import Document
from pydantic import Field


class Event(Document):
    """An important event, as alerted to the admins (T146): saved before Telegram is tried,
    so a muted kind, an empty token or a failed delivery never loses it."""
    kind: str  # notify.KINDS
    text: str  # the alert itself, Telegram HTML
    user: str = ""  # email of whom it is about; "" = nobody in particular (digest, a stranger)
    sent: bool = False  # reached Telegram
    at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "events"
        indexes = ["user", "kind", "at"]
