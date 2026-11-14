from datetime import datetime, timezone
from typing import Annotated

from beanie import Document, Indexed, PydanticObjectId
from pydantic import Field

CLAIM_STATUSES = ("claimed", "accepted", "returned")  # заявлено · зараховано · повернуто (the teacher's word)


class Game(Document):
    """The student's game (the catalog base game is models/base_game.py)."""
    owner: Annotated[str, Indexed(unique=True)]  # user email; one game per student
    title: str
    base_game: str = ""  # catalog game slug; "" = custom base
    base_custom: str = ""  # free-text base when not from the catalog
    description: str = ""  # markdown
    phases: list[str] = []  # the order of one tick / turn: ввід → гравець → вороги → … (T257)
    moments: str = ""  # «Як це грається»: scenarios of frames, markdown like a base game's examples (T276, moments.py)
    poured: float = 0  # an etalon (owner `<slug>@etalon`): the mtime of the template it was poured from — routes/etalon.py
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "student_games"

    def api(self) -> dict:
        return {
            "id": str(self.id), "owner": self.owner, "title": self.title,
            "base_game": self.base_game, "base_custom": self.base_custom,
            "description": self.description, "phases": self.phases, "moments": self.moments, "created_at": self.created_at.isoformat(),
        }


class Part(Document):
    """A piece of the game's description: the field (one), an entity, a window, a menu, a level — the anchor of claims and screenshots."""
    game: Annotated[PydanticObjectId, Indexed()]
    kind: str  # field | entity | window | menu | level (vocab.PART_KINDS)
    title: str
    task: str = ""  # window type: catalog card of kind window
    role: str = ""  # entity: the `opt` of a role card
    icon: str = ""  # entity: its own emoji; "" = the role's
    description: str = ""
    screenshots: list[str] = []  # file names under uploads/<game-id>/
    window: str = ""  # menu: id of the host window part
    items: list[dict] = []  # menu: {title, window: part id, task: slug, note}
    props: dict = {}  # field: values by vocab.FIELD keys; level: vocab.LEVEL + the field's it overrides
    stats: list[dict] = []  # entity, level: {key, label, value, unit} — HP, життя, швидкість…
    states: list[str] = []  # entity: its states; transitions are rules with set_state
    order: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "game_parts"

    def api(self) -> dict:
        return {
            "id": str(self.id), "game": str(self.game), "kind": self.kind, "title": self.title,
            "task": self.task, "role": self.role, "icon": self.icon, "description": self.description,
            "screenshots": self.screenshots, "window": self.window, "items": self.items,
            "props": self.props, "stats": self.stats, "states": self.states,
            "order": self.order, "created_at": self.created_at.isoformat(),
        }


class Claim(Document):
    game: Annotated[PydanticObjectId, Indexed()]
    task: str  # catalog task slug
    part: str = ""  # Part id; "" with no rule = game-level claim, or a draft waiting for its anchor
    rule: str = ""  # Rule id: a card of kind rule anchors on the rule that describes it
    auto: bool = False  # made by the description itself (a window's type, a role, a stat, a field option): auto_claims.py
    params: dict = {}  # values for the card's slots {key: value}
    note: str = ""
    link: str = ""  # GitHub link (commit-pin normalization — later phase)
    shots: list[str] = []  # the proof (T284 §7): up to three pictures, file names under uploads/<game-id>/
    status: str = "claimed"  # CLAIM_STATUSES; the teacher sets accepted / returned
    verdict: str = ""  # the teacher's line with the status
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "claims"

    def api(self) -> dict:
        return {
            "id": str(self.id), "game": str(self.game), "task": self.task, "part": self.part, "rule": self.rule,
            "auto": self.auto, "params": self.params, "note": self.note, "link": self.link, "shots": self.shots,
            "status": self.status, "verdict": self.verdict,
            "created_at": self.created_at.isoformat(),
        }
