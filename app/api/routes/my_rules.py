from beanie import PydanticObjectId
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel

from bot import game_alerts
from deps import active_user
from models.game import Game, Part
from models.history import record, record_delete, record_new
from models.rule import EFFECTS, TRIGGERS, Rule
from models.user import User
from routes.my_game import my_game

router = APIRouter(prefix="/api/my/game/rules")


class RuleIn(BaseModel):
    when: dict = {}
    then: list[dict] = []
    note: str = ""


def need_int(d: dict, key: str, minimum: int | None = 1) -> int:
    try:
        n = int(d.get(key))
    except (TypeError, ValueError):
        raise HTTPException(422, f"«{key}» — число.")
    if minimum is not None and n < minimum:
        raise HTTPException(422, f"«{key}» — від {minimum}.")
    return n


async def clean(data: RuleIn, game: Game) -> dict:
    parts = await Part.find(Part.game == game.id).to_list()
    ids = {kind: {str(p.id) for p in parts if p.kind == kind} for kind in ("entity", "window")}

    kind = data.when.get("kind")
    if kind == "contact":
        a, b = data.when.get("a"), data.when.get("b")
        if a not in ids["entity"] or b not in ids["entity"]:
            raise HTTPException(422, "Обидві сторони контакту — сутності твоєї гри.")
        when = {"kind": kind, "a": a, "b": b}
    elif kind == "timer":
        when = {"kind": kind, "every": need_int(data.when, "every")}
    else:
        raise HTTPException(422, "Невідомий тригер КОЛИ.")

    effects = []
    for e in data.then:
        if e.get("kind") not in EFFECTS:
            raise HTTPException(422, "Невідомий ефект ТО.")
        out = {"kind": e["kind"]}
        arg = EFFECTS[e["kind"]]
        if arg == "n":
            out["n"] = need_int(e, "n", minimum=None if e["kind"] == "score" else 1)
        elif arg in ("entity", "window"):
            if e.get("part") not in ids[arg]:
                raise HTTPException(422, "Ціль ефекту — сутність чи вікно твоєї гри.")
            out["part"] = e["part"]
        elif arg == "text":
            out["text"] = str(e.get("text") or "").strip()
            if not out["text"]:
                raise HTTPException(422, "Ефект «інше» — опиши текстом.")
        effects.append(out)
    if not effects:
        raise HTTPException(422, "Хоч один ефект ТО.")
    return {"when": when, "then": effects, "note": data.note.strip()}


async def get_rule(id: PydanticObjectId, game: Game) -> Rule:
    rule = await Rule.get(id)
    if not rule or rule.game != game.id:
        raise HTTPException(404)
    return rule


@router.post("")
async def create_rule(data: RuleIn, tasks: BackgroundTasks, game: Game = Depends(my_game),
                      user: User = Depends(active_user)):
    rule = Rule(game=game.id, **await clean(data, game))
    await rule.insert()
    await record_new(rule, actor=user.email)
    tasks.add_task(game_alerts.rule, user, rule, 0)
    return rule.api()


@router.put("/{id}")
async def update_rule(id: PydanticObjectId, data: RuleIn, game: Game = Depends(my_game),
                      user: User = Depends(active_user)):
    rule = await get_rule(id, game)
    await record(rule, await clean(data, game), actor=user.email)
    return rule.api()


@router.delete("/{id}")
async def delete_rule(id: PydanticObjectId, tasks: BackgroundTasks, game: Game = Depends(my_game),
                      user: User = Depends(active_user)):
    rule = await get_rule(id, game)
    await record_delete(rule, actor=user.email)
    tasks.add_task(game_alerts.rule, user, rule, 2)
    return {"ok": True}
