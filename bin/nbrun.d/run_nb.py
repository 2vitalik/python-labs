"""The frame inside the ods-nbrun box (T354, started by bin/nbrun): a notebook on stdin → one JSON on stdout.

  python run_nb.py ipynb|marimo   stdin: a JSON header line {marker, limit, files}, then the notebook's bytes
  python run_nb.py engine         the versions, one line

The notebook runs in child processes (a Jupyter kernel, marimo) whose stdout and stderr are /tmp/log. This process is
PID 1 and not dumpable: the children can neither reach its stdout or memory through /proc nor kill it, so what stands
between the two markers is the frame's own word."""
import base64
import ctypes
import json
import os
import re
import shutil
import signal
import sys
import threading
import time
import warnings
import zlib

from engines import ipynb, marimo, swarm

LOG = "/tmp/log"
LINE = re.compile(r"^LAB\d+ \S+ .*=")
EXECUTED = 12 * 2**20
PACKAGES = ("numpy", "scipy", "sympy", "matplotlib", "pandas", "scikit-learn", "marimo", "nbclient")


def engine() -> str:
    from importlib.metadata import version
    return " · ".join([f"python {sys.version.split()[0]}"] + [f"{p} {version(p)}" for p in PACKAGES])


def report(nb: dict | None, note: str) -> dict:
    cells = (nb or {}).get("cells", [])
    outs = [(i, o) for i, c in enumerate(cells) for o in c.get("outputs", [])]
    errors = {str(i): {"key": str(i), "name": str(o.get("ename", "")), "text": str(o.get("evalue", ""))[:300]}
              for i, o in reversed(outs) if o.get("output_type") == "error"}  # reversed: the first error of a cell wins
    text = "".join("".join(o.get("text", "")) for _, o in outs if o.get("output_type") == "stream")
    lines = [l for l in text.splitlines() if LINE.match(l)]
    raw = json.dumps(nb, ensure_ascii=False).encode() if nb else b""
    log = ""
    if note:  # cell errors speak for themselves; the box's log only when the run itself broke
        with open(LOG, "rb") as f:  # only the tail: the notebook may have flooded it
            f.seek(max(0, os.path.getsize(LOG) - 3072))
            log = note + "\n" + f.read().decode(errors="replace")
    return {"ok": bool(nb) and not note and not errors, "line": lines[-1] if lines else "",
            "errors": sorted(errors.values(), key=lambda e: int(e["key"])), "engine": engine(), "log": log[-4096:],
            **({"executed": base64.b64encode(zlib.compress(raw, 9)).decode()} if 0 < len(raw) <= EXECUTED else {})}


def main():
    if sys.argv[1] == "engine":
        return print(engine())
    ctypes.CDLL(None).prctl(4, 0, 0, 0, 0)  # PR_SET_DUMPABLE = 0: /proc/1/{fd,mem,environ} close to the children
    out = os.dup(1)  # not inheritable: the notebook's processes never get it
    log = os.open(LOG, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    os.dup2(log, 1), os.dup2(log, 2)
    warnings.simplefilter("ignore")  # nbformat's own nagging would crowd the log's tail
    for s in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP, signal.SIGUSR1, signal.SIGUSR2):
        signal.signal(s, lambda *_: None)  # a handler, not SIG_IGN: children get the default back on exec
    head = json.loads(sys.stdin.buffer.readline())
    src = sys.stdin.buffer.read()
    os.makedirs("/tmp/work")
    for name, data in head.get("files", {}).items():
        path = os.path.normpath(os.path.join("/tmp/work", name))
        if path.startswith("/tmp/work/"):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "wb") as f:
                f.write(base64.b64decode(data))
    shutil.copytree("/opt/mpl", "/tmp/mpl")  # the font cache from the build: no seconds lost on it every run
    state = {"nb": None, "note": ""}

    def work():
        try:
            state["note"] = (ipynb if sys.argv[1] == "ipynb" else marimo)(src, state)
        except Exception as e:  # noqa: BLE001 — whatever broke, the host gets a JSON saying so
            state["note"] = f"{type(e).__name__}: {e}"[:1000]

    # In a thread, so nbclient installs no SIGINT/SIGTERM handlers here: a signal from the notebook changes nothing.
    worker = threading.Thread(target=work, daemon=True)
    worker.start()
    end, crowded = time.monotonic() + head["limit"], False
    while worker.is_alive() and time.monotonic() < end and not crowded:  # a fork bomb is stopped before it eats memory
        worker.join(0.25)
        crowded = swarm()
    if worker.is_alive():
        os.kill(-1, signal.SIGKILL)  # every process in the box but this one
        worker.join(5)
        why = "ноутбук наплодив процесів понад пів ліміту (256)" if crowded else f"загальний ліміт {head['limit']} с вичерпано"
        state["note"] = f"{why} — процеси ноутбука зупинено" + (f" · {state['note']}" if state["note"] else "")
    try:
        result = report(state["nb"], state["note"])
    except Exception as e:  # noqa: BLE001 — a half-written notebook must not cost the whole answer
        result = report(None, f"{state['note']} · виконаний ноутбук не зібрався: {e}"[:1000])
    marker = head["marker"].encode()
    with os.fdopen(out, "wb") as f:
        f.write(marker + json.dumps(result, ensure_ascii=False).encode() + marker + b"\n")


if __name__ == "__main__":
    main()
