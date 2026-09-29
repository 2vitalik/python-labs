from datetime import datetime, timezone

from beanie import Document
from pydantic import Field
from starlette.requests import Request


class Activity(Document):
    """A student's footprint on the site — sign-ins, page views, API calls; edits live in `history` by actor.
    Later: an activity map per student over the semester."""
    user: str  # email
    kind: str  # login · view · api
    path: str = ""  # page for `view`, path?query for `api`
    method: str = ""  # api
    status: int = 0  # api: HTTP status
    ms: int = 0  # api: server time
    ua: str = ""  # user-agent: phone or desktop, every row — a session cookie lives 14 days, so logins alone would miss moves
    ip: str = ""  # whereabouts, every row
    at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "activity"
        indexes = ["user", "at"]


def client(request: Request) -> dict:
    """`ua` + `ip` for a row; behind a proxy the real IP is the first in X-Forwarded-For."""
    ip = request.headers.get("x-forwarded-for", "").split(",")[0].strip() or (request.client.host if request.client else "")
    return {"ua": request.headers.get("user-agent", "")[:200], "ip": ip}
