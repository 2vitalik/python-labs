"""Run from sites/ods/api: uv run python -m bot"""
from bot import intake
from core.bot import run
from db import init_db

run.ROUTERS.append(intake.router)  # the teacher's forwards of students' messages (T368)
run.run(init_db)
