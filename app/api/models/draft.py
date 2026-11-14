from datetime import datetime, timezone
from typing import Annotated

from beanie import Document, Indexed, PydanticObjectId
from pydantic import Field

from core.models.history import stamp


class Draft(Document):
    """One «Описати словами» request (T289, T291 §14): the student's text and what the AI proposed of it — each proposal with
    its state, until the student adds or rejects it. Also what the limits and the month's budget count."""
    game: Annotated[PydanticObjectId, Indexed()]
    owner: Annotated[str, Indexed()]  # who asked (the author: the teacher in a student's game)
    text: str
    model: str = ""
    usage: dict = {}  # the API's tokens; an error with a paid answer (a refusal) keeps them too
    cost: float = 0  # USD, ai/cost.py
    items: list[dict] = []  # proposals: ai/normalize.py
    error: str = ""  # the API failed: the student's line; such a request is not counted in the limits
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "game_drafts"

    def api(self) -> dict:
        return {"id": str(self.id), "at": stamp(self.created_at), "text": self.text, "model": self.model,
                "cost": self.cost, "items": self.items, "error": self.error}
