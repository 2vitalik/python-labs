"""The docker side of bin/nbrun (T354): one notebook → one locked container → the body of PUT /variants/file/{id}/run."""
import base64
import json
import secrets
import subprocess
import threading
import time
from functools import cache
from pathlib import Path

IMAGE = "ods-nbrun"
LIMIT, CAP = 300, 60 * 2**20  # seconds per notebook, bytes of stdout read
BOX = ["--network", "none", "--read-only", "--tmpfs", "/tmp:rw,exec,size=512m", "--memory", "1g", "--memory-swap", "1g",
       "--cpus", "1", "--pids-limit", "256", "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
       "--user", "1000:1000", "--log-driver", "none", "--pull", "never", "-e", "HOME=/tmp", "-e", "MPLBACKEND=Agg",
       "-e", "MPLCONFIGDIR=/tmp/mpl", "-e", "JUPYTER_RUNTIME_DIR=/tmp/jrt"]


def build() -> None:
    subprocess.run(["docker", "build", "-t", IMAGE, str(Path(__file__).resolve().parent)], check=True)


def ready() -> None:
    r = subprocess.run(["docker", "image", "inspect", IMAGE], capture_output=True, text=True, check=False)
    if r.returncode:
        raise SystemExit(f"образу {IMAGE} нема або Docker не запущено — спершу bin/nbrun build · {r.stderr.strip()[:200]}")


@cache
def engine() -> str:
    r = subprocess.run(["docker", "run", "--rm", *BOX, IMAGE, "engine"], capture_output=True, text=True, check=False)
    return r.stdout.strip()


def feed(pipe, data: bytes) -> None:
    try:
        pipe.write(data)
        pipe.close()
    except (BrokenPipeError, OSError):  # the box died before taking it all: the exit code tells why
        pass


def read(pipe, buf: bytearray, cap: int, over=None) -> None:
    while chunk := pipe.read1(1 << 16):
        buf += chunk[:max(0, cap + 1 - len(buf))]
        if len(buf) > cap and over:
            return over()  # stdout past the cap: stop reading, kill the box


def run(data: bytes, kind: str, files: dict[str, bytes] | None = None, limit: int = LIMIT) -> dict:
    name, marker = f"nbrun-{secrets.token_hex(4)}", secrets.token_hex(16)
    head = {"marker": marker, "limit": limit - 30, "files": {k: base64.b64encode(v).decode() for k, v in (files or {}).items()}}
    out, err, why = bytearray(), bytearray(), []

    def kill(reason: str) -> None:  # the container by its name: killing the docker client alone would leave it running
        why.append(reason)
        subprocess.run(["docker", "kill", name], capture_output=True, check=False)
        p.kill()

    start = time.monotonic()
    p = subprocess.Popen(["docker", "run", "-i", "--rm", "--name", name, *BOX, IMAGE, kind],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    jobs = [threading.Thread(target=feed, args=(p.stdin, json.dumps(head).encode() + b"\n" + data)),
            threading.Thread(target=read, args=(p.stdout, out, CAP, lambda: kill("cap"))),
            threading.Thread(target=read, args=(p.stderr, err, 1 << 16))]
    for j in jobs:
        j.start()
    try:
        p.wait(limit)
    except subprocess.TimeoutExpired:
        kill("time")
        p.wait()
    finally:
        for j in jobs:
            j.join(10)
        subprocess.run(["docker", "rm", "-f", name], capture_output=True, check=False)
    if p.returncode == 125 and not why:  # docker itself failed, the notebook never ran: nothing to tell the site
        raise SystemExit(f"docker не запустив контейнер: {err.decode(errors='replace').strip()[-300:]}")
    body = {"ok": False, "line": "", "seconds": round(time.monotonic() - start, 1), "errors": [], "engine": "", "log": ""}
    m, text = marker.encode(), bytes(out).strip()
    if not why and text.count(m) == 2 and text.startswith(m) and text.endswith(m):
        try:
            return body | clean(json.loads(text[len(m):-len(m)]))
        except ValueError:
            why.append("json")
    body["engine"] = engine()
    body["log"] = (cause(why, p.returncode, limit) + "\n" + err.decode(errors="replace"))[-4096:]
    return body


def cause(why: list, code: int, limit: int) -> str:
    if "cap" in why:
        return f"вивід понад {CAP >> 20} МБ — читання зупинено, контейнер зупинено"
    if "time" in why:
        return f"час вичерпано: {limit} с — контейнер зупинено (docker kill)"
    if code == 137:
        return "контейнер убито (код 137): найпевніше, забракло памʼяті (1 ГБ)"
    return f"пісочниця не віддала результату (код {code}{', вивід зіпсовано' if 'json' in why else ''})"


def clean(r: dict) -> dict:
    """The frame is ours, but its word is still checked for shape before it goes to the site."""
    errors = [e for e in r.get("errors", []) if isinstance(e, dict)][:500]
    return {"ok": r.get("ok") is True, "line": str(r.get("line", ""))[:1000], "engine": str(r.get("engine", ""))[:300],
            "errors": [{k: str(e.get(k, ""))[:300] for k in ("key", "name", "text")} for e in errors],
            "log": str(r.get("log", ""))[-4096:], **({"executed": r["executed"]} if isinstance(r.get("executed"), str) else {})}
