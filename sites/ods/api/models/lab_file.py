import zlib
from datetime import datetime, timezone

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field
from pymongo import IndexModel

from core.models.history import when

MAX_BYTES = 12 * 2**20  # the original; zlib keeps a stored one well under Mongo's 16 MB


class LabFile(Document):
    """One version of a student's notebook (T354 §2): every upload is a new one, nothing is overwritten.
    origin `run` — the copy bin/nbrun executed on the teacher's machine, `of` — the student's version it ran."""
    lab: int
    vid: str
    student: str
    kind: str  # ipynb · marimo
    name: str
    size: int
    sha: str  # sha256 of the original
    raw: bytes = b""  # zlib of the original
    at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    by: str = ""
    origin: str = "student"
    via: str = ""  # telegram — the teacher brought it over from the student's message to them, `at` is that message's time (T368)
    of: str = ""
    facts: dict = {}
    line: str = ""
    run: dict | None = None  # RUN (routes/lab_run.py)
    log: str = ""  # the re-run's own words, its tail

    class Settings:
        name = "lab_files"
        indexes = [IndexModel([("lab", 1), ("vid", 1), ("at", 1)]), "student"]

    def data(self) -> bytes:
        return zlib.decompress(self.raw)


class FileHead(BaseModel):
    """A version without its bytes: lists of versions never load the notebooks themselves."""
    id: PydanticObjectId = Field(alias="_id")
    lab: int
    vid: str
    student: str
    kind: str
    name: str
    size: int
    sha: str
    at: datetime
    by: str = ""
    origin: str = "student"
    via: str = ""
    line: str = ""
    run: dict | None = None


def file_api(f: LabFile | FileHead) -> dict:
    """FILE = {id, name, kind, size, at, by, via, line, run}: `line` — the file carries an answer line."""
    return {"id": str(f.id), "name": f.name, "kind": f.kind, "size": f.size, "at": when(f.at), "by": f.by.split("@")[0],
            "via": f.via, "line": bool(f.line), "run": f.run}
