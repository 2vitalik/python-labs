from datetime import datetime, timezone

from beanie import Document
from pydantic import Field
from pymongo import IndexModel

from core.models.history import when

DATES = ("created_at", "updated_at", "archived_at", "opened_at", "used_at")


class View(Document):
    """A saved look at the table (T240, T315): the columns, filters, sort and grouping as the URL carries them, under a name,
    with its versions, where it came from, its folder and how much it is used."""
    slug: str
    title: str
    emoji: str = ""
    about: str = ""  # what the view is for, one line
    folder: str = ""
    tags: list[str] = []
    etalon: bool = False  # ⭐ a good start for a new view
    pinned: bool = True  # on the tabs of /table
    query: dict = {}  # cols · group · sort · lab · f.<column> — what /table?… holds
    version: int = 0  # the current one of its ViewVersion; 0 — a view from before T316, core.views gives it its 1
    parent: str = ""  # the view it was made from, at its version
    parent_version: int = 0
    order: int = 0
    by: str = ""  # "" — the site's own (views_seed.py)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = None
    archived_at: datetime | None = None
    opens: int = 0
    opened_at: datetime | None = None
    uses: int = 0  # opened and worked with (T315 §9)
    used_at: datetime | None = None
    seconds: int = 0

    class Settings:
        name = "views"
        indexes = [IndexModel([("slug", 1)], unique=True)]

    def api(self) -> dict:
        out = self.model_dump(exclude={"id", "revision_id"})
        return out | {k: when(out[k]) for k in DATES} | {"by": self.by.split("@")[0]}


class ViewVersion(Document):
    """A view as it was saved: a new one on every save, but the same person's quick re-saves amend the last (core/views.py)."""
    view: str  # slug
    n: int
    title: str
    emoji: str = ""
    query: dict = {}
    name: str = ""
    note: str = ""
    star: bool = False
    by: str = ""
    at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "view_versions"
        indexes = [IndexModel([("view", 1), ("n", 1)], unique=True)]

    def api(self) -> dict:
        return self.model_dump(exclude={"id", "revision_id"}) | {"by": self.by.split("@")[0], "at": when(self.at)}
