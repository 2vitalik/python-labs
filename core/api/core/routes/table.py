"""The table of students (T240), for admins and agents alike; the teacher's settings of it (T315)."""
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from core.deps import editor_user
from core.models.pref import set_pref
from core.models.user import User
from core.table import table
from core.views import QUIET, prefs

router = APIRouter(prefix="/api/table")


class PrefsIn(BaseModel):
    quiet: list[str] | None = None  # the columns grey everywhere (T315 §3)


@router.get("")
async def get_table(user: User = Depends(editor_user)):
    return await table()


@router.put("/prefs")
async def put_prefs(data: PrefsIn, user: User = Depends(editor_user)):
    if data.quiet is not None:
        await set_pref(QUIET, list(dict.fromkeys(k.strip() for k in data.quiet if k.strip())))
    return await prefs()
