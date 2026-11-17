"""The student's side of a defense (T328 §4): the remarks that were sent, and an answer to each — done or not, a line,
a GitHub link to the commit. Nothing of the teacher's impressions comes this way."""
from urllib.parse import urlparse

from beanie import PydanticObjectId
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel

import defense_vocab as V
import defenses
from bot import defense_alerts
from core.config import settings
from core.deps import active_user
from core.models.history import record
from core.models.user import User
from models.defense import Remark, now

router = APIRouter(prefix="/api/my/remarks")
NOTE_MAX, LINK_MAX = 1000, 500
TEACHERS = ("facts", "rates", "marks", "answers", "scale")  # the words of what a student never sees


class ReplyIn(BaseModel):
    state: str
    note: str = ""
    link: str = ""


def clean_link(link: str) -> str:
    """A GitHub address; the scheme may be left out."""
    link = link.strip()
    if link and "://" not in link:
        link = "https://" + link
    u = urlparse(link)
    if link and (u.scheme != "https" or u.netloc.lower() not in ("github.com", "www.github.com") or " " in link or len(link) > LINK_MAX):
        raise HTTPException(422, "Потрібне посилання на GitHub: коміт або файл із рядками.")
    return link


@router.get("")
async def get_mine(user: User = Depends(active_user)):
    """The defenses that were sent, the newest first, each with its remarks."""
    out = []
    for d in await defenses.of_student(user.email):
        if d.sent_at:
            remarks = await Remark.find(Remark.defense == d.id, Remark.state != "draft").sort("order", "created_at").to_list()
            out.append(defenses.defense(d, user, remarks, "student") | {"remarks": [defenses.remark(r, "student", user.github) for r in remarks]})
    vocab = {k: v for k, v in V.vocab().items() if k not in TEACHERS}
    return {"defenses": out, "repo": user.github, "vocab": vocab | {"coins": settings.remark_coins if settings.remark_coins == "open" else "off"}}


@router.put("/{id}")
async def put_reply(id: PydanticObjectId, data: ReplyIn, tasks: BackgroundTasks, user: User = Depends(active_user)):
    """An answer to one's own remark; a returned one is answered again. «Done» shows where, «not done» says why."""
    r = await Remark.get(id)
    if not r or r.student != user.email or r.state == "draft":
        raise HTTPException(404)
    if r.state == "accepted" or data.state not in V.REPLIES:
        raise HTTPException(422, "Це зауваження вже прийнято." if r.state == "accepted" else "Такої відповіді нема.")
    link, note = clean_link(data.link), data.note.strip()[:NOTE_MAX]
    if data.state in V.LINKED and not link:
        raise HTTPException(422, "Додай посилання на коміт або рядки файлу на GitHub — щоб було видно, де виправлено.")
    if data.state not in V.LINKED and not note:
        raise HTTPException(422, "Напиши рядок: чому не робив або що саме не так.")
    if await record(r, {"reply": {"state": data.state, "note": note, "link": link, "at": now()}, "state": "answered"}, actor=user.email):
        tasks.add_task(defense_alerts.replied, user, r)
    return defenses.remark(r, "student", user.github)
