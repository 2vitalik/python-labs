"""MY — «Моя лаба» of one student (T354 §5): the card, the line, the versions of the notebook, what the site sees in the file,
the grade hint, the formats to start in, the student's deadline. BRIEF — the same lab as a row of the student's list."""
import secrets
from datetime import datetime, timezone

from pydantic import BaseModel

from core.labs import due_for, effective, utc
from core.models.deadline import Deadline, LabMark
from core.models.history import when
from core.models.user import User
from lab_gates import gate, teacher
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


def due_at(mark: LabMark | None, base: Deadline | None) -> datetime | None:
    """The platform's effective(), and: extended with the date not known yet — there is no moment to be late for."""
    return None if mark and mark.open and not mark.until else effective(mark, base)


async def due_of(lab: int, user: User) -> datetime | None:
    """The student's deadline: an extension of theirs over their group's deadline over everyone's."""
    base = due_for(await Deadline.find(Deadline.lab == lab).sort("created_at").to_list(), lab, user.group)
    return due_at(await LabMark.find_one(LabMark.user == user.email, LabMark.lab == lab), base)


async def card_of(v: LabVariant, live: bool) -> str:
    """The card to paste; a lab whose check() reports to the site adds the card's token (made on the first ask)."""
    if not live:
        return v.card
    if not v.token:  # two first asks at once must end with one token: only an empty one is set, then read back
        await LabVariant.find_one(LabVariant.id == v.id, LabVariant.token == "").update({"$set": {"token": secrets.token_urlsafe(9)}})
        v.token = (await LabVariant.get(v.id)).token
    return f'{v.card}\nTOKEN = "{v.token}"'


async def times(v: LabVariant, user: User, files: list[FileHead]) -> dict:
    """The deadline against what is handed in: `late` — the latest of it (or, with nothing handed in, this very moment)
    is past the deadline; `in_time` — some version of the file came before it."""
    due = await due_of(v.lab, user)
    handed = max((utc(at) for at in (v.checked_at, files[0].at if files else None) if at), default=None)
    return {"due": when(due), "late": None if not due else (handed or datetime.now(timezone.utc)) > due,
            "in_time": None if not due else any(utc(f.at) <= due for f in files)}


async def my(v: LabVariant, user: User) -> dict:
    f = await LabShape.find_one(LabShape.lab == v.lab).project(Formats)
    files = await heads(v)
    return v.api() | await times(v, user, files) | {
        "card": await card_of(v, bool(f and f.live)), "files": [file_api(x) for x in files],
        "handin": "site" if teacher(user) else await gate(v.lab),  # site · telegram (lab_gates.py)
        "formats": {"jupyter": bool(f and f.jupyter), "marimo": bool(f and f.marimo), "live": bool(f and f.live)}}


async def brief(v: LabVariant, user: User, state: str) -> dict:
    """BRIEF — the lab among the student's labs: the card, where it is handed in (`state` — its gate), the deadline,
    what is handed in."""
    files = await heads(v)
    return {"vid": v.vid, "handin": "site" if teacher(user) else state, "handed": bool(files) or v.attempts > 0, "ok": v.right(),
            "total": len(v.answers), "points": v.points} | await times(v, user, files)
