from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

import uploads
from bot import errors
from config import settings
from db import init_db
from guide_io import seed
from routes import (auth, games, guide, me, my_claims, my_game, my_parts, my_rules, profile, refs,
                    student_games, students, tasks, taxonomy)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await seed()  # guide pages from data/guide/ on the first run
    yield


app = FastAPI(title="Python Labs", lifespan=lifespan)
app.add_exception_handler(Exception, errors.api_handler)
app.add_middleware(SessionMiddleware, secret_key=settings.session_secret)
app.include_router(auth.router)
app.include_router(me.router)
app.include_router(profile.router)
app.include_router(students.router)
app.include_router(student_games.router)
app.include_router(games.router)
app.include_router(tasks.router)
app.include_router(taxonomy.router)
app.include_router(my_game.router)
app.include_router(my_parts.router)
app.include_router(my_claims.router)
app.include_router(my_rules.router)
app.include_router(refs.router)
app.include_router(guide.router)
uploads.ROOT.mkdir(parents=True, exist_ok=True)
app.mount("/api/uploads", StaticFiles(directory=uploads.ROOT), name="uploads")
