"""Lab variants on the site (T200): a student's card and answer line, the teacher's table and marks. Variants come from lab_io.py."""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from core.deps import active_user, admin_user
from core.models.history import record
from core.models.user import User
from labs_check import parse_line, verdict
from models.lab import LabVariant

router = APIRouter(prefix="/api/labs")
NOTEBOOK = 300


class MyIn(BaseModel):
    line: str = ""
    notebook: str = ""


class MarkIn(BaseModel):
    points: int | None = None
    note: str = ""


async def mine(lab: int, user: User) -> LabVariant:
    """The student's variant of the lab; the first visit takes the lowest free card of their group."""
    if v := await LabVariant.find_one(LabVariant.lab == lab, LabVariant.student == user.email):
        return v
    if not user.group:
        raise HTTPException(404, "У профілі немає групи — скажи викладачеві, яка в тебе група")
    free = LabVariant.find(LabVariant.lab == lab, LabVariant.group == user.group, LabVariant.student == "", LabVariant.n > 0)
    if not (v := await free.sort("n").first_or_none()):
        raise HTTPException(404, f"Карток для групи {user.group} ще нема — скажи викладачеві")
    await record(v, {"student": user.email, "assigned_at": datetime.now(timezone.utc)}, actor=user.email)
    return v


@router.get("")
async def list_labs(user: User = Depends(active_user)):
    """Which labs have cards, and whether this student already holds one."""
    held = {v.lab for v in await LabVariant.find(LabVariant.student == user.email).to_list()}
    return [{"n": n, "mine": n in held} for n in sorted(await LabVariant.distinct("lab"))]


@router.get("/{lab}/my")
async def get_my(lab: int, user: User = Depends(active_user)):
    return (await mine(lab, user)).api()


@router.put("/{lab}/my")
async def put_my(lab: int, data: MyIn, user: User = Depends(active_user)):
    """Check the answer line and keep it; an empty line keeps the old one and saves the notebook link alone."""
    v = await mine(lab, user)
    fields, note = {"notebook": data.notebook.strip()[:NOTEBOOK]}, ""
    if line := " ".join(data.line.split()):
        try:
            n, vid, values = parse_line(line)
        except ValueError as e:
            raise HTTPException(422, str(e))
        if (n, vid) != (lab, v.vid):
            raise HTTPException(422, f"Це рядок варіанта {vid} лаби {n}, а твій — {v.vid} лаби {lab}")
        got = verdict(values, v.answers)
        fields |= {"line": line, "values": values, "verdict": got, "attempts": v.attempts + 1, "checked_at": datetime.now(timezone.utc)}
        note = f"{sum(x['ok'] for x in got.values())}/{len(v.answers)}"
    await record(v, fields, actor=user.email, note=note)
    return v.api()


@router.get("/{lab}/results")
async def results(lab: int, user: User = Depends(admin_user)):
    rows = await LabVariant.find(LabVariant.lab == lab).sort("group", "n").to_list()
    emails = [v.student for v in rows if v.student]
    people = {u.email: u.person() for u in await User.find({"email": {"$in": emails}}).to_list()}
    return [v.row() | {"who": people.get(v.student)} for v in rows]


@router.put("/{lab}/results/{vid}")
async def mark(lab: int, vid: str, data: MarkIn, user: User = Depends(admin_user)):
    v = await LabVariant.find_one(LabVariant.lab == lab, LabVariant.vid == vid)
    if not v:
        raise HTTPException(404)
    if data.points is not None and not 0 <= data.points <= 20:
        raise HTTPException(422, "Бали — від 0 до 20")
    await record(v, {"points": data.points, "note": data.note.strip()}, actor=user.email)
    return v.row()
