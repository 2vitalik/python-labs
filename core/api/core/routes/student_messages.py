"""A student's Telegram chat pasted from the clipboard (T230): the bot never gets history, the teacher's copy of it does."""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from core.deps import admin_user
from core.models.message import TgMessage
from core.models.user import User
from core.tg_paste import guess, parse_paste

router = APIRouter(prefix="/api/students")


class PasteIn(BaseModel):
    text: str
    student: str | None = None  # the pasted name that is the student (the rest is the teacher); None — only look: authors and a guess


def minute(at: datetime) -> datetime:
    """A paste carries minutes, the bot's rows seconds; Mongo gives UTC without a zone."""
    at = at.astimezone(timezone.utc) if at.tzinfo else at
    return at.replace(tzinfo=None, second=0, microsecond=0)


async def seen(student: User) -> set[tuple[datetime, str]]:
    """(minute, text) of the chat's rows so far: earlier pastes by `about`, the bot's own by the chat — once the student is linked."""
    chat = [{"about": student.email}] + ([{"chat_id": student.tg_chat_id}] if student.tg_chat_id else [])
    return {(minute(m.at), m.text) async for m in TgMessage.find({"chat_type": "business", "$or": chat})}


@router.post("/{nick}/messages")
async def paste_messages(nick: str, data: PasteIn, admin: User = Depends(admin_user)):
    student = await User.by_nick(nick)
    if not student:
        raise HTTPException(404)
    rows, errors = parse_paste(data.text)
    names = list(dict.fromkeys(r["name"] for r in rows))
    if data.student is None:
        return {"authors": [{"name": n, "n": sum(r["name"] == n for r in rows)} for n in names],
                "student": guess(names, student, admin), "errors": errors}
    if errors or not rows:
        raise HTTPException(422, "Є рядки з незрозумілою датою" if errors else "Не знайшов жодного повідомлення")
    old = await seen(student)
    added = {"student": 0, "teacher": 0}
    for r in rows:
        key = (minute(r["at"]), r["text"])
        if key in old:
            continue
        who = student if r["name"] == data.student else admin
        await TgMessage(dir="in", chat_id=student.tg_chat_id or 0, chat_type="business", from_id=who.tg_chat_id,
                        username=who.tg_username, user=who.email, about=student.email, text=r["text"], kind="import",
                        raw={"author": r["name"]}, at=r["at"]).insert()
        old.add(key)
        added["student" if who is student else "teacher"] += 1
    return {"added": sum(added.values()), "skipped": len(rows) - sum(added.values()), **added}
