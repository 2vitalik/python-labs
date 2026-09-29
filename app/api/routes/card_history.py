"""History of the catalog (T156): every edit of a task or a game with what changed, and the way back —
a revert is a new edit that puts the old values of those fields in place."""
from datetime import timezone
from zoneinfo import ZoneInfo

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException

from core.deps import editor_user
from core.models.history import Change, record, stamp
from core.models.user import User
from models.base_game import BaseGame
from models.task import Task

router = APIRouter(prefix="/api/catalog/history")
KINDS = {"tasks": Task, "games": BaseGame}
TZ = ZoneInfo("Europe/Kyiv")


def model(kind: str):
    if kind not in KINDS:
        raise HTTPException(404)
    return KINDS[kind]


@router.get("/{kind}")
async def history(kind: str, slug: str = "", user: User = Depends(editor_user)):
    docs = {d.id: d for d in await model(kind).find_all().to_list()}
    one = next((d for d in docs.values() if d.slug == slug), None)
    if slug and not one:
        raise HTTPException(404)
    out = []
    for c in await Change.find({"coll": kind} | ({"doc_id": one.id} if one else {})).sort("-at").limit(200).to_list():
        if d := docs.get(c.doc_id):
            out.append({"id": str(c.id), "at": stamp(c.at), "actor": c.actor.split("@")[0], "note": c.note,
                        "slug": d.slug, "title": d.title, "changes": c.changes,
                        "created": all(v["old"] is None for v in c.changes.values())})
    return out


@router.post("/{kind}/{id}/revert")
async def revert(kind: str, id: PydanticObjectId, user: User = Depends(editor_user)):
    c = await Change.get(id)
    doc = c and c.coll == kind and await model(kind).get(c.doc_id)
    if not doc:
        raise HTTPException(404)
    data = {k: v["old"] for k, v in c.changes.items()}
    if all(v is None for v in data.values()):
        raise HTTPException(422, "Це створення, його не відкотити — постав статус «архів».")
    other = "slug" in data and await model(kind).find_one({"slug": data["slug"]})
    if other and other.id != doc.id:
        raise HTTPException(422, f"Slug «{data['slug']}» уже зайнятий — відкотити цю правку не вийде.")
    at = c.at.replace(tzinfo=timezone.utc).astimezone(TZ)
    await record(doc, data, actor=user.email, note=f"відкат правки від {at:%d.%m %H:%M}")
    return doc.api()
