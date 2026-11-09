"""Smoke: student games / parts / claims / rules / screenshots / gallery / templates on a scratch DB. Run from app/api:
DB_NAME=python_labs_smoke UPLOADS_DIR=... uv run python tests/smoke_games.py"""
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, os.getcwd())
from pymongo import MongoClient  # noqa: E402

DB = os.environ["DB_NAME"]
assert DB.endswith("_smoke"), "refuse to run on a non-smoke DB"
mongo = MongoClient()
mongo.drop_database(DB)
subprocess.run(["uv", "run", "python", "catalog_io.py", "import"], check=True, capture_output=True)
# the catalog has no drafts any more (T213): two cards are made drafts here to test the lock on them
mongo[DB].tasks.update_many({"slug": {"$in": ["settings-window", "sound-volume"]}}, {"$set": {"status": "draft"}})

from fastapi.testclient import TestClient  # noqa: E402

import main  # noqa: E402
import uploads  # noqa: E402
from core.config import settings  # noqa: E402

PNG = b"\x89PNG\r\n\x1a\n" + b"0" * 100
results = []


def check(name, cond, extra=""):
    results.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def login(c, email, status):
    settings.fake_user_email = email
    c.get("/api/auth/dev-login")
    mongo[DB].users.update_one({"email": email}, {"$set": {"status": status}})


with TestClient(main.app) as c:
    check("guest: /students → 401", c.get("/api/students").status_code == 401)
    v = c.get("/api/vocab").json()
    check("vocab: roles, triggers, conditions, effects, field, stats",
          "terrain" in v["roles"] and "contact" in v["triggers"] and "free" in v["conditions"] and "disappear" in v["effects"]
          and v["field"][0]["key"] == "size" and v["stats"][0]["key"] == "hp")
    check("vocab: no arg is called kind", all(a["name"] != "kind" for dic in ("triggers", "conditions", "effects") for s in v[dic].values() for a in s["args"]))

    login(c, "waiting@nure.ua", "pending")  # stays pending: gallery visibility check below
    check("pending: POST /my/game → 403", c.post("/api/my/game", json={"title": "x", "base_custom": "y"}).status_code == 403)

    login(c, "stud@nure.ua", "student")
    check("no game yet: GET /my/game → null", c.get("/api/my/game").json() is None)
    r = c.post("/api/my/game", json={"title": "Танчики Пілот", "base_game": "battle-city"})
    check("create game", r.status_code == 200, r.text)
    gid = r.json()["id"]
    check("second game → 409", c.post("/api/my/game", json={"title": "Друга", "base_custom": "x"}).status_code == 409)
    check("bad base → 422", c.put("/api/my/game", json={"title": "Т", "base_game": "no-such"}).status_code == 422)
    check("no base → 422", c.put("/api/my/game", json={"title": "Т"}).status_code == 422)
    r = c.put("/api/my/game", json={"title": "Танчики Пілот", "base_game": "battle-city", "phases": [" ввід ", "гравець", "вороги", "Вороги", ""]})
    check("phases cleaned", r.status_code == 200 and r.json()["phases"] == ["ввід", "гравець", "вороги"], r.text)
    check("13 phases → 422", c.put("/api/my/game", json={"title": "Т", "base_game": "battle-city", "phases": [str(i) for i in range(13)]}).status_code == 422)

    r = c.post("/api/my/game/parts", json={"kind": "window", "task": "main-menu", "title": "Головне меню"})
    check("window create", r.status_code == 200, r.text)
    win = r.json()["id"]
    check("draft type for student → 422",
          c.post("/api/my/game/parts", json={"kind": "window", "task": "settings-window", "title": "Н"}).status_code == 422)
    check("non-window card as type → 422",
          c.post("/api/my/game/parts", json={"kind": "window", "task": "player-death", "title": "Х"}).status_code == 422)
    r = c.get("/api/students/stud/game")
    check("passport by nick", r.status_code == 200, r.text)
    check("auto-claim of window type", [cl["task"] for cl in r.json()["claims"]] == ["main-menu"])
    check("claims enriched with card info", r.json()["tasks"]["main-menu"]["coin"] == "tin")
    check("unknown nick → 404", c.get("/api/students/nobody/game").status_code == 404)
    check("a pending student is not a student's to see → 404", c.get("/api/students/waiting/game").status_code == 404)

    r = c.post("/api/my/game/parts", json={"kind": "menu", "title": "Меню старту", "window": win,
                                           "items": [{"title": "Нова гра", "window": win},
                                                     {"title": "Гучність", "task": "sound-volume"},
                                                     {"title": "  "}]})
    check("menu create (items cleaned)", r.status_code == 200 and len(r.json()["items"]) == 2, r.text)
    menu = r.json()["id"]
    check("bad item target → 422",
          c.post("/api/my/game/parts", json={"kind": "menu", "title": "М",
                                             "items": [{"title": "x", "window": "000000000000000000000000"}]}).status_code == 422)

    # the field: one per game, props by the vocab
    r = c.post("/api/my/game/parts", json={"kind": "field", "props": {"size": " 20×15 ", "topology": "square", "wrap": 1, "layers": "підлога, обʼєкти", "junk": "x", "view": ""}})
    check("field create: props cleaned", r.status_code == 200 and r.json()["title"] == "Поле"
          and r.json()["props"] == {"size": "20×15", "topology": "square", "wrap": True, "layers": ["підлога", "обʼєкти"]}, r.text)
    field = r.json()["id"]
    check("second field → 409", c.post("/api/my/game/parts", json={"kind": "field"}).status_code == 409)
    check("field bad choice → 422", c.put(f"/api/my/game/parts/{field}", json={"title": "Поле", "props": {"topology": "donut"}}).status_code == 422)
    check("unknown part kind → 422", c.post("/api/my/game/parts", json={"kind": "level", "title": "x"}).status_code == 422)

    r = c.post(f"/api/my/game/parts/{win}/screenshot", files={"file": ("s.png", PNG, "image/png")})
    check("screenshot upload", r.status_code == 200 and len(r.json()["screenshots"]) == 1, r.text)
    shot = r.json()["screenshots"][0]
    check("file on disk", (Path(os.environ["UPLOADS_DIR"]) / gid / shot).is_file())
    check("static serve", c.get(f"/api/uploads/{gid}/{shot}").status_code == 200)
    check("bad type → 422",
          c.post(f"/api/my/game/parts/{win}/screenshot", files={"file": ("s.txt", b"x", "text/plain")}).status_code == 422)
    check("oversize → 422",
          c.post(f"/api/my/game/parts/{win}/screenshot",
                 files={"file": ("s.png", b"0" * (8 * 2**20 + 1), "image/png")}).status_code == 422)

    r = c.get("/api/students").json()
    me = next(s for s in r if s["nick"] == "stud")
    check("gallery: cover + counters + field flag", me["game"]["cover"].endswith(shot) and me["game"]["windows"] == 1 and me["game"]["field"] is True)
    check("gallery: student sees no emails/pending", all("email" not in s for s in r)
          and not any(s["nick"] == "waiting" for s in r))

    r = c.post("/api/my/claims", json={"task": "player-death"})
    check("game-level claim", r.status_code == 200, r.text)
    check("duplicate claim → 409", c.post("/api/my/claims", json={"task": "player-death"}).status_code == 409)
    check("draft card claim for student → 422",
          c.post("/api/my/claims", json={"task": "sound-volume"}).status_code == 422)
    r = c.post("/api/my/claims", json={"task": "status-panel", "part": win})
    check("part claim", r.status_code == 200, r.text)
    check("claim on alien part → 422",
          c.post("/api/my/claims", json={"task": "time-out", "part": "abc"}).status_code == 422)
    check("field claim", c.post("/api/my/claims", json={"task": "console-render", "part": field}).status_code == 200)

    r = c.delete(f"/api/my/game/parts/{win}")
    check("window delete", r.status_code == 200)
    r = c.get("/api/students/stud/game").json()
    check("cascade: window claims gone", {cl["task"] for cl in r["claims"]} == {"player-death", "console-render"})
    m = next(p for p in r["parts"] if p["id"] == menu)
    check("cascade: menu host stripped", m["window"] == "")
    check("cascade: item target stripped", m["items"][0]["window"] == "")
    check("cascade: file left original dir", not (Path(os.environ["UPLOADS_DIR"]) / gid / shot).is_file())
    check("cascade: file in trash", (uploads.TRASH / gid / shot).is_file())

    # entities: role from the vocab, stats and states
    r = c.post("/api/my/game/parts", json={"kind": "entity", "title": "Гравець", "role": "player",
                                           "stats": [{"key": "hp", "value": 3}, {"key": "швидкість", "value": "1", "unit": "кл/тік"}, {"key": "HP", "value": 9}],
                                           "states": ["звичайний", " зі щитом ", "Звичайний"]})
    check("entity create: stats labelled, states unique", r.status_code == 200 and r.json()["role"] == "player"
          and r.json()["stats"] == [{"key": "hp", "label": "HP", "value": "3", "unit": ""}, {"key": "швидкість", "label": "швидкість", "value": "1", "unit": "кл/тік"}]
          and r.json()["states"] == ["звичайний", "зі щитом"], r.text)
    player = r.json()["id"]
    check("entity bad role → 422",
          c.post("/api/my/game/parts", json={"kind": "entity", "title": "Бос", "role": "dragon"}).status_code == 422)
    check("entity new role terrain", c.post("/api/my/game/parts", json={"kind": "entity", "title": "Лід", "role": "terrain"}).status_code == 200)
    check("stat without value → 422",
          c.put(f"/api/my/game/parts/{player}", json={"title": "Гравець", "role": "player", "stats": [{"key": "hp", "value": ""}]}).status_code == 422)
    check("13 states → 422",
          c.put(f"/api/my/game/parts/{player}", json={"title": "Гравець", "role": "player", "states": [str(i) for i in range(13)]}).status_code == 422)
    enemy = c.post("/api/my/game/parts", json={"kind": "entity", "title": "Ворожий танк", "role": "enemy"}).json()["id"]
    check("claim on entity", c.post("/api/my/claims", json={"task": "status-panel", "part": player}).status_code == 200)

    # rules: КОЛИ → ЯКЩО → ТО from the dictionaries, sides @a/@b, conditions with not
    r = c.post("/api/my/game/rules", json={"when": {"kind": "contact", "a": player, "b": enemy},
                                           "cond": [{"kind": "state", "a": "@a", "s": "зі щитом", "not": True}],
                                           "then": [{"kind": "damage", "a": "@a", "n": 1}, {"kind": "disappear", "a": "@b"}]})
    check("rule contact create (cond + sides)", r.status_code == 200 and r.json()["cond"][0]["not"] is True
          and r.json()["then"][1]["a"] == "@b", r.text)
    check("rule non-entity side → 422",
          c.post("/api/my/game/rules", json={"when": {"kind": "contact", "a": player, "b": menu}, "then": [{"kind": "win"}]}).status_code == 422)
    check("rule unknown effect → 422",
          c.post("/api/my/game/rules", json={"when": {"kind": "timer", "every": 5}, "then": [{"kind": "explode_everything"}]}).status_code == 422)
    check("rule unknown trigger → 422",
          c.post("/api/my/game/rules", json={"when": {"kind": "full_moon"}, "then": [{"kind": "win"}]}).status_code == 422)
    check("rule missing required arg → 422",
          c.post("/api/my/game/rules", json={"when": {"kind": "contact", "a": player, "b": enemy}, "then": [{"kind": "damage", "a": "@a"}]}).status_code == 422)
    check("rule @a without such side → 422",
          c.post("/api/my/game/rules", json={"when": {"kind": "timer", "every": 5}, "then": [{"kind": "disappear", "a": "@a"}]}).status_code == 422)
    check("rule choice out of list → 422",
          c.post("/api/my/game/rules", json={"when": {"kind": "input", "action": "стрілки"}, "then": [{"kind": "move", "a": player, "dir": "sideways"}]}).status_code == 422)
    check("rule unknown condition → 422",
          c.post("/api/my/game/rules", json={"when": {"kind": "tick"}, "cond": [{"kind": "moon"}], "then": [{"kind": "win"}]}).status_code == 422)
    check("rule without effects → 422",
          c.post("/api/my/game/rules", json={"when": {"kind": "tick"}, "then": []}).status_code == 422)
    r = c.post("/api/my/game/rules", json={"when": {"kind": "timer", "every": 20},
                                           "cond": [{"kind": "count", "what": enemy, "op": "<", "n": 4}],
                                           "then": [{"kind": "spawn", "entity": enemy, "cell": "any"}], "note": "хвилі ворогів"})
    check("rule timer + count + spawn create", r.status_code == 200 and r.json()["cond"][0]["what"] == enemy, r.text)
    check("rule anyone (*) as a side", c.post("/api/my/game/rules", json={"when": {"kind": "contact", "a": "*", "b": enemy}, "then": [{"kind": "block"}]}).status_code == 200)
    r = c.get("/api/students/stud/game").json()
    check("passport: rules present", len(r["rules"]) == 3 and r["rules"][0]["when"]["kind"] == "contact")
    check("entity delete", c.delete(f"/api/my/game/parts/{enemy}").status_code == 200)
    r = c.get("/api/students/stud/game").json()
    check("cascade: entity rules gone (all three named it)", r["rules"] == [] and any(p["id"] == player for p in r["parts"]))

    # claims with params; the game level may wait for required ones (drafts), a part may not
    r = c.post("/api/my/claims", json={"task": "spawn-schedule", "params": {"every": 20, "max_alive": 4}})
    check("claim with params", r.status_code == 200 and r.json()["params"] == {"every": 20, "max_alive": 4}, r.text)
    spawn_claim = r.json()["id"]
    check("params: game-level without required → draft, 200", c.post("/api/my/claims", json={"task": "collect-quota"}).status_code == 200)
    check("params: on a part without required → 422",
          c.post("/api/my/claims", json={"task": "shoot-cooldown", "part": player}).status_code == 422)
    check("params: wrong type → 422",
          c.post("/api/my/claims", json={"task": "time-out", "params": {"limit": "довго"}}).status_code == 422)
    check("params: unknown key → 422",
          c.post("/api/my/claims", json={"task": "event-points", "params": {"x": 1}}).status_code == 422)
    r = c.put(f"/api/my/claims/{spawn_claim}", json={"params": {"every": 30}})
    check("params update", r.status_code == 200 and r.json()["params"] == {"every": 30}, r.text)
    r = c.put(f"/api/my/claims/{spawn_claim}", json={"params": {"every": 30}, "part": player})
    check("claim moves to an entity (drafts pool → anchor)", r.status_code == 200 and r.json()["part"] == player, r.text)
    check("claim move to alien part → 422", c.put(f"/api/my/claims/{spawn_claim}", json={"params": {"every": 30}, "part": "abc"}).status_code == 422)
    r = c.post("/api/my/claims", json={"task": "spawn-schedule", "params": {"every": 5}})
    check("same card again at game level — another anchor, ok", r.status_code == 200, r.text)
    check("move onto a duplicate → 409", c.put(f"/api/my/claims/{r.json()['id']}", json={"params": {"every": 5}, "part": player}).status_code == 409)
    r = c.get("/api/students/stud/game").json()
    check("passport: slots on card + params on claim",
          r["tasks"]["spawn-schedule"]["slots"][0]["key"] == "every"
          and next(cl for cl in r["claims"] if cl["task"] == "spawn-schedule" and cl["part"] == player)["params"] == {"every": 30})
    check("student cannot judge own claim → 403", c.put(f"/api/students/stud/claims/{spawn_claim}", json={"status": "accepted"}).status_code == 403)
    check("tasks api carries aliases", isinstance(c.get("/api/tasks").json()[0]["aliases"], list))

    r = c.post("/api/refs", json={"url": "https://youtu.be/dQw4w9WgXcQ", "note": "патерн погоні"})
    check("ref create", r.status_code == 200, r.text)
    ref = r.json()["id"]
    check("ref bad url → 422", c.post("/api/refs", json={"url": "просто текст"}).status_code == 422)
    r = c.get("/api/refs").json()
    check("refs list: author nick + mine", r[0]["author"] == "stud" and r[0]["mine"] is True)

    login(c, "stud2@nure.ua", "student")
    mongo[DB].users.update_one({"email": "stud2@nure.ua"}, {"$set": {"group": "ПЗПІ-25-2"}})
    check("foreign ref edit → 403",
          c.put(f"/api/refs/{ref}", json={"url": "https://x.com"}).status_code == 403)

    login(c, "admin@nure.ua", "admin")
    check("admin: edit any ref", c.put(f"/api/refs/{ref}", json={"url": "https://x.com", "note": "патерн погоні"}).status_code == 200)
    check("ref edit in history: actor admin, url old → new",
          mongo[DB].history.find_one({"coll": "refs", "actor": "admin@nure.ua"})["changes"]["url"]["new"] == "https://x.com")
    check("admin: delete any ref", c.delete(f"/api/refs/{ref}").status_code == 200)
    r = c.post("/api/my/game", json={"title": "Демо викладача", "base_custom": "Своя гра-прикладка"})
    check("admin: own game, custom base", r.status_code == 200, r.text)
    r = c.post("/api/my/game/parts", json={"kind": "window", "task": "settings-window", "title": "Налаштування"})
    check("admin: draft type allowed", r.status_code == 200, r.text)
    check("params: choice not in options → 422",
          c.post("/api/my/claims", json={"task": "maze-generation", "params": {"algo": "bfs"}}).status_code == 422)
    check("params: choice ok",
          c.post("/api/my/claims", json={"task": "maze-generation", "params": {"algo": "dfs"}}).status_code == 200)
    check("params: bool not bool → 422",
          c.post("/api/my/claims", json={"task": "enemy-waves", "params": {"waves": 5, "final_wave": "так"}}).status_code == 422)
    check("params: bool ok",
          c.post("/api/my/claims", json={"task": "enemy-waves", "params": {"waves": 5, "final_wave": True}}).status_code == 200)

    # the teacher's verdict on a student's claim
    r = c.put(f"/api/students/stud/claims/{spawn_claim}", json={"status": "accepted", "verdict": " молодець "})
    check("admin judges a claim", r.status_code == 200 and r.json()["status"] == "accepted" and r.json()["verdict"] == "молодець", r.text)
    check("judge: bad status → 422", c.put(f"/api/students/stud/claims/{spawn_claim}", json={"status": "maybe"}).status_code == 422)
    check("judge: unknown claim → 404", c.put("/api/students/stud/claims/000000000000000000000000", json={"status": "accepted"}).status_code == 404)
    r = c.get("/api/students").json()
    stud_row = next(s for s in r if s["nick"] == "stud")
    check("gallery: accepted counter + coins_accepted", stud_row["game"]["accepted"] == 1 and stud_row["game"]["coins_accepted"] == {"tin": 1.0}, stud_row["game"])
    check("admin gallery: emails + pending visible", any(s.get("email") for s in r)
          and any(s["nick"] == "waiting" for s in r))
    check("gallery: 2 games", sum(1 for s in r if s["game"]) == 2)
    check("passport of another: mine=false", c.get("/api/students/stud/game").json()["mine"] is False)
    check("admin: student by nick", c.get("/api/students/stud").json()["email"] == "stud@nure.ua")
    r = c.get("/api/students/waiting/game")
    check("a student without a game → the student, game: null", r.status_code == 200 and r.json()["game"] is None
          and r.json()["student"]["nick"] == "waiting", r.text)
    r = c.put("/api/students/stud", json={"last_name": "Тест", "group": "ПЗПІ-25-1"})
    check("admin: edit by nick", r.status_code == 200 and r.json()["group"] == "ПЗПІ-25-1", r.text)
    check("gallery: entity/rule counters", stud_row["game"]["entities"] == 2 and stud_row["game"]["rules"] == 0)
    check("history recorded", mongo[DB].history.count_documents({"coll": "student_games"}) >= 2)
    check("cascade deletes logged", mongo[DB].history.count_documents({"coll": "claims", "changes.task.new": None}) >= 1)
    check("rules history: 3 creates + 3 cascade deletes", mongo[DB].history.count_documents({"coll": "rules"}) == 6)

    # reference descriptions (Д4): every template pours into a fresh game without a single skipped item, and is idempotent
    tpls = c.get("/api/templates").json()
    check("templates listed", len(tpls) >= 1 and all("rules" in t for t in tpls.values()), list(tpls))
    check("template for a base without one → 404", c.post("/api/my/game/template", json={"slug": "no-such"}).status_code == 404)
    for slug, summary in tpls.items():
        login(c, f"tpl-{slug.replace('.', '-')}@nure.ua", "student")
        r = c.post("/api/my/game", json={"title": f"Еталон {slug}", "base_game": slug})
        if r.status_code != 200:
            r = c.post("/api/my/game", json={"title": f"Еталон {slug}", "base_custom": slug})
        r = c.post("/api/my/game/template", json={"slug": slug})
        ok = r.status_code == 200 and not r.json()["skipped"] and r.json()["added"]["rules"] == summary["rules"] \
            and r.json()["added"]["entities"] == summary["entities"] and r.json()["added"]["windows"] == summary["windows"]
        check(f"template {slug}: applied fully", ok, r.text[:400])
        r2 = c.post("/api/my/game/template", json={"slug": slug})
        check(f"template {slug}: second apply adds nothing", r2.status_code == 200 and not any(r2.json()["added"].values()), r2.text[:200])
        if not ok:
            break

    login(c, "admin@nure.ua", "admin")
    mongo[DB].users.insert_many([{"email": "old@nure.ua", "status": "student", "group": "ПЗПІ-24-1"},
                                 {"email": "ind@nure.ua", "status": "student", "group": "ПЗПІи-25-1"},
                                 {"email": "lost@nure.ua", "status": "student", "group": ""}])
    r = c.get("/api/students").json()
    check("admin gallery: every stream", {"old", "ind", "lost"} <= {s["nick"] for s in r}, [s["nick"] for s in r])

    login(c, "stud@nure.ua", "student")  # the teacher's game is not a student's to see (T216), nor another stream's
    r = c.get("/api/students").json()
    check("student gallery: own stream only — no teacher, pending, other year, other specialty, no group",
          {s["nick"] for s in r} == {"stud", "stud2"}, [s["nick"] for s in r])
    check("student: the teacher's passport → 404", c.get("/api/students/admin/game").status_code == 404)
    check("student: another year's passport → 404", c.get("/api/students/old/game").status_code == 404)
    check("student: another specialty's passport → 404", c.get("/api/students/ind/game").status_code == 404)
    login(c, "lost@nure.ua", "student")
    r = c.get("/api/students").json()
    check("no group: only themselves", {s["nick"] for s in r} == {"lost"}, [s["nick"] for s in r])

ok = sum(1 for _, p in results if p)
print(f"\n{ok}/{len(results)} PASS")
sys.exit(0 if ok == len(results) else 1)
