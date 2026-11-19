"""A cell's outputs as the site reads them (T354 §3): text for the answer line and the marks of check(), pictures, errors;
for showing — text, image, latex, error or skipped. HTML and scripts never pass: the site shows what a student sent."""
import base64
import binascii
import re

from labs_nb import text

ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")
TEXT_MAX, IMAGE_MAX, TRACE = 20_000, 3 * 2**20, 8
MAGIC = {"image/png": b"\x89PNG", "image/jpeg": b"\xff\xd8"}


def plain(o: dict) -> str:
    """What the student saw as text: a stream or the plain form of a result."""
    if o.get("output_type") == "stream":
        return ANSI.sub("", text(o.get("text")))
    return ANSI.sub("", text((o.get("data") or {}).get("text/plain"))) if isinstance(o.get("data"), dict) else ""


def lines(outputs: list) -> list[str]:
    return [line for o in outputs if isinstance(o, dict) for line in plain(o).split("\n")]


def image(o: dict) -> dict | None:
    """{mime, data} of a real png / jpeg within the limit; data is base64 without line breaks."""
    data = o.get("data") if isinstance(o.get("data"), dict) else {}
    for mime, magic in MAGIC.items():
        if isinstance(b64 := text(data.get(mime)), str) and b64:
            b64 = "".join(b64.split())
            try:
                raw = base64.b64decode(b64, validate=True)
            except (binascii.Error, ValueError):
                continue
            if raw.startswith(magic) and len(raw) <= IMAGE_MAX:
                return {"mime": mime, "data": b64}
    return None


def has_image(outputs: list) -> bool:
    return any(isinstance(o, dict) and image(o) for o in outputs)


def error(outputs: list) -> str:
    """The name of the first error a cell raised; "" — none."""
    return next((str(o.get("ename") or "Error") for o in outputs if isinstance(o, dict) and o.get("output_type") == "error"), "")


def show(o: dict) -> dict:
    kind = o.get("output_type")
    if kind == "stream":
        return {"type": "text", "text": plain(o)[:TEXT_MAX], "stream": o.get("name", "stdout")}
    if kind == "error":
        trace = [ANSI.sub("", str(t)) for t in o.get("traceback") or []][-TRACE:]
        return {"type": "error", "name": str(o.get("ename", "")), "value": ANSI.sub("", str(o.get("evalue", "")))[:TEXT_MAX],
                "trace": "\n".join(trace)[-TEXT_MAX:]}
    if img := image(o):
        return {"type": "image"} | img
    data = o.get("data") if isinstance(o.get("data"), dict) else {}
    if latex := text(data.get("text/latex")):
        return {"type": "latex", "text": latex[:TEXT_MAX]}
    if "text/plain" in data:
        return {"type": "text", "text": plain(o)[:TEXT_MAX], "stream": "result"}
    return {"type": "skipped", "mimes": sorted(str(k) for k in data)[:5]}
