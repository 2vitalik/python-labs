import secrets

from datetime import datetime, timezone

from fastapi import APIRouter, BackgroundTasks, Depends, Request
from pydantic import BaseModel

from bot import alerts
from config import settings
from deps import active_user, current_user
from models.activity import Activity, client
from models.history import record
from models.user import Status, User

router = APIRouter()


async def me_data(user: User) -> dict:
    data = user.api()
    if user.status != Status.pending and settings.tg_bot_name:
        if not user.tg_token:
            user.tg_token = secrets.token_urlsafe(16)
            await user.save()
        data["tg_link"] = f"https://t.me/{settings.tg_bot_name}?start={user.tg_token}"
    return data


@router.get("/api/me")
async def me(user: User | None = Depends(current_user)):
    return await me_data(user) if user else None


class ViewIn(BaseModel):
    path: str


@router.post("/api/me/view", status_code=204)
async def view(data: ViewIn, request: Request, user: User = Depends(current_user)):
    """The SPA reports every page it opens for a signed-in user (App.vue); guests are not tracked."""
    if not user:
        return
    await Activity(user=user.email, kind="view", path=data.path[:200], **client(request)).insert()
    user.last_seen_at = datetime.now(timezone.utc)
    await user.save()


@router.delete("/api/me/telegram")
async def unlink_telegram(tasks: BackgroundTasks, user: User = Depends(active_user)):
    user.tg_token = ""  # rotate: me_data mints a new one, so the old link is dead
    user.tg_linked_at = None
    changes = await record(user, {"tg_chat_id": None, "tg_username": ""}, actor=user.email)
    tasks.add_task(alerts.profile, user, changes)
    return await me_data(user)
