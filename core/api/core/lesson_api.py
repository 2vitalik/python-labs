"""What the lesson routes share: who reads, the input shapes, the lesson as the API shows it."""
from fastapi import Depends, HTTPException, Request
from pydantic import BaseModel

from core.deps import agent, allow, current_user
from core.lesson_people import people, speakers
from core.models.lesson import Lesson, Link
from core.models.lesson_file import FileMeta, LessonFile, file_api
from core.models.user import Status, User


class LessonIn(BaseModel):
    kind: str = "pz"
    n: int | None = None  # None = the next of its kind
    date: str = ""
    time: str = ""
    title: str = ""
    groups: list[str] = []
    links: list[Link] = []
    video_start: str = ""
    context: str = ""
    meeting: str = ""
    published: bool = False


class LessonPatch(BaseModel):
    """PUT: the fields sent are the fields changed; `rev` is the one the editor saw."""
    rev: int
    note: str = ""  # one line for history
    date: str | None = None
    time: str | None = None
    title: str | None = None
    groups: list[str] | None = None
    links: list[Link] | None = None
    video_start: str | None = None
    context: str | None = None
    transcript: str | None = None
    summary: str | None = None
    notes: str | None = None
    chat: str | None = None
    meeting: str | None = None
    published: bool | None = None


async def reader(request: Request, user: User | None = Depends(current_user)) -> User:
    return agent(request) or allow(user, user and user.status != Status.pending)


def is_admin(user: User) -> bool:
    return user.status == Status.admin  # the agent comes built as an admin


async def lesson(slug: str) -> Lesson:
    l = await Lesson.find_one(Lesson.slug == slug)
    if not l:
        raise HTTPException(404)
    return l


async def seen(slug: str, user: User) -> Lesson:
    """A draft is nobody's but the admin's — not even a «нема доступу» for a student."""
    l = await lesson(slug)
    if not l.published and not is_admin(user):
        raise HTTPException(404)
    return l


def fields(data: BaseModel) -> dict:
    out = {k: v.strip() if isinstance(v, str) else v for k, v in data.model_dump(exclude={"rev", "note", "kind", "n"}, exclude_none=True).items()}
    if "groups" in out:
        out["groups"] = [g.strip() for g in out["groups"] if g.strip()]
    if "links" in out:
        out["links"] = [Link(label=l["label"].strip(), url=l["url"].strip()) for l in out["links"] if l["url"].strip()]
    return out


async def full(l: Lesson, admin: bool) -> dict:
    files = await LessonFile.find(LessonFile.lesson == l.slug).sort("role", "name").project(FileMeta).to_list()
    data = l.api(admin) | {"files": [file_api(f) for f in files if admin or f.role == "file"], "people": await people(l.transcript)}
    return data | ({"speakers": speakers(l.transcript)} if admin else {})
