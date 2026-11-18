"""Smoke: AI agents in the catalog (T155) — a token adds and edits cards and games, history names the agents, the snapshot;
the routes it does not open; the guide, the lists and the footprint are the platform's: core/api/tests/smoke_agent.py.
Run from app/api: DB_NAME=python_labs_agent_smoke ~/.venvs/python-labs/bin/python tests/smoke_agent.py"""
import os
import sys

sys.path.insert(0, os.getcwd())
import yaml  # noqa: E402
from pymongo import MongoClient  # noqa: E402

DB = os.environ["DB_NAME"]
assert DB.endswith("_smoke"), "refuse to run on a non-smoke DB"
mongo = MongoClient()
mongo.drop_database(DB)

from fastapi.testclient import TestClient  # noqa: E402

import main  # noqa: E402
from core.config import settings  # noqa: E402

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
    closed = [c.get(p, headers=CLAUDE).status_code for p in ("/api/refs", "/api/my/game")]
    check("token: no finds, no student's game", closed == [401] * 2, closed)

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
    grid = "Хід гравця\n\n```field\n⬛ ▫️ ⬛\n⬛[😎]⬛\n⬛(✨)⬛\n```"
    game = {"slug": "agent-game", "title": "Гра агента", "description": "рядок 1\n\nрядок 2", "examples": grid}
    r = c.post("/api/games", json=game, headers=CLAUDE)
    check("catalog: games too", r.status_code == 200 and mongo[DB].history.count_documents({"coll": "games", "actor": "claude@agent"}) == 1, r.text)
    check("game: examples kept and listed", r.json()["examples"] == grid and c.get("/api/games", headers=CLAUDE).json()[0]["examples"] == grid)
    r = c.put(f"/api/games/{r.json()['id']}", json=game | {"examples": grid + "\n\nДалі"}, headers=CLAUDE)
    h = mongo[DB].history.find_one({"coll": "games", "changes.examples.old": grid})
    check("game: an edit of examples alone is in history", r.status_code == 200 and h and list(h["changes"]) == ["examples"], h)
    y = c.get("/api/catalog/snapshot", headers=CLAUDE)
    check("snapshot: all five files, the cards in them", y.status_code == 200
          and set(y.json()) == {"games.yaml", "tasks.yaml", "aliases.yaml", "proof.yaml", "core.yaml"}
          and "agent-card: 🥈 Картка агента" in y.json()["tasks.yaml"] and "slug: agent-game" in y.json()["games.yaml"], y.text[:300])
    games = y.json()["games.yaml"]
    check("snapshot: texts line by line, read back the same", "  examples: |-\n    Хід гравця\n\n    ```field\n    ⬛ ▫️ ⬛\n    ⬛[😎]⬛\n" in games
          and yaml.safe_load(games)[0]["examples"] == grid + "\n\nДалі", games)
    check("snapshot: not for a guest", c.get("/api/catalog/snapshot").status_code == 401)

    login(c, "stud@nure.ua", "student")
    check("student: no card edits, no snapshot", c.post("/api/tasks", json=card | {"slug": "y"}).status_code == 403
          and c.get("/api/catalog/snapshot").status_code == 403)

ok = sum(1 for _, p in results if p)
print(f"\n{ok}/{len(results)} PASS")
sys.exit(0 if ok == len(results) else 1)
