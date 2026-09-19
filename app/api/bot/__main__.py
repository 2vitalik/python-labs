"""Telegram bot on the same Mongo + models as the API. Run from app/api: uv run python -m bot"""
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from bot.start import router
from config import settings
from db import init_db


async def main():
    logging.basicConfig(level=logging.INFO)
    await init_db()
    bot = Bot(settings.tg_bot_token, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()
    dp.include_router(router)
    logging.info("polling as @%s", (await bot.get_me()).username)
    await dp.start_polling(bot)


if not settings.tg_bot_token:
    sys.exit("TG_BOT_TOKEN is empty: put the BotFather token into app/api/.env")
asyncio.run(main())
