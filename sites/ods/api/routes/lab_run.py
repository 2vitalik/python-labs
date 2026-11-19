"""A notebook re-run on the teacher's machine (T354 §7, bin/nbrun): the report lands on the student's version as RUN;
the executed copy is kept as a version of its own, and a file without outputs (marimo .py) gets its facts from it."""
import base64
import binascii
import zlib
from datetime import datetime, timezone

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

import labs_align
import labs_facts
from core.deps import editor_user
from core.models.history import record, when
from core.models.user import User
from lab_line import judge
from lab_store import TOO_BIG, parse, shape_of, version
from models.lab import LabVariant
from models.lab_file import MAX_BYTES, LabFile, file_api

router = APIRouter(prefix="/api/variants")
TEXT = 500


class RunIn(BaseModel):
    ok: bool = False
    line: str = ""
    seconds: float = 0
    errors: list[dict] = []  # [{key?, cell?, name, text}] — when no executed copy comes to read them from
    engine: str = ""
    log: str = ""
    executed: str = ""  # base64 of zlib of the executed .ipynb


def unpack(b64: str) -> bytes:
    try:
        z = zlib.decompressobj()
        data = z.decompress(base64.b64decode(b64, validate=True), MAX_BYTES + 1)
    except (binascii.Error, ValueError, zlib.error):
        raise HTTPException(422, "executed — base64 від zlib виконаного .ipynb") from None
    if len(data) > MAX_BYTES or not z.eof:
        raise HTTPException(422, TOO_BIG)
    return data


def errors_of(nb: dict, shape: dict | None) -> list[dict]:
    """[{key, name, text}] of the executed copy: key — the task of the cell that raised."""
    marks = labs_align.assign(nb["cells"], labs_facts.template(shape, nb["kind"]))
    return [{"key": m["task"], "name": str(o.get("ename", "")), "text": str(o.get("evalue", ""))[:TEXT]}
            for c, m in zip(nb["cells"], marks) for o in c["outputs"] if isinstance(o, dict) and o.get("output_type") == "error"][:50]


def ran_of(facts: dict, ok: bool, errors: list) -> dict | None:
    """The executed copy of a marimo file has no counters (execution_count null): the box ran it top to bottom itself."""
    ran = facts.get("ran")
    if not ran or ran["count"]:
        return ran
    return {"count": ran["of"], "of": ran["of"], "ordered": True, "fresh": True, "errors": len(errors) or int(not ok)}


def verdict_of(v: LabVariant, line: str) -> dict | None:
    try:
        return {k: x["ok"] for k, x in judge(v, line)[0].items()} if line else None
    except HTTPException:
        return None


@router.put("/file/{id}/run")
async def run(id: PydanticObjectId, data: RunIn, user: User = Depends(editor_user)):
    f = await LabFile.get(id)
    if not f or f.origin != "student":
        raise HTTPException(404)
    if not (v := await LabVariant.find_one(LabVariant.lab == f.lab, LabVariant.vid == f.vid)):
        raise HTTPException(404)
    copy, errors = None, [{"key": str(e.get("key") or e.get("cell", "")), "name": str(e.get("name", ""))[:80],
                           "text": str(e.get("text", ""))[:TEXT]} for e in data.errors[:50]]
    if data.executed:
        raw = unpack(data.executed)
        nb, shape = parse(raw), await shape_of(f.lab)
        facts = labs_facts.facts(nb, shape)
        copy = version(nb, raw, lab=f.lab, vid=f.vid, student=f.student, name=f.name.rsplit(".", 1)[0] + ".run.ipynb", by=user.email,
                       origin="run", of=str(f.id), facts=facts, line=facts["line"])
        await copy.insert()
        errors = errors_of(nb, shape)
    line = " ".join(data.line.split()) or (copy.line if copy else "")
    got, theirs = verdict_of(v, line), verdict_of(v, f.line or v.line)
    report = {"at": when(datetime.now(timezone.utc)), "by": user.email.split("@")[0], "ok": data.ok,
              "same": got == theirs if got is not None and theirs is not None else None, "line": line,
              "right": sum(got.values()) if got is not None else None, "total": len(v.answers), "seconds": data.seconds,
              "errors": errors, "engine": data.engine[:300], "file": str(copy.id) if copy else None}
    await f.set({LabFile.run: report, LabFile.log: data.log[-20_000:]})
    if v.student == f.student and v.file.get("id") == str(f.id):
        own = f.facts.get("ran")
        if copy and (own is None or not own["count"]):
            v.facts = copy.facts | {"from": "run", "ran": ran_of(copy.facts, data.ok, errors)}
        await record(v, {"file": file_api(f)}, actor=user.email, note="перезапуск")
    return report
