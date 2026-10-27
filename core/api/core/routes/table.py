"""The table of students (T240), for admins and agents alike."""
from fastapi import APIRouter, Depends

from core.deps import editor_user
from core.models.user import User
from core.table import table

router = APIRouter(prefix="/api/table")


@router.get("")
async def get_table(user: User = Depends(editor_user)):
    return await table()
