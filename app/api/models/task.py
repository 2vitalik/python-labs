from datetime import datetime, timezone
from typing import Annotated

from beanie import Document, Indexed
from pydantic import Field, field_validator

from zones import kind_of

LANGS = ("uk", "ru", "en")
PROOFS = ("shot", "gif", "video", "code")  # how a claim best shows the work (T284 §7); "" — nothing in particular


def langs(v) -> dict:
    """Aliases by language; a plain list is the old format — Ukrainian (and whatever else people typed)."""
    v = {"uk": v} if isinstance(v, list) else v or {}
    return {k: list(v.get(k) or []) for k in LANGS}


class Task(Document):
    slug: Annotated[str, Indexed(unique=True)]
    title: str
    description: str = ""  # markdown: what to do + "what I check"
    zone: str
    subzone: str
    kind: str = ""  # zones.KINDS; "" = the subzone's (zones.kind_of)
    icon: str = ""  # emoji of a role, a stat, a field option
    opt: str = ""  # what the card means in a description: a role key, a stat key, `prop:value` of the field
    tags: list[str] = []  # mechanics/entities + "algo" (⭐)
    games: list[str] = []  # game slugs; [] = universal
    coin: str = ""  # wood | tin | bronze | silver | gold | crown
    amount: float = 1
    max_count: int = 1  # 1 = once · N = N times · 0 = unlimited (extra levels etc.)
    tiers: list[list] = []  # price steps [[upto, factor], …] (pricing.py, T291 §13); max_count follows the last upto
    parent: str = ""  # slug of the family card; children are full tasks, one level deep
    slots: list[dict] = []  # claim param specs {key, label, type: int|choice|bool|text, options?, unit?, required?}
    rule: dict = {}  # a rule-card's blank: {when, cond, then} in the vocab's words, args optional
    aliases: dict = {k: [] for k in LANGS}  # other names people search by, per language — data/catalog/aliases.yaml
    proof: str = ""  # PROOFS: a hint to the claim, never a must — data/catalog/proof.yaml
    status: str = "draft"  # draft | active | archived
    core: bool = False  # in the core: claimed at once; the rest of the active cards are «за запитом» (T319) — data/catalog/core.yaml
    order: int = 0  # manual order within subzone
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "tasks"

    @field_validator("aliases", mode="before")
    @classmethod
    def aliases_by_lang(cls, v):
        return langs(v)

    def api(self) -> dict:
        return {
            "id": str(self.id), "slug": self.slug, "title": self.title, "description": self.description,
            "zone": self.zone, "subzone": self.subzone, "kind": kind_of(self), "icon": self.icon, "opt": self.opt,
            "tags": self.tags, "games": self.games, "coin": self.coin, "amount": self.amount, "max_count": self.max_count,
            "tiers": self.tiers, "parent": self.parent, "slots": self.slots, "rule": self.rule, "aliases": self.aliases, "proof": self.proof,
            "status": self.status, "core": self.core, "order": self.order,
        }
