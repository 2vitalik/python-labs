"""Lessons (T218): meetings with students — meta, links, transcript and summary in Mongo, edited on the site by admins and
by AI agents with a token (bin/lesson); every save goes to `history`. Students read what is published, a draft is the admin's."""
from collections import Counter

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from core.deps import admin_user, editor_user
from core.lesson_api import LessonIn, LessonPatch, fields, full, is_admin, lesson, reader, seen
from core.lesson_people import people
from core.models.history import record, record_delete, record_new
from core.models.lesson import KINDS, Lesson, save
from core.models.lesson_file import FileRef, LessonFile
from core.models.user import User

router = APIRouter(prefix="/api/lessons")


class AliasIn(BaseModel):
    name: str  # as the transcript writes the speaker
    nick: str


@router.get("")
async def list_lessons(user: User = Depends(reader)):
    rows = await Lesson.find({} if is_admin(user) else {"published": True}).sort("-date", "-n").to_list()
    files = Counter(f.lesson for f in await LessonFile.find(LessonFile.role == "file").project(FileRef).to_list())
    return [r.row() | {"has": r.row()["has"] | {"files": files[r.slug]}} for r in rows]


@router.get("/{slug}")
async def get_lesson(slug: str, user: User = Depends(reader)):
    return await full(await seen(slug, user), is_admin(user))


@router.post("")
async def create_lesson(data: LessonIn, user: User = Depends(editor_user)):
    if data.kind not in KINDS:
        raise HTTPException(422, f"Вид заняття — один із: {', '.join(KINDS)}")
    last = await Lesson.find(Lesson.kind == data.kind).sort("-n").first_or_none()
    n = data.n or (last.n + 1 if last else 1)
    slug = f"{data.kind}{n}"
    if await Lesson.find_one(Lesson.slug == slug):
        raise HTTPException(409, f"{KINDS[data.kind]} {n} вже є")
    l = Lesson(slug=slug, kind=data.kind, n=n, updated_by=user.email, **fields(data))
    await l.insert()
    await record_new(l, actor=user.email)
    return await full(l, True)


@router.put("/{slug}")
async def update_lesson(slug: str, data: LessonPatch, user: User = Depends(editor_user)):
    l = await lesson(slug)
    if data.rev != l.rev:
        raise HTTPException(409, "Заняття вже змінили (в іншій вкладці або через bin/lesson) — перезавантаж і повтори правку")
    await save(l, fields(data), user.email, data.note.strip())
    return await full(l, True)


@router.delete("/{slug}")
async def delete_lesson(slug: str, user: User = Depends(admin_user)):
    l = await lesson(slug)
    await LessonFile.find(LessonFile.lesson == slug).delete()
    await record_delete(l, actor=user.email)
    return {"ok": True}


@router.post("/{slug}/alias")
async def add_alias(slug: str, data: AliasIn, user: User = Depends(editor_user)):
    """A speaker the transcript names is this student: the name joins their aliases, every lesson sees it from now on."""
    l, u, name = await lesson(slug), await User.by_nick(data.nick), data.name.strip()
    if not u:
        raise HTTPException(404)
    if name and name not in u.aliases:
        await record(u, {"aliases": [*u.aliases, name]}, actor=user.email)
    return {"people": await people(l.transcript)}
