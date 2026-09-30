"""Votes (T174): every `poll_answer` → `votes`, every `poll` state → its send. The raw update goes to a file first:
once a handler has run, Telegram moves on and never gives the update again — the file is the copy for `polls_replay`."""
import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from aiogram import Router
from aiogram.types import Poll as TgPoll
from aiogram.types import PollAnswer, Update
from pymongo.errors import DuplicateKeyError

from core.bot.log import dump, email
from core.models.poll import Poll
from core.models.poll_send import PollSend
from core.models.vote import Vote

router = Router()
LOG = Path("logs/poll_updates.jsonl")  # in the site's folder, where the bot is started
logger = logging.getLogger(__name__)


def keep(update: Update) -> None:
    """The copy on disk; if it fails, the vote still goes to Mongo."""
    try:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps(dump(update), ensure_ascii=False) + "\n")
    except OSError:
        logger.exception("poll update not kept on disk")


def state(poll: TgPoll) -> dict:
    """Telegram's own count: how many vote now and for what."""
    return {"total": poll.total_voter_count, "counts": [o.voter_count for o in poll.options], "is_closed": poll.is_closed,
            "at": datetime.now(timezone.utc).isoformat()}


async def record_answer(answer: PollAnswer, update_id: int) -> bool:
    """False — the update is in already: Telegram delivered it twice, or a replay met it."""
    send = await PollSend.find_one(PollSend.tg_poll_id == answer.poll_id)
    poll = await Poll.get(send.poll) if send else None
    who = answer.user
    try:
        await Vote(update_id=update_id, tg_poll_id=answer.poll_id, poll=poll.id if poll else None, tg_id=who.id if who else None,
                   username=(who.username if who else answer.voter_chat and answer.voter_chat.title) or "",
                   user=await email(who.id) if who else "", option_ids=answer.option_ids,
                   text=poll.answer(answer.option_ids) if poll else "", raw=dump(answer)).insert()
    except DuplicateKeyError:
        return False
    return True


async def record_state(poll: TgPoll) -> None:
    send = await PollSend.find_one(PollSend.tg_poll_id == poll.id)
    if not send:
        return  # not ours: it stays on disk only
    fields = {"state": state(poll)}
    if poll.is_closed and send.status == "sent":
        fields |= {"status": "closed", "closed_at": datetime.now(timezone.utc)}
    await send.set(fields)


@router.poll_answer()
async def answered(answer: PollAnswer, event_update: Update):
    keep(event_update)
    await record_answer(answer, event_update.update_id)


@router.poll()
async def counted(poll: TgPoll, event_update: Update):
    """Comes after every vote in a poll the bot sent — and when it is closed."""
    keep(event_update)
    await record_state(poll)
