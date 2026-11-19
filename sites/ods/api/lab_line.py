"""An answer line checked as an attempt (T200): pasted on «Моя лаба» or found in a handed-in notebook — the same rule."""
from datetime import datetime, timezone

from fastapi import HTTPException

from labs_check import parse_line, verdict
from models.lab import LabVariant


def judge(v: LabVariant, line: str) -> tuple[dict, dict]:
    """({name: {ok, why}}, values) of a line of this very variant; anything else — 422 in the student's words."""
    try:
        n, vid, values = parse_line(line)
    except ValueError as e:
        raise HTTPException(422, str(e)) from None
    if (n, vid) != (v.lab, v.vid):
        raise HTTPException(422, f"Це рядок варіанта {vid} лаби {n}, а твій — {v.vid} лаби {v.lab}")
    return verdict(values, v.answers), values


def attempt(v: LabVariant, line: str, at: datetime | None = None) -> tuple[dict, str]:
    """The fields of one more attempt and the note for history: «9/13»; `at` — when the line was handed in, if not now."""
    got, values = judge(v, line)
    fields = {"line": line, "values": values, "verdict": got, "attempts": v.attempts + 1, "checked_at": at or datetime.now(timezone.utc)}
    return fields, f"{sum(x['ok'] for x in got.values())}/{len(v.answers)}"
