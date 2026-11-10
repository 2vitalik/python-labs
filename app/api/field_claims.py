"""Cards about the field live on the field (T274 §3): claimed with no place, they go onto it, and those claimed before
it was described wait unanchored and sit on it once it is."""
from core.models.history import record
from models.game import Claim, Game, Part
from models.task import Task
from zones import kind_of


async def field_of(game: Game, task: Task) -> str:
    """The field's id for a field card claimed with no place; "" — no field yet, or the card is not about it."""
    field = kind_of(task) == "field" and await Part.find_one(Part.game == game.id, Part.kind == "field")
    return str(field.id) if field else ""


async def seat(game: Game, field: Part, actor: str) -> None:
    waiting = [c for c in await Claim.find(Claim.game == game.id, Claim.part == "").to_list() if not c.rule]
    cards = {t.slug for t in await Task.find({"slug": {"$in": [c.task for c in waiting]}}).to_list() if kind_of(t) == "field"}
    for c in waiting:
        if c.task in cards:
            await record(c, {"part": str(field.id)}, actor=actor)
