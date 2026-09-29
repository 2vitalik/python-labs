from datetime import datetime, timezone
from typing import Annotated

from beanie import Document, Indexed
from pydantic import Field


class Media(Document):
    """A picture of a lecture or a lab: kept in Mongo, like the texts — never in git (the repo may go public)."""
    path: Annotated[str, Indexed(unique=True)]  # lec05/pca-cloud.png — the page's slug and the file's name
    type: str  # image/png
    data: bytes
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "media"
