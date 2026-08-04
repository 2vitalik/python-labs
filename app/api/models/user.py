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
    email: Annotated[str, Indexed(unique=True)]
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
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "users"

    def api(self) -> dict:
        return {
            "id": str(self.id), "email": self.email, "name": self.name, "picture": self.picture,
            "status": self.status, "last_name": self.last_name, "first_name": self.first_name,
            "patronymic": self.patronymic, "group": self.group, "github": self.github,
            "tg_username": self.tg_username, "tg_linked": self.tg_chat_id is not None,
        }
