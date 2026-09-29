"""Lectures and labs: md on disk (sites/ods/data, outside git) → Mongo. Pages go to the guide (`lec05`, `lab3`),
their pictures to `media`. Teacher versions (`*.hid.*`) stay on disk. Run from sites/ods/api: uv run python content_io.py"""
import asyncio
import mimetypes
import re
from pathlib import Path

from core.models.guide import Guide, save
from core.models.history import record_new
from db import init_db
from models.media import Media

DATA = Path("../data")
IMG = re.compile(r"(\]\(|src=\")img/([^)\"\s]+)")  # ![…](img/x.png) or <img src="img/x.png">


def sources() -> dict[str, Path]:
    lectures = {p.stem: p for p in sorted(DATA.glob("lectures/lec*/lec*.md"))}
    labs = {p.parent.name: p for p in sorted(DATA.glob("labs/lab*/lab*-student.md"))}
    return lectures | labs


def parse(slug: str, path: Path) -> tuple[str, str, list[str]]:
    """(title, body, pictures); the italic line under the title is the converter's note, not the text."""
    title, _, body = path.read_text().partition("\n")
    body = re.sub(r"\A\s*\*[^\n]*\*\n", "", body).strip()
    pics = [p for _, p in IMG.findall(body) if ".hid." not in p]
    return title.lstrip("# ").strip(), IMG.sub(rf"\1/api/media/{slug}/\2", body), pics


async def put_page(slug: str, title: str, body: str) -> str:
    g = await Guide.find_one(Guide.slug == slug)
    if not g:
        await record_new(await Guide(slug=slug, title=title, body=body, updated_by="import").insert(), actor="import")
        return "new"
    return "updated" if await save(g, title, body, actor="import") else ""


async def put_media(path: str, file: Path) -> bool:
    data, m = file.read_bytes(), await Media.find_one(Media.path == path)
    if m and m.data == data:
        return False
    m = m or Media(path=path, type="", data=b"")
    m.type, m.data = mimetypes.guess_type(file.name)[0] or "application/octet-stream", data
    await m.save()
    return True


async def main():
    await init_db()
    pages, pics = {"new": 0, "updated": 0, "": 0}, 0
    for slug, path in sources().items():
        title, body, names = parse(slug, path)
        pages[await put_page(slug, title, body)] += 1
        for name in names:
            pics += await put_media(f"{slug}/{name}", path.parent / "img" / name)
    print(f"ods: сторінок нових {pages['new']} · оновлено {pages['updated']} · без змін {pages['']} · картинок записано {pics}")


if __name__ == "__main__":
    asyncio.run(main())
