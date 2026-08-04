import re

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from deps import admin_user
from models.history import record, record_new
from models.user import Status, User
from routes.profile import ProfileIn, clean

EMAIL_RE = re.compile(r"[A-Za-z0-9._+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
GROUP_RE = re.compile(r"груп[иа]\s+(\S+)")

router = APIRouter(prefix="/api/students")


class StudentIn(ProfileIn):
    group: str = ""
    status: Status = Status.student


class ImportIn(BaseModel):
    text: str


def parse_students(text: str) -> tuple[str, list[dict]]:
    """Tolerant parser for pasted group lists (data/students/cist.txt and alike):
    group name from the header, email by regex, ПІБ = first tab-field without @."""
    group = m[1] if (m := GROUP_RE.search(text)) else ""
    rows = []
    for line in text.splitlines():
        if not (m := EMAIL_RE.search(line)):
            continue
        fio = next((f.strip() for f in line.split("\t") if f.strip() and "@" not in f), "")
        parts = fio.split()
        rows.append({"email": m[0], "last_name": parts[0] if parts else "",
                     "first_name": parts[1] if len(parts) > 1 else "",
                     "patronymic": " ".join(parts[2:])})
    return group, rows


@router.get("")
async def list_students(admin: User = Depends(admin_user)):
    users = await User.find(User.status != Status.admin).sort("group", "last_name").to_list()
    return [u.api() for u in users]


@router.get("/{id}")
async def get_student(id: PydanticObjectId, admin: User = Depends(admin_user)):
    user = await User.get(id)
    if not user:
        raise HTTPException(404)
    return user.api()


@router.put("/{id}")
async def update_student(id: PydanticObjectId, data: StudentIn, admin: User = Depends(admin_user)):
    user = await User.get(id)
    if not user:
        raise HTTPException(404)
    await record(user, clean(data), actor=admin.email)
    return user.api()


@router.post("/import")
async def import_students(data: ImportIn, admin: User = Depends(admin_user)):
    group, rows = parse_students(data.text)
    added, skipped = 0, 0
    for row in rows:
        if await User.find_one(User.email == row["email"]):
            skipped += 1
            continue
        user = User(**row, group=group, status=Status.student)
        await user.insert()
        await record_new(user, actor=admin.email)
        added += 1
    return {"added": added, "skipped": skipped, "group": group}
