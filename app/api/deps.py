from fastapi import Depends, HTTPException, Request

from models.user import Status, User


async def current_user(request: Request) -> User | None:
    email = request.session.get("email")
    return await User.find_one(User.email == email) if email else None


async def active_user(user: User | None = Depends(current_user)) -> User:
    if not user or user.status == Status.pending:
        raise HTTPException(403)
    return user


async def admin_user(user: User | None = Depends(current_user)) -> User:
    if not user or user.status != Status.admin:
        raise HTTPException(403)
    return user
