import re

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


def parse_students(text: str) -> list[dict]:
    """Tolerant parser for pasted group lists (data/students/cist.txt and alike):
    «Список групи …» headers switch the current group, email by regex, ПІБ = first tab-field without @."""
    group, rows = "", []
    for line in text.splitlines():
        if m := GROUP_RE.search(line):
            group = m[1]
            continue
        if not (m := EMAIL_RE.search(line)):
            continue
        fio = next((f.strip() for f in line.split("\t") if f.strip() and "@" not in f), "")
        parts = fio.split()
        rows.append({"email": m[0], "group": group,
                     "last_name": parts[0] if parts else "",
                     "first_name": parts[1] if len(parts) > 1 else "",
                     "patronymic": " ".join(parts[2:])})
    return rows


@router.get("/{nick}")
async def get_student(nick: str, admin: User = Depends(admin_user)):
    user = await User.by_nick(nick)
    if not user:
        raise HTTPException(404)
    return user.api()


@router.put("/{nick}")
async def update_student(nick: str, data: StudentIn, admin: User = Depends(admin_user)):
    user = await User.by_nick(nick)
    if not user:
        raise HTTPException(404)
    await record(user, clean(data), actor=admin.email)
    return user.api()


@router.post("/import")
async def import_students(data: ImportIn, admin: User = Depends(admin_user)):
    added, updated, unchanged = 0, 0, 0
    for row in parse_students(data.text):
        user = await User.find_one(User.email == row["email"])
        if not user:
            user = User(**row, status=Status.student)
            await user.insert()
            await record_new(user, actor=admin.email)
            added += 1
            continue
        # existing: refresh group, fill ПІБ only if empty — self-edits win over the import
        patch = {"group": row["group"]} if row["group"] and row["group"] != user.group else {}
        if not user.last_name and not user.first_name:
            patch |= {k: row[k] for k in ("last_name", "first_name", "patronymic")}
        if patch:
            await record(user, patch, actor=admin.email)
            updated += 1
        else:
            unchanged += 1
    return {"added": added, "updated": updated, "unchanged": unchanged}
