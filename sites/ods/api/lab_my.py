"""MY — «Моя лаба» of one student (T354 §5): the card, the line, the versions of the notebook, what the site sees in the file,
the grade hint, the formats to start in, the student's deadline."""
import secrets
from datetime import datetime, timezone

from pydantic import BaseModel

from core.labs import due_for, effective, utc
from core.models.deadline import Deadline, LabMark
from core.models.history import when
from core.models.user import User
from models.lab import LabVariant
from models.lab_file import FileHead, LabFile, file_api
from models.lab_shape import LabShape


class Formats(BaseModel):
    jupyter: bytes = b""
    marimo: str = ""
    live: bool = False


async def heads(v: LabVariant, origin: str = "student") -> list[FileHead]:
    """The versions the card's holder handed in, the newest first, without their bytes; a freed card starts afresh."""
    found = LabFile.find(LabFile.lab == v.lab, LabFile.vid == v.vid, LabFile.student == v.student, LabFile.origin == origin)
    return await found.sort("-at").project(FileHead).to_list()


async def due_of(lab: int, user: User) -> datetime | None:
    """The student's deadline: an extension of theirs over their group's deadline over everyone's."""
    base = due_for(await Deadline.find(Deadline.lab == lab).sort("created_at").to_list(), lab, user.group)
    return effective(await LabMark.find_one(LabMark.user == user.email, LabMark.lab == lab), base)


async def card_of(v: LabVariant, live: bool) -> str:
    """The card to paste; a lab whose check() reports to the site adds the card's token (made on the first ask)."""
    if not live:
        return v.card
    if not v.token:
        await v.set({LabVariant.token: secrets.token_urlsafe(9)})
    return f'{v.card}\nTOKEN = "{v.token}"'


async def my(v: LabVariant, user: User) -> dict:
    f = await LabShape.find_one(LabShape.lab == v.lab).project(Formats)
    files = await heads(v)
    due = await due_of(v.lab, user)
    handed = max((utc(at) for at in (v.checked_at, files[0].at if files else None) if at), default=None)
    late = None if not due else (handed or datetime.now(timezone.utc)) > due
    return v.api() | {"card": await card_of(v, bool(f and f.live)), "files": [file_api(x) for x in files], "due": when(due),
                      "late": late,
                      "formats": {"jupyter": bool(f and f.jupyter), "marimo": bool(f and f.marimo), "live": bool(f and f.live)}}
