"""The lectures' folder (sites/ods/data/lectures, its own git): the text then (tag `orig`) and now, the journal, the notes,
the catalogue's files. A file is written only when more than its `built` changed — the same input, the same bytes."""
import json
import os
import subprocess
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LECT = Path(os.environ.get("ODS_DATA") or ROOT / "sites/ods/data") / "lectures"
OUT, NOTES = LECT / "changes", LECT / "changes/notes"


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(LECT), *args], capture_output=True, text=True, check=True).stdout


def numbers() -> list[int]:
    return sorted(int(p.name[3:]) for p in LECT.glob("lec[0-9][0-9]") if (p / f"{p.name}.md").exists())


def text(n: int) -> tuple[str, str]:
    """(the text as converted from pptx, the text on disk)."""
    name = f"lec{n:02}/lec{n:02}.md"
    return git("show", f"orig:{name}"), (LECT / name).read_text()


def head(n: int) -> str:
    """The last commit of the lecture's text; «+» — the file on disk has more than it."""
    name = f"lec{n:02}/lec{n:02}.md"
    return git("log", "-1", "--format=%H", "--", name).strip() + ("+" if git("status", "--porcelain", "--", name).strip() else "")


def journal(n: int) -> str:
    path = LECT / f"fixes/lec{n:02}.md"
    return path.read_text() if path.exists() else ""


def load(path: Path, empty: dict) -> dict:
    return json.loads(path.read_text()) if path.exists() else empty


def notes(n: int) -> dict:
    return load(NOTES / f"lec{n:02}.json", {})


def rules() -> list[dict]:
    return load(NOTES / "rules.json", {"rules": []})["rules"]


def dump(data) -> str:
    return json.dumps(data, ensure_ascii=False, indent=1) + "\n"


def save(n: int, data: dict) -> bool:
    """Writes changes/lecNN.json unless only the time would change; True — written."""
    path = OUT / f"lec{n:02}.json"
    old = load(path, {})
    if old and {**old, "built": ""} == {**data, "built": ""}:
        return False
    OUT.mkdir(exist_ok=True)
    path.write_text(dump({**data, "built": datetime.now(UTC).isoformat(timespec="seconds")}))
    return True


def built(n: int) -> dict | None:
    path = OUT / f"lec{n:02}.json"
    return json.loads(path.read_text()) if path.exists() else None
