"""What a notebook file says without running it (T354 §3): FACTS = {kind, tool, cells, vid, card, lab, line, ran, tasks, count, times}
(`lab` — the lab its own last cell names: every template prints "LABn" there; None — that cell is gone).
A step is done when its code has lines the template has not (comments aside) or its words run 20 characters past the label.
None — the file cannot tell: marimo's .py carries no outputs, a lab without a template cannot tell code of its own."""
import re

import labs_align
import labs_keys
import labs_nb
import labs_out
from labs_ran import ran, times

LINE = re.compile(r"^\s*(LAB\d+\s+\S+.*)$")
SAYS_LAB = re.compile(r"""print\(\s*["']LAB(\d+)["']""")
CHECK = re.compile(r"^\s*(✅|❌|⬜)\s+(\S+)")
MARKS = {"✅": True, "❌": False, "⬜": None}
COMMENT = re.compile(r"<!--.*?-->", re.S)
WORDS_MIN = 20


def code_done(c: dict, tc: dict | None) -> bool:
    had = {labs_nb.norm(x) for x in (tc["source"] if tc else "").split("\n")}
    return any(x.strip() and not x.strip().startswith("#") and labs_nb.norm(x) not in had for x in c["source"].split("\n"))


def words_done(c: dict) -> bool:
    body = COMMENT.sub("", labs_nb.LABEL.sub("", c["source"], count=1))
    return len(" ".join(body.split())) >= WORDS_MIN


def all3(oks) -> bool | None:
    oks = list(oks)
    return False if False in oks else None if None in oks else True


def task_facts(nb: dict, tmpl: list[dict] | None, tasks: list[dict]) -> list[dict]:
    cells, own, outs, out = nb["cells"], tmpl is None, nb["kind"] != "marimo", []
    ref, marks = tmpl or labs_keys.keyed(cells), labs_align.assign(cells, tmpl)
    for t in tasks:
        mine = [(c, None if own or m["t"] is None else ref[m["t"]]) for c, m in zip(cells, marks) if m["task"] == t["key"]]
        mine += [(c, None) for c, m in zip(cells, marks) if m["task"] != t["key"] and c["kind"] == "code"  # two steps in one cell
                 and t["key"] in [x[2] for x in labs_nb.MARK.finditer(c["source"]) if not x[1]]]
        code = [c for c, _ in mine if c["kind"] == "code"]
        ok = {"code": None if own else any(code_done(c, tc) for c, tc in mine if c["kind"] == "code"),
              "words": any(words_done(c) for c, _ in mine if c["kind"] != "code")}
        need = {"code" if c["kind"] == "code" else "words" for c in ref if c["key"] == t["key"]}
        lines = labs_out.lines([o for c in code for o in c["outputs"]])
        out.append({"key": t["key"], "role": t["role"], "case": t["case"], "title": t["title"], "done": all3(ok[p] for p in need) if need else None,
                    "plot": t["plot"], "image": any(labs_out.has_image(c["outputs"]) for c in code) if outs else None,
                    "error": next((e for c in code if (e := labs_out.error(c["outputs"]))), "") if outs else None,
                    "checks": {m[2]: MARKS[m[1]] for x in lines if (m := CHECK.match(x))} if outs else None})
    return out


def count(ts: list[dict], shaped: bool, outs: bool) -> dict:
    def pair(*roles):
        done = [t["done"] for t in ts if t["role"] in roles]
        return [None if None in done else sum(done), len(done)]

    plots = [t for t in ts if t["plot"]]
    one = {r: next((t["done"] for t in ts if t["role"] == r), None) for r in ("report", "ai")}
    return {"tasks": pair("task", "note"), "plots": [sum(bool(t["image"]) for t in plots) if outs else None, len(plots)] if shaped else [None, None],
            "conclusions": pair("conclusion"), "stars": pair("star")} | one


def template(shape: dict | None, kind: str) -> list[dict] | None:
    """The template cells a file of this kind is read against; None — the lab has none."""
    return (shape["mcells" if kind == "marimo" else "cells"] or None) if shape else None


def facts(nb: dict, shape: dict | None) -> dict:
    ts = task_facts(nb, template(shape, nb["kind"]), shape["tasks"] if shape else labs_keys.tasks(labs_keys.keyed(nb["cells"])))
    code = [c for c in nb["cells"] if c["kind"] == "code"]
    vid = next((m[1].strip() for c in code if (m := labs_nb.VARIANT.search(c["source"]))), "")
    found = [m[1] for c in code for x in labs_out.lines(c["outputs"]) if (m := LINE.match(x))]
    lab = next((int(m[1]) for c in code if (m := SAYS_LAB.search(c["source"]))), None)
    return {"kind": nb["kind"], "tool": nb["tool"], "cells": len(nb["cells"]), "vid": vid, "card": bool(vid), "lab": lab,
            "line": " ".join(found[-1].split()) if found else "", "ran": ran(nb), "tasks": ts,
            "count": count(ts, bool(shape), nb["kind"] != "marimo"), "times": times(nb["cells"])}
