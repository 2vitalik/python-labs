import re

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from deps import active_user
from models.history import record
from models.user import User

GITHUB_RE = re.compile(r"https://github\.com/[\w.-]+/[\w.-]+/?")

router = APIRouter()


class ProfileIn(BaseModel):
    last_name: str = ""
    first_name: str = ""
    patronymic: str = ""
    github: str = ""
    tg_username: str = ""


def clean(data: BaseModel) -> dict:
    fields = {k: v.strip() if isinstance(v, str) else v for k, v in data.model_dump(mode="json").items()}
    fields["tg_username"] = fields["tg_username"].lstrip("@")
    fields["github"] = fields["github"].rstrip("/")
    if fields["github"] and not GITHUB_RE.fullmatch(fields["github"]):
        raise HTTPException(422, "Очікую посилання виду https://github.com/користувач/репозиторій")
    return fields


@router.put("/api/profile")
async def update_profile(data: ProfileIn, user: User = Depends(active_user)):
    await record(user, clean(data), actor=user.email)
    return user.api()
