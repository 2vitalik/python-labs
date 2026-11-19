"""«Вхідні» (T368 §2.6): what the teacher forwarded to the bot from students' chats — whose it is, what became a version
of «Моя лаба». The teacher's and an agent's; every change answers with the whole INTAKE (intake_view.py)."""
import zlib
from urllib.parse import quote

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel

from core.config import settings
from core.deps import editor_user
from core.models.user import User
from intake_apply import apply, settle
from intake_read import score
from intake_view import intake
from models.forward import Forward
from routes.lab_files import TYPES

router = APIRouter(prefix="/api/intake")


class PersonIn(BaseModel):
    key: str
    student: str  # a nick; "" — nobody's again


class RowIn(BaseModel):
    """Only the fields sent change."""
    lab: int | None = None
    asks: bool = False
    skip: bool = False


async def row(id: PydanticObjectId) -> Forward:
    if not (f := await Forward.get(id)):
        raise HTTPException(404)
    return f


@router.get("")
async def get_intake(user: User = Depends(editor_user)):
    await settle()
    return await intake()


@router.put("/person")
async def put_person(data: PersonIn, user: User = Depends(editor_user)):
    """All the rows of the talk; versions already made stay on the site."""
    talk = Forward.find(Forward.key == data.key)
    if not await talk.count():
        raise HTTPException(404, "Такої розмови нема")
    fields = {"student": "", "how": "", "trouble": ""}
    if nick := data.student.strip().lstrip("@"):
        if not (student := await User.by_nick(nick)):
            raise HTTPException(404, f"Студента {nick} на сайті нема")
        fields |= {"student": student.email, "how": "hand"}
    await talk.update({"$set": fields})
    await settle()
    return await intake()


@router.put("/{id}")
async def put_row(id: PydanticObjectId, data: RowIn, user: User = Depends(editor_user)):
    """A new lab: the line is checked against that lab's card, and the notebook goes over if it now can."""
    f, sent = await row(id), data.model_fields_set
    fields = {k: getattr(data, k) for k in ("asks", "skip") if k in sent}
    if "lab" in sent and data.lab != f.lab:
        if f.version:
            raise HTTPException(409, f"Файл уже став версією лаби {f.lab} на сайті — лабу тут не змінити")
        if data.lab is not None and not 1 <= data.lab <= settings.labs:
            raise HTTPException(422, f"Лаба — від 1 до {settings.labs}")
        ok, total = await score(data.lab, f.line)
        fields |= {"lab": data.lab, "ok": ok, "total": total, "trouble": ""}
    if fields:
        await f.set(fields)
    await settle()
    return await intake()


@router.post("/{id}/apply")
async def apply_again(id: PydanticObjectId, user: User = Depends(editor_user)):
    """Once more, after the cause in `trouble` is fixed; the teacher's click goes over «відкласти» and the teacher's own line."""
    f = await row(id)
    if not f.kind:
        raise HTTPException(422, "Тут нема ноутбука")
    if not (f.lab and f.student):
        raise HTTPException(422, "Спершу вкажи лабу й студента")
    if not f.version:
        await apply(f)
    return await intake()


@router.get("/{id}/raw")
async def raw(id: PydanticObjectId, user: User = Depends(editor_user)):
    """The file as it came."""
    f = await row(id)
    if not f.raw:
        raise HTTPException(404, "Файла тут нема")
    return Response(zlib.decompress(f.raw), media_type=TYPES.get(f.kind, "application/octet-stream"),
                    headers={"Content-Disposition": f"attachment; filename*=UTF-8''{quote(f.file.get('name') or 'file')}"})
