#!/usr/bin/env python3
"""check.py <transcript.md> [--raw <dir>] — grammar check and stats of a merged lesson transcript (merge.md).

Exit code 1 when a line is outside the grammar, time runs backwards, or a section's time differs from its first line."""
import re
import sys
from collections import Counter
from pathlib import Path

LINE = re.compile(r"^\*\*(?P<who>[^*]+)\*\* · (?P<t>\d{1,2}:\d{2}) — (?P<text>.+)$")
LINE_NO_TIME = re.compile(r"^\*\*(?P<who>[^*]+)\*\* — (?P<text>.+)$")
HEAD = re.compile(r"^## (?P<title>.+) · (?P<t>\d{1,2}:\d{2})$")
NOTE = re.compile(r"^\*\[.+\]\*$")
UNSURE = ("[?]", "[нерозбірливо]")
STUDENT = re.compile(r"^Студент( \d+)?$")
# raw markup to drop before counting a source's words: label lines and speaker prefixes
MARKUP = re.compile(r"^\[[^\]]+\] \d\d:\d\d:\d\d$|^\d\d:\d\d:\d\d Speaker \d+$|^[^:\n]{1,40}:\s|^- |^Transcript$", re.M)
ZOOM_NAME = re.compile(r"^\[([^\]]+)\] \d\d:\d\d:\d\d$", re.M)


def minutes(t: str) -> int:
    h, m = t.split(":")
    return int(h) * 60 + int(m)


def content_words(path: Path) -> int:
    return len(MARKUP.sub("", path.read_text()).split())


def main():
    args = sys.argv[1:]
    raw = None
    if "--raw" in args:
        i = args.index("--raw")
        raw = Path(args[i + 1])
        del args[i:i + 2]
    path = Path(args[0])
    text = path.read_text()
    meta, body = {}, text
    if text.startswith("---\n"):
        _, front, body = text.split("---\n", 2)
        meta = {k.strip(): v.split("#")[0].strip() for k, v in (l.split(":", 1) for l in front.splitlines() if ":" in l)}

    words, lines, heads, bad, back, off = Counter(), Counter(), [], [], [], []
    unsure, last, pending = 0, -1, None  # pending — a section waiting for its first line
    for n, line in enumerate(body.splitlines(), 1):
        if not line.strip() or line.startswith("# ") or NOTE.match(line):
            continue
        if m := HEAD.match(line):
            heads.append((m["t"], m["title"]))
            pending = (n, m["t"])
            continue
        if m := LINE.match(line) or LINE_NO_TIME.match(line):
            words[m["who"]] += len(m["text"].split())
            lines[m["who"]] += 1
            unsure += sum(m["text"].count(u) for u in UNSURE)
            t = m.groupdict().get("t")
            if t:
                if minutes(t) < last:
                    back.append((n, t))
                last = minutes(t)
                if pending and pending[1] != t:
                    off.append((pending[0], pending[1], t))
            pending = None
            continue
        bad.append((n, line[:90]))

    total = sum(words.values())
    print(f"{path}: {len(heads)} розділів · {sum(lines.values())} реплік · {total} слів · [?]/[нерозбірливо]: {unsure}")
    if meta:
        print("  " + " · ".join(f"{k}: {v or '—'}" for k, v in meta.items()))
    for who, w in words.most_common():
        print(f"  {who:<28} {lines[who]:>4} реплік {w:>6} слів")
    if heads:
        print("Розділи:")
        for t, title in heads:
            print(f"  {t}  {title}")
    if raw and raw.is_dir():
        sizes = sorted(((content_words(p), p.name) for p in raw.glob("*.txt")), reverse=True)
        if sizes:
            print(f"Частка слів від найбільшого джерела без розмітки ({sizes[0][1]}, {sizes[0][0]} слів): {total / sizes[0][0]:.0%}")
        zoom = raw / "zoom.txt"
        if zoom.exists():
            names = set(ZOOM_NAME.findall(zoom.read_text()))
            known = lambda who: who in names or STUDENT.match(who) or any(who.split()[0] in n for n in names)
            if odd := [who for who in words if not known(who)]:
                print("Мовці, яких нема в Zoom (roster або помилка): " + ", ".join(odd))
    if back:
        print(f"Час іде назад — {len(back)} рядків: " + ", ".join(f"{n} ({t})" for n, t in back[:10]))
    if off:
        print(f"Час розділу ≠ час першої репліки — {len(off)}: " + ", ".join(f"{n} ({a}→{b})" for n, a, b in off[:10]))
    if bad:
        print(f"Поза граматикою — {len(bad)} рядків:")
        for n, l in bad[:20]:
            print(f"  {n}: {l}")
    sys.exit(1 if bad or back or off else 0)


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        pass
