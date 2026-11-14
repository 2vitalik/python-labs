from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException

from core.deps import editor_user, viewer
from core.models.history import record, record_new
from core.models.user import Status, User
from models.task import Task
from tasks_clean import TaskIn, clean

router = APIRouter(prefix="/api/tasks")


@router.get("")
async def list_tasks(user: User | None = Depends(viewer)):
    tasks = await Task.find_all().sort("zone", "subzone", "order", "slug").to_list()
    if not user or user.status != Status.admin:  # guests see the catalog too, active only
        tasks = [t for t in tasks if t.status == "active"]
    return [t.api() for t in tasks]


@router.post("")
async def create_task(data: TaskIn, admin: User = Depends(editor_user)):
    d = await clean(data)
    if await Task.find_one(Task.slug == d["slug"]):
        raise HTTPException(422, "Завдання з таким slug уже існує.")
    task = Task(**d)
    await task.insert()
    await record_new(task, actor=admin.email)
    return task.api()


@router.put("/{id}")
async def update_task(id: PydanticObjectId, data: TaskIn, admin: User = Depends(editor_user)):
    task = await Task.get(id)
    if not task:
        raise HTTPException(404)
    d = await clean(data, task)
    other = await Task.find_one(Task.slug == d["slug"])
    if other and other.id != task.id:
        raise HTTPException(422, "Завдання з таким slug уже існує.")
    await record(task, d, actor=admin.email)
    return task.api()
