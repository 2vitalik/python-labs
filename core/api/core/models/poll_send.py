from datetime import datetime, timezone

from beanie import Document, PydanticObjectId
from pydantic import Field

from core.models.poll import when


class PollSend(Document):
    """The poll as one message in one chat or topic (T174): Telegram gives each its own poll id, and votes come to that id.
    Written before Telegram is asked, so a send that died halfway still shows."""
    poll: PydanticObjectId
    chat_id: int
    thread_id: int | None = None  # forum topic
    where: str = ""  # «chat › topic» as it was called then
    silent: bool = False
    status: str = "queued"  # queued · sent · failed · closed
    tg_poll_id: str = ""
    message_id: int = 0
    url: str = ""  # t.me link to the message; private chats have none
    option_ids: list[str] = []  # Telegram's persistent ids of the answers, in our order
    error: str = ""
    state: dict = {}  # Telegram's own count, last heard: total, counts, is_closed, at — what our votes are checked against
    by: str = ""
    at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    sent_at: datetime | None = None
    closed_at: datetime | None = None

    class Settings:
        name = "poll_sends"
        indexes = ["poll", "tg_poll_id"]

    def api(self) -> dict:
        return {"id": str(self.id), "chat_id": self.chat_id, "thread_id": self.thread_id, "where": self.where, "silent": self.silent,
                "status": self.status, "url": self.url, "error": self.error, "state": self.state, "at": when(self.at),
                "sent_at": when(self.sent_at), "closed_at": when(self.closed_at)}
