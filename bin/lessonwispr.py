"""Wispr Flow's meeting notes as a source of a lesson (T337): the app keeps every meeting it listened to on this Mac — a
row in flow.sqlite and a folder with the transcript. Read only. The layout is the app's own, undocumented, and may change
with it: a failure here must never stop a collect."""
import json
import sqlite3
from bisect import bisect_right
from datetime import datetime
from pathlib import Path

HOME = Path.home() / "Library" / "Application Support" / "Wispr Flow"


def local(utc: datetime) -> datetime:
    return utc.astimezone().replace(tzinfo=None)


def meetings(start: datetime, end: datetime) -> list[dict]:
    """The meetings that overlap the span (local clock), the earliest first."""
    db = sqlite3.connect(f"file:{HOME / 'flow.sqlite'}?mode=ro", uri=True)
    found = db.execute("select id, title, createdAt, endedAt, speakerMap from Meetings where isDeleted = 0 and endedAt is not null").fetchall()
    db.close()
    out = []
    for id, title, created, ended, speakers in found:
        a = local(datetime.fromisoformat(created.replace(" +", "+")))
        b = local(datetime.fromtimestamp(ended / 1000).astimezone())
        if a < end and b > start:
            out.append({"id": id, "title": title, "start": a, "end": b, "speakers": json.loads(speakers or "{}").get("people", {})})
    return sorted(out, key=lambda m: m["start"])


def rows(path: Path) -> list[dict]:
    return [x for x in map(json.loads, path.read_text().splitlines()) if "text" in x] if path.exists() else []


def since(x: dict) -> int:
    """A row's «MM:SS» or «H:MM:SS» from the start of the recording, in ms."""
    return sum(int(n) * 60 ** i for i, n in enumerate(reversed(x["timestamp"].split(":")))) * 1000


def text(m: dict) -> str:
    """«[Speaker] HH:MM:SS» and the words under it, by the wall clock — the shape of Zoom's saved transcript. The refined
    text is the cleaner one but may stop early: the live one is taken when it goes further. Refined rows count time from
    the start of the recording with the pauses cut out — the live rows know the clock of each moment. «Мікрофон» is
    whoever sat at this Mac (the teacher); a name is there only when the app has matched the voice to a contact."""
    d = HOME / "meetings" / m["id"]
    live, fine = rows(d / "live.ndjson"), rows(d / "refined.ndjson")
    marks = sorted((x["startRecordingMs"], x["startEpochMs"] - x["startRecordingMs"]) for x in live if "startEpochMs" in x)
    names = {key.split("-")[1]: who["name"] for key, who in m["speakers"].items() if key.startswith("voice-") and who.get("name")}
    out = []
    for x in fine if fine and (not live or since(fine[-1]) >= since(live[-1]) - 120_000) else live:
        shift = marks[max(bisect_right(marks, (since(x), float("inf"))) - 1, 0)][1] if marks else m["start"].timestamp() * 1000
        clock = datetime.fromtimestamp(x.get("startEpochMs", since(x) + shift) / 1000)
        speaker = x.get("speaker", {})
        who = names.get(str(speaker.get("id"))) or speaker.get("name") or ("Мікрофон" if speaker.get("source") == "mic" else f"Speaker {speaker.get('id')}")
        out.append(f"[{who}] {clock:%H:%M:%S}\n{x['text'].strip()}\n")
    return "\n".join(out)
