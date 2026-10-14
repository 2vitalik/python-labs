"""Attendance (T222): Zoom's joined-left segments → rows of `attendance`, the meeting's span, the threshold of «був».
How the pages read the rows — attendance_read.py."""
from datetime import datetime

from core.models.attendance import Attendance, Segment
from core.models.history import stamp
from core.models.lesson import Lesson
from core.models.user import User

PRESENT = 0.25  # «був» = in the room for at least this share of the meeting; less — a pale avatar (T223 Q1)


def parse(iso: str) -> datetime:
    return datetime.fromisoformat(iso.replace("Z", "+00:00"))


def merged(spans: list[tuple[datetime, datetime]]) -> list[Segment]:
    """Sorted, overlaps joined: two devices, or a re-join before the leave registered, count once."""
    out: list[Segment] = []
    for a, b in sorted(spans):
        if out and a <= out[-1].leave:
            out[-1].leave = max(out[-1].leave, b)
        else:
            out.append(Segment(join=a, leave=b))
    return out


def rows(slug: str, uuid: str, start: datetime, participants: list[dict]) -> list[Attendance]:
    """Zoom gives a row per segment; the same name as shown (case aside) is one person."""
    by: dict[str, dict] = {}
    for p in participants:
        if not p.get("join_time") or not p.get("leave_time"):
            continue
        name = (p.get("name") or "").strip() or "(без імені)"
        d = by.setdefault(name.lower(), {"name": name, "email": "", "spans": []})
        d["email"] = d["email"] or p.get("user_email") or ""
        d["spans"].append((parse(p["join_time"]), parse(p["leave_time"])))
    out = []
    for d in by.values():
        segs = merged(d["spans"])
        out.append(Attendance(lesson=slug, name=d["name"], email=d["email"], segments=segs, meeting_uuid=uuid,
                              seconds=sum(int((s.leave - s.join).total_seconds()) for s in segs),
                              late=max(0, int((segs[0].join - start).total_seconds()))))
    return sorted(out, key=lambda a: -a.seconds)


def span(l: Lesson) -> int:
    """The meeting's length in seconds; 0 until something was pulled."""
    return int((parse(l.zoom.end) - parse(l.zoom.start)).total_seconds()) if l.zoom.start and l.zoom.end else 0


def cell(seconds: int, total: int) -> dict:
    return {"seconds": seconds, "present": seconds >= PRESENT * total}


def view(a: Attendance, u: User | None, total: int, admin: bool) -> dict:
    row = {"name": a.name, "person": u.person() if u else None} | cell(a.seconds, total)
    if admin:
        row |= {"late": a.late, "email": a.email, "segments": [{"join": stamp(s.join), "leave": stamp(s.leave)} for s in a.segments]}
    return row
