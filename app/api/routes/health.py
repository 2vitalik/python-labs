import asyncio

from fastapi import APIRouter, HTTPException
from pymongo.errors import PyMongoError

from db import mongo

router = APIRouter()


@router.get("/api/health")
async def health():
    """Probe for `deploy`/`check` on the VPS: a site without its DB is not ok. Caddy answers 404 on this path from outside."""
    try:
        await asyncio.wait_for(mongo.admin.command("ping"), 3)  # the probes wait 5-10 s, the client alone would wait 30
    except (PyMongoError, TimeoutError):
        raise HTTPException(503, "no db")
    return {"ok": True}
