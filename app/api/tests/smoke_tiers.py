"""Smoke: repeats and a falling price (T291 §13) — a card's `tiers` (cleaning, the cap they set), the price of the n-th claim,
claimed and accepted, a repeat with no place up to the cap, a card with no steps as before, tiers through export / import —
on a scratch DB. Run from app/api: DB_NAME=python_labs_tiers_smoke TG_BOT_TOKEN= UPLOADS_DIR=... uv run python tests/smoke_tiers.py"""
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, os.getcwd())
from pymongo import MongoClient  # noqa: E402

DB = os.environ["DB_NAME"]
assert DB.endswith("_smoke"), "refuse to run on a non-smoke DB"
mongo = MongoClient()
mongo.drop_database(DB)
subprocess.run(["uv", "run", "python", "catalog_io.py", "import"], check=True, capture_output=True)

from fastapi.testclient import TestClient  # noqa: E402

import catalog_io  # noqa: E402
import main  # noqa: E402
from core.config import settings  # noqa: E402
from pricing import factor, worth  # noqa: E402

CLAIMS = "/api/my/claims"
STEPS = [[3, 1], [10, 0.5], [0, 0.25]]
IO = "import asyncio, sys, pathlib, catalog_io; catalog_io.CATALOG = pathlib.Path(sys.argv.pop(1)); asyncio.run(catalog_io.main())"
results = []


def check(name, cond, extra=""):
    results.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def login(c, email, status):
    settings.fake_user_email = email
    c.get("/api/auth/dev-login")
    mongo[DB].users.update_one({"email": email}, {"$set": {"status": status, "group": "ПЗПІ-25-1"}})


def put_card(c, slug, **kw):
    t = next(x for x in c.get("/api/tasks").json() if x["slug"] == slug)
    return c.put(f"/api/tasks/{t['id']}", json={k: v for k, v in t.items() if k != "tiers"} | kw)


def card(slug):
    return mongo[DB].tasks.find_one({"slug": slug})


def io(folder, cmd):
    return subprocess.run([sys.executable, "-c", IO, str(folder), cmd], capture_output=True, text=True)


def card_of(tiers=(), max_count=1):
    return SimpleNamespace(tiers=list(tiers), max_count=max_count)


check("price: 12 claims of [[3,1],[10,0.5],[0,0.25]] → 3 + 3.5 + 0.5 = 7", worth(card_of(STEPS), 12) == 7)
check("price: the 3rd full, the 4th and the 10th a half, the 11th a quarter",
      [factor(card_of(STEPS), n) for n in (3, 4, 10, 11, 100)] == [1, 0.5, 0.5, 0.25, 0.25])
check("price: past the last upto — nothing", worth(card_of([[2, 1], [4, 0.5]]), 9) == 3 and factor(card_of([[2, 1], [4, 0.5]]), 5) == 0)
check("price: no steps — max_count as before", (worth(card_of(), 3), worth(card_of(max_count=5), 7), worth(card_of(max_count=0), 7)) == (1, 5, 7))
check("price: no claims — 0", worth(card_of(STEPS), 0) == 0)

with TestClient(main.app) as c:
    check("the repo's catalog has steps on the two drawn cards only",
          not mongo[DB].tasks.find_one({"tiers": {"$ne": []}, "slug": {"$nin": ["moment-frames", "level-map-drawn"]}}))
    login(c, "admin@nure.ua", "admin")
    for bad in ([[3, 1], [2, 0.5]], [[0, 1], [5, 0.5]], [[3, 1], [10, 1.5]], [[3, 0.5], [10, 1]], [[3, 0]], [[3.5, 1]],
                [[3, "x"]], [[3]], [3, 1], [[-1, 1]], [[True, 1]]):
        r = put_card(c, "save-game", tiers=bad)
        check(f"PUT tiers {bad} → 422 in words", r.status_code == 422 and r.json()["detail"].startswith("Сходинки ціни")
              and card("save-game")["tiers"] == [], r.text)
    r = put_card(c, "save-game", tiers=[[3, 1.0], [10, 0.5], [0, 0.25]], max_count=1)
    check("PUT tiers: kept, max_count from the last step (0 — no cap)",
          r.status_code == 200 and r.json()["tiers"] == STEPS and r.json()["max_count"] == 0 and card("save-game")["max_count"] == 0, r.text)
    r = put_card(c, "save-game", max_count=1)
    check("PUT without tiers: the steps stay, and the cap with them", r.json()["tiers"] == STEPS and r.json()["max_count"] == 0, r.text)
    check("GET /api/tasks: tiers", next(t for t in c.get("/api/tasks").json() if t["slug"] == "save-game")["tiers"] == STEPS)
    r = put_card(c, "status-panel", tiers=[[2, 1], [4, 0.5]])
    check("PUT tiers with an end: max_count = the last upto", r.json()["max_count"] == 4, r.text)
    r = put_card(c, "gui-render", tiers=[[0, 0.5]])
    check("PUT one step with no end", r.status_code == 200 and r.json()["tiers"] == [[0, 0.5]] and r.json()["max_count"] == 0, r.text)
    put_card(c, "console-render", tiers=[[2, 1]])
    r = put_card(c, "console-render", tiers=[], max_count=1)
    check("PUT tiers []: the steps gone, max_count as sent", r.json()["tiers"] == [] and r.json()["max_count"] == 1, r.text)

    snap = c.get("/api/catalog/snapshot").json()["tasks.yaml"]
    check("snapshot: tiers on one line", "tiers: [[3, 1], [10, 0.5], [0, 0.25]]\n" in snap and "tiers: [[2, 1], [4, 0.5]]\n" in snap, snap[:300])

    login(c, "stud@nure.ua", "student")
    c.post("/api/my/game", json={"title": "Сходинки", "base_custom": "своя"})

    def claim(**kw):
        r = c.post(CLAIMS, json=kw)
        return r.status_code if r.status_code == 200 else r.json()["detail"]

    def coins(key="claimed"):
        return c.get("/api/students/stud/game").json()["coins"][key]

    ids = [c.post(CLAIMS, json={"task": "save-game"}).json()["id"] for _ in range(12)]
    check("no cap: 12 claims with no place", all(ids) and mongo[DB].claims.count_documents({"task": "save-game"}) == 12)
    check("claimed: 12 → 7 silver", coins().get("silver") == 7, coins())
    p = c.get("/api/students/stud/game").json()
    check("passport: the card's tiers", p["tasks"]["save-game"]["tiers"] == STEPS and p["tasks"]["save-game"]["max_count"] == 0)

    check("with a cap: four with no place", [claim(task="status-panel") for _ in range(4)] == [200] * 4)
    over = claim(task="status-panel")
    check("…the fifth → 409 in words", over == "Цю картку вже заявлено 4 рази — більше не зараховується.", over)
    check("claimed: 2 + 2 × ½ = 3 tin", coins().get("tin") == 3, coins())

    check("no steps, once: a second with no place → 409 as before",
          claim(task="player-death") == 200 and claim(task="player-death") == "Така заявка вже є серед заявок гри.")
    check("no steps, 🔁5: five with no place, the sixth → 409", [claim(task="extra-level") for _ in range(5)] == [200] * 5
          and claim(task="extra-level") == "Цю картку вже заявлено 5 разів — більше не зараховується.")
    check("no steps: each in full", coins().get("wood") == 6, coins())

    fld = c.post("/api/my/game/parts", json={"kind": "field"}).json()
    first, second = (c.post(CLAIMS, json={"task": "gui-render"}).json() for _ in range(2))
    check("a field card with repeats: the first onto the field, a repeat at game level", first["part"] == fld["id"] and second["part"] == "",
          (first, second))
    check("…a repeat on the same place → 409", claim(task="gui-render", part=fld["id"]) == "Така заявка вже є.")
    check("…the field card's price: ½ + ½ = 1 silver more", coins().get("silver") == 8, coins())
    r = c.put(f"{CLAIMS}/{first['id']}", json={"part": ""})
    check("moving a claim off its place: one more repeat with no place", r.status_code == 200 and r.json()["part"] == "", r.text)

    login(c, "admin@nure.ua", "admin")
    for cid in ids[:4]:
        c.put(f"/api/students/stud/claims/{cid}", json={"status": "accepted"})
    check("accepted: 4 of 12 take the dearest places → 3 + ½", coins("accepted").get("silver") == 3.5, coins("accepted"))
    me = next(r for r in c.get("/api/students").json() if r.get("game", {}).get("title") == "Сходинки")
    check("the students' table: the same coins, 🌱 by them", me["game"]["coins"].get("silver") == 8
          and me["game"]["coins_accepted"]["silver"] == 3.5 and me["game"]["wood_accepted"] == 28, me["game"])

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        out = io(tmp, "export")
        text = (tmp / "tasks.yaml").read_text()
        check("export: tiers on one line, a card without them has none", out.returncode == 0
              and "tiers: [[3, 1], [10, 0.5], [0, 0.25]]\n" in text and text.count("tiers:") == 5, out.stderr[-300:])
        again = io(tmp, "import")
        check("export → import: nothing changes", again.returncode == 0 and "оновлено 0" in again.stdout, again.stdout + again.stderr[-300:])
        (tmp / "tasks.yaml").write_text(text.replace("tiers: [[3, 1], [10, 0.5], [0, 0.25]]", "tiers: [[5, 1], [8, 0.5]]"))
        out = io(tmp, "import")
        check("import: new steps and the cap they say", out.returncode == 0 and card("save-game")["tiers"] == [[5, 1], [8, 0.5]]
              and card("save-game")["max_count"] == 8, out.stdout + out.stderr[-300:])
        (tmp / "tasks.yaml").write_text(re.sub(r"\n *tiers: \[\[2, 1\], \[4, 0\.5\]\]", "", text))
        out = io(tmp, "import")
        check("import: a card that lost its tiers → []", out.returncode == 0 and card("status-panel")["tiers"] == [], out.stderr[-300:])
        (tmp / "tasks.yaml").write_text(text.replace("tiers: [[3, 1], [10, 0.5], [0, 0.25]]", "tiers: [[5, 1], [3, 0.5]]"))
        out = io(tmp, "import")
        check("import: bad steps stop it in words", out.returncode != 0 and "save-game" in out.stderr and "Сходинки ціни" in out.stderr
              and card("save-game")["tiers"] == STEPS, out.stderr[-300:])  # the file before it put the steps back
    check("the repo's tasks.yaml untouched", (catalog_io.CATALOG / "tasks.yaml").read_text().count("tiers:") == 2)

ok = sum(results)
print(f"\n{ok}/{len(results)} PASS")
sys.exit(0 if ok == len(results) else 1)
