"""An entity's state renamed (T344). The rules name a state by its word, so a rename is one step here: the word changes on
the card and in every rule that means this entity's state — renamed on the card alone, the rules would name nothing."""
from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from core.models.history import record
from core.models.user import User
from models.game import Game, Part
from models.rule import Rule
from parts_clean import clean_states
from routes.my_game import author, my_game
from routes.my_parts import get_part

router = APIRouter(prefix="/api/my/game/parts")


class RenameIn(BaseModel):
    old: str
    new: str


def means(item: dict, when: dict, pid: str, lone: bool) -> bool:
    """Is the clause about this entity: its `a` is the entity, or a side of the trigger that is. A clause about anyone
    counts while no other entity has a state of that word (`lone`)."""
    a = str(item.get("a") or "")
    who = str(when.get(a[1:]) or "") if a in ("@a", "@b") else a
    return who == pid or (lone and (not who or who[0] in "@*"))


def renamed(rule: Rule, pid: str, old: str, new: str, lone: bool) -> dict:
    """The rule's clauses with the state's new word; {} — it does not name the state."""
    def fix(item: dict) -> dict:
        return item | {"s": new} if item.get("s") == old and means(item, rule.when, pid, lone) else item
    patch = {"when": fix(rule.when), "cond": [fix(c) for c in rule.cond], "then": [fix(e) for e in rule.then]}
    return {k: v for k, v in patch.items() if v != getattr(rule, k)}


@router.post("/{id}/states/rename")
async def rename_state(id: PydanticObjectId, data: RenameIn, game: Game = Depends(my_game), user: User = Depends(author)):
    part = await get_part(id, game)
    new = " ".join(data.new.split())
    if part.kind != "entity" or data.old not in part.states:
        raise HTTPException(404, "Такого стану в цієї сутності вже нема — онови сторінку.")
    if not new:
        raise HTTPException(422, "Назва стану — не порожня.")
    states = [new if s == data.old else s for s in part.states]
    if len(clean_states(states)) != len(states):
        raise HTTPException(422, f"Стан «{new}» у цієї сутності вже є.")
    others = [p for p in await Part.find(Part.game == game.id, Part.kind == "entity").to_list() if p.id != part.id]
    lone = not any(data.old in p.states for p in others)
    rules = 0
    for rule in await Rule.find(Rule.game == game.id).to_list():
        if patch := renamed(rule, str(part.id), data.old, new, lone):
            await record(rule, patch, actor=user.email)
            rules += 1
    await record(part, {"states": states}, actor=user.email)
    return {"part": part.api(), "rules": rules}
