"""The versions of the views (T315 §7): all of them for the tree and the comparison, a name, a note or a ⭐ on one, one restored."""
from fastapi import APIRouter, Depends

from core.deps import editor_user
from core.models.history import record
from core.models.user import User
from core.models.view import ViewVersion
from core.views import all_views, get_version, get_view, save_version
from core.views_in import VersionIn, clean_version

router = APIRouter(prefix="/api/views")


@router.get("/versions")
async def list_versions(user: User = Depends(editor_user)):
    await all_views()  # a view from before versions gets its 1
    return {"versions": [x.api() for x in await ViewVersion.find_all().sort("view", "n").to_list()]}


@router.put("/{slug}/versions/{n}")
async def update_version(slug: str, n: int, data: VersionIn, user: User = Depends(editor_user)):
    ver = await get_version(await get_view(slug), n)
    await record(ver, clean_version(data), user.email)
    return ver.api()


@router.post("/{slug}/versions/{n}/restore")
async def restore_version(slug: str, n: int, user: User = Depends(editor_user)):
    """Version n's look becomes a new version on top: nothing is lost."""
    v = await get_view(slug)
    old = await get_version(v, n)
    await record(v, {"query": old.query}, user.email)
    await save_version(v, user.email, f"повернуто версію {n}")
    return v.api()
