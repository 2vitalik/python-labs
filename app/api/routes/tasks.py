from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from deps import active_user, admin_user
from models.history import record, record_new
from models.task import Task
from models.user import Status, User
from zones import COINS, STATUSES, ZONES

router = APIRouter(prefix="/api/tasks")


class VariantIn(BaseModel):
    slug: str
    title: str
    coin: str = ""
    amount: float = 1


class TaskIn(BaseModel):
    slug: str
    title: str
    description: str = ""
    zone: str
    subzone: str
    tags: list[str] = []
    games: list[str] = []
    coin: str = ""
    amount: float = 1
    max_count: int = 1
    variants: list[VariantIn] = []
    status: str = "draft"
    order: int = 0


def clean(data: TaskIn) -> dict:
    d = data.model_dump()
    d["slug"], d["title"] = d["slug"].strip().lower(), d["title"].strip()
    if not d["slug"] or not d["title"]:
        raise HTTPException(422, "Slug і назва — обовʼязкові.")
    if d["zone"] not in ZONES or d["subzone"] not in ZONES[d["zone"]]["subzones"]:
        raise HTTPException(422, "Невідома зона або підзона.")
    coins = [d["coin"]] + [v["coin"] for v in d["variants"]]
    if any(c and c not in COINS for c in coins):
        raise HTTPException(422, "Невідомий тип монетки.")
    if d["status"] not in STATUSES:
        raise HTTPException(422, "Невідомий статус.")
    return d


@router.get("")
async def list_tasks(user: User = Depends(active_user)):
    tasks = await Task.find_all().sort("zone", "subzone", "order", "slug").to_list()
    if user.status != Status.admin:
        tasks = [t for t in tasks if t.status == "active"]
    return [t.api() for t in tasks]


@router.post("")
async def create_task(data: TaskIn, admin: User = Depends(admin_user)):
    d = clean(data)
    if await Task.find_one(Task.slug == d["slug"]):
        raise HTTPException(422, "Завдання з таким slug уже існує.")
    task = Task(**d)
    await task.insert()
    await record_new(task, actor=admin.email)
    return task.api()


@router.put("/{id}")
async def update_task(id: PydanticObjectId, data: TaskIn, admin: User = Depends(admin_user)):
    task = await Task.get(id)
    if not task:
        raise HTTPException(404)
    d = clean(data)
    other = await Task.find_one(Task.slug == d["slug"])
    if other and other.id != task.id:
        raise HTTPException(422, "Завдання з таким slug уже існує.")
    await record(task, d, actor=admin.email)
    return task.api()
