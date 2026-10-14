"""Zoom as the site sees it (T221): a Server-to-Server OAuth token, the runs of a recurring meeting, who was in one and
for how long, the cloud recording's files. Nothing here knows about lessons — core/attendance.py and routes/attendance.py do."""
from datetime import datetime, timedelta, timezone
from urllib.parse import quote

import httpx
from fastapi import HTTPException

from core.config import settings

API = "https://api.zoom.us/v2"
NOT_SET = "Zoom не налаштовано: потрібні ZOOM_ACCOUNT_ID, ZOOM_CLIENT_ID, ZOOM_CLIENT_SECRET у .env сайту"


def path_id(meeting: str) -> str:
    """A UUID that starts with / or holds // must be double-encoded in the path (Zoom's rule); a numeric ID goes as is."""
    return quote(quote(meeting, safe=""), safe="") if "/" in meeting else quote(meeting, safe="")


class Zoom:
    def __init__(self):
        self.token, self.until = "", datetime.min.replace(tzinfo=timezone.utc)

    @property
    def ready(self) -> bool:
        return bool(settings.zoom_account_id and settings.zoom_client_id and settings.zoom_client_secret)

    async def auth(self) -> str:
        """account_credentials → a bearer token for an hour; no refresh token, just ask again."""
        if self.token and datetime.now(timezone.utc) < self.until:
            return self.token
        async with httpx.AsyncClient(timeout=20) as c:
            r = await c.post("https://zoom.us/oauth/token", data={"grant_type": "account_credentials", "account_id": settings.zoom_account_id},
                             auth=(settings.zoom_client_id, settings.zoom_client_secret))
        if r.status_code != 200:
            raise HTTPException(502, f"Zoom не дав токен: {r.status_code} · {r.text[:200]}")
        d = r.json()
        self.token, self.until = d["access_token"], datetime.now(timezone.utc) + timedelta(seconds=d.get("expires_in", 3600) - 60)
        return self.token

    async def get(self, path: str, **params) -> dict:
        if not self.ready:
            raise HTTPException(503, NOT_SET)
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.get(f"{API}{path}", params=params, headers={"Authorization": f"Bearer {await self.auth()}"})
        if r.status_code != 200:
            said = r.json().get("message", "") if r.headers.get("content-type", "").startswith("application/json") else ""
            raise HTTPException(502, f"Zoom {path.split('?')[0]}: {r.status_code} · {said or r.text[:200]}")
        return r.json()

    async def instances(self, meeting_id: str) -> list[dict]:
        """Every past run of a meeting: {uuid, start_time}."""
        return (await self.get(f"/past_meetings/{path_id(meeting_id)}/instances")).get("meetings", [])

    async def details(self, meeting: str) -> dict:
        """{uuid, topic, start_time, end_time, duration (minutes), participants_count}; a numeric ID means its last run."""
        return await self.get(f"/past_meetings/{path_id(meeting)}")

    async def participants(self, uuid: str) -> list[dict]:
        """Every joined-left segment: {name, user_email, join_time, leave_time, duration (seconds)} — a person may have several."""
        rows, token = [], ""
        while True:
            d = await self.get(f"/past_meetings/{path_id(uuid)}/participants", page_size=300, **({"next_page_token": token} if token else {}))
            rows += d.get("participants", [])
            token = d.get("next_page_token", "")
            if not token:
                return rows

    async def recordings(self, uuid: str) -> dict:
        """The cloud recording: share_url, download_access_token and recording_files [{file_type: MP4|M4A|TRANSCRIPT|CHAT|SUMMARY…, download_url}]."""
        return await self.get(f"/meetings/{path_id(uuid)}/recordings", include_fields="download_access_token")

    async def download(self, url: str, token: str = "") -> bytes:
        async with httpx.AsyncClient(timeout=120, follow_redirects=True) as c:
            r = await c.get(url, headers={"Authorization": f"Bearer {token or await self.auth()}"})
        if r.status_code != 200:
            raise HTTPException(502, f"Zoom не віддав файл: {r.status_code}")
        return r.content
