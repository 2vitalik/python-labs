from fastapi import APIRouter, Depends

from core.deps import admin_user
from core.models.user import Status, User
from core.models.week import Week, frame

router = APIRouter()


@router.get("/api/weeks")
async def list_weeks(admin: User = Depends(admin_user)):
    """Every student's week for /week: the page lays them over one grid itself.
    `me` — the teacher's own week: the hours they are busy are no hours for a class."""
    students = await User.find({"status": Status.student, "test": {"$ne": True}}).sort("group", "last_name").to_list()
    weeks = {w.user: w.api() for w in await Week.find_all().to_list()}
    return {"frame": frame(), "me": weeks.get(admin.email),
            "students": [s.person() | {"tg_username": s.tg_username, "week": weeks.get(s.email)} for s in students]}
