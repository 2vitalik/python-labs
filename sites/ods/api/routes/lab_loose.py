"""Students without a card (T375): the cards are the teacher's to pin — on «Результати», from the stream's free ones."""
from fastapi import APIRouter, Depends

from core.deps import admin_user
from core.models.user import Status, User
from models.lab import LabVariant

router = APIRouter(prefix="/api/variants")


@router.get("/{lab}/loose")
async def loose(lab: int, user: User = Depends(admin_user)):
    """LOOSE: {students: [person + email], free: [vid…]} — the course's students no card of the lab is pinned to, and the
    cards nobody holds (the demo is not one to pin)."""
    holders = set(await LabVariant.distinct("student", {"lab": lab}))
    people = await User.find(User.status == Status.student, {"test": {"$ne": True}}).sort("group", "last_name").to_list()
    cards = await LabVariant.find(LabVariant.lab == lab, LabVariant.student == "", LabVariant.n > 0).sort("group", "n").to_list()
    return {"students": [u.person() | {"email": u.email} for u in people if u.email not in holders], "free": [v.vid for v in cards]}
