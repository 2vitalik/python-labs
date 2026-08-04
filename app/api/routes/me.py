import secrets

from fastapi import APIRouter, Depends

from config import settings
from deps import current_user
from models.user import Status, User

router = APIRouter()


@router.get("/api/me")
async def me(user: User | None = Depends(current_user)):
    if not user:
        return None
    data = user.api()
    if user.status != Status.pending and settings.tg_bot_name:
        if not user.tg_token:
            user.tg_token = secrets.token_urlsafe(16)
            await user.save()
        data["tg_link"] = f"https://t.me/{settings.tg_bot_name}?start={user.tg_token}"
    return data
