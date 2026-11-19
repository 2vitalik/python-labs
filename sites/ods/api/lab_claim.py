"""Whose card is whose (T354 §1): the student names their number in the stream's list, or their first file names the variant;
the number held in one lab takes the same card of another lab silently. The demo card (n = 0) — the teacher's and test students'."""
from datetime import datetime, timezone

from fastapi import HTTPException

from core.models.history import record
from core.models.user import Status, User
from models.lab import LabVariant

DEMO = "ДЕМО"


def may_demo(user: User) -> bool:
    return user.status == Status.admin or user.test


async def group_of(lab: int, user: User) -> str:
    """The cards' group of the student: their group or its stream (`ПЗПІ-24` of `ПЗПІ-24-3`), any case; the longest wins."""
    mine = user.group.lower()
    groups = [g for g in await LabVariant.distinct("group", {"lab": lab}) if g and (mine == g.lower() or mine.startswith(g.lower() + "-"))]
    return max(groups, key=len, default="") if mine else ""


async def take(v: LabVariant, user: User) -> LabVariant:
    await record(v, {"student": user.email, "assigned_at": datetime.now(timezone.utc)}, actor=user.email)
    return v


async def held(lab: int, user: User) -> LabVariant | None:
    """The student's card of the lab; none yet — the card of the number they hold in another lab, if nobody has it."""
    if v := await LabVariant.find_one(LabVariant.lab == lab, LabVariant.student == user.email):
        return v
    for other in await LabVariant.find(LabVariant.student == user.email).sort("lab").to_list():
        same = LabVariant.find_one(LabVariant.lab == lab, LabVariant.group == other.group, LabVariant.n == other.n, LabVariant.student == "")
        if v := await same:
            return await take(v, user)
    return None


async def mine(lab: int, user: User) -> LabVariant:
    if v := await held(lab, user):
        return v
    if not await LabVariant.find_one(LabVariant.lab == lab):
        raise HTTPException(404, f"Карток лаби {lab} ще нема — скажи викладачеві")
    if not user.group and not may_demo(user):
        raise HTTPException(404, "У профілі немає групи — скажи викладачеві, яка в тебе група")
    if not await group_of(lab, user) and not may_demo(user):
        raise HTTPException(404, f"Карток для групи {user.group} ще нема — скажи викладачеві")
    raise HTTPException(404, "Ще не знаю твого варіанта: назви свій номер у списку потоку або завантаж ноутбук зі своєю карткою")


async def claim(lab: int, user: User, n: int) -> LabVariant:
    """Number n of the student's stream; the demo — taken over from whoever held it."""
    if (v := await held(lab, user)) and v.n == n:
        return v
    if v:
        raise HTTPException(409, f"У тебе вже є варіант {v.vid} — щоб змінити його, скажи викладачеві")
    if n == 0:
        if not may_demo(user):
            raise HTTPException(403, "Демо-картку беруть лише викладач і тестові студенти")
        if not (v := await LabVariant.find_one(LabVariant.lab == lab, LabVariant.group == DEMO, LabVariant.n == 0)):
            raise HTTPException(404, f"Демо-картки лаби {lab} ще нема")
        return await take(v, user)
    if not (group := await group_of(lab, user)):
        raise HTTPException(404, f"Карток для групи {user.group or '(у профілі групи нема)'} ще нема — скажи викладачеві")
    if not (v := await LabVariant.find_one(LabVariant.lab == lab, LabVariant.group == group, LabVariant.n == n)):
        raise HTTPException(404, f"Номера {n} у списку {group} нема — перевір свій номер")
    if v.student:
        raise HTTPException(409, f"Номер {n} уже взяв інший студент — перевір свій номер у списку потоку або скажи викладачеві")
    return await take(v, user)


async def named(lab: int, user: User, vid: str) -> LabVariant:
    """The card the student's first file names, if it may be theirs: free, of their stream (the demo — for whom it is).
    Not taken yet: the file is checked first."""
    if not vid:
        raise HTTPException(422, "У ноутбуці нема картки (рядка VARIANT = …): встав свою картку або спершу назви свій номер")
    if not (v := await LabVariant.find_one(LabVariant.lab == lab, LabVariant.vid == vid)):
        raise HTTPException(422, f"Картки {vid} у лабі {lab} нема — перевір, що вставив свою картку цієї лаби")
    if v.group == DEMO and may_demo(user):
        return v
    if v.group != await group_of(lab, user):
        raise HTTPException(422, f"Картка {vid} — не з твого потоку: встав свою картку або назви свій номер")
    if v.student:
        raise HTTPException(409, f"Картку {vid} уже взяв інший студент — перевір свою картку або скажи викладачеві")
    return v
