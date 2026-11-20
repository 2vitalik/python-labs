"""INTAKE (T368 §2.6): the forwards by talk — whose, a guess while nobody's, every row with its file and that file's deadline —
and a strip of the stream's card numbers per lab: which numbers sent a notebook and when."""
from beanie.operators import In
from pydantic import BaseModel

from core.labs import due_for, utc
from core.models.deadline import Deadline, LabMark
from core.models.history import when
from core.models.user import User
from intake_match import clues, guess, who
from lab_claim import DEMO
from lab_my import due_at
from models.forward import Forward, ForwardHead
from models.lab import LabVariant


class Card(BaseModel):
    lab: int
    vid: str
    group: str
    n: int
    student: str = ""


def file(r: ForwardHead, due) -> dict | None:
    """FILE; `due` — the deadline it is held to (None — the lab has none, or the lab is not known)."""
    if not r.file:
        return None
    f = r.file
    return {"name": f.get("name", ""), "size": f.get("size"), "link": f.get("link", ""), "kind": r.kind, "lab": r.lab, "vid": r.vid,
            "line": bool(r.line), "ok": r.ok, "total": r.total, "why": r.why, "version": r.version, "trouble": r.trouble,
            "due": when(due), "late": utc(r.sent_at) > due if due else None}


def strips(rows: list[ForwardHead], cards: dict, files: dict, names: dict, dues: dict) -> list[dict]:
    """Per lab with a notebook from a real stream (not the demo): the newest file of each card number; `top` — the stream's last."""
    newest: dict[int, dict[int, ForwardHead]] = {}
    for r in rows:
        c = cards.get((r.lab, r.vid)) if r.kind and not r.mine and not r.skip else None
        if c and c.group != DEMO:
            got = newest.setdefault(r.lab, {})
            got[c.n] = r if c.n not in got or utc(got[c.n].sent_at) <= utc(r.sent_at) else got[c.n]
    out = []
    for lab, got in sorted(newest.items()):
        groups = {cards[(lab, r.vid)].group for r in got.values()}
        top = max(c.n for c in cards.values() if c.lab == lab and c.group in groups)
        out.append({"lab": lab, "due": when(dues.get(lab)), "top": top, "cells": [
            {"n": n, "vid": r.vid, "who": names.get(r.student) or r.name, "sent_at": when(r.sent_at), "ok": r.ok, "total": r.total,
             "late": files[r.id]["late"], "version": bool(r.version), "id": str(r.id)} for n, r in sorted(got.items())]})
    return out


async def intake() -> dict:
    """INTAKE = {people, strips}: talks the newest first, rows within a talk the oldest first."""
    rows = await Forward.find_all().sort("sent_at", "msg").project(ForwardHead).to_list()
    users = {u.email: u for u in await User.find_all().to_list()}
    people, held = await clues()
    cards = {(c.lab, c.vid): c for c in await LabVariant.find_all().project(Card).to_list()}
    deadlines = await Deadline.find_all().sort("created_at").to_list()
    marks = {(m.user, m.lab): m for m in await LabMark.find(In(LabMark.user, list({r.student for r in rows if r.student}))).to_list()}
    common = {lab: due_at(None, due_for(deadlines, lab, "")) for lab in {r.lab for r in rows if r.lab}}

    def due(r: ForwardHead):
        u = users.get(r.student)
        return due_at(marks.get((u.email, r.lab)), due_for(deadlines, r.lab, u.group)) if u and r.lab else common.get(r.lab)

    files = {r.id: file(r, due(r)) for r in rows}
    talks: dict[str, list[ForwardHead]] = {}
    for r in rows:
        if r.key:  # "" — the teacher's lines that joined nobody's talk
            talks.setdefault(r.key, []).append(r)
    out = []
    for key, rs in sorted(talks.items(), key=lambda t: t[1][-1].sent_at, reverse=True):
        last, u = ([r for r in rs if not r.mine] or rs)[-1], users.get(next((r.student for r in rs if r.student), ""))
        out.append({"key": key, "name": last.name, "username": last.username, "tg_id": last.tg_id, "student": who(u) if u else None,
                    "how": next((r.how for r in rs if r.how), ""), "guess": None if u else guess(rs, people, held),
                    "last": when(rs[-1].sent_at), "rows": [{"id": str(r.id), "mine": r.mine, "sent_at": when(r.sent_at), "text": r.text,
                                                            "asks": r.asks, "skip": r.skip, "file": files[r.id]} for r in rs]})
    names = {e: who(u)["name"] for e, u in users.items()}
    return {"people": out, "strips": strips(rows, cards, files, names, common)}
