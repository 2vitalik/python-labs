import re
from datetime import datetime, timezone
from enum import Enum
from typing import Annotated

from beanie import Document, Indexed
from pydantic import Field


class Status(str, Enum):
    pending = "pending"
    student = "student"
    admin = "admin"


class User(Document):
    email: Annotated[str, Indexed(unique=True)]  # nick = local part, unique (single domain)
    name: str = ""
    picture: str = ""
    status: Status = Status.pending
    last_name: str = ""
    first_name: str = ""
    patronymic: str = ""
    group: str = ""
    github: str = ""
    tg_username: str = ""
    tg_token: str = ""
    tg_chat_id: int | None = None
    seen_at: datetime | None = None  # last sign-in; None = never been on the site
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "users"

    @property
    def nick(self) -> str:
        return self.email.split("@")[0]

    @classmethod
    async def by_nick(cls, nick: str) -> "User | None":
        return await cls.find_one({"email": {"$regex": f"^{re.escape(nick)}@"}})

    def api(self) -> dict:
        return {
            "id": str(self.id), "email": self.email, "nick": self.nick,
            "name": self.name, "picture": self.picture,
            "status": self.status, "last_name": self.last_name, "first_name": self.first_name,
            "patronymic": self.patronymic, "group": self.group, "github": self.github,
            "tg_username": self.tg_username, "tg_linked": self.tg_chat_id is not None,
        }
