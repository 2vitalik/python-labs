"""Smoke: one game's history (T278 §12) — the game, its parts, rules and claims, the deleted ones too, with who made each
change and in words; the owner and the teacher read it, nobody else; pages by `before`; the sandbox leaves nothing — on a
scratch DB. Run from app/api: DB_NAME=python_labs_history_smoke TG_BOT_TOKEN= UPLOADS_DIR=... uv run python tests/smoke_game_history.py"""
import os
import subprocess
import sys
from datetime import datetime, timezone

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

PARTS, RULES, CLAIMS, H = "/api/my/game/parts", "/api/my/game/rules", "/api/my/claims", "/api/students/stud/game/history"
results = []


def check(name, cond, extra=""):
    results.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def login(c, email, status, group="ПЗПІ-25-1", last=""):
    settings.fake_user_email = email
    c.get("/api/auth/dev-login")
    mongo[DB].users.update_one({"email": email}, {"$set": {"status": status, "group": group, "last_name": last}})


def card(slug):
    return mongo[DB].tasks.find_one({"slug": slug})["title"]


def find(rows, what, action, title=None):
    return [r for r in rows if r["what"] == what and r["action"] == action and (title is None or r["title"] == title)]


with TestClient(main.app) as c:
    check("guest → 401", c.get(H).status_code == 401)
    login(c, "stud@nure.ua", "student", last="Студентенко")
    check("no game yet → []", c.get(H).json() == [])
    c.post("/api/my/game", json={"title": "Привиди", "base_game": "sokoban"})
    hero = c.post(PARTS, json={"kind": "entity", "title": "Герой", "role": "player"}).json()
    ghost = c.post(PARTS, json={"kind": "entity", "title": "Привид", "role": "enemy", "states": ["злий"]}).json()
    rule = c.post(RULES, json={"when": {"kind": "contact", "a": hero["id"], "b": ghost["id"]}, "then": [{"kind": "lose"}]}).json()
    death = c.post(CLAIMS, json={"task": "player-death", "rule": rule["id"]}).json()
    when = {"kind": "contact", "a": hero["id"], "b": ghost["id"]}
    scare = c.post(RULES, json={"when": when, "cond": [{"kind": "state", "a": "@a", "s": "злий", "not": True}], "then": [{"kind": "disappear", "a": "@b"}]}).json()
    c.put(f"{RULES}/{scare['id']}", json=scare | {"then": [{"kind": "disappear", "a": "@a"}]})
    c.put(f"{CLAIMS}/{death['id']}", json={"note": "смерть від привида"})
    c.put(f"{PARTS}/{ghost['id']}", json=ghost | {"title": "Привид-2", "description": "лякає"})
    c.put(f"{PARTS}/{hero['id']}", json=hero | {"order": 5})  # plumbing alone: no row
    win = c.post(PARTS, json={"kind": "window", "task": "main-menu", "title": "Головне меню"}).json()
    c.post(PARTS, json={"kind": "menu", "title": "Меню", "window": win["id"], "items": [{"title": "Нова гра", "window": win["id"]}]})
    field = c.post(PARTS, json={"kind": "field", "props": {"wrap": True, "size": "20×15"}}).json()
    c.put(f"{PARTS}/{field['id']}", json=field | {"props": {"wrap": True, "size": "30×20"}})
    c.put("/api/my/game", json={"title": "Привиди", "base_game": "sokoban", "phases": ["ввід", "гравець"]})
    spawn = c.post(CLAIMS, json={"task": "spawn-schedule", "params": {"every": 20, "max_alive": 4}}).json()
    quota = c.post(CLAIMS, json={"task": "collect-quota"}).json()
    check("delete the ghost: its rule and claims go with it", c.delete(f"{PARTS}/{ghost['id']}").status_code == 200
          and mongo[DB].rules.count_documents({}) == 0 and not mongo[DB].claims.find_one({"_id": ObjectId(death["id"])}))
    mine = c.get(H, params={"limit": 200}).json()
    check("the owner reads it", len(mine) > 10, len(mine))

    login(c, "admin@nure.ua", "admin", group="", last="Викладач")
    c.put(f"/api/students/stud/claims/{spawn['id']}", json={"status": "accepted", "verdict": "молодець"})
    c.put(f"/api/students/stud/claims/{quota['id']}", json={"status": "returned", "verdict": "де код?"})
    now = datetime.now(timezone.utc)
    mongo[DB].history.insert_many([  # the agent's and the script's ways in: nothing writes a game as them yet
        {"coll": "claims", "doc_id": ObjectId(spawn["id"]), "actor": "claude@agent", "at": now, "changes": {"note": {"old": "", "new": "код є"}}, "note": ""},
        {"coll": "claims", "doc_id": ObjectId(spawn["id"]), "actor": "auto-sync", "at": now, "changes": {"auto": {"old": False, "new": True}}, "note": ""},
    ])
    r = c.get(H, params={"limit": 200})
    rows = r.json()
    check("the teacher reads it", r.status_code == 200 and len(rows) == len(mine) + 3, f"{len(rows)} vs {len(mine)}")
    check("newest first", [x["at"] for x in rows] == sorted((x["at"] for x in rows), reverse=True))
    check("row shape", set(rows[0]) == {"id", "at", "actor", "coll", "what", "title", "action", "fields"}
          and set(rows[0]["actor"]) == {"nick", "name", "role"}, rows[0])
    by_role = {x["actor"]["nick"]: x["actor"] for x in rows}
    check("actors: student by name, teacher, agent", by_role["stud"] == {"nick": "stud", "name": "Студентенко", "role": "student"}
          and by_role["admin"]["role"] == "teacher" and by_role["claude"] == {"nick": "claude", "name": "claude", "role": "agent"}, by_role)
    check("a change of plumbing alone is no row: the hero's order, the script's auto flag",
          not find(rows, "сутність", "changed", "Герой") and "auto-sync" not in by_role)
    check("no plumbing among the fields", not {f["key"] for x in rows for f in x["fields"]} & {"game", "owner", "order", "kind", "auto"})

    g = find(rows, "гра", "added", "Привиди")
    base = mongo[DB].games.find_one({"slug": "sokoban"})["title"]
    check("game added: its base by name", g and {"key": "base_game", "label": "основа", "old": None, "new": base} in g[0]["fields"], g)
    g = find(rows, "гра", "changed", "Привиди")
    check("game changed: the tick order in words", g and g[0]["fields"] == [{"key": "phases", "label": "порядок тіку", "old": None, "new": "ввід → гравець"}], g)
    check("entity added: today's name of a deleted one is its last one", find(rows, "сутність", "added", "Привид-2") and find(rows, "сутність", "added", "Герой"))
    e = find(rows, "сутність", "changed", "Привид-2")
    check("entity renamed: назва and опис, old → new", e and {"key": "title", "label": "назва", "old": "Привид", "new": "Привид-2"} in e[0]["fields"]
          and {"key": "description", "label": "опис", "old": None, "new": "лякає"} in e[0]["fields"], e)
    e = find(rows, "сутність", "deleted", "Привид-2")
    check("entity deleted: by the student, with its last values", e and e[0]["actor"]["role"] == "student"
          and {"key": "states", "label": "стани", "old": "злий", "new": None} in e[0]["fields"], e)
    ru = find(rows, "правило", "added") + find(rows, "правило", "deleted")
    check("rules added and deleted: the sentence with the names", len(ru) == 4 and all(x["title"].startswith("КОЛИ") and "Герой" in x["title"]
          and "Привид-2" in x["title"] for x in ru), [x["title"] for x in ru])
    sc = [x for x in rows if x["what"] == "правило" and "злий" in x["title"]]
    clauses = {f["label"]: f for x in sc for f in x["fields"] if x["action"] == "added"}
    check("rule clauses alone, in the sentence's words: коли · якщо with its «не» · то", set(clauses) == {"коли", "якщо", "то"}
          and "не" in clauses["якщо"]["new"].split() and "злий" in clauses["якщо"]["new"]
          and not any(f["new"].startswith(("КОЛИ", "ЯКЩО", "ТО", "→")) for f in clauses.values()), clauses)
    ch = [x for x in sc if x["action"] == "changed"]
    check("rule changed: only ТО, old → new", ch and [f["label"] for f in ch[0]["fields"]] == ["то"]
          and ch[0]["fields"][0]["old"].startswith("зникає") and ch[0]["fields"][0]["new"].startswith("зникає")
          and ch[0]["fields"][0]["old"] != ch[0]["fields"][0]["new"], ch)
    dc = [x for x in rows if x["what"] == "заявка" and x["title"] == card("player-death")]
    check("claim on the rule: added, note changed, deleted", [x["action"] for x in dc] == ["deleted", "changed", "added"], [x["action"] for x in dc])
    check("claim note: one field", dc[1]["fields"] == [{"key": "note", "label": "нотатка", "old": None, "new": "смерть від привида"}], dc[1])
    check("claim added: its rule as a sentence", any(f["label"] == "правило" and f["new"].startswith("КОЛИ") for f in dc[2]["fields"]), dc[2])
    m = find(rows, "переходи", "added", "Головне меню")
    check("menu: named by its window, items in words", m and {"key": "items", "label": "переходи", "old": None, "new": "Нова гра → 🪟 Головне меню"} in m[0]["fields"], m)
    f = find(rows, "поле", "changed")
    check("field: only the property that changed", f and f[0]["fields"] == [{"key": "props", "label": "властивості", "old": "Розмір: 20×15", "new": "Розмір: 30×20"}], f)
    a = find(rows, "заявка", "accepted", card("spawn-schedule"))
    check("verdict accepted: the teacher, стан and коментар", a and a[0]["actor"]["role"] == "teacher"
          and {(x["label"], x["new"]) for x in a[0]["fields"]} == {("стан", "зараховано"), ("коментар викладача", "молодець")}, a)
    check("verdict returned", find(rows, "заявка", "returned", card("collect-quota"))[0]["actor"]["role"] == "teacher")
    check("the agent's row", rows[0]["actor"]["role"] == "agent" and rows[0]["fields"] == [{"key": "note", "label": "нотатка", "old": None, "new": "код є"}], rows[0])
    check("an auto-claim comes with its part: no row of its own", not find(rows, "заявка", "added", card("main-menu")))

    ids, before = [], None
    while True:
        page = c.get(H, params={"limit": 3} | ({"before": before} if before else {})).json()
        if not page:
            break
        ids += [x["id"] for x in page]
        before = page[-1]["at"]
    check("pages by `before`: the same rows, none twice", ids == [x["id"] for x in rows], f"{len(ids)} vs {len(rows)}")

    own, rest = c.get(H, params={"limit": 200, "who": "student"}).json(), c.get(H, params={"limit": 200, "who": "staff"}).json()
    check("who=student: the owner's rows only", own and {x["actor"]["role"] for x in own} == {"student"}, {x["actor"]["role"] for x in own})
    others = {x["actor"]["role"] for x in rows} - {"student"}
    check("who=staff: everyone but the owner", {"teacher", "agent"} <= others == {x["actor"]["role"] for x in rest}, {x["actor"]["role"] for x in rest})
    check("who: the two halves make the whole", len(own) + len(rest) == len(rows), f"{len(own)} + {len(rest)} vs {len(rows)}")
    check("who=staff pages too", [x["id"] for x in c.get(H, params={"limit": 1, "who": "staff"}).json()] == [rest[0]["id"]])
    check("who: an unknown value → 422", c.get(H, params={"who": "nobody"}).status_code == 422)

    check("view as the student: own history", c.post("/api/me/as/stud").status_code == 200 and len(c.get(H, params={"limit": 200}).json()) == len(rows))
    c.delete("/api/me/as")
    login(c, "stud2@nure.ua", "student", group="ПЗПІ-25-2")
    check("a fellow student sees the game, not its history → 403", c.get("/api/students/stud/game").status_code == 200 and c.get(H).status_code == 403)
    login(c, "stud3@nure.ua", "student", group="КІ-24-1")
    check("another stream → 404", c.get(H).status_code == 404)
    check("nobody by that nick → 404", c.get("/api/students/ghost/game/history").status_code == 404)

    login(c, "stud@nure.ua", "student", last="Студентенко")
    c.post("/api/games/sokoban/sandbox")
    c.post(PARTS, headers={"X-Sandbox": "sokoban"}, json={"kind": "entity", "title": "Пробний", "role": "enemy"})
    check("the sandbox leaves no row", len(c.get(H, params={"limit": 200}).json()) == len(rows))

ok = sum(results)
print(f"\n{ok}/{len(results)} PASS")
sys.exit(0 if ok == len(results) else 1)
