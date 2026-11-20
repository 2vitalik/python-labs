"""What bin/lecchanges prints: a lecture's line, its `todo`, the checks, the table of all lectures."""
import re
from collections import Counter

import store
from build import build
from classify import KINDS, ORIGIN, STATUS, WHERE, problems


def line(data: dict, hows: Counter, state: str) -> str:
    edits = sum(len(it["edits"]) for it in data["items"])
    return (f"{data['slug']}: записів {len(data['items'])} · правок {edits} · авто {hows['auto']} · за правилами {hows['rule']}"
            f" · за нотатками {hows['key']} · з журналу {hows['journal']} · склад {hows['set']} · todo {data['todo']} · {state}")


def around(text: str, span: list[int], words: int = 5) -> str:
    left = " ".join(text[:span[0]].split()[-words:])
    right = " ".join(text[span[1]:].split()[:words])
    return f"…{left} ⟦{text[span[0]:span[1]]}⟧ {right}…"


def todo(data: dict):
    rows = [it for it in data["items"] if it["kind"] == "todo"]
    for it in rows:
        e, h = it["edits"][0], data["hunks"][it["hunk"]]
        hint = " · ru?" if re.search(r"[ыэъё]", e["del"], re.IGNORECASE) else ""
        print(f"{it['id'].split('-', 1)[1]} · сл. {it['slide']} · {e['del'] or '∅'} → {e['ins'] or '∅'}{hint}")
        print(f"    {around(h['after'], e['b']) if h['after'] else around(h['before'], e['a'])}")
    print(f"{data['slug']}: todo {len(rows)}")


def wrong(it: dict) -> list[str]:
    bad = [f"kind {it['kind']}"] if it["kind"] not in KINDS else []
    bad += [f"sev {it['sev']}"] if it["sev"] not in (0, 1, 2, 3) else []
    bad += [f"status {it['status']}"] if it["status"] not in STATUS else []
    bad += [f"where {it['where']}"] if it["where"] not in WHERE else []
    bad += [f"origin {it['origin']}"] if it["origin"] not in ORIGIN else []
    return [f"{it['id']}: " + ", ".join(bad)] if bad else []


def check(lecs: list[int]) -> int:
    bad, todos = [p for i, r in enumerate(store.rules()) for p in problems(r, f"rules.json #{i + 1}")], 0
    for n in lecs:
        data, meta = build(n)
        notes = store.notes(n)
        bad += [p for i, r in enumerate(notes.get("rules", [])) for p in problems(r, f"notes/lec{n:02}.json rules #{i + 1}")]
        bad += [p for k, v in notes.get("keys", {}).items() for p in problems(v, f"notes/lec{n:02}.json {k}")]
        stale = sorted(set(notes.get("keys", {})) - meta["keys"])
        bad += [w for it in data["items"] for w in wrong(it)]
        todos += data["todo"]
        old = store.built(n)
        print(f"lec{n:02}: todo {data['todo']}" + (f" (bin/lecchanges todo {n})" if data["todo"] else "")
              + (f" · ключів нотаток без правки {len(stale)}: {', '.join(stale[:5])}" if stale else "")
              + ("" if old and {**old, "built": ""} == {**data, "built": ""} else " · файл застарів — bin/lecchanges build"))
    print("\n".join(bad))
    return 1 if bad or todos else 0


def stats(lecs: list[int]):
    """Items by group and by what classified them; the journal's entries by section (A, B, G, H — ids, not items)."""
    cols = ["content", "lang", "look", "media", "set", "open", "todo"]
    head = ["лекція", "записів", "правок", *cols, "авто", "правила", "нотатки", "журнал", "A", "B", "G", "H"]
    print("| " + " | ".join(head) + " |\n|" + "--:|" * len(head))
    total = Counter()
    for n in lecs:
        data, meta = build(n)
        hows, g = meta["hows"], Counter(it["group"] for it in data["items"])
        refs = Counter(r[3] for r in {it["ref"].split(".")[0] for it in data["items"] if it["ref"]})
        row = [len(data["items"]), sum(len(it["edits"]) for it in data["items"]), *(g[c] for c in cols),
               hows["auto"], hows["rule"], hows["key"], hows["journal"], *(refs[x] for x in "ABGH")]
        total.update(dict(enumerate(row)))
        print(f"| {n:02} | " + " | ".join(map(str, row)) + " |")
    print("| **Σ** | " + " | ".join(str(total[i]) for i in range(len(head) - 1)) + " |")
