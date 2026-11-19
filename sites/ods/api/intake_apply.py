"""A forwarded notebook becomes a version of «Моя лаба» (T368 §2.5) with the time of the student's message. The teacher
brings it over, so the lab gates do not apply and no alert goes out; what stopped it is kept in words for the teacher."""
import zlib

from fastapi import HTTPException

from core.models.user import User
from intake_match import by_telegram
from lab_claim import DEMO
from lab_store import store
from models.forward import Forward
from models.lab import LabVariant


async def why_not(f: Forward, user: User) -> str:
    """The two usual causes in the teacher's words (store() speaks to the student): they hold another card of the lab,
    or another student holds the file's card."""
    if not f.vid:
        return ""
    if (own := await LabVariant.find_one(LabVariant.lab == f.lab, LabVariant.student == user.email)) and own.vid != f.vid:
        return f"У файлі картка {f.vid}, а студент тримає {own.vid}"
    v = await LabVariant.find_one(LabVariant.lab == f.lab, LabVariant.vid == f.vid)
    if not v or not v.student or v.student == user.email or v.group == DEMO:
        return ""
    holder = await User.find_one(User.email == v.student)
    return f"Картку {f.vid} тримає {holder.person()['name'] or holder.nick if holder else v.student}"


async def apply(f: Forward) -> bool:
    """A notebook with its lab and student known → a version; `trouble` — why not (a foreign card or line, not that stream)."""
    try:
        if not (user := await User.find_one(User.email == f.student)):
            raise HTTPException(404, f"Студента {f.student} на сайті нема")
        if word := await why_not(f, user):
            raise HTTPException(409, word)
        name = f.file.get("name") or "telegram.ipynb"
        _, made = await store(f.lab, user, name, zlib.decompress(f.raw), at=f.sent_at, via="telegram", by=f.by)
    except HTTPException as e:
        await f.set({Forward.trouble: str(e.detail)})
        return False
    await f.set({Forward.version: str(made.id), Forward.trouble: "", Forward.vid: f.vid or made.vid})  # a file without a card: the card it went to
    return True


async def settle(user: User | None = None) -> int:
    """Whatever can be done now: talks whose writer linked the bot become theirs, their notebooks — versions, oldest first;
    the teacher's own lines and the rows set aside are left. A row that failed waits for «ще раз» or a change that clears
    its trouble, so a page load does not re-read it; `user` — only theirs («Моя лаба»), the failed too: the student may
    have fixed their profile. How many versions were made."""
    await by_telegram(user)
    q = {"kind": {"$ne": ""}, "lab": {"$ne": None}, "student": user.email if user else {"$ne": ""}, "version": "", "skip": False,
         "mine": False} | ({} if user else {"trouble": ""})
    return sum([await apply(f) for f in await Forward.find(q).sort("sent_at", "msg").to_list()])
