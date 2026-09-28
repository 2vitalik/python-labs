"""«Очима студента» (T144): an admin looks at the site as a student. `as` in the session goes before `email`
in current_user, so every page and API call answers as to that student; signing in stays Google's.
Test students can be edited, real ones are read-only (deps.py)."""
from fastapi import APIRouter, Depends, HTTPException, Request

from deps import admin_user, real_user
from models.user import Status, User
from routes.me import me_data

router = APIRouter(prefix="/api/me/as")


@router.post("/{nick}")
async def start(nick: str, request: Request, admin: User = Depends(admin_user)):
    user = await User.by_nick(nick)
    if not user or user.status == Status.admin:
        raise HTTPException(404)
    request.session["as"] = user.email
    return await me_data(user, link=user.test) | {"viewing": True}


@router.delete("")
async def stop(request: Request, user: User | None = Depends(real_user)):
    request.session.pop("as", None)
    return await me_data(user) | {"viewing": False} if user else None
