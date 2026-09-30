"""Telegram bot on the same Mongo + models as the API. A site starts it from its `bot/__main__.py`: run(init_db)."""
import asyncio
import logging
import sys

from aiogram import Dispatcher
from aiogram.types import BotCommand, BotCommandScopeAllChatAdministrators

from core.bot import chats, digest, errors, here, log, notes, polls, spot, start
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


async def main(init_db):
    logging.basicConfig(level=logging.INFO)
    await init_db()
    dp = build()
    commands = notes.COMMANDS | spot.COMMANDS
    await bot().set_my_commands([BotCommand(command=c, description=d, is_ephemeral=c in ("hide", "poll")) for c, d in commands.items()],
                                scope=BotCommandScopeAllChatAdministrators())  # ephemeral: only the sender and the bot see it
    daily = asyncio.create_task(digest.loop())
    logging.info("polling as @%s · updates: %s", (await bot().get_me()).username, ", ".join(dp.resolve_used_update_types()))
    try:
        await dp.start_polling(bot())
    finally:
        daily.cancel()


def run(init_db):
    """`init_db` — the site's: the platform's documents and its own."""
    if not settings.tg_bot_token:
        sys.exit("TG_BOT_TOKEN is empty: put the BotFather token into .env")
    asyncio.run(main(init_db))
