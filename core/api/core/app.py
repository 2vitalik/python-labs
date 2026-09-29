from contextlib import asynccontextmanager
from time import perf_counter

from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware

from core.bot import errors
from core.config import settings
from core.db import init_db
from core.guide_io import seed
from core.models.activity import Activity, client
from core.routes import activity, auth, front_errors, guide, health, me, profile, students, view_as

ROUTERS = [health.router, auth.router, me.router, view_as.router, profile.router, students.router, guide.router, activity.router,
           front_errors.router]
QUIET = {("GET", "/api/me"), ("POST", "/api/me/view")}  # session probe and page views: they have their own rows
SILENT = ("/api/auth/", "/api/uploads/", "/api/activity")  # the activity page polls, its own calls would flood what it shows


async def footprint(request: Request, call_next):
    """Every API call of a signed-in user → `activity` kind=api (T139): what they did inside a page, not just that they opened it."""
    t = perf_counter()
    status = 500  # a crash gets here as an exception, not as a response
    try:
        response = await call_next(request)
        status = response.status_code
        return response
    finally:
        path, method = request.url.path, request.method
        email = request.session.get("email") or getattr(request.state, "agent", "")
        if email and path.startswith("/api/") and not path.startswith(SILENT) and (method, path) not in QUIET:
            await Activity(user=email, kind="api", method=method, path=path + (f"?{request.url.query}" if request.url.query else ""),
                           status=status, ms=int((perf_counter() - t) * 1000), **client(request)).insert()


def create_app(routers=(), models=()) -> FastAPI:
    """The platform plus the site's own routers and documents."""
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await init_db(models)
        await seed()  # guide pages from the site's files on the first run
        yield

    app = FastAPI(title=settings.site_name, lifespan=lifespan)
    app.add_exception_handler(Exception, errors.api_handler)
    app.middleware("http")(footprint)
    # added last = outermost: the session is set before footprint()
    app.add_middleware(SessionMiddleware, secret_key=settings.session_secret, session_cookie=settings.session_cookie)
    for router in (*ROUTERS, *routers):
        app.include_router(router)
    return app
