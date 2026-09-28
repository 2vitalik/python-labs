"""Smoke: history of tasks and games (T156) — every edit with what changed, a revert as a new edit, what cannot be
reverted, who may look, the YAML import in the same journal. Run from app/api:
DB_NAME=python_labs_smoke uv run python tests/smoke_card_history.py"""
import os
import subprocess
import sys

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
settings.agent_tokens = "claude:tok-claude"
CLAUDE = {"Authorization": "Bearer tok-claude"}
H = "/api/catalog/history"


def check(name, cond, extra=""):
    results.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def login(c, email, status):
    settings.fake_user_email = email
    c.get("/api/auth/dev-login")
    mongo[DB].users.update_one({"email": email}, {"$set": {"status": status}})


with TestClient(main.app) as c:
    login(c, "admin@nure.ua", "admin")
    card = {"slug": "card-a", "title": "Картка", "zone": "code", "subzone": "git", "coin": "tin", "description": "рядок 1\nрядок 2"}
    t = c.post("/api/tasks", json=card).json()
    c.put(f"/api/tasks/{t['id']}", json=card | {"coin": "silver", "description": "рядок 1\nрядок 2 змінено", "tags": ["algo"]})
    h = c.get(f"{H}/tasks").json()
    check("two rows, newest first: the edit, the creation", [e["created"] for e in h] == [False, True], h)
    check("the edit: fields with old → new, actor, card", h[0]["changes"]["coin"] == {"old": "tin", "new": "silver"}
          and set(h[0]["changes"]) == {"coin", "description", "tags"} and h[0]["actor"] == "admin" and h[0]["slug"] == "card-a", h[0])
    check("time carries the zone", h[0]["at"].endswith("+00:00"), h[0]["at"])
    check("the guide's history too", all(e["at"].endswith("+00:00") for e in c.get("/api/guide/history").json()))

    r = c.post(f"{H}/tasks/{h[0]['id']}/revert")
    check("revert: the old values are back", r.status_code == 200 and r.json()["coin"] == "tin" and r.json()["tags"] == []
          and r.json()["description"] == "рядок 1\nрядок 2", r.text)
    h = c.get(f"{H}/tasks?slug=card-a").json()
    check("revert is a new edit with a note", len(h) == 3 and h[0]["note"].startswith("відкат правки від ")
          and h[0]["changes"]["coin"] == {"old": "silver", "new": "tin"}, h[0])
    check("revert of the revert: forward again", c.post(f"{H}/tasks/{h[0]['id']}/revert").json()["coin"] == "silver")
    check("a creation is not reverted → 422", c.post(f"{H}/tasks/{h[-1]['id']}/revert").status_code == 422)

    c.put(f"/api/tasks/{t['id']}", json=card | {"slug": "card-b", "coin": "silver", "tags": ["algo"], "description": "рядок 1\nрядок 2 змінено"})
    c.post("/api/tasks", json=card | {"slug": "card-a", "title": "Інша"})
    rename = next(e for e in c.get(f"{H}/tasks?slug=card-b").json() if "slug" in e["changes"])
    r = c.post(f"{H}/tasks/{rename['id']}/revert")
    check("revert to a taken slug → 422, the card stays", r.status_code == 422 and "card-a" in r.json()["detail"]
          and mongo[DB].tasks.count_documents({"slug": "card-b"}) == 1, r.text)

    g = c.post("/api/games", json={"slug": "game-a", "title": "Гра", "summary": "було"}).json()
    c.put(f"/api/games/{g['id']}", json={"slug": "game-a", "title": "Гра", "summary": "стало"})
    h = c.get(f"{H}/games?slug=game-a").json()
    r = c.post(f"{H}/games/{h[0]['id']}/revert")
    check("games: history and revert", len(h) == 2 and r.status_code == 200 and r.json()["summary"] == "було", r.text)
    check("a game's edit is not a task's", c.post(f"{H}/tasks/{h[0]['id']}/revert").status_code == 404)
    check("unknown kind, card, edit → 404", [c.get(f"{H}/users").status_code, c.get(f"{H}/tasks?slug=nope").status_code,
                                             c.post(f"{H}/tasks/{'0' * 24}/revert").status_code] == [404] * 3)

    c.cookies.clear()
    check("guest: 401", c.get(f"{H}/tasks").status_code == 401 and c.post(f"{H}/games/{h[0]['id']}/revert").status_code == 401)
    last = c.get(f"{H}/games", headers=CLAUDE).json()[0]  # the admin's revert: undoing it puts «стало» back
    r = c.post(f"{H}/games/{last['id']}/revert", headers=CLAUDE)
    check("agent: reads and reverts, under its name", r.status_code == 200 and r.json()["summary"] == "стало"
          and c.get(f"{H}/games", headers=CLAUDE).json()[0]["actor"] == "claude", r.text)
    login(c, "stud@nure.ua", "student")
    check("student: 403", c.get(f"{H}/tasks").status_code == 403 and c.post(f"{H}/games/{h[0]['id']}/revert").status_code == 403)

    before = mongo[DB].history.count_documents({"actor": "import"})
    run = lambda: subprocess.run(["uv", "run", "python", "catalog_io.py", "import"], capture_output=True, text=True)  # noqa: E731
    out = run()
    cards = mongo[DB].tasks.count_documents({}) + mongo[DB].games.count_documents({})
    logged = mongo[DB].history.count_documents({"actor": "import"})
    check("import: every new card logged", out.returncode == 0 and before == 0 and logged == cards - 3, f"{logged} of {cards} · {out.stderr[-300:]}")
    run()
    check("import again: nothing new in history", mongo[DB].history.count_documents({"actor": "import"}) == logged)
    mongo[DB].tasks.update_one({"slug": "main-menu"}, {"$set": {"coin": "crown"}})
    run()
    row = mongo[DB].history.find_one({"actor": "import", "changes.coin.old": "crown"})
    check("import over a changed card: the edit is logged", row and mongo[DB].tasks.find_one({"slug": "main-menu"})["coin"] == row["changes"]["coin"]["new"])
    login(c, "admin@nure.ua", "admin")
    rows = c.get("/api/activity?src=edit&limit=500").json()["rows"]
    check("activity: import rows hidden with the staff", not any(r["user"] == "import" for r in rows))

ok = sum(1 for _, p in results if p)
print(f"\n{ok}/{len(results)} PASS")
sys.exit(0 if ok == len(results) else 1)
