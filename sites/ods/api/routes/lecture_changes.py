"""The catalogue of changes in the lectures (T374): every difference from the lecturer's slides with its kind, weight and
the text before and after. For the teacher and the agents; filled by `bin/content push` from changes/lecNN.json on disk."""
import hashlib
import json
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException

from core.deps import editor_user
from core.models.user import User
from models.lecture_change import LectureChanges

router = APIRouter(prefix="/api/lectures/changes")
put_router = APIRouter(prefix="/api/content/changes")


@router.get("")
async def all_changes(user: User = Depends(editor_user)):
    """Every lecture's items; the blocks' texts (hunks) come per lecture — they are most of the weight."""
    rows = await LectureChanges.find_all().sort("slug").to_list()
    return {"lectures": [{k: v for k, v in r.data.items() if k != "hunks"} | {"slug": r.slug} for r in rows]}


@router.get("/{slug}")
async def hunks(slug: str, user: User = Depends(editor_user)):
    row = await LectureChanges.find_one(LectureChanges.slug == slug)
    if not row:
        raise HTTPException(404)
    return {"hunks": row.data.get("hunks", {})}


@put_router.put("/{slug}")
async def put_changes(slug: str, data: dict, user: User = Depends(editor_user)):
    if not isinstance(data.get("items"), list) or not isinstance(data.get("hunks"), dict):
        raise HTTPException(422, "чекаю changes/lecNN.json: items — список, hunks — словник")
    sha = hashlib.sha1(json.dumps(data, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    row = await LectureChanges.find_one(LectureChanges.slug == slug)
    if row and row.sha == sha:
        return {"state": "same"}
    state = "updated" if row else "new"
    row = row or LectureChanges(slug=slug, data={}, sha="")
    row.data, row.sha, row.updated_at = data, sha, datetime.now(timezone.utc)
    await row.save()
    return {"state": state}
