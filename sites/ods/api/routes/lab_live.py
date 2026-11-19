"""check() → the site (T354 §9, labs 3–5): the notebook's service cell reports each answer with the card's token.
No cookie and any origin (Colab's kernel, marimo in the browser); the body may come as text/plain to spare a preflight.
The site judges the value itself by the line's rule; no history row per check."""
import json
import math
from datetime import datetime, timezone
from secrets import compare_digest

from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse

from core.models.history import when
from labs_check import verdict
from models.lab import LabVariant

router = APIRouter(prefix="/api/variants")
CORS = {"Access-Control-Allow-Origin": "*"}
BODY, TRIES = 2048, 999


@router.options("/{lab}/live")
async def preflight(lab: int):
    return Response(status_code=204, headers=CORS | {"Access-Control-Allow-Methods": "POST, OPTIONS",
                                                     "Access-Control-Allow-Headers": "Content-Type", "Access-Control-Max-Age": "86400"})


async def body(request: Request) -> dict | None:
    raw = b""
    async for chunk in request.stream():
        raw += chunk
        if len(raw) > BODY:
            return None
    try:
        d = json.loads(raw)
        return {"vid": str(d["vid"]), "token": str(d["token"]), "name": str(d["name"]), "value": float(d["value"])}
    except (ValueError, KeyError, TypeError):
        return None


@router.post("/{lab}/live")
async def live(lab: int, request: Request):
    if not (d := await body(request)) or not math.isfinite(d["value"]):
        return Response(status_code=422, headers=CORS)
    v = await LabVariant.find_one(LabVariant.lab == lab, LabVariant.vid == d["vid"])
    if not v or not v.token or not compare_digest(v.token.encode(), d["token"].encode()):
        return Response(status_code=403, headers=CORS)
    if (name := d["name"]) not in v.answers:
        return Response(status_code=422, headers=CORS)
    now = datetime.now(timezone.utc)
    entry = {"ok": verdict({name: d["value"]}, {name: v.answers[name]})[name]["ok"], "value": d["value"],
             "tries": min((v.live.get(name) or {}).get("tries", 0) + 1, TRIES), "at": when(now)}
    await LabVariant.find_one(LabVariant.id == v.id).update({"$set": {f"live.{name}": entry, "live_at": now}})
    return JSONResponse({"ok": True}, headers=CORS)
