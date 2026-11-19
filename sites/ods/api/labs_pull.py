"""A notebook by the student's Colab or Drive link (T354 §5): Google's hosts only, 15 s, 12 MB.
A file not shared «with anyone with the link» comes back as Google's HTML page — not a notebook."""
import asyncio
import json
import re

import httpx

from models.lab_file import MAX_BYTES

FAIL = "Не вдалося взяти файл за посиланням: відкрий доступ „Усі, хто має посилання“ або завантаж файл сюди"
NOT_GOOGLE = "Посилання не з Google Colab чи Drive — завантаж файл сюди"
IDS = (re.compile(r"colab\.research\.google\.com/drive/([\w-]{10,})"), re.compile(r"drive\.google\.com/file/d/([\w-]{10,})"),
       re.compile(r"drive\.google\.com/open\?(?:[^#]*&)?id=([\w-]{10,})"))
URL = "https://drive.google.com/uc?export=download&id={}"
HOSTS = ("google.com", "googleusercontent.com")
TIMEOUT, HOPS = 15, 5


def drive_id(link: str) -> str | None:
    return next((m[1] for p in IDS if (m := p.search(link or ""))), None)


def google(url: httpx.URL) -> bool:
    return url.scheme == "https" and any(url.host == h or url.host.endswith("." + h) for h in HOSTS)


async def get(url: str) -> bytes:
    """Redirects are followed only within Google; more than 12 MB — refused while reading."""
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        for _ in range(HOPS):
            async with client.stream("GET", url) as r:
                if r.is_redirect:
                    nxt = r.url.join(r.headers.get("location", ""))
                    if not google(nxt):
                        raise ValueError(FAIL)
                    url = str(nxt)
                    continue
                if r.status_code != 200:
                    raise ValueError(FAIL)
                data = bytearray()
                async for chunk in r.aiter_bytes():
                    data += chunk
                    if len(data) > MAX_BYTES:
                        raise ValueError("Файл за посиланням завеликий: ліміт 12 МБ")
                return bytes(data)
    raise ValueError(FAIL)


async def pull(link: str) -> bytes:
    """The .ipynb behind the link; a ValueError speaks to the student."""
    if not (file_id := drive_id(link)):
        raise ValueError(NOT_GOOGLE)
    try:
        async with asyncio.timeout(TIMEOUT):
            data = await get(URL.format(file_id))
    except (httpx.HTTPError, TimeoutError):
        raise ValueError(FAIL) from None
    try:
        nb = json.loads(data)
    except ValueError:
        nb = None
    if not isinstance(nb, dict) or not isinstance(nb.get("cells"), list):
        raise ValueError(FAIL)
    return data
