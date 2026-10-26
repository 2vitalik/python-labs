"""Labs × students (T235): the matrix of states the teacher reads, the deadlines of labs. Admins and agents alike."""
from datetime import datetime

from beanie import PydanticObjectId
from core.config import settings
from core.deps import editor_user
from core.labs import Index, naive
from core.models.deadline import Deadline
from core.models.history import record, record_delete, record_new
from core.models.user import Status, User
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/labs")


class DeadlineIn(BaseModel):
    at: datetime
    groups: list[str] = []  # none = everyone


def lab_no(n: int) -> int:
    if not 1 <= n <= settings.labs:
        raise HTTPException(404, f"Лаби {n} нема: їх {settings.labs}")
    return n


def labs_api(deadlines: list[Deadline]) -> list[dict]:
    return [{"n": n, "deadlines": [d.api() for d in deadlines if d.lab == n]} for n in range(1, settings.labs + 1)]


async def all_deadlines() -> list[Deadline]:
    return await Deadline.find_all().sort("lab", "created_at").to_list()


@router.get("")
async def matrix(user: User = Depends(editor_user)):
    """Students × labs: the state of every cell, the repository of every student, the deadlines of every lab."""
    students = await User.find(User.status == Status.student, User.test != True).sort("group", "last_name").to_list()
    index = await Index.load()
    rows = []
    for u in students:
        repo = index.repos.get(u.email)
        rows.append(u.person() | {"github": u.github, "repo": repo.api() if repo else None,
                                  "cells": index.cells(u.email, u.github, u.group, settings.labs)})
    return {"labs": labs_api(index.deadlines), "rows": rows}


@router.put("/{n}/deadline")
async def set_deadline(n: int, data: DeadlineIn, user: User = Depends(editor_user)):
    """The lab's deadline for these groups (none = everyone): one document per such set, rewritten."""
    groups = sorted({g.strip() for g in data.groups if g.strip()})
    same = next((d for d in await Deadline.find(Deadline.lab == lab_no(n)).to_list() if sorted(d.groups) == groups), None)
    if same:
        await record(same, {"at": naive(data.at)}, user.email)
    else:
        same = await Deadline(lab=n, at=naive(data.at), groups=groups).insert()
        await record_new(same, user.email)
    return labs_api(await all_deadlines())


@router.delete("/deadlines/{id}")
async def drop_deadline(id: PydanticObjectId, user: User = Depends(editor_user)):
    d = await Deadline.get(id)
    if not d:
        raise HTTPException(404)
    await record_delete(d, user.email)
    return labs_api(await all_deadlines())
