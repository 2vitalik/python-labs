from datetime import datetime, timezone
from typing import Annotated

from beanie import Document, Indexed, PydanticObjectId
from pydantic import Field

ROLES = ("player", "enemy", "object", "pickup", "static")
# rule dictionaries grow by the rule of three (T98); value = argument spec
TRIGGERS = {"contact": ("a", "b"), "timer": ("every",)}
EFFECTS = {
    "disappear_a": None, "disappear_b": None, "disappear_both": None,
    "block": None, "push": None, "pickup": None, "teleport": None,
    "damage": "n", "score": "n", "spawn": "entity", "transform": "entity",
    "window": "window", "win": None, "lose": None, "custom": "text",
}


class Rule(Document):
    """A game rule as a WHEN→[IF]→THEN sentence built from dictionaries (T98)."""
    game: Annotated[PydanticObjectId, Indexed()]
    when: dict  # {kind: TRIGGERS key, ...args}
    cond: dict = {}  # optional IF — dictionary comes in a later phase
    then: list[dict]  # effects: {kind: EFFECTS key, ...args}
    note: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "rules"

    def api(self) -> dict:
        return {
            "id": str(self.id), "game": str(self.game), "when": self.when, "cond": self.cond,
            "then": self.then, "note": self.note, "created_at": self.created_at.isoformat(),
        }

    def uses(self, part_id: str) -> bool:
        return part_id in (self.when.get("a"), self.when.get("b")) or \
            any(e.get("part") == part_id for e in self.then)
