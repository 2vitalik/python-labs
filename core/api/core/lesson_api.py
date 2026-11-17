"""What the lesson routes share: who reads, the input shapes, a lesson found or 404. How a reader sees it — lesson_view.py."""
from itertools import count

from fastapi import Depends, HTTPException, Request
from pydantic import BaseModel

from core.deps import agent, allow, current_user
from core.lesson_view import can_see, is_admin
from core.models.lesson import PARTS, Lesson, Link, Part
from core.models.user import Status, User


class LessonIn(BaseModel):
    date: str = ""  # a day's address is its date…
    tag: str = ""  # …and a tag for a second stream on the same date: 2026-11-10-cpo
    kind: str = ""  # an old address, kind + n (pz1), when given
    n: int | None = None  # None = the next of its kind
    time: str = ""
    title: str = ""
    groups: list[str] = []
    links: list[Link] = []
    parts: list[Part] = []
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
    parts: list[Part] | None = None  # the whole list: what is not sent is gone
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


async def lesson(slug: str) -> Lesson:
    l = await Lesson.find_one(Lesson.slug == slug)
    if not l:
        raise HTTPException(404)
    return l


async def seen(slug: str, user: User) -> Lesson:
    """A draft or somebody's private day is not even a «нема доступу» for a student."""
    l = await lesson(slug)
    if not can_see(l, user, is_admin(user)):
        raise HTTPException(404)
    return l


def links(raw: list[dict]) -> list[Link]:
    return [Link(label=l["label"].strip(), url=l["url"].strip()) for l in raw if l["url"].strip()]


def parts(raw: list[dict]) -> list[Part]:
    """Cleaned; a part sent without a key gets the next free p<n>."""
    taken, free = {p["key"] for p in raw}, count(1)
    out = []
    for p in raw:
        if p["kind"] not in PARTS:
            raise HTTPException(422, f"Вид частини — один із: {', '.join(PARTS)}")
        p = {k: v.strip() if isinstance(v, str) else v for k, v in p.items()}
        key = p["key"] or next(k for k in (f"p{i}" for i in free) if k not in taken)
        out.append(Part(**p | {"key": key, "links": links(p["links"]), "only": [e.strip().lower() for e in p["only"] if e.strip()]}))
    return out


def fields(data: BaseModel) -> dict:
    out = {k: v.strip() if isinstance(v, str) else v
           for k, v in data.model_dump(exclude={"rev", "note", "kind", "n", "tag"}, exclude_none=True).items()}
    if "groups" in out:
        out["groups"] = [g.strip() for g in out["groups"] if g.strip()]
    if "links" in out:
        out["links"] = links(out["links"])
    if "parts" in out:
        out["parts"] = parts(out["parts"])
    return out
