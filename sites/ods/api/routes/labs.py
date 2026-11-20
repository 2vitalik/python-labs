"""«Моя лаба» (T200, T354, T375): a student's card — the one the teacher pinned to them — the answer line, the link,
the form of defence. The teacher's side is routes/lab_review.py; variants come from lab_io.py."""
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel

import labs_pull
from bot import lab_alerts
from core.deps import active_user
from core.models.history import record
from core.models.user import User
from intake_apply import settle
from lab_claim import demo, demo_card, may_demo, mine
from lab_gates import BY_TELEGRAM, gates, here, opened, teacher
from lab_line import attempt
from lab_my import brief, my
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


@router.get("")
async def list_labs(user: User = Depends(active_user)):
    """Which labs have cards; `mine` — a card of the lab is pinned to this reader, and then BRIEF comes along: where the
    lab is handed in, the deadline, what is handed in. A hidden lab is the teacher's."""
    own = {v.lab: v for v in await LabVariant.find(LabVariant.student == user.email).to_list()}
    states = await gates()
    return [{"n": n, "mine": n in own} | (await brief(own[n], user, states.get(n, "site")) if n in own else {})
            for n in sorted(await LabVariant.distinct("lab")) if teacher(user) or states.get(n) != "hidden"]


@router.get("/{lab}/my")
async def get_my(lab: int, soft: bool = False, user: User = Depends(opened)):
    """MY; no card pinned — 404 with the words why, or with `soft` 200 {vid: None, why, demo, demo_taken}: «Моя лаба» asks
    so, a visit without a card is not an error in the browser's console; `demo` — the demo card's vid for one who may
    open it, `demo_taken` — somebody else holds it now and their work on it ends with this reader's click."""
    await settle(user)  # notebooks the teacher forwarded before the student linked the bot become theirs here (T368)
    try:
        v = await mine(lab, user)
    except HTTPException as e:
        if soft and e.status_code == 404:
            card = may_demo(user) and await demo_card(lab)
            return {"vid": None, "why": e.detail, "demo": card.vid if card else None, "demo_taken": bool(card and card.student)}
        raise
    return await my(v, user)


@router.post("/{lab}/my/demo")
async def open_demo(lab: int, user: User = Depends(opened)):
    """The teacher and a test student are not in the stream's list: the demo card instead."""
    return await my(await demo(lab, user), user)


@router.put("/{lab}/my")
async def put_my(lab: int, data: MyIn, tasks: BackgroundTasks, user: User = Depends(opened)):
    """Check the answer line and keep it; an empty or absent line keeps the old one, and the same line again is not one
    more attempt (nor a later hand-in). A lab handed in by Telegram takes no line here — the link, the form of defence
    and the video it does."""
    v = await mine(lab, user)
    fields, note = {}, ""
    for name in ("notebook", "video"):  # the teacher will click them: links only, and the notebook's — one a file comes by
        if (link := getattr(data, name)) is not None:
            fields[name] = link.strip()[:LINK]
            if fields[name] and not fields[name].startswith("https://"):
                raise HTTPException(422, "Посилання має починатися з https://")
            if name == "notebook" and fields[name] and not labs_pull.drive_id(fields[name]):
                raise HTTPException(422, labs_pull.NOT_GOOGLE)
    if data.way is not None:
        if data.way not in WAYS:
            raise HTTPException(422, "Форма захисту — none, record або live")
        fields["way"] = data.way
    if (line := " ".join((data.line or "").split())) and line != v.line:
        if not await here(lab, user):
            raise HTTPException(409, BY_TELEGRAM.format(lab=lab))
        more, note = attempt(v, line)
        fields |= more
    await record(v, fields, actor=user.email, note=note)
    if note:
        tasks.add_task(lab_alerts.checked, user, v)
    return await my(v, user)
