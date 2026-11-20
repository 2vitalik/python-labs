"""The teacher's side of a lab (T200, T354 §5): the table of the stream, one student's work for review, the marks;
a card freed, pinned or passed to another student (T375: the cards are the teacher's to pin)."""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from core.deps import admin_user
from core.models.history import record
from core.models.user import User
from lab_claim import DEMO, may_demo, spread
from lab_my import heads
from models.lab import FRESH, LabVariant
from models.lab_file import LabFile, file_api
from models.lab_shape import LabShape

router = APIRouter(prefix="/api/variants")
DEFENCES = ("", "record", "live")


class MarkIn(BaseModel):
    """Only the fields sent change; `student`: "" frees the card, an email passes it on with everything handed in."""
    points: int | None = None
    note: str = ""
    defended: str = ""
    stars: int | None = None
    student: str = ""


async def people(emails: list[str]) -> dict:
    return {u.email: u.person() for u in await User.find({"email": {"$in": emails}}).to_list()}


async def variant(lab: int, vid: str) -> LabVariant:
    if not (v := await LabVariant.find_one(LabVariant.lab == lab, LabVariant.vid == vid)):
        raise HTTPException(404)
    return v


@router.get("/{lab}/results")
async def results(lab: int, user: User = Depends(admin_user)):
    rows = await LabVariant.find(LabVariant.lab == lab).sort("group", "n").to_list()
    who = await people([v.student for v in rows if v.student])
    return [v.row() | {"who": who.get(v.student)} for v in rows]


@router.get("/{lab}/results/{vid}")
async def review(lab: int, vid: str, user: User = Depends(admin_user)):
    """One student's work: the key, the versions, what the file says, the ladder; ← → among the cards somebody holds."""
    v = await variant(lab, vid)
    order = [x.vid for x in await LabVariant.find(LabVariant.lab == lab, LabVariant.student != "").sort("group", "n").to_list()]
    i = order.index(vid) if vid in order else -1
    shape = await LabShape.find_one(LabShape.lab == lab)
    return v.row() | {"who": (await people([v.student])).get(v.student), "answers": v.answers, "values": v.values,
                      "files": [file_api(f) for f in await heads(v)], "facts": v.facts, "grade": v.grade(),
                      "shape": {"tasks": shape.tasks if shape else []},
                      "prev": order[i - 1] if i > 0 else None, "next": order[i + 1] if 0 <= i < len(order) - 1 else None}


@router.put("/{lab}/results/{vid}")
async def mark(lab: int, vid: str, data: MarkIn, user: User = Depends(admin_user)):
    v, sent = await variant(lab, vid), data.model_fields_set
    if data.points is not None and not 0 <= data.points <= 20:
        raise HTTPException(422, "Бали — від 0 до 20")
    if data.defended not in DEFENCES:
        raise HTTPException(422, "Захист — record або live")
    if data.stars is not None and not 0 <= data.stars <= 4:
        raise HTTPException(422, "Зірочок — від 0 до 4")
    fields = {k: getattr(data, k) for k in ("points", "defended", "stars") if k in sent}
    if "note" in sent:
        fields["note"] = data.note.strip()
    if "student" in sent and (email := data.student.strip()) != v.student:
        fields |= await passed(v, email)
    await record(v, fields, actor=user.email)
    if fields.get("student") and v.group != DEMO:  # the demo is taken lab by lab
        await spread(v, await User.find_one(User.email == v.student), user.email)
    return v.row()


async def passed(v: LabVariant, email: str) -> dict:
    """"" — the card is free and starts afresh (history keeps what was); an email — the card with its work goes to them."""
    if not email:
        return FRESH | {"student": "", "assigned_at": None}
    if not (student := await User.find_one(User.email == email)):
        raise HTTPException(404, f"Студента {email} на сайті нема")
    if v.group == DEMO and not may_demo(student):
        raise HTTPException(409, "Демо-картка — лише для викладача й тестових студентів")
    if other := await LabVariant.find_one(LabVariant.lab == v.lab, LabVariant.student == email):
        raise HTTPException(409, f"У {email} уже є картка {other.vid} цієї лаби — спершу звільни її")
    await LabFile.find(LabFile.lab == v.lab, LabFile.vid == v.vid, LabFile.student == v.student).update({"$set": {"student": email}})
    return {"student": email, "assigned_at": datetime.now(timezone.utc)}
