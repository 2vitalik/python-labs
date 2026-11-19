"""How open each lab is (lab_gates.py, T368): a student reads the labs open to them; the teacher and an agent — every lab,
and say how open each one is."""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from core.config import settings
from core.deps import editor_user, lister
from core.models.history import record, record_new
from core.models.user import User
from lab_gates import STATES, gates, teacher
from models.lab_gate import LabGate

router = APIRouter(prefix="/api/labgates")


class GateIn(BaseModel):
    state: str


@router.get("")
async def list_gates(user: User = Depends(lister)):
    """{lab: state}; a student's answer has no hidden lab in it."""
    return {n: s for n, s in (await gates()).items() if teacher(user) or s != "hidden"}


@router.put("/{lab}")
async def set_gate(lab: int, data: GateIn, user: User = Depends(editor_user)):
    if not 1 <= lab <= settings.labs:
        raise HTTPException(404, f"Лаби {lab} нема: їх {settings.labs}")
    if data.state not in STATES:
        raise HTTPException(422, "Стан лаби — hidden, telegram або site")
    g = await LabGate.find_one(LabGate.lab == lab)
    if not g:
        await record_new(await LabGate(lab=lab, state=data.state, by=user.email).insert(), user.email)
    elif g.state != data.state:
        await record(g, {"state": data.state, "by": user.email, "at": datetime.now(timezone.utc)}, actor=user.email)
    return await gates()
