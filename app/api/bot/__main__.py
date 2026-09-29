"""Run from app/api: uv run python -m bot"""
from core.bot.run import run
from db import init_db

run(init_db)
