"""The site's part of a student's row in /students and /table (T352, T354): the card of each lab, the answers, the notebook,
the defence, the grade hint and the teacher's points."""
from core.models.user import User
from core.routes import students
from models.lab import LabVariant

KEYS = ("vid", "ok", "total", "attempts", "checked_at", "notebook", "points", "note", "assigned_at", "way", "defended", "stars", "files")


async def variants(users: list[User]) -> dict:
    """Lab n → the student's card as the teacher's table reads it (LabVariant.row); {} — no card taken yet."""
    out = {u.email: {"variants": {}} for u in users}
    for v in await LabVariant.find({"student": {"$in": list(out)}}).to_list():
        row = v.row()
        own = ((row["count"] or {}).get("stars") or [None])[0]  # the stars that count: the teacher's word, else the file's
        out[v.student]["variants"][str(v.lab)] = {k: row[k] for k in KEYS} | {
            "file_at": (row["file"] or {}).get("at"), "work": row["grade"]["work"], "hint": row["grade"]["hint"],
            "stars": own if v.stars is None else v.stars, "stars_file": v.stars is None and own is not None}
    return out


students.TEACHER.append(variants)  # points, the teacher's note, the notebook and the hint are not for fellow students
