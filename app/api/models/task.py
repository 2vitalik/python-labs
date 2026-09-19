from datetime import datetime, timezone
from typing import Annotated

from beanie import Document, Indexed
from pydantic import Field


class Task(Document):
    slug: Annotated[str, Indexed(unique=True)]
    title: str
    description: str = ""  # markdown: what to do + "what I check"
    zone: str
    subzone: str
    tags: list[str] = []  # mechanics/entities + "algo" (⭐)
    games: list[str] = []  # game slugs; [] = universal
    coin: str = ""  # wood | tin | bronze | silver | gold | crown
    amount: float = 1
    max_count: int = 1  # 1 = once · N = N times · 0 = unlimited (extra levels etc.)
    parent: str = ""  # slug of the family card; children are full tasks, one level deep
    slots: list[dict] = []  # claim param specs {key, label, type: int|choice|bool|text, options?, unit?, required?}
    status: str = "draft"  # draft | active | archived
    order: int = 0  # manual order within subzone
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "tasks"

    def api(self) -> dict:
        return {
            "id": str(self.id), "slug": self.slug, "title": self.title, "description": self.description,
            "zone": self.zone, "subzone": self.subzone, "tags": self.tags, "games": self.games,
            "coin": self.coin, "amount": self.amount, "max_count": self.max_count,
            "parent": self.parent, "slots": self.slots, "status": self.status, "order": self.order,
        }
