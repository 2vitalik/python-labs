from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from pydantic import BaseModel

import uploads
from deps import active_user
from models.history import record, record_delete, record_new
from models.task import Task
from models.user import Status, User
from models.work import Claim, Work, WorkObject
from routes.works import my_work

router = APIRouter(prefix="/api/works/my/objects")


class ObjectIn(BaseModel):
    kind: str = ""  # window | menu; fixed after creation
    title: str
    task: str = ""  # window type: catalog slug tagged "window"
    description: str = ""
    window: str = ""  # menu: host window object id
    items: list[dict] = []
    order: int = 0


async def obj_of(work: Work, oid: str, kind: str = "") -> WorkObject | None:
    try:
        obj = await WorkObject.get(PydanticObjectId(oid))
    except Exception:
        return None
    ok = obj and obj.work == work.id and (not kind or obj.kind == kind)
    return obj if ok else None


async def get_object(id: PydanticObjectId, work: Work) -> WorkObject:
    obj = await obj_of(work, str(id))
    if not obj:
        raise HTTPException(404)
    return obj


async def check_window_type(slug: str, user: User) -> None:
    task = await Task.find_one(Task.slug == slug)
    if not task or "window" not in task.tags or task.status == "archived":
        raise HTTPException(422, "Тип вікна — картка каталогу з тегом window.")
    if task.status != "active" and user.status != Status.admin:
        raise HTTPException(422, "Ця картка-тип ще чернетка.")


async def clean_menu(data: ObjectIn, work: Work) -> dict:
    if data.window and not await obj_of(work, data.window, kind="window"):
        raise HTTPException(422, "Вікно-хост не знайдено.")
    items = []
    for it in data.items:
        item = {k: str(it.get(k) or "").strip() for k in ("title", "window", "task", "note")}
        if not item["title"]:
            continue
        if item["window"] and not await obj_of(work, item["window"], kind="window"):
            raise HTTPException(422, f"Пункт «{item['title']}»: цільове вікно не знайдено.")
        if item["task"] and not await Task.find_one(Task.slug == item["task"]):
            raise HTTPException(422, f"Пункт «{item['title']}»: немає такої картки.")
        items.append(item)
    return {"window": data.window, "items": items}


@router.post("")
async def create_object(data: ObjectIn, work: Work = Depends(my_work), user: User = Depends(active_user)):
    if data.kind not in ("window", "menu"):
        raise HTTPException(422, "Невідомий тип обʼєкта.")
    d = {"work": work.id, "kind": data.kind, "title": data.title.strip(),
         "description": data.description, "order": data.order}
    if not d["title"]:
        raise HTTPException(422, "Назва — обовʼязкова.")
    if data.kind == "window":
        await check_window_type(data.task, user)
        d["task"] = data.task
    else:
        d |= await clean_menu(data, work)
    obj = WorkObject(**d)
    await obj.insert()
    await record_new(obj, actor=user.email)
    if data.kind == "window":  # a window claims its type card automatically
        claim = Claim(work=work.id, task=data.task, object=str(obj.id))
        await claim.insert()
        await record_new(claim, actor=user.email)
    return obj.api()


@router.put("/{id}")
async def update_object(id: PydanticObjectId, data: ObjectIn, work: Work = Depends(my_work),
                        user: User = Depends(active_user)):
    obj = await get_object(id, work)
    d = {"title": data.title.strip(), "description": data.description, "order": data.order}
    if not d["title"]:
        raise HTTPException(422, "Назва — обовʼязкова.")
    if obj.kind == "menu":
        d |= await clean_menu(data, work)
    await record(obj, d, actor=user.email)
    return obj.api()


@router.delete("/{id}")
async def delete_object(id: PydanticObjectId, work: Work = Depends(my_work), user: User = Depends(active_user)):
    obj = await get_object(id, work)
    for claim in await Claim.find(Claim.work == work.id, Claim.object == str(obj.id)).to_list():
        await claim.delete()
    for name in obj.screenshots:
        uploads.drop_shot(str(work.id), name)
    if obj.kind == "window":  # strip dangling references from menus
        oid = str(obj.id)
        for menu in await WorkObject.find(WorkObject.work == work.id, WorkObject.kind == "menu").to_list():
            patch = {"window": ""} if menu.window == oid else {}
            items = [it | {"window": ""} if it.get("window") == oid else it for it in menu.items]
            if items != menu.items:
                patch["items"] = items
            if patch:
                await record(menu, patch, actor=user.email)
    await record_delete(obj, actor=user.email)
    return {"ok": True}


@router.post("/{id}/screenshot")
async def add_screenshot(id: PydanticObjectId, file: UploadFile, work: Work = Depends(my_work),
                         user: User = Depends(active_user)):
    obj = await get_object(id, work)
    name = await uploads.save_shot(str(work.id), file)
    await record(obj, {"screenshots": obj.screenshots + [name]}, actor=user.email)
    return obj.api()


@router.delete("/{id}/screenshot/{name}")
async def delete_screenshot(id: PydanticObjectId, name: str, work: Work = Depends(my_work),
                            user: User = Depends(active_user)):
    obj = await get_object(id, work)
    if name not in obj.screenshots:
        raise HTTPException(404)
    uploads.drop_shot(str(work.id), name)
    await record(obj, {"screenshots": [s for s in obj.screenshots if s != name]}, actor=user.email)
    return obj.api()
