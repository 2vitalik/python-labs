from datetime import datetime, timezone
from typing import Annotated, Literal

from beanie import Document, Indexed
from pydantic import BaseModel, Field

from core.config import settings
from core.models.history import when

STEP = 15  # minutes in a slot


class Mark(BaseModel):
    """A run of slots of one kind within a day (T177): minutes from midnight, `end` is not in it. An unmarked slot means «можу»."""
    day: int  # 0 — Monday
    start: int
    end: int
    kind: Literal["no", "meh", "ok"]  # не можу · можу, але незручно · найкраще
    why: str = ""  # the reason, only for `no`


class Week(Document):
    """A person's usual week (T177): when they can come to a class of the whole stream."""
    user: Annotated[str, Indexed(unique=True)]  # email
    marks: list[Mark] = []
    comment: str = ""
    done_at: datetime | None = None  # «Готово» is pressed: an empty week then says «можу будь-коли», not «не відкривав»
    updated_at: datetime | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "weeks"

    def api(self) -> dict:
        return {"marks": [m.model_dump() for m in self.marks], "comment": self.comment,
                "done_at": when(self.done_at), "updated_at": when(self.updated_at)}


def frame() -> dict:
    """The grid everybody marks. The pages draw what they get here, so a site changes it in site.env alone."""
    first, last = (int(h) for h in settings.week_hours.split("-"))
    return {"days": settings.week_days, "from": first * 60, "to": last * 60, "step": STEP}
