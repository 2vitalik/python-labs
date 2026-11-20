"""A forwarded file read without running anything (T368 §2.3): whether it is a notebook, whose card it carries, which lab
it is — by its answer line, else by the lab its own last cell names, else by the lab template it is closest to, else by
its name — and how its line fares against the card's key. No student is needed for any of it."""
import hashlib
import re
import zlib

from pydantic import BaseModel

import labs_align
import labs_facts
import labs_nb
from core.config import settings
from lab_store import TOO_BIG
from labs_check import LINE, parse_line, verdict
from models.lab import LabVariant
from models.lab_file import MAX_BYTES
from models.lab_shape import LabShape

NOT_NB = "Не ноутбук"
LIKE, AHEAD = 0.5, 0.15  # a lab's template: this share of its cells found in the file, and this far ahead of the next lab's
NAMED = re.compile(r"(?:lab|лаб|лр)[^\W\d_]*[\s_.№#-]*0?(\d)(?!\d)", re.I)  # lab2 · Lab_02 · лаб 2 · лабораторна-2 · ЛР2


class Templates(BaseModel):
    lab: int
    cells: list[dict] = []
    mcells: list[dict] = []


def wanted(name: str) -> bool:
    """What is worth fetching: Jupyter or marimo."""
    return name.lower().endswith((".ipynb", ".py"))


def found(cells: list[dict], tmpl: list[dict]) -> float:
    """The share of the template's cells the file has as they are; a pairing by kind alone does not count."""
    at = labs_align.match(cells, tmpl)
    return len({t for c, t in zip(cells, at, strict=True) if t is not None and tmpl[t]["sig"] == labs_nb.sig(c)}) / len(tmpl)


async def by_template(nb: dict) -> int | None:
    side = "mcells" if nb["kind"] == "marimo" else "cells"
    shares = sorted(((found(nb["cells"], getattr(s, side)), s.lab) for s in await LabShape.find_all().project(Templates).to_list()
                     if getattr(s, side)), reverse=True) + [(0, None), (0, None)]
    (best, lab), (second, _) = shares[:2]
    return lab if best >= LIKE and best - second >= AHEAD else None


def by_name(name: str) -> int | None:
    m = NAMED.search(name)
    return int(m[1]) if m and 1 <= int(m[1]) <= settings.labs else None


async def score(lab: int | None, line: str) -> tuple[int | None, int | None]:
    """(ok, total) of the line against the key of the card it names; None — no line, or it is not of this lab."""
    if not (lab and line):
        return None, None
    try:
        n, vid, values = parse_line(line)
    except ValueError:
        return None, None
    v = await LabVariant.find_one(LabVariant.lab == lab, LabVariant.vid == vid) if n == lab else None
    if not v:
        return None, None
    return sum(x["ok"] for x in verdict(values, v.answers).values()), len(v.answers)


async def read(name: str, data: bytes) -> dict:
    """{kind, sha, raw, lab, vid, line, ok, total, why}: kind "" — not a notebook, `why` says so."""
    out = {"kind": "", "sha": hashlib.sha256(data).hexdigest(), "raw": b"", "lab": None, "vid": "", "line": "", "ok": None, "total": None,
           "why": ""}
    if len(data) > MAX_BYTES:
        return out | {"why": TOO_BIG}
    out["raw"] = zlib.compress(data)
    try:
        nb = labs_nb.read(data)
    except ValueError:
        return out | {"why": NOT_NB}
    facts = labs_facts.facts(nb, None)
    line = LINE.match(facts["line"])
    said = facts["lab"] if facts["lab"] and 1 <= facts["lab"] <= settings.labs else None  # its own last cell prints "LABn"
    lab = int(line[1]) if line else said or await by_template(nb) or by_name(name)
    ok, total = await score(lab, facts["line"])
    return out | {"kind": nb["kind"], "lab": lab, "vid": facts["vid"], "line": facts["line"], "ok": ok, "total": total}
