"""Smoke: the teacher edits a student's game (T282 Б) — «Моя гра»'s routes under `X-Game-Of: <nick>` work on that student's
game and write the teacher into its history; only an admin; no alerts; nothing else moves — on a scratch DB. Run from app/api:
DB_NAME=python_labs_teacher_smoke TG_BOT_TOKEN= UPLOADS_DIR=... uv run python tests/smoke_teacher_edit.py"""
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
db = mongo[DB]
subprocess.run(["uv", "run", "python", "catalog_io.py", "import"], check=True, capture_output=True)

from fastapi.testclient import TestClient  # noqa: E402

import main  # noqa: E402
import uploads  # noqa: E402
from core.config import settings  # noqa: E402

PNG = b"\x89PNG\r\n\x1a\n" + b"0" * 100
GAME, PARTS, RULES, CLAIMS = "/api/my/game", "/api/my/game/parts", "/api/my/game/rules", "/api/my/claims"
H = {"X-Game-Of": "stud"}
results = []


def check(name, cond, extra=""):
    results.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def login(c, email, status, last=""):
    settings.fake_user_email = email
    c.get("/api/auth/dev-login")
    db.users.update_one({"email": email}, {"$set": {"status": status, "group": "ПЗПІ-25-1", "last_name": last}})


def alerts():
    return db.events.count_documents({"kind": {"$in": ["game", "claim"]}})


with TestClient(main.app) as c:
    login(c, "stud@nure.ua", "student", last="Студентенко")
    c.post(GAME, json={"title": "Привиди", "base_game": "sokoban"})
    hero = c.post(PARTS, json={"kind": "entity", "title": "Герой", "role": "player"}).json()
    sid = db.student_games.find_one({"owner": "stud@nure.ua"})["_id"]
    login(c, "lonely@nure.ua", "student")  # no game
    login(c, "other@nure.ua", "student")
    check("a student with the header → 403", c.get(GAME, headers=H).status_code == 403
          and c.post(PARTS, headers=H, json={"kind": "entity", "title": "Х", "role": "enemy"}).status_code == 403)
    login(c, "admin@nure.ua", "admin", last="Викладач")
    c.post(GAME, json={"title": "Моя", "base_game": "sokoban"})
    aid = db.student_games.find_one({"owner": "admin@nure.ua"})["_id"]
    db.users.insert_one({"email": "test.student@nure.ua", "status": "student", "test": True})
    c.post("/api/me/as/test.student")
    check("looking as a student with the header → 403", c.get(GAME, headers=H).status_code == 403)
    c.delete("/api/me/as")

    r = c.get(GAME, headers=H)
    check("the admin with the header reads the student's game", r.status_code == 200 and r.json()["title"] == "Привиди", r.text)
    r = c.get(GAME, headers={"X-Game-Of": "nobody"})
    check("no such student → 404 in words", r.status_code == 404 and "не знайдено" in r.json()["detail"], r.text)
    r = c.post(PARTS, headers={"X-Game-Of": "lonely"}, json={"kind": "entity", "title": "Х", "role": "enemy"})
    check("a student with no game → 404 in words", r.status_code == 404 and "ще нема гри" in r.json()["detail"], r.text)
    r = c.post(GAME, headers={"X-Game-Of": "lonely"}, json={"title": "За нього", "base_game": "sokoban"})
    check("no creating a game for a student → 403", r.status_code == 403 and not db.student_games.find_one({"owner": "lonely@nure.ua"}), r.text)
    check("with the sandbox at once → 422", c.get(GAME, headers=H | {"X-Sandbox": "sokoban"}).status_code == 422)

    before = alerts()
    ghost = c.post(PARTS, headers=H, json={"kind": "entity", "title": "Привид", "role": "enemy"})
    check("part → in the student's game", ghost.status_code == 200 and db.game_parts.find_one({"_id": ObjectId(ghost.json()["id"])})["game"] == sid, ghost.text)
    ghost = ghost.json()
    r = c.put(f"{PARTS}/{hero['id']}", headers=H, json=hero | {"description": "ходить"})
    check("the student's part edited", r.status_code == 200 and db.game_parts.find_one({"_id": ObjectId(hero["id"])})["description"] == "ходить")
    rule = c.post(RULES, headers=H, json={"when": {"kind": "contact", "a": hero["id"], "b": ghost["id"]}, "then": [{"kind": "lose"}]})
    check("rule → in the student's game", rule.status_code == 200 and db.rules.find_one({"_id": ObjectId(rule.json()["id"])})["game"] == sid, rule.text)
    claim = c.post(CLAIMS, headers=H, json={"task": "player-death", "rule": rule.json()["id"]})
    check("claim → in the student's game", claim.status_code == 200 and db.claims.find_one({"_id": ObjectId(claim.json()["id"])})["game"] == sid, claim.text)
    c.put(f"{CLAIMS}/{claim.json()['id']}", headers=H, json={"note": "викладач дописав"})
    draft = db.tasks.find_one_and_update({"slug": "game-pause"}, {"$set": {"status": "draft"}})  # the catalog keeps no drafts of its own
    r = c.post(CLAIMS, headers=H, json={"task": draft["slug"]})
    check("a draft card: the teacher may claim it", r.status_code == 200, r.text)
    r = c.post(f"{PARTS}/{ghost['id']}/screenshot", headers=H, files={"file": ("s.png", PNG, "image/png")})
    shot = r.json()["screenshots"][0] if r.status_code == 200 else ""
    check("screenshot → the student's game folder", shot and (uploads.ROOT / str(sid) / shot).exists(), r.text)
    r = c.put(GAME, headers=H, json={"title": "Привиди 2", "base_game": "sokoban"})
    check("the card renamed", r.status_code == 200 and db.student_games.find_one({"_id": sid})["title"] == "Привиди 2", r.text)
    check("no alerts for the teacher's edits", alerts() == before, f"{before} → {alerts()}")

    rows = c.get("/api/students/stud/game/history", params={"who": "staff", "limit": 200}).json()
    done = {(x["what"], x["action"]) for x in rows}
    check("history, who=staff: the teacher's rows only", rows and all(x["actor"]["nick"] == "admin" and x["actor"]["role"] == "teacher" for x in rows), rows[:2])
    check("history: part, rule, claim, screenshot, card", {("сутність", "added"), ("правило", "added"), ("заявка", "added"),
                                                           ("сутність", "changed"), ("гра", "changed")} <= done, done)
    mine = c.get("/api/students/stud/game/history", params={"who": "student", "limit": 200}).json()
    check("history, who=student: none of them", mine and all(x["actor"]["nick"] == "stud" for x in mine), mine[:2])

    row = lambda: next(s for s in c.get("/api/students").json() if s["nick"] == "stud")["game"]  # noqa: E731
    own = lambda: db.claims.count_documents({"game": sid, "auto": False, "status": "claimed"})  # noqa: E731
    g = row()
    check("the list: ⏳ — claims waiting for the word, auto ones aside", g["waiting"] == own() >= 2, f"{g['waiting']} vs {own()}")
    c.put(f"/api/students/stud/claims/{claim.json()['id']}", json={"status": "accepted"})
    rate = {"wood": 1, "tin": 2, "bronze": 4, "silver": 8, "gold": 16, "crown": 32}
    g2 = row()
    check("a verdict: one less waiting, the accepted in 🌱", g2["waiting"] == g["waiting"] - 1 and g2["wood_accepted"] > 0
          and g2["wood_accepted"] == sum(rate[k] * n for k, n in g2["coins_accepted"].items())
          and g2["wood_claimed"] == sum(rate[k] * n for k, n in g2["coins"].items()), g2)

    r = c.get(GAME)
    check("no header: the admin's own game, untouched", r.json()["title"] == "Моя" and db.game_parts.count_documents({"game": aid}) == 0
          and db.claims.count_documents({"game": aid}) == 0, r.text)
    r = c.delete(f"{PARTS}/{ghost['id']}", headers=H)
    check("delete in the student's game: the rule goes too", r.status_code == 200 and db.rules.count_documents({"game": sid}) == 0)

    login(c, "stud@nure.ua", "student", last="Студентенко")
    before = alerts()
    r = c.post(PARTS, json={"kind": "entity", "title": "Скриня", "role": "enemy"})
    check("no header: the student writes their own game, with an alert", r.status_code == 200
          and db.game_parts.find_one({"_id": ObjectId(r.json()["id"])})["game"] == sid and alerts() == before + 1, f"{r.text} · {alerts() - before}")

ok = sum(results)
print(f"\n{ok}/{len(results)} PASS")
sys.exit(0 if ok == len(results) else 1)
