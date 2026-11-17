"""Lessons (T218, T333): a day with students — meta, links, parts, transcript and summary in Mongo, edited on the site by
admins and by AI agents with a token (bin/lesson); every save goes to `history`. Students read what is published and theirs."""
from collections import Counter

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from core.deps import admin_user, editor_user
from core.lesson_api import LessonIn, LessonPatch, fields, lesson, reader
from core.lesson_people import people
from core.lesson_view import can_see, full, is_admin, rows, virtual
from core.models.history import record, record_delete, record_new
from core.models.lesson import DAY, KINDS, Lesson, save
from core.models.lesson_file import FileRef, LessonFile
from core.models.user import User

router = APIRouter(prefix="/api/lessons")


class AliasIn(BaseModel):
    name: str  # as the transcript writes the speaker
    nick: str


@router.get("")
async def list_lessons(user: User = Depends(reader)):
    found = await Lesson.find({} if is_admin(user) else {"published": True}).sort("-date", "-n").to_list()
    files = Counter(f.lesson for f in await LessonFile.find(LessonFile.role == "file").project(FileRef).to_list())
    return [r | {"has": r["has"] | {"files": files[r["slug"]]}} for r in await rows(found, user)]


@router.get("/{slug}")
async def get_lesson(slug: str, user: User = Depends(reader)):
    l = await Lesson.find_one(Lesson.slug == slug)
    if l and can_see(l, user, is_admin(user)):
        return await full(l, user)
    if day := DAY.fullmatch(slug) and await virtual(slug, user):
        return day
    raise HTTPException(404)


async def address(data: LessonIn) -> dict:
    """A day's address is its date (and a tag); an old one — the kind and the next number."""
    if not data.kind:
        slug = "-".join(x for x in (data.date.strip(), data.tag.strip().lower()) if x)
        if not DAY.fullmatch(slug):
            raise HTTPException(422, "Потрібна дата заняття: РРРР-ММ-ДД")
        return {"slug": slug}
    if data.kind not in KINDS:
        raise HTTPException(422, f"Вид заняття — один із: {', '.join(KINDS)}")
    last = await Lesson.find(Lesson.kind == data.kind).sort("-n").first_or_none()
    n = data.n or (last.n + 1 if last else 1)
    return {"slug": f"{data.kind}{n}", "kind": data.kind, "n": n}


@router.post("")
async def create_lesson(data: LessonIn, user: User = Depends(editor_user)):
    where = await address(data)
    if await Lesson.find_one(Lesson.slug == where["slug"]):
        raise HTTPException(409, f"Заняття {where['slug']} вже є")
    l = Lesson(**where, updated_by=user.email, **fields(data))
    await l.insert()
    await record_new(l, actor=user.email)
    return await full(l, user)


@router.put("/{slug}")
async def update_lesson(slug: str, data: LessonPatch, user: User = Depends(editor_user)):
    l = await lesson(slug)
    if data.rev != l.rev:
        raise HTTPException(409, "Заняття вже змінили (в іншій вкладці або через bin/lesson) — перезавантаж і повтори правку")
    if not l.kind and data.date not in (None, l.date):
        raise HTTPException(422, "Дата — адреса заняття: інша дата — це інше заняття")
    await save(l, fields(data), user.email, data.note.strip())
    return await full(l, user)


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
    return {"people": await people("\n".join([l.transcript, *(p.transcript for p in l.parts)]))}
