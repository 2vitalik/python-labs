"""A hint at the grade (T354 §4) by the ladder of T228, one for all five labs: the level the work reaches × the form of defence.
Only a hint — the points are the teacher's. A need the file cannot tell (no file, marimo without outputs) is ok: None."""
import math

CAPS = {"none": 12, "record": 16, "live": 20}  # what each form of defence lets in
STEPS = ((12, "Відповіді й запуск", ""), (13, "Половина рівня 14", "record"), (14, "Усе зроблено", "record"),
         (16, "Одна зірочка", "record"), (18, "Дві зірочки", "live"), (19, "Три зірочки", "live"), (20, "Усі зірочки", "live"))


def all3(oks) -> bool | None:
    oks = list(oks)
    return False if False in oks else None if None in oks else True


def need(key: str, ok, text: str) -> dict:
    return {"key": key, "ok": ok, "text": text}


def ran_ok(facts: dict) -> bool | None:
    r = facts.get("ran")
    return None if not r else r["count"] > 0 and r["count"] == r["of"] and r["ordered"] and not r["errors"]


def pair(count: dict, key: str, word: str) -> dict:
    n, of = count.get(key) or [None, None]
    return need(key, None if n is None or of is None else n >= of, f"{word} {'?' if n is None else n} із {'?' if of is None else of}")


def half(count: dict) -> dict:
    """Level 13: at least half of level 14's items — every step, plot and conclusion, and the report."""
    parts = [count.get(k) or [None, None] for k in ("tasks", "plots", "conclusions")] + [[count.get("report"), 1]]
    parts = [[None if p[0] is None else int(p[0]), p[1]] for p in parts]
    if any(of is None for _, of in parts):
        return need("half", None, "половина рівня 14")
    known, unknown, total = sum(n or 0 for n, _ in parts), sum(of for n, of in parts if n is None), sum(of for _, of in parts)
    goal = math.ceil(total / 2)
    ok = True if known >= goal else None if known + unknown >= goal else False
    return need("half", ok, f"пунктів рівня 14: {known}{'+?' if unknown else ''} із {total}")


def grade(ok: int, total: int, checked: bool, facts: dict | None, stars: int | None, way: str) -> dict:
    """GRADE = {steps: [{level, title, way, needs, ok}], work, way, cap, hint}; `stars` — the teacher's word over the file."""
    facts = facts or {}
    count = facts.get("count") or {}
    of_stars = (count.get("stars") or [None, None])[1] or 4
    got = stars if stars is not None else (count.get("stars") or [None])[0]
    needs = {12: [need("answers", checked and total > 0 and ok == total, f"{ok} із {total} ✅"),
                  need("ran", ran_ok(facts) if facts else None, "виконано згори донизу без помилок")],
             13: [half(count)],
             14: [pair(count, "tasks", "кроки"), pair(count, "plots", "графіки"), pair(count, "conclusions", "висновки"),
                  need("report", count.get("report"), "рапорт")]}
    for level, k in ((16, 1), (18, 2), (19, 3), (20, of_stars)):
        needs[level] = [need("stars", None if got is None else got >= k, f"зірочок {k}")]
    steps = [{"level": lv, "title": title, "way": w, "needs": needs[lv], "ok": all3(n["ok"] for n in needs[lv])} for lv, title, w in STEPS]
    ok_at = {s["level"]: s["ok"] is True for s in steps}
    reach = {12: ok_at[12], 13: ok_at[12] and ok_at[13], 14: ok_at[12] and ok_at[14]}
    for prev, lv in ((14, 16), (16, 18), (18, 19), (19, 20)):  # each star level stands on the one below
        reach[lv] = reach[prev] and ok_at[lv]
    work = max((lv for lv, yes in reach.items() if yes), default=None)
    cap = CAPS.get(way)
    return {"steps": steps, "work": work, "way": way, "cap": cap, "hint": None if work is None else min(work, cap or 20)}
