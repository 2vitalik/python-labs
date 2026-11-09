from beanie import PydanticObjectId
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel

from bot import game_alerts
from core.deps import active_user
from core.models.history import record, record_delete, record_new
from core.models.user import User
from models.game import Game, Part
from models.rule import Rule
from models.vocab import CONDITIONS, EFFECTS, OPTIONS, SIDES, TRIGGERS
from routes.my_game import my_game

router = APIRouter(prefix="/api/my/game/rules")


class RuleIn(BaseModel):
    when: dict = {}
    cond: list[dict] = []
    then: list[dict] = []
    note: str = ""


def clean_item(dic: dict, item: dict, ids: dict, sides: set, what: str) -> dict:
    """One word of a sentence with its arguments, checked against the dictionary's arg specs."""
    spec = dic.get(item.get("kind"))
    if not spec:
        raise HTTPException(422, f"Невідоме слово {what}: «{item.get('kind')}».")
    out = {"kind": item["kind"]}
    for a in spec["args"]:
        v = item.get(a["name"])
        if v is None or v == "":
            if a["required"]:
                raise HTTPException(422, f"«{spec['label']}»: не вистачає «{a['name']}».")
            continue
        t = a["type"]
        if t == "entity":
            if v not in sides and v not in ids["entity"]:
                raise HTTPException(422, f"«{spec['label']}»: сутність має бути з твоєї гри.")
        elif t == "window":
            if v not in ids["window"]:
                raise HTTPException(422, f"«{spec['label']}»: вікно має бути з твоєї гри.")
        elif t == "int":
            try:
                v = int(v)
            except (TypeError, ValueError):
                raise HTTPException(422, f"«{spec['label']}»: «{a['name']}» — число.")
            if a["name"] in ("every", "p", "dur", "n") and v < 0 and item["kind"] not in ("lives", "score", "currency", "counter", "grow", "speed"):
                raise HTTPException(422, f"«{spec['label']}»: «{a['name']}» — не менше 0.")
        elif t == "bool":
            v = bool(v)
        elif t.startswith("choice:"):
            if str(v) not in OPTIONS[t[7:]]:
                raise HTTPException(422, f"«{spec['label']}»: «{a['name']}» — зі списку.")
            v = str(v)
        else:
            v = " ".join(str(v).split())
            if not v:
                raise HTTPException(422, f"«{spec['label']}»: «{a['name']}» — порожнє.")
        out[a["name"]] = v
    if dic is CONDITIONS and item.get("not"):
        out["not"] = True
    return out


async def clean(data: RuleIn, game: Game) -> dict:
    parts = await Part.find(Part.game == game.id).to_list()
    ids = {kind: {str(p.id) for p in parts if p.kind == kind} for kind in ("entity", "window")}
    when = clean_item(TRIGGERS, data.when, ids, {"*"}, "КОЛИ")
    # @a / @b point at the trigger's sides — only when it has them
    sides = {"*"} | {s for s in ("@a", "@b") if s[1:] in when} | ({"@both"} if "a" in when and "b" in when else set())
    cond = [clean_item(CONDITIONS, c, ids, sides, "ЯКЩО") for c in data.cond]
    then = [clean_item(EFFECTS, e, ids, sides, "ТО") for e in data.then]
    if not then:
        raise HTTPException(422, "Хоч один ефект ТО.")
    return {"when": when, "cond": cond, "then": then, "note": data.note.strip()}


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


SIDE_NAMES = SIDES  # re-export for the bot's sentence rendering
