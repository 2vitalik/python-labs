from datetime import datetime, timezone
from typing import Annotated

from beanie import Document, Indexed, PydanticObjectId
from pydantic import Field, field_validator

from models.vocab import CONDITIONS, EFFECTS, TRIGGERS  # noqa: F401 — the dictionaries live in vocab.py, routes import them from here too


class Rule(Document):
    """A game rule as a WHEN→[IF]→THEN sentence built from the dictionaries (T98, T257)."""
    game: Annotated[PydanticObjectId, Indexed()]
    when: dict  # {kind: TRIGGERS key, ...args}
    cond: list[dict] = []  # IF, all must hold: {kind: CONDITIONS key, not?: true, ...args}
    then: list[dict]  # effects: {kind: EFFECTS key, ...args}
    note: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "rules"

    @field_validator("cond", mode="before")
    @classmethod
    def cond_as_list(cls, v):  # v1 stored a dict here, always empty
        if isinstance(v, dict):
            return [v] if v else []
        return v

    def api(self) -> dict:
        return {
            "id": str(self.id), "game": str(self.game), "when": self.when, "cond": self.cond,
            "then": self.then, "note": self.note, "created_at": self.created_at.isoformat(),
        }

    def refs(self) -> set[str]:
        """Every Part id the sentence names — in the trigger, the conditions or the effects."""
        items = [self.when, *self.cond, *self.then]
        return {str(v) for it in items for k, v in it.items() if k not in ("kind", "not") and isinstance(v, str)}

    def uses(self, part_id: str) -> bool:
        return part_id in self.refs()
