from datetime import datetime, timezone
from typing import Annotated

from beanie import Document, Indexed, PydanticObjectId
from pydantic import Field
from pymongo import IndexModel

NEEDS = ("", "must", "skip")  # as the course says · the teacher wants it · the teacher lets it go


class Video(Document):
    """A video the game is asked for (T318, videos.py): the demo by a lab's deadline, an async defense, a gold card
    explained. A link, never a file — and every link it ever had: a demo may be replaced, what was shown by the deadline stays."""
    game: Annotated[PydanticObjectId, Indexed()]
    slot: str  # demo3 · defense1 · gold:<card slug> (videos.py)
    versions: list[dict] = []  # {link, note, at, by} oldest first; the last one is the one shown
    note: str = ""  # a line while there is no link yet; the first link takes it along as its own
    need: str = ""  # NEEDS: the teacher's word on whether it is wanted from this student
    why: str = ""  # …and a line with it: «показав на онлайн-захисті»
    status: str = "claimed"  # game.CLAIM_STATUSES, as on a claim
    verdict: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "videos"
        indexes = [IndexModel([("game", 1), ("slot", 1)], unique=True)]
