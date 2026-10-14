from datetime import datetime, timezone
from typing import Annotated

from beanie import Document, Indexed, PydanticObjectId
from pydantic import BaseModel, Field

from core.models.history import stamp


class LessonFile(Document):
    """A raw transcript of one service, or a file the class worked with: bytes in Mongo, like ods pictures — never in git."""
    lesson: Annotated[str, Indexed()]  # slug
    role: str  # source — a raw transcript (zoom.txt, plaud.txt…), the admin's and the agent's; file — what students may take
    name: str
    type: str
    data: bytes
    size: int = 0
    words: int = 0  # of a source: its size in the admin's card
    uploaded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    uploaded_by: str = ""

    class Settings:
        name = "lesson_files"


class FileMeta(BaseModel):
    """A file without its bytes — the lists (a projection of LessonFile)."""
    id: PydanticObjectId = Field(alias="_id")
    role: str
    name: str
    type: str
    size: int = 0
    words: int = 0
    uploaded_at: datetime
    uploaded_by: str = ""


class FileRef(BaseModel):
    lesson: str


def file_api(f: LessonFile | FileMeta) -> dict:
    return {"id": str(f.id), "role": f.role, "name": f.name, "type": f.type, "size": f.size, "words": f.words,
            "uploaded": stamp(f.uploaded_at), "by": f.uploaded_by.split("@")[0]}
