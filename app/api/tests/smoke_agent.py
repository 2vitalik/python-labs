"""Smoke: AI agents in the guide (T153) and the catalog (T155) — a token opens these routes and nothing else, the edit
is the agent's in history, the footprint is kept, no token configured = no way in. Run from app/api:
DB_NAME=python_labs_smoke uv run python tests/smoke_agent.py"""
import os
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
settings.agent_tokens = "claude:tok-claude, codex:tok-codex, nobody:"
CLAUDE, CODEX = ({"Authorization": f"Bearer tok-{n}"} for n in ("claude", "codex"))


def check(name, cond, extra=""):
    results.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def login(c, email, status):
    settings.fake_user_email = email
    c.get("/api/auth/dev-login")
    mongo[DB].users.update_one({"email": email}, {"$set": {"status": status}})


with TestClient(main.app) as c:
    bad = ("Bearer nope", "Bearer ", "Bearer", "Basic tok-claude", "tok-claude", "")
    check("no token, wrong, empty, not Bearer → 401",
          all(c.get("/api/guide/history", headers={"Authorization": h}).status_code == 401 for h in bad))
    check("… and the page as a guest gets it: no drafts", "public" not in c.get("/api/guide/game", headers={"Authorization": bad[0]}).json())
    check("token: list, page, history", all(c.get(f"/api/guide{p}", headers=CLAUDE).status_code == 200 for p in ("", "/game", "/history")))

    g = c.get("/api/guide/game", headers=CLAUDE).json()
    check("token: the text with drafts", "public" in g)
    edit = {"title": g["title"], "body": g["body"] + "\n\nрядок агента", "rev": g["rev"], "note": "додав рядок", "section": "Кінець"}
    r = c.put("/api/guide/game", json=edit, headers=CLAUDE)
    check("PUT: rev 1, updated by claude", r.status_code == 200 and r.json()["rev"] == 1 and r.json()["updated_by"] == "claude", r.text)
    check("stale rev → 409", c.put("/api/guide/game", json=edit, headers=CLAUDE).status_code == 409)
    h = c.get("/api/guide/history?slug=game", headers=CLAUDE).json()[0]
    check("history: actor claude, note, old → new", h["actor"] == "claude" and h["note"] == "додав рядок" and h["old"] == g["body"])
    check("history row keeps the full name", mongo[DB].history.count_documents({"coll": "guide", "actor": "claude@agent"}) == 2)
    d = c.get("/api/guide/changes-draft", headers=CLAUDE).json()
    check("draft line from the note", "Ігри › Кінець: додав рядок" in d["body"], d["body"])
    r = c.put("/api/guide/lab1", json={"title": "Лаба 1", "body": "текст codex", "rev": 0}, headers=CODEX)
    check("second agent: its own name", r.status_code == 200 and r.json()["updated_by"] == "codex", r.text)

    closed = [c.get(p, headers=CLAUDE).status_code for p in ("/api/students", "/api/activity", "/api/refs", "/api/my/game")]
    check("token opens nothing but the guide and the catalog", closed == [401] * 4, closed)
    r = c.post("/api/guide/changes/publish", json={"line": d["body"].split("\n")[0]}, headers=CLAUDE)
    check("publish stays the admin's", r.status_code == 401 and "додав рядок" in c.get("/api/guide/changes-draft", headers=CLAUDE).json()["body"])
    check("no agent in users", mongo[DB].users.count_documents({"email": {"$regex": "@agent$"}}) == 0)
    rows = list(mongo[DB].activity.find({"user": "claude@agent", "kind": "api"}))
    check("footprint: the agent's calls, the PUT among them",
          any(a["method"] == "PUT" and a["path"] == "/api/guide/game" and a["status"] == 200 for a in rows), len(rows))
    check("footprint: a wrong token leaves no row", mongo[DB].activity.count_documents({"user": ""}) == 0)

    card = {"slug": "agent-card", "title": "Картка агента", "zone": "code", "subzone": "git", "coin": "tin"}
    r = c.post("/api/tasks", json=card, headers=CLAUDE)
    check("catalog: the agent adds a card, a draft", r.status_code == 200 and r.json()["status"] == "draft", r.text)
    slugs = lambda headers: [t["slug"] for t in c.get("/api/tasks", headers=headers).json()]  # noqa: E731
    check("catalog: the agent sees drafts, a guest does not", "agent-card" in slugs(CLAUDE) and "agent-card" not in slugs({}))
    r = c.put(f"/api/tasks/{r.json()['id']}", json=card | {"coin": "silver", "status": "active"}, headers=CODEX)
    check("catalog: the agent edits a card", r.status_code == 200 and r.json()["coin"] == "silver", r.text)
    h = list(mongo[DB].history.find({"coll": "tasks"}).sort("at", 1))
    check("catalog: history names the agents", [x["actor"] for x in h] == ["claude@agent", "codex@agent"]
          and h[1]["changes"]["coin"] == {"old": "tin", "new": "silver"}, h)
    check("catalog: a bad card → 422", c.post("/api/tasks", json=card | {"slug": "x", "zone": "nope"}, headers=CLAUDE).status_code == 422)
    r = c.post("/api/games", json={"slug": "agent-game", "title": "Гра агента", "description": "рядок 1\n\nрядок 2"}, headers=CLAUDE)
    check("catalog: games too", r.status_code == 200 and mongo[DB].history.count_documents({"coll": "games", "actor": "claude@agent"}) == 1, r.text)
    y = c.get("/api/catalog/snapshot", headers=CLAUDE)
    check("snapshot: both files, the cards in them", y.status_code == 200 and set(y.json()) == {"games.yaml", "tasks.yaml"}
          and "agent-card: 🥈 Картка агента" in y.json()["tasks.yaml"] and "slug: agent-game" in y.json()["games.yaml"], y.text[:300])
    check("snapshot: not for a guest", c.get("/api/catalog/snapshot").status_code == 401)

    login(c, "stud@nure.ua", "student")
    check("student: no card edits, no snapshot", c.post("/api/tasks", json=card | {"slug": "y"}).status_code == 403
          and c.get("/api/catalog/snapshot").status_code == 403)
    check("student's session: no drafts, no history", "public" not in c.get("/api/guide/game").json()
          and c.get("/api/guide/history").status_code == 403)
    check("student with a token: the agent", "public" in c.get("/api/guide/game", headers=CLAUDE).json())
    login(c, "admin@nure.ua", "admin")
    g = c.get("/api/guide/game").json()
    r = c.put("/api/guide/game", json={"title": g["title"], "body": g["body"] + "!", "rev": g["rev"]})
    check("admin's session edits as before", r.status_code == 200 and r.json()["updated_by"] == "admin", r.text)
    who = lambda q: {r["user"] for r in c.get(f"/api/activity?src=edit{q}").json()["rows"]}  # noqa: E731
    check("activity: agents hidden with the staff", not who("") & {"claude@agent", "codex@agent"}, who(""))
    check("activity: shown with «і викладачі»", {"claude@agent", "codex@agent"} <= who("&staff=true"), who("&staff=true"))

    c.cookies.clear()
    settings.agent_tokens = ""
    check("no tokens configured → 401", c.get("/api/guide/history", headers=CLAUDE).status_code == 401)
    check("… and an empty token too", c.get("/api/guide/history", headers={"Authorization": "Bearer "}).status_code == 401)

ok = sum(1 for _, p in results if p)
print(f"\n{ok}/{len(results)} PASS")
sys.exit(0 if ok == len(results) else 1)
