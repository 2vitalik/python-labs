"""Smoke: a deadline's verdict (T340) — a student per case: the answer, the case, the hours late, the flags; the status poll;
the teacher's word with leniency. Run from app/api: DB_NAME=python_labs_t340_case_smoke uv run python tests/smoke_due_case.py"""
import os
import sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.getcwd())
from pymongo import MongoClient  # noqa: E402

DB = os.environ["DB_NAME"]
assert DB.endswith("_smoke"), "refuse to run on a non-smoke DB"
MongoClient().drop_database(DB)
db = MongoClient()[DB]
from fastapi.testclient import TestClient  # noqa: E402

import main  # noqa: E402
from core.config import settings  # noqa: E402

ADMIN = "admin@nure.ua"
settings.admin_emails, settings.tg_bot_token, settings.fake_user_email = ADMIN, "", ADMIN
D, NOW = datetime(2026, 10, 20, 21, 59), datetime.now(timezone.utc).replace(tzinfo=None)
at = lambda hours: D + timedelta(hours=hours)  # noqa: E731
SAY = ["✅", "☑️", "⏱️", "🚫", "💬", "👁️"]
SIX, NEAR, HALF = ["done"] * 6, ["done"] * 5 + ["partial"], ["done", "partial", "partial", "none", "done", "done"]
results = []
# nick → what the site knows (commits — hours from the deadline; review — verdict at the cut, at the head, required, kind)
# and what it must answer for lab 1: (answer, case, hours late), the flags
CASES = {
    "ontime": dict(commits=[-30], review=("done", "done", SIX), says=0, want=("yes", "ontime", None)),
    "extended": dict(commits=[-30, 24], mark={"until": at(48), "asked": True}, review=("done", "done", SIX), says=2, want=("yes", "extended", None), flags={"says_less"}),
    "early": dict(commits=[-30], mark={"until": at(48)}, review=("done", "done", SIX), want=("yes", "ontime", None)),
    "slip": dict(commits=[-30, 0.4], review=("none", "done", SIX), want=("yes", "slip", 0.4)),
    "moved": dict(commits=[-30, 20], mark={"until": at(48)}, review=("none", "done", SIX), want=("yes", "extended", None)),
    "bit": dict(commits=[21.8], review=("none", "done", SIX), says=1, want=("ask", "late_bit", 21.8), flags={"says_more", "ext_unknown"}),
    "days": dict(commits=[-80, 59], review=("none", "done", SIX), says=0, want=("ask", "late_days", 59.0), flags={"says_more"}),
    "far": dict(commits=[96.5], review=("none", "done", SIX), tg_at=at(39), want=("ask", "late_far", 96.5), flags={"reg_late"}),
    "near": dict(commits=[-8], review=("partial", "partial", NEAR), says=0, want=("ask", "near", None), flags={"says_more"}),
    "partial": dict(commits=[-8, 300], review=("partial", "partial", HALF, "game", 0), says=3, want=("ask", "partial", None), flags={"fresh"}),
    "nothing": dict(commits=[-8], review=("none", "none", ["none"] * 6, "none"), want=("no", "nothing", None)),
    "other": dict(commits=[-8], review=("none", "none", ["none"] * 6, "other"), want=("ask", "other", None)),
    "nosite": dict(seen=False, tg=False, github=False, want=("no", "nosite", None)),
    "norepo": dict(github=False, tg=False, says=3, want=("no", "norepo", None), flags={"nobot"}),
    "noaccess": dict(ok=False, want=("ask", "noaccess", None)),
    "empty": dict(commits=[], want=("no", "empty", None)),
    "void": dict(ok=False, error="репозиторій порожній: жодного коміту", want=("no", "empty", None)),
    "unread": dict(commits=[-5], want=("wait", "unreviewed", None)),
    "after": dict(commits=[10.6], want=("ask", "after", 10.6)),
    "word": dict(commits=[90], mark={"met": True}, want=("yes", "word", None)),
    "wordno": dict(commits=[-30], mark={"met": False}, review=("done", "done", SIX), says=0, want=("no", "word_no", None), flags={"says_more"}),
    "open": dict(commits=[-30], mark={"open": True}, want=("wait", "ext_open", None)),
    "running": dict(commits=[-30], mark={"until": NOW + timedelta(days=3)}, want=("wait", "ext_run", None)),
}


def check(name, cond, extra=""):
    results.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def seed(i, nick, c):
    email, shas = f"{nick}@nure.ua", [f"{nick}c{k}" for k in range(len(c.get("commits", [])))]
    tg = 100 + i if c.get("tg", True) else None
    db.users.insert_one({"email": email, "name": nick, "status": "student", "last_name": nick.title(), "first_name": "X", "patronymic": "", "picture": "",
                         "group": "ПЗПІ-25-1", "test": False, "github": f"https://github.com/{nick}/game" if c.get("github", True) else "", "tg_username": "",
                         "aliases": [], "tg_token": "", "tg_chat_id": tg, "tg_linked_at": c.get("tg_at", at(-200)) if tg else None,
                         "first_seen_at": at(-300) if c.get("seen", True) else None})
    if "commits" in c or "ok" in c:
        db.repos.insert_one({"user": email, "url": "u", "ok": c.get("ok", True), "error": c.get("error", ""), "branch": "main", "head": shas[-1] if shas else "", "pulled_at": NOW, "by": "",
                             "commits": [{"sha": s, "at": at(h), "author": nick, "msg": "m", "files": 1, "add": 10, "rm": 0} for s, h in zip(shas, c["commits"])] if shas else []})
    if "review" in c:
        verdict, head_verdict, required, kind, head = (*c["review"], *("game", -1)[len(c["review"]) - 3:])
        cut = [s for s, h in zip(shas, c["commits"]) if h <= 0]
        db.reviews.insert_one({"user": email, "lab": 1, "commit": cut[-1] if cut else "", "verdict": verdict, "head": shas[head], "head_verdict": head_verdict, "kind": kind,
                               "required": required, "summary": "", "report": "", "profile": {}, "by": "", "at": NOW})
    if "mark" in c:
        db.lab_marks.insert_one({"user": email, "lab": 1, "until": None, "open": False, "reason": "", "met": None, "grace": False, "note": "", "asked": False,
                                 "asked_for": "", "by": ADMIN, "at": NOW} | c["mark"])
    if "says" in c:
        db.votes.insert_one({"update_id": i, "tg_poll_id": "tg1", "poll": pid, "tg_id": tg or 900 + i, "username": "", "user": email, "option_ids": [c["says"]],
                             "text": "", "raw": {}, "at": at(24)})


def poll(title, tags, emoji):
    return db.polls.insert_one({"template": None, "title": title, "question": "?", "options": [{"emoji": e, "text": e} for e in emoji], "multiple": False, "tags": tags,
                                "status": "open", "by": ADMIN, "created_at": NOW, "sent_at": NOW, "closed_at": None}).inserted_id


pid, other = poll("Дедлайн 1: Статус", ["дедлайн", "lab1"], SAY), poll("Пара 1", ["lab1"], ["✅", "❌"])
db.poll_sends.insert_one({"poll": pid, "chat_id": -1, "thread_id": None, "where": "Polls", "silent": False, "status": "sent", "tg_poll_id": "tg1", "message_id": 1,
                          "url": "", "option_ids": [], "error": "", "state": {}, "by": "", "at": NOW})
db.deadlines.insert_many([{"lab": 1, "at": D, "groups": [], "created_at": NOW}, {"lab": 2, "at": at(240), "groups": [], "created_at": NOW},
                          {"lab": 3, "at": NOW + timedelta(days=30), "groups": [], "created_at": NOW}])
for i, (nick, c) in enumerate(CASES.items()):
    seed(i, nick, c)

with TestClient(main.app) as c:
    c.get("/api/auth/dev-login", follow_redirects=False)
    t = c.get("/api/table").json()
    rows = {r["nick"]: r["labs"] for r in t["rows"]}
    for nick, spec in CASES.items():
        got = rows[nick]["1"]["case"]
        check(f"{nick}: {' · '.join(str(x) for x in spec['want'] if x is not None)}", (got["answer"], got["code"], got["late"]) == spec["want"], got)
        check(f"{nick}: flags {sorted(spec.get('flags', set())) or '—'}", set(got["flags"]) == spec.get("flags", set()), got["flags"])
    check("the status poll is known by its tag and its ✅ 🚫", {p["title"]: p["says_lab"] for p in t["polls"]} == {"Дедлайн 1: Статус": 1, "Пара 1": None}, t["polls"])
    check("the word of the poll and when", rows["bit"]["1"]["case"]["says"] == "ext" and rows["bit"]["1"]["case"]["said_at"].startswith("2026-10-21"), rows["bit"]["1"]["case"])
    check("no bot linked → the vote is nobody's", rows["norepo"]["1"]["case"]["says"] is None)
    check("lab 2, its window empty, nothing after → nowork", rows["ontime"]["2"]["case"]["code"] == "nowork" and rows["ontime"]["2"]["case"]["answer"] == "ask", rows["ontime"]["2"])
    check("lab 2, commits in its window → unreviewed", rows["days"]["2"]["case"]["code"] == "unreviewed", rows["days"]["2"])
    check("lab 3 ahead → wait", rows["ontime"]["3"]["case"] | {"flags": []} == {"answer": "wait", "code": "ahead", "late": None, "says": None, "said_at": None, "flags": []})
    check("lab 4 without a deadline → nodue", rows["ontime"]["4"]["case"]["code"] == "nodue")

    r = c.put("/api/students/days/labs/1", json={"grace": True}).json()
    check("leniency: met with it, the cell answers with the case", r["mark"]["met"] is True and r["mark"]["grace"] and (r["case"]["answer"], r["case"]["code"]) == ("yes", "grace"), r)
    check("leniency told to the admins", "🤝" in db.events.find({"kind": "due"}).sort("_id", -1)[0]["text"])
    r = c.put("/api/students/days/labs/1", json={"met": False}).json()
    check("«не вклався» takes the leniency back", r["mark"]["met"] is False and not r["mark"]["grace"] and r["case"]["code"] == "word_no", r)
    r = c.put("/api/students/days/labs/1", json={"met": None}).json()
    check("the word given back to the site", r["mark"]["met"] is None and r["case"]["code"] == "late_days" and r["case"]["late"] == 59.0, r)
    card = c.get("/api/students/near/labs").json()
    check("a student's card carries the cases too", card["labs"][0]["case"]["code"] == "near" and card["labs"][0]["case"]["says"] == "ok", card["labs"][0])

print(f"\n{sum(results)}/{len(results)}")
MongoClient().drop_database(DB)
sys.exit(0 if all(results) else 1)
