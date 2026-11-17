"""Saved views (T315): every view has its versions 1..version — a view from before them gets its 1 here, when first read."""
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError

from core.models.pref import get_pref, set_pref
from core.models.view import View, ViewVersion
from core.views_seed import ensure_seeds

AMEND = timedelta(minutes=15)  # the same person's saves within it rewrite their last version (T315 §7)
FOLDERS, QUIET = "table.folders", "table.quiet"


async def ensure_version(v: View) -> View:
    if not v.version:
        try:
            await ViewVersion(view=v.slug, n=1, title=v.title, emoji=v.emoji, query=v.query, by=v.by, at=v.created_at).insert()
        except DuplicateKeyError:  # a parallel request made it first
            pass
        await View.find(View.id == v.id).update({"$max": {"version": 1}})
        v.version = 1
    return v


async def all_views() -> list[View]:
    """Every view, archived too; the site's own are made first if missing."""
    await ensure_seeds()
    return [await ensure_version(v) for v in await View.find_all().sort("order", "created_at").to_list()]


async def get_view(slug: str) -> View:
    v = await View.find_one(View.slug == slug)
    if not v:
        raise HTTPException(404, f"Виду «{slug}» нема")
    return await ensure_version(v)


async def get_version(v: View, n: int) -> ViewVersion:
    ver = await ViewVersion.find_one(ViewVersion.view == v.slug, ViewVersion.n == n)
    if not ver:
        raise HTTPException(404, f"У виду «{v.title}» нема версії {n}")
    return ver


async def save_version(v: View, actor: str, note: str = ""):
    """After `v` changed: a new version — or the last one rewritten, while it is the same person's draft of the last 15 minutes
    that nobody named, noted, starred or made a view of."""
    now = datetime.now(timezone.utc)
    snap = {"title": v.title, "emoji": v.emoji, "query": v.query, "at": now}
    last = await ViewVersion.find_one(ViewVersion.view == v.slug, ViewVersion.n == v.version)
    draft = last and last.n > 1 and last.by == actor and now - last.at.replace(tzinfo=timezone.utc) < AMEND
    if draft and not (note or last.name or last.note or last.star) and not await View.find_one(View.parent == v.slug, View.parent_version == last.n):
        await last.set(snap)
    else:
        v.version += 1
        await ViewVersion(view=v.slug, n=v.version, **snap, note=note, by=actor).insert()
    v.updated_at = now
    await v.save()


async def prefs() -> dict:
    return {"quiet": await get_pref(QUIET, []), "folders": await get_pref(FOLDERS, [])}


async def add_folder(name: str):
    """A view saved into a folder the list does not have yet: the folder goes last."""
    folders = await get_pref(FOLDERS, [])
    if name and name not in folders:
        await set_pref(FOLDERS, [*folders, name])
