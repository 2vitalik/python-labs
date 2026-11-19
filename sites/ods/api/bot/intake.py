"""Messages the teacher forwards to the bot from students' chats (T368 §2.2) → `forwards`: ✍ on each, one summary after
QUIET seconds of silence. A burst lives in memory only: after a restart an unfinished one just gives no summary."""
import asyncio
import logging
from dataclasses import dataclass, field

from aiogram import F, Router
from aiogram.exceptions import TelegramAPIError
from aiogram.types import Message, ReactionTypeEmoji
from beanie.operators import In

import intake_apply
import intake_match
from bot import intake_say
from bot.intake_take import take
from core.bot import notify
from core.bot.notes import as_admin
from core.models.user import User
from models.forward import Forward, ForwardHead

router = Router()
router.message.filter(F.chat.type == "private", F.forward_origin, as_admin)
QUIET = 3
logger = logging.getLogger(__name__)


@dataclass
class Burst:
    ids: list = field(default_factory=list)
    again: int = 0
    other: int = 0  # from a group or a channel: not taken
    busy: int = 0  # handlers still at work: the silence starts when the last one is done
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)  # one at a time: a repeat within a burst is seen as one
    timer: asyncio.Task | None = None


BURSTS: dict[int, Burst] = {}  # the bot's chat with a teacher → the burst being forwarded


async def heads(ids: list) -> list[ForwardHead]:
    return await Forward.find(In(Forward.id, ids)).sort("sent_at", "msg").project(ForwardHead).to_list()


async def close(ids: list, again: int = 0, other: int = 0) -> str:
    """The burst is over: the teacher's lines join their talk, whatever can become a version does; the summary."""
    await intake_match.attach(await heads(ids))
    await intake_apply.settle()
    rows = await heads(ids)
    users = {u.email: u for u in await User.find(In(User.email, list({r.student for r in rows if r.student}))).to_list()}
    return intake_say.summary(rows, users, again, other, await intake_match.clues())


async def later(chat: int, b: Burst) -> None:
    await asyncio.sleep(QUIET)
    if BURSTS.get(chat) is b:
        del BURSTS[chat]
    try:
        for page in intake_say.pages(await close(b.ids, b.again, b.other)):
            await notify.bot().send_message(chat, page)
    except Exception:  # noqa: BLE001 — a task's error has nobody to go to
        logger.exception("intake summary not sent")


async def react(message: Message) -> None:
    try:
        await notify.bot().set_message_reaction(message.chat.id, message.message_id, [ReactionTypeEmoji(emoji="✍")])
    except TelegramAPIError:
        pass


@router.message()
async def forwarded(message: Message, admin: User):
    b = BURSTS.setdefault(message.chat.id, Burst())
    b.busy += 1
    if b.timer:
        b.timer.cancel()
    try:
        async with b.lock:
            if message.forward_origin.type not in ("user", "hidden_user"):
                b.other += 1
                return
            if f := await take(message, admin):
                b.ids.append(f.id)
            else:
                b.again += 1
            await react(message)
    finally:
        b.busy -= 1
        if not b.busy:
            b.timer = asyncio.create_task(later(message.chat.id, b))
