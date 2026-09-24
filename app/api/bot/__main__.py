"""Telegram bot on the same Mongo + models as the API. Run from app/api: uv run python -m bot"""
import asyncio
import logging
import sys

from aiogram import Dispatcher
from aiogram.types import BotCommand, BotCommandScopeAllChatAdministrators

from bot import digest, errors, here, log, notes, start
from bot.notify import bot
from config import settings
from db import init_db


async def main():
    logging.basicConfig(level=logging.INFO)
    await init_db()
    dp = Dispatcher()
    dp.errors.register(errors.bot_handler)
    for observer in (dp.message, dp.business_message, dp.guest_message):
        observer.outer_middleware(log.incoming)
    dp.include_router(here.router)  # admin commands before start: its fallback would swallow them in private chats
    dp.include_router(notes.router)
    dp.include_router(start.router)
    dp.include_router(log.router)  # edits and deletions: nobody else handles them
    await bot().set_my_commands([BotCommand(command=c, description=d, is_ephemeral=c == "hide") for c, d in notes.COMMANDS.items()],
                                scope=BotCommandScopeAllChatAdministrators())  # ephemeral: only the sender and the bot see it
    daily = asyncio.create_task(digest.loop())
    logging.info("polling as @%s", (await bot().get_me()).username)
    try:
        await dp.start_polling(bot())
    finally:
        daily.cancel()


if not settings.tg_bot_token:
    sys.exit("TG_BOT_TOKEN is empty: put the BotFather token into app/api/.env")
asyncio.run(main())
