"""Course guide pages: markdown in Mongo (`guide`), edited on the site by admins (T126); every save goes to
`history` with a note, and a note also lands in the «Що змінилось» draft page until published.
Reading is admin-only too while the guide is unfinished (T136): to reopen, `current_user` on the two GETs and
404 for DRAFT to non-admins."""
from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from deps import admin_user
from models.guide import DRAFT, Guide, save
from models.history import Change
from models.user import User

router = APIRouter(prefix="/api/guide")


class PageIn(BaseModel):
    title: str
    body: str
    rev: int
    note: str = ""  # one line for the changes draft; empty = silent edit
    section: str = ""  # heading of the edited part, named in the draft line


class LineIn(BaseModel):
    line: str


async def page(slug: str) -> Guide:
    g = await Guide.find_one(Guide.slug == slug)
    if not g:
        raise HTTPException(404)
    return g


@router.get("")
async def list_pages(user: User = Depends(admin_user)):
    pages = await Guide.find(Guide.slug != DRAFT).to_list()
    return [{"slug": g.slug, "title": g.title, "updated": g.updated_at.isoformat()} for g in pages]


@router.get("/history")
async def history(slug: str = "", user: User = Depends(admin_user)):
    pages = {g.id: g for g in await Guide.find_all().to_list()}
    query = {"coll": "guide"} | ({"doc_id": (await page(slug)).id} if slug else {})
    out = []
    for c in await Change.find(query).sort("-at").limit(200).to_list():
        if g := pages.get(c.doc_id):
            body, title = c.changes.get("body", {}), c.changes.get("title", {})
            out.append({"id": str(c.id), "at": c.at.isoformat(), "actor": c.actor.split("@")[0], "note": c.note,
                        "slug": g.slug, "title": g.title, "old": body.get("old"), "new": body.get("new"),
                        "old_title": title.get("old"), "new_title": title.get("new")})
    return out


@router.get("/{slug}")
async def get_page(slug: str, user: User = Depends(admin_user)):
    return (await page(slug)).api()


@router.put("/{slug}")
async def put_page(slug: str, data: PageIn, user: User = Depends(admin_user)):
    g = await page(slug)
    if data.rev != g.rev:
        raise HTTPException(409, "Сторінку вже змінили в іншій вкладці — перезавантаж і повтори правку")
    note = data.note.strip()
    if await save(g, data.title.strip(), data.body.strip(), user.email, note) and note and slug != DRAFT:
        where = g.title + (f" › {data.section.strip()}" if data.section.strip() else "")
        await add_draft(f"- **{date.today().isoformat()}** — {where}: {note}", user.email)
    return g.api()


async def add_draft(line: str, actor: str):
    d = await Guide.find_one(Guide.slug == DRAFT)
    d = d or await Guide(slug=DRAFT, title="Чернетка «Що змінилось»", body="", updated_by=actor).insert()
    await save(d, d.title, f"{line}\n{d.body}".strip(), actor)


@router.post("/changes/publish")
async def publish(data: LineIn, user: User = Depends(admin_user)):
    """Move one draft line into the public «Що змінилось» — newest first, above the earlier entries."""
    d, c = await page(DRAFT), await page("changes")
    lines = c.body.split("\n")
    at = next((i for i, l in enumerate(lines) if l.startswith("- ")), None)
    lines[at:at] = [data.line] if at is not None else ["", data.line]
    await save(c, c.title, "\n".join(lines), user.email)
    await save(d, d.title, "\n".join(l for l in d.body.split("\n") if l != data.line), user.email)
    return c.api()
