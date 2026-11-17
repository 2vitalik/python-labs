#!/usr/bin/env python3
"""prep.py <raw dir> [--offset HH:MM:SS] — every raw source with time as «one fragment = one line» with clock time, into
<raw dir>/../prep/: zoom*.txt and wispr*.txt («[Who] HH:MM:SS» and the text under it), zoom-cc*.txt (captions, a line
each, no names), plaud.txt (counts from the start of its own recording).

Plaud's clock time of 00:00:00 is found by matching early fragments against Zoom unless given with --offset. Prints what
each source covers — its span and the gaps — so the merge starts from facts, not from reading."""
import re
import sys
from pathlib import Path

ZOOM = re.compile(r"^\[(?P<who>[^\]]+)\] (?P<t>\d\d:\d\d:\d\d)$")
PLAUD = re.compile(r"^(?P<t>\d\d:\d\d:\d\d) (?P<who>Speaker \d+)$")
CAPTION = re.compile(r"^(?P<t>\d\d:\d\d:\d\d) (?P<text>.+)$")
WORD = re.compile(r"\w+")
GAP = 300  # a silence longer than this is worth a line: a break, a source switched off


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


def captions(path: Path) -> list[tuple[int, str, str]]:
    return [(secs(m["t"]), "", m["text"]) for m in map(CAPTION.match, path.read_text().splitlines()) if m]


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


def write(out: Path, name: str, rows: list, shift: int = 0, note: str = ""):
    (out / name).write_text("\n".join(f"{clock(t + shift)} {w}: {x}" if w else f"{clock(t + shift)} {x}" for t, w, x in rows) + "\n")
    who = sorted({w for _, w, _ in rows if w})
    gaps = [f"{clock(a + shift)[:5]}–{clock(b + shift)[:5]}" for (a, _, _), (b, _, _) in zip(rows, rows[1:]) if b - a > GAP]
    print(f"{name}: {len(rows)} фрагментів · {clock(rows[0][0] + shift)}–{clock(rows[-1][0] + shift)}"
          + (f" · {len(who)} мовців: {', '.join(who)}" if who else " · без імен") + (f" · прогалини: {', '.join(gaps)}" if gaps else "") + (f" · {note}" if note else ""))


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
    zoom = []
    for p in sorted(raw.glob("*.txt")):
        if p.name.startswith(("plaud", "chat")):
            continue
        rows = captions(p) if p.name.startswith("zoom-cc") else fragments(p, ZOOM)
        if rows:
            write(out, p.name, rows)
            zoom = zoom or rows  # the first clocked source in name order: what Plaud is matched against
    plaud = fragments(raw / "plaud.txt", PLAUD) if (raw / "plaud.txt").exists() else []
    if plaud:
        note = "час відносний, зсув невідомий"
        if offset is None and zoom:
            offset, spread = offset_by_text(zoom, plaud)
            note = f"Plaud 00:00:00 = {clock(offset)} (за текстом; розкид оцінок {spread} с — перевір на двох фразах)"
        elif offset is not None:
            note = f"Plaud 00:00:00 = {clock(offset)} (задано)"
        write(out, "plaud.txt", plaud, offset or 0, note)
    print(f"→ {out}")


if __name__ == "__main__":
    main()
