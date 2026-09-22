"""Smoke: guide pages in Mongo — seed from files, admin PUT with rev/409, history with notes, «Що змінилось» draft
and publish, export/import round trip in a temp dir, ideas in refs. Run from app/api:
DB_NAME=python_labs_smoke uv run python tests/smoke_guide.py"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.getcwd())
from pymongo import MongoClient  # noqa: E402

DB = os.environ["DB_NAME"]
assert DB.endswith("_smoke"), "refuse to run on a non-smoke DB"
mongo = MongoClient()
mongo.drop_database(DB)

from fastapi.testclient import TestClient  # noqa: E402

import main  # noqa: E402
from config import settings  # noqa: E402

results = []
IO = ("import asyncio, pathlib, sys, guide_io\nfrom db import init_db\nguide_io.ROOT = pathlib.Path(sys.argv[1])\n"
      "async def go():\n    await init_db()\n    await getattr(guide_io, sys.argv[2])()\nasyncio.run(go())")


def check(name, cond, extra=""):
    results.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def login(c, email, status):
    settings.fake_user_email = email
    c.get("/api/auth/dev-login")
    mongo[DB].users.update_one({"email": email}, {"$set": {"status": status}})


def io(root, cmd):
    return subprocess.run(["uv", "run", "python", "-c", IO, str(root), cmd], capture_output=True, text=True)


with TestClient(main.app) as c:
    pages = c.get("/api/guide").json()
    check("seed: pages from data/guide, no draft", len(pages) >= 10 and all(p["slug"] != "changes-draft" for p in pages))
    check("seed logged", mongo[DB].history.count_documents({"coll": "guide", "actor": "seed"}) == len(pages))
    g = c.get("/api/guide/game").json()
    check("page: title/body/rev 0", g["title"].endswith("Ігри") and g["rev"] == 0 and "## " in g["body"])
    edit = {"title": g["title"], "body": g["body"].replace("## Своя гра", "## Своя гра 2"), "rev": 0,
            "note": "уточнив своє", "section": "Своя гра"}
    check("guest: draft 404, PUT 401",
          c.get("/api/guide/changes-draft").status_code == 404 and c.put("/api/guide/game", json=edit).status_code == 401)
    login(c, "stud@nure.ua", "student")
    check("student: PUT 403, history 403",
          c.put("/api/guide/game", json=edit).status_code == 403 and c.get("/api/guide/history").status_code == 403)

    login(c, "admin@nure.ua", "admin")
    r = c.put("/api/guide/game", json=edit)
    check("PUT: rev 1 + new body", r.status_code == 200 and r.json()["rev"] == 1 and "Своя гра 2" in r.json()["body"], r.text)
    check("stale rev → 409", c.put("/api/guide/game", json=edit).status_code == 409)
    r = c.put("/api/guide/game", json=edit | {"rev": 1, "note": "нічого"})
    check("same text: no new rev, no draft line", r.json()["rev"] == 1 and "нічого" not in c.get("/api/guide/changes-draft").json()["body"])
    d = c.get("/api/guide/changes-draft").json()
    check("draft line from note", d["body"].startswith("- **") and "Ігри › Своя гра: уточнив своє" in d["body"], d["body"])
    h = c.get("/api/guide/history?slug=game").json()
    check("history: note, old → new, actor",
          h[0]["note"] == "уточнив своє" and h[0]["old"] == g["body"] and h[0]["new"] == edit["body"] and h[0]["actor"] == "admin")
    check("history all: seeds + the edit + the draft line", len(c.get("/api/guide/history").json()) == len(pages) + 2)

    line = d["body"].split("\n")[0]
    r = c.post("/api/guide/changes/publish", json={"line": line})
    body = r.json()["body"]
    check("publish: line above earlier entries", r.status_code == 200 and body.index(line) < body.index("- **2026-09-20**"), r.text)
    check("publish: draft emptied", c.get("/api/guide/changes-draft").json()["body"] == "")

    root = Path(tempfile.mkdtemp())
    r = io(root, "export")
    check("export: files with the edit, no draft", r.returncode == 0 and "Своя гра 2" in (root / "game.md").read_text()
          and not (root / "changes-draft.md").exists(), r.stderr)
    (root / "lab1.md").write_text("# Лаба 1 нова\n\nтекст\n")
    r = io(root, "import_")
    lab1 = c.get("/api/guide/lab1").json()
    check("import: file → page, rev 1, actor import", r.returncode == 0 and lab1["title"] == "Лаба 1 нова"
          and lab1["rev"] == 1 and lab1["updated_by"] == "import", r.stderr)

    r = c.post("/api/refs", json={"note": "ідея без лінка"})
    check("idea: kind idea, no url", r.status_code == 200 and r.json()["kind"] == "idea" and r.json()["url"] == "", r.text)
    check("empty idea → 422", c.post("/api/refs", json={"note": " "}).status_code == 422)
    check("bad url → 422", c.post("/api/refs", json={"url": "просто текст"}).status_code == 422)
    link = c.post("/api/refs", json={"url": "https://x.com", "note": "лінк"}).json()["id"]
    r = c.post("/api/refs", json={"note": "під лінком", "parent": link}).json()
    check("idea under a find", r["parent"] == link and r["kind"] == "idea")

ok = sum(1 for _, p in results if p)
print(f"\n{ok}/{len(results)} PASS")
sys.exit(0 if ok == len(results) else 1)
