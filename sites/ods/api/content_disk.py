"""The ods texts on disk (sites/ods/data, outside git): which pages there are, what each says, which files go with it.
No database and no platform here: content_io.py (straight into Mongo) and bin/content (through the API, T357) both read
the disk by this. Teacher versions (`*.hid.*`) stay on disk."""
import json
import mimetypes
import os
import re
import sys
from pathlib import Path

DATA = Path(os.environ.get("ODS_DATA") or Path(__file__).resolve().parent.parent / "data")  # ../data of this folder
IMG = re.compile(r"(\]\(|src=\")img/([^)\"\s]+)")  # ![…](img/x.png) or <img src="img/x.png">
NEW = (("task", "", "Умова"), ("guide", "guide", "Розбір"), ("marimo", "marimo", "marimo"))  # labN-<file>.md → the part, its word
TEMPLATES = (("jupyter.ipynb", "Шаблон для Jupyter і Colab — без картки"), ("marimo.py", "Шаблон для marimo — без картки"))


def found(path: Path) -> bool:
    """A file named but missing on disk: a line to stderr, and on without it."""
    if not path.exists():
        print(f"нема файла: {path}", file=sys.stderr)
        return False
    return True


def glob(pattern: str) -> list[Path]:
    return [p for p in sorted(DATA.glob(pattern)) if ".hid." not in p.name]


def lectures() -> list[dict]:
    return [{"slug": p.stem, "file": p} for p in glob("lectures/lec*/lec*.md")]


def new_labs() -> list[dict]:
    """labs/new/labN: the task is the lab's own page and hands out the templates; the walk-through and the marimo note are its parts."""
    out = []
    for folder in glob("labs/new/lab[0-9]*"):
        n = int(folder.name[3:])
        files = [{"name": f"lab{n}-{ext}", "title": title, "path": folder / f"lab{n}-{ext}"} for ext, title in TEMPLATES
                 if (folder / f"lab{n}-{ext}").exists()]
        for order, (file, part, nav) in enumerate(NEW):
            if (path := folder / f"lab{n}-{file}.md").exists():
                out.append({"slug": f"lab{n}-{part}".rstrip("-"), "file": path, "kind": "lab", "lab": n, "part": part, "nav": nav, "order": order,
                            "files": [] if part else files})
    return out


def site_labs() -> list[dict]:
    """labs/site/pages.json — the layout written for the site (T355)."""
    root = DATA / "labs/site"
    if not (root / "pages.json").exists():
        return []
    out = []
    for p in json.loads((root / "pages.json").read_text()):
        if not found(root / p["file"]):
            continue
        common = p["kind"] == "common"
        part = p["slug"].removeprefix("labs-") if common else p["slug"].partition("-")[2]
        out.append({"slug": p["slug"], "file": root / p["file"], "kind": p["kind"], "lab": None if common else p["lab"], "part": part,
                    "nav": p.get("nav") or p["title"], "order": p.get("order", 0),
                    "files": [f | {"path": root / f["path"]} for f in p.get("files", []) if found(root / f["path"])]})
    return out


def lab_pages() -> list[dict]:
    """A lab the site's layout describes takes all its pages from there, the others — from labs/new."""
    site = site_labs()
    told = {p["lab"] for p in site}
    return [p for p in new_labs() if p["lab"] not in told] + site


def old_labs() -> list[dict]:
    """The labs of past years — the teacher's archive (`guide_staff`), not a row among the labs' pages."""
    return [{"slug": f"old-{p.parent.name}", "file": p} for p in glob("labs/old/lab[0-9]*/lab[0-9]*-student.md")]


def parse(slug: str, path: Path) -> tuple[str, str, list[str]]:
    """(title, body, pictures); the italic line under the title is the converter's note, not the text."""
    title, _, body = path.read_text().partition("\n")
    body = re.sub(r"\A\s*\*[^\n]*\*\n", "", body).strip()
    pics = [p for _, p in IMG.findall(body) if ".hid." not in p]
    return title.lstrip("# ").strip(), IMG.sub(rf"\1/api/media/{slug}/\2", body), pics


def media(p: dict, pics: list[str]) -> dict[str, Path]:
    """What goes to `media` with the page: its pictures `<slug>/x.png` and the files it hands out `files/<slug>/<name>`."""
    out = {f"{p['slug']}/{name}": p["file"].parent / "img" / name for name in pics}
    out |= {f"files/{p['slug']}/{f['name']}": f["path"] for f in p.get("files", [])}
    return {path: file for path, file in out.items() if found(file)}


def mime(file: Path) -> str:
    return mimetypes.guess_type(file.name)[0] or "application/octet-stream"


def row(p: dict) -> dict:
    """The page's line in the list of the labs' pages (`lab_pages`)."""
    files = [{"name": f["name"], "title": f.get("title", ""), "url": f"/api/media/files/{p['slug']}/{f['name']}"} for f in p.get("files", [])]
    return {"slug": p["slug"], "kind": p["kind"], "lab": p["lab"], "part": p["part"], "nav": p["nav"], "order": p["order"], "files": files}
