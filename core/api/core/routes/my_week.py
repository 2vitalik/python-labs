from datetime import datetime, timezone

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel

from core.bot import week as alert
from core.deps import active_user
from core.models.history import record
from core.models.user import User
from core.models.week import Mark, Week, frame
from core.week_marks import clean, missing_why, summary

COMMENT = 1000
router = APIRouter(prefix="/api/my/week")


class WeekIn(BaseModel):
    marks: list[Mark] = []
    comment: str = ""
    done: bool = False  # «Готово» is pressed with this save


def shown(week: Week) -> dict:
    return {"frame": frame()} | week.api()


@router.get("")
async def get_my_week(user: User = Depends(active_user)):
    return shown(await Week.find_one(Week.user == user.email) or Week(user=user.email))


@router.put("")
async def put_my_week(data: WeekIn, tasks: BackgroundTasks, user: User = Depends(active_user)):
    """The page saves itself after every change. «Готово» is the save that insists on a reason for each «не можу»;
    once pressed it stays: later changes are saved as they are, and the page asks for the reasons they lack."""
    marks, comment = clean(data.marks, frame()), data.comment.strip()
    if len(comment) > COMMENT:
        raise HTTPException(422, f"Коментар — до {COMMENT} символів")
    if data.done and (bare := missing_why(marks)):
        raise HTTPException(422, f"Поясни червоні слоти: {', '.join(bare)}")
    now = datetime.now(timezone.utc)
    week = await Week.find_one(Week.user == user.email) or await Week(user=user.email).insert()
    first = data.done and not week.done_at
    fields = {"marks": marks, "comment": comment, "done_at": week.done_at or (now if data.done else None)}
    if await record(week, fields, actor=user.email, note=summary(marks)):
        await week.set({Week.updated_at: now})
    if first:
        tasks.add_task(alert.done, user, week)
    return shown(week)
