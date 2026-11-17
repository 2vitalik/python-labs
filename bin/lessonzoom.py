"""Zoom's local recordings as lessons (T334): a folder «2026-11-10 15.31.42 Topic» in ~/Documents/Zoom is one meeting — its
recording pieces with their clock spans, the captions, the transcript saved in the meeting, the chat. Read only; nothing
here talks to Zoom. ZOOM_DIR names another folder."""
import json
import os
import re
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from statistics import median

ZOOM = Path(os.environ.get("ZOOM_DIR", Path.home() / "Documents" / "Zoom"))
FOLDER = re.compile(r"(\d{4}-\d{2}-\d{2}) (\d\d)\.(\d\d)\.(\d\d) (.+)")
CUE = re.compile(r"(\d\d):(\d\d):(\d\d)[.,]\d+ --> .*\n(.+)")
CAPTION = re.compile(r"^(\d\d):(\d\d):(\d\d) (.+)$", re.M)


def folders(date: str = "", topic: str = "") -> list[dict]:
    out = []
    for d in sorted(ZOOM.iterdir()) if ZOOM.is_dir() else []:
        m = FOLDER.fullmatch(d.name)
        if m and d.is_dir() and (not date or m[1] == date) and re.search(topic, m[5], re.I):
            out.append({"path": d, "date": m[1], "start": datetime.fromisoformat(f"{m[1]}T{m[2]}:{m[3]}:{m[4]}"), "topic": m[5],
                        "raw": bool(list(d.glob("double_click_to_convert_*.zoom")))})  # never converted: no pieces yet
    return out


def seconds(path: Path) -> float:
    got = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    return float(got.stdout.strip() or 0)


def order(d: Path) -> list[Path]:
    """video<N><magic>.mp4 by N; the magic number is the recording's own (recording.conf)."""
    conf = d / "recording.conf"
    magic = json.loads(conf.read_text()).get("magic_number", "") if conf.exists() else ""
    n = lambda p: int(p.stem[5:len(p.stem) - len(magic)] or 0) if magic and p.stem.endswith(magic) else 0  # noqa: E731
    return sorted(d.glob("video*.mp4"), key=lambda p: (n(p), p.stat().st_mtime))


def started(vtt: Path, clocks: dict[str, int]) -> int | None:
    """The second of the day a piece starts at: a cue of its .vtt (time from the piece's start) found once among the
    captions (the wall clock) gives the difference; the median of such — the answer."""
    if not vtt.exists():
        return None
    found = [clocks[text.strip()] - (int(h) * 3600 + int(m) * 60 + int(s)) for h, m, s, text in CUE.findall(vtt.read_text(errors="replace"))
             if text.strip() in clocks]
    return round(median(found)) if found else None


def pieces(folder: dict) -> list[dict]:
    """The recording pieces in order with clock times. Without captions to align by, a piece starts where the one
    before ended (the first — when the meeting did): right while the recording was never stopped for long."""
    d = folder["path"]
    cc = (d / "closed_caption.txt").read_text(errors="replace") if (d / "closed_caption.txt").exists() else ""
    seen: dict[str, list[int]] = {}
    for h, m, s, text in CAPTION.findall(cc):
        seen.setdefault(text.strip(), []).append(int(h) * 3600 + int(m) * 60 + int(s))
    clocks = {text: at[0] for text, at in seen.items() if len(at) == 1 and len(text) > 12}  # said once, long enough to be itself
    day = folder["start"].replace(hour=0, minute=0, second=0)
    cursor, out = folder["start"], []
    for v in order(d):
        length = seconds(v)
        at = started(v.with_suffix(".vtt"), clocks)
        start = day + timedelta(seconds=at) if at is not None else cursor
        cursor = start + timedelta(seconds=length)
        # captions were on, and this piece has none: nobody spoke in it — a break left recording
        out.append({"file": v, "seconds": round(length), "start": start, "end": cursor, "quiet": bool(clocks) and not v.with_suffix(".vtt").exists()})
    return out


def sources(folder: dict) -> dict[str, Path]:
    """What the folder gives the merge: zoom.txt — the transcript saved in the meeting (names and clock, up to the moment
    it was saved), zoom-cc.txt — the captions (the whole recording, no names), chat.txt."""
    d = folder["path"]
    saved = sorted(d.glob("* transcript_*.txt"))
    found = {"zoom.txt": saved[-1] if saved else None, "zoom-cc.txt": d / "closed_caption.txt", "chat.txt": d / "chat.txt"}
    return {name: p for name, p in found.items() if p and p.exists() and p.stat().st_size}
