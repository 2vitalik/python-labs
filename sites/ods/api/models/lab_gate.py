from datetime import datetime, timezone
from typing import Annotated

from beanie import Document, Indexed
from pydantic import Field


class LabGate(Document):
    """The teacher's word on how open a lab is to students (T368) — over where the lab starts (lab_gates.py)."""
    lab: Annotated[int, Indexed(unique=True)]
    state: str  # hidden · telegram · site
    by: str = ""
    at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "lab_gates"
