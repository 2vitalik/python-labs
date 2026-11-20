"""A notebook handed in (T354 §5): every upload is a new version; the answer line in it is checked as an attempt;
what the file says (FACTS) is kept on the version and on the card. The card in the file is only checked against the pinned one."""
import hashlib
import zlib
from datetime import datetime

from fastapi import HTTPException

import labs_facts
import labs_nb
from core.labs import utc
from core.models.history import record
from core.models.user import User
from lab_claim import NO_CARD, held
from lab_line import attempt, judge
from models.lab import LabVariant
from models.lab_file import MAX_BYTES, FileHead, LabFile, file_api
from models.lab_shape import LabShape

TOO_BIG = "Файл завеликий: ліміт 12 МБ"


async def shape_of(lab: int) -> dict | None:
    s = await LabShape.find_one(LabShape.lab == lab)
    return s.view() if s else None


def parse(data: bytes) -> dict:
    if len(data) > MAX_BYTES:
        raise HTTPException(422, TOO_BIG)
    try:
        return labs_nb.read(data)
    except ValueError as e:
        raise HTTPException(422, str(e)) from None


def version(nb: dict, data: bytes, **fields) -> LabFile:
    return LabFile(kind=nb["kind"], size=len(data), sha=hashlib.sha256(data).hexdigest(), raw=zlib.compress(data), **fields)


async def store(lab: int, user: User, name: str, data: bytes, at: datetime | None = None, via: str = "", by: str = "") -> tuple[LabVariant, LabFile, bool]:
    """One more version of the student's notebook → (the card, the version, whether it is a new one); no card pinned,
    a foreign card, lab or line — refused, nothing is stored. The same bytes again are not one more version (nor a later
    hand-in): the newest version sent once more, or — with `at` — any version. `at` — it was handed in elsewhere then
    (a message to the teacher, T368): the version takes that time, and the card's «latest» stays with the newest version."""
    nb = parse(data)
    if not nb["cells"]:
        raise HTTPException(422, "У ноутбуці нема жодної клітинки — перевір, який файл здаєш")
    facts = labs_facts.facts(nb, await shape_of(lab))
    if not (v := await held(lab, user)):
        raise HTTPException(409, NO_CARD)
    if facts["vid"] and facts["vid"] != v.vid:
        raise HTTPException(422, f"У файлі картка {facts['vid']}, а за тобою закріплено {v.vid}: встав у ноутбук свою картку — вона на «Моїй лабі»")
    if facts["lab"] and facts["lab"] != lab:  # the card is the same in every lab: it cannot tell a lab from a lab
        raise HTTPException(422, f"Це ноутбук лаби {facts['lab']}, а тут лаба {lab} — перевір, який файл здаєш")
    if facts["line"]:
        judge(v, facts["line"])  # a foreign line — 422
    actor = by or user.email
    f = version(nb, data, lab=lab, vid=v.vid, student=user.email, name=name[:120], by=actor, via=via, facts=facts, line=facts["line"],
                **({"at": at} if at else {}))
    mine = (LabFile.lab == lab, LabFile.vid == v.vid, LabFile.student == user.email, LabFile.origin == "student")
    newest = await LabFile.find(*mine).sort("-at").project(FileHead).first_or_none()
    if (same := await LabFile.find_one(*mine, LabFile.sha == f.sha)) and (at or same.id == newest.id):
        return v, same, False
    await f.insert()
    files = await LabFile.find(*mine).count()
    if at and newest and utc(newest.at) > utc(at):  # an earlier version found later: the card keeps what the newest one says
        await record(v, {"files": files}, actor=actor, note="файл, раніший за останній")
        return v, f, True
    fields, note = attempt(v, facts["line"], at) if facts["line"] else ({}, "")
    v.facts = facts  # the versions keep every FACTS; history keeps what the card's fields were
    await record(v, fields | {"files": files, "file": file_api(f)}, actor=actor, note=f"файл {note}".strip())
    return v, f, True


async def hand_in(lab: int, user: User, name: str, data: bytes) -> tuple[LabVariant, bool]:
    """(the card, whether a version was made): the same file once more makes none — and no word to the teacher."""
    v, _, new = await store(lab, user, name, data)
    return v, new
