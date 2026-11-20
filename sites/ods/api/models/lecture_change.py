from datetime import datetime, timezone
from typing import Annotated

from beanie import Document, Indexed
from pydantic import Field


class LectureChanges(Document):
    """What differs in a lecture's text from the lecturer's slides (T374): `data` is the whole changes/lecNN.json that
    bin/lecchanges builds on disk — items (a kind, a weight, a place, the edits) and hunks (the blocks before and after).
    Like the texts, it holds the lectures' words: Mongo only, never git."""
    slug: Annotated[str, Indexed(unique=True)]  # lec05
    data: dict
    sha: str  # of the file as sent: bin/content sends only what differs
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "lecture_changes"
