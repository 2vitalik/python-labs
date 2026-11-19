"""A notebook handed in (T354 §5): every upload is a new version; the answer line in it is checked as an attempt;
what the file says (FACTS) is kept on the version and on the card. The first file of a student without a card names it."""
import hashlib
import zlib

from fastapi import HTTPException

import labs_facts
import labs_nb
from core.models.history import record
from core.models.user import User
from lab_claim import held, named, take
from lab_line import attempt, judge
from models.lab import LabVariant
from models.lab_file import MAX_BYTES, LabFile, file_api
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


async def hand_in(lab: int, user: User, name: str, data: bytes) -> LabVariant:
    """A foreign card or line — 422 and nothing is stored."""
    nb = parse(data)
    facts = labs_facts.facts(nb, await shape_of(lab))
    v = await held(lab, user)
    fresh = v is None
    v = v or await named(lab, user, facts["vid"])
    if facts["vid"] and facts["vid"] != v.vid:
        raise HTTPException(422, f"У файлі картка {facts['vid']}, а твоя — {v.vid}: встав у ноутбук свою картку")
    if facts["line"]:
        judge(v, facts["line"])  # a foreign line — 422 before the card is taken
    if fresh:
        await take(v, user)
    fields, note = attempt(v, facts["line"]) if facts["line"] else ({}, "")
    f = version(nb, data, lab=lab, vid=v.vid, student=user.email, name=name[:120], by=user.email, facts=facts, line=facts["line"])
    await f.insert()
    files = await LabFile.find(LabFile.lab == lab, LabFile.vid == v.vid, LabFile.student == user.email, LabFile.origin == "student").count()
    v.facts = facts  # the versions keep every FACTS; history keeps what the card's fields were
    await record(v, fields | {"files": files, "file": file_api(f)}, actor=user.email, note=f"файл {note}".strip())
    return v
