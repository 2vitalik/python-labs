from datetime import datetime, timezone

from beanie import Document, PydanticObjectId
from pydantic import Field
from pymongo import IndexModel

from core.models.poll import when


class Vote(Document):
    """One `poll_answer` as Telegram sent it (T174). The journal is only added to: a person's answer is their latest vote,
    an empty `option_ids` — the vote taken back. Who it is — by `tg_id` when read (T150); `user` is only who it was then."""
    update_id: int  # with the poll id — a vote Telegram delivered twice is kept once
    tg_poll_id: str
    poll: PydanticObjectId | None = None  # ours, when the poll id was known as the vote came
    tg_id: int | None = None  # None — an anonymous group admin voting as the chat
    username: str = ""
    user: str = ""
    option_ids: list[int] = []
    text: str = ""  # «Пара 3: ✅ так» — the activity feed's row
    raw: dict = {}
    at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))  # when the bot got it: Telegram does not say when it was cast

    class Settings:
        name = "votes"
        indexes = [IndexModel([("tg_poll_id", 1), ("update_id", 1)], unique=True, name="once"), "tg_id", "user", "at"]


class TgChat(Document):
    """A place the bot can send polls to (T174): a group, or a forum topic in it; the bot notes it as it hears messages there."""
    chat_id: int
    thread_id: int | None = None  # forum topic; None — the chat itself or its General topic
    title: str = ""
    topic: str = ""  # Telegram tells a topic's name only in its service messages, so it may stay unknown
    name: str = ""  # the admin's own; "" — «title › topic»
    type: str = ""
    left: bool = False  # the bot is not in the chat any more
    hidden: bool = False  # the admin took it off the list of places
    seen_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "tg_chats"
        indexes = [IndexModel([("chat_id", 1), ("thread_id", 1)], unique=True, name="place")]

    @property
    def where(self) -> str:
        topic = self.topic or (f"#{self.thread_id}" if self.thread_id else "")
        return self.name or " › ".join(x for x in (self.title or str(self.chat_id), topic) if x)

    def api(self) -> dict:
        return {"id": str(self.id), "chat_id": self.chat_id, "thread_id": self.thread_id, "title": self.title, "topic": self.topic,
                "name": self.name, "where": self.where, "type": self.type, "left": self.left, "hidden": self.hidden,
                "seen_at": when(self.seen_at)}
