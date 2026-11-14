from beanie import PydanticObjectId
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel

import field_claims
import uploads
from bot import game_alerts
from claims_clean import clean_params
from core.models.history import record, record_delete, record_new
from core.models.user import Status, User
from models.game import Claim, Game
from models.rule import Rule
from models.task import Task
from pricing import cap, repeatable
from routes.my_game import author, my_game
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


async def check_unique(game: Game, slug: str, part: str, rule: str, task: Task | None, me: Claim | None = None) -> None:
    """One claim of a card per place; a card with repeats goes again with no place, up to its cap (T291 §13)."""
    mine = [c for c in await Claim.find(Claim.game == game.id, Claim.task == slug).to_list() if not me or c.id != me.id]
    if not any(c.part == part and c.rule == rule for c in mine):  # compared here: old claims have no `rule`
        return
    if part or rule:
        raise HTTPException(409, "Така заявка вже є.")
    if not task or not repeatable(task):
        raise HTTPException(409, "Така заявка вже є серед заявок гри.")
    if (n := cap(task)) and len(mine) >= n:
        raise HTTPException(409, f"Цю картку вже заявлено {times(len(mine))} — більше не зараховується.")


def times(n: int) -> str:
    few = n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14)
    return f"{n} " + ("раз" if n % 10 == 1 and n % 100 != 11 else "рази" if few else "разів")


@router.post("")
async def create_claim(data: ClaimIn, tasks: BackgroundTasks, game: Game = Depends(my_game),
                       user: User = Depends(author)):
    task = await Task.find_one(Task.slug == data.task)
    if not task or task.status == "archived":
        raise HTTPException(422, "Немає такої картки в каталозі.")
    if task.status != "active" and user.status != Status.admin:
        raise HTTPException(422, "Ця картка ще чернетка.")
    part, rule = data.part or "", data.rule or ""
    loose = not (part or rule)  # sent with no place («＋ у гру»): required params may wait, even once it sits on the field
    if loose:
        part = await field_claims.field_of(game, task)
        if part and repeatable(task) and await Claim.find_one(Claim.game == game.id, Claim.task == task.slug, Claim.part == part):
            part = ""  # the field holds it already: a repeat stays at game level (T291 §13)
    await check_place(game, task, part, rule)
    await check_unique(game, data.task, part, rule, task)
    claim = Claim(game=game.id, task=data.task, part=part, rule=rule, note=data.note.strip(), link=data.link.strip(),
                  params=clean_params(task, data.params or {}, loose=loose))
    await claim.insert()
    await record_new(claim, actor=user.email)
    tasks.add_task(game_alerts.claim, user, claim, 0)
    return claim.api()


@router.put("/{id}")
async def update_claim(id: PydanticObjectId, data: ClaimIn, tasks: BackgroundTasks, game: Game = Depends(my_game),
                       user: User = Depends(author)):
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
            await check_unique(game, claim.task, part, rule, task, me=claim)
            patch |= {"part": part, "rule": rule}
        if task:  # card gone from the catalog → params frozen as claimed
            params = claim.params if data.params is None else data.params
            patch["params"] = clean_params(task, params, loose=not (part or rule))
    if changes := await record(claim, patch, actor=user.email):
        tasks.add_task(game_alerts.claim, user, claim, 1, changes)
    return claim.api()


@router.delete("/{id}")
async def delete_claim(id: PydanticObjectId, tasks: BackgroundTasks, game: Game = Depends(my_game),
                       user: User = Depends(author)):
    claim = await get_claim(id, game)
    if claim.auto:
        raise HTTPException(422, HELD)
    uploads.drop_shots(claim)
    await record_delete(claim, actor=user.email)
    tasks.add_task(game_alerts.claim, user, claim, 2)
    return {"ok": True}
