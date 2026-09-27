from datetime import datetime, timezone

from beanie import Document
from pydantic import Field


class Error(Document):
    """An unhandled failure, whole (T149): the alert carries a line of it, the traceback and the request stay here."""
    source: str  # api · bot · front
    title: str  # "RuntimeError: boom"; front — the JS message
    trace: str = ""  # the full traceback; front — the JS stack
    user: str = ""  # email; "" = a guest or a stranger
    method: str = ""  # api
    path: str = ""  # api: path?query · front: the page · bot: the update type
    where: str = ""  # front: the component and what it was doing, in Vue's words
    ua: str = ""
    ip: str = ""
    at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "errors"
        indexes = ["source", "user", "at"]
