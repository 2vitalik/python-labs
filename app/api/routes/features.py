"""The teacher's lock on the game page's features (T319): which are closed to students; /api/vocab says it to everyone."""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

import features
from core.deps import admin_user
from core.models.pref import set_pref
from core.models.user import User

router = APIRouter()


class ClosedIn(BaseModel):
    closed: list[str]


@router.put("/api/features")
async def set_closed(data: ClosedIn, admin: User = Depends(admin_user)):
    if bad := [x for x in data.closed if x not in features.EXTRAS]:
        raise HTTPException(422, f"Невідома можливість «{bad[0]}».")
    await set_pref(features.PREF, [x for x in features.EXTRAS if x in data.closed])
    return {"closed": await features.closed()}
