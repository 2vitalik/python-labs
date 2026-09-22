from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from deps import active_user
from models.history import record, record_delete, record_new
from models.ref import Ref
from models.user import Status, User

router = APIRouter(prefix="/api/refs")


class RefIn(BaseModel):
    url: str = ""
    title: str = ""
    note: str = ""
    parent: str = ""


def clean(data: RefIn) -> dict:
    url, title, note = data.url.strip(), data.title.strip(), data.note.strip()
    if url and not url.startswith(("http://", "https://")):
        raise HTTPException(422, "Посилання починається з http(s)://")
    if not url and not (title or note):
        raise HTTPException(422, "Ідея порожня — напиши хоч рядок")
    return {"url": url, "title": title, "note": note, "kind": "link" if url else "idea", "parent": data.parent.strip()}


async def own_ref(id: PydanticObjectId, user: User) -> Ref:
    ref = await Ref.get(id)
    if not ref:
        raise HTTPException(404)
    if ref.author != user.email and user.status != Status.admin:
        raise HTTPException(403)
    return ref


@router.get("")
async def list_refs(user: User = Depends(active_user)):
    refs = await Ref.find_all().sort("-created_at").to_list()
    return [r.api() | {"mine": r.author == user.email} for r in refs]


@router.post("")
async def create_ref(data: RefIn, user: User = Depends(active_user)):
    ref = Ref(author=user.email, **clean(data))
    await ref.insert()
    await record_new(ref, actor=user.email)
    return ref.api()


@router.put("/{id}")
async def update_ref(id: PydanticObjectId, data: RefIn, user: User = Depends(active_user)):
    ref = await own_ref(id, user)
    await record(ref, clean(data), actor=user.email)
    return ref.api()


@router.delete("/{id}")
async def delete_ref(id: PydanticObjectId, user: User = Depends(active_user)):
    ref = await own_ref(id, user)
    await record_delete(ref, actor=user.email)
    return {"ok": True}
