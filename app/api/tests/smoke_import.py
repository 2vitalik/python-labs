"""Smoke: student import tells CIST from DL per row (2026-10-23) — a DL paste with tabs and one flattened to spaces,
the teacher skipped, groups from the row, re-import updates the group and leaves names alone. Run from app/api:
DB_NAME=python_labs_smoke uv run python tests/smoke_import.py"""
import os
import sys

sys.path.insert(0, os.getcwd())
from pymongo import MongoClient  # noqa: E402

DB = os.environ["DB_NAME"]
assert DB.endswith("_smoke"), "refuse to run on a non-smoke DB"
MongoClient().drop_database(DB)
db = MongoClient()[DB]
from fastapi.testclient import TestClient  # noqa: E402

import main  # noqa: E402
from core.config import settings  # noqa: E402
from core.routes.students import parse_students  # noqa: E402

ADMIN = "admin@nure.ua"
settings.admin_emails, settings.tg_bot_token, settings.tg_bot_name = ADMIN, "", "smoke_bot"
results = []

CIST = ("Список групи ПЗПІ-25-1 (анг)\n№\tПрізвище, ім'я, по батькові\t№ залікової книжки\tКонтракт\tПримітки\n"
        "1\nПетренко Петро Петрович\t25.F2 ПЗПІ.0101\t \tpetro.petrenko@nure.ua\n"
        "2\nІваненко Іван\t25.F2 ПЗПІ.0102\t \tivan.ivanenko@nure.ua\n"
        "Список групи ПЗПІ-25-2\n1\nСидоренко Сидір Сидорович\t25.F2 ПЗПІ.0201\t \tsydir.sydorenko@nure.ua\n")
DL = ('Виберіть "Петренко Петро"\n\tПетренко Петро\tpetro.petrenko@nure.ua\tСтудент\tПЗПІпз-25-1\t1 година 8 хв\t\nАктивний\n'
      'Виберіть "Ляпота Віталій Миколайович"\n\tЛяпота Віталій Миколайович\tteacher@nure.ua\tВикладач\tНемає груп\t30 сек\t\nАктивний\n'
      'Виберіть "Коваль Марія"\n\tКоваль Марія\tmariia.koval.cpe@nure.ua\tСтудент\tПЗПІпз-25-1\tНіколи\t\nАктивний\n'
      'Виберіть "Бондар Олег"\n\tБондар Олег\toleh.bondar.cpe@nure.ua\tСтудент\tНемає груп\tНіколи\t\nАктивний\n')
DL_SPACES = DL.replace("\t", "    ")


def check(name, cond, extra=""):
    results.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


rows = parse_students(CIST)
check("cist: 3 rows, groups from headers", [(r["email"], r["group"]) for r in rows] == [
    ("petro.petrenko@nure.ua", "ПЗПІ-25-1"), ("ivan.ivanenko@nure.ua", "ПЗПІ-25-1"), ("sydir.sydorenko@nure.ua", "ПЗПІ-25-2")], rows)
check("cist: ПІБ split", rows[0]["last_name"] == "Петренко" and rows[0]["first_name"] == "Петро" and rows[0]["patronymic"] == "Петрович", rows[0])
for name, text in (("dl tabs", DL), ("dl spaces", DL_SPACES)):
    rows = parse_students(text)
    check(f"{name}: students only, teacher skipped", [r["email"] for r in rows] == ["petro.petrenko@nure.ua", "mariia.koval.cpe@nure.ua", "oleh.bondar.cpe@nure.ua"], rows)
    check(f"{name}: group from the row, «Немає груп» → empty", [r["group"] for r in rows] == ["ПЗПІпз-25-1", "ПЗПІпз-25-1", ""], rows)
    check(f"{name}: names", (rows[1]["last_name"], rows[1]["first_name"], rows[1]["patronymic"]) == ("Коваль", "Марія", ""), rows[1])
rows = parse_students(CIST + DL)
check("mixed paste: cist rows keep header groups, dl rows their own", [r["group"] for r in rows] == ["ПЗПІ-25-1", "ПЗПІ-25-1", "ПЗПІ-25-2", "ПЗПІпз-25-1", "ПЗПІпз-25-1", "ПЗПІ-25-2"], rows)

with TestClient(main.app) as c:
    settings.fake_user_email = ADMIN
    c.get("/api/auth/dev-login", follow_redirects=False)
    r = c.post("/api/students/import", json={"text": CIST}).json()
    check("import cist: 3 added", r == {"added": 3, "updated": 0, "unchanged": 0}, r)
    r = c.post("/api/students/import", json={"text": DL}).json()
    check("import dl: 2 added, petro's group refreshed, teacher not added", r == {"added": 2, "updated": 1, "unchanged": 0}, r)
    users = {u["email"]: u for u in db.users.find()}
    check("petro: group from dl, ПІБ from cist kept", users["petro.petrenko@nure.ua"]["group"] == "ПЗПІпз-25-1"
          and users["petro.petrenko@nure.ua"]["patronymic"] == "Петрович", users["petro.petrenko@nure.ua"])
    check("teacher absent, the imported are students", "teacher@nure.ua" not in users
          and all(u["status"] == "student" for e, u in users.items() if e != ADMIN), sorted(users))
    r = c.post("/api/students/import", json={"text": DL}).json()
    check("import dl again: unchanged", r == {"added": 0, "updated": 0, "unchanged": 3}, r)

ok = sum(results)
print(f"\n{ok}/{len(results)} PASS")
sys.exit(0 if ok == len(results) else 1)
