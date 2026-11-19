"""«Моя лаба» (T200, T354): a student's card — claimed by number or named by their notebook — the answer line, the link,
the form of defence. The teacher's side is routes/lab_review.py; variants come from lab_io.py."""
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel

from bot import lab_alerts
from core.deps import active_user
from core.models.history import record
from core.models.user import User
from lab_claim import DEMO, claim, group_of, may_demo, mine
from lab_line import attempt
from lab_my import my
from models.lab import LabVariant

router = APIRouter(prefix="/api/variants")  # /api/labs is the platform's: deadlines of labs
LINK = 300
WAYS = ("", "none", "record", "live")


class MyIn(BaseModel):
    """A field left out stays as it was."""
    line: str | None = None
    notebook: str | None = None
    way: str | None = None
    video: str | None = None


class ClaimIn(BaseModel):
    n: int


@router.get("")
async def list_labs(user: User = Depends(active_user)):
    """Which labs have cards, and whether this student already holds one."""
    held_ = {v.lab for v in await LabVariant.find(LabVariant.student == user.email).to_list()}
    return [{"n": n, "mine": n in held_} for n in sorted(await LabVariant.distinct("lab"))]


@router.get("/{lab}/my")
async def get_my(lab: int, soft: bool = False, user: User = Depends(active_user)):
    """MY; no card yet — 404 with the words why, or with `soft` 200 {vid: None, why}: «Моя лаба» asks so, an ordinary
    first visit is not an error in the browser's console."""
    try:
        v = await mine(lab, user)
    except HTTPException as e:
        if soft and e.status_code == 404:
            return {"vid": None, "why": e.detail}
        raise
    return await my(v, user)


@router.get("/{lab}/free")
async def free(lab: int, user: User = Depends(active_user)):
    """The numbers of the student's stream nobody holds; `own` — the group in their profile; `same` — the number they hold
    in another lab; `demo` — the demo card's vid when they may take it (n = 0), else None."""
    group = await group_of(lab, user)
    cards = await LabVariant.find(LabVariant.lab == lab, LabVariant.group == group, LabVariant.student == "", LabVariant.n > 0).sort("n").to_list() if group else []
    other = await LabVariant.find_one(LabVariant.student == user.email, LabVariant.lab != lab)
    demo = may_demo(user) and await LabVariant.find_one(LabVariant.lab == lab, LabVariant.group == DEMO, LabVariant.n == 0)
    return {"group": group, "own": user.group, "free": [v.n for v in cards], "same": other.n if other else None, "demo": demo.vid if demo else None}


@router.post("/{lab}/my/claim")
async def claim_my(lab: int, data: ClaimIn, user: User = Depends(active_user)):
    return await my(await claim(lab, user, data.n), user)


@router.put("/{lab}/my")
async def put_my(lab: int, data: MyIn, tasks: BackgroundTasks, user: User = Depends(active_user)):
    """Check the answer line and keep it; an empty or absent line keeps the old one."""
    v = await mine(lab, user)
    fields, note = {}, ""
    if data.notebook is not None:
        fields["notebook"] = data.notebook.strip()[:LINK]
    if data.video is not None:
        fields["video"] = data.video.strip()[:LINK]
    if data.way is not None:
        if data.way not in WAYS:
            raise HTTPException(422, "Форма захисту — none, record або live")
        fields["way"] = data.way
    if line := " ".join((data.line or "").split()):
        more, note = attempt(v, line)
        fields |= more
    await record(v, fields, actor=user.email, note=note)
    if note:
        tasks.add_task(lab_alerts.checked, user, v)
    return await my(v, user)
