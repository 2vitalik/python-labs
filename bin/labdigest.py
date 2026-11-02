"""Digest of one lab's reviews (T254): header × profile × facts consistency, extra_missing against the AST counters, tables by group
and the distributions. Prints Markdown; bin/repos digest runs it, the per-student table is `bin/repos reviews --dry`."""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean

# an item of the lab's extra list, as the agent names it → the facts' syntax counter
AST = {"or": "or", "and": "and", "not": "not", "nonlocal": "nonlocal", "global": "global", "lambda": "lambda", "float": "float", "a<b<c": "chain",
       "for-else": "loop_else", "continue": "continue", "break": "break", "kwargs": "kwdefault", "*": "star", "/": "slash", "nested": "nested",
       "elif": "elif", "else": "else", "bool": "bool", "None": "none", "range": "range", "for": "for", "while": "while", "int": "int", "str": "str"}
done = lambda req: sum(1 for x in req if x == "done")


def header(path: Path) -> dict:
    head, _, body = path.read_text()[4:].partition("\n---\n")
    d = {k.strip(): v.strip() for k, _, v in (line.partition(":") for line in head.splitlines()) if k.strip()}
    return d | {"required": d.get("required", "").split(), "lines": body.strip().count("\n") + 1, "evidence": len(re.findall(r"[\w./-]+\.py:\d+", body))}


def check(nick: str, h: dict, p: dict | None, f: dict | None) -> list[str]:
    out = [] if p else ["нема profile.json"]
    if len(h["required"]) != 6:
        out.append(f"required має {len(h['required'])} слів")
    if len(h.get("summary", "")) > 100:
        out.append(f"summary {len(h['summary'])} знаків")
    if not 25 <= h["lines"] <= 80:
        out.append(f"тіло {h['lines']} рядків")
    for k in ("kind", "verdict", "head_verdict"):
        if p and str(p.get(k, "")) != h.get(k, ""):
            out.append(f"{k}: шапка «{h.get(k)}», профіль «{p.get(k)}»")
    if p and p.get("required") != h["required"]:
        out.append(f"required різні: шапка {h['required']} · профіль {p.get('required')}")
    for item in (p or {}).get("extra_missing") or []:
        key = AST.get(item.strip("`"))
        if f and key and f["code"]["syntax"].get(key, 0):
            out.append(f"«{item}» у extra_missing, а AST бачить {key}={f['code']['syntax'][key]} (можливо, не в лабі)")
    return [f"{nick}: {x}" for x in out]


def digest(reviews: Path, lab: int, group_of: dict[str, str]) -> str:
    rows, problems = [], []
    for md in sorted(reviews.glob(f"*/lab{lab}.md")):
        nick = md.parent.name
        if nick.startswith("."):
            continue
        p = json.loads(md.with_suffix(".profile.json").read_text()) if md.with_suffix(".profile.json").exists() else None
        f = json.loads(md.with_suffix(".facts.json").read_text()) if md.with_suffix(".facts.json").exists() else None
        h = header(md)
        problems += check(nick, h, p, f)
        rows.append((group_of.get(nick, "?"), h, p or {}, f or {}))
    out = [f"# Лаба {lab} · звітів {len(rows)} · проблем {len(problems)}", ""] + [f"- {x}" for x in problems]
    by = defaultdict(list)
    for r in rows:
        by[r[0]].append(r)
    out += ["", "| Група | Звітів | game | tasks | other | none | done | partial | none | 6/6 | 4–5 | ≤3 | рівень | ШІ strong/weak |",
            "|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|"]
    for g in sorted(by):
        rs = by[g]
        kind, verd = Counter(h.get("kind", "") for _, h, _, _ in rs), Counter(h.get("verdict", "") for _, h, _, _ in rs)
        dn, lvl = [done(h["required"]) for _, h, _, _ in rs], [p["level"] for _, _, p, _ in rs if isinstance(p.get("level"), (int, float))]
        ai = Counter((p.get("ai") or {}).get("level") for _, _, p, _ in rs)
        out.append(f"| {g} | {len(rs)} | {kind['game']} | {kind['tasks']} | {kind['other']} | {kind['none']} | {verd['done']} | {verd['partial']} | {verd['none']} | "
                   f"{sum(x == 6 for x in dn)} | {sum(4 <= x <= 5 for x in dn)} | {sum(x <= 3 for x in dn)} | {mean(lvl):.1f} | {ai['strong']}/{ai['weak']} |" if lvl else
                   f"| {g} | {len(rs)} | {kind['game']} | {kind['tasks']} | {kind['other']} | {kind['none']} | {verd['done']} | {verd['partial']} | {verd['none']} | "
                   f"{sum(x == 6 for x in dn)} | {sum(4 <= x <= 5 for x in dn)} | {sum(x <= 3 for x in dn)} | — | — |")
    out.append("")
    dist = (("kind", lambda h, p, f: h.get("kind")), ("verdict", lambda h, p, f: h.get("verdict")), ("✔/6", lambda h, p, f: done(h["required"])),
            ("ui", lambda h, p, f: f.get("code", {}).get("ui")), ("рівень", lambda h, p, f: p.get("level")), ("ШІ", lambda h, p, f: (p.get("ai") or {}).get("level")),
            ("ритм", lambda h, p, f: (p.get("process") or {}).get("rhythm")), ("дати", lambda h, p, f: (p.get("process") or {}).get("dates")),
            ("повідомлення", lambda h, p, f: (p.get("process") or {}).get("messages")), ("впевненість", lambda h, p, f: p.get("confidence")),
            ("game.input", lambda h, p, f: (p.get("game") or {}).get("input")), ("game.field", lambda h, p, f: (p.get("game") or {}).get("field")))
    for name, get in dist:
        c = Counter(get(h, p, f) for _, h, p, f in rows)
        out.append(f"- **{name}**: " + " · ".join(f"{k} {v}" for k, v in sorted(c.items(), key=lambda kv: -kv[1])))
    miss = Counter(item for _, _, p, _ in rows for item in (p.get("extra_missing") or []))
    out.append("- **чого бракує найчастіше (extra_missing)**: " + " · ".join(f"{k} {v}" for k, v in miss.most_common(15)))
    return "\n".join(out)
