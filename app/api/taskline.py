"""One-line task format for tasks.yaml (T77 + Vitalik's tweaks):
'🥉[×N] Назва [game, game] @kind ⭐ #tag 🔁[N] ✍️ — опис' · no status mark = active · no @kind = the subzone's (T270).
A rule-card's blank rides in the same token: '@rule(contact?free>push)' or, with the subzone's kind, '@(all_gone>win)'."""
import re

from zones import KINDS

COIN_EMOJI = {"wood": "🌱", "tin": "📎", "bronze": "🥉", "silver": "🥈", "gold": "🥇", "crown": "👑"}
EMOJI_COIN = {v: k for k, v in COIN_EMOJI.items()}
COIN_RE = "|".join(COIN_EMOJI.values())
KIND_RE = rf"(?<!\S)@({'|'.join(KINDS)})(?!\S)"
BLANK_RE = rf"(?<!\S)@({'|'.join(KINDS)}|)\(([^)\s]*)\)"


def fmt_num(x: float) -> str:
    return str(int(x)) if x == int(x) else str(x)


def plain(rule: dict) -> bool:
    """A blank of words alone, no arguments — the kind that fits one token."""
    return all(set(it) <= {"kind"} for it in [rule.get("when") or {}, *(rule.get("cond") or []), *(rule.get("then") or [])])


def blank(rule: dict) -> str:
    """when?cond+cond>then+then"""
    cond = "+".join(c["kind"] for c in rule.get("cond") or [])
    return (rule.get("when") or {}).get("kind", "") + (f"?{cond}" if cond else "") + ">" + "+".join(e["kind"] for e in rule.get("then") or [])


def unblank(text: str) -> dict:
    head, _, then = text.partition(">")
    when, _, cond = head.partition("?")
    lists = {"cond": [{"kind": k} for k in cond.split("+") if k], "then": [{"kind": k} for k in then.split("+") if k]}
    return ({"when": {"kind": when}} if when else {}) | {k: v for k, v in lists.items() if v}


def render_line(t) -> str:
    parts = []
    if t.coin:
        parts.append(COIN_EMOJI[t.coin] + (f"×{fmt_num(t.amount)}" if t.amount != 1 else ""))
    parts.append(t.title)
    if t.games:
        parts.append("[" + ", ".join(t.games) + "]")
    if t.rule:
        parts.append(f"@{t.kind}({blank(t.rule)})")
    elif t.kind:
        parts.append("@" + t.kind)
    if "algo" in t.tags:
        parts.append("⭐")
    parts += [f"#{x}" for x in t.tags if x != "algo"]
    if t.max_count == 0:
        parts.append("🔁")
    elif t.max_count > 1:
        parts.append(f"🔁{t.max_count}")
    if t.status != "active":
        parts.append({"draft": "✍️", "archived": "🗄️"}[t.status])
    line = " ".join(parts)
    if t.description:
        line += " — " + t.description
    return line


def parse_line(slug: str, line: str, zone: str, subzone: str, order: int) -> dict:
    d = {"slug": slug, "zone": zone, "subzone": subzone, "order": order, "description": "", "kind": "", "icon": "", "opt": "",
         "rule": {}, "tags": [], "games": [], "coin": "", "amount": 1.0, "max_count": 1, "status": "active", "parent": ""}
    if " — " in line:
        line, d["description"] = (s.strip() for s in line.split(" — ", 1))
    if m := re.search(r"\[([^\]]*)\]", line):
        d["games"] = [g.strip() for g in m.group(1).split(",") if g.strip()]
        line = line.replace(m.group(0), " ")
    if m := re.search(BLANK_RE, line):
        d["kind"], d["rule"] = m.group(1), unblank(m.group(2))
        line = line[:m.start()] + " " + line[m.end():]
    elif m := re.search(KIND_RE, line):
        d["kind"] = m.group(1)
        line = line[:m.start()] + " " + line[m.end():]
    if m := re.match(rf"\s*({COIN_RE})(?:×(\d+(?:\.\d+)?))?", line):
        d["coin"], d["amount"] = EMOJI_COIN[m.group(1)], float(m.group(2) or 1)
        line = line[m.end():]
    if "⭐" in line:
        d["tags"].append("algo")
        line = line.replace("⭐", " ")
    d["tags"] += re.findall(r"#([\w-]+)", line)
    line = re.sub(r"#[\w-]+", " ", line)
    for mark, status in (("✍️", "draft"), ("✍", "draft"), ("🗄️", "archived"), ("🗄", "archived")):
        if mark in line:
            d["status"] = status
            line = line.replace(mark, " ")
    if m := re.search(r"🔁(\d*)", line):
        d["max_count"] = int(m.group(1)) if m.group(1) else 0
        line = line[:m.start()] + " " + line[m.end():]
    d["title"] = " ".join(line.split())
    return d
