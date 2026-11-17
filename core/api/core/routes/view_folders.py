"""Where the views stand (T315 §8): their order and the folders of the library."""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from core.deps import editor_user
from core.models.history import record
from core.models.pref import set_pref
from core.models.user import User
from core.models.view import View
from core.views import FOLDERS, all_views, prefs
from core.views_in import FOLDER, short, words

router = APIRouter(prefix="/api/views")


class OrderIn(BaseModel):
    slugs: list[str]


class FoldersIn(BaseModel):
    folders: list[str] | None = None  # in their order, empty ones too
    rename: list[str] | None = None  # [old, new]; new "" — the folder goes, its views go up


def folder(name: str) -> str:
    return short(words(name), FOLDER, "Назва папки")


@router.post("/order")
async def order_views(data: OrderIn, user: User = Depends(editor_user)):
    """The named ones first, the rest after them as they were."""
    rest = [v.slug for v in await all_views() if v.slug not in data.slugs]
    for i, slug in enumerate([*data.slugs, *rest]):
        await View.find(View.slug == slug).update({"$set": {"order": i}})
    return {"views": [v.api() for v in await all_views()]}


@router.post("/folders")
async def set_folders(data: FoldersIn, user: User = Depends(editor_user)):
    """The order, or a folder renamed with all its views; a folder some view is in stays in the list, last if not sent."""
    folders = (await prefs())["folders"] if data.folders is None else [folder(f) for f in data.folders]
    if data.rename is not None:
        if len(data.rename) != 2 or not words(data.rename[0]):
            raise HTTPException(422, "Перейменування: [стара назва, нова]")
        old, new = words(data.rename[0]), folder(data.rename[1])
        folders = [new if f == old else f for f in folders]
        for v in await View.find(View.folder == old).to_list():
            await record(v, {"folder": new}, user.email)
    views = await all_views()
    folders = list(dict.fromkeys(f for f in [*folders, *(v.folder for v in views)] if f))
    await set_pref(FOLDERS, folders)
    return {"folders": folders, "views": [v.api() for v in views]}
