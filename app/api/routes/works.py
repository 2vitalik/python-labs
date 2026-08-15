from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from deps import active_user
from models.game import Game
from models.history import record, record_new
from models.task import Task
from models.user import User
from models.work import Claim, Work, WorkObject

router = APIRouter(prefix="/api/works")


class WorkIn(BaseModel):
    title: str
    base_game: str = ""
    base_custom: str = ""
    description: str = ""


async def my_work(user: User = Depends(active_user)) -> Work:
    work = await Work.find_one(Work.owner == user.email)
    if not work:
        raise HTTPException(404, "Спершу створи свою гру.")
    return work


async def clean(data: WorkIn) -> dict:
    d = data.model_dump()
    d["title"] = d["title"].strip()
    if not d["title"]:
        raise HTTPException(422, "Назва — обовʼязкова.")
    if d["base_game"]:
        if not await Game.find_one(Game.slug == d["base_game"]):
            raise HTTPException(422, "Немає такої гри-основи в каталозі.")
    elif not d["base_custom"].strip():
        raise HTTPException(422, "Обери гру-основу з каталогу або опиши свою.")
    return d


async def task_index(slugs: set[str]) -> dict:
    """Minimal card info for rendering claims/objects, drafts included (viewer may not see them in the catalog)."""
    tasks = await Task.find({"slug": {"$in": list(slugs)}}).to_list()
    return {t.slug: {"title": t.title, "coin": t.coin, "amount": t.amount,
                     "zone": t.zone, "subzone": t.subzone, "status": t.status} for t in tasks}


def owner_info(u: User | None) -> dict:
    if not u:
        return {}
    full = " ".join(x for x in (u.last_name, u.first_name) if x)
    return {"name": full or u.name, "group": u.group, "picture": u.picture}


@router.get("")
async def list_works(user: User = Depends(active_user)):
    works = await Work.find_all().sort("-created_at").to_list()
    users = {u.email: u for u in await User.find({"email": {"$in": [w.owner for w in works]}}).to_list()}
    out = []
    for w in works:
        objects = await WorkObject.find(WorkObject.work == w.id).sort("order", "created_at").to_list()
        shots = [(str(o.id), s) for o in objects for s in o.screenshots]
        out.append(w.api() | {
            "owner_info": owner_info(users.get(w.owner)),
            "windows": sum(o.kind == "window" for o in objects), "menus": sum(o.kind == "menu" for o in objects),
            "claims": await Claim.find(Claim.work == w.id).count(),
            "cover": f"/api/uploads/{w.id}/{shots[0][1]}" if shots else "",
        })
    return out


@router.get("/my")
async def get_my_work(user: User = Depends(active_user)):
    work = await Work.find_one(Work.owner == user.email)
    return work.api() if work else None


@router.post("")
async def create_work(data: WorkIn, user: User = Depends(active_user)):
    if await Work.find_one(Work.owner == user.email):
        raise HTTPException(409, "Гра вже створена — вона в тебе одна.")
    work = Work(owner=user.email, **await clean(data))
    await work.insert()
    await record_new(work, actor=user.email)
    return work.api()


@router.put("/my")
async def update_work(data: WorkIn, work: Work = Depends(my_work), user: User = Depends(active_user)):
    await record(work, await clean(data), actor=user.email)
    return work.api()


@router.get("/{id}")
async def get_work(id: PydanticObjectId, user: User = Depends(active_user)):
    work = await Work.get(id)
    if not work:
        raise HTTPException(404)
    objects = await WorkObject.find(WorkObject.work == work.id).sort("order", "created_at").to_list()
    claims = await Claim.find(Claim.work == work.id).sort("created_at").to_list()
    slugs = {o.task for o in objects if o.task} | {c.task for c in claims} | \
            {i["task"] for o in objects for i in o.items if i.get("task")}
    return {
        "work": work.api(), "owner_info": owner_info(await User.find_one(User.email == work.owner)),
        "objects": [o.api() for o in objects], "claims": [c.api() for c in claims],
        "tasks": await task_index(slugs), "mine": work.owner == user.email,
    }
