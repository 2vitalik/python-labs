"""The stream at a glance (T354 §5): where students go wrong, answer by answer; the latest notebooks for bin/nbrun."""
from fastapi import APIRouter, Depends

from core.deps import admin_user, editor_user
from core.models.history import when
from core.models.user import User
from lab_claim import DEMO
from models.lab import LabVariant
from models.lab_file import FileHead, LabFile

router = APIRouter(prefix="/api/variants")


@router.get("/{lab}/stats")
async def stats(lab: int, user: User = Depends(admin_user)):
    """[{name, ok, bad, why: [{text, n, who: [{vid, nick, name}]}]}] over the lines handed in; the demo and test students left out.
    `why` "" — a wrong number of no known cause; «нема в рядку» — the answer missing from the line."""
    rows = await LabVariant.find(LabVariant.lab == lab, LabVariant.attempts > 0, LabVariant.group != DEMO).sort("group", "n").to_list()
    users = {u.email: u for u in await User.find({"email": {"$in": [v.student for v in rows]}}).to_list()}
    names: dict[str, dict] = {}
    for v in rows:
        u = users.get(v.student)
        if not u or u.test:
            continue
        who = {"vid": v.vid, "nick": u.nick, "name": u.person()["name"]}
        for name in v.answers:
            got = v.verdict.get(name) or {"ok": False, "why": ""}
            s = names.setdefault(name, {"name": name, "ok": 0, "bad": 0, "why": {}})
            s["ok" if got["ok"] else "bad"] += 1
            if not got["ok"]:
                s["why"].setdefault(got["why"], []).append(who)
    return [s | {"why": sorted(({"text": k, "n": len(w), "who": w} for k, w in s["why"].items()), key=lambda x: -x["n"])}
            for s in names.values()]


@router.get("/{lab}/files")
async def files(lab: int, todo: bool = False, user: User = Depends(editor_user)):
    """The latest version of every card somebody holds; todo — those not run yet."""
    holders = {(v.vid, v.student) for v in await LabVariant.find(LabVariant.lab == lab, LabVariant.student != "").to_list()}
    latest: dict[tuple, FileHead] = {}
    for f in await LabFile.find(LabFile.lab == lab, LabFile.origin == "student").sort("-at").project(FileHead).to_list():
        latest.setdefault((f.vid, f.student), f)
    return [{"id": str(f.id), "vid": f.vid, "student": f.student, "kind": f.kind, "name": f.name, "size": f.size, "at": when(f.at),
             "sha": f.sha, "run": bool(f.run)} for key, f in latest.items() if key in holders and not (todo and f.run)]
