"""What the model's answer is checked against (T291 §14): the cards a claim may name, the catalog's options, and what the
game already has — to say «уже є» and to point rules at its entities and windows."""
from dataclasses import dataclass

import options
from models.base_game import BaseGame
from models.game import Claim, Game, Part
from models.rule import Rule
from models.task import Task
from template_rules import sentence_key


@dataclass
class Ctx:
    cards: dict[str, Task]  # slug → card: active ones, drafts too for the admin (as options.catalog)
    cat: dict  # options.catalog(): roles, stats, field options
    parts: dict[tuple, tuple]  # (kind, title.lower()) → (id, title) of the game's parts
    field: str  # the game's field part id; "" — none
    rules: dict[str, str]  # sentence_key() → id of the game's rules
    claimed: set  # (task, part, rule) of the game's claims

    def part(self, kind: str, title: str) -> tuple | None:
        return self.parts.get((kind, title.strip().lower()))


async def cards(admin: bool) -> dict[str, Task]:
    return {t.slug: t for t in await Task.find({"status": {"$in": ["active", "draft"] if admin else ["active"]}}).to_list()}


async def of_game(game: Game, admin: bool) -> Ctx:
    parts = await Part.find(Part.game == game.id).to_list()
    return Ctx(await cards(admin), await options.catalog(admin), {(p.kind, p.title.lower()): (str(p.id), p.title) for p in parts},
               next((str(p.id) for p in parts if p.kind == "field"), ""),
               {sentence_key(r.when, r.cond, r.then): str(r.id) for r in await Rule.find(Rule.game == game.id).to_list()},
               {(c.task, c.part, c.rule) for c in await Claim.find(Claim.game == game.id).to_list()})


async def of_names(names: list[str]) -> Ctx:
    """ai.replay: an empty game, or one with these entities and windows (a name stands for both)."""
    parts = {(kind, n.lower()): (f"have-{i}", n) for i, n in enumerate(names) for kind in ("entity", "window")}
    return Ctx(await cards(False), await options.catalog(False), parts, "", {}, set())


async def have(game: Game, ctx: Ctx) -> dict:
    """The «Уже є в грі» block of the user's message (prompt.message)."""
    base = await BaseGame.find_one(BaseGame.slug == game.base_game) if game.base_game else None
    titles = lambda kind: [t for (k, _), (_, t) in ctx.parts.items() if k == kind]  # noqa: E731
    return {"base": base.title if base else game.base_custom, "field": bool(ctx.field),
            "entities": titles("entity"), "windows": titles("window"), "levels": titles("level")}
