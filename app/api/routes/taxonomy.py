from fastapi import APIRouter, Depends

from deps import active_user
from models.user import User
from zones import ZONES

router = APIRouter()


@router.get("/api/zones")
async def get_zones(user: User = Depends(active_user)):
    return ZONES
