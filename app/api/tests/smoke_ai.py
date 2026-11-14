"""Smoke: «Описати словами» (T291 §14, AI-CONTRACT) — the switch, the key, admin vs student, the limits, one at a time, the
budget and its alerts, the proposals (bad words and cards, a mentioned entity, «exists»), apply with needs, apply again, the
states, the history, the schema and the stable prompt — on a scratch DB, the model replaced by a fake that answers
examples.json. Run from app/api: DB_NAME=python_labs_ai_smoke UPLOADS_DIR=... uv run python tests/smoke_ai.py"""
import copy
import inspect
import json
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

import anthropic  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

import main  # noqa: E402
from ai import client, cost, limits, prompt, schema, source  # noqa: E402
from core.config import settings  # noqa: E402

AI = "/api/my/game/ai"
EXAMPLE = json.loads(Path("ai/examples.json").read_text())[0]
USAGE = {"input_tokens": 1000, "cache_creation_input_tokens": 40000, "cache_read_input_tokens": 0, "output_tokens": 5000}
PRICE = (1000 * 2 + 40000 * 2 * 1.25 + 5000 * 10) / 1e6  # sonnet: $2 in, $10 out, a cache write ×1.25
fake = {"answer": EXAMPLE["answer"], "fail": None, "systems": []}
results = []


async def ask(model, system, user, schema_):
    fake["systems"].append(system)
    if fake["fail"]:
        raise client.AskError(fake["fail"], {"model": model} | USAGE)
    return copy.deepcopy(fake["answer"]), {"model": model} | USAGE


client.ask = ask
settings.ai_model, settings.ai_describe, settings.anthropic_api_key, settings.tg_bot_token = "claude-sonnet-5-5", "off", "", ""


def check(name, cond, extra=""):
    results.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def login(c, email, status):
    settings.fake_user_email = email
    c.get("/api/auth/dev-login")
    mongo[DB].users.update_one({"email": email}, {"$set": {"status": status}})


def answer(**changes):
    return copy.deepcopy(EXAMPLE["answer"]) | changes


def post(c, text="Гра — лабіринт", **kw):
    if "answer" in kw:
        fake["answer"] = kw.pop("answer")
    r = c.post(AI, json={"text": text})
    fake["answer"] = EXAMPLE["answer"]
    return r


def group(draft, g):
    return [it for it in draft["items"] if it["group"] == g]


def by_title(draft, g, title):
    return next(it for it in draft["items"] if it["group"] == g and it["data"].get("title") == title)


def events(text=""):
    return [e["text"] for e in mongo[DB].events.find({"kind": "ai"}) if text in e["text"]]


def counts(gid):
    return [mongo[DB][k].count_documents({"game": ObjectId(gid)}) for k in ("game_parts", "rules", "claims")]


with TestClient(main.app) as c:
    src = c.portal.call(source.load)
    sch = schema.build(src)
    check("examples.json: the answer fits the schema", schema.mismatch(EXAMPLE["answer"], sch) == [], schema.mismatch(EXAMPLE["answer"], sch)[:3])
    check("the schema's checker: an extra field, a word off the list, a missing one", len(schema.mismatch(
        answer(extra=1, rules=[EXAMPLE["answer"]["rules"][0] | {"when": {"kind": "nope", "args": []}}], unknown=None) | {"levels": "x"}, sch)) >= 3)
    check("STABLE: the same bytes twice", prompt.stable(src) == prompt.stable(c.portal.call(source.load)))
    for model in ("claude-sonnet-5-5", "claude-haiku-5-5"):
        kw = client.request(model, "s", "u", sch)
        api = anthropic.AsyncAnthropic(api_key="x")
        fn = api.beta.messages.create if "betas" in kw else api.messages.create
        check(f"SDK takes our arguments ({model})", set(kw) <= set(inspect.signature(fn).parameters)
              and {"output_config", "system", "betas", "fallbacks"} <= set(inspect.signature(api.beta.messages.create).parameters))
    check("cost from usage", abs(cost.of({"model": "claude-sonnet-5-5"} | USAGE, "x") - PRICE) < 1e-9
          and cost.of({"model": "claude-haiku-5-5", "cache_read_input_tokens": 1_000_000}, "x") == 0.01 and cost.of({}, "x") == 0)

    login(c, "stud@nure.ua", "student")
    c.post("/api/my/game", json={"title": "Лабіринт", "base_custom": "своя"})
    g = c.get(AI).json()
    check("off: no panel, POST → 403", g["mode"] == "off" and g["why"] == "off" and post(c).status_code == 403, g)
    settings.ai_describe = "admin"
    check("admin only: a student sees nothing", c.get(AI).json()["why"] == "off")
    login(c, "admin@nure.ua", "admin")
    c.post("/api/my/game", json={"title": "Моя", "base_custom": "своя"})
    g = c.get(AI).json()
    r = post(c)
    check("admin, no key: «nokey», POST → 503 in words", g["why"] == "nokey" and r.status_code == 503 and r.json()["detail"] == "ШІ-помічник ще не підключено", r.text)
    settings.anthropic_api_key = "test"
    g = c.get(AI).json()
    check("admin: on, no limits (null), the numbers for the panel", g["mode"] == "on" and g["left_today"] is None and g["left_total"] is None
          and (g["per_day"], g["total"], g["max_chars"]) == (10, 60, 4000) and g["drafts"] == [], g)

    settings.ai_describe = "students"
    login(c, "stud@nure.ua", "student")
    g = c.get(AI).json()
    check("students: on, 10 of 10 today, 60 of 60", (g["mode"], g["left_today"], g["left_total"]) == ("on", 10, 60), g)
    check("empty text → 422", post(c, "   ").status_code == 422)
    check("too long → 422", post(c, "x" * 4001).status_code == 422)
    r = post(c, EXAMPLE["text"])
    d = r.json()
    check("POST → a draft", r.status_code == 200 and d["text"] == EXAMPLE["text"] and d["model"] == "claude-sonnet-5-5" and d["error"] == "", r.text[:300])
    check("the draft's cost", abs(d["cost"] - PRICE) < 1e-9, d.get("cost"))
    check("the prompt is the same on every request", len(fake["systems"]) == 1 and fake["systems"][0] == prompt.stable(src))
    unknown = group(d, "unknown")
    check("the example: every proposal passes, only its own «не розпізнано»", len(unknown) == 1 and unknown[0]["data"]["candidates"] == ["fog-of-war", "save-game"],
          [u["data"]["why"] for u in unknown])
    check("the example: field, 5 entities, 5 rules, 3 windows, 1 level", [len(group(d, k)) for k in ("field", "entity", "rule", "window", "level")] == [1, 5, 5, 3, 1])
    keys = [it["key"] for it in d["items"]]
    check("keys: f, e1…, r1…, w1…, l1…, u1", keys[:3] == ["f", "e1", "e2"] and "r5" in keys and "w3" in keys and keys[-1] == "u1", keys)
    r3 = next(it for it in d["items"] if it["key"] == "r3")
    check("a rule: names, ints, needs", r3["data"]["then"][1] == {"kind": "counter", "name": "ключів", "n": 1} and r3["needs"] == ["e1", "e3", "e4"], r3)
    check("a menu needs its window", by_title(d, "window", "Головне меню")["needs"] == ["w2"])
    check("field: wrap left out, control a list", group(d, "field")[0]["data"] == {"control": ["direct"], "size": "17×7"})
    check("the request's alert: the text quoted, counts, the price", any("<blockquote>Гра — лабіринт" in e and "пропозицій 15 · не розпізнано 1" in e
                                                                          and "за місяць $0.15 з $30" in e for e in events()), events())
    g = c.get(AI).json()
    check("GET: the draft, 9 left today", len(g["drafts"]) == 1 and g["left_today"] == 9 and g["left_total"] == 59)
    hist = c.get("/api/students/stud/game/history").json()
    row = next((x for x in hist if x["coll"] == "game_drafts"), None)
    check("history: «✨ опис словами» with the text", row and row["what"] == "✨ опис словами" and row["title"] == "15 пропозицій · не розпізнано 1"
          and row["fields"] == [{"key": "text", "label": "текст", "old": None, "new": EXAMPLE["text"]}], row)

    # apply one rule: its entities come along
    r = c.post(f"{AI}/{d['id']}/apply", json={"keys": ["r3"]})
    a = r.json()
    states = {it["key"]: it["state"] for it in a["draft"]["items"]}
    check("apply r3 → r3, e1, e3, e4 added, nothing else", r.status_code == 200 and [k for k, s in states.items() if s == "added"] == ["e1", "e3", "e4", "r3"]
          and a["added"]["entities"] == 3 and a["added"]["rules"] == 1 and a["skipped"] == [], r.text[:400])
    made = {it["key"]: it["made"] for it in a["draft"]["items"] if it["made"]}
    check("made: p-/r- of things in the game", made["e1"].startswith("p-") and made["r3"].startswith("r-")
          and mongo[DB].rules.find_one({"_id": ObjectId(made["r3"][2:])}) and mongo[DB].game_parts.find_one({"_id": ObjectId(made["e3"][2:])})["title"] == "Ключ")
    check("the rule's card came too", mongo[DB].claims.find_one({"task": "key-and-door", "rule": made["r3"][2:]}))

    # reject / bring back
    s = c.post(f"{AI}/{d['id']}/state", json={"keys": ["e2", "e1"], "state": "rejected"}).json()
    st = {it["key"]: it["state"] for it in s["items"]}
    check("state: e2 rejected, an added one stays", st["e2"] == "rejected" and st["e1"] == "added")
    st = {it["key"]: it["state"] for it in c.post(f"{AI}/{d['id']}/state", json={"keys": ["e2"], "state": "open"}).json()["items"]}
    check("state: back to open", st["e2"] == "open")
    c.post(f"{AI}/{d['id']}/state", json={"keys": ["e2"], "state": "rejected"})
    check("apply named a rejected one → not added", c.post(f"{AI}/{d['id']}/apply", json={"keys": ["e2"]}).json()["added"]["entities"] == 0)

    # apply everything open: a rejected one a rule needs comes too
    gid = c.get("/api/my/game").json()["id"]
    a = c.post(f"{AI}/{d['id']}/apply", json={"keys": keys}).json()
    items = {it["key"]: it for it in a["draft"]["items"]}
    check("apply all → every proposal added but «не розпізнано»", all(it["state"] == "added" for k, it in items.items() if k != "u1")
          and a["skipped"] == [], [(k, it["state"]) for k, it in items.items()] + a["skipped"])
    coll = {"p": "game_parts", "r": "rules", "c": "claims"}
    check("every made leads to a doc of this game", all(mongo[DB][coll[it["made"][0]]].find_one({"_id": ObjectId(it["made"][2:]), "game": ObjectId(gid)})
                                                        for k, it in items.items() if k != "u1"))
    parts = {(p["kind"], p["title"]) for p in mongo[DB].game_parts.find({"game": ObjectId(gid)})}
    check("the game: field, entities, windows, the menu, the level", {("field", "Поле"), ("entity", "Стіна"), ("window", "Перемога"),
                                                                     ("menu", "Меню «Головне меню»"), ("level", "Лабіринт")} <= parts, parts)
    menu = mongo[DB].game_parts.find_one({"game": ObjectId(gid), "kind": "menu"})
    game_win = mongo[DB].game_parts.find_one({"game": ObjectId(gid), "title": "Гра"})
    check("the menu's item points at the window", menu["items"][0]["window"] == str(game_win["_id"]))
    before = counts(gid)
    a = c.post(f"{AI}/{d['id']}/apply", json={"keys": keys}).json()
    check("apply again → nothing doubled", counts(gid) == before and sum(a["added"].values()) == 0, (before, counts(gid)))

    # the same text again: the game has it all
    d2 = post(c, EXAMPLE["text"]).json()
    check("again: everything «exists», needs empty", all(it["state"] == "exists" and it["needs"] == [] for it in d2["items"] if it["group"] != "unknown"),
          [(it["key"], it["state"]) for it in d2["items"]])

    # what the server makes of a bad answer
    ans = answer(unknown=[])
    ans["entities"][0]["claims"] = [{"slug": "no-such-card", "params": []}, {"slug": "fog-of-war", "params": []}]
    ans["entities"][1]["title"] = "Стіна зі шпичаками"
    ans["rules"][0]["when"] = {"kind": "teleport_all", "args": []}
    ans["rules"][3]["when"]["args"].append({"name": "x", "value": "1"})
    ans["rules"].append({"when": {"kind": "contact", "args": [{"name": "a", "value": "Гравець"}, {"name": "b", "value": "Привид"}]}, "cond": [],
                         "then": [{"kind": "lives", "args": [{"name": "n", "value": "-1"}]}], "note": "", "claims": [], "quote": "привид забирає життя"})
    ans["rules"].append({"when": {"kind": "timer", "args": [{"name": "every", "value": "часто"}]}, "cond": [], "then": [{"kind": "win", "args": []}],
                         "note": "", "claims": [], "quote": "час"})
    ans["claims"] = [{"slug": "fog-of-war", "params": [], "quote": "туман"}, {"slug": "move-4dir", "params": [], "quote": "рух"}]
    login(c, "stud2@nure.ua", "student")
    c.post("/api/my/game", json={"title": "Друга", "base_custom": "своя"})
    d3 = post(c, answer=ans).json()
    why = [u["data"]["why"] for u in group(d3, "unknown")]
    check("a bad word → «не розпізнано» with the reason", any(w.startswith("Правило: Невідоме слово КОЛИ: «teleport_all»") for w in why), why)
    check("an extra argument → the reason", any("зайвий аргумент «x»" in w for w in why), why)
    check("not a number → the reason", any("Правило:" in w and "число" in w for w in why), why)
    e1 = by_title(d3, "entity", "Гравець")
    check("a bad card goes, the entity stays", e1["state"] == "open" and "claims" not in e1["data"]
          and any("картки «no-such-card» нема в каталозі" in w for w in why) and "Сутність «Гравець»: «Туман війни»: Картка про поле додається до поля." in why, why)
    bad = next(u for u in group(d3, "unknown") if "Туман" in u["data"]["why"] or "fog-of-war" in u["data"]["candidates"])
    check("a misplaced card: its quote, itself as the candidate", bad["quote"] == e1["quote"] and bad["data"]["candidates"] == ["fog-of-war"], bad)
    ghost = by_title(d3, "entity", "Привид")
    rule = next(r for r in group(d3, "rule") if r["data"]["when"].get("b") == "Привид")
    check("a mentioned entity is proposed: object, the hint, the rule needs it", ghost["data"] == {"title": "Привид", "role": "object"}
          and ghost["hint"] == "у тексті лише згадана" and ghost["quote"] == "привид забирає життя" and ghost["key"] in rule["needs"], (ghost, rule))
    check("the renamed wall: the rule naming «Стіна» proposes it as mentioned", by_title(d3, "entity", "Стіна")["hint"] == "у тексті лише згадана")
    check("game-level cards: a field one waits for the proposed field, a rule one goes with the reason",
          [(x["data"], x["needs"]) for x in group(d3, "claim")] == [({"slug": "fog-of-war"}, ["f"])]
          and any(u["data"]["candidates"] == ["move-4dir"] for u in group(d3, "unknown")), group(d3, "claim"))

    # limits: a day, a semester, one at a time, a failure not counted
    settings.ai_per_day = 1
    r = post(c)
    check("the day's limit → 429 in words", r.status_code == 429 and r.json()["detail"] == "На сьогодні запити вичерпано — лишилось 0 з 1", r.text)
    settings.ai_per_day, settings.ai_total = 10, 1
    r = post(c)
    check("the semester's limit → 429", r.status_code == 429 and r.json()["detail"] == "На семестр запити вичерпано — лишилось 0 з 1", r.text)
    settings.ai_total = 60
    limits.busy.add("stud2@nure.ua")
    r = post(c)
    check("one at a time → 409", r.status_code == 409 and r.json()["detail"] == "Попередній текст ще розбирається")
    limits.busy.clear()
    fake["fail"] = "Модель відмовилась розбирати цей текст — спробуй сформулювати інакше"
    r = post(c)
    fake["fail"] = None
    g = c.get(AI).json()
    check("a failure → 502, its draft with the error, not counted", r.status_code == 502 and r.json()["detail"].startswith("Модель відмовилась")
          and g["drafts"][0]["error"] and g["left_today"] == 9 and g["drafts"][0]["cost"] > 0, (r.text, g["left_today"]))
    check("…and its alert", any("⚠️ Модель відмовилась" in e for e in events()))

    # the month's budget: the steps once each, then closed for everybody
    spent = c.portal.call(limits.spent)
    settings.ai_budget_usd = round((spent + PRICE / 2) / 0.5, 6)  # the next request steps over 50 %
    post(c)
    check("50 % → one alert", len(events("витрачено 50 %")) == 1 and not events("80 %"), events("💸"))
    settings.ai_budget_usd = round((spent + PRICE * 1.5) / 0.8, 6)  # the next one over 80 %, not 100 %
    post(c)
    check("80 % → one, 50 % not again", len(events("витрачено 50 %")) == 1 and len(events("витрачено 80 %")) == 1 and not events("100 %"), events("💸"))
    settings.ai_budget_usd = c.portal.call(limits.spent)
    g = c.get(AI).json()
    r = post(c)
    check("the ceiling: «budget», POST → 503", g["why"] == "budget" and r.status_code == 503 and "бюджет" in r.json()["detail"], (g["why"], r.text))
    login(c, "admin@nure.ua", "admin")
    check("…the admin too", post(c).status_code == 503)

ok = sum(results)
print(f"\n{ok}/{len(results)} PASS")
sys.exit(0 if ok == len(results) else 1)
