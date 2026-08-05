from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from config import settings
from db import init_db
from routes import auth, games, me, profile, students, tasks, taxonomy


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="Python Labs", lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key=settings.session_secret)
app.include_router(auth.router)
app.include_router(me.router)
app.include_router(profile.router)
app.include_router(students.router)
app.include_router(games.router)
app.include_router(tasks.router)
app.include_router(taxonomy.router)
