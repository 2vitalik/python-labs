"""Whose card is whose (T372, T375): the teacher pins the cards by the stream's list — a student's number in it, the same in
every lab; the student neither picks a number nor names a card by a file, and nothing is taken by a mere visit: a card
the teacher freed stays free. The teacher's pin goes for every lab where that number is free. The demo card (n = 0) —
the teacher's and test students', by a click."""
from datetime import datetime, timezone

from fastapi import HTTPException

from core.models.history import record
from core.models.user import Status, User
from models.lab import FRESH, LabVariant
from models.lab_file import LabFile

DEMO = "ДЕМО"
NO_CARD = ("Картки варіантів закріплює викладач — за списком потоку. За тобою картки цієї лаби ще нема: "
           "напиши викладачеві, і вона зʼявиться тут.")


def may_demo(user: User) -> bool:
    return user.status == Status.admin or user.test


async def shelve(v: LabVariant) -> None:
    """A card that starts afresh: its holder's versions stay in the base, out of the card's sight — the same file handed
    in again is a version again."""
    mine = (LabFile.lab == v.lab, LabFile.vid == v.vid, LabFile.student == v.student, LabFile.origin == "student")
    await LabFile.find(*mine).update({"$set": {"origin": "freed"}})


async def take(v: LabVariant, user: User) -> LabVariant:
    """The demo taken over from someone else starts afresh: their line, marks and file are not the new holder's."""
    fresh = FRESH if v.student and v.student != user.email else {}
    if fresh:
        await shelve(v)
    await record(v, fresh | {"student": user.email, "assigned_at": datetime.now(timezone.utc)}, actor=user.email)
    return v


async def held(lab: int, user: User) -> LabVariant | None:
    return await LabVariant.find_one(LabVariant.lab == lab, LabVariant.student == user.email)


async def spread(v: LabVariant, user: User, actor: str) -> None:
    """The teacher's pin goes for every lab: where the student has no card and that number is free, it is theirs."""
    for lab in await LabVariant.distinct("lab"):
        free = LabVariant.find_one(LabVariant.lab == lab, LabVariant.group == v.group, LabVariant.n == v.n, LabVariant.student == "")
        if not await held(lab, user) and (same := await free):
            await record(same, {"student": user.email, "assigned_at": datetime.now(timezone.utc)}, actor=actor)


async def demo_card(lab: int) -> LabVariant | None:
    return await LabVariant.find_one(LabVariant.lab == lab, LabVariant.group == DEMO, LabVariant.n == 0)


async def mine(lab: int, user: User) -> LabVariant:
    if v := await held(lab, user):
        return v
    if not await LabVariant.find_one(LabVariant.lab == lab):
        raise HTTPException(404, f"Карток лаби {lab} ще нема — скажи викладачеві")
    raise HTTPException(404, NO_CARD)


async def demo(lab: int, user: User) -> LabVariant:
    """The demo card of this lab for one who is not in the stream's list; taken over from whoever held it."""
    if not may_demo(user):
        raise HTTPException(403, "Демо-варіант — лише для викладача й тестових студентів")
    if v := await held(lab, user):
        return v
    if not (v := await demo_card(lab)):
        raise HTTPException(404, f"Демо-картки лаби {lab} ще нема")
    return await take(v, user)
