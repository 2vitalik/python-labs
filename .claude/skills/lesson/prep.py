#!/usr/bin/env python3
"""prep.py <raw dir> [--offset HH:MM:SS] — zoom.txt and plaud.txt as «one fragment = one line» with clock time, into <raw dir>/../prep/.

Plaud counts from the start of its own recording; the clock time of its 00:00:00 is found by matching early fragments
against Zoom unless given with --offset. Prints what it found so the merge can start from facts, not from reading."""
import re
import sys
from pathlib import Path

ZOOM = re.compile(r"^\[(?P<who>[^\]]+)\] (?P<t>\d\d:\d\d:\d\d)$")
PLAUD = re.compile(r"^(?P<t>\d\d:\d\d:\d\d) (?P<who>Speaker \d+)$")
WORD = re.compile(r"\w+")


def secs(t: str) -> int:
    h, m, s = map(int, t.split(":"))
    return h * 3600 + m * 60 + s


def clock(s: int) -> str:
    return f"{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}"


def fragments(path: Path, head: re.Pattern) -> list[tuple[int, str, str]]:
    """(seconds, who, text) per label line; the text is every non-blank line until the next label."""
    out = []
    for line in path.read_text().splitlines():
        if m := head.match(line.strip()):
            out.append([secs(m["t"]), m["who"], []])
        elif out and line.strip():
            out[-1][2].append(line.strip())
    return [(t, w, " ".join(x)) for t, w, x in out]


def words(text: str) -> set[str]:
    return {w.lower() for w in WORD.findall(text) if len(w) > 3}


def offset_by_text(zoom, plaud) -> tuple[int, int]:
    """(offset, spread): clock time of Plaud 00:00:00 as the median over early Plaud fragments of «earliest Zoom fragment
    sharing ≥3 long words with the fragment's opening words». A Plaud fragment spans 30–60 s, so only its start is matched."""
    offsets = []
    for pt, _, ptext in [f for f in plaud[:40] if len(f[2].split()) >= 8][:12]:
        opening = words(" ".join(ptext.split()[:12]))
        hits = [zt for zt, _, ztext in zoom[:400] if len(opening & words(ztext)) >= 3]
        if hits:
            offsets.append(min(hits) - pt)
    if not offsets:
        return 0, 0
    offsets.sort()
    return offsets[len(offsets) // 2], offsets[-1] - offsets[0]


def main():
    args = sys.argv[1:]
    offset = None
    if "--offset" in args:
        i = args.index("--offset")
        offset = secs(args[i + 1])
        del args[i:i + 2]
    raw = Path(args[0])
    out = raw.parent / "prep"
    out.mkdir(exist_ok=True)
    zoom = fragments(raw / "zoom.txt", ZOOM) if (raw / "zoom.txt").exists() else []
    plaud = fragments(raw / "plaud.txt", PLAUD) if (raw / "plaud.txt").exists() else []
    if zoom:
        (out / "zoom.txt").write_text("\n".join(f"{clock(t)} {w}: {x}" for t, w, x in zoom) + "\n")
        who = sorted({w for _, w, _ in zoom})
        print(f"zoom: {len(zoom)} фрагментів · {clock(zoom[0][0])}–{clock(zoom[-1][0])} · {len(who)} мовців: {', '.join(who)}")
    if plaud:
        note = "час відносний, зсув невідомий"
        if offset is None and zoom:
            offset, spread = offset_by_text(zoom, plaud)
            note = f"Plaud 00:00:00 = {clock(offset)} (за текстом; розкид оцінок {spread} с — перевір на двох фразах)"
        elif offset is not None:
            note = f"Plaud 00:00:00 = {clock(offset)} (задано)"
        shift = offset or 0
        (out / "plaud.txt").write_text("\n".join(f"{clock(t + shift)} {w}: {x}" for t, w, x in plaud) + "\n")
        print(f"plaud: {len(plaud)} фрагментів · {clock(plaud[0][0] + shift)}–{clock(plaud[-1][0] + shift)} · {note}")
    print(f"→ {out}")


if __name__ == "__main__":
    main()
