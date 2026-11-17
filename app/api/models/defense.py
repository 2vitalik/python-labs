from datetime import datetime, timezone
from typing import Annotated

from beanie import Document, Indexed, PydanticObjectId
from pydantic import Field


def now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)  # the way Mongo gives it back


class Defense(Document):
    """One defense of one student (T327): who, what, when — and what the teacher made of it.
    The impressions and the note are the teacher's own: no route gives them to a student or an agent."""
    student: Annotated[str, Indexed()]  # email
    labs: list[int] = []
    kind: str = "online"  # defense_vocab.KINDS
    started_at: datetime | None = None
    ended_at: datetime | None = None
    facts: dict = {}  # what happened: {key: yes | partly | no}
    rates: dict = {}  # the scales in words: {key: 1…4, a half — between two steps}
    marks: list[str] = []
    note: str = ""
    result: str = ""  # defense_vocab.RESULTS; "" — not said yet
    rank: float = 0  # the place among the defenses of one overall step, higher is better: the ladder
    scale: int = 1  # the wording of the scales these impressions were given by
    link: str = ""  # the recording of the talk
    sent_at: datetime | None = None  # from here on the student sees the remarks and the result
    by: str = ""  # the teacher
    created_at: datetime = Field(default_factory=now)

    class Settings:
        name = "defenses"


class Remark(Document):
    """A remark of a defense (T328): what it is about (tags), what it asks of the student (kind) and where it is on the
    way «given → answered → checked» (state)."""
    defense: Annotated[PydanticObjectId, Indexed()]
    student: Annotated[str, Indexed()]
    text: str  # what the student reads
    raw: str = ""  # as dictated, once the text was cleaned
    tags: list[str] = []  # the first one leads: the group and the colour
    kind: str = "better"  # defense_vocab.REMARK_KINDS
    state: str = "draft"  # draft · open · answered · accepted · returned
    reply: dict = {}  # the student's: {state, note, link, at}
    check: dict = {}  # the teacher's word on it: {state, note, by, at}
    agent: dict = {}  # an agent's opinion on the reply, never the word itself: {state, note, by, at}
    hint: dict = {}  # what a model or an agent proposes: {text, like, by}
    own: list[str] = []  # the fields the teacher set by hand: a proposal leaves them alone
    coin: str = ""  # the reward for the rework (T329); "" — none
    amount: float = 0
    order: int = 0
    created_at: datetime = Field(default_factory=now)  # minus the defense's start — the minute of the recording

    class Settings:
        name = "remarks"
