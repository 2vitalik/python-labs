"""Whose talk a forward is (T368 §2.4): for sure — the Telegram account a student linked to the bot (`how = tg`); the teacher's
word (`hand`, routes/intake.py); a guess — the card in their file held on the site, the Telegram nick, the words of the name —
counted while reading, never stored: the teacher confirms it with one click."""
from beanie.operators import In
from pydantic import BaseModel

from core.models.user import User
from core.tg_paste import words
from models.forward import Forward, ForwardHead
from models.lab import LabVariant


class Held(BaseModel):
    lab: int
    vid: str
    student: str


def who(user: User) -> dict:
    """WHO = {nick, name, group}."""
    p = user.person()
    return {"nick": p["nick"], "name": p["name"], "group": p["group"]}


async def clues() -> tuple[list[User], dict]:
    """What a guess goes by: the people it may name (not the teacher, not test ones) and the cards held — (lab, vid) and vid → email."""
    people = await User.find({"status": {"$ne": "admin"}, "test": {"$ne": True}}).to_list()
    cards = await LabVariant.find(LabVariant.student != "").project(Held).to_list()
    return people, {k: c.student for c in cards for k in (c.vid, (c.lab, c.vid))}


async def owner(key: str) -> dict:
    """{student, how} the talk's earlier rows already have: one more forward of a known talk is known too."""
    f = await Forward.find_one(Forward.key == key, Forward.student != "") if key else None
    return {"student": f.student, "how": f.how} if f else {}


async def attach(rows: list[ForwardHead]) -> None:
    """The teacher's own lines of a burst join the talk of the student's line nearest to them in the bot's chat."""
    theirs = [r for r in rows if not r.mine]
    for r in rows:
        if r.mine and not r.key and theirs:
            near = min(theirs, key=lambda t: (abs(t.msg - r.msg), t.msg > r.msg))
            r.key = near.key
            await Forward.find(Forward.id == r.id).update({"$set": {"key": near.key} | await owner(near.key)})


async def by_telegram(user: User | None = None) -> None:
    """Talks nobody owns yet whose writer linked the bot are theirs, the teacher's lines of them too; `user` — only theirs."""
    if user and not user.tg_chat_id:
        return
    q = {"key": {"$regex": "^tg:"}, "student": "", "mine": False} | ({"tg_id": user.tg_chat_id} if user else {})
    for u in await User.find(In(User.tg_chat_id, await Forward.distinct("tg_id", q))).to_list():
        await Forward.find(Forward.key == f"tg:{u.tg_chat_id}", Forward.student == "").update({"$set": {"student": u.email, "how": "tg"}})


def named(said: set[str], people: list[User]) -> User | None:
    """The one person a Telegram name fits best: words in common, the surname counting twice; two at least, no tie."""
    def fit(u: User) -> int:
        return len(said & words(u.last_name, u.first_name, u.name, *u.aliases)) + bool(said & words(u.last_name))
    ranked = sorted(((fit(u), u) for u in people), key=lambda x: -x[0]) + [(0, None)]
    return ranked[0][1] if ranked[0][0] >= 2 and ranked[1][0] < ranked[0][0] else None


def guess(rows: list[ForwardHead], people: list[User], cards: dict) -> dict | None:
    """WHO + {why}: `card` — the card of their newest notebook is held on the site (`cards`: (lab, vid) or vid → email),
    `username` — their Telegram nick is in someone's profile, `name` — the words of their name."""
    theirs = [r for r in rows if not r.mine]
    by_email = {u.email: u for u in people}
    for r in reversed(theirs):
        if r.vid and (u := by_email.get(cards.get((r.lab, r.vid)) or cards.get(r.vid, ""))):
            return who(u) | {"why": "card"}
    nicks = {r.username.lower() for r in theirs if r.username}
    if u := next((u for u in people if u.tg_username and u.tg_username.lower() in nicks), None):
        return who(u) | {"why": "username"}
    if u := named({w for r in theirs for w in words(r.name)}, people):
        return who(u) | {"why": "name"}
    return None
