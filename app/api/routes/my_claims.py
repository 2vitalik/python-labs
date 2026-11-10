from beanie import PydanticObjectId
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel

from bot import game_alerts
from claims_clean import clean_params
from core.deps import active_user
from core.models.history import record, record_delete, record_new
from core.models.user import Status, User
from models.game import Claim, Game
from models.rule import Rule
from models.task import Task
from routes.my_game import my_game
from routes.my_parts import part_of
from zones import kind_of, misplaced

router = APIRouter(prefix="/api/my/claims")
HELD = "Ця заявка тримається сама: зміни тип, параметр чи властивість."


class ClaimIn(BaseModel):
    task: str = ""
    part: str | None = None  # None on PUT = leave as is; "" = unanchored: game level / the drafts pool
    rule: str | None = None  # a rule's id — for cards of kind rule; the same None / "" as part
    params: dict | None = None  # None on PUT = leave as is
    note: str = ""
    link: str = ""


async def get_claim(id: PydanticObjectId, game: Game) -> Claim:
    claim = await Claim.get(id)
    if not claim or claim.game != game.id:
        raise HTTPException(404)
    return claim


async def check_place(game: Game, task: Task | None, part: str, rule: str) -> None:
    """The anchor exists in this game, and the card's kind may live there."""
    if part and rule:
        raise HTTPException(422, "Заявка — або на обʼєкті, або на правилі.")
    where = ""
    if part:
        if not (p := await part_of(game, part)):
            raise HTTPException(422, "Обʼєкт не знайдено.")
        where = p.kind
    if rule:
        r = await Rule.get(PydanticObjectId(rule)) if PydanticObjectId.is_valid(rule) else None
        if not r or r.game != game.id:
            raise HTTPException(422, "Правило не знайдено.")
        where = "rule"
    if task and (why := misplaced(kind_of(task), where)):
        raise HTTPException(422, why)


async def check_unique(game: Game, task: str, part: str, rule: str, me: Claim | None = None) -> None:
    same = [c for c in await Claim.find(Claim.game == game.id, Claim.task == task).to_list()
            if c.part == part and c.rule == rule and (not me or c.id != me.id)]  # filtered here: old claims have no `rule`
    if same:
        raise HTTPException(409, "Така заявка вже є." if part or rule else "Така заявка вже є серед заявок гри.")


@router.post("")
async def create_claim(data: ClaimIn, tasks: BackgroundTasks, game: Game = Depends(my_game),
                       user: User = Depends(active_user)):
    task = await Task.find_one(Task.slug == data.task)
    if not task or task.status == "archived":
        raise HTTPException(422, "Немає такої картки в каталозі.")
    if task.status != "active" and user.status != Status.admin:
        raise HTTPException(422, "Ця картка ще чернетка.")
    part, rule = data.part or "", data.rule or ""
    await check_place(game, task, part, rule)
    await check_unique(game, data.task, part, rule)
    claim = Claim(game=game.id, task=data.task, part=part, rule=rule, note=data.note.strip(), link=data.link.strip(),
                  params=clean_params(task, data.params or {}, loose=not (part or rule)))
    await claim.insert()
    await record_new(claim, actor=user.email)
    tasks.add_task(game_alerts.claim, user, claim, 0)
    return claim.api()


@router.put("/{id}")
async def update_claim(id: PydanticObjectId, data: ClaimIn, tasks: BackgroundTasks, game: Game = Depends(my_game),
                       user: User = Depends(active_user)):
    claim = await get_claim(id, game)
    patch = {"note": data.note.strip(), "link": data.link.strip()}
    if claim.auto:  # its anchor and value are the part's: only the note and the link are the student's
        if data.part not in (None, claim.part) or data.rule not in (None, claim.rule) or data.params not in (None, claim.params):
            raise HTTPException(422, HELD)
    else:
        task = await Task.find_one(Task.slug == claim.task)
        part = data.part if data.part is not None else "" if data.rule else claim.part  # anchoring on one lets go of the other
        rule = data.rule if data.rule is not None else "" if data.part else claim.rule
        if (part, rule) != (claim.part, claim.rule):
            await check_place(game, task, part, rule)
            await check_unique(game, claim.task, part, rule, me=claim)
            patch |= {"part": part, "rule": rule}
        if task:  # card gone from the catalog → params frozen as claimed
            params = claim.params if data.params is None else data.params
            patch["params"] = clean_params(task, params, loose=not (part or rule))
    if changes := await record(claim, patch, actor=user.email):
        tasks.add_task(game_alerts.claim, user, claim, 1, changes)
    return claim.api()


@router.delete("/{id}")
async def delete_claim(id: PydanticObjectId, tasks: BackgroundTasks, game: Game = Depends(my_game),
                       user: User = Depends(active_user)):
    claim = await get_claim(id, game)
    if claim.auto:
        raise HTTPException(422, HELD)
    await record_delete(claim, actor=user.email)
    tasks.add_task(game_alerts.claim, user, claim, 2)
    return {"ok": True}
