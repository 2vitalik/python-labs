from fastapi import APIRouter, Depends, HTTPException, Response

from core.models.user import User
from core.routes.guide import reader
from models.media import Media

router = APIRouter(prefix="/api/media")


@router.get("/{path:path}")
async def get_media(path: str, user: User = Depends(reader)):
    """Pictures open to whoever reads the texts they stand in."""
    m = await Media.find_one(Media.path == path)
    if not m:
        raise HTTPException(404)
    return Response(m.data, media_type=m.type, headers={"Cache-Control": "private, max-age=86400"})
