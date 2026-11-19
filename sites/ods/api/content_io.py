"""Lectures and labs: md on disk (sites/ods/data, outside git) → Mongo of this machine; to a site through its API —
bin/content (T357). What the disk holds is content_disk.py: pages go to the guide (`lec05`, `lab3`, `lab3-guide`,
`labs-grading`, `old-lab2`), their pictures and files to `media`, what stands where among the labs' pages to `lab_pages`.
Run from sites/ods/api: ~/.venvs/python-labs/bin/python content_io.py"""
import asyncio
from pathlib import Path

from content_disk import lab_pages, lectures, media, mime, old_labs, parse, row
from core.models.guide import Guide, save
from core.models.history import record_new
from db import init_db
from models.lab_page import LabPage
from models.media import Media


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
    m.type, m.data = mime(file), data
    await m.save()
    return True


async def main():
    await init_db()
    pages, kept, labs = {"new": 0, "updated": 0, "": 0}, 0, lab_pages()
    for p in lectures() + labs + old_labs():
        title, body, pics = parse(p["slug"], p["file"])
        pages[await put_page(p["slug"], title, body)] += 1
        for path, file in media(p, pics).items():
            kept += await put_media(path, file)
    await LabPage.delete_all()  # the list is the disk's: a page gone from it leaves the site's rows, its text stays in the guide
    if labs:
        await LabPage.insert_many([LabPage(**row(p)) for p in labs])
    print(f"ods: сторінок нових {pages['new']} · оновлено {pages['updated']} · без змін {pages['']} · картинок і файлів записано {kept}"
          f" · сторінок лаб у переліку {len(labs)}")


if __name__ == "__main__":
    asyncio.run(main())
