from secrets import compare_digest

from fastapi import Depends, HTTPException, Request

from core.config import settings
from core.models.user import Status, User


async def real_user(request: Request) -> User | None:
    """Who has signed in — the footprint is theirs even while they look as a student."""
    email = request.session.get("email")
    return await User.find_one(User.email == email) if email else None


async def current_user(request: Request) -> User | None:
    """`as` in the session — «Очима студента» (routes/view_as.py): the admin gets that student's pages and rights.
    A test student can be edited, a real one is for looking only."""
    viewed = request.session.get("as")
    email = viewed or request.session.get("email")
    user = await User.find_one(User.email == email) if email else None
    if viewed and user and not user.test and request.method != "GET":
        raise HTTPException(403, "Лише перегляд: ти дивишся очима студента")
    return user


async def active_user(user: User | None = Depends(current_user)) -> User:
    return allow(user, user and user.status != Status.pending)


async def admin_user(user: User | None = Depends(current_user)) -> User:
    return allow(user, user and user.status == Status.admin)


def agent(request: Request) -> User | None:
    """An AI agent by `Authorization: Bearer <token>` (T153): no row in `users`, the email is its name in `history`."""
    kind, _, token = request.headers.get("authorization", "").partition(" ")
    sent = token.strip().encode() if kind.lower() == "bearer" else b""
    email = next((e for t, e in settings.agents.items() if compare_digest(t.encode(), sent)), None)
    if not email:
        return None
    request.state.agent = email  # for footprint() in app.py: the session is empty
    return User(email=email, name=email.split("@")[0], status=Status.admin)


async def editor_user(request: Request, user: User | None = Depends(current_user)) -> User:
    """Who edits the guide and the site's own texts: admins and AI agents. The token opens only the routes that ask for this."""
    return agent(request) or allow(user, user and user.status == Status.admin)


async def viewer(request: Request, user: User | None = Depends(current_user)) -> User | None:
    """Whom the site's open lists answer: an agent sees what an admin does."""
    return agent(request) or user


def allow(user: User | None, ok) -> User:
    if not user:
        raise HTTPException(401)  # guest: the SPA sends them to /login and back
    if not ok:
        raise HTTPException(403)
    return user
