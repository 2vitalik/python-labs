"""Files of a lesson: raw transcripts (the admin's and the agent's) and attachments for students; `bundle` — everything
the agent needs to work on a lesson locally (bin/lesson pull)."""
import mimetypes
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, Form, HTTPException, Response, UploadFile

from core.deps import editor_user
from core.lesson_people import known, roster
from core.models.lesson import Lesson, save
from core.models.lesson_file import LessonFile, file_api
from core.models.user import User
from core.lesson_api import full, is_admin, lesson, reader, seen

router = APIRouter(prefix="/api/lessons/{slug}")
MAX_BYTES = 15 * 2**20  # a Mongo document holds 16 MB
INLINE = ("image/", "application/pdf", "text/")


async def store(l: Lesson, role: str, name: str, data: bytes, actor: str, type: str = "") -> LessonFile:
    """The same name in the same role replaces the file: a push is repeatable. A source named chat… is Zoom's chat too."""
    if len(data) > MAX_BYTES:
        raise HTTPException(422, "Файл завеликий: ліміт 15 МБ")
    f = await LessonFile.find_one(LessonFile.lesson == l.slug, LessonFile.role == role, LessonFile.name == name)
    f = f or LessonFile(lesson=l.slug, role=role, name=name, type="", data=b"")
    text = data.decode("utf-8", "replace") if role == "source" else ""
    f.type = type or mimetypes.guess_type(name)[0] or "application/octet-stream"
    f.data, f.size, f.words, f.uploaded_at, f.uploaded_by = data, len(data), len(text.split()), datetime.now(timezone.utc), actor
    await f.save()
    if role == "source" and name.startswith("chat"):
        await save(l, {"chat": text.strip()}, actor)
    return f


@router.post("/files")
async def upload_file(slug: str, file: UploadFile, role: str = Form("file"), user: User = Depends(editor_user)):
    l = await lesson(slug)
    if role not in ("source", "file"):
        raise HTTPException(422, "role — source або file")
    sent = file.content_type if file.content_type and file.content_type != "application/octet-stream" else ""
    return file_api(await store(l, role, Path(file.filename or "file").name, await file.read(), user.email, sent))


@router.get("/files/{id}")
async def download_file(slug: str, id: PydanticObjectId, user: User = Depends(reader)):
    await seen(slug, user)
    f = await LessonFile.get(id)
    if not f or f.lesson != slug:
        raise HTTPException(404)
    if f.role == "source" and not is_admin(user):
        raise HTTPException(403)
    how = "inline" if f.type.startswith(INLINE) else "attachment"
    return Response(f.data, media_type=f.type, headers={"Content-Disposition": f"{how}; filename*=UTF-8''{quote(f.name)}",
                                                        "Cache-Control": "private, max-age=86400"})


@router.delete("/files/{id}")
async def delete_file(slug: str, id: PydanticObjectId, user: User = Depends(editor_user)):
    f = await LessonFile.get(id)
    if not f or f.lesson != slug:
        raise HTTPException(404)
    await f.delete()
    return {"ok": True}


@router.get("/bundle")
async def bundle(slug: str, user: User = Depends(editor_user)):
    """The lesson with its raw sources as text and the roster (Zoom names → students) — the folder bin/lesson pull writes."""
    l = await lesson(slug)
    sources = await LessonFile.find(LessonFile.lesson == slug, LessonFile.role == "source").sort("name").to_list()
    return await full(l, True) | {"sources": [{"name": f.name, "text": f.data.decode("utf-8", "replace")} for f in sources],
                                  "roster": roster(await known())}
