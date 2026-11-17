"""Smoke: the core and the requests (T319, T321) — `core` from core.yaml, a card outside the core claimed with a line why,
the coins it waits with, the teacher's «Запити» (GET / PUT /api/asks, an agent's token), core.yaml through export / import and
`catalog_io.py core`, the page's features (Game.extras, the closed ones) — on a scratch DB. Run from app/api:
DB_NAME=python_labs_asks_smoke TG_BOT_TOKEN= UPLOADS_DIR=... uv run python tests/smoke_asks.py"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

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

import catalog_core  # noqa: E402
import catalog_io  # noqa: E402
import features  # noqa: E402
import main  # noqa: E402
from claims_clean import WHY  # noqa: E402
from core.config import settings  # noqa: E402

CLAIMS, ASKS, EXTRAS = "/api/my/claims", "/api/asks", "/api/my/game/extras"
WHY_OK = "  Гравець зберігає гру клавішею S і продовжує з того ж місця  "
IO = "import asyncio, sys, pathlib, catalog_io; catalog_io.CATALOG = pathlib.Path(sys.argv.pop(1)); asyncio.run(catalog_io.main())"
settings.agent_tokens = "claude:tok-claude"
AGENT = {"Authorization": "Bearer tok-claude"}
results = []


def check(name, cond, extra=""):
    results.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def login(c, email, status, test=False):
    settings.fake_user_email = email
    c.get("/api/auth/dev-login")
    db.users.update_one({"email": email}, {"$set": {"status": status, "group": "ПЗПІ-25-1", "test": test}})


def card(slug):
    return db.tasks.find_one({"slug": slug})


def put_card(c, slug, **kw):
    t = next(x for x in c.get("/api/tasks").json() if x["slug"] == slug)
    return c.put(f"/api/tasks/{t['id']}", json=t | kw)


def io(folder, cmd):
    return subprocess.run([sys.executable, "-c", IO, str(folder), cmd], capture_output=True, text=True)


core = catalog_core.slugs(catalog_io.CATALOG / "core.yaml")
check("import: core from core.yaml, the rest «за запитом»", db.tasks.count_documents({"core": True}) == len(core) > 100
      and card("game-pause")["core"] and not card("save-progress")["core"] and not card("lab1")["core"])

with TestClient(main.app) as c:
    tasks = {t["slug"]: t for t in c.get("/api/tasks").json()}
    check("GET /api/tasks: core", tasks["game-pause"]["core"] is True and tasks["save-progress"]["core"] is False)
    v = c.get("/api/vocab").json()
    check("vocab: features — all, closed by default, not free for a guest; no depth",
          v["features"] == {"all": list(features.EXTRAS), "closed": ["map", "moments"], "free": False} and "depth" not in v, v.get("features"))
    check("vocab: roles and stats say core", v["roles"]["player"]["core"] is True and v["roles"]["ally"]["core"] is False
          and next(s for s in v["stats"] if s["key"] == "hp")["core"] is True)

    login(c, "stud@nure.ua", "student")
    c.post("/api/my/game", json={"title": "Сейви", "base_custom": "своя"})
    check("a core card with no why → 200", c.post(CLAIMS, json={"task": "game-pause"}).status_code == 200)
    for why in (None, "", "   коротко   ", " " * 30):
        r = c.post(CLAIMS, json={"task": "save-progress"} | ({"why": why} if why is not None else {}))
        check(f"outside the core, why {why!r} → 422 in words", r.status_code == 422 and r.json()["detail"] == WHY, r.text)
    r = c.post(CLAIMS, json={"task": "save-progress", "why": WHY_OK})
    save = r.json()
    check("…with a line why → stored stripped", r.status_code == 200 and save["why"] == WHY_OK.strip(), r.text)
    r = c.post(CLAIMS, json={"task": "cheat-codes", "why": "я" * 700})
    check("…a long why cut at 600", r.status_code == 200 and len(r.json()["why"]) == 600, r.text)
    cheat = r.json()
    ent = c.post("/api/my/game/parts", json={"kind": "entity", "title": "Друг", "role": "ally"}).json()
    check("a role outside the core: the entity claims it with no why",
          db.claims.find_one({"task": "role-ally", "auto": True, "part": ent["id"]}) is not None)

    def coins():
        return c.get("/api/students/stud/game").json()["coins"]

    w = coins()
    check("coins: outside the core — asked, not claimed", w["claimed"] == {"wood": 1} and w["asked"] == {"tin": 2, "wood": 1}
          and w["accepted"] == {}, w)
    check("PUT why None → left as is", c.put(f"{CLAIMS}/{save['id']}", json={"note": "н"}).json()["why"] == WHY_OK.strip())
    r = c.put(f"{CLAIMS}/{save['id']}", json={"why": "мало"})
    check("PUT a short why → 422", r.status_code == 422 and r.json()["detail"] == WHY, r.text)
    r = c.put(f"{CLAIMS}/{save['id']}", json={"why": "Зберігання в JSON-файл після кожного рівня"})
    check("PUT a new why → stored", r.status_code == 200 and r.json()["why"].startswith("Зберігання"), r.text)
    hist = c.get("/api/students/stud/game/history").json()
    check("game log: the why is «пояснення»", any(f["label"] == "пояснення" for h in hist for f in h["fields"]), hist[:2])

    r = c.put(EXTRAS, json={"extras": ["levels", "nope"]})
    check("extras: an unknown one → 422", r.status_code == 422 and "nope" in r.json()["detail"], r.text)
    r = c.put(EXTRAS, json={"extras": ["levels", "map", "stats", "stats"]})
    check("extras: a closed one dropped for a student, the order the page's", r.json()["extras"] == ["stats", "levels"], r.text)

    login(c, "stud2@nure.ua", "student")
    c.post("/api/my/game", json={"title": "Двоє", "base_custom": "своя"})
    hot = c.post(CLAIMS, json={"task": "hot-seat", "why": "Двоє гравців по черзі за одним ноутбуком"}).json()
    c.post(CLAIMS, json={"task": "shop-sales", "why": "Знижки в магазині між рівнями щоп'ятниці"})
    c.post(CLAIMS, json={"task": "local-two-players", "why": "Другий гравець на стрілках, перший на WASD"})
    hero = c.post("/api/my/game/parts", json={"kind": "entity", "title": "Привид", "role": "enemy"}).json()["id"]
    beam = c.post(CLAIMS, json={"task": "beam-tracing", "part": hero, "why": "Привид стріляє променем до першої стіни"}).json()
    rule = c.post("/api/my/game/rules", json={"when": {"kind": "contact", "a": hero, "b": hero}, "then": [{"kind": "win"}]}).json()["id"]
    c.post(CLAIMS, json={"task": "enemy-reached-base", "rule": rule, "why": "Привид дійшов до бази — гравець програв"})
    login(c, "tester@nure.ua", "student", test=True)
    c.post("/api/my/game", json={"title": "Тест", "base_custom": "своя"})
    c.post(CLAIMS, json={"task": "hot-seat", "why": "Тестовий студент теж просить картку"})
    login(c, "stud@nure.ua", "student")
    c.post(CLAIMS, json={"task": "shop-sales", "why": "Магазин зі знижками після кожного боса"})

    login(c, "admin@nure.ua", "admin")
    c.get("/api/games/sokoban/etalon")
    c.post("/api/games/sokoban/sandbox")
    r = c.post(CLAIMS, json={"task": "hot-seat"}, headers={"X-Sandbox": "sokoban"})
    check("a sandbox claims outside the core with no why", r.status_code == 200, r.text)
    r = c.post(CLAIMS, json={"task": "shop-buyback"}, headers={"X-Game-Of": "stud"})
    check("the teacher in a student's game: no why needed", r.status_code == 200, r.text)
    r = c.put(EXTRAS, json={"extras": ["map", "stats", "levels"]}, headers={"X-Game-Of": "stud"})
    check("extras: the teacher adds a closed one", r.json()["extras"] == ["stats", "levels", "map"], r.text)

    asks = c.get(ASKS).json()
    by = {g["task"]["slug"]: g for g in asks}
    check("asks: by card, the most asked first", asks[0]["task"]["slug"] == "shop-sales" and by["shop-sales"]["games"] == 2
          and [g["games"] for g in asks] == sorted((g["games"] for g in asks), reverse=True), [(g["task"]["slug"], g["games"]) for g in asks])
    check("asks: the card's fields", set(by["shop-sales"]["task"]) == {"slug", "title", "icon", "zone", "subzone", "kind", "coin",
                                                                       "amount", "description"}, by["shop-sales"]["task"])
    rows = [r for g in asks for r in g["claims"]]
    check("asks: no etalon, no sandbox, no core card", all(r["nick"] in ("stud", "stud2", "tester") for r in rows)
          and "game-pause" not in by and "hot-seat" in by, [r["nick"] for r in rows])
    check("asks: a test student listed, not counted", by["hot-seat"]["games"] == 1
          and sorted(r["test"] for r in by["hot-seat"]["claims"]) == [False, True], by["hot-seat"])
    row = next(r for r in by["hot-seat"]["claims"] if r["nick"] == "stud2")
    check("asks: a row", {k: row[k] for k in ("id", "nick", "game", "where", "anchor", "status", "auto")} == {
        "id": hot["id"], "nick": "stud2", "game": "Двоє", "where": "", "anchor": f"c-{hot['id']}", "status": "claimed", "auto": False}
        and row["why"].startswith("Двоє") and set(row) >= {"name", "params", "note", "link", "shots", "verdict", "created_at"}, row)
    check("asks: where — an entity, a rule", by["beam-tracing"]["claims"][0]["where"] == "сутність «Привид»"
          and by["enemy-reached-base"]["claims"][0]["where"].startswith("правило «КОЛИ"), by["enemy-reached-base"]["claims"][0]["where"])
    check("asks: a role by the description — auto, no why", by["role-ally"]["claims"][0]["auto"] is True)
    check("asks: a request waiting for the teacher's word is listed", "save-progress" in by)
    check("asks: an agent's token reads them", c.get(ASKS, headers=AGENT).json() == asks)

    r = c.put(f"{ASKS}/{save['id']}", json={"status": "accepted", "verdict": "  Так, зараховую  "})
    check("PUT asks: accept with a line", r.status_code == 200 and (r.json()["status"], r.json()["verdict"]) == ("accepted", "Так, зараховую"), r.text)
    check("…the student hears it", db.events.count_documents({"kind": "claim", "user": "stud@nure.ua", "text": {"$regex": "зараховано"}}) == 1)
    check("…gone from the requests", "save-progress" not in {g["task"]["slug"] for g in c.get(ASKS).json()})
    w = coins()
    check("coins: an accepted request counts as claimed", w["claimed"] == {"wood": 1, "tin": 1} and w["accepted"] == {"tin": 1}
          and w["asked"] == {"tin": 3, "wood": 1}, w)
    me = next(x["game"] for x in c.get("/api/students").json() if x.get("game", {}).get("title") == "Сейви")
    check("students' table: asked — the claims waiting outside the core", me["asked"] == 4 and me["coins"] == {"wood": 1, "tin": 1}, me)

    r = put_card(c, "cheat-codes", core=True)
    check("PUT /api/tasks core: true", r.status_code == 200 and r.json()["core"] is True, r.text)
    check("…its claims count as claimed", coins()["claimed"] == {"wood": 1, "tin": 2} and coins()["asked"] == {"tin": 2, "wood": 1}, coins())
    t = next(x for x in c.get("/api/tasks").json() if x["slug"] == "cheat-codes")
    r = c.put(f"/api/tasks/{t['id']}", json={k: v for k, v in t.items() if k != "core"} | {"title": "Чіт-коди"})
    check("PUT /api/tasks with no core: left as is", r.json()["core"] is True and r.json()["title"] == "Чіт-коди", r.text)
    check("…the core in the card's history", db.history.find_one({"coll": "tasks", "changes.core": {"old": False, "new": True}}))

    r = c.put(f"{ASKS}/{row['id']}", json={"status": "returned", "verdict": "Це вже є: «Двоє за одним»"})
    check("PUT asks: return", r.json()["status"] == "returned", r.text)
    check("…a returned one stays listed with its status",
          next(x for g in c.get(ASKS).json() for x in g["claims"] if x["id"] == row["id"])["status"] == "returned")
    r = c.put(f"{ASKS}/{row['id']}", json={"task": "time-out"})
    check("PUT asks: to a card of another kind → 422", r.status_code == 422 and "того самого типу" in r.json()["detail"], r.text)
    r = c.put(f"{ASKS}/{row['id']}", json={"task": "local-two-players"})
    check("PUT asks: to a card the game has already → 409", r.status_code == 409, r.text)
    r = c.put(f"{ASKS}/{row['id']}", json={"task": "online-multiplayer"})
    check("PUT asks: moved to a card of the same kind", r.status_code == 200 and r.json()["task"] == "online-multiplayer"
          and db.claims.find_one({"_id": ObjectId(row["id"])})["task"] == "online-multiplayer", r.text)
    auto = by["role-ally"]["claims"][0]["id"]
    check("PUT asks: a role's claim is not moved", c.put(f"{ASKS}/{auto}", json={"task": "role-boss"}).status_code == 422)
    check("PUT asks: a bad status → 422", c.put(f"{ASKS}/{beam['id']}", json={"status": "nope"}).status_code == 422)
    pause = next(x for x in c.get("/api/students/stud/game").json()["claims"] if x["task"] == "game-pause")
    check("PUT asks: a core card's claim → 404", c.put(f"{ASKS}/{pause['id']}", json={"verdict": "x"}).status_code == 404)
    check("PUT asks: an agent answers", c.put(f"{ASKS}/{beam['id']}", json={"verdict": "Добре"}, headers=AGENT).json()["verdict"] == "Добре")

    r = c.put("/api/features", json={"closed": ["nope"]})
    check("PUT features: an unknown one → 422", r.status_code == 422, r.text)
    r = c.put("/api/features", json={"closed": ["moments", "map", "map", "cards"]})
    check("PUT features: stored in the page's order", r.json() == {"closed": ["map", "moments", "cards"]}, r.text)
    check("vocab: the closed ones; the teacher is free", c.get("/api/vocab").json()["features"]["closed"] == ["map", "moments", "cards"]
          and c.get("/api/vocab").json()["features"]["free"] is True)
    c.put("/api/features", json={"closed": ["map", "moments"]})

    login(c, "stud@nure.ua", "student")
    check("a student: no asks, no features", c.get(ASKS).status_code == 403 and c.put(f"{ASKS}/{beam['id']}", json={}).status_code == 403
          and c.put("/api/features", json={"closed": []}).status_code == 403)
    r = c.put(EXTRAS, json={"extras": ["map", "moments", "stats"]})
    check("extras: a closed one the game had stays, a new closed one is dropped", r.json()["extras"] == ["stats", "map"], r.text)
    hist = c.get("/api/students/stud/game/history").json()
    check("game log: «можливості» in words", any(f["label"] == "можливості" and "мапа рівня клітинками" in (f["new"] or "")
                                                 for h in hist for f in h["fields"]), [h["fields"] for h in hist[:2]])
    check("guest: asks → 401", TestClient(main.app).get(ASKS).status_code == 401)

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        io(tmp, "export")
        text = (tmp / "core.yaml").read_text()
        check("export: core.yaml with the opened card, the head kept", text.startswith(catalog_core.CORE_HEAD) and "cheat-codes" in text
              and catalog_core.slugs(tmp / "core.yaml") == core | {"cheat-codes"})
        out = io(tmp, "import")
        check("export → import: nothing changes", out.returncode == 0 and "оновлено 0" in out.stdout, out.stdout + out.stderr[-300:])
        (tmp / "core.yaml").write_text(text.replace(", cheat-codes", "").replace("cheat-codes, ", "").replace("[cheat-codes]", "[]"))
        out = io(tmp, "import")
        check("import: a card gone from core.yaml — «за запитом»", out.returncode == 0 and not card("cheat-codes")["core"], out.stderr[-300:])
        (tmp / "core.yaml").write_text(text.replace("game-pause", "no-such-card"))
        out = io(tmp, "import")
        check("import: an unknown slug stops it, named", out.returncode != 0 and "no-such-card" in out.stderr and card("game-pause")["core"],
              out.stderr[-300:])
        (tmp / "core.yaml").write_text(text.replace("game-pause", "game-pause, save-progress"))
        (tmp / "tasks.yaml").write_text((tmp / "tasks.yaml").read_text().replace("Чіт-коди", "Чіти"))
        out = io(tmp, "core")
        check("core: only the core, printed", out.returncode == 0 and "в основі: save-progress" in out.stdout and "в основі: cheat-codes" in out.stdout
              and card("save-progress")["core"] and card("cheat-codes")["title"] == "Чіт-коди", out.stdout[-300:] + out.stderr[-300:])
        check("core: in history as the import's", db.history.find_one({"coll": "tasks", "actor": "import", "changes.core.new": True}))
        (tmp / "core.yaml").unlink()
        out = io(tmp, "import")
        check("import with no core.yaml: the core as it is", out.returncode == 0 and card("save-progress")["core"], out.stderr[-300:])
        check("core with no file → stops", io(tmp, "core").returncode != 0)
    check("the repo's core.yaml untouched", catalog_core.slugs(catalog_io.CATALOG / "core.yaml") == core)

ok = sum(results)
print(f"\n{ok}/{len(results)} PASS")
sys.exit(0 if ok == len(results) else 1)
