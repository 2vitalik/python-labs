from datetime import datetime, timedelta, timezone

from aiogram import html
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request
from pydantic import BaseModel

from bot import notify
from deps import real_user
from models.activity import client
from models.error import Error
from models.user import User

router = APIRouter()
PER_MINUTE = 5  # from one IP: the door is open to guests too
QUIET = timedelta(minutes=10)  # the same message alerts once in this time; every report is saved


class ErrorIn(BaseModel):
    message: str
    stack: str = ""
    path: str = ""
    where: str = ""


def recent(since: timedelta, **match):
    return Error.find({"source": "front", "at": {"$gt": datetime.now(timezone.utc) - since}} | match)


@router.post("/api/errors", status_code=204)
async def front_error(data: ErrorIn, request: Request, tasks: BackgroundTasks, user: User | None = Depends(real_user)):
    """A JS error nobody caught in the SPA (problem.js)."""
    who = client(request)
    if await recent(timedelta(minutes=1), ip=who["ip"]).count() >= PER_MINUTE:
        raise HTTPException(429)
    email, title, path, where = user.email if user else "", data.message[:300], data.path[:200], data.where[:200]
    known = await recent(QUIET, title=title).count()
    await Error(source="front", title=title, trace=data.stack[:5000], user=email, path=path, where=where, **who).insert()
    if known:
        return
    rows = [f"💥 Сайт · {html.quote(path)}" + (f" · {html.quote(user.nick)}" if user else ""), f"❗ {html.quote(title)}"]
    if where:
        rows.append(f"📍 {html.quote(where)}")
    tasks.add_task(notify.send, "error", "\n".join(rows), email)
