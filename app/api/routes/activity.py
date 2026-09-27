from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query

from activity_feed import SOURCES, feed
from activity_people import people
from deps import admin_user
from models.user import Status, User
from routes.student_games import person

router = APIRouter(prefix="/api/activity")
DEFAULT = [s for s in SOURCES if s not in ("api", "event")]  # on request: every API call is noise, alerts repeat what the journals say


@router.get("")
async def get_feed(user: str = "", src: str = "", before: datetime | None = None, limit: int = Query(100, ge=1, le=500),
                   staff: bool = False, admin: User = Depends(admin_user)):
    """Newest first. `user` — a nick, `src` — sources by comma, `before` — `at` of the last row seen, for the next page."""
    users = await User.find_all().to_list()
    one = next((u for u in users if u.nick == user), None)
    if user and not one:
        raise HTTPException(404)
    hide = [] if staff else ["seed", *(u.email for u in users if u.status == Status.admin)]
    sources = [s for s in src.split(",") if s in SOURCES] or DEFAULT
    if "api" in sources:
        sources = [s for s in sources if s != "fail"]  # already among all the calls
    rows = await feed(sources, one, hide, before, limit)
    by_id = {str(u.id): u.email for u in users}
    for r in rows:
        if r["src"] == "edit" and r["coll"] == "users":
            r["about"] = by_id.get(r["doc"], "")  # whose profile: the bot and the teacher edit other people's
    seen = {e for r in rows for e in (r["user"], r.get("about"), r.get("by"))} | {one.email if one else ""}
    return {"rows": rows, "people": {u.email: person(u) for u in users if u.email in seen},
            "one": one.email if one else "", "more": len(rows) == limit}


@router.get("/people")
async def get_people(days: int = Query(7, ge=0), staff: bool = False, admin: User = Depends(admin_user)):
    return await people(days, staff)
