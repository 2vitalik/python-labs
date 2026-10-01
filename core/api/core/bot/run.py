"""Telegram bot on the same Mongo + models as the API. A site starts it from its `bot/__main__.py`: run(init_db)."""
import asyncio
import logging
import subprocess
import sys

from aiogram import Dispatcher, html
from aiogram.types import BotCommand, BotCommandScopeAllChatAdministrators

from core.bot import chats, digest, errors, here, log, notes, notify, polls, spot, start
from core.bot.notify import bot
from core.config import settings


def build() -> Dispatcher:
    dp = Dispatcher()
    dp.errors.register(errors.bot_handler)
    for observer in (dp.message, dp.business_message, dp.guest_message):
        observer.outer_middleware(log.incoming)
    dp.message.outer_middleware(chats.seen)  # the places polls can go to
    dp.my_chat_member.outer_middleware(chats.joined)
    dp.include_router(here.router)  # admin commands before start: its fallback would swallow them in private chats
    dp.include_router(notes.router)
    dp.include_router(spot.router)
    dp.include_router(start.router)
    dp.include_router(polls.router)  # a handler is what makes aiogram ask Telegram for `poll` and `poll_answer` at all
    dp.include_router(log.router)  # edits and deletions: nobody else handles them
    return dp


def commit() -> str:
    """The deployed commit, if the bot runs from a git checkout."""
    try:
        return subprocess.run(["git", "log", "-1", "--format=%h %s"], capture_output=True, text=True, timeout=5).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


async def started(username: str) -> None:
    """«Deploy went through» for the admins; failing to say so must not stop the bot."""
    lines = [f"🚀 Бот запустився · @{username}"] + ([f"🔖 {html.quote(c)}"] if (c := commit()) else [])
    try:
        await notify.send("start", "\n".join(lines))
    except Exception:  # noqa: BLE001
        logging.exception("start alert not sent")


async def main(init_db):
    logging.basicConfig(level=logging.INFO)
    await init_db()
    dp = build()
    commands = notes.COMMANDS | spot.COMMANDS
    await bot().set_my_commands([BotCommand(command=c, description=d, is_ephemeral=c in ("hide", "poll")) for c, d in commands.items()],
                                scope=BotCommandScopeAllChatAdministrators())  # ephemeral: only the sender and the bot see it
    daily = asyncio.create_task(digest.loop())
    me = await bot().get_me()
    logging.info("polling as @%s · updates: %s", me.username, ", ".join(dp.resolve_used_update_types()))
    await started(me.username)
    try:
        await dp.start_polling(bot())
    finally:
        daily.cancel()


def run(init_db):
    """`init_db` — the site's: the platform's documents and its own."""
    if not settings.tg_bot_token:
        sys.exit("TG_BOT_TOKEN is empty: put the BotFather token into .env")
    asyncio.run(main(init_db))
