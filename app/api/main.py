from contextlib import asynccontextmanager
from time import perf_counter

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

import uploads
from bot import errors
from config import settings
from db import init_db
from guide_io import seed
from models.activity import Activity, client
from routes import (auth, games, guide, me, my_claims, my_game, my_parts, my_rules, profile, refs,
                    student_games, students, tasks, taxonomy)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await seed()  # guide pages from data/guide/ on the first run
    yield


app = FastAPI(title="Python Labs", lifespan=lifespan)
app.add_exception_handler(Exception, errors.api_handler)
QUIET = {("GET", "/api/me"), ("POST", "/api/me/view")}  # session probe and page views: they have their own rows


@app.middleware("http")
async def footprint(request: Request, call_next):
    """Every API call of a signed-in user → `activity` kind=api (T139): what they did inside a page, not just that they opened it."""
    t = perf_counter()
    response = await call_next(request)
    path, method = request.url.path, request.method
    email = request.session.get("email")
    if email and path.startswith("/api/") and not path.startswith(("/api/auth/", "/api/uploads/")) and (method, path) not in QUIET:
        await Activity(user=email, kind="api", method=method, path=path + (f"?{request.url.query}" if request.url.query else ""),
                       status=response.status_code, ms=int((perf_counter() - t) * 1000), **client(request)).insert()
    return response


app.add_middleware(SessionMiddleware, secret_key=settings.session_secret)  # added last = outermost: the session is set before footprint()
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
