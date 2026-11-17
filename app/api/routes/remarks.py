"""Remarks of a defense (T328): the teacher dictates lines, each becomes a remark with guessed tags; a click fixes a tag,
the kind, the reward. An agent with a token proposes — tags and kind where the teacher has not set them, a cleaner text
as a hint, an opinion on the student's reply; the word on a reply is the teacher's alone."""
import re

from beanie import PydanticObjectId
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request
from pydantic import BaseModel

import defense_vocab as V
import defenses
import remark_ai
import remark_guess
from bot import defense_alerts
from core.deps import admin_user, agent, editor_user
from core.models.history import record, record_delete, record_new
from core.models.user import User
from grading import WOOD
from models.defense import Defense, Remark, now

router = APIRouter(prefix="/api")
TEXT_MAX, NOTE_MAX, LINES_MAX = 1000, 500, 40
MARKER = re.compile(r"^\s*(?:[-–—•*]|\d+[.)])\s*")  # what a dictation or a paste puts before a line


class LinesIn(BaseModel):
    text: str


class RemarkIn(BaseModel):
    """The fields sent are the fields set."""
    text: str | None = None
    tags: list[str] | None = None
    kind: str | None = None
    coin: str | None = None
    amount: float | None = None
    order: int | None = None
    like: str | None = None  # an agent's: the id of a remark that says the same


class CheckIn(BaseModel):
    state: str
    note: str = ""


def reader(request: Request) -> str:
    return "agent" if agent(request) else "teacher"


async def get(id: PydanticObjectId) -> Remark:
    if r := await Remark.get(id):
        return r
    raise HTTPException(404)


def clean(patch: dict) -> dict:
    tags = patch.get("tags") or []
    if "text" in patch:
        patch["text"] = (patch["text"] or "").strip()[:TEXT_MAX]
    ok = (set(tags) <= V.TAGS.keys() and len(tags) <= V.MAX_TAGS and patch.get("kind", "tip") in V.REMARK_KINDS
          and patch.get("coin", "") in ("", *WOOD) and 0 <= (patch.get("amount") or 0) <= 10 and patch.get("text", "x"))
    if not ok:
        raise HTTPException(422, "Такого значення в зауваженні нема.")
    return patch | ({"tags": list(dict.fromkeys(tags))} if "tags" in patch else {})


@router.post("/defenses/{id}/remarks")
async def post_remarks(id: PydanticObjectId, data: LinesIn, request: Request, tasks: BackgroundTasks, user: User = Depends(editor_user)):
    """A line — a remark, a draft till the defense is sent; its tags and kind are the first guess by its words —
    a model says them better a moment later, when there is one."""
    d = await Defense.get(id)
    rows = [t[:TEXT_MAX] for line in data.text.splitlines() if (t := MARKER.sub("", line).strip())]
    if not d:
        raise HTTPException(404)
    if not rows or len(rows) > LINES_MAX:
        raise HTTPException(422, "Напиши зауваження — кожен рядок стане окремим." if not rows else f"Забагато рядків за раз: до {LINES_MAX}.")
    last = await Remark.find(Remark.defense == d.id).sort("-order").first_or_none()
    out, fresh = [], []
    for i, text in enumerate(rows, (last.order if last else 0) + 1):
        found = remark_guess.tags(text)
        r = Remark(defense=d.id, student=d.student, text=text, tags=found, kind=remark_guess.kind(text, found), order=i)
        await r.insert()
        await record_new(r, actor=user.email)
        out.append(defenses.remark(r, reader(request)))
        fresh.append(r.id)
    if not agent(request):  # an agent sorts its own lines
        tasks.add_task(remark_ai.sort, d.id, fresh)
    return out


@router.put("/remarks/{id}")
async def put_remark(id: PydanticObjectId, data: RemarkIn, request: Request, user: User = Depends(editor_user)):
    r, patch = await get(id), clean(data.model_dump(exclude_unset=True))
    if agent(request):
        hint = {k: patch[k] for k in ("text", "like") if k in patch}
        patch = {k: v for k, v in patch.items() if k in ("tags", "kind") and k not in r.own}
        if hint:
            patch["hint"] = r.hint | hint | {"by": user.email}
    else:
        patch.pop("like", None)
        patch["own"] = sorted(set(r.own) | (patch.keys() & {"tags", "kind", "text"}))
        if patch.get("text", r.text) != r.text:  # rewritten or a proposal taken: the dictated line stays, the proposal is spent
            patch |= {"raw": r.raw or r.text, "hint": {k: v for k, v in r.hint.items() if k != "text"}}
        if "coin" in patch:
            patch["amount"] = patch.get("amount") or (1 if patch["coin"] else 0)
    if patch.get("kind", r.kind) not in V.PAID:
        patch |= {"coin": "", "amount": 0}
    await record(r, patch, actor=user.email)
    owner = await User.find_one(User.email == r.student)
    return defenses.remark(r, reader(request), owner.github if owner else "")


@router.put("/remarks/{id}/check")
async def put_check(id: PydanticObjectId, data: CheckIn, request: Request, tasks: BackgroundTasks, user: User = Depends(editor_user)):
    """The teacher accepts or returns; the same call from an agent leaves its opinion next to the reply."""
    r = await get(id)
    word = {"state": data.state, "note": " ".join(data.note.split())[:NOTE_MAX], "by": user.email, "at": now()}
    if data.state not in V.CHECKS:
        raise HTTPException(422, "Слово на відповідь — прийнято або повернуто.")
    owner = await User.find_one(User.email == r.student)
    if agent(request):
        if not r.reply:
            raise HTTPException(422, "Студент ще не відповів — нема про що мати думку.")
        await record(r, {"agent": word}, actor=user.email)
    elif r.state == "draft" or (data.state == "returned" and not word["note"]):
        raise HTTPException(422, "Зауваження ще не надіслано студентові." if r.state == "draft" else "Повертаючи, напиши рядок чому.")
    elif await record(r, {"check": word, "state": data.state}, actor=user.email) and owner:
        tasks.add_task(defense_alerts.checked, owner, r)
    return defenses.remark(r, reader(request), owner.github if owner else "")


@router.delete("/remarks/{id}", status_code=204)
async def delete_remark(id: PydanticObjectId, admin: User = Depends(admin_user)):
    r = await get(id)
    if r.reply:
        raise HTTPException(422, "Студент уже відповів на це зауваження — його можна прийняти, а не видалити.")
    await record_delete(r, actor=admin.email)
