"""Smoke: student games / parts / claims / rules / screenshots / gallery / templates, and T270 — card kinds, auto-claims,
placement, levels, the coin cap, the catalog in the vocab, import --prune — on a scratch DB. Run from app/api:
DB_NAME=python_labs_smoke UPLOADS_DIR=... uv run python tests/smoke_games.py"""
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, os.getcwd())
from bson import ObjectId  # noqa: E402
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
import templates  # noqa: E402
import uploads  # noqa: E402
import zones  # noqa: E402
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
    check("vocab: roles, triggers, conditions, effects, field, stats, args, level, kinds",
          "terrain" in v["roles"] and "contact" in v["triggers"] and "free" in v["conditions"] and "disappear" in v["effects"]
          and v["field"][0]["key"] == "topology" and v["stats"][0]["key"] == "hp" and v["args"]["a"] == "хто"
          and [x["key"] for x in v["level"]] == ["mode", "count", "size"] and list(v["kinds"]) == list(zones.KINDS))
    check("vocab: a guest gets the site's depth", v["depth"] == settings.game_depth == "simple", v["depth"])
    check("vocab: no arrows left in the templates", not any(ch in s["tpl"] for dic in ("triggers", "conditions", "effects")
                                                            for s in v[dic].values() for ch in "→←⇄"))
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
    check("auto-claim of window type", [(cl["task"], cl["auto"]) for cl in r.json()["claims"]] == [("main-menu", True)])
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
    check("unknown part kind → 422", c.post("/api/my/game/parts", json={"kind": "dragon", "title": "x"}).status_code == 422)

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
    check("cascade: window claims gone", {cl["task"] for cl in r["claims"] if not cl["auto"]} == {"player-death", "console-render"})
    check("the field's options claimed by themselves", {cl["task"] for cl in r["claims"] if cl["auto"]} == {"grid-square", "wrap-edges"})
    m = next(p for p in r["parts"] if p["id"] == menu)
    check("cascade: menu host stripped", m["window"] == "")
    check("cascade: item target stripped", m["items"][0]["window"] == "")
    check("cascade: file left original dir", not (Path(os.environ["UPLOADS_DIR"]) / gid / shot).is_file())
    check("cascade: file in trash", (uploads.TRASH / gid / shot).is_file())

    # entities: role from the vocab, stats and states
    r = c.post("/api/my/game/parts", json={"kind": "entity", "title": "Гравець", "role": "player",
                                           "stats": [{"key": "hp", "value": 3}, {"key": "HP", "value": 9}]})
    check("entity: the same stat twice → 422", r.status_code == 422 and r.json()["detail"] == "Параметр «HP» уже є в цієї сутності.", r.text)
    stat = {x["key"]: x for x in c.get("/api/vocab").json()["stats"]}
    r = c.post("/api/my/game/parts", json={"kind": "entity", "title": "Гравець", "role": "player",
                                           "stats": [{"key": "cost", "value": 50, "label": "моя", "unit": "сонць"}, {"key": "лут", "value": "1", "unit": "шт"},
                                                     {"key": "speed", "value": 2, "label": "моя", "unit": "км/год"}],
                                           "states": ["звичайний", " зі щитом ", "Звичайний"]})
    check("entity create: a catalog stat takes the card's title, and its unit when the card has one; own words keep theirs; states unique",
          stat["cost"]["unit"] == "" and stat["speed"]["unit"] and r.status_code == 200 and r.json()["role"] == "player"
          and r.json()["stats"] == [{"key": "cost", "label": stat["cost"]["label"], "value": "50", "unit": "сонць"},
                                    {"key": "лут", "label": "лут", "value": "1", "unit": "шт"},
                                    {"key": "speed", "label": stat["speed"]["label"], "value": "2", "unit": stat["speed"]["unit"]}]
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
    check("claim on entity", c.post("/api/my/claims", json={"task": "body-queue", "part": player}).status_code == 200)

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

    # claims with params; unanchored may wait for required ones (drafts), anchored may not
    wave = c.post("/api/my/game/rules", json={"when": {"kind": "timer", "every": 20}, "then": [{"kind": "spawn", "entity": player}]}).json()["id"]
    r = c.post("/api/my/claims", json={"task": "spawn-schedule", "params": {"every": 20, "max_alive": 4}})
    check("claim with params", r.status_code == 200 and r.json()["params"] == {"every": 20, "max_alive": 4}, r.text)
    spawn_claim = r.json()["id"]
    check("params: game-level without required → draft, 200", c.post("/api/my/claims", json={"task": "collect-quota"}).status_code == 200)
    check("params: on a rule without required → 422",
          c.post("/api/my/claims", json={"task": "pattern-automaton", "rule": wave}).status_code == 422)
    check("params: wrong type → 422",
          c.post("/api/my/claims", json={"task": "time-out", "params": {"limit": "довго"}}).status_code == 422)
    check("params: unknown key → 422",
          c.post("/api/my/claims", json={"task": "event-points", "params": {"x": 1}}).status_code == 422)
    r = c.put(f"/api/my/claims/{spawn_claim}", json={"params": {"every": 30}})
    check("params update", r.status_code == 200 and r.json()["params"] == {"every": 30}, r.text)
    r = c.put(f"/api/my/claims/{spawn_claim}", json={"params": {"every": 30}, "rule": wave})
    check("claim moves onto a rule (drafts pool → anchor)", r.status_code == 200 and r.json()["rule"] == wave, r.text)
    check("claim move to an alien anchor → 422", c.put(f"/api/my/claims/{spawn_claim}", json={"params": {"every": 30}, "rule": "abc"}).status_code == 422
          and c.put(f"/api/my/claims/{spawn_claim}", json={"params": {"every": 30}, "part": "abc"}).status_code == 422)
    r = c.post("/api/my/claims", json={"task": "spawn-schedule", "params": {"every": 5}})
    check("same card again at game level — another anchor, ok", r.status_code == 200, r.text)
    check("move onto a duplicate → 409", c.put(f"/api/my/claims/{r.json()['id']}", json={"params": {"every": 5}, "rule": wave}).status_code == 409)
    r = c.get("/api/students/stud/game").json()
    check("passport: slots on card + params on claim",
          r["tasks"]["spawn-schedule"]["slots"][0]["key"] == "every"
          and next(cl for cl in r["claims"] if cl["task"] == "spawn-schedule" and cl["rule"] == wave)["params"] == {"every": 30})
    check("student cannot judge own claim → 403", c.put(f"/api/students/stud/claims/{spawn_claim}", json={"status": "accepted"}).status_code == 403)
    check("tasks api carries aliases by language", set(c.get("/api/tasks").json()[0]["aliases"]) == {"uk", "ru", "en"})

    r = c.post("/api/refs", json={"url": "https://youtu.be/dQw4w9WgXcQ", "note": "патерн погоні"})
    check("ref create", r.status_code == 200, r.text)
    ref = r.json()["id"]
    check("ref bad url → 422", c.post("/api/refs", json={"url": "просто текст"}).status_code == 422)
    r = c.get("/api/refs").json()
    check("refs list: author nick + mine", r[0]["author"] == "stud" and r[0]["mine"] is True)
    r = c.post("/api/refs", json={"title": "Тип вікна «Мапа скарбів»", "note": "такого типу нема"})
    ev = mongo[DB].events.find_one({"kind": "idea"})
    check("idea → an alert to the teacher (kind idea): the author, the title, the note",
          r.status_code == 200 and ev and "Мапа скарбів" in ev["text"] and "такого типу нема" in ev["text"] and ev["user"] == "stud@nure.ua", ev)
    c.post("/api/refs", json={"url": "https://example.com/x"})
    check("a link → no idea alert", mongo[DB].events.count_documents({"kind": "idea"}) == 1)

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
    check("gallery: entity/rule counters", stud_row["game"]["entities"] == 2 and stud_row["game"]["rules"] == 1)
    check("history recorded", mongo[DB].history.count_documents({"coll": "student_games"}) >= 2)
    check("cascade deletes logged", mongo[DB].history.count_documents({"coll": "claims", "changes.task.new": None}) >= 1)
    check("rules history: 4 creates + 3 cascade deletes", mongo[DB].history.count_documents({"coll": "rules"}) == 7)

    # reference descriptions (Д4): every template pours into a fresh game — nothing skipped, no card left without its
    # place (T270 §6) — and is idempotent
    tpls = c.get("/api/templates").json()
    check("templates listed", len(tpls) >= 1 and all("rules" in t and "levels" in t for t in tpls.values()), list(tpls))
    check("template for a base without one → 404", c.post("/api/my/game/template", json={"slug": "no-such"}).status_code == 404)
    for slug, summary in tpls.items():
        nick = f"tpl-{slug.replace('.', '-')}"
        login(c, f"{nick}@nure.ua", "student")
        r = c.post("/api/my/game", json={"title": f"Еталон {slug}", "base_game": slug})
        if r.status_code != 200:
            r = c.post("/api/my/game", json={"title": f"Еталон {slug}", "base_custom": slug})
        r = c.post("/api/my/game/template", json={"slug": slug})
        skipped = r.json().get("skipped", []) if r.status_code == 200 else []
        ok = r.status_code == 200 and not skipped and r.json()["added"]["rules"] == summary["rules"] \
            and r.json()["added"]["entities"] == summary["entities"] and r.json()["added"]["windows"] == summary["windows"]
        check(f"template {slug}: applied, nothing skipped", ok, skipped or r.text[:400])
        r2 = c.post("/api/my/game/template", json={"slug": slug})
        check(f"template {slug}: second apply adds nothing", r2.status_code == 200 and not any(r2.json()["added"].values()), r2.text[:200])
        full = c.get(f"/api/students/{nick}/game").json()
        kind = {x["id"]: full["tasks"][x["task"]]["kind"] for x in full["claims"]}
        drafts = [x["task"] for x in full["claims"] if not x["part"] and not x["rule"] and kind[x["id"]] not in ("level", "game")]
        check(f"template {slug}: no card left in the drafts", not drafts, drafts)
        entities = sum(p["kind"] == "entity" for p in full["parts"])
        check(f"template {slug}: every entity's type claimed by itself", sum(x["auto"] and kind[x["id"]] == "role" for x in full["claims"]) == entities)
        if not ok:
            break

    # T270: card kinds, auto-claims, where a card may live, levels, the coin cap, the catalog in the vocab
    login(c, "v3@nure.ua", "student")
    PARTS, CLAIMS = "/api/my/game/parts", "/api/my/claims"
    cards = {t["slug"]: t for t in c.get("/api/tasks").json()}
    samples = ("role-player", "stat-hp", "grid-hex", "main-menu", "level-select", "player-death", "status-panel", "body-queue",
               "console-render", "level-from-txt", "save-game")
    check("tasks: the kind resolved — by the subzone, a window type by its tag",
          [cards[x]["kind"] for x in samples] == ["role", "stat", "fieldopt", "window", "window", "rule", "element", "mechanic",
                                                   "field", "level", "game"], [cards[x]["kind"] for x in samples])
    check("tasks: a role card has its icon and opt", cards["role-player"]["icon"] == "🧍" and cards["role-player"]["opt"] == "player")
    v = c.get("/api/vocab").json()
    check("vocab: roles are catalog cards, grouped by their family", v["roles"]["player"]["slug"] == "role-player"
          and v["roles"]["player"]["label"] == "Гравець" and v["roles"]["player"]["group"] == "Живі"
          and v["roles"]["terrain"]["group"] == "Клітини поля"
          and len(v["roles"]) == sum(t["kind"] == "role" and bool(t["opt"]) for t in cards.values()), v["roles"].get("player"))
    check("vocab: stats are catalog cards, the unit from the slot", v["stats"][0]["slug"] == "stat-hp"
          and next(x for x in v["stats"] if x["key"] == "speed")["unit"] == "кл/тік" and len(v["stats"]) == sum(t["kind"] == "stat" for t in cards.values()))
    f = {x["key"]: x for x in v["field"]}
    check("vocab: the field's options are cards; time and control take several; no «нема»",
          f["topology"]["options"]["hex"]["slug"] == "grid-hex" and f["wrap"]["options"]["on"]["slug"] == "wrap-edges"
          and f["time"]["multi"] and f["control"]["multi"] and set(f["gravity"]["options"]) == {"down", "up", "per-type", "toward-center"})
    check("vocab: a student's depth — the site's", v["depth"] == settings.game_depth)
    mongo[DB].tasks.update_one({"slug": "role-boss"}, {"$set": {"status": "draft"}})
    check("vocab: a draft role is not a student's", "boss" not in c.get("/api/vocab").json()["roles"])
    c.post("/api/my/game", json={"title": "Типи карток", "base_custom": "своя"})
    check("entity: a draft role → 422", c.post(PARTS, json={"kind": "entity", "title": "Бос", "role": "boss"}).status_code == 422)

    def auto(pid):
        claims = c.get("/api/students/v3/game").json()["claims"]
        return {x["task"]: x for x in claims if x["part"] == pid and x["auto"]}

    def coins():
        return c.get("/api/students/v3/game").json()["coins"]["claimed"]

    hero = c.post(PARTS, json={"kind": "entity", "title": "Герой", "role": "player", "icon": " 🦸 ",
                               "stats": [{"key": "hp", "value": 3}, {"key": "лут", "value": "2"}]}).json()
    check("entity: its own icon", hero["icon"] == "🦸", hero)
    a = auto(hero["id"])
    check("auto-claims: the role, and a catalog stat with its value (an own word claims nothing)",
          set(a) == {"role-player", "stat-hp"} and a["stat-hp"]["params"] == {"value": "3"}, list(a))
    mongo[DB].claims.update_one({"_id": ObjectId(a["stat-hp"]["id"])}, {"$set": {"status": "accepted", "verdict": "так"}})
    c.put(f"{PARTS}/{hero['id']}", json={"title": "Герой", "role": "enemy", "stats": [{"key": "hp", "value": "5"}]})
    b = auto(hero["id"])
    check("auto-claims follow the part: the role swapped, the stat's value updated, its verdict kept",
          set(b) == {"role-enemy", "stat-hp"} and b["stat-hp"]["id"] == a["stat-hp"]["id"] and b["stat-hp"]["params"] == {"value": "5"}
          and b["stat-hp"]["status"] == "accepted", list(b))
    c.put(f"{PARTS}/{hero['id']}", json={"title": "Герой", "role": "enemy"})
    check("auto-claims: a stat removed — its claim gone", set(auto(hero["id"])) == {"role-enemy"})
    r = c.put(f"{PARTS}/{hero['id']}", json={"title": "Герой", "role": "enemy", "stats": [{"key": "speed", "value": 1}, {"key": "Швидкість", "value": 2}]})
    check("entity: a stat twice by its label → 422", r.status_code == 422 and "Швидкість" in r.json()["detail"], r.text)
    held = auto(hero["id"])["role-enemy"]["id"]
    r = c.put(f"{CLAIMS}/{held}", json={"note": "мій ворог"})
    check("auto-claim: the note stays the student's", r.status_code == 200 and r.json()["note"] == "мій ворог", r.text)
    r = c.put(f"{CLAIMS}/{held}", json={"part": ""})
    check("auto-claim: not moved by hand → 422", r.status_code == 422 and "тримається сама" in r.json()["detail"], r.text)
    check("auto-claim: not deleted by hand → 422", c.delete(f"{CLAIMS}/{held}").status_code == 422)

    fld = c.post(PARTS, json={"kind": "field", "props": {"topology": "square", "time": "turn", "control": ["direct", "click-cell", "direct"],
                                                         "gravity": "none", "wrap": True}}).json()
    check("field: multi-valued as lists, the old «none» dropped",
          fld["props"] == {"topology": "square", "time": ["turn"], "control": ["direct", "click-cell"], "wrap": True}, fld["props"])
    check("field: its options claimed by themselves",
          set(auto(fld["id"])) == {"grid-square", "time-turn", "control-direct", "control-click-cell", "wrap-edges"}, set(auto(fld["id"])))
    check("field: an unknown time → 422", c.put(f"{PARTS}/{fld['id']}", json={"title": "Поле", "props": {"time": ["turn", "someday"]}}).status_code == 422)
    check("field: two grids → 422", c.put(f"{PARTS}/{fld['id']}", json={"title": "Поле", "props": {"topology": ["square", "hex"]}}).status_code == 422)
    c.put(f"{PARTS}/{fld['id']}", json={"title": "Поле", "props": {"topology": "hex", "time": ["turn", "realtime"]}})
    check("field: the auto-claims follow a change", set(auto(fld["id"])) == {"grid-hex", "time-turn", "time-realtime"}, set(auto(fld["id"])))

    win = c.post(PARTS, json={"kind": "window", "title": "Меню", "task": "main-menu"}).json()
    r = c.put(f"{PARTS}/{win['id']}", json={"title": "Меню", "task": "pause-menu"})
    check("window: its type changed, the auto-claim follows", r.json()["task"] == "pause-menu" and set(auto(win["id"])) == {"pause-menu"}, r.text)
    check("window: a card that is no window type → 422", c.put(f"{PARTS}/{win['id']}", json={"title": "Меню", "task": "player-death"}).status_code == 422)

    r = c.post(PARTS, json={"kind": "level", "title": "Печери 5–9", "props": {"mode": "generated", "count": " 5 ", "gravity": "down", "junk": 1},
                            "stats": [{"key": "складність", "value": 3}]})
    lvl = r.json()
    check("level: its own props and the field's it overrides, free stats", r.status_code == 200
          and lvl["props"] == {"mode": "generated", "count": "5", "gravity": "down"} and lvl["stats"][0]["label"] == "складність", r.text)
    check("level: an overridden field option claims its card", set(auto(lvl["id"])) == {"gravity-down"})
    check("level: no title → 422", c.post(PARTS, json={"kind": "level"}).status_code == 422)
    check("level: a mode off the list → 422", c.post(PARTS, json={"kind": "level", "title": "Х", "props": {"mode": "dreamed"}}).status_code == 422)
    check("level: a stat twice → 422", c.post(PARTS, json={"kind": "level", "title": "Х", "stats": [{"key": "a", "value": 1}, {"key": "A", "value": 2}]}).status_code == 422)
    check("level: several per game", c.post(PARTS, json={"kind": "level", "title": "Бонус"}).status_code == 200)

    villain = c.post(PARTS, json={"kind": "entity", "title": "Лиходій", "role": "enemy"}).json()
    rule = c.post("/api/my/game/rules", json={"when": {"kind": "contact", "a": hero["id"], "b": villain["id"]}, "then": [{"kind": "lose"}]}).json()

    def claim(**kw):
        r = c.post(CLAIMS, json=kw)
        return r.status_code if r.status_code == 200 else r.json()["detail"]

    check("place: an automatic kind by hand → 422", claim(task="role-ally", part=hero["id"]) == zones.AUTO and claim(task="stat-hp") == zones.AUTO)
    check("place: element — on a window only", claim(task="status-panel", part=hero["id"]) == zones.HOMES["element"][1]
          and claim(task="status-panel", part=win["id"]) == 200)
    check("place: mechanic — on an entity only", claim(task="body-queue", part=win["id"]) == zones.HOMES["mechanic"][1])
    check("place: field — on the field only", claim(task="console-render", part=hero["id"]) == zones.HOMES["field"][1]
          and claim(task="console-render", part=fld["id"]) == 200)
    check("place: level — on a level or in the section", claim(task="level-from-txt", part=hero["id"]) == zones.HOMES["level"][1]
          and claim(task="level-from-txt", part=lvl["id"]) == 200 and claim(task="level-from-txt") == 200)
    check("place: rule — on a rule only", claim(task="player-death", part=hero["id"]) == zones.HOMES["rule"][1])
    r = c.post(CLAIMS, json={"task": "player-death", "rule": rule["id"]})
    check("place: a rule card on the rule", r.status_code == 200 and r.json()["rule"] == rule["id"] and r.json()["part"] == "", r.text)
    on_rule = r.json()["id"]
    check("place: the same card on the same rule → 409", claim(task="player-death", rule=rule["id"]) == "Така заявка вже є.")
    check("place: game — no anchor", claim(task="save-game", part=hero["id"]) == zones.HOMES["game"][1] and claim(task="save-game") == 200)
    check("place: unanchored is the drafts pool for every other kind", [claim(task=x) for x in ("status-panel", "console-render", "player-death")] == [200] * 3)
    check("place: a part and a rule at once → 422", isinstance(claim(task="time-out", part=hero["id"], rule=rule["id"]), str))
    check("place: someone else's rule → 422", claim(task="time-out", rule="0" * 24) == "Правило не знайдено.")
    draft = c.post(CLAIMS, json={"task": "time-out"}).json()["id"]
    r = c.put(f"{CLAIMS}/{draft}", json={"rule": rule["id"], "params": {"limit": 60}})
    check("claim moves from the drafts onto a rule", r.status_code == 200 and r.json()["rule"] == rule["id"], r.text)
    check("claim cannot move onto an entity by its kind → 422", c.put(f"{CLAIMS}/{draft}", json={"part": hero["id"]}).status_code == 422)

    bronze = coins().get("bronze", 0)
    claim(task="body-queue", part=hero["id"])
    one = coins().get("bronze", 0)
    claim(task="body-queue", part=villain["id"])
    check("coins: a card counts up to its max_count — the second entity adds nothing", one == bronze + 1 and coins().get("bronze", 0) == one,
          (bronze, one, coins()))

    check("rule delete takes the claims on it", c.delete(f"/api/my/game/rules/{rule['id']}").status_code == 200
          and not mongo[DB].claims.find_one({"_id": ObjectId(on_rule)}) and not mongo[DB].claims.find_one({"_id": ObjectId(draft)}))
    rule = c.post("/api/my/game/rules", json={"when": {"kind": "died", "a": villain["id"]}, "then": [{"kind": "win"}]}).json()
    on_rule = c.post(CLAIMS, json={"task": "player-death", "rule": rule["id"]}).json()["id"]
    c.delete(f"{PARTS}/{villain['id']}")
    check("part delete: its rules go, and their claims with them", not mongo[DB].rules.find_one({"_id": ObjectId(rule["id"])})
          and not mongo[DB].claims.find_one({"_id": ObjectId(on_rule)}) and not auto(villain["id"]))
    row = next(x for x in c.get("/api/students").json() if x["nick"] == "v3")
    check("gallery: levels counted", row["game"]["levels"] == 2, row["game"])

    login(c, "tester@nure.ua", "student")
    mongo[DB].users.update_one({"email": "tester@nure.ua"}, {"$set": {"test": True}})
    check("vocab: a test student — full depth", c.get("/api/vocab").json()["depth"] == "full")
    login(c, "admin@nure.ua", "admin")
    v = c.get("/api/vocab").json()
    check("vocab: the teacher — full depth, draft cards among the options", v["depth"] == "full" and "boss" in v["roles"])
    mongo[DB].tasks.update_one({"slug": "role-boss"}, {"$set": {"status": "active"}})
    card = {"slug": "push-blank", "title": "Штовхання", "zone": "entities", "subzone": "interact", "kind": "rule", "icon": " 📦 ",
            "rule": {"when": {"kind": "contact"}, "cond": [], "then": [{"kind": "push", "a": "@b"}]},
            "slots": [{"key": "n", "label": "Скільки", "type": "int", "required": 1, "junk": 1}], "aliases": ["штовхати", " "]}
    r = c.post("/api/tasks", json=card)
    check("tasks: kind, icon, a rule blank, slots, aliases by language", r.status_code == 200 and r.json()["kind"] == "rule"
          and r.json()["icon"] == "📦" and r.json()["rule"] == {"when": {"kind": "contact"}, "then": [{"kind": "push", "a": "@b"}]}
          and r.json()["slots"] == [{"key": "n", "label": "Скільки", "type": "int", "required": True}]
          and r.json()["aliases"] == {"uk": ["штовхати"], "ru": [], "en": []}, r.text)
    r = c.put(f"/api/tasks/{r.json()['id']}", json=card | {"kind": "mechanic", "aliases": {"uk": ["штовхати"], "ru": ["толкать"]}})
    check("tasks: the subzone's own kind is kept implicit; aliases per language",
          r.json()["kind"] == "mechanic" and mongo[DB].tasks.find_one({"slug": "push-blank"})["kind"] == ""
          and r.json()["aliases"]["ru"] == ["толкать"], r.text)
    bad = [card | {"slug": "x1", "kind": "dragon"}, card | {"slug": "x2", "slots": [{"key": "a", "label": "A", "type": "float"}]},
           card | {"slug": "x3", "slots": [{"key": "a", "label": "A", "type": "choice"}]}, card | {"slug": "x4", "rule": {"then": [{"kind": "fly"}]}}]
    check("tasks: a bad kind, slot type, choice without options, rule word → 422", [c.post("/api/tasks", json=x).status_code for x in bad] == [422] * 4)

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

    # a base game's etalon as a described game (T270): poured once, again when the template file is newer
    c.cookies.clear()
    r = c.get("/api/games/sokoban/etalon")
    e = r.json()
    check("etalon: a guest gets it in the passport's shape", r.status_code == 200 and set(e) == {"game", "parts", "claims", "rules", "coins", "tasks"}
          and e["game"]["owner"] == "sokoban@etalon" and e["parts"] and e["rules"] and e["claims"], r.text[:300])
    check("etalon: a second call pours nothing", [p["id"] for p in c.get("/api/games/sokoban/etalon").json()["parts"]] == [p["id"] for p in e["parts"]])
    path = templates.DIR / "sokoban.yaml"
    st = path.stat()
    os.utime(path, (st.st_atime, st.st_mtime + 60))
    again = c.get("/api/games/sokoban/etalon").json()
    os.utime(path, (st.st_atime, st.st_mtime))
    check("etalon: a newer template file pours it again", again["game"]["id"] == e["game"]["id"] and len(again["parts"]) == len(e["parts"])
          and not {p["id"] for p in again["parts"]} & {p["id"] for p in e["parts"]})
    login(c, "admin@nure.ua", "admin")
    check("etalon: no history, no row in the gallery", mongo[DB].history.count_documents({"actor": "sokoban@etalon"}) == 0
          and not any(x["game"] and x["game"]["owner"].endswith("@etalon") for x in c.get("/api/students").json()))
    check("etalon: no template → 404", c.get("/api/games/no-such/etalon").status_code == 404)

    # the catalog snapshot is the truth on import: what it lacks goes to the archive (T270)
    out = subprocess.run(["uv", "run", "python", "catalog_io.py", "import", "--prune"], capture_output=True, text=True, check=False)
    t = {x["slug"]: x for x in mongo[DB].tasks.find({"slug": {"$in": ["push-blank", "main-menu", "settings-window"]}})}
    check("import --prune: a card missing from the YAML goes to the archive and is printed, the rest as in the YAML",
          t["push-blank"]["status"] == "archived" and "push-blank" in out.stdout
          and t["main-menu"]["status"] == t["settings-window"]["status"] == "active", out.stdout[-400:] + out.stderr[-400:])

ok = sum(1 for _, p in results if p)
print(f"\n{ok}/{len(results)} PASS")
sys.exit(0 if ok == len(results) else 1)
