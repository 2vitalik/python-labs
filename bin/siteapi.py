"""What bin/guide and bin/catalog share (T153, T155): the sites and the agent's tokens from .site/.env, calls to the API,
the working copy .site/<target>/<kind>/<slug>.md and the git snapshot in data/."""
import json
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / ".site"
SNAP = "prod"  # the site whose texts and cards git keeps in data/; also where the scripts go without -t


def target(name: str) -> tuple[str, str]:
    env = HOME / ".env"
    lines = env.read_text().splitlines() if env.exists() else []
    keys = dict(l.split("=", 1) for l in lines if "=" in l and not l.startswith("#"))
    url, token = (keys.get(f"{name.upper()}_{k}", "").strip() for k in ("URL", "TOKEN"))
    if not url or not token:
        sys.exit(f"нема {name.upper()}_URL або {name.upper()}_TOKEN у {env}")
    return url.rstrip("/"), token


def call(to: str, method: str, path: str, data: dict | None = None):
    url, token = target(to)
    request = Request(f"{url}/api{path}", method=method, data=json.dumps(data).encode() if data else None,
                      headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    try:
        with urlopen(request) as response:
            return json.load(response)
    except HTTPError as e:
        sys.exit(f"{method} {path}: {e.code} · {e.read().decode()[:300]}")
    except URLError as e:
        sys.exit(f"{url} не відповідає · {e.reason}")


def file(to: str, kind: str, slug: str) -> Path:
    return HOME / to / kind / f"{slug}.md"


def taken(to: str, kind: str, slug: str) -> dict | None:
    """The document as it came from the site: what a push compares the file and the site with."""
    path = HOME / to / ".taken" / kind / f"{slug}.json"
    return json.loads(path.read_text()) if path.exists() else None


def keep(to: str, kind: str, doc: dict, text: str) -> Path:
    path = file(to, kind, doc["slug"])
    for where, what in ((HOME / to / ".taken" / kind / f"{doc['slug']}.json", json.dumps(doc, ensure_ascii=False)), (path, text)):
        where.parent.mkdir(parents=True, exist_ok=True)
        where.write_text(what)
    return path


def pull(to: str, kind: str, doc: dict, text) -> Path:
    """`text` — how the document looks as a file. Edits that were never sent are set aside, not written over."""
    was, path = taken(to, kind, doc["slug"]), file(to, kind, doc["slug"])
    if was and path.exists() and path.read_text() not in (text(was), text(doc)):
        path.rename(path.with_suffix(".mine.md"))
        print(f"{kind}/{doc['slug']}: невідправлені правки → {doc['slug']}.mine.md")
    return keep(to, kind, doc, text(doc))


def snap(folder: Path, files: dict[str, str]):
    folder.mkdir(parents=True, exist_ok=True)
    for name, text in files.items():
        (folder / name).write_text(text)
    print(f"знімок: {len(files)} файлів → {folder}")
