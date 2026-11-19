"""Smoke: a notebook read without running it (T354 §3–4) — roles, alignment with the template, facts, outputs for showing,
the grade hint, the card pasted into a template, a Colab / Drive link. Pure: no DB, invented notebooks (tests/nb_fixture.py).
Run from sites/ods/api: ~/.venvs/python-labs/bin/python tests/smoke_nb.py"""
import asyncio
import json
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.getcwd())
sys.path.insert(0, str(Path(__file__).parent))
import labs_facts  # noqa: E402
import labs_marimo  # noqa: E402
import labs_nb  # noqa: E402
import labs_out  # noqa: E402
import labs_pull  # noqa: E402
import labs_shape  # noqa: E402
import labs_show  # noqa: E402
import labs_start  # noqa: E402
import nb_fixture as fx  # noqa: E402
from labs_grade import grade  # noqa: E402

results = []


def check(name, cond, extra=""):
    results.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def raises(f, *args) -> str:
    try:
        f(*args)
    except ValueError as e:
        return str(e)
    return ""


data = Path(tempfile.mkdtemp())
lab = data / "labs/new/lab9"
(lab / "solved").mkdir(parents=True)
(lab / "lab9-jupyter.ipynb").write_bytes(fx.notebook(fx.TEMPLATE))
(lab / "solved/lab9-jupyter.hid.ipynb").write_bytes(fx.notebook(fx.solved()))
(lab / "lab9-marimo.py").write_text(fx.marimo(fx.TEMPLATE))
shape = labs_shape.build(9, labs_shape.folder(data, 9))
tasks = {t["key"]: t for t in shape["tasks"]}
check("shape: the steps, the conclusion by its prompt's number, the star with its conclusion, report, ai",
      list(tasks) == ["1.1", "1.2", "1.3", "★1", "report", "ai"] and tasks["1.3"]["role"] == "conclusion" and tasks["★1"]["role"] == "star", list(tasks))
check("shape: titles off the prompts, answer names off check()", (tasks["1.1"]["title"], tasks["1.2"]["title"], tasks["★1"]["title"]) == ("Порахуй", "Графік", "зірочка 1")
      and tasks["1.1"]["names"] == ["x"] and tasks["★1"]["names"] == ["y"], tasks)
check("shape: a plot where the solved step draws; the star's picture does not count", shape["plots"] == 1 and tasks["1.2"]["plot"] and not tasks["★1"]["plot"])
check("shape: marimo cells keyed the same way, not live", len(shape["mcells"]) == len(shape["cells"]) + 1 and not shape["live"]
      and [c["key"] for c in shape["mcells"] if c["key"]] == [c["key"] for c in shape["cells"] if c["key"]])
site = data / "labs/site/lab9"
site.mkdir(parents=True)
check("folder: a site folder without a template is passed over", labs_shape.folder(data, 9) == lab)
(site / "lab9-jupyter.ipynb").write_bytes(fx.notebook(fx.TEMPLATE))
check("folder: the site's version wins once it has the template", labs_shape.folder(data, 9) == site)

f = labs_facts.facts(labs_nb.read(fx.notebook(fx.student(), colab=True)), shape)
t = {x["key"]: x for x in f["tasks"]}
check("facts: Colab, the card, the line", (f["kind"], f["tool"], f["vid"], f["card"], f["line"]) == ("ipynb", "colab", "КН-1-01", True, "LAB9 КН-1-01 x=2 y=3"), f)
check("facts: a split solution and a removed mark still count", t["1.1"]["done"] and t["1.2"]["done"] and t["1.2"]["image"] and t["1.1"]["checks"] == {"x": True}, t)
check("facts: counts", f["count"] == {"tasks": [2, 2], "plots": [1, 1], "conclusions": [1, 1], "stars": [1, 1], "report": True, "ai": False}, f["count"])
check("facts: run top to bottom, fresh, no errors", f["ran"] == {"count": 7, "of": 7, "ordered": True, "fresh": True, "errors": 0}, f["ran"])
check("facts: Colab's first and last moment, no names", f["times"]["first"] < f["times"]["last"] and "x" not in json.dumps(f["times"]), f["times"])

bad = labs_facts.facts(labs_nb.read(fx.notebook(fx.student(star_out=[fx.ERROR]))), shape)
check("facts: an error is named on its task and counted", {x["key"]: x for x in bad["tasks"]}["★1"]["error"] == "ZeroDivisionError"
      and bad["ran"]["errors"] == 1 and bad["tool"] == "jupyter" and bad["times"] is None)
empty = labs_facts.facts(labs_nb.read(fx.notebook(fx.TEMPLATE)), shape)
check("facts: the template itself — nothing done, never run", empty["count"]["tasks"] == [0, 2] and empty["count"]["conclusions"] == [0, 1]
      and empty["count"]["stars"] == [0, 1] and not empty["count"]["report"] and empty["ran"]["count"] == 0 and empty["vid"] == "")
cells = fx.student()
merged = cells[:5] + [("code", "# ✍ 1.1 порахуй x\nx = 2\n# ✍ 1.2 намалюй графік\nplt.plot([x])", [], 3)] + cells[9:]
m = labs_facts.facts(labs_nb.read(fx.notebook(merged)), shape)
check("facts: two steps merged into one cell are both done", m["count"]["tasks"] == [2, 2], m["tasks"])
mo = labs_facts.facts(labs_nb.read(fx.marimo(fx.student()).encode()), shape)
check("facts: marimo — steps read off the code, no outputs to tell", (mo["kind"], mo["ran"], mo["line"], mo["vid"]) == ("marimo", None, "", "КН-1-01")
      and mo["count"]["tasks"] == [2, 2] and mo["count"]["plots"] == [None, 1] and mo["tasks"][0]["checks"] is None, mo["count"])
own = labs_facts.facts(labs_nb.read(fx.notebook(fx.student())), None)
check("facts without a template: words counted, code unknown, a removed mark unseen", own["count"]["conclusions"] == [1, 1] and own["count"]["tasks"] == [None, 1]
      and own["count"]["plots"] == [None, None] and own["line"], own["count"])

shown = labs_show.cells(labs_nb.read(fx.notebook(fx.student())), shape)
outs = [o for c in shown for o in c["out"]]
check("show: roles and tasks of the cells", (shown[6]["role"], shown[6]["task"], shown[8]["role"], shown[8]["key"], shown[0]["given"], shown[5]["given"])
      == ("extra", "1.1", "task", "1.2", True, False), [(c["role"], c["key"], c["task"]) for c in shown[5:9]])
check("show: html is skipped, the picture inline, ANSI gone", {"type": "skipped", "mimes": ["text/html"]} in outs
      and any(o["type"] == "image" and o["mime"] == "image/png" for o in outs) and shown[5]["out"][0]["text"] == "проміжне\n" and "<script" not in json.dumps(shown))
check("show: a cell's fingerprint follows its text", shown[0]["h"] == labs_nb.h({"kind": "markdown", "source": fx.HEAD[1]}) and shown[0]["h"] != shown[3]["h"])
err = labs_out.show(fx.ERROR)
check("show: an error with its name, value and the tail of the trace", err == {"type": "error", "name": "ZeroDivisionError", "value": "division by zero",
                                                                               "trace": "Traceback\n1/0"}, err)
check("outputs: a picture that is not a PNG, or not base64, is no picture", not labs_out.image({"data": {"image/png": "aGVsbG8="}})
      and not labs_out.image({"data": {"image/png": "%%%"}}) and labs_out.image({"data": {"image/png": fx.png()[:20] + "\n" + fx.png()[20:]}}))
check("not a notebook", all(labs_nb.NOT_NB == raises(labs_nb.read, b) for b in (b"hello", b"{}", b'{"cells": 1}', b"print(1)\n")))
check("marimo that is not Python names the line", "рядок" in raises(labs_nb.read, b"import marimo\napp = marimo.App(\n"))

ok = grade(2, 2, True, f, None, "record")
check("grade: everything done, one star — the work reaches 16, a recording lets in 16", (ok["work"], ok["cap"], ok["hint"]) == (16, 16, 16)
      and [s["level"] for s in ok["steps"]] == [12, 13, 14, 16, 18, 19, 20], ok)
check("grade: needs in words", [n["text"] for n in ok["steps"][0]["needs"]] == ["2 із 2 ✅", "виконано згори донизу без помилок"]
      and [n["text"] for n in ok["steps"][2]["needs"]] == ["кроки 2 із 2", "графіки 1 із 1", "висновки 1 із 1", "рапорт"])
check("grade: no defence named — no cap; none — 12; the teacher's stars over the file", grade(2, 2, True, f, None, "")["hint"] == 16
      and grade(2, 2, True, f, None, "none")["hint"] == 12 and grade(2, 2, True, f, 1, "live")["work"] == 16 and grade(2, 2, True, f, 0, "live")["work"] == 14)
check("grade: a wrong answer or an error — not even 12", grade(1, 2, True, f, None, "live")["work"] is None and grade(2, 2, True, bad, None, "live")["work"] is None)
half = json.loads(json.dumps(f))
half["count"] |= {"plots": [0, 1], "report": False}  # 3 of 5 items
check("grade: level 13 — half of level 14's items", grade(2, 2, True, half, None, "record")["work"] == 13
      and grade(2, 2, True, empty | {"ran": f["ran"]}, None, "record")["work"] == 12)
g = grade(2, 2, True, mo, None, "live")
check("grade: marimo cannot tell how it ran — 12 is unknown, no work", g["work"] is None and g["steps"][0]["needs"][1]["ok"] is None)
check("grade: no file at all — needs are unknown", grade(0, 2, False, None, None, "")["steps"][2]["needs"][0]["ok"] is None)

card = fx.CARD.format(vid="КН-1-01").split("\n") + ['TOKEN = "t"']
made = json.loads(labs_start.made("jupyter", fx.notebook(fx.TEMPLATE), card))
check("start: Jupyter — the card in place of `# ✂`", "".join(made["cells"][1]["source"]) == "\n".join(card) and len(made["cells"]) == len(fx.TEMPLATE))
mtext = labs_start.made("marimo", fx.marimo(fx.TEMPLATE), card).decode()
mcells = labs_marimo.cells(mtext)
check("start: marimo — the card at the cell's indentation, still Python", '    X = [1, 2,\n         3]' in mtext and mcells[2]["source"] == "\n".join(card), mcells[2])
check("start: a template without `# ✂` → ValueError", raises(labs_start.made, "jupyter", fx.notebook(fx.TEMPLATE[2:]), card)
      and raises(labs_start.made, "marimo", "import marimo\napp = marimo.App()\n", card))

ids = [labs_pull.drive_id(x) for x in ("https://colab.research.google.com/drive/1AbC-dEf_ghIJkl?usp=sharing",
                                       "https://drive.google.com/file/d/1AbC-dEf_ghIJkl/view", "https://drive.google.com/open?id=1AbC-dEf_ghIJkl",
                                       "https://github.com/x/y/blob/main/a.ipynb", "")]
check("pull: the file id of the three Google links, none of others", ids == ["1AbC-dEf_ghIJkl"] * 3 + [None, None], ids)


async def pulled(link: str, body: bytes) -> str:
    async def fake(url):
        return body
    labs_pull.get = fake
    try:
        return "ok" if await labs_pull.pull(link) == body else "?"
    except ValueError as e:
        return str(e)


link = "https://colab.research.google.com/drive/1AbC-dEf_ghIJkl"
check("pull: Google's sign-in page is no notebook → words", asyncio.run(pulled(link, b"<!doctype html><title>Sign in</title>")) == labs_pull.FAIL)
check("pull: a notebook comes through", asyncio.run(pulled(link, fx.notebook(fx.student()))) == "ok")
check("pull: not a Google link → words", asyncio.run(pulled("https://example.com/a.ipynb", b"{}")) == labs_pull.NOT_GOOGLE)
check("pull: only Google's hosts, https", labs_pull.google(labs_pull.httpx.URL("https://drive.usercontent.google.com/x"))
      and not labs_pull.google(labs_pull.httpx.URL("https://google.com.evil.io/x")) and not labs_pull.google(labs_pull.httpx.URL("http://drive.google.com/x")))

print(f"\n{sum(ok for _, ok in results)}/{len(results)} PASS")
sys.exit(not all(ok for _, ok in results))
