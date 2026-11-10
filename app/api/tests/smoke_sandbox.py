"""Smoke: the etalon's sandbox (T274 §7) — the copy, «Моя гра»'s routes under X-Sandbox, no traces, the reset — on a scratch
DB. Run from app/api: DB_NAME=python_labs_smoke TG_BOT_TOKEN= UPLOADS_DIR=... uv run python tests/smoke_sandbox.py"""
import os
import subprocess
import sys

sys.path.insert(0, os.getcwd())
from bson import ObjectId  # noqa: E402
from pymongo import MongoClient  # noqa: E402

DB = os.environ["DB_NAME"]
assert DB.endswith("_smoke"), "refuse to run on a non-smoke DB"
mongo = MongoClient()
mongo.drop_database(DB)
subprocess.run(["uv", "run", "python", "catalog_io.py", "import"], check=True, capture_output=True)

from fastapi.testclient import TestClient  # noqa: E402

import main  # noqa: E402
from core.config import settings  # noqa: E402

PNG = b"\x89PNG\r\n\x1a\n" + b"0" * 100
PARTS, RULES, CLAIMS = "/api/my/game/parts", "/api/my/game/rules", "/api/my/claims"
H = {"X-Sandbox": "sokoban"}
BOX = "stud+nure.ua@sandbox"
results = []


def check(name, cond, extra=""):
    results.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def login(c, email, status):
    settings.fake_user_email = email
    c.get("/api/auth/dev-login")
    mongo[DB].users.update_one({"email": email}, {"$set": {"status": status}})


def titles(p):
    return sorted((x["kind"], x["title"]) for x in p["parts"])


with TestClient(main.app) as c:
    check("guest: no sandbox → 401", c.post("/api/games/sokoban/sandbox").status_code == 401)
    login(c, "waiting@nure.ua", "pending")
    check("pending: no sandbox → 403", c.post("/api/games/sokoban/sandbox").status_code == 403)

    login(c, "stud@nure.ua", "student")
    c.post("/api/my/game", json={"title": "Мій сокобан", "base_game": "sokoban"})
    mine = c.post(PARTS, json={"kind": "entity", "title": "Герой", "role": "player"}).json()
    real = lambda: c.get("/api/students/stud/game").json()  # noqa: E731
    before = real()
    check("no copy yet → 404", c.get("/api/games/sokoban/sandbox").status_code == 404)
    r = c.post(PARTS, headers=H, json={"kind": "entity", "title": "Х", "role": "enemy"})
    check("the header and no copy → 404 «Пісочницю не відкрито»", r.status_code == 404 and "Пісочницю не відкрито" in r.json()["detail"], r.text)
    check("no etalon → 404", c.post("/api/games/no-such/sandbox").status_code == 404)

    r = c.post("/api/games/sokoban/sandbox")
    box, etalon = r.json(), c.get("/api/games/sokoban/etalon").json()
    check("create: the etalon's copy in the passport's shape, owned by the made-up address",
          r.status_code == 200 and set(box) == {"game", "parts", "claims", "rules", "coins", "tasks"} and box["game"]["owner"] == BOX
          and box["game"]["base_game"] == "sokoban" and titles(box) == titles(etalon) and len(box["claims"]) == len(etalon["claims"])
          and len(box["rules"]) == len(etalon["rules"]) and box["game"]["id"] != etalon["game"]["id"], r.text[:300])
    check("GET: the copy", c.get("/api/games/sokoban/sandbox").json()["game"]["id"] == box["game"]["id"])
    check("GET of another base → 404", c.get("/api/games/battle-city/sandbox").status_code == 404)

    check("GET /my/game under the header → the copy", c.get("/api/my/game", headers=H).json()["owner"] == BOX)
    r = c.put("/api/my/game", headers=H, json={"title": "Пробую", "base_game": "sokoban", "description": "так", "phases": ["ввід", "гравець"]})
    check("PUT /my/game: the copy's title, description, phases", r.status_code == 200 and r.json()["owner"] == BOX
          and r.json()["title"] == "Пробую" and r.json()["phases"] == ["ввід", "гравець"], r.text)
    check("PUT /my/game: another base in the sandbox → 422",
          c.put("/api/my/game", headers=H, json={"title": "Пробую", "base_game": "battle-city"}).status_code == 422)
    r = c.post(PARTS, headers=H, json={"kind": "entity", "title": "Привид", "role": "enemy"})
    ghost = r.json()
    check("part: into the copy", r.status_code == 200 and ghost["game"] == box["game"]["id"], r.text)
    hero = next(p for p in box["parts"] if p["kind"] == "entity")
    r = c.post(RULES, headers=H, json={"when": {"kind": "contact", "a": hero["id"], "b": ghost["id"]}, "then": [{"kind": "lose"}]})
    rule = r.json()
    check("rule: into the copy", r.status_code == 200 and rule["game"] == box["game"]["id"], r.text)
    r = c.post(CLAIMS, headers=H, json={"task": "player-death", "rule": rule["id"]})
    check("claim: into the copy", r.status_code == 200 and r.json()["game"] == box["game"]["id"], r.text)
    r = c.put(f"{CLAIMS}/{r.json()['id']}", headers=H, json={"note": "спроба"})
    check("claim edit in the copy", r.status_code == 200 and r.json()["note"] == "спроба", r.text)
    gone = next(p for p in box["parts"] if p["kind"] == "window")
    check("part delete in the copy", c.delete(f"{PARTS}/{gone['id']}", headers=H).status_code == 200)
    check("the real game's part is not the copy's → 404", c.delete(f"{PARTS}/{mine['id']}", headers=H).status_code == 404)
    r = c.post(f"{PARTS}/{ghost['id']}/screenshot", headers=H, files={"file": ("s.png", PNG, "image/png")})
    check("screenshot → 403", r.status_code == 403 and "скриншоти не зберігаються" in r.json()["detail"], r.text)
    check("template → 403", c.post("/api/my/game/template", headers=H, json={}).status_code == 403)
    check("the header naming another base → 404", c.post(PARTS, headers={"X-Sandbox": "battle-city"}, json={"kind": "level", "title": "Х"}).status_code == 404)
    check("the real game untouched", real() == before)

    copy = c.get("/api/games/sokoban/sandbox").json()
    r = c.post(PARTS, json={"kind": "entity", "title": "Справжній", "role": "enemy"})
    check("no header → the real game, the copy untouched", r.json()["game"] == before["game"]["id"]
          and c.get("/api/games/sokoban/sandbox").json() == copy and c.get("/api/my/game").json()["owner"] == "stud@nure.ua")

    ids = [x["id"] for k in ("parts", "claims", "rules") for x in copy[k]] + [copy["game"]["id"]]
    check("no history: neither by the made-up author nor of the copy's documents",
          mongo[DB].history.count_documents({"actor": BOX}) == 0
          and mongo[DB].history.count_documents({"doc_id": {"$in": [ObjectId(i) for i in ids]}}) == 0)
    check("no alerts from the sandbox, the real game's are there",
          mongo[DB].events.count_documents({"user": {"$regex": "@sandbox$"}}) == 0 and mongo[DB].events.count_documents({"user": "stud@nure.ua"}) >= 2)

    r = c.post("/api/games/sokoban/sandbox")
    again = r.json()
    check("reset: the etalon again — the card, parts and rules as poured, own edits gone",
          r.status_code == 200 and titles(again) == titles(etalon) and len(again["rules"]) == len(etalon["rules"])
          and again["game"]["title"] == box["game"]["title"] and again["game"]["phases"] == [] and not any(p["title"] == "Привид" for p in again["parts"]))
    check("reset: one copy per user, no history", mongo[DB].student_games.count_documents({"owner": BOX}) == 1
          and mongo[DB].history.count_documents({"actor": BOX}) == 0)
    r = c.post("/api/games/battle-city/sandbox")
    check("another base: the copy switches to it", r.status_code == 200 and r.json()["game"]["base_game"] == "battle-city"
          and c.get("/api/games/sokoban/sandbox").status_code == 404 and c.post(PARTS, headers=H, json={"kind": "level", "title": "Х"}).status_code == 404
          and mongo[DB].student_games.count_documents({"owner": BOX}) == 1)

    login(c, "stud2@nure.ua", "student")
    check("another user: no copy of theirs → 404", c.post(PARTS, headers=H, json={"kind": "level", "title": "Х"}).status_code == 404)
    r = c.post("/api/games/sokoban/sandbox")
    check("another user: a copy of their own", r.json()["game"]["owner"] == "stud2+nure.ua@sandbox"
          and mongo[DB].student_games.count_documents({"owner": BOX, "base_game": "battle-city"}) == 1)

    login(c, "admin@nure.ua", "admin")
    rows = c.get("/api/students").json()
    check("gallery: no sandbox, the real game is there", not any(x["game"] and x["game"]["owner"].endswith("@sandbox") for x in rows)
          and any(x["nick"] == "stud" and x["game"] for x in rows), [x["nick"] for x in rows])
    check("no passport by the sandbox's nick", c.get("/api/students/stud+nure.ua/game").status_code == 404)
    who = {x["user"] for x in c.get("/api/activity", params={"src": "edit,event", "limit": 500}).json()["rows"]}
    check("activity feed: the student's edits, nothing by the sandbox", "stud@nure.ua" in who and not any(u.endswith("@sandbox") for u in who), who)

ok = sum(results)
print(f"\n{ok}/{len(results)} PASS")
sys.exit(0 if ok == len(results) else 1)
