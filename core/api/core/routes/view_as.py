"""«Очима студента» (T144): an admin looks at the site as a student. `as` in the session goes before `email`
in current_user, so every page and API call answers as to that student; signing in stays Google's.
Test students can be edited, real ones are read-only (deps.py). `POST /api/me/as` without a nick (T357) — the site's
test student, made up on the first click."""
from fastapi import APIRouter, Depends, HTTPException, Request

from core.deps import admin_user, real_user
from core.models.history import record_new
from core.models.user import Status, User
from core.routes.me import me_data

router = APIRouter(prefix="/api/me/as")


async def view(request: Request, user: User) -> dict:
    request.session["as"] = user.email
    return await me_data(user, link=user.test) | {"viewing": True}


async def test_student(admin: User) -> User:
    user = await User.find({"test": True, "status": {"$ne": "admin"}}).sort("_id").first_or_none()
    if not user:
        user = User(email=f"test.student@{admin.email.partition('@')[2]}", last_name="Тестовий", first_name="Студент",
                    status=Status.student, test=True)
        await user.insert()
        await record_new(user, actor=admin.email)
    return user


@router.post("")
async def start_test(request: Request, admin: User = Depends(admin_user)):
    return await view(request, await test_student(admin))


@router.post("/{nick}")
async def start(nick: str, request: Request, admin: User = Depends(admin_user)):
    user = await User.by_nick(nick)
    if not user or user.status == Status.admin:
        raise HTTPException(404)
    return await view(request, user)


@router.delete("")
async def stop(request: Request, user: User | None = Depends(real_user)):
    request.session.pop("as", None)
    return await me_data(user) | {"viewing": False} if user else None
