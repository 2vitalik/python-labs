"""Clicks on a lesson's links (T333): a student's click is counted, the teacher's own is not — it would blur which of
Telegram, Drive or YouTube the students really open. The teacher reads the counts per link and per hosting."""
import re
from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from core.deps import editor_user
from core.lesson_api import lesson, reader, seen
from core.lesson_view import is_admin, mine
from core.models.lesson_click import LessonClick
from core.models.user import User

router = APIRouter()
HOSTS = {"telegram": r"t\.me|telegram\.me", "drive": r"google\.com", "youtube": r"youtube\.com|youtu\.be", "zoom": r"zoom\.us"}


class ClickIn(BaseModel):
    url: str


def hosting(url: str) -> str:
    return next((k for k, host in HOSTS.items() if re.search(rf"//([\w.-]*\.)?({host})/", url)), "other")


def counted(clicks: list[LessonClick], key) -> dict[str, dict]:
    """key(click) → how many clicks and how many different people."""
    by = defaultdict(list)
    for c in clicks:
        by[key(c)].append(c.user)
    return {k: {"clicks": len(users), "people": len(set(users))} for k, users in by.items()}


@router.post("/api/lessons/{slug}/click")
async def click(slug: str, data: ClickIn, user: User = Depends(reader)):
    l = await seen(slug, user)
    admin = is_admin(user)
    if data.url not in [x.url for x in l.links] + [x.url for p in mine(l, user, admin) for x in p.links]:
        raise HTTPException(404)
    if not admin:
        await LessonClick(lesson=slug, url=data.url, user=user.email).insert()
    return {"ok": True}


@router.get("/api/lessons/{slug}/clicks")
async def lesson_clicks(slug: str, user: User = Depends(editor_user)):
    await lesson(slug)
    return counted(await LessonClick.find(LessonClick.lesson == slug).to_list(), lambda c: c.url)


@router.get("/api/lesson-clicks")
async def all_clicks(user: User = Depends(editor_user)):
    found = await LessonClick.find().to_list()
    return {"hostings": counted(found, lambda c: hosting(c.url)), "lessons": counted(found, lambda c: c.lesson)}
