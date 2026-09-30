"""Smoke: polls on the site (T176) — templates, drafts, sending with a fake Telegram, results, the table, closing, deleting.
Run from app/api: DB_NAME=python_labs_smoke uv run python tests/smoke_polls_api.py"""
import os
import sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.getcwd())
from pymongo import MongoClient  # noqa: E402

DB = os.environ["DB_NAME"]
assert DB.endswith("_smoke"), "refuse to run on a non-smoke DB"
MongoClient().drop_database(DB)
db = MongoClient()[DB]
from aiogram.exceptions import TelegramAPIError, TelegramBadRequest  # noqa: E402
from aiogram.types import Chat, Message, PollOption  # noqa: E402
from aiogram.types import Poll as TgPoll  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

import main  # noqa: E402
from core.bot import notify  # noqa: E402
from core.config import settings  # noqa: E402

ADMIN, VASYA = "admin@nure.ua", "vasya@nure.ua"
FORUM, GROUP = -1001234567890, -200
settings.admin_emails, settings.tg_bot_token = ADMIN, "fake"
alerts, asked, stopped, results = [], [], [], []
broken, gone, final = set(), set(), {}  # chats where sending fails · where the poll message is gone · stopPoll's counts
now = datetime.now(timezone.utc)


def tg_poll(poll_id, texts, total=0, counts=None, closed=False):
    counts = counts or [0] * len(texts)
    return TgPoll(id=poll_id, question="?", options=[PollOption(persistent_id=f"o{i}", text=t, voter_count=counts[i]) for i, t in enumerate(texts)],
                  total_voter_count=total, is_closed=closed, is_anonymous=False, type="regular", allows_multiple_answers=False,
                  allows_revoting=True, members_only=False)


class FakeBot:
    async def send_message(self, chat_id, text, message_thread_id=None):
        alerts.append(text)

    async def send_poll(self, chat_id, question, options, **kw):
        if chat_id in broken:
            raise TelegramAPIError(method=None, message="Bad Request: not enough rights to send polls to the chat")
        asked.append({"chat_id": chat_id, "question": question, "options": [o.text for o in options], **kw})
        chat = Chat(id=chat_id, type="supergroup" if chat_id == FORUM else "group" if chat_id < 0 else "private")
        return Message(message_id=100 + len(asked), date=now, chat=chat, message_thread_id=kw["message_thread_id"],
                       is_topic_message=bool(kw["message_thread_id"]) or None, poll=tg_poll(f"tg{len(asked)}", [o.text for o in options]))

    async def stop_poll(self, chat_id, message_id):
        stopped.append(chat_id)
        if chat_id in gone:
            raise TelegramBadRequest(method=None, message="Bad Request: message to stop poll not found")
        total, counts = final.get(chat_id, (0, None))
        return tg_poll("x", ["a", "b", "c"], total, counts, closed=True)


notify.bot = lambda: FakeBot()


def check(name, cond, extra=""):
    results.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def person(email, group, last, tg=None, **extra):
    db.users.insert_one({"email": email, "status": "student", "group": group, "last_name": last, "first_name": last[0], "tg_chat_id": tg} | extra)


def vote(update_id, tg_poll_id, tg_id, ids, minutes, user=""):
    db.votes.insert_one({"update_id": update_id, "tg_poll_id": tg_poll_id, "tg_id": tg_id, "username": f"u{tg_id}", "user": user,
                         "option_ids": ids, "text": f"vote {ids}", "raw": {}, "at": now - timedelta(minutes=minutes)})


db.users.insert_one({"email": ADMIN, "status": "admin", "first_name": "Віталій", "tg_chat_id": 1})
person(VASYA, "ПЗПІ-25-1", "Пупкін", 42)
person("petro@nure.ua", "ПЗПІ-25-1", "Петренко", 43)
person("ivan@nure.ua", "ПЗПІ-25-1", "Іваненко", 45)
person("olga@nure.ua", "ПЗПІ-25-2", "Ольченко")  # no bot: her votes come in as a stranger's
person("test@nure.ua", "ПЗПІ-25-1", "Тестовий", 44, test=True)
topic = db.tg_chats.insert_one({"chat_id": FORUM, "thread_id": 5, "title": "ПЗПІ-25 Python", "topic": "25-1", "name": "", "type": "supergroup",
                                "left": False, "hidden": False, "seen_at": now}).inserted_id
group = db.tg_chats.insert_one({"chat_id": GROUP, "thread_id": None, "title": "Стара група", "topic": "", "name": "", "type": "group",
                                "left": False, "hidden": False, "seen_at": now}).inserted_id
OPTIONS = [{"emoji": "✅", "text": "так"}, {"emoji": "🤒", "text": "хворію"}, {"emoji": "❌", "text": "ні"}]
QUESTION = {"title": "", "question": "Хто на парі?", "options": OPTIONS, "tags": ["відвідуваність", "#відвідуваність", " "]}


def sign_in(c, email):
    settings.fake_user_email = email
    c.get("/api/auth/dev-login", follow_redirects=False)


with TestClient(main.app, raise_server_exceptions=False) as c:
    check("guest: polls → 401", c.get("/api/polls").status_code == 401)
    sign_in(c, VASYA)
    check("student: polls, templates, table → 403", {c.get(p).status_code for p in ("/api/polls", "/api/polls/templates", "/api/polls/matrix")} == {403})
    sign_in(c, ADMIN)

    t = c.post("/api/polls/templates", json=QUESTION | {"title": "Хто на парі"}).json()
    check("template: saved, tags cleaned (# and duplicates gone)", t["tags"] == ["відвідуваність"] and t["options"][1]["emoji"] == "🤒", t)
    got = c.get("/api/polls/templates").json()
    check("templates list + known tags", len(got["templates"]) == 1 and got["tags"] == ["відвідуваність"])
    bad = [QUESTION | {"options": OPTIONS[:1]}, QUESTION | {"question": "?" * 301}, QUESTION | {"options": [*OPTIONS, {"text": "x" * 101}]},
           QUESTION | {"options": [*OPTIONS, OPTIONS[0]]}, QUESTION | {"question": " "}]
    codes = [c.post("/api/polls", json=b) for b in bad]
    check("Telegram's limits said in Ukrainian: 1 answer, long question, long answer, twins, empty",
          all(r.status_code == 422 and isinstance(r.json()["detail"], str) for r in codes), [r.json() for r in codes])

    p = c.post("/api/polls", json=QUESTION | {"title": "Пара 30.09", "template": t["id"]}).json()
    check("poll: a draft copied from the template", p["status"] == "draft" and p["template"] == t["id"] and p["title"] == "Пара 30.09")
    pid = p["id"]
    check("draft: the question can change", c.put(f"/api/polls/{pid}", json=QUESTION | {"title": "Пара 30.09", "question": "Хто сьогодні на парі?"})
          .json()["question"] == "Хто сьогодні на парі?")
    untitled = c.post("/api/polls", json=QUESTION).json()
    check("no title: the question stands in", untitled["title"] == "Хто на парі?")
    check("draft without votes: deleted", c.delete(f"/api/polls/{untitled['id']}").status_code == 200 and not c.get(f"/api/polls/{untitled['id']}").is_success)

    chats = c.get("/api/polls/chats").json()
    check("places: both chats, the topic by name; `me` — the admin's own chat", len(chats["chats"]) == 2 and chats["me"] == 1
          and {x["where"] for x in chats["chats"]} == {"ПЗПІ-25 Python › 25-1", "Стара група"})

    broken.add(GROUP)
    r = c.post(f"/api/polls/{pid}/send", json={"targets": [str(topic), str(group), "me"], "silent": True}).json()
    by = {s["where"]: s for s in r["sends"]}
    check("send: the topic and my chat — sent, the group — failed with Telegram's words",
          by["ПЗПІ-25 Python › 25-1"]["status"] == "sent" and by["особисто · Віталій"]["status"] == "sent"
          and by["Стара група"]["status"] == "failed" and "not enough rights" in by["Стара група"]["error"], r)
    a = asked[0]
    check("Telegram got: the question, «emoji text» answers, not anonymous, silent, the topic, no HTML parsing",
          a["question"] == "Хто сьогодні на парі?" and a["options"] == ["✅ так", "🤒 хворію", "❌ ні"] and a["is_anonymous"] is False
          and a["disable_notification"] is True and a["message_thread_id"] == 5 and a["question_parse_mode"] is None, a)
    check("link to the message in the forum topic", by["ПЗПІ-25 Python › 25-1"]["url"] == "https://t.me/c/1234567890/5/101")
    check("the poll is open now", c.get(f"/api/polls/{pid}").json()["poll"]["status"] == "open")
    check("a failed send → alert `poll` with the place and the reason", any("Не надіслав" in x and "Стара група" in x for x in alerts)
          and db.events.count_documents({"kind": "poll"}) == 1)

    n = len(asked)
    r = c.post(f"/api/polls/{pid}/send", json={"targets": [str(topic), "me", str(group)]}).json()
    check("send again: no second message where it is already; the failed place is tried again", len(asked) == n
          and [s["status"] for s in r["sends"]] == ["failed"])
    broken.clear()
    sid = r["sends"][0]["id"]
    r = c.post(f"/api/polls/{pid}/sends/{sid}/retry")
    check("retry: the same row, sent now", r.status_code == 200 and r.json()["status"] == "sent" and r.json()["id"] == sid
          and db.poll_sends.count_documents({"poll": db.polls.find_one()["_id"]}) == 3)
    check("retry of a sent one → 409", c.post(f"/api/polls/{pid}/sends/{sid}/retry").status_code == 409)

    check("open poll: the question is frozen", c.put(f"/api/polls/{pid}", json=QUESTION | {"title": "Пара 30.09", "question": "Інше?"}).status_code == 409)
    r = c.put(f"/api/polls/{pid}", json=QUESTION | {"title": "Пара 1.10", "question": "Хто сьогодні на парі?", "tags": ["відвідуваність", "пари"]})
    check("open poll: title and tags still change", r.status_code == 200 and r.json()["title"] == "Пара 1.10" and r.json()["tags"] == ["відвідуваність", "пари"])

    vote(1, "tg1", 42, [0], 50)  # Вася in the topic: так…
    vote(2, "tg1", 43, [2], 40)  # Петро: ні…
    vote(3, "tg1", 43, [], 30)  # …and took it back
    vote(4, "tg3", 99, [1], 20)  # a stranger in the group
    vote(5, "tg2", 1, [0], 15)  # the teacher tries it in his own chat
    vote(6, "tg3", 42, [1], 10)  # Вася again, in the group, before linking — the row has no email: хворію
    db.poll_sends.update_one({"tg_poll_id": "tg1"}, {"$set": {"state": {"total": 2, "counts": [1, 0, 1], "is_closed": False, "at": ""}}})

    res = c.get(f"/api/polls/{pid}").json()
    names = lambda voters: [v["who"].get("nick") or v["who"].get("tg_id") for v in voters]  # noqa: E731
    check("results: an answer per person — their latest, across all messages", res["options"][0]["voters"] == []
          and names(res["options"][1]["voters"]) == ["vasya", 99] and res["options"][2]["voters"] == [], [names(o["voters"]) for o in res["options"]])
    check("…the teacher's try in his own chat is apart, not an answer", names(res["tries"]) == ["admin"] and res["tries"][0]["ids"] == [0])
    check("…Петро took it back, Іван with the bot has not voted, Ольга is not counted (no bot)", names(res["retracted"]) == ["petro"]
          and [[p["nick"] for p in g["people"]] for g in res["missing"]] == [["ivan"]] and res["unlinked"] == 1, res["missing"])
    check("…every vote in the timeline, newest first", [e["ids"] for e in res["timeline"]] == [[1], [0], [1], [], [2], [0]])
    m = {s["where"]: s["mismatch"] for s in res["sends"]}
    check("Telegram counts 2 in the topic, we have 1: mismatch shown; others agree or unknown",
          m["ПЗПІ-25 Python › 25-1"] == {"telegram": 2, "ours": 1} and m["Стара група"] is None, m)
    check("students have voted: not deletable", not res["can_delete"] and c.delete(f"/api/polls/{pid}").status_code == 409)

    lst = c.get("/api/polls").json()
    row = lst["polls"][0]
    check("list: voters now (the teacher's try aside), where it went, the mismatch flag, tags", row["voters"] == 2 and len(row["sends"]) == 3 and row["mismatch"]
          and lst["tags"] == ["відвідуваність", "пари"], row)
    check("list by tag", len(c.get("/api/polls?tag=пари").json()["polls"]) == 1 and not c.get("/api/polls?tag=інше").json()["polls"])

    mx = c.get("/api/polls/matrix").json()
    cells = {r["nick"]: r["cells"].get(pid) for r in mx["rows"]}
    check("table: students only, by group; Вася — 🤒, Петро — taken back, Іван and Ольга — nothing",
          list(cells) == ["ivan", "petro", "vasya", "olga"] and cells["vasya"]["ids"] == [1] and cells["petro"]["ids"] == []
          and cells["ivan"] is None and cells["olga"] is None, cells)
    check("…everyone else who voted is under `others`: the teacher and the stranger",
          sorted(str(o["who"].get("nick") or o["who"].get("tg_id")) for o in mx["others"]) == ["99", "admin"])
    check("table filters: another tag or template — no columns", not c.get("/api/polls/matrix?tag=інше").json()["polls"]
          and not c.get("/api/polls/matrix?template=000000000000000000000000").json()["polls"]
          and len(c.get(f"/api/polls/matrix?template={t['id']}&days=1").json()["polls"]) == 1)

    feed = c.get("/api/activity", params={"src": "vote", "user": "vasya"}).json()["rows"]
    check("activity: Вася's votes, the one cast before linking too", len(feed) == 2 and all(r["user"] == VASYA for r in feed), feed)

    final[FORUM], final[1] = (2, [1, 0, 1]), (1, [1, 0, 0])
    gone.add(GROUP)
    res = c.post(f"/api/polls/{pid}/close").json()
    st = {s["where"]: s for s in res["sends"]}
    check("close: every message stopped, Telegram's final count kept; a vanished message is closed with a note",
          res["poll"]["status"] == "closed" and all(s["status"] == "closed" for s in res["sends"]) and st["ПЗПІ-25 Python › 25-1"]["state"]["total"] == 2
          and "not found" in st["Стара група"]["error"], st)
    check("close with a mismatch → alert with both counts", any("Закрито" in x and "Telegram нарахував 2, у нас 1" in x for x in alerts))
    check("closed: no more sending", c.post(f"/api/polls/{pid}/send", json={"targets": ["me"]}).status_code == 409)

    tpl = c.post(f"/api/polls/{pid}/template")
    check("a poll becomes a template", tpl.status_code == 200 and len(c.get("/api/polls/templates").json()["templates"]) == 2)
    check("template: edited, then deleted", c.put(f"/api/polls/templates/{t['id']}", json=QUESTION | {"title": "Пара"}).json()["title"] == "Пара"
          and c.delete(f"/api/polls/templates/{t['id']}").status_code == 200 and len(c.get("/api/polls/templates").json()["templates"]) == 1)

    tried = c.post("/api/polls", json=QUESTION | {"title": "Спроба"}).json()
    c.post(f"/api/polls/{tried['id']}/send", json={"targets": ["me"]})
    vote(7, f"tg{len(asked)}", 1, [0], 1)
    n = len(stopped)
    check("a poll only the teacher voted in: deleted, its message stopped first", c.get(f"/api/polls/{tried['id']}").json()["can_delete"]
          and c.delete(f"/api/polls/{tried['id']}").status_code == 200 and len(stopped) == n + 1
          and not db.poll_sends.find_one({"poll": db.polls.find_one({"title": "Спроба"})}))
    check("history: polls and templates recorded", db.history.count_documents({"coll": "polls"}) >= 5 and db.history.count_documents({"coll": "poll_templates"}) >= 4)

    api = lambda method: db.activity.count_documents({"kind": "api", "method": method, "path": {"$regex": "^/api/polls"}})  # noqa: E731
    check("footprint: the pages' self-refreshing reads are not logged, the actions are", api("GET") == 0 and api("POST") > 0)

    r = c.put(f"/api/polls/chats/{group}", json={"name": "  Архів  групи ", "hidden": True}).json()
    check("a place renamed and hidden", r["where"] == "Архів групи" and r["hidden"])

    settings.tg_bot_token = ""
    p2 = c.post("/api/polls", json=QUESTION | {"title": "Без бота"}).json()
    s = c.post(f"/api/polls/{p2['id']}/send", json={"targets": ["me"]}).json()["sends"][0]
    check("no bot token: the send fails with a reason, the poll stays a draft", s["status"] == "failed" and "TG_BOT_TOKEN" in s["error"]
          and c.get(f"/api/polls/{p2['id']}").json()["poll"]["status"] == "draft")

ok = sum(results)
print(f"\n{ok}/{len(results)} PASS")
sys.exit(0 if ok == len(results) else 1)
