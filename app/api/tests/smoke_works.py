"""Smoke: works/objects/claims/screenshots flow on a scratch DB. Run from app/api:
DB_NAME=python_labs_smoke UPLOADS_DIR=... uv run python <this file>"""
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, os.getcwd())
from pymongo import MongoClient  # noqa: E402

DB = os.environ["DB_NAME"]
assert DB.endswith("_smoke"), "refuse to run on a non-smoke DB"
mongo = MongoClient()
mongo.drop_database(DB)
subprocess.run(["uv", "run", "python", "catalog_io.py", "import"], check=True, capture_output=True)

from fastapi.testclient import TestClient  # noqa: E402

import main  # noqa: E402
from config import settings  # noqa: E402

PNG = b"\x89PNG\r\n\x1a\n" + b"0" * 100
results = []


def check(name, cond, extra=""):
    results.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def login(c, email, status):
    settings.fake_user_email = email
    c.get("/api/auth/dev-login")
    mongo[DB].users.update_one({"email": email}, {"$set": {"status": status}})


with TestClient(main.app) as c:
    check("guest: /works → 403", c.get("/api/works").status_code == 403)

    login(c, "stud@nure.ua", "pending")
    check("pending: POST /works → 403", c.post("/api/works", json={"title": "x", "base_custom": "y"}).status_code == 403)
    mongo[DB].users.update_one({"email": "stud@nure.ua"}, {"$set": {"status": "student"}})

    check("no work yet: GET /my → null", c.get("/api/works/my").json() is None)
    r = c.post("/api/works", json={"title": "Танчики Пілот", "base_game": "battle-city"})
    check("create work", r.status_code == 200, r.text)
    wid = r.json()["id"]
    check("second work → 409", c.post("/api/works", json={"title": "Друга", "base_custom": "x"}).status_code == 409)
    check("bad base → 422", c.put("/api/works/my", json={"title": "Т", "base_game": "no-such"}).status_code == 422)
    check("no base → 422", c.put("/api/works/my", json={"title": "Т"}).status_code == 422)

    r = c.post("/api/works/my/objects", json={"kind": "window", "task": "main-menu", "title": "Головне меню"})
    check("window create", r.status_code == 200, r.text)
    win = r.json()["id"]
    check("draft type for student → 422",
          c.post("/api/works/my/objects", json={"kind": "window", "task": "settings-window", "title": "Н"}).status_code == 422)
    check("non-window card as type → 422",
          c.post("/api/works/my/objects", json={"kind": "window", "task": "player-death", "title": "Х"}).status_code == 422)
    r = c.get(f"/api/works/{wid}")
    check("auto-claim of window type", [cl["task"] for cl in r.json()["claims"]] == ["main-menu"])
    check("claims enriched with card info", r.json()["tasks"]["main-menu"]["coin"] == "tin")

    r = c.post("/api/works/my/objects", json={"kind": "menu", "title": "Меню старту", "window": win,
                                              "items": [{"title": "Нова гра", "window": win},
                                                        {"title": "Гучність", "task": "sound-volume"},
                                                        {"title": "  "}]})
    check("menu create (items cleaned)", r.status_code == 200 and len(r.json()["items"]) == 2, r.text)
    menu = r.json()["id"]
    check("bad item target → 422",
          c.post("/api/works/my/objects", json={"kind": "menu", "title": "М",
                                                "items": [{"title": "x", "window": "000000000000000000000000"}]}).status_code == 422)

    r = c.post(f"/api/works/my/objects/{win}/screenshot", files={"file": ("s.png", PNG, "image/png")})
    check("screenshot upload", r.status_code == 200 and len(r.json()["screenshots"]) == 1, r.text)
    shot = r.json()["screenshots"][0]
    check("file on disk", (Path(os.environ["UPLOADS_DIR"]) / wid / shot).is_file())
    check("static serve", c.get(f"/api/uploads/{wid}/{shot}").status_code == 200)
    check("bad type → 422",
          c.post(f"/api/works/my/objects/{win}/screenshot", files={"file": ("s.txt", b"x", "text/plain")}).status_code == 422)
    check("oversize → 422",
          c.post(f"/api/works/my/objects/{win}/screenshot",
                 files={"file": ("s.png", b"0" * (8 * 2**20 + 1), "image/png")}).status_code == 422)
    check("gallery cover set", c.get("/api/works").json()[0]["cover"].endswith(shot))

    r = c.post("/api/works/my/claims", json={"task": "player-death"})
    check("game-level claim", r.status_code == 200, r.text)
    check("duplicate claim → 409", c.post("/api/works/my/claims", json={"task": "player-death"}).status_code == 409)
    check("draft card claim for student → 422",
          c.post("/api/works/my/claims", json={"task": "sound-volume"}).status_code == 422)
    r = c.post("/api/works/my/claims", json={"task": "status-panel", "object": win})
    check("object claim", r.status_code == 200, r.text)
    check("claim on alien object → 422",
          c.post("/api/works/my/claims", json={"task": "time-out", "object": "abc"}).status_code == 422)

    r = c.delete(f"/api/works/my/objects/{win}")
    check("window delete", r.status_code == 200)
    r = c.get(f"/api/works/{wid}").json()
    check("cascade: window claims gone", {cl["task"] for cl in r["claims"]} == {"player-death"})
    m = next(o for o in r["objects"] if o["id"] == menu)
    check("cascade: menu host stripped", m["window"] == "")
    check("cascade: item target stripped", m["items"][0]["window"] == "")
    check("cascade: file removed", not (Path(os.environ["UPLOADS_DIR"]) / wid / shot).is_file())

    login(c, "admin@nure.ua", "admin")
    r = c.post("/api/works", json={"title": "Демо викладача", "base_custom": "Своя гра-прикладка"})
    check("admin: own work, custom base", r.status_code == 200, r.text)
    r = c.post("/api/works/my/objects", json={"kind": "window", "task": "settings-window", "title": "Налаштування"})
    check("admin: draft type allowed", r.status_code == 200, r.text)
    r = c.get("/api/works").json()
    check("gallery: 2 works with owners", len(r) == 2 and all("owner_info" in w for w in r))
    check("passport of another: mine=false", c.get(f"/api/works/{wid}").json()["mine"] is False)
    check("history recorded", mongo[DB].history.count_documents({"coll": "works"}) >= 2)

ok = sum(1 for _, p in results if p)
print(f"\n{ok}/{len(results)} PASS")
sys.exit(0 if ok == len(results) else 1)
