from fastapi import Depends, HTTPException, Request

from models.user import Status, User


async def current_user(request: Request) -> User | None:
    email = request.session.get("email")
    return await User.find_one(User.email == email) if email else None


async def active_user(user: User | None = Depends(current_user)) -> User:
    return allow(user, user and user.status != Status.pending)


async def admin_user(user: User | None = Depends(current_user)) -> User:
    return allow(user, user and user.status == Status.admin)


def allow(user: User | None, ok) -> User:
    if not user:
        raise HTTPException(401)  # guest: the SPA sends them to /login and back
    if not ok:
        raise HTTPException(403)
    return user
