"""bin/lesson scan / collect (T334): after a class everything a lesson needs is already on this Mac — Zoom's recording
folder and Wispr Flow's meeting. `scan` lists the folders against the site; `collect` makes the day's draft from them:
the parts by the recording pieces, the raw sources, pieces.yml for `bin/lesson video`."""
import shutil
import sys
from datetime import timedelta
from pathlib import Path

import yaml

import lessonwispr
import lessonzoom
from siteapi import call

SHORT = 60  # a piece shorter than this is a slip of the record button, not a part


def wispr(start, end) -> list[dict]:
    try:
        return lessonwispr.meetings(start - timedelta(minutes=10), end + timedelta(minutes=10))
    except Exception as e:  # the app's own files, not ours: the collect goes on without them
        print(f"Wispr Flow не прочитано · {e}")
        return []


def span(seconds: float) -> str:
    m = round(seconds / 60)
    return f"{m // 60} год {m % 60:02d} хв" if m >= 60 else f"{m} хв"


def scan(to: str, topic: str):
    have = {l["slug"]: l for l in call(to, "GET", "/lessons")}
    for f in lessonzoom.folders(topic=topic):
        ps = [] if f["raw"] else lessonzoom.pieces(f)
        has = [name if name != "zoom.txt" else f"zoom.txt до {p.stem[-8:-3].replace('.', ':')}" for name, p in lessonzoom.sources(f).items()]
        if ps:
            has += [f"Wispr {span((m['end'] - m['start']).total_seconds())}" for m in wispr(ps[0]["start"], ps[-1]["end"])]
        l = have.get(f["date"])
        site = "нема" if not l else ("показано" if l["published"] else "чернетка") + (" 🗣" if l["has"]["transcript"] else "") + (" 🎬" if l["has"]["video"] else "")
        what = "не сконвертовано — відкрий запис у Zoom" if f["raw"] else f"{len(ps)} шматків · {span(sum(p['seconds'] for p in ps))} · {' · '.join(has) or 'без джерел'}"
        print(f"{f['date']} {f['start']:%H:%M}  {f['topic']:<16} {what} · сайт: {site}")


def overlap(p: dict, part: dict, date: str) -> float:
    a, b = (lessonzoom.datetime.fromisoformat(f"{date}T{t if len(t) > 5 else t + ':00'}") for t in (part["start"], part["end"]))
    return (min(p["end"], b) - max(p["start"], a)).total_seconds()


def collect(to: str, date: str, tag: str, topic: str, dry: bool, folder: Path, pull, push):
    found = lessonzoom.folders(date, topic)
    for f in found:
        if f["raw"]:
            print(f"⚠️ {f['path'].name}: запис не сконвертовано — відкрий його в Zoom (Recordings → Convert), потім collect ще раз")
    pieces = sorted((p for f in found if not f["raw"] for p in lessonzoom.pieces(f)), key=lambda p: p["start"])
    if not pieces:
        sys.exit(f"у {lessonzoom.ZOOM} нема запису за {date}" + (f" з темою «{topic}»" if topic else "") + " — bin/lesson scan покаже, що є")
    slug, start, end = "-".join(x for x in (date, tag) if x), pieces[0]["start"], pieces[-1]["end"]
    parts = [{"kind": "break" if p["quiet"] else "pz", "start": f"{p['start']:%H:%M:%S}", "end": f"{p['end']:%H:%M:%S}"} for p in pieces if p["seconds"] >= SHORT]
    notes = wispr(start, end)
    print(f"{slug}: {start:%H:%M}–{end:%H:%M} · {len(pieces)} шматків запису → {len(parts)} частин · Wispr Flow: {len(notes)} зустрічей")
    if dry:
        return
    if slug not in {l["slug"] for l in call(to, "GET", "/lessons")}:
        call(to, "POST", "/lessons", {"date": date, "tag": tag, "time": f"{start:%H:%M}–{end:%H:%M}", "parts": parts})
    cur = call(to, "GET", f"/lessons/{slug}")
    if not [p for p in cur["parts"] if not p.get("site")]:  # parts somebody has set by hand are theirs
        cur = call(to, "PUT", f"/lessons/{slug}", {"rev": cur["rev"], "parts": parts, "time": cur["time"] or f"{start:%H:%M}–{end:%H:%M}", "note": "частини за шматками запису"})
    pull(to, slug)
    raw = folder / slug / "raw"
    for i, f in enumerate(f for f in found if not f["raw"]):
        for name, path in lessonzoom.sources(f).items():
            shutil.copyfile(path, raw / (name if not i else name.replace(".", f"-{i + 1}.")))
    for i, m in enumerate(notes):
        text = lessonwispr.text(m)
        if text:
            (raw / ("wispr.txt" if not i else f"wispr-{i + 1}.txt")).write_text(text)
    own = [p for p in cur["parts"] if not p.get("site") and p["start"] and p["end"]]
    best = lambda p: max(own, key=lambda part: overlap(p, part, date), default=None)  # noqa: E731
    (folder / slug / "pieces.yml").write_text(yaml.safe_dump(
        [{"part": (best(p) or {}).get("key", "") if p["seconds"] >= SHORT else "", "file": str(p["file"]), "start": f"{p['start']:%H:%M:%S}",
          "end": f"{p['end']:%H:%M:%S}", "seconds": p["seconds"]} for p in pieces], allow_unicode=True, sort_keys=False))
    push(to, slug, "зібрано з теки Zoom", False)
    print(f"далі: /lesson merge {folder / slug} → /lesson summary → bin/lesson push {slug} · відео: bin/lesson video {slug}")
