"""Saved looks at the table (T240)."""
import re

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from core.deps import editor_user
from core.fields import free_key, slugify
from core.models.history import record, record_delete, record_new
from core.models.user import User
from core.models.view import View

router = APIRouter(prefix="/api/views")
BUILT_IN = re.compile(r"^(all|start|lab\d+)$")  # the views the page itself has (table.js)
KEYS = ("cols", "group", "sort", "q")  # plus f.<column>: a filter


class ViewIn(BaseModel):
    title: str = ""
    emoji: str = ""
    query: dict = {}


class OrderIn(BaseModel):
    slugs: list[str]


def clean(data: ViewIn) -> dict:
    title = " ".join(data.title.split())
    if not title:
        raise HTTPException(422, "Назви вид")
    query = {k: str(v)[:2000] for k, v in data.query.items() if (k in KEYS or k.startswith("f.")) and isinstance(v, (str, int, float))}
    return {"title": title, "emoji": data.emoji.strip(), "query": query}


async def get_view(slug: str) -> View:
    v = await View.find_one(View.slug == slug)
    if not v:
        raise HTTPException(404, f"Виду «{slug}» нема")
    return v


@router.get("")
async def list_views(user: User = Depends(editor_user)):
    return {"views": [v.api() for v in await View.find_all().sort("order", "created_at").to_list()]}


@router.post("")
async def create_view(data: ViewIn, user: User = Depends(editor_user)):
    views = await View.find_all().to_list()
    slug = free_key(slugify(data.title), {v.slug for v in views}, "vyd")
    if BUILT_IN.match(slug):
        slug = f"{slug}-2"
    v = await View(slug=slug, **clean(data), order=max((x.order for x in views), default=-1) + 1, by=user.email).insert()
    await record_new(v, user.email)
    return v.api()


@router.put("/{slug}")
async def update_view(slug: str, data: ViewIn, user: User = Depends(editor_user)):
    v = await get_view(slug)
    await record(v, clean(data), user.email)
    return v.api()


@router.delete("/{slug}")
async def delete_view(slug: str, user: User = Depends(editor_user)):
    await record_delete(await get_view(slug), user.email)
    return {"ok": True}


@router.post("/order")
async def order_views(data: OrderIn, user: User = Depends(editor_user)):
    for i, slug in enumerate(data.slugs):
        await View.find(View.slug == slug).update({"$set": {"order": i}})
    return {"views": [v.api() for v in await View.find_all().sort("order", "created_at").to_list()]}
