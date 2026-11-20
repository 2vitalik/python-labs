"""Import of the site's texts through the API (T357, bin/content): guide pages, their pictures and files, the list of
the labs' pages. Editors only — an admin or an agent with a token; what the site has goes back as sha1, so only what differs is sent."""
import hashlib
import re
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from core.deps import editor_user
from core.models.guide import Guide, save
from core.models.history import record_new
from core.models.user import User
from models.lab_page import LabPage
from models.lecture_change import LectureChanges
from models.media import Media

router = APIRouter(prefix="/api/content")
SLUG = re.compile(r"[a-z0-9-]+")
PATH = re.compile(r"[A-Za-z0-9._-]+(/[A-Za-z0-9._-]+)*")
MAX = 12 * 2**20


class PageIn(BaseModel):
    title: str
    body: str
    note: str = ""


class LabPageIn(BaseModel):
    slug: str
    kind: str
    lab: int | None = None
    part: str = ""
    nav: str
    order: int = 0
    files: list[dict] = []


def sha(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()


@router.get("")
async def have(user: User = Depends(editor_user)):
    pages = {g.slug: sha(f"{g.title}\n{g.body}".encode()) for g in await Guide.find_all().to_list()}
    media = {m.path: sha(m.data) for m in await Media.find_all().to_list()}
    labpages = [p.model_dump(exclude={"id"}) for p in await LabPage.find_all().sort("lab", "order").to_list()]
    changes = {c.slug: c.sha for c in await LectureChanges.find_all().to_list()}  # the lectures' changes (routes/lecture_changes.py)
    return {"pages": pages, "media": media, "labpages": labpages, "changes": changes}


@router.put("/pages/{slug}")
async def put_page(slug: str, data: PageIn, user: User = Depends(editor_user)):
    if not SLUG.fullmatch(slug):
        raise HTTPException(422, "slug — малі латинські літери, цифри й дефіс")
    title, body = data.title.strip(), data.body.strip()
    g = await Guide.find_one(Guide.slug == slug)
    if not g:
        g = await Guide(slug=slug, title=title, body=body, updated_by=user.email).insert()
        await record_new(g, actor=user.email)
        return {"state": "new", "rev": g.rev}
    return {"state": "updated" if await save(g, title, body, user.email, data.note.strip()) else "same", "rev": g.rev}


@router.put("/media/{path:path}")
async def put_media(path: str, request: Request, user: User = Depends(editor_user)):
    if not PATH.fullmatch(path) or {".", ".."} & set(path.split("/")):
        raise HTTPException(422, "шлях — латинські літери, цифри, «._-» і «/» між ними, без «..»")
    data = bytearray()
    async for chunk in request.stream():
        data += chunk
        if len(data) > MAX:
            raise HTTPException(413, "файл більший за 12 МБ")
    kind = request.headers.get("content-type", "application/octet-stream")
    m = await Media.find_one(Media.path == path)
    if m and (m.data, m.type) == (data, kind):
        return {"state": "same"}
    state = "updated" if m else "new"
    m = m or Media(path=path, type=kind, data=b"")
    m.type, m.data, m.updated_at = kind, bytes(data), datetime.now(timezone.utc)
    await m.save()
    return {"state": state}


@router.put("/labpages")
async def put_labpages(rows: list[LabPageIn], user: User = Depends(editor_user)):
    """The list is the disk's: replaced whole; a page gone from it keeps its text in the guide."""
    slugs = [r.slug for r in rows]
    if len(set(slugs)) != len(slugs) or not all(SLUG.fullmatch(s) for s in slugs):
        raise HTTPException(422, "slug-и сторінок лаб — різні, з малих латинських літер, цифр і дефіса")
    await LabPage.delete_all()
    if rows:
        await LabPage.insert_many([LabPage(**r.model_dump()) for r in rows])
    return {"count": len(rows)}
