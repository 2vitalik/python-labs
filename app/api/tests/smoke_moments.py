"""Smoke: what a student draws on the site (T276) — the game's moments (saved, kept by the other forms, the limit, the history),
a level's map, the cards they claim by themselves (a scenario of three frames and more — one claim each, a level with a map —
one on it; gone when the drawing is) and their falling price — on a scratch DB.
Run from app/api: DB_NAME=python_labs_moments_smoke TG_BOT_TOKEN= UPLOADS_DIR=... uv run python tests/smoke_moments.py"""
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
mongo[DB].tasks.update_many({"slug": {"$in": ["moment-frames", "level-map-drawn"]}}, {"$set": {"core": True}})  # their price, not a request (T319)

from fastapi.testclient import TestClient  # noqa: E402

import main  # noqa: E402
from core.config import settings  # noqa: E402
from moments import scenes  # noqa: E402

GAME, PARTS, H = "/api/my/game", "/api/my/game/parts", "/api/students/stud/game/history"
BASE = {"title": "Лабіринт", "base_custom": "своя"}
results = []


def check(name, cond, extra=""):
    results.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def login(c, email, status):
    settings.fake_user_email = email
    c.get("/api/auth/dev-login")
    mongo[DB].users.update_one({"email": email}, {"$set": {"status": status, "group": "ПЗПІ-25-1"}})


def frame(i):
    return f"Крок {i}:\n\n```field\n⬛ ⬛ ⬛\n⬛ [😎]⬛\n```"


def scenario(title, n):
    return "\n\n".join([f"### {title}"] + [frame(i) for i in range(n)])


def text(*sizes):
    return "\n\n".join(["- 😎 — **гравець**", "**Приклад ігрового моменту**"] + [scenario(f"С{i}", n) for i, n in enumerate(sizes)])


def put(c, moments):
    return c.put(GAME, json=BASE | {"moments": moments})


def autos(task):
    return [x for x in c.get("/api/students/stud/game").json()["claims"] if x["task"] == task and x["auto"]]


def wood():
    return c.get("/api/students/stud/game").json()["coins"]["claimed"].get("wood", 0)


check("frames counted like the editor: a bare fence too, a heading splits, an empty fence is no frame",
      scenes("x\n\n```\n⬛ ⬛\n```\n\n### Б\n\n```field\n⬛\n```\n\n```field\n```") == [1, 1])
check("the cards are in the catalog", mongo[DB].tasks.count_documents({"slug": {"$in": ["moment-frames", "level-map-drawn"]}, "status": "active"}) == 2)

with TestClient(main.app) as c:
    login(c, "stud@nure.ua", "student")
    c.post(GAME, json=BASE)
    r = put(c, text(2))
    check("moments saved and given back", r.status_code == 200 and r.json()["moments"] == text(2), r.text)
    check("a scenario of two frames claims nothing", autos("moment-frames") == [])
    r = c.put(GAME, json=BASE | {"phases": ["ввід", "гравець"]})
    check("a form without moments leaves them be", r.json()["moments"] == text(2) and r.json()["phases"] == ["ввід", "гравець"], r.text)
    r = put(c, "⬛ " * 10_001)
    check("over 20 000 characters → 422 in words", r.status_code == 422 and "20 000" in r.json()["detail"]
          and c.get(GAME).json()["moments"] == text(2), r.text)

    put(c, text(3))
    a = autos("moment-frames")
    check("three frames → one claim of the game as a whole", len(a) == 1 and a[0]["part"] == "" and a[0]["rule"] == "", a)
    check("its price: 🌱 1", wood() == 1, wood())
    put(c, text(3, 1, 4, 5))
    check("three scenarios of 3+ → three claims, the first kept", len(autos("moment-frames")) == 3 and a[0]["id"] in {x["id"] for x in autos("moment-frames")})
    check("price by the steps [[2, 1], [5, 0.5], …]: 1 + 1 + ½", wood() == 2.5, wood())
    put(c, text(3, 2))
    check("a scenario gone → its claim gone", [x["id"] for x in autos("moment-frames")] == [a[0]["id"]])
    rows = c.get(H, params={"limit": 100}).json()
    labels = {f["label"] for x in rows if x["what"] == "гра" for f in x["fields"]}
    check("history: «як це грається»", "як це грається" in labels, labels)

    lvl = c.post(PARTS, json={"kind": "level", "title": "Рівень 1", "props": {"mode": "hand", "map": "⬛ ⬛ ⬛\n⬛ 😎 🏁  \n"}}).json()
    check("a level keeps its map, trailing spaces and the last newline trimmed", lvl["props"] == {"mode": "hand", "map": "⬛ ⬛ ⬛\n⬛ 😎 🏁"}, lvl)
    m = autos("level-map-drawn")
    check("a level with a map → a claim on it", len(m) == 1 and m[0]["part"] == lvl["id"], m)
    check("its price: ½ 🌱 more", wood() == 1.5, wood())
    r = c.put(f"{PARTS}/{lvl['id']}", json={"title": "Рівень 1", "props": {"mode": "hand", "map": "⬛" * 4001}})
    check("a map over 4 000 characters → 422", r.status_code == 422 and "4 000" in r.json()["detail"], r.text)
    r = c.put(f"{PARTS}/{lvl['id']}", json={"title": "Рівень 1", "props": {"mode": "hand", "map": "  \n "}})
    check("the map wiped → no map, the claim gone", r.json()["props"] == {"mode": "hand"} and autos("level-map-drawn") == [], r.text)
    two = [c.post(PARTS, json={"kind": "level", "title": f"Р{i}", "props": {"map": "🟩"}}).json() for i in range(4)]
    check("four maps → four claims, ½ × (1 + 1 + 1 + ½)", len(autos("level-map-drawn")) == 4 and wood() == 1 + 1.75, wood())
    c.delete(f"{PARTS}/{two[0]['id']}")
    check("a level deleted → its claim with it", len(autos("level-map-drawn")) == 3)
    r = c.post("/api/my/claims", json={"task": "level-map-drawn", "part": two[1]["id"]})
    check("by hand → 422: what is drawn claims itself", r.status_code == 422 and "заявляється сама" in r.json()["detail"], r.text)

    mongo[DB].tasks.update_one({"slug": "moment-frames"}, {"$set": {"status": "archived"}})
    put(c, text(3, 3))
    check("a card the catalog has not → nothing claimed, the old one goes", autos("moment-frames") == [])

ok = sum(results)
print(f"\n{ok}/{len(results)} PASS")
sys.exit(0 if ok == len(results) else 1)
