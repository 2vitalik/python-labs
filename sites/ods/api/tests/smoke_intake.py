"""Smoke: the teacher's forwards of students' messages (T368 §2) — the bot's handler with Telegram replaced by a recorder, one
summary per burst, the file read without running (lab by its line, template, name), whose it is (Telegram, a guess, the teacher's
word), «Вхідні» and its changes, notebooks becoming versions of «Моя лаба» with the time of the student's message. Made-up data.
Run from sites/ods/api: DB_NAME=ods_t368_intake_smoke SESSION_SECRET=x ~/.venvs/python-labs/bin/python tests/smoke_intake.py"""
import asyncio
import io
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from itertools import count
from pathlib import Path

sys.path.insert(0, os.getcwd())
sys.path.insert(0, str(Path(__file__).parent))
from pymongo import MongoClient  # noqa: E402

import nb_fixture as fx  # noqa: E402

DB = os.environ["DB_NAME"]
assert DB.endswith("_smoke"), "refuse to run on a non-smoke DB"
mongo = MongoClient()
mongo.drop_database(DB)
db = mongo[DB]
os.environ |= {"AGENT_TOKENS": "claude:tok-123", "SESSION_SECRET": os.environ.get("SESSION_SECRET", "x"), "LAB_GATES": ""}
results = []


def check(name, cond, extra=""):
    results.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def card(group, n, lab):
    vid = f"{group}-{n:02d}"
    return {"lab": lab, "vid": vid, "group": group, "n": n, "card": fx.CARD.format(vid=vid), "ask": [],
            "answers": {"x": {"value": 2, "step": 0, "traps": []}, "y": {"value": 3, "step": 0, "traps": []}}}


def lab2(cells):
    """Lab 2's own words around the same marks: its template is not lab 1's."""
    words = {"Вигадана": "Друга", "Перша": "Інша", "Порахуй": "Обчисли", "Графік.": "Діаграма.", "Що вийшло": "Що видно", "## Рапорт": "## Звіт"}
    out = []
    for kind, src, *rest in cells:
        for a, b in words.items() if kind == "markdown" else ():
            src = src.replace(a, b)
        out.append((kind, src, *rest))
    return out


data = Path(tempfile.mkdtemp())
for n, cells in ((1, fx.TEMPLATE), (2, lab2(fx.TEMPLATE))):
    (data / f"labs/new/lab{n}").mkdir(parents=True)
    (data / f"labs/new/lab{n}/lab{n}-jupyter.ipynb").write_bytes(fx.notebook(cells))
for n in (1, 2, 3):
    for group, nums in (("КН-1", range(1, 6)), ("ДЕМО", (0,))):
        (data / f"labs/new/lab{n}/out/{group}").mkdir(parents=True)
        (data / f"labs/new/lab{n}/out/{group}/site.hid.json").write_text(json.dumps([card(group, k, n) for k in nums], ensure_ascii=False))
out = subprocess.run([sys.executable, "lab_io.py"], env=os.environ | {"ODS_DATA": str(data)}, check=True, capture_output=True, text=True).stdout
check("lab_io: the cards of three labs, the templates of two", "нових 18" in out and "будова ноутбуків: нових 2" in out, out)

import httpx  # noqa: E402
from aiogram.exceptions import TelegramAPIError  # noqa: E402
from aiogram.types import Chat, Document, Message, MessageOriginChannel, MessageOriginHiddenUser, MessageOriginUser  # noqa: E402
from aiogram.types import User as TgUser  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

import intake_apply  # noqa: E402
import intake_read  # noqa: E402
import labs_pull  # noqa: E402
import main  # noqa: E402
from bot import intake as bot_intake  # noqa: E402
from bot import intake_say  # noqa: E402
from core.bot import notify  # noqa: E402
from core.config import settings  # noqa: E402
from core.models.user import User  # noqa: E402
from lab_store import TOO_BIG  # noqa: E402
from models.lab_file import MAX_BYTES  # noqa: E402

AGENT = {"Authorization": "Bearer tok-123"}
FILES, BROKEN, seq = {}, set(), count(100)


class FakeBot:
    sent, reacted, downloads = [], [], []

    async def send_message(self, chat_id, text, **kw):
        self.sent.append((chat_id, text))

    async def set_message_reaction(self, chat_id, message_id, reaction):
        self.reacted.append((message_id, reaction[0].emoji))

    async def download(self, file_id):
        self.downloads.append(file_id)
        if file_id in BROKEN:
            raise TelegramAPIError(method=None, message="file is temporarily unavailable")
        return io.BytesIO(FILES[file_id])


tg = FakeBot()
notify.bot = lambda: tg


def at(day, hour=10, minute=0):
    return datetime(2026, 11, day, hour, minute, tzinfo=timezone.utc)


def naive(d):
    return d.replace(tzinfo=None)


def person(tg_id, first, last=None, username=None):
    return TgUser(id=tg_id, is_bot=False, first_name=first, last_name=last, username=username)


TEACHER = person(7, "Віталій", username="teacher_tg")


def doc(name, body=b"", size=None, broken=False):
    fid = f"f{len(FILES)}"
    FILES[fid] = body
    if broken:
        BROKEN.add(fid)
    return Document(file_id=fid, file_unique_id=f"u{fid}", file_name=name, file_size=len(body) if size is None else size)


def fwd(origin, text=None, document=None, sender=TEACHER):
    return Message(message_id=next(seq), date=datetime.now(timezone.utc), chat=Chat(id=sender.id, type="private"), from_user=sender,
                   forward_origin=origin, text=None if document else text, caption=text if document else None, document=document)


def by(user, when):
    return MessageOriginUser(date=when, sender_user=user)


def hid(name, when):
    return MessageOriginHiddenUser(date=when, sender_user_name=name)


def nb(vid, line="x=2 y=3", lab=1):
    return fx.notebook(fx.student(vid, lab, line))


OWN = fx.notebook([("code", "import numpy as np\nprint(np.pi)", [], 1), ("markdown", "мої нотатки до пари")])
LAB2 = fx.notebook(lab2(fx.student("КН-1-04", 2, "")))


def login(c, email, status, group="", **fields):
    settings.fake_user_email = email
    c.get("/api/auth/dev-login")
    db.users.update_one({"email": email}, {"$set": {"status": status, "group": group, **fields}})


class Bare:
    """Calls without the session cookie — a guest, an agent."""
    def __getattr__(self, method):
        def call(url, **kw):
            saved, c.cookies = c.cookies, httpx.Cookies()
            try:
                return getattr(c, method)(url, **kw)
            finally:
                c.cookies = saved
        return call


bare = Bare()


async def admin_doc():
    return await User.find_one(User.email == "admin@nure.ua")


async def burst(msgs, admin, timer=False):
    """The messages as aiogram hands them over — at once; `timer` — the silence sends the summary, else it is closed here."""
    sent = len(tg.sent)
    await asyncio.gather(*(bot_intake.forwarded(m, admin) for m in msgs))
    if timer:
        for _ in range(100):
            if len(tg.sent) > sent:
                return tg.sent[-1][1]
            await asyncio.sleep(0.05)
        return ""
    b = bot_intake.BURSTS.pop(TEACHER.id)
    b.timer.cancel()
    return await bot_intake.close(b.ids, b.again, b.other)


async def root(m):
    return await bot_intake.router.message.check_root_filters(m)


def talks(r):
    return {p["key"]: p for p in r.json()["people"]}


with TestClient(main.app) as c:
    run = c.portal.call
    for email, fields in (("a@nure.ua", {"last_name": "Антоненко", "first_name": "Анна", "tg_chat_id": 101, "tg_username": "anna_tg"}),
                          ("b@nure.ua", {"last_name": "Пупкін", "first_name": "Василь"}),
                          ("c@nure.ua", {"last_name": "Сидоренко", "first_name": "Петро"}),
                          ("d@nure.ua", {"last_name": "Дорошенко", "first_name": "Дмитро", "tg_username": "Dmytro_TG"}),
                          ("e@nure.ua", {"last_name": "Єременко", "first_name": "Євген", "tg_chat_id": 105}),
                          ("f@nure.ua", {"last_name": "Федоренко", "first_name": "Фросина"}),
                          ("h@nure.ua", {"last_name": "Гнатенко", "first_name": "Ганна", "tg_chat_id": 108, "group": "КН-2"}),
                          ("z@nure.ua", {"last_name": "Зінченко", "first_name": "Зоя"})):
        login(c, email, "student", **{"group": "КН-1"} | fields)
        if email in ("b@nure.ua", "z@nure.ua"):
            c.post("/api/variants/1/my/claim", json={"n": 2 if email == "b@nure.ua" else 3})
    db.deadlines.insert_many([{"lab": n, "at": naive(at(15, 0)), "groups": [], "created_at": datetime.now(timezone.utc)} for n in (1, 2)])
    db.lab_marks.insert_one({"user": "a@nure.ua", "lab": 1, "until": naive(at(17, 0))})
    login(c, "admin@nure.ua", "admin", tg_chat_id=7, last_name="Викладач")
    admin = run(admin_doc)

    A, D, E, G = person(101, "Анна", "Антоненко", "anna_tg"), person(104, "Дмитро", username="dmytro_tg"), person(105, "Євген"), person(106, "Гліб")
    check("the router: the teacher's forward in the bot's chat passes, with the admin", run(root, fwd(by(A, at(16))))[1].get("admin").email == "admin@nure.ua")
    check("the router: a student's forward and the teacher's own message do not",
          not run(root, fwd(by(A, at(16)), "x", sender=person(101, "Анна")))[0] and not run(root, Message(message_id=1, date=at(16),
              chat=Chat(id=7, type="private"), from_user=TEACHER, text="привіт"))[0])

    got = {n: run(intake_read.read, n, body) for n, body in (("x.ipynb", nb("КН-1-01", "x=5 y=3")), ("lab3.ipynb", nb("КН-1-01", "")),
                                                              ("colab.ipynb", LAB2), ("ЛР3 Сидоренко.ipynb", OWN), ("notes.ipynb", OWN),
                                                              ("empty.ipynb", b'{"cells": []}'), ("lab1.py", b"print(1)"))}
    check("read: the lab by the line, the line against the card's key", (got["x.ipynb"]["lab"], got["x.ipynb"]["ok"], got["x.ipynb"]["total"]) == (1, 1, 2)
          and got["x.ipynb"]["vid"] == "КН-1-01" and got["x.ipynb"]["kind"] == "ipynb" and len(got["x.ipynb"]["sha"]) == 64, got["x.ipynb"])
    check("read: no line — the closest template, over the file's name", got["lab3.ipynb"]["lab"] == 1 and got["colab.ipynb"]["lab"] == 2
          and got["colab.ipynb"]["ok"] is None, (got["lab3.ipynb"]["lab"], got["colab.ipynb"]["lab"]))
    check("read: no template close — the name; nothing — None", got["ЛР3 Сидоренко.ipynb"]["lab"] == 3 and got["notes.ipynb"]["lab"] is None
          and got["empty.ipynb"]["lab"] is None and got["empty.ipynb"]["kind"] == "ipynb")
    check("read: not a notebook — the words, the bytes kept", got["lab1.py"]["why"] == intake_read.NOT_NB and got["lab1.py"]["kind"] == ""
          and got["lab1.py"]["raw"])

    # burst 1: a student known by Telegram, the teacher's reply, a repeat, a channel, not a notebook, too big — the timer sends the summary
    bot_intake.QUIET = 0.05
    first = doc("lab1_anna.ipynb", nb("КН-1-01"))
    say = run(burst, [fwd(by(A, at(16)), "ось лаба", first), fwd(by(TEACHER, at(16, 10, 5)), "Дякую, прийняв, можна здати й пізніше"),
                      fwd(by(A, at(16, 10, 6)), "А можна здати другу пізніше?"), fwd(by(A, at(16)), "ось лаба", first),
                      fwd(MessageOriginChannel(date=at(16), chat=Chat(id=-100, type="channel", title="Новини"), message_id=5), "новина"),
                      fwd(by(A, at(16, 10, 7)), "звіт", doc("report.pdf", b"%PDF-1.4")), fwd(by(A, at(16, 10, 8)), None, doc("big.ipynb", size=MAX_BYTES + 1))],
              admin, True)
    rows = list(db.forwards.find({"key": "tg:101"}).sort("sent_at"))
    check("burst: one document per message, the repeat and the channel not stored", db.forwards.count_documents({}) == 5 and len(rows) == 5, len(rows))
    check("burst: ✍ on each but the channel's; one download — the notebook", len(tg.reacted) == 6 and {e for _, e in tg.reacted} == {"✍"}
          and tg.downloads == [first.file_id], (tg.reacted, tg.downloads))
    mine = next(r for r in rows if r["mine"])
    check("the teacher's line joins the talk and its student; no 🙋 on it", mine["key"] == "tg:101" and mine["student"] == "a@nure.ua"
          and not mine["asks"] and next(r for r in rows if "другу" in r["text"])["asks"], mine)
    check("known by Telegram: every row is theirs for sure", {(r["student"], r["how"]) for r in rows} == {("a@nure.ua", "tg")})
    f = db.lab_files.find_one({"student": "a@nure.ua"})
    v = db.variants.find_one({"lab": 1, "vid": "КН-1-01"})
    check("the notebook → a version with the message's time, via telegram, by the teacher", f and f["at"] == naive(at(16)) and f["via"] == "telegram"
          and f["by"] == "admin@nure.ua" and rows[0]["version"] == str(f["_id"]), f and {k: f[k] for k in ("at", "via", "by")})
    check("…and the card took itself, the line an attempt at that time", v["student"] == "a@nure.ua" and v["attempts"] == 1
          and v["checked_at"] == naive(at(16)) and v["file"]["via"] == "telegram", {k: v[k] for k in ("student", "attempts", "checked_at")})
    big, pdf = next(r for r in rows if r["file"].get("name") == "big.ipynb"), next(r for r in rows if r["file"].get("name") == "report.pdf")
    check("too big and not a notebook: words, no bytes, no kind", big["why"] == TOO_BIG and pdf["why"] == intake_read.NOT_NB
          and not big["raw"] and not pdf["raw"] and not big["kind"])
    check("summary: one, to the teacher, after the silence", len(tg.sent) == 1 and tg.sent[0][0] == 7)
    check("summary: who, the notebook line, messages and 🙋, repeats, the channel, the link", "🎓 <b><a href=" in say and "Антоненко Анна" in say
          and "📓 Лаба 1 · КН-1-01 · 2/2 ✅ · 16.11 12:00 · на сайті" in say and "💬 повідомлень: 5 · 🙋 просить час" in say
          and "♻️ вже були: 1" in say and "📢 з груп і каналів не беру: 1" in say and "/intake\">Вхідні</a>" in say
          and "📎 report.pdf · Не ноутбук" in say and "📎 big.ipynb · Файл завеликий" in say, say)

    # burst 2: hidden accounts, unknown ones, a link, a foreign card, a demo card, Telegram failing — closed here, without the timer
    bot_intake.QUIET = 60

    async def pulled(link):
        return LAB2

    labs_pull.pull = pulled
    say = run(burst, [fwd(hid("Вася П.", at(14, 9)), "лаба 1", doc("lab1.ipynb", nb("КН-1-02"))),
                      fwd(hid("Петро Сидоренко", at(14, 9, 30)), None, doc("ЛР3 Сидоренко.ipynb", OWN)),
                      fwd(by(D, at(16, 11)), "ось https://colab.research.google.com/drive/1AbC-dEf_ghIJkl"),
                      fwd(by(D, at(16, 11, 1)), None, doc("notes.ipynb", OWN)), fwd(by(D, at(16, 11, 2)), None, doc("lab2_final.ipynb", b"{}", broken=True)),
                      fwd(by(E, at(13, 9)), "моя", doc("lab1_e.ipynb", nb("КН-1-03"))), fwd(by(G, at(13, 9)), "демо", doc("demo.ipynb", nb("ДЕМО-00")))], admin)
    check("summary without the timer: the unknown by name and nick, the known with the reason in the teacher's words",
          "❓ Вася П. · не впізнаю" in say and "❓ Дмитро · @dmytro_tg · не впізнаю" in say and "Єременко Євген" in say
          and "⚠️ Картку КН-1-03 тримає Зінченко Зоя" in say and "Telegram не віддав файл: file is temporarily unavailable" in say
          and "📓 Лаба 2 · КН-1-04 · без рядка · 16.11 13:00" in say and "📓 Лаба ? · без рядка" in say and len(tg.sent) == 1, say)
    check("summary: the guess next to the unknown, and why", "не впізнаю · схоже, Пупкін Василь (за карткою)" in say
          and "@dmytro_tg · не впізнаю · схоже, Дорошенко Дмитро (за ніком)" in say and "Петро Сидоренко · не впізнаю · схоже, Сидоренко Петро (за імʼям)" in say
          and "❓ Гліб · не впізнаю\n" in say, say)

    login(c, "admin@nure.ua", "admin", tg_chat_id=7, last_name="Викладач")
    r = c.get("/api/intake")
    p = talks(r)
    check("INTAKE: people the newest talk first, rows the oldest first", r.status_code == 200 and r.json()["people"][0]["key"] == "tg:104"
          and [x["sent_at"][:16] for x in p["tg:101"]["rows"]] == ["2026-11-16T10:00", "2026-11-16T10:05", "2026-11-16T10:06", "2026-11-16T10:07", "2026-11-16T10:08"])
    a = p["tg:101"]
    check("PERSON: the student, how, no guess, the Telegram name", a["student"] == {"nick": "a", "name": "Антоненко Анна", "group": "КН-1"}
          and a["how"] == "tg" and a["guess"] is None and (a["name"], a["username"], a["tg_id"]) == ("Анна Антоненко", "anna_tg", 101), a)
    f1 = a["rows"][0]["file"]
    check("FILE: the student's own deadline (an extension) — on time", f1["due"].startswith("2026-11-17T00:00") and f1["late"] is False
          and f1["version"] and f1["line"] is True and (f1["ok"], f1["total"]) == (2, 2) and a["rows"][1]["mine"] and a["rows"][1]["file"] is None, f1)
    check("guesses: the card held on the site, the name, the nick", p["name:Вася П."]["guess"] == {"nick": "b", "name": "Пупкін Василь", "group": "КН-1", "why": "card"}
          and p["name:Петро Сидоренко"]["guess"]["nick"] == "c" and p["name:Петро Сидоренко"]["guess"]["why"] == "name"
          and (p["tg:104"]["guess"]["nick"], p["tg:104"]["guess"]["why"]) == ("d", "username") and p["tg:106"]["guess"] is None)
    d = p["tg:104"]["rows"]
    check("the link: the notebook behind it, the lab by the template; nobody's — the common deadline, late", d[0]["file"]["link"].startswith("https://colab")
          and d[0]["file"]["name"] == "colab.ipynb" and d[0]["file"]["lab"] == 2 and d[0]["file"]["due"].startswith("2026-11-15") and d[0]["file"]["late"] is True, d[0]["file"])
    check("no lab known, no deadline; Telegram failed — words", d[1]["file"]["lab"] is None and d[1]["file"]["due"] is None and d[1]["file"]["late"] is None
          and d[2]["file"]["why"].startswith("Telegram не віддав файл") and d[2]["file"]["kind"] == "")
    e = p["tg:105"]["rows"][0]["file"]
    check("a card another student holds: no version, the trouble in the teacher's words", p["tg:105"]["student"]["nick"] == "e"
          and not e["version"] and e["trouble"] == "Картку КН-1-03 тримає Зінченко Зоя", e)
    strips = {s["lab"]: s for s in r.json()["strips"]}
    s1 = strips[1]
    check("strips: a lab with notebooks; top — the stream's last number; the demo left out", sorted(strips) == [1, 2] and s1["top"] == 5
          and [x["n"] for x in s1["cells"]] == [1, 2, 3] and s1["due"].startswith("2026-11-15"), strips)
    check("strip cells: who (the student or the Telegram name), when, n/N, late, the row", s1["cells"][0]["who"] == "Антоненко Анна"
          and s1["cells"][1]["who"] == "Вася П." and s1["cells"][1]["late"] is False and (s1["cells"][0]["ok"], s1["cells"][0]["total"]) == (2, 2)
          and s1["cells"][0]["id"] == a["rows"][0]["id"] and strips[2]["cells"][0]["n"] == 4 and strips[2]["cells"][0]["late"] is True, s1["cells"])
    check("strip cells: whether the number's file is on the site already", [x["version"] for x in s1["cells"]] == [True, False, False], s1["cells"])

    r = c.put("/api/intake/person", json={"key": "name:Вася П.", "student": "b"})
    b = talks(r)["name:Вася П."]
    fb = db.lab_files.find_one({"student": "b@nure.ua"})
    check("the teacher's word: the talk is theirs, the notebook a version with the message's time", b["student"]["nick"] == "b" and b["how"] == "hand"
          and b["guess"] is None and b["rows"][0]["file"]["version"] == str(fb["_id"]) and fb["at"] == naive(at(14, 9)) and fb["via"] == "telegram", b)
    check("the teacher's word: an unknown nick, an unknown talk — 404", c.put("/api/intake/person", json={"key": "name:Вася П.", "student": "nobody"}).status_code == 404
          and c.put("/api/intake/person", json={"key": "tg:1", "student": "b"}).status_code == 404)
    run(burst, [fwd(hid("Вася П.", at(14, 9, 5)), "і ще питання")], admin)
    check("one more forward of a talk the teacher named: theirs at once", db.forwards.find_one({"text": "і ще питання"})["student"] == "b@nure.ua"
          and db.forwards.find_one({"text": "і ще питання"})["how"] == "hand")
    long = intake_say.pages("\n\n".join(["📓 " + "x" * 1500] * 5))
    check("a long summary: several messages, split between talks", len(long) == 3 and all(len(x) <= intake_say.LIMIT for x in long)
          and intake_say.pages("a\n\nb") == ["a\n\nb"])

    run(burst, [fwd(by(A, at(14, 8)), "стара", doc("lab1_old.ipynb", nb("КН-1-01", "x=5 y=3"))),
                fwd(by(A, at(15, 9)), "не та", doc("lab1_b.ipynb", nb("КН-1-02")))], admin)
    check("the student holds another card of the lab: the trouble in the teacher's words",
          db.forwards.find_one({"text": "не та"})["trouble"] == "У файлі картка КН-1-02, а студент тримає КН-1-01")
    v = db.variants.find_one({"lab": 1, "vid": "КН-1-01"})
    old = db.lab_files.find_one({"student": "a@nure.ua", "at": naive(at(14, 8))})
    check("an earlier file found later: a version of its time, the card keeps the newest", old and v["files"] == 2 and v["file"]["id"] == str(f["_id"])
          and v["values"] == {"x": 2, "y": 3} and v["attempts"] == 1, {k: v[k] for k in ("files", "values", "attempts")})

    eid = p["tg:105"]["rows"][0]["id"]
    c.put("/api/variants/1/results/КН-1-03", json={"student": ""})
    e = talks(c.get("/api/intake"))["tg:105"]["rows"][0]["file"]
    check("a page load does not try a failed row again", not e["version"] and e["trouble"].startswith("Картку КН-1-03"), e)
    r = c.post(f"/api/intake/{eid}/apply")
    e = talks(r)["tg:105"]["rows"][0]["file"]
    check("the trouble fixed (the card freed) → once more: a version, the trouble gone", e["version"] and e["trouble"] == ""
          and db.variants.find_one({"lab": 1, "vid": "КН-1-03"})["student"] == "e@nure.ua", e)

    r = c.put("/api/intake/person", json={"key": "tg:104", "student": "@d"})
    d = talks(r)["tg:104"]["rows"]
    check("the link's notebook goes over too; a row without a lab waits", d[0]["file"]["version"] and not d[1]["file"]["version"] and not d[1]["file"]["trouble"])
    r = c.put(f"/api/intake/{d[1]['id']}", json={"lab": 1})
    d = talks(r)["tg:104"]["rows"]
    check("the teacher names the lab: it goes over", d[1]["file"]["lab"] == 1 and d[1]["file"]["version"] and d[1]["file"]["ok"] is None, d[1]["file"])
    check("a lab of a row already on the site — 409, out of range — 422", c.put(f"/api/intake/{d[1]['id']}", json={"lab": 2}).status_code == 409
          and c.put(f"/api/intake/{p['name:Петро Сидоренко']['rows'][0]['id']}", json={"lab": 9}).status_code == 422)

    pid = p["name:Петро Сидоренко"]["rows"][0]["id"]
    c.put(f"/api/intake/{pid}", json={"skip": True})
    r = c.put("/api/intake/person", json={"key": "name:Петро Сидоренко", "student": "c"})
    row = talks(r)["name:Петро Сидоренко"]["rows"][0]
    check("set aside: not taken over", row["skip"] and not row["file"]["version"] and not row["file"]["trouble"], row)
    r = c.put(f"/api/intake/{pid}", json={"skip": False})
    row = talks(r)["name:Петро Сидоренко"]["rows"][0]
    check("back: tried, the reason — no card in the file", not row["skip"] and "VARIANT" in row["file"]["trouble"] and row["file"]["lab"] == 3, row)
    aid = a["rows"][2]["id"]
    check("🙋 is the teacher's switch", talks(c.put(f"/api/intake/{aid}", json={"asks": False}))["tg:101"]["rows"][2]["asks"] is False)
    r = c.put("/api/intake/person", json={"key": "name:Вася П.", "student": ""})
    b = talks(r)["name:Вася П."]
    check("nobody's again: the student gone, the version stays", b["student"] is None and b["how"] == "" and b["rows"][0]["file"]["version"]
          and b["guess"]["why"] == "card" and db.lab_files.count_documents({"student": "b@nure.ua"}) == 1, b)
    check("once more: no notebook, no student — 422", c.post(f"/api/intake/{a['rows'][3]['id']}/apply").status_code == 422
          and c.post(f"/api/intake/{p['tg:106']['rows'][0]['id']}/apply").status_code == 422)
    raw = c.get(f"/api/intake/{a['rows'][0]['id']}/raw")
    check("raw: the file as it came; none downloaded — 404", raw.content == nb("КН-1-01") and "lab1_anna.ipynb" in raw.headers["content-disposition"]
          and c.get(f"/api/intake/{a['rows'][3]['id']}/raw").status_code == 404)

    F = person(107, "Фрося")
    run(burst, [fwd(by(F, at(15, 9)), None, doc("lab1.ipynb", nb("КН-1-05")))], admin)
    db.users.update_one({"email": "f@nure.ua"}, {"$set": {"tg_chat_id": 107}})

    async def mine_settled(email):
        return await intake_apply.settle(await User.find_one(User.email == email))

    check("«Моя лаба» settles its student: linked the bot — the file and the card are there", run(mine_settled, "f@nure.ua") == 1
          and db.variants.find_one({"lab": 1, "vid": "КН-1-05"})["student"] == "f@nure.ua" and db.forwards.find_one({"tg_id": 107})["how"] == "tg")
    run(burst, [fwd(by(person(108, "Ганна"), at(15, 10)), None, doc("lab2.ipynb", fx.notebook(lab2(fx.student("КН-1-03", 2)))))], admin)
    db.users.update_one({"email": "h@nure.ua"}, {"$set": {"group": "КН-1"}})
    h = talks(c.get("/api/intake"))["tg:108"]["rows"][0]["file"]
    check("a wrong group: the trouble; fixed in the profile — a page load leaves it", "не з твого потоку" in h["trouble"] and not h["version"], h)
    check("…«Моя лаба» of that student tries it again: a version", run(mine_settled, "h@nure.ua") == 1
          and db.forwards.find_one({"tg_id": 108})["version"] and db.forwards.find_one({"tg_id": 108})["trouble"] == "")

    bot_intake.QUIET, intake_say.LIMIT, sent = 0.05, 60, len(tg.sent)
    run(burst, [fwd(by(TEACHER, at(17)), "нагадую всім про дедлайн")], admin, True)
    run(asyncio.sleep, 0.3)
    intake_say.LIMIT = 4096
    check("the timer sends a long summary in parts", len(tg.sent) == sent + 3 and tg.sent[-2][1].startswith("🧑‍🏫 Лише твої"), tg.sent[sent:])
    check("the teacher's lines of nobody's talk: not among the people", "" not in talks(c.get("/api/intake"))
          and db.forwards.count_documents({"key": "", "mine": True}) == 1)
    check("no alerts about files", db.events.count_documents({"kind": "lab"}) == 0)

    check("rights: a guest 401, an agent 200", bare.get("/api/intake").status_code == 401 and bare.get("/api/intake", headers=AGENT).status_code == 200)
    login(c, "a@nure.ua", "student", "КН-1")
    check("rights: a student 403", c.get("/api/intake").status_code == 403 and c.put("/api/intake/person", json={"key": "tg:101", "student": ""}).status_code == 403
          and c.get(f"/api/intake/{a['rows'][0]['id']}/raw").status_code == 403)

print(f"\n{sum(ok for _, ok in results)}/{len(results)} PASS")
sys.exit(not all(ok for _, ok in results))
