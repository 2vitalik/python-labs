"""Smoke: the ludopedia corpus in the site (T260) — the import from data/ludopedia, who sees what, the parsed shape,
the card → games lookup. Run from app/api: DB_NAME=python_labs_smoke uv run python tests/smoke_ludopedia.py"""
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
from core.config import settings  # noqa: E402

results = []
settings.agent_tokens = "claude:tok-claude"
CLAUDE = {"Authorization": "Bearer tok-claude"}
L = "/api/ludopedia"


def check(name, cond, extra=""):
    results.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def login(c, email, status):
    settings.fake_user_email = email
    c.get("/api/auth/dev-login")
    mongo[DB].users.update_one({"email": email}, {"$set": {"status": status}})


run = lambda: subprocess.run([sys.executable, "ludopedia_io.py", "import", "--prune"], capture_output=True, text=True)  # noqa: E731
out = run()
n = mongo[DB].ludo_games.count_documents({})
check("import: the corpus is in, one row per file", out.returncode == 0 and n >= 275 and "додано" in out.stdout, out.stdout[-300:] + out.stderr[-300:])
check("import again: nothing changes", "оновлено 0" in run().stdout and mongo[DB].ludo_games.count_documents({}) == n)

with TestClient(main.app) as c:
    check("guest: list and game closed, by-card and mechanics open", c.get(L).status_code == 401 and c.get(f"{L}/chips-challenge").status_code == 401
          and c.get(f"{L}/by-card/push-object").status_code == 200 and c.get(f"{L}/mechanics").status_code == 200)
    cards = c.get(f"{L}/by-card/push-object").json()
    check("by-card: Sokoban pushes, rows carry the ⭐ link", any(g["slug"] == "sokoban" for g in cards) and all(g["url"] for g in cards), cards[:2])
    check("by-card matches the `+tag` of files written before the card existed", c.get(f"{L}/by-card/undo-redo").json())
    rows = c.get(L, headers=CLAUDE).json()
    check("agent: the list, light rows", len(rows) == n and "sections" not in rows[0] and rows[0]["url"], rows[0])
    g = c.get(f"{L}/chips-challenge", headers=CLAUDE).json()
    check("a game: 13 sections, entities and rules parsed, best link first", len(g["sections"]) == 13 and len(g["entities"]) > 30
          and g["rules"][0]["when"] == ["contact(chip, ic)"] and g["url"] == "https://bitbusters.club/wiki/", {k: g[k] for k in ("url",)})
    check("unknown slug → 404", c.get(f"{L}/nope", headers=CLAUDE).status_code == 404)
    s = c.get(f"{L}/stats", headers=CLAUDE).json()
    check("stats: totals by family and class", s["total"] == n and s["families"]["maze-arcade"] >= 18 and s["klass"]["avatar"] > 0, s)
    login(c, "stud@nure.ua", "student")
    check("student: 403 on the list, by-card still open", c.get(L).status_code == 403 and c.get(f"{L}/by-card/push-object").status_code == 200)
    login(c, "admin@nure.ua", "admin")
    check("admin: sees the list", len(c.get(L).json()) == n)

ok = sum(1 for _, p in results if p)
print(f"\n{ok}/{len(results)} PASS")
sys.exit(0 if ok == len(results) else 1)
