"""How open each lab is to students (T368): `hidden` — as if it were not there · `telegram` — read it, take the card, hand the
notebook to the teacher in Telegram · `site` — hand it in here. A lab starts as `LAB_GATES` of site.env says (lab 1 first;
a lab not named there — `site`); the teacher's click on /labs (`lab_gates`) goes over that. The teacher and agents see every lab."""
import re

from fastapi import Depends, HTTPException
from pydantic_settings import BaseSettings

from core.config import settings
from core.deps import active_user
from core.models.user import Status, User
from core.routes import guide
from models.lab_gate import LabGate

STATES = ("hidden", "telegram", "site")
PAGE = re.compile(r"lab(\d+)(-|$)")  # lab4 · lab4-case1 — not labs-grading, not old-lab4
BY_TELEGRAM = "Лабу {lab} здаємо викладачеві в Telegram — на сайті здача ще закрита"


class Start(BaseSettings):
    lab_gates: str = ""
    model_config = {"env_file": ("site.env", ".env"), "extra": "ignore"}


START = [w.strip() for w in Start().lab_gates.split(",")]


def start(lab: int) -> str:
    word = START[lab - 1] if 0 < lab <= len(START) else ""
    return word if word in STATES else "site"


async def gates() -> dict[int, str]:
    own = {g.lab: g.state for g in await LabGate.find_all().to_list()}
    return {n: own.get(n) or start(n) for n in range(1, settings.labs + 1)}


async def gate(lab: int) -> str:
    return (await gates()).get(lab, "site")


def teacher(user: User | None) -> bool:
    return bool(user) and user.status == Status.admin


async def here(lab: int, user: User) -> bool:
    """The lab is handed in on the site by this person: the teacher tries any lab, a student — one that takes files here."""
    return teacher(user) or await gate(lab) == "site"


async def opened(lab: int, user: User = Depends(active_user)) -> User:
    """«Моя лаба» of a lab: a hidden one is not there for a student."""
    if not teacher(user) and await gate(lab) == "hidden":
        raise HTTPException(404, f"Лаби {lab} ще нема")
    return user


async def taking(lab: int, user: User = Depends(opened)) -> User:
    if not await here(lab, user):
        raise HTTPException(409, BY_TELEGRAM.format(lab=lab))
    return user


async def hidden_pages():
    """slug → bool for the guide: the pages of a hidden lab are the teacher's."""
    states = await gates()

    def hidden(slug: str) -> bool:
        m = PAGE.match(slug)
        return bool(m) and states.get(int(m[1])) == "hidden"

    return hidden


guide.STAFF.append(hidden_pages)
