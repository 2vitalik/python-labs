from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from deps import active_user
from models.history import record, record_delete, record_new
from models.task import Task
from models.user import Status, User
from models.work import Claim, Work
from routes.work_objects import obj_of
from routes.works import my_work

router = APIRouter(prefix="/api/works/my/claims")


class ClaimIn(BaseModel):
    task: str = ""
    object: str = ""
    note: str = ""
    link: str = ""


async def get_claim(id: PydanticObjectId, work: Work) -> Claim:
    claim = await Claim.get(id)
    if not claim or claim.work != work.id:
        raise HTTPException(404)
    return claim


@router.post("")
async def create_claim(data: ClaimIn, work: Work = Depends(my_work), user: User = Depends(active_user)):
    task = await Task.find_one(Task.slug == data.task)
    if not task or task.status == "archived":
        raise HTTPException(422, "Немає такої картки в каталозі.")
    if task.status != "active" and user.status != Status.admin:
        raise HTTPException(422, "Ця картка ще чернетка.")
    if data.object and not await obj_of(work, data.object):
        raise HTTPException(422, "Обʼєкт не знайдено.")
    if await Claim.find_one(Claim.work == work.id, Claim.task == data.task, Claim.object == data.object):
        raise HTTPException(409, "Така заявка вже є.")
    claim = Claim(work=work.id, task=data.task, object=data.object,
                  note=data.note.strip(), link=data.link.strip())
    await claim.insert()
    await record_new(claim, actor=user.email)
    return claim.api()


@router.put("/{id}")
async def update_claim(id: PydanticObjectId, data: ClaimIn, work: Work = Depends(my_work),
                       user: User = Depends(active_user)):
    claim = await get_claim(id, work)
    await record(claim, {"note": data.note.strip(), "link": data.link.strip()}, actor=user.email)
    return claim.api()


@router.delete("/{id}")
async def delete_claim(id: PydanticObjectId, work: Work = Depends(my_work), user: User = Depends(active_user)):
    claim = await get_claim(id, work)
    await record_delete(claim, actor=user.email)
    return {"ok": True}
