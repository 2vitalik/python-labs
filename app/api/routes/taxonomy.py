from fastapi import APIRouter

from zones import ZONES

router = APIRouter()


@router.get("/api/zones")
async def get_zones():
    return ZONES
