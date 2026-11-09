from datetime import UTC, datetime
from typing import Annotated

from beanie import Document, Indexed
from pydantic import Field


class LudoGame(Document):
    """A reference game of the ludopedia corpus (data/ludopedia/games/<family>/<slug>.md, T253): the YAML head as fields,
    the body section by section, the entities table / rules / sources parsed. Truth is the file; ludopedia_io.py imports."""
    slug: Annotated[str, Indexed(unique=True)]
    title: str
    headline: str = ""  # the H1 tail: the game in one line
    aka: list[str] = []
    family: str
    also: list[str] = []
    klass: str = ""  # avatar | cursor | figure | puzzle | hybrid
    axes: dict = {}  # field, time, opponent, info, random, goal — EN values of vocab/classes.md
    year: str = ""
    platforms: list[str] = []
    links: list[dict] = []  # {kind, url, best, note}
    stage: str = "v1"
    coverage: int = 0
    mechanics: list[str] = []  # catalog card slugs; `+new` for what the catalog lacks
    proposes: list[str] = []
    author: str = ""
    date: str = ""
    sections: dict = {}  # essence, field, entities, rules, controls, ui, features, variations, course, catalog_map, proposals, sources, uncertain
    entities: list[dict] = []  # {name, role, params, behavior}
    rules: list[dict] = []  # {text, when, cond, then}
    sources: list[dict] = []  # {title, url, note, best}
    path: str = ""
    imported_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    class Settings:
        name = "ludo_games"
        indexes = ["family", "mechanics", "klass"]

    @property
    def best(self) -> str:
        return next((l.get("url", "") for l in self.links if l.get("best")), self.links[0].get("url", "") if self.links else "")

    def brief(self) -> dict:
        """The list row: no texts."""
        return {
            "slug": self.slug, "title": self.title, "headline": self.headline, "aka": self.aka, "family": self.family, "also": self.also,
            "klass": self.klass, "axes": self.axes, "year": self.year, "stage": self.stage, "coverage": self.coverage,
            "mechanics": self.mechanics, "url": self.best, "entities": len(self.entities), "rules": len(self.rules),
        }

    def api(self) -> dict:
        return self.brief() | {
            "platforms": self.platforms, "links": self.links, "proposes": self.proposes, "author": self.author, "date": self.date,
            "sections": self.sections, "entities": self.entities, "rules": self.rules, "sources": self.sources, "path": self.path,
        }
