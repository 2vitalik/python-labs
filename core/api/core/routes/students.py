import re

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from core.deps import active_user, admin_user
from core.models.history import record, record_new
from core.models.user import Status, User
from core.routes.profile import ProfileIn, clean

EMAIL_RE = re.compile(r"[A-Za-z0-9._+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
GROUP_RE = re.compile(r"груп[иа]\s+(\S+)")

router = APIRouter(prefix="/api/students")
EXTRAS = []  # the site's own part of a row in the list: async (users) → {email: {…}}


class StudentIn(ProfileIn):
    group: str = ""
    status: Status = Status.student
    test: bool = False
    aliases: list[str] = []


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


def can_see(viewer: User, u: User) -> bool:
    """Whom a student's lists show: fellow students — not the teacher, the waiting, or the test ones (unless that is themselves)."""
    return viewer.status == Status.admin or (u.status == Status.student and (not u.test or u.email == viewer.email))


@router.get("")
async def list_students(user: User = Depends(active_user)):
    """The admin's full list; a student's slice of it (can_see) as `person()` rows — the same page hosts both."""
    users = await User.find_all().sort("group", "last_name").to_list()
    users.sort(key=lambda u: u.test)  # stable: test students go last
    users = [u for u in users if can_see(user, u)]
    rows = {u.email: u.person() for u in users}
    for extra in EXTRAS:
        for email, more in (await extra(users)).items():
            rows[email] |= more
    if user.status == Status.admin:
        for u in users:
            rows[u.email] |= {"email": u.email, "github": u.github,
                              "tg_username": u.tg_username, "tg_linked": u.tg_chat_id is not None,
                              "seen": u.first_seen_at is not None}
    return list(rows.values())


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
    fields = clean(data) | {"aliases": [a.strip() for a in data.aliases if a.strip()]}
    await record(user, fields, actor=admin.email)
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
