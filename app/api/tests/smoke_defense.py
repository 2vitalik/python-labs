"""Smoke: a defense from start to «прийнято» (T326) — the teacher starts it, dictates remarks, marks impressions, sends;
the student answers with a link; the teacher accepts or returns; an agent with a token reads and proposes, never decides.
Run from app/api: DB_NAME=python_labs_t326_defense_smoke TG_BOT_TOKEN= uv run python tests/smoke_defense.py"""
import os
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

settings.agent_tokens = "claude:tok"
settings.remark_coins = "draft"
AGENT = {"Authorization": "Bearer tok"}
D, MY = "/api/defenses", "/api/my/remarks"
REPO = "https://github.com/stud/game"
COMMIT = f"{REPO}/commit/0123abc"
results = []


def check(name, cond, extra=""):
    results.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def login(c, email, status):
    settings.fake_user_email = email
    c.get("/api/auth/dev-login")
    mongo[DB].users.update_one({"email": email}, {"$set": {"status": status, "group": "ПЗПІ-25-1", "github": REPO if status == "student" else ""}})


with TestClient(main.app) as c:
    login(c, "stud@nure.ua", "student")
    check("a student: no defenses yet", c.get(MY).json()["defenses"] == [])
    check("the teacher's routes are closed to a student", c.get(D).status_code == 403 and c.post(D, json={"nick": "stud"}).status_code == 403
          and c.get(f"{D}/vocab").status_code == 403)

    login(c, "admin@nure.ua", "admin")
    v = c.get(f"{D}/vocab").json()
    check("the words: tags, kinds, four-step scales, facts", {t["key"] for t in v["tags"]} >= {"naming", "dup", "other"} and len(v["remark_kinds"]) == 4
          and all(len(r["steps"]) == 4 for r in v["rates"]) and v["facts"] and v["coins"] == "draft", v.keys())
    check("an unknown student → 404, an unknown lab or kind → 422", c.post(D, json={"nick": "nobody"}).status_code == 404
          and c.post(D, json={"nick": "stud", "labs": [9]}).status_code == 422 and c.post(D, json={"nick": "stud", "kind": "chat"}).status_code == 422)
    d = c.post(D, json={"nick": "stud", "labs": [3, 2, 3]}).json()
    did = d["id"]
    check("a new defense: started now, labs sorted, no end", d["started_at"] and d["ended_at"] is None and d["labs"] == [2, 3]
          and d["student"]["nick"] == "stud" and d["result"] == "", d)

    text = "- назви змінних a, b, c незрозумілі\n2. метод update великий і в ньому дублюється код\n\n   гра падає, коли ворогів нема\nна майбутнє: спробуй dataclass\nщось зовсім інше"
    rows = c.post(f"{D}/{did}/remarks", json={"text": text}).json()
    check("a line — a remark, markers and blank lines gone", [r["text"] for r in rows][:2] == ["назви змінних a, b, c незрозумілі", "метод update великий і в ньому дублюється код"]
          and len(rows) == 5 and all(r["state"] == "draft" for r in rows), rows)
    check("the first guess: tags by words, two at most; a bug is a debt, «на майбутнє» a tip; nothing found — no tag",
          rows[0]["tags"] == ["naming"] and set(rows[1]["tags"]) == {"size", "dup"} and (rows[2]["tags"], rows[2]["kind"]) == (["bug"], "debt")
          and rows[3]["kind"] == "tip" and (rows[4]["tags"], rows[4]["kind"]) == ([], "better"), [(r["tags"], r["kind"]) for r in rows])
    check("no lines → 422", c.post(f"{D}/{did}/remarks", json={"text": " \n - \n"}).status_code == 422)
    rid = [r["id"] for r in rows]

    r = c.put(f"/api/remarks/{rid[4]}", json={"tags": ["structure", "oop"], "kind": "quest", "coin": "bronze"}).json()
    check("the teacher sets tags, kind, a reward: they are the teacher's own now", r["tags"] == ["structure", "oop"] and r["kind"] == "quest"
          and (r["coin"], r["amount"]) == ("bronze", 1) and set(r["own"]) == {"tags", "kind"}, r)
    r = c.put(f"/api/remarks/{rid[4]}", json={"kind": "debt"}).json()
    check("a debt carries no reward", (r["kind"], r["coin"], r["amount"]) == ("debt", "", 0), r)
    check("an unknown tag, three tags, an empty text → 422", all(c.put(f"/api/remarks/{rid[0]}", json=j).status_code == 422 for j in (
        {"tags": ["nope"]}, {"tags": ["naming", "dup", "size"]}, {"text": "  "}, {"kind": "fine"}, {"coin": "diamond"})))

    r = c.put(f"/api/remarks/{rid[4]}", json={"tags": ["bug"], "kind": "tip", "text": "Винести логіку гри з класу вікна", "like": rid[1]}, headers=AGENT).json()
    check("an agent: the teacher's tags and kind stay, the text is a proposal", r["tags"] == ["structure", "oop"] and r["kind"] == "debt"
          and r["text"] == "щось зовсім інше" and r["hint"] == {"text": "Винести логіку гри з класу вікна", "like": rid[1], "by": "claude@agent"}, r)
    r = c.put(f"/api/remarks/{rid[0]}", json={"tags": ["naming", "style"], "kind": "debt"}, headers=AGENT).json()
    check("an agent: tags and kind land where the teacher has not set them", r["tags"] == ["naming", "style"] and r["kind"] == "debt" and r["own"] == [], r)
    r = c.put(f"/api/remarks/{rid[4]}", json={"text": "Винести логіку гри з класу вікна"}).json()
    check("the teacher takes the proposal: the dictated line stays as raw, the proposal is spent", r["text"].startswith("Винести") and r["raw"] == "щось зовсім інше"
          and "text" not in r["hint"] and "text" in r["own"], r)

    p = c.put(f"{D}/{did}", json={"facts": {"own": "yes", "changes": "partly"}, "rates": {"grasp": 3, "all": 3.5}, "marks": ["star"], "note": "сильний, але квапиться",
                                  "result": "cond"}).json()
    check("impressions: facts, steps with a half, marks, a note, the result", p["facts"] == {"own": "yes", "changes": "partly"} and p["rates"] == {"grasp": 3, "all": 3.5}
          and p["marks"] == ["star"] and p["note"] and p["result"] == "cond" and p["scale"] == v["scale"], p)
    check("an unknown fact, step or mark → 422", all(c.put(f"{D}/{did}", json=j).status_code == 422 for j in (
        {"facts": {"own": "maybe"}}, {"facts": {"nope": "yes"}}, {"rates": {"grasp": 5}}, {"rates": {"all": 2.2}}, {"marks": ["nope"]}, {"result": "ok"})))
    check("the end before the start → 422", c.put(f"{D}/{did}", json={"ended_at": "2020-01-01T10:00:00Z"}).status_code == 422)

    a = c.get(f"{D}/{did}", headers=AGENT).json()
    check("an agent reads the defense without the teacher's own", a["remarks"] and not {"facts", "rates", "marks", "note", "rank"} & a.keys() and a["student"]["github"] == REPO, a.keys())
    c.cookies.clear()  # an agent has no session: the token is all it comes with
    check("an agent may not start, change, send or delete a defense, nor delete a remark", all(s == 401 for s in (
        c.post(D, json={"nick": "stud"}, headers=AGENT).status_code, c.put(f"{D}/{did}", json={"note": "x"}, headers=AGENT).status_code,
        c.post(f"{D}/{did}/send", headers=AGENT).status_code, c.delete(f"{D}/{did}", headers=AGENT).status_code,
        c.delete(f"/api/remarks/{rid[0]}", headers=AGENT).status_code)) and c.get(D, headers=AGENT).status_code == 200)
    login(c, "admin@nure.ua", "admin")
    check("an opinion before any reply → 422; a word on a draft → 422", c.put(f"/api/remarks/{rid[0]}/check", json={"state": "accepted"}, headers=AGENT).status_code == 422
          and c.put(f"/api/remarks/{rid[0]}/check", json={"state": "accepted"}).status_code == 422)

    login(c, "stud@nure.ua", "student")
    check("drafts are not the student's yet", c.get(MY).json()["defenses"] == [] and c.put(f"{MY}/{rid[0]}", json={"state": "fixed", "link": COMMIT}).status_code == 404)
    login(c, "admin@nure.ua", "admin")
    s = c.post(f"{D}/{did}/send").json()
    full = c.get(f"{D}/{did}").json()
    check("send: every draft opens, the defense ends", s == {"sent": 5} and full["sent_at"] and full["ended_at"] and full["minutes"] == 0
          and full["counts"]["open"] == 5 and full["counts"]["debts"] == 3, full["counts"])
    check("a sent defense is not deleted", c.delete(f"{D}/{did}").status_code == 422)

    login(c, "stud@nure.ua", "student")
    mine = c.get(MY).json()
    m = mine["defenses"][0]
    check("the student sees the result and the remarks — nothing of the teacher's own", m["result"] == "cond" and len(m["remarks"]) == 5
          and not {"facts", "rates", "marks", "note", "student"} & m.keys() and not {"raw", "hint", "own", "agent"} & m["remarks"][0].keys()
          and "facts" not in mine["vocab"] and mine["vocab"]["coins"] == "off" and all(r["coin"] == "" for r in m["remarks"]), m.keys())
    check("«done» needs a link, «not done» a line, the link is GitHub's", c.put(f"{MY}/{rid[0]}", json={"state": "fixed"}).status_code == 422
          and c.put(f"{MY}/{rid[0]}", json={"state": "skipped"}).status_code == 422
          and c.put(f"{MY}/{rid[0]}", json={"state": "fixed", "link": "https://gitlab.com/x/y"}).status_code == 422)
    r = c.put(f"{MY}/{rid[0]}", json={"state": "fixed", "link": COMMIT.removeprefix("https://"), "note": " перейменував "}).json()
    check("an answer with a commit: answered, the scheme added, the link is fine", r["state"] == "answered" and r["reply"]["link"] == COMMIT
          and r["reply"]["note"] == "перейменував" and r["reply"]["link_note"] == "", r)
    r1 = c.put(f"{MY}/{rid[1]}", json={"state": "partly", "link": f"{REPO}/blob/main/game.py#L10"}).json()
    r2 = c.put(f"{MY}/{rid[2]}", json={"state": "fixed", "link": "https://github.com/other/repo/commit/abc1234"}).json()
    check("a link to a branch and a link to another repo are told apart", (r1["reply"]["link_note"], r2["reply"]["link_note"]) == ("branch", "foreign"), (r1, r2))
    check("somebody else's remark → 404", c.put(f"{MY}/{'0' * 24}", json={"state": "fixed", "link": COMMIT}).status_code == 404)
    c.put(f"{MY}/{rid[3]}", json={"state": "skipped", "note": "подивлюсь пізніше"})
    c.put(f"{MY}/{rid[4]}", json={"state": "ask", "note": "не розумію, що саме винести"})

    login(c, "admin@nure.ua", "admin")
    o = c.put(f"/api/remarks/{rid[0]}/check", json={"state": "accepted", "note": "коміт бачу"}, headers=AGENT).json()
    check("an agent's opinion sits next to the reply; the remark still waits for the teacher", o["agent"]["state"] == "accepted" and o["agent"]["by"] == "claude@agent"
          and o["state"] == "answered" and o["check"] == {}, o)
    check("to return, say why", c.put(f"/api/remarks/{rid[1]}/check", json={"state": "returned"}).status_code == 422)
    ok = c.put(f"/api/remarks/{rid[0]}/check", json={"state": "accepted"}).json()
    back = c.put(f"/api/remarks/{rid[1]}/check", json={"state": "returned", "note": "дублювання лишилось у draw()"}).json()
    check("the teacher's word: accepted, returned with a line", (ok["state"], back["state"], back["check"]["note"]) == ("accepted", "returned", "дублювання лишилось у draw()"), (ok, back))
    check("an answered remark is not deleted", c.delete(f"/api/remarks/{rid[2]}").status_code == 422)
    row = next(x for x in c.get(D).json() if x["id"] == did)
    check("the list: where the remarks stand", (row["counts"]["accepted"], row["counts"]["returned"], row["counts"]["answered"], row["counts"]["all"]) == (1, 1, 3, 5)
          and row["student"]["nick"] == "stud" and row["rates"] == {"grasp": 3, "all": 3.5}, row)
    check("the list of one student, of nobody", len(c.get(f"{D}?nick=stud").json()) == 1 and c.get(f"{D}?nick=nobody").json() == [])

    login(c, "stud@nure.ua", "student")
    check("an accepted remark takes no more answers", c.put(f"{MY}/{rid[0]}", json={"state": "fixed", "link": COMMIT}).status_code == 422)
    again = c.put(f"{MY}/{rid[1]}", json={"state": "fixed", "link": COMMIT}).json()
    check("a returned one is answered again; the teacher's line stays to read", again["state"] == "answered" and again["check"]["note"].startswith("дублювання"), again)

    login(c, "admin@nure.ua", "admin")
    d2 = c.post(D, json={"nick": "stud", "labs": [4], "kind": "live"}).json()
    page = c.get(f"{D}/{d2['id']}").json()
    check("the next defense opens with what is owed from the first", {r["id"] for r in page["debts"]} == {rid[1], rid[2], rid[4]}
          and [o["id"] for o in page["others"]] == [did], page["debts"])
    c.post(f"{D}/{d2['id']}/remarks", json={"text": "чернетка"})
    check("a defense not sent yet goes away with its drafts", c.delete(f"{D}/{d2['id']}").status_code == 204 and c.get(f"{D}/{d2['id']}").status_code == 404
          and mongo[DB].remarks.count_documents({}) == 5)
    hist = mongo[DB].history.count_documents({"coll": {"$in": ["defenses", "remarks"]}})
    check("every change is in the history", hist > 20, hist)
    events = [e["text"] for e in mongo[DB].events.find({"kind": "defense"})]
    check("alerts: sent, and once the student answered them all", len(events) == 3 and "надіслано зауважень: 5" in events[0] and "відповів на всі" in events[1], events)

ok = sum(results)
print(f"\n{ok}/{len(results)} PASS")
sys.exit(0 if ok == len(results) else 1)
