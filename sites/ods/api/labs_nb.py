"""Reading a handed-in notebook without running it (T354 §3): .ipynb is JSON, marimo .py — labs_marimo.py.
A cell is {kind, source, outputs, count, meta}; its role comes from the lab's marks: # ✂, # ✍ 1.3, # ✍ ★ 2, ✍ *Мітка:*."""
import hashlib
import json
import re

import labs_marimo

NOT_NB = "Це не ноутбук: потрібен файл .ipynb (Jupyter, Colab) або .py із marimo"
MARK = re.compile(r"^\s*#\s*✍\s*(★)?\D*?(\d+(?:\.\d+)?)", re.M)  # the first prompt of a code cell: a task or a star
LABEL = re.compile(r"\s*✍\s*\*([^*\n]+?):\*")  # ✍ *Висновок:* — where the student's words go
VARIANT = re.compile(r"^\s*VARIANT\s*=\s*[\"']([^\"'\n]+)[\"']", re.M)
LINE_CALL = re.compile(r"print\(\s*[\"']LAB\d")
NAMES = re.compile(r"check\(\s*[\"']([^\"']+)[\"']")
WORDS = {"Висновок": "conclusion", "Рапорт": "report", "Про ШІ": "ai"}  # any other label is a note


def text(src) -> str:
    return "".join(x for x in src if isinstance(x, str)) if isinstance(src, list) else src if isinstance(src, str) else ""


def ipynb(data: bytes) -> dict:
    try:
        nb = json.loads(data)
    except (ValueError, RecursionError):
        nb = None
    raw = nb.get("cells") if isinstance(nb, dict) else None
    if not isinstance(raw, list) or not all(isinstance(c, dict) for c in raw):
        raise ValueError(NOT_NB)
    cells = [{"kind": "code" if c.get("cell_type") == "code" else "markdown", "source": text(c.get("source")),
              "outputs": c["outputs"] if isinstance(c.get("outputs"), list) else [],
              "count": c.get("execution_count") if isinstance(c.get("execution_count"), int) else None,
              "meta": c.get("metadata") if isinstance(c.get("metadata"), dict) else {}} for c in raw]
    meta = nb.get("metadata") if isinstance(nb.get("metadata"), dict) else {}
    colab = "colab" in meta or any("executionInfo" in c["meta"] for c in cells)
    return {"kind": "ipynb", "tool": "colab" if colab else "jupyter", "cells": cells}


def read(data: bytes) -> dict:
    """{kind, tool, cells}; a ValueError speaks to the student."""
    if data.lstrip(b"\xef\xbb\xbf \t\r\n")[:1] == b"{":
        return ipynb(data)
    try:
        src = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise ValueError(NOT_NB) from None
    if not labs_marimo.is_marimo(src):
        raise ValueError(NOT_NB)
    return {"kind": "marimo", "tool": "marimo", "cells": labs_marimo.cells(src)}


def role(cell: dict) -> tuple[str, str]:
    """(role, mark): mark — a task's «1.3», a star's «2», the label of the student's words."""
    src = cell["source"]
    if cell["kind"] != "code":
        if not (m := LABEL.match(src)):
            return "given", ""
        label = m[1].strip()
        return next((r for w, r in WORDS.items() if label.startswith(w)), "note"), label
    first = next((line for line in src.split("\n") if line.strip()), "")
    if first.startswith("# ✂") or VARIANT.search(src):
        return "card", ""
    if "def check(" in src:
        return "service", ""
    if m := MARK.search(src):
        return ("star", m[2]) if m[1] else ("task", m[2])
    return ("line", "") if LINE_CALL.search(src) else ("given", "")


def norm(src: str) -> str:
    return " ".join(src.split())


def sig(cell: dict) -> str:
    """What alignment compares: a marked cell by its mark, any other by its text."""
    r, mark = role(cell)
    if r in ("card", "service", "line"):
        return r
    if r != "given":
        return f"{r}:{mark}"
    return cell["kind"][0] + ":" + hashlib.sha1(norm(cell["source"]).encode()).hexdigest()[:10]


def h(cell: dict) -> str:
    """A cell's fingerprint: two versions of a notebook show which cells changed."""
    return hashlib.sha1((cell["kind"] + "\n" + norm(cell["source"])).encode()).hexdigest()[:12]
