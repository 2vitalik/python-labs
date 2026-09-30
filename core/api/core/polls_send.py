"""Sending and closing polls (T174): the API process does it with the bot's token; the votes are the bot process's to collect.
A send is written down before Telegram is asked and ends `sent` or `failed` — never lost in between."""
from datetime import datetime, timezone

from aiogram import html
from aiogram.exceptions import TelegramAPIError, TelegramBadRequest
from aiogram.types import InputPollOption

from core.bot import notify
from core.bot.polls import state
from core.config import settings
from core.models.poll import Poll
from core.models.poll_send import PollSend
from core.polls_read import mismatch, votes_of

STALE = 120  # seconds a send may stay `queued` before it counts as stuck: the request that made it has died


def now() -> datetime:
    return datetime.now(timezone.utc)


def head(poll: Poll, what: str) -> str:
    return f'🗳 {what} · <b><a href="{settings.site_url}/polls/{poll.id}">{html.quote(poll.title)}</a></b>'


async def ask(poll: Poll, s: PollSend):
    """Telegram gets the texts as they are: the bot's default HTML would eat a «<3»."""
    return await notify.bot().send_poll(
        s.chat_id, poll.question, [InputPollOption(text=o.label, text_parse_mode=None) for o in poll.options],
        question_parse_mode=None, is_anonymous=False, allows_multiple_answers=poll.multiple,  # anonymous votes never reach the bot
        message_thread_id=s.thread_id, disable_notification=s.silent)


async def send(poll: Poll, s: PollSend) -> PollSend:
    """`s` — a new send, or a failed one tried again: the same row, so a place keeps one line."""
    if s.id:
        await s.set({"status": "queued", "error": "", "where": s.where, "silent": s.silent, "at": now()})
    else:
        await s.insert()
    try:
        if not settings.tg_bot_token:
            raise TelegramAPIError(method=None, message="бот вимкнений: у .env нема TG_BOT_TOKEN")
        m = await ask(poll, s)
    except TelegramAPIError as e:
        await s.set({"status": "failed", "error": e.message})
        await notify.send("poll", "\n".join([head(poll, "Не надіслав"), f"📍 {html.quote(s.where)}", f"❌ {html.quote(e.message)}"]))
        return s
    await s.set({"status": "sent", "tg_poll_id": m.poll.id, "message_id": m.message_id, "url": m.get_url(include_thread_id=True) or "",
                 "option_ids": [o.persistent_id for o in m.poll.options], "sent_at": now()})
    if poll.status == "draft":
        await poll.set({"status": "open", "sent_at": now()})
    return s


def stuck(s: PollSend) -> bool:
    return s.status == "failed" or s.status == "queued" and (now() - s.at.replace(tzinfo=timezone.utc)).total_seconds() > STALE


async def close(poll: Poll) -> None:
    """Stops the poll in every chat; Telegram answers with its final count, which our votes are checked against."""
    sends = await PollSend.find(PollSend.poll == poll.id).to_list()
    for s in sends:
        if s.status != "sent":
            continue
        try:
            final = {"state": state(await notify.bot().stop_poll(s.chat_id, s.message_id))} if settings.tg_bot_token else {}
        except TelegramBadRequest as e:  # the message was deleted or the poll stopped already: nothing is left to close
            final = {"error": f"Telegram: {e.message}"}
        except TelegramAPIError as e:  # network, flood: stays open, closing again may help
            await s.set({"error": f"Не закрив: {e.message}"})
            continue
        await s.set({"status": "closed", "closed_at": now(), "error": ""} | final)
    if poll.status != "closed":
        await poll.set({"status": "closed", "closed_at": now()})
    votes = await votes_of(sends)
    off = [(s, d) for s in sends if s.status == "closed" and (d := mismatch(s, votes))]
    if off:
        lines = [f"⚠️ 📍 {html.quote(s.where)}: Telegram нарахував {d['telegram']}, у нас {d['ours']}" for s, d in off]
        await notify.send("poll", "\n".join([head(poll, "Закрито"), *lines, "☝️ Частина голосів не дійшла — мабуть, бот довго не працював"]))
