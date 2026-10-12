"""Checking an answer line on the server: the rule of the lab's notebook and check.py, without the generator behind it."""
import math
import re

MISSING = "нема в рядку"
LINE = re.compile(r"LAB(\d+)\s+(\S+)\s*(.*)", re.S)


def parse_line(line: str) -> tuple[int, str, dict]:
    """`LAB1 КН-23-1-07 d1=0.2049 r1=8.18 …` → (lab, vid, {name: value}); a ValueError speaks to the student."""
    m = LINE.fullmatch(line.strip())
    if not m:
        raise ValueError("Рядок має починатися з LAB<номер лаби> і номера варіанта — скопіюй те, що надрукувала остання клітинка")
    values = {}
    for pair in m[3].split():
        name, eq, text = pair.partition("=")
        try:
            values[name] = float(text)
        except ValueError:
            raise ValueError(f"Не розберу «{pair}»: потрібно назва=число") from None
        if not name or math.isnan(values[name]):
            raise ValueError(f"Не розберу «{pair}»: потрібно назва=число")
    return int(m[1]), m[2], values


def near(step: float, got: float, want: float) -> bool:
    """The notebook's own rule (the lab's card.near): the same bucket of `step` or a neighbouring one; exact answers — the same integer."""
    return round(got) == round(want) if not step else abs(round(got / step) - round(want / step)) <= 1


def verdict(values: dict, answers: dict) -> dict:
    """name → {ok, why}: what the student saw as ✅ in the notebook is ✅ here; a known wrong number is named by its cause."""
    out = {}
    for name, a in answers.items():
        got = values.get(name)
        if got is None:
            out[name] = {"ok": False, "why": MISSING}
            continue
        ok = near(a["step"], got, a["value"])
        why = "" if ok else next((t["why"] for t in a.get("traps", []) if near(a["step"], got, t["value"])), "")
        out[name] = {"ok": ok, "why": why}
    return out
