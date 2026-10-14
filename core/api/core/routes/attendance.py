"""Attendance from Zoom (T222): one pull after the class — by the admin on the page or the agent through bin/zoom — brings
who was in the meeting and for how long; students see the published lesson's block, the admin the whole matrix."""
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from core import attendance as att
from core import attendance_read as read
from core.deps import admin_user, editor_user
from core.lesson_api import is_admin, lesson, reader, seen
from core.models.attendance import Attendance
from core.models.lesson import Lesson, Link, Meeting, save
from core.models.user import User
from core.routes.lesson_files import store
from core.zoom import Zoom

router = APIRouter()
zoom = Zoom()  # the smoke swaps in a fake
FILES = {"TRANSCRIPT": "zoom.vtt", "CHAT": "chat.txt"}  # of the cloud recording — as the lesson's sources


class PullIn(BaseModel):
    meeting: str = ""  # Zoom meeting ID or one run's UUID; empty = the lesson's own
    sources: bool = False  # the cloud recording's transcript, chat and link too


async def run(meeting: str, date: str) -> dict:
    """A UUID names one run; a meeting ID names the link — its run on the lesson's date, or the last one when the date is unknown."""
    if not meeting.isdigit():
        return await zoom.details(meeting)
    runs = await zoom.instances(meeting)
    on_day = [r for r in runs if r.get("start_time", "").startswith(date)] if date else runs
    if runs and not on_day:
        days = ", ".join(sorted(r["start_time"][:10] for r in runs)[-5:])
        raise HTTPException(404, f"У Zoom нема проведення зустрічі {meeting} за {date}; останні — {days}")
    return await zoom.details(max(on_day, key=lambda r: r["start_time"])["uuid"] if on_day else meeting)


async def sources(l: Lesson, uuid: str, actor: str) -> dict:
    """The cloud recording: its transcript and chat become sources (the chat — the lesson's chat too), its page — a link."""
    rec = await zoom.recordings(uuid)
    for f in rec.get("recording_files", []):
        name = FILES.get(f.get("file_type", ""))
        if name and f.get("download_url") and f.get("status", "completed") == "completed":
            await store(l, "source", name, await zoom.download(f["download_url"], rec.get("download_access_token", "")), actor)
    url = rec.get("share_url", "")
    return {"links": [*l.links, Link(label="Запис Zoom", url=url)]} if url and all(x.url != url for x in l.links) else {}


@router.post("/api/lessons/{slug}/zoom")
async def pull(slug: str, data: PullIn, user: User = Depends(editor_user)):
    l = await lesson(slug)
    meeting = data.meeting.strip() or l.meeting
    if not meeting:
        raise HTTPException(422, "Вкажи ID зустрічі Zoom або UUID проведення")
    d = await run(meeting, l.date)
    start = att.parse(d["start_time"])
    end = d.get("end_time") or (start + timedelta(minutes=d.get("duration", 0))).isoformat()
    rows = att.rows(slug, d["uuid"], start, await zoom.participants(d["uuid"]))
    await Attendance.find(Attendance.lesson == slug).delete()
    if rows:
        await Attendance.insert_many(rows)
    patch = {"meeting": meeting, "zoom": Meeting(uuid=d["uuid"], topic=d.get("topic", ""), start=d["start_time"], end=end,
                                                  pulled=datetime.now(timezone.utc).isoformat())}
    if data.sources:
        patch |= await sources(l, d["uuid"], user.email)
    await save(l, patch, user.email, "відвідування із Zoom")
    return await read.attendance(l, True) | {"pulled": len(rows)}


@router.get("/api/lessons/{slug}/attendance")
async def get_attendance(slug: str, user: User = Depends(reader)):
    return await read.attendance(await seen(slug, user), is_admin(user))


@router.get("/api/attendance")
async def get_matrix(user: User = Depends(admin_user)):
    return await read.matrix()
