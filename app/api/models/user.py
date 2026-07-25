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
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "users"
