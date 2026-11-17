"""Smoke: the videos of «Супровід» (T318) — the fixed rows of a game, a link and its versions, the deadline of a demo,
a gold card's row, the teacher's word, the lists of students, the game's history — on a scratch DB.
Run from app/api: DB_NAME=python_labs_videos_smoke TG_BOT_TOKEN= UPLOADS_DIR=... uv run python tests/smoke_videos.py"""
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone

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

GAME, V, WORD = "/api/students/stud/game", "/api/my/game/videos", "/api/students/stud/videos"
results = []


def check(name, cond, extra=""):
    results.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def login(c, email, status):
    settings.fake_user_email = email
    c.get("/api/auth/dev-login")
    mongo[DB].users.update_one({"email": email}, {"$set": {"status": status, "group": "ПЗПІ-25-1"}})


def rows(c):
    return {v["slot"]: v for v in c.get(GAME).json()["videos"]}


with TestClient(main.app) as c:
    login(c, "admin@nure.ua", "admin")
    gold = next(t for t in c.get("/api/tasks").json() if t["coin"] == "gold" and t["kind"] == "game" and not t["slots"] and t["status"] == "active")
    now = datetime.now(timezone.utc)
    mongo[DB].deadlines.insert_many([{"lab": 3, "at": now + timedelta(days=7), "groups": []}, {"lab": 4, "at": now - timedelta(days=1), "groups": []}])

    login(c, "stud@nure.ua", "student")
    c.post("/api/my/game", json={"title": "Привиди", "base_game": "sokoban"})
    r = c.get(GAME).json()["videos"]
    check("a new game: two demos and two defenses, in order, empty", [v["slot"] for v in r] == ["demo3", "demo4", "defense1", "defense2"]
          and all(v["versions"] == [] and v["need"] == "" and v["status"] == "claimed" for v in r), r)
    check("a demo knows its lab's deadline, a defense has none", r[0]["lab"] == 3 and r[0]["due"] and r[1]["due"] and r[2]["due"] is None and r[0]["on_time"] is None, r)

    r = c.put(f"{V}/demo3", json={"link": " youtu.be/abc "})
    check("a link: the scheme added, version 1, on time", r.status_code == 200 and r.json()["versions"][0]["link"] == "https://youtu.be/abc"
          and r.json()["versions"][0]["by"] == "stud" and r.json()["on_time"] is True, r.text)
    r = c.put(f"{V}/demo3", json={"link": "https://youtu.be/abc", "note": "  з   1:20 — бій з босом "})
    check("the same link again: its note, no new version", len(r.json()["versions"]) == 1 and r.json()["versions"][0]["note"] == "з 1:20 — бій з босом", r.text)
    r = c.put(f"{V}/demo3", json={"link": "https://drive.google.com/file/d/1/view"})
    check("another link: version 2, the first stays", [v["link"] for v in r.json()["versions"]] == ["https://youtu.be/abc", "https://drive.google.com/file/d/1/view"], r.text)
    r = c.put(f"{V}/demo4", json={"link": "https://loom.com/share/x"})
    check("a demo after its deadline: late", r.json()["on_time"] is False, r.text)
    mongo[DB].lab_marks.insert_one({"user": "stud@nure.ua", "lab": 4, "until": now + timedelta(days=3), "open": False, "reason": "", "note": "",
                                    "asked": False, "asked_for": "", "by": "admin@nure.ua"})
    check("the teacher moved the student's deadline: on time", rows(c)["demo4"]["on_time"] is True, rows(c)["demo4"])
    for bad in ("", "не посилання", "ftp://x.y/z", "https://nodot/x"):
        check(f"not a link «{bad}» → 422", c.put(f"{V}/defense1", json={"link": bad}).status_code == 422)
    check("an unknown row → 404", c.put(f"{V}/demo9", json={"link": "https://youtu.be/x"}).status_code == 404)
    slot = f"gold:{gold['slug']}"
    check("a gold card's row: none while the card is not claimed", slot not in rows(c) and c.put(f"{V}/{slot}", json={"link": "https://youtu.be/x"}).status_code == 404)
    c.post("/api/my/claims", json={"task": gold["slug"]})
    c.post("/api/my/claims", json={"task": "player-death"})
    r = rows(c)
    check("a gold card claimed: its row after the fixed ones, a cheaper card has none", list(r) == ["demo3", "demo4", "defense1", "defense2", slot]
          and r[slot]["kind"] == "gold" and r[slot]["task"] == gold["slug"], list(r))
    check("a gold card's video", c.put(f"{V}/{slot}", json={"link": "https://youtu.be/gold"}).json()["versions"][0]["link"] == "https://youtu.be/gold")
    check("the word is the teacher's → 403", c.put(f"{WORD}/defense1", json={"need": "skip"}).status_code == 403)

    c.post("/api/games/sokoban/sandbox")
    r = c.put(f"{V}/demo3", json={"link": "https://youtu.be/box"}, headers={"X-Sandbox": "sokoban"})
    check("the sandbox takes no videos → 422", r.status_code == 422 and len(rows(c)["demo3"]["versions"]) == 2, r.text)
    etalon = c.get("/api/games/sokoban/etalon").json()
    check("an etalon has no videos", "videos" not in etalon and etalon["game"], list(etalon))

    login(c, "admin@nure.ua", "admin")
    r = c.put(f"{WORD}/defense1", json={"need": "skip", "why": " був онлайн-захист "})
    check("the teacher: not wanted, with a line why — before any link", r.status_code == 200 and (r.json()["need"], r.json()["why"], r.json()["versions"]) == ("skip", "був онлайн-захист", []), r.text)
    r = c.put(f"{WORD}/{slot}", json={"need": "must"})
    check("the teacher: a gold card's video is a must; the link stays", r.json()["need"] == "must" and len(r.json()["versions"]) == 1, r.text)
    r = c.put(f"{WORD}/demo3", json={"status": "returned", "verdict": "звуку нема"})
    check("the teacher returns a demo: the need untouched", (r.json()["status"], r.json()["verdict"], r.json()["need"]) == ("returned", "звуку нема", ""), r.text)
    check("an unknown need or status → 422", c.put(f"{WORD}/demo3", json={"need": "maybe"}).status_code == 422
          and c.put(f"{WORD}/demo3", json={"status": "fine"}).status_code == 422)
    check("an unknown student or row → 404", c.put("/api/students/nobody/videos/demo3", json={"need": "must"}).status_code == 404
          and c.put(f"{WORD}/demo9", json={"need": "must"}).status_code == 404)
    r = c.put(f"{V}/defense2", json={"link": "https://youtu.be/byteacher"}, headers={"X-Game-Of": "stud"})
    check("the teacher gives a link in the student's stead: signed by the teacher", r.status_code == 200 and r.json()["versions"][0]["by"] == "admin", r.text)

    row = next(s for s in c.get("/api/students").json() if s["nick"] == "stud")["game"]
    check("the students' list: videos with a link wait for the teacher's word with the claims", row["waiting"] == 2 + 3, row["waiting"])  # 2 claims; demo4, defense2, gold
    me = row["videos"]
    check("the students' list: what is handed in, by row", set(me) == {"demo3", "demo4", "defense1", "defense2"} and me["demo3"]["n"] == 2
          and me["demo3"]["link"].startswith("https://drive") and me["demo3"]["at"] < me["demo3"]["last"] and me["demo3"]["status"] == "returned", me)
    check("the students' list: the teacher's word with no link yet", me["defense1"] == {"at": None, "last": None, "n": 0, "link": "", "status": "claimed", "need": "skip"}, me["defense1"])
    hist = [h for h in c.get(f"{GAME}/history").json() if h["what"] == "відео"]
    titles = {h["title"] for h in hist}
    check("history: the videos by their names", {"демка до лаби 3", "асинхронний захист 1", gold["title"]} <= titles, titles)
    newest = next(h for h in hist if h["title"] == "демка до лаби 3")
    check("history: the teacher's return, in words", newest["action"] == "returned" and newest["actor"]["role"] == "teacher"
          and {f["label"] for f in newest["fields"]} == {"стан", "коментар викладача"}, newest)
    second = next(h for h in hist if h["title"] == "демка до лаби 3" and any("версія 2" in (f["new"] or "") for f in h["fields"]))
    check("history: a new version says which", second["actor"]["nick"] == "stud", second)

ok = sum(results)
print(f"\n{ok}/{len(results)} PASS")
sys.exit(0 if ok == len(results) else 1)
