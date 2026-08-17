"""Smoke: student games / parts / claims / screenshots / gallery on a scratch DB. Run from app/api:
DB_NAME=python_labs_smoke UPLOADS_DIR=... uv run python tests/smoke_games.py"""
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
import uploads  # noqa: E402
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
    check("guest: /students → 403", c.get("/api/students").status_code == 403)

    login(c, "waiting@nure.ua", "pending")  # stays pending: gallery visibility check below
    check("pending: POST /my/game → 403", c.post("/api/my/game", json={"title": "x", "base_custom": "y"}).status_code == 403)

    login(c, "stud@nure.ua", "student")
    check("no game yet: GET /my/game → null", c.get("/api/my/game").json() is None)
    r = c.post("/api/my/game", json={"title": "Танчики Пілот", "base_game": "battle-city"})
    check("create game", r.status_code == 200, r.text)
    gid = r.json()["id"]
    check("second game → 409", c.post("/api/my/game", json={"title": "Друга", "base_custom": "x"}).status_code == 409)
    check("bad base → 422", c.put("/api/my/game", json={"title": "Т", "base_game": "no-such"}).status_code == 422)
    check("no base → 422", c.put("/api/my/game", json={"title": "Т"}).status_code == 422)

    r = c.post("/api/my/game/parts", json={"kind": "window", "task": "main-menu", "title": "Головне меню"})
    check("window create", r.status_code == 200, r.text)
    win = r.json()["id"]
    check("draft type for student → 422",
          c.post("/api/my/game/parts", json={"kind": "window", "task": "settings-window", "title": "Н"}).status_code == 422)
    check("non-window card as type → 422",
          c.post("/api/my/game/parts", json={"kind": "window", "task": "player-death", "title": "Х"}).status_code == 422)
    r = c.get("/api/students/stud/game")
    check("passport by nick", r.status_code == 200, r.text)
    check("auto-claim of window type", [cl["task"] for cl in r.json()["claims"]] == ["main-menu"])
    check("claims enriched with card info", r.json()["tasks"]["main-menu"]["coin"] == "tin")
    check("unknown nick → 404", c.get("/api/students/nobody/game").status_code == 404)

    r = c.post("/api/my/game/parts", json={"kind": "menu", "title": "Меню старту", "window": win,
                                           "items": [{"title": "Нова гра", "window": win},
                                                     {"title": "Гучність", "task": "sound-volume"},
                                                     {"title": "  "}]})
    check("menu create (items cleaned)", r.status_code == 200 and len(r.json()["items"]) == 2, r.text)
    menu = r.json()["id"]
    check("bad item target → 422",
          c.post("/api/my/game/parts", json={"kind": "menu", "title": "М",
                                             "items": [{"title": "x", "window": "000000000000000000000000"}]}).status_code == 422)

    r = c.post(f"/api/my/game/parts/{win}/screenshot", files={"file": ("s.png", PNG, "image/png")})
    check("screenshot upload", r.status_code == 200 and len(r.json()["screenshots"]) == 1, r.text)
    shot = r.json()["screenshots"][0]
    check("file on disk", (Path(os.environ["UPLOADS_DIR"]) / gid / shot).is_file())
    check("static serve", c.get(f"/api/uploads/{gid}/{shot}").status_code == 200)
    check("bad type → 422",
          c.post(f"/api/my/game/parts/{win}/screenshot", files={"file": ("s.txt", b"x", "text/plain")}).status_code == 422)
    check("oversize → 422",
          c.post(f"/api/my/game/parts/{win}/screenshot",
                 files={"file": ("s.png", b"0" * (8 * 2**20 + 1), "image/png")}).status_code == 422)

    r = c.get("/api/students").json()
    me = next(s for s in r if s["nick"] == "stud")
    check("gallery: cover + counters", me["game"]["cover"].endswith(shot) and me["game"]["windows"] == 1)
    check("gallery: student sees no emails/pending", all("email" not in s for s in r)
          and not any(s["nick"] == "waiting" for s in r))

    r = c.post("/api/my/claims", json={"task": "player-death"})
    check("game-level claim", r.status_code == 200, r.text)
    check("duplicate claim → 409", c.post("/api/my/claims", json={"task": "player-death"}).status_code == 409)
    check("draft card claim for student → 422",
          c.post("/api/my/claims", json={"task": "sound-volume"}).status_code == 422)
    r = c.post("/api/my/claims", json={"task": "status-panel", "part": win})
    check("part claim", r.status_code == 200, r.text)
    check("claim on alien part → 422",
          c.post("/api/my/claims", json={"task": "time-out", "part": "abc"}).status_code == 422)

    r = c.delete(f"/api/my/game/parts/{win}")
    check("window delete", r.status_code == 200)
    r = c.get("/api/students/stud/game").json()
    check("cascade: window claims gone", {cl["task"] for cl in r["claims"]} == {"player-death"})
    m = next(p for p in r["parts"] if p["id"] == menu)
    check("cascade: menu host stripped", m["window"] == "")
    check("cascade: item target stripped", m["items"][0]["window"] == "")
    check("cascade: file left original dir", not (Path(os.environ["UPLOADS_DIR"]) / gid / shot).is_file())
    check("cascade: file in trash", (uploads.TRASH / gid / shot).is_file())

    login(c, "admin@nure.ua", "admin")
    r = c.post("/api/my/game", json={"title": "Демо викладача", "base_custom": "Своя гра-прикладка"})
    check("admin: own game, custom base", r.status_code == 200, r.text)
    r = c.post("/api/my/game/parts", json={"kind": "window", "task": "settings-window", "title": "Налаштування"})
    check("admin: draft type allowed", r.status_code == 200, r.text)
    r = c.get("/api/students").json()
    check("admin gallery: emails + pending visible", any(s.get("email") for s in r)
          and any(s["nick"] == "waiting" for s in r))
    check("gallery: 2 games", sum(1 for s in r if s["game"]) == 2)
    check("passport of another: mine=false", c.get("/api/students/stud/game").json()["mine"] is False)
    check("admin: student by nick", c.get("/api/students/stud").json()["email"] == "stud@nure.ua")
    r = c.put("/api/students/stud", json={"last_name": "Тест", "group": "ПЗПІ-25-1"})
    check("admin: edit by nick", r.status_code == 200 and r.json()["group"] == "ПЗПІ-25-1", r.text)
    check("history recorded", mongo[DB].history.count_documents({"coll": "student_games"}) >= 2)
    check("cascade deletes logged", mongo[DB].history.count_documents({"coll": "claims", "changes.task.new": None}) >= 1)

ok = sum(1 for _, p in results if p)
print(f"\n{ok}/{len(results)} PASS")
sys.exit(0 if ok == len(results) else 1)
