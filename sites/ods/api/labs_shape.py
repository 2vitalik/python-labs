"""A lab's notebook shape from its files on disk (T354 §2): the Jupyter and marimo templates keyed cell by cell, the tasks,
which of them the solved notebook draws a plot in, whether the service cell reports to the site. lab_io.py stores it."""
from pathlib import Path

import labs_align
import labs_keys
import labs_marimo
import labs_nb
import labs_out

LIVE = "/api/variants/"  # the service cell of a lab whose check() reports to the site (T354 §9)
SHOW = "plt.show("


def folder(data: Path, n: int) -> Path:
    """The site's version of a lab (labs/site/labN) when it has a template, else the lab as written (labs/new/labN)."""
    site = data / f"labs/site/lab{n}"
    return site if (site / f"lab{n}-jupyter.ipynb").exists() else data / f"labs/new/lab{n}"


def plotted(tmpl: list[dict], solved: list[dict]) -> set[str]:
    """Steps (not stars) whose cells in the solved notebook draw: a picture in the outputs, or `plt.show(` in the code —
    a solved notebook executed without inline pictures (MPLBACKEND=Agg) still asks for its plots."""
    marks = labs_align.assign(solved, tmpl)
    return {m["task"] for c, m in zip(solved, marks) if m["task"] and not m["task"].startswith("★")
            and (labs_out.has_image(c["outputs"]) or SHOW in c["source"])}


def build(n: int, d: Path) -> dict | None:
    """LabShape's fields; None — the folder has no Jupyter template."""
    tpl, solved, mo = d / f"lab{n}-jupyter.ipynb", d / f"solved/lab{n}-jupyter.hid.ipynb", d / f"lab{n}-marimo.py"
    if not tpl.exists():
        return None
    jupyter = tpl.read_bytes()
    cells = labs_keys.keyed(labs_nb.read(jupyter)["cells"])
    tasks = labs_keys.tasks(cells)
    drawn = plotted(cells, labs_nb.read(solved.read_bytes())["cells"]) if solved.exists() else set()
    for t in tasks:
        t["plot"] = t["key"] in drawn and t["role"] in ("task", "note")
    marimo = mo.read_text() if mo.exists() else ""
    service = next((c["source"] for c in cells if c["role"] == "service"), "")
    return {"lab": n, "cells": cells, "mcells": labs_keys.keyed(labs_marimo.cells(marimo)) if marimo else [], "tasks": tasks,
            "plots": sum(t["plot"] for t in tasks), "jupyter": jupyter, "marimo": marimo, "live": LIVE in service}
