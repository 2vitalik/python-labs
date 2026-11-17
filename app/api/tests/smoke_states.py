"""Smoke: an entity's state renamed (T344) — the word changes on the card and in the rules that mean this entity's state,
not in another entity's; duplicates and unknown states are refused; the history keeps both — on a scratch DB.
Run from app/api: DB_NAME=python_labs_states_smoke TG_BOT_TOKEN= UPLOADS_DIR=... uv run python tests/smoke_states.py"""
import os
import subprocess
import sys

sys.path.insert(0, os.getcwd())
from pymongo import MongoClient  # noqa: E402

DB = os.environ["DB_NAME"]
assert DB.endswith("_smoke"), "refuse to run on a non-smoke DB"
mongo = MongoClient()
mongo.drop_database(DB)
subprocess.run(["uv", "run", "python", "catalog_io.py", "import"], check=True, capture_output=True)

from fastapi.testclient import TestClient  # noqa: E402

import main  # noqa: E402
from core.config import settings  # noqa: E402

PARTS, RULES = "/api/my/game/parts", "/api/my/game/rules"
results = []


def check(name, cond, extra=""):
    results.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


with TestClient(main.app) as c:
    settings.fake_user_email = "stud@nure.ua"
    c.get("/api/auth/dev-login")
    mongo[DB].users.update_one({"email": "stud@nure.ua"}, {"$set": {"status": "student", "group": "ПЗПІ-25-1"}})
    c.post("/api/my/game", json={"title": "Привиди", "base_game": "pac-man"})
    ghost = c.post(PARTS, json={"kind": "entity", "title": "Привид", "role": "enemy", "states": ["злий", "наляканий"]}).json()["id"]
    hero = c.post(PARTS, json={"kind": "entity", "title": "Герой", "role": "player", "states": ["звичайний", "наляканий"]}).json()["id"]
    wall = c.post(PARTS, json={"kind": "entity", "title": "Стіна", "role": "terrain"}).json()["id"]

    def rule(when, then, cond=()):
        r = c.post(RULES, json={"when": when, "cond": list(cond), "then": then})
        assert r.status_code == 200, r.text
        return r.json()["id"]

    direct = rule({"kind": "state_on", "a": ghost, "s": "наляканий"}, [{"kind": "clear_state", "a": ghost, "s": "злий"}])
    side = rule({"kind": "contact", "a": hero, "b": ghost}, [{"kind": "set_state", "a": "@b", "s": "наляканий"}],
                [{"kind": "state", "a": "@a", "s": "наляканий"}])
    other = rule({"kind": "state_on", "a": hero, "s": "наляканий"}, [{"kind": "set_state", "a": hero, "s": "звичайний"}])
    anyone = rule({"kind": "contact", "a": hero, "b": wall}, [{"kind": "set_state", "a": "*", "s": "злий"}])

    def rules():
        return {r["id"]: r for r in c.get("/api/students/stud/game").json()["rules"]}

    r = c.post(f"{PARTS}/{ghost}/states/rename", json={"old": "наляканий", "new": "  тікає   геть "})
    check("rename: the card has the new word in the old place", r.status_code == 200 and r.json()["part"]["states"] == ["злий", "тікає геть"], r.text)
    check("rename: two rules followed", r.json()["rules"] == 2, r.text)
    now = rules()
    check("a rule about the entity itself: the trigger renamed, its other state untouched",
          now[direct]["when"]["s"] == "тікає геть" and now[direct]["then"][0]["s"] == "злий", now[direct])
    check("a rule by the trigger's sides: the ghost's side renamed, the hero's same word stays",
          now[side]["then"][0]["s"] == "тікає геть" and now[side]["cond"][0]["s"] == "наляканий", now[side])
    check("another entity's state of the same word stays", now[other]["when"]["s"] == "наляканий", now[other])

    r = c.post(f"{PARTS}/{ghost}/states/rename", json={"old": "злий", "new": "лютий"})
    check("a clause about anyone follows while the word is this entity's alone", r.json()["rules"] == 2 and rules()[anyone]["then"][0]["s"] == "лютий", r.text)
    r = c.post(f"{PARTS}/{hero}/states/rename", json={"old": "наляканий", "new": "тремтить"})
    check("…the hero's rename takes its own clauses", r.json()["rules"] == 2 and rules()[side]["cond"][0]["s"] == "тремтить"
          and rules()[other]["when"]["s"] == "тремтить", r.text)

    check("a state the entity has already → 422", c.post(f"{PARTS}/{ghost}/states/rename", json={"old": "лютий", "new": "Тікає геть"}).status_code == 422)
    check("an empty name → 422", c.post(f"{PARTS}/{ghost}/states/rename", json={"old": "лютий", "new": "  "}).status_code == 422)
    check("an unknown state → 404", c.post(f"{PARTS}/{ghost}/states/rename", json={"old": "нема", "new": "є"}).status_code == 404)
    check("an entity without that state → 404", c.post(f"{PARTS}/{wall}/states/rename", json={"old": "лютий", "new": "є"}).status_code == 404)
    r = c.post(f"{PARTS}/{ghost}/states/rename", json={"old": "лютий", "new": "Лютий"})
    check("the same word in another case: renamed", r.status_code == 200 and r.json()["part"]["states"][0] == "Лютий", r.text)
    r = c.post(f"{PARTS}/{ghost}/states/rename", json={"old": "Лютий", "new": "злий"})
    check("back again: the rules come back too", r.json()["rules"] == 2 and rules()[direct]["then"][0]["s"] == "злий" and rules()[anyone]["then"][0]["s"] == "злий", r.text)

    settings.fake_user_email = "admin@nure.ua"
    c.get("/api/auth/dev-login")
    mongo[DB].users.update_one({"email": "admin@nure.ua"}, {"$set": {"status": "admin"}})
    hist = c.get("/api/students/stud/game/history").json()
    check("history: the entity's states and the rules' clauses, each its own row",
          any(h["what"] == "сутність" and any(f["label"] == "стани" for f in h["fields"]) for h in hist)
          and any(h["what"] == "правило" and any("тікає геть" in (f["new"] or "") for f in h["fields"]) for h in hist), hist[:3])

ok = sum(results)
print(f"\n{ok}/{len(results)} PASS")
sys.exit(0 if ok == len(results) else 1)
