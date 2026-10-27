from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, Query

from core.deps import editor_user
from core.models.user import User
from core.polls_view import matrix, results
from core.routes.polls import get_poll

router = APIRouter(prefix="/api/polls")


@router.get("/matrix")
async def get_matrix(tag: str = "", template: str = "", days: int = Query(0, ge=0), user: User = Depends(editor_user)):
    """Students × polls; `days` — polls sent within that many days, 0 — all."""
    return await matrix(tag, template, days)


@router.get("/{id}")
async def get_results(id: PydanticObjectId, user: User = Depends(editor_user)):
    return await results(await get_poll(id))
