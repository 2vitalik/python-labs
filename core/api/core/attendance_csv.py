"""Zoom's participants report as a CSV (T336): attendance that needs no admin — the host exports it himself from
Reports → Meeting and webinar history → the number of participants → Export. A row per join; the times are local ones,
of whoever exported. Zoom publishes no spec of the file, so the header row is found by its first column, not by position."""
import csv
import io
import re
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

FORMATS = ("%m/%d/%Y %I:%M:%S %p", "%m/%d/%Y %H:%M:%S", "%Y-%m-%d %H:%M:%S", "%d.%m.%Y %H:%M:%S", "%d/%m/%Y %H:%M:%S")


def when(text: str, tz: str) -> str:
    """A local time of the report → ISO UTC, "" when it is not a time."""
    for f in FORMATS:
        try:
            return datetime.strptime(text.strip(), f).replace(tzinfo=ZoneInfo(tz)).astimezone(timezone.utc).isoformat()
        except ValueError:
            pass
    return ""


def column(cols: list[str], *starts: str) -> int | None:
    return next((i for i, c in enumerate(cols) if c.startswith(starts)), None)


def participants(data: bytes, tz: str) -> tuple[list[dict], dict]:
    """→ rows as Zoom's API gives them (name, user_email, join_time, leave_time) and the meeting's own line
    (topic, start, end) when the export was made «with meeting data». Raises ValueError with what is wrong in the file."""
    rows = [[c.strip() for c in r] for r in csv.reader(io.StringIO(data.decode("utf-8-sig", "replace"))) if any(c.strip() for c in r)]
    head = next((i for i, r in enumerate(rows) if r[0].lower().startswith("name")), None)
    if head is None:
        raise ValueError("Не схоже на звіт учасників Zoom: нема рядка заголовків «Name (original name)…»")
    cols = [c.lower() for c in rows[head]]
    name, email, join, leave, waiting = 0, column(cols, "email", "user email"), column(cols, "join"), column(cols, "leave"), column(cols, "in waiting")
    if join is None or leave is None:
        raise ValueError("У звіті нема часу входу й виходу — експортуй без галочки «Show unique users»")
    out = []
    for r in rows[head + 1:]:
        r += [""] * (len(cols) - len(r))
        a, b = when(r[join], tz), when(r[leave], tz)
        if a and b and not (waiting is not None and r[waiting].lower() == "yes"):  # the waiting room is not the class
            out.append({"name": re.sub(r"\s*\([^()]*\)$", "", r[name]), "user_email": r[email] if email is not None else "", "join_time": a, "leave_time": b})
    meeting = {}
    if head >= 2 and (top := [c.lower() for c in rows[head - 2]]) and column(top, "topic") is not None:
        line = rows[head - 1] + [""] * len(top)
        pick = lambda *starts: line[i] if (i := column(top, *starts)) is not None else ""  # noqa: E731
        meeting = {"topic": pick("topic"), "start": when(pick("start time"), tz), "end": when(pick("end time"), tz)}
    return out, meeting
