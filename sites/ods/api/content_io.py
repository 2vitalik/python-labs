"""Lectures and labs: md on disk (sites/ods/data, outside git) → Mongo. Pages go to the guide (`lec05`, `lab3`, `lab3-guide`,
`labs-grading`), their pictures and files to `media`, what stands where among the labs' pages to `lab_pages`.
Teacher versions (`*.hid.*`) stay on disk. Run from sites/ods/api: ~/.venvs/python-labs/bin/python content_io.py"""
import asyncio
import json
import mimetypes
import os
import re
from pathlib import Path

from core.models.guide import Guide, save
from core.models.history import record_new
from db import init_db
from models.lab_page import LabPage
from models.media import Media

DATA = Path(os.environ.get("ODS_DATA", "../data"))
IMG = re.compile(r"(\]\(|src=\")img/([^)\"\s]+)")  # ![…](img/x.png) or <img src="img/x.png">
NEW = (("task", "", "Умова"), ("guide", "guide", "Розбір"), ("marimo", "marimo", "marimo"))  # labN-<file>.md → the part, its word


def lectures() -> list[dict]:
    return [{"slug": p.stem, "file": p} for p in sorted(DATA.glob("lectures/lec*/lec*.md"))]


def new_labs() -> list[dict]:
    """labs/new/labN: the task is the lab's own page, the walk-through and the marimo note are its parts."""
    out = []
    for folder in sorted(DATA.glob("labs/new/lab[0-9]*")):
        n = int(folder.name[3:])
        for order, (file, part, nav) in enumerate(NEW):
            if (path := folder / f"lab{n}-{file}.md").exists():
                out.append({"slug": f"lab{n}-{part}".rstrip("-"), "file": path, "kind": "lab", "lab": n, "part": part, "nav": nav, "order": order})
    return out


def site_labs() -> list[dict]:
    """labs/site/pages.json — the layout written for the site (T355)."""
    root = DATA / "labs/site"
    if not (root / "pages.json").exists():
        return []
    out = []
    for p in json.loads((root / "pages.json").read_text()):
        common = p["kind"] == "common"
        part = p["slug"].removeprefix("labs-") if common else p["slug"].partition("-")[2]
        out.append({"slug": p["slug"], "file": root / p["file"], "kind": p["kind"], "lab": None if common else p["lab"], "part": part,
                    "nav": p.get("nav") or p["title"], "order": p.get("order", 0),
                    "files": [f | {"path": root / f["path"]} for f in p.get("files", [])]})
    return out


def lab_pages() -> list[dict]:
    """A lab the site's layout describes takes all its pages from there, the others — from labs/new."""
    site = site_labs()
    told = {p["lab"] for p in site}
    return [p for p in new_labs() if p["lab"] not in told] + site


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
    if not file.exists():
        print(f"нема файла: {file}")
        return False
    data, m = file.read_bytes(), await Media.find_one(Media.path == path)
    if m and m.data == data:
        return False
    m = m or Media(path=path, type="", data=b"")
    m.type, m.data = mimetypes.guess_type(file.name)[0] or "application/octet-stream", data
    await m.save()
    return True


def listed(p: dict) -> LabPage:
    files = [{"name": f["name"], "title": f.get("title", ""), "url": f"/api/media/files/{p['slug']}/{f['name']}"} for f in p.get("files", [])]
    return LabPage(slug=p["slug"], kind=p["kind"], lab=p["lab"], part=p["part"], nav=p["nav"], order=p["order"], files=files)


async def main():
    await init_db()
    pages, kept, labs = {"new": 0, "updated": 0, "": 0}, 0, lab_pages()
    for p in lectures() + labs:
        title, body, names = parse(p["slug"], p["file"])
        pages[await put_page(p["slug"], title, body)] += 1
        for name in names:
            kept += await put_media(f"{p['slug']}/{name}", p["file"].parent / "img" / name)
        for f in p.get("files", []):
            kept += await put_media(f"files/{p['slug']}/{f['name']}", f["path"])
    await LabPage.delete_all()  # the list is the disk's: a page gone from it leaves the site's rows, its text stays in the guide
    if labs:
        await LabPage.insert_many([listed(p) for p in labs])
    print(f"ods: сторінок нових {pages['new']} · оновлено {pages['updated']} · без змін {pages['']} · картинок і файлів записано {kept}"
          f" · сторінок лаб у переліку {len(labs)}")


if __name__ == "__main__":
    asyncio.run(main())
