from datetime import datetime, timezone

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field

from core.models.history import stamp


def when(at: datetime | None) -> str | None:
    return stamp(at) if at else None


class Option(BaseModel):
    """One answer: Telegram shows «emoji text», the table — the emoji alone (T174)."""
    emoji: str = ""
    text: str = ""

    @property
    def label(self) -> str:
        return f"{self.emoji} {self.text}".strip()


class PollTemplate(Document):
    """A poll asked again and again (T174): each new poll copies it, so editing it never rewrites the past."""
    title: str
    question: str
    options: list[Option]
    multiple: bool = False
    tags: list[str] = []
    by: str  # admin's email
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "poll_templates"

    def api(self) -> dict:
        return {"id": str(self.id), "title": self.title, "question": self.question, "options": [o.model_dump() for o in self.options],
                "multiple": self.multiple, "tags": self.tags, "created_at": when(self.created_at)}


class Poll(Document):
    """A question asked once (T174). The question and the answers freeze once Telegram has them; `title` heads the table column."""
    template: PydanticObjectId | None = None
    title: str
    question: str
    options: list[Option]
    multiple: bool = False
    tags: list[str] = []
    status: str = "draft"  # draft · open (reached a chat) · closed
    by: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    sent_at: datetime | None = None
    closed_at: datetime | None = None

    class Settings:
        name = "polls"
        indexes = ["tags", "status", "created_at"]

    def answer(self, ids: list[int]) -> str:
        """«Пара 3: ✅ так» — a vote as the activity feed shows it; no ids — the vote was taken back."""
        chosen = ", ".join(self.options[i].label for i in ids if 0 <= i < len(self.options))
        return f"{self.title}: {chosen or '↩︎ відкликано'}"

    def api(self) -> dict:
        return {"id": str(self.id), "template": str(self.template or ""), "title": self.title, "question": self.question,
                "options": [o.model_dump() for o in self.options], "multiple": self.multiple, "tags": self.tags, "status": self.status,
                "by": self.by.split("@")[0], "created_at": when(self.created_at), "sent_at": when(self.sent_at),
                "closed_at": when(self.closed_at)}
