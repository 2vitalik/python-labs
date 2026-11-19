"""«Мій ноутбук» (T354 §5, §8, §9): the lab's template with the student's card in it, as a file — Jupyter or marimo;
a lab whose check() reports to the site gets the card's token too."""
from urllib.parse import quote

from fastapi import APIRouter, Depends, HTTPException, Query, Response

import labs_start
from core.models.user import User
from lab_claim import mine
from lab_gates import opened
from lab_my import card_of
from models.lab_shape import LabShape

router = APIRouter(prefix="/api/variants")
FILES = {"jupyter": ("ipynb", "application/x-ipynb+json"), "marimo": ("py", "text/x-python; charset=utf-8")}


@router.get("/{lab}/my/start")
async def start(lab: int, kind: str = Query("jupyter", alias="as"), user: User = Depends(opened)):
    if kind not in FILES:
        raise HTTPException(422, "Формат — jupyter або marimo")
    v = await mine(lab, user)
    shape = await LabShape.find_one(LabShape.lab == lab)
    tpl = shape and (shape.jupyter if kind == "jupyter" else shape.marimo)
    if not tpl:
        raise HTTPException(404, f"Шаблону {kind} для лаби {lab} ще нема — скажи викладачеві")
    try:
        body = labs_start.made(kind, tpl, (await card_of(v, shape.live)).split("\n"))
    except ValueError:
        raise HTTPException(404, f"У шаблоні {kind} лаби {lab} нема місця для картки — скажи викладачеві") from None
    ext, mime = FILES[kind]
    name = f"lab{lab}-{v.vid}.{ext}"
    return Response(body, media_type=mime, headers={"Content-Disposition": f"attachment; filename*=UTF-8''{quote(name)}"})
