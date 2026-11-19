from datetime import datetime, timezone

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field


class Forward(Document):
    """A message the teacher forwarded to the bot from a student's chat (T368 §2.1): who wrote it and when, the words,
    the file kept whole — a notebook becomes a version of «Моя лаба» with the time of the student's message."""
    key: str = ""  # whose talk it is: `tg:<id>`, or `name:<as Telegram shows them>` when the account hides behind forwards; "" — the teacher's line of nobody's talk yet
    tg_id: int | None = None  # the writer; on the teacher's own lines — the teacher
    name: str = ""
    username: str = ""
    mine: bool = False  # the teacher's own line of that talk
    sent_at: datetime  # when it was written: Telegram's date of the original
    got_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    by: str = ""  # the admin who forwarded it
    msg: int = 0  # the forward's message_id in the bot's chat: the order within a burst
    text: str = ""
    file: dict = {}  # {name, size, uid, tg} — Telegram's document: uid is file_unique_id, tg — file_id; {name, link} — a notebook taken by the Colab / Drive link in the text
    kind: str = ""  # ipynb · marimo — a notebook read; "" — none
    sha: str = ""
    raw: bytes = b""  # zlib of the notebook
    lab: int | None = None  # what the notebook is: by its answer line, else by the lab's template; the teacher's word goes over
    vid: str = ""
    line: str = ""
    ok: int | None = None  # the line against the card's key
    total: int | None = None
    why: str = ""  # why there is no notebook here though a file came: too big, not one, Telegram did not give it
    student: str = ""  # email, once known
    how: str = ""  # tg — by the Telegram account · hand — the teacher said
    version: str = ""  # the LabFile it became
    trouble: str = ""  # why it did not: the words for the teacher
    asks: bool = False  # reads as asking for more time; the teacher's click flips it
    skip: bool = False  # set aside by the teacher

    class Settings:
        name = "forwards"
        indexes = ["key", "tg_id", "student", "sent_at"]


class ForwardHead(BaseModel):
    """A forward without the notebook's bytes: the lists never load them."""
    id: PydanticObjectId = Field(alias="_id")
    key: str = ""
    tg_id: int | None = None
    name: str = ""
    username: str = ""
    mine: bool = False
    sent_at: datetime
    got_at: datetime
    by: str = ""
    msg: int = 0
    text: str = ""
    file: dict = {}
    kind: str = ""
    sha: str = ""
    lab: int | None = None
    vid: str = ""
    line: str = ""
    ok: int | None = None
    total: int | None = None
    why: str = ""
    student: str = ""
    how: str = ""
    version: str = ""
    trouble: str = ""
    asks: bool = False
    skip: bool = False
