"""Saved looks at the table (T240, T315): made, changed with a version on every new look, archived, deleted for good, counted."""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, ValidationError

from core.deps import editor_user
from core.fields import free_key, slugify
from core.models.history import record, record_delete, record_new
from core.models.user import User
from core.models.view import View, ViewVersion
from core.views import add_folder, all_views, get_view, save_version
from core.views_in import ViewIn, clean, clean_note
from core.views_seed import ensure_seeds, forget_seed

router = APIRouter(prefix="/api/views")


class ArchiveIn(BaseModel):
    on: bool = True


class SeenIn(BaseModel):
    open: bool = False  # on screen 3 seconds
    use: bool = False  # a minute of work and five actions
    seconds: int = 0  # of work since the last call


@router.get("")
async def list_views(user: User = Depends(editor_user)):
    return {"views": [v.api() for v in await all_views()]}


@router.post("")
async def create_view(data: ViewIn, user: User = Depends(editor_user)):
    """The slug is the title in Latin; one taken, the site's own too, gets `-2`. Version 1 is what it is now."""
    fields, note, parent = clean(data), clean_note(data.note), data.parent.strip()
    await ensure_seeds()
    views = await View.find_all().to_list()
    slug = free_key(slugify(fields["title"]), {v.slug for v in views}, "vyd")
    v = await View(slug=slug, **fields, parent=parent, parent_version=data.parent_version if parent else 0, version=1,
                   order=max((x.order for x in views), default=-1) + 1, by=user.email).insert()
    await ViewVersion(view=slug, n=1, title=v.title, emoji=v.emoji, query=v.query, note=note, by=user.email, at=v.created_at).insert()
    await record_new(v, user.email)
    await add_folder(v.folder)
    return v.api()


@router.put("/{slug}")
async def update_view(slug: str, data: ViewIn, user: User = Depends(editor_user)):
    """Only the fields sent; a new look (`query`) or a `note` — a version (save_version)."""
    v = await get_view(slug)
    fields, note = clean(data, data.model_fields_set), clean_note(data.note)
    new_look = "query" in fields and fields["query"] != v.query
    changed = await record(v, fields, user.email)
    if new_look or note:
        await save_version(v, user.email, note)
    elif changed:
        await v.set({"updated_at": datetime.now(timezone.utc)})
    if "folder" in fields:
        await add_folder(v.folder)
    return v.api()


@router.post("/{slug}/archive")
async def archive_view(slug: str, data: ArchiveIn, user: User = Depends(editor_user)):
    v = await get_view(slug)
    await record(v, {"archived_at": (v.archived_at or datetime.now(timezone.utc)) if data.on else None}, user.email)
    return v.api()


@router.delete("/{slug}")
async def delete_view(slug: str, user: User = Depends(editor_user)):
    """For good, with its versions; the site's own is not made again."""
    await record_delete(await get_view(slug), user.email)
    await ViewVersion.find(ViewVersion.view == slug).delete()
    await forget_seed(slug)
    return {"ok": True}


@router.post("/{slug}/seen")
async def seen_view(slug: str, request: Request, user: User = Depends(editor_user)):
    """The use count (T315 §9), no history. The body is read by hand: navigator.sendBeacon sends JSON as text/plain."""
    try:
        data = SeenIn.model_validate_json(await request.body() or b"{}")
    except ValidationError:
        raise HTTPException(422, "Лік: чекаю JSON {open, use, seconds}")
    v, now = await get_view(slug), datetime.now(timezone.utc)
    inc, at = {"seconds": max(0, min(data.seconds, 3600))}, {}
    if data.open:
        inc["opens"], at["opened_at"] = 1, now
    if data.use:
        inc["uses"], at["used_at"] = 1, now
    await View.find(View.id == v.id).update({"$inc": inc} | ({"$set": at} if at else {}))
    return {"ok": True}
