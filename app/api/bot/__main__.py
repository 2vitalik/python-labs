"""Telegram bot on the same Mongo + models as the API. Run from app/api: uv run python -m bot"""
import asyncio
import logging
import sys

from aiogram import Dispatcher

from bot import digest, errors, here, start
from bot.notify import bot
from config import settings
from db import init_db


async def main():
    logging.basicConfig(level=logging.INFO)
    await init_db()
    dp = Dispatcher()
    dp.errors.register(errors.bot_handler)
    dp.include_router(here.router)  # before start: its fallback would swallow /here in private chats
    dp.include_router(start.router)
    daily = asyncio.create_task(digest.loop())
    logging.info("polling as @%s", (await bot().get_me()).username)
    try:
        await dp.start_polling(bot())
    finally:
        daily.cancel()


if not settings.tg_bot_token:
    sys.exit("TG_BOT_TOKEN is empty: put the BotFather token into app/api/.env")
asyncio.run(main())
