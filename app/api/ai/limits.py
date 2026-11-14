"""Who may ask and how much (T289 §7, T291 §14): the switch, the key, a student's requests per day and per semester, one
request at a time, the month's budget for everyone. Days, months and semesters are Kyiv's."""
from contextlib import asynccontextmanager
from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import HTTPException

import options
from core.config import settings
from core.models.user import Status, User
from models.draft import Draft

TZ = ZoneInfo("Europe/Kyiv")
STEPS = (50, 80, 100)  # % of the month's budget: an alert once each
busy: set[str] = set()  # who waits for an answer now — one process serves the API


def since(span: str, now: datetime | None = None) -> datetime:
    """The start of this day, month or semester (autumn from September, spring from February)."""
    now = (now or datetime.now(TZ)).astimezone(TZ)
    day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    if span == "day":
        return day
    if span == "month":
        return day.replace(day=1)
    autumn = now.month >= 9 or now.month == 1
    return day.replace(year=now.year - (now.month == 1), month=9 if autumn else 2, day=1)


async def used(email: str, span: str) -> int:
    """Requests that got an answer: a failed one is not counted."""
    return await Draft.find(Draft.owner == email, Draft.error == "", Draft.created_at >= since(span)).count()


async def spent() -> float:
    return await Draft.find(Draft.created_at >= since("month")).sum(Draft.cost) or 0


def allowed(user: User) -> bool:
    return settings.ai_describe == "students" or (settings.ai_describe == "admin" and options.is_admin(user))


async def why(user: User) -> str:
    """"" — on; off — not for this user (no panel at all); nokey; budget — the month's ceiling is reached."""
    if not allowed(user):
        return "off"
    if not settings.anthropic_api_key:
        return "nokey"
    return "budget" if await spent() >= settings.ai_budget_usd else ""


async def state(user: User) -> dict:
    """GET /api/my/game/ai without the drafts; the admin's limits are none — null."""
    off = await why(user)

    async def left(n: int, span: str) -> int | None:
        return None if user.status == Status.admin else max(0, n - await used(user.email, span))
    return {"mode": "off" if off else "on", "why": off, "left_today": await left(settings.ai_per_day, "day"),
            "left_total": await left(settings.ai_total, "semester"), "per_day": settings.ai_per_day, "total": settings.ai_total,
            "max_chars": settings.ai_max_chars}


async def check(user: User, text: str) -> None:
    off = await why(user)
    if off == "off":
        raise HTTPException(403, "ШІ-помічник поки вимкнено.")
    if off:
        raise HTTPException(503, "ШІ-помічник ще не підключено" if off == "nokey" else "На цей місяць бюджет ШІ-помічника вичерпано")
    if not text:
        raise HTTPException(422, "Напиши, що є в твоїй грі.")
    if len(text) > settings.ai_max_chars:
        raise HTTPException(422, f"Задовго: {len(text)} знаків, можна до {settings.ai_max_chars} — розбий на частини.")
    if user.status == Status.admin:
        return
    for span, n, word in (("day", settings.ai_per_day, "сьогодні"), ("semester", settings.ai_total, "семестр")):
        if await used(user.email, span) >= n:
            raise HTTPException(429, f"На {word} запити вичерпано — лишилось 0 з {n}")


@asynccontextmanager
async def alone(email: str):
    if email in busy:
        raise HTTPException(409, "Попередній текст ще розбирається")
    busy.add(email)
    try:
        yield
    finally:
        busy.discard(email)


def crossed(before: float, after: float) -> list[int]:
    """The budget's steps this request stepped over."""
    budget = settings.ai_budget_usd
    return [p for p in STEPS if budget and before < budget * p / 100 <= after]
