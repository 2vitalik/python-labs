"""The notebook file of a lab (T354 §5): the student hands it in (upload or their Colab / Drive link); its owner, the teacher
and an agent read it — parsed for showing or the original."""
from pathlib import Path
from urllib.parse import quote

from beanie import PydanticObjectId
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Response, UploadFile

import labs_nb
import labs_pull
import labs_show
from bot import lab_alerts
from core.deps import viewer
from core.models.user import Status, User
from lab_claim import mine
from lab_gates import taking
from lab_my import my
from lab_store import hand_in, shape_of
from models.lab_file import MAX_BYTES, LabFile, file_api

router = APIRouter(prefix="/api/variants")
TYPES = {"ipynb": "application/x-ipynb+json", "marimo": "text/x-python"}


@router.post("/{lab}/my/file")
async def upload(lab: int, file: UploadFile, tasks: BackgroundTasks, user: User = Depends(taking)):
    v, new = await hand_in(lab, user, Path(file.filename or "notebook.ipynb").name, await file.read(MAX_BYTES + 1))
    if new:
        tasks.add_task(lab_alerts.uploaded, user, v)
    return await my(v, user)


@router.post("/{lab}/my/pull")
async def pull(lab: int, tasks: BackgroundTasks, user: User = Depends(taking)):
    """The notebook behind the link saved on «Моя лаба»."""
    v = await mine(lab, user)
    if not v.notebook:
        raise HTTPException(422, "Спершу збережи посилання на свій ноутбук у Colab")
    try:
        data = await labs_pull.pull(v.notebook)
    except ValueError as e:
        raise HTTPException(422, str(e)) from None
    v, new = await hand_in(lab, user, "colab.ipynb", data)
    if new:
        tasks.add_task(lab_alerts.uploaded, user, v)
    return await my(v, user)


async def readable(id: PydanticObjectId, user: User | None) -> LabFile:
    """Its owner, an admin or an agent."""
    if not user:
        raise HTTPException(401)
    f = await LabFile.get(id)
    if not f:
        raise HTTPException(404)
    if user.status != Status.admin and f.student != user.email:
        raise HTTPException(403)
    return f


@router.get("/file/{id}")
async def show(id: PydanticObjectId, user: User | None = Depends(viewer)):
    """NOTEBOOK: the cells with their roles, tasks and outputs, built from the stored file — nothing runs."""
    f = await readable(id, user)
    nb = labs_nb.read(f.data())
    return {"file": file_api(f), "lab": f.lab, "vid": f.vid, "tool": nb["tool"], "cells": labs_show.cells(nb, await shape_of(f.lab)),
            "facts": f.facts}


@router.get("/file/{id}/raw")
async def raw(id: PydanticObjectId, user: User | None = Depends(viewer)):
    f = await readable(id, user)
    return Response(f.data(), media_type=TYPES.get(f.kind, "application/octet-stream"),
                    headers={"Content-Disposition": f"attachment; filename*=UTF-8''{quote(f.name)}"})
