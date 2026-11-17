"""Alerts about defenses (T326), kind `defense`: remarks sent, a student answered them all — and a line to the student's
own chat when there is something to do."""
import logging

from aiogram import html
from aiogram.exceptions import TelegramAPIError

import defense_vocab as V
from core.bot import notify
from core.bot.alerts import event
from core.config import settings
from core.models.user import User
from models.defense import Defense, Remark

logger = logging.getLogger(__name__)
PAGE = "/my/remarks"


async def tell(owner: User, rows: list[str]) -> None:
    """To the student, when the bot is linked. A dev site keeps quiet: its links lead nowhere, its people are real."""
    local = "127.0.0.1" in settings.site_url or "localhost" in settings.site_url
    if local or owner.test or not owner.tg_chat_id or not settings.tg_bot_token:
        return
    try:
        await notify.bot().send_message(owner.tg_chat_id, "\n".join(rows + [f'👉 <a href="{settings.site_url}{PAGE}">відкрити зауваження</a>']))
    except TelegramAPIError as e:
        logger.warning("defense line to %s failed: %s", owner.email, e.message)


async def left(r: Remark, states: tuple) -> int:
    return await Remark.find({"defense": r.defense, "state": {"$in": list(states)}, "kind": {"$ne": "tip"}}).count()


async def sent(owner: User, d: Defense, n: int) -> None:
    result = " ".join(V.RESULTS[d.result]) if d.result else "результат ще не сказано"
    await notify.send("defense", event(0, "Захист", owner, [f"📨 надіслано зауважень: {n}", f"🏁 {result}"]), owner.email)
    await tell(owner, [f"🛡 Захист: {result}", f"📝 зауважень: {n} — на кожне потрібна відповідь"] if n else [f"🛡 Захист: {result}"])


async def replied(owner: User, r: Remark) -> None:
    """One alert when nothing waits for the student any more — not a line per answer."""
    if not await left(r, ("open", "returned")):
        n = await Remark.find({"defense": r.defense, "state": "answered"}).count()
        await notify.send("defense", event(1, "Захист", owner, [f"💬 відповів на всі зауваження — чекають перевірки: {n}"]), owner.email)


async def checked(owner: User, r: Remark) -> None:
    if r.state == "returned":
        await tell(owner, [f"↩️ Зауваження повернуто: {html.quote(r.text[:120])}", f"💬 {html.quote(r.check.get('note', ''))}"])
    elif not await left(r, ("open", "answered", "returned")):
        await tell(owner, ["✅ Усі зауваження захисту прийнято"])
