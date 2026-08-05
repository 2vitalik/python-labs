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
    coin: str = ""  # wood | tin | bronze | silver | gold
    amount: float = 1
    max_count: int = 1  # 1 = once · N = N times · 0 = unlimited (extra levels etc.)
    variants: list[dict] = []  # family: [{slug, title, coin, amount}]
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
            "variants": self.variants, "status": self.status, "order": self.order,
        }
