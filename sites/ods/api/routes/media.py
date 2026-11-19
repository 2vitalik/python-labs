from fastapi import APIRouter, Depends, HTTPException, Response

from core.models.user import Status, User
from core.routes.guide import closed, reader
from models.media import Media

router = APIRouter(prefix="/api/media")


def page_of(path: str) -> str:
    """`lec05/x.png` → lec05, `files/lab3/x.ipynb` → lab3."""
    first, _, rest = path.partition("/")
    return rest.partition("/")[0] if first == "files" else first


@router.get("/{path:path}")
async def get_media(path: str, user: User | None = Depends(reader)):
    """Pictures open to whoever reads the texts they stand in; those of a page closed to students (`guide_staff`, T357;
    a hidden lab, T368) — to the admin only."""
    if not (user and user.status == Status.admin) and (await closed())(page_of(path)):
        raise HTTPException(404)
    m = await Media.find_one(Media.path == path)
    if not m:
        raise HTTPException(404)
    return Response(m.data, media_type=m.type, headers={"Cache-Control": "private, max-age=86400"})
