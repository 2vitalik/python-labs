"""Check a reference description against the vocab and the catalog before it reaches the site: the words, the cards,
and each card's kind against the place it is written at (T270 §6) — what the import would skip or leave in the drafts.
Run from the repo root: cd app/api && uv run python -I ../../data/catalog/templates/validate.py <template.yaml> [more…]"""
import importlib.util
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    sys.modules[name] = mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


vocab, zones = load("vocab", "app/api/models/vocab.py"), load("zones", "app/api/zones.py")
taskline = load("taskline", "app/api/taskline.py")  # after zones: it imports it


def catalog() -> dict[str, dict]:
    """slug → {kind, opt, status, slots} of every card in tasks.yaml."""
    cards = {}

    def take(slug, node, zone, sub):
        d = taskline.parse_line(slug, node, zone, sub, 0) if isinstance(node, str) else {"tags": [], "kind": "", "opt": "", "status": "draft"} | node
        cards[slug] = {"kind": d["kind"] or zones.default_kind(zone, sub, d["tags"]), "opt": d["opt"], "status": d["status"],
                       "slots": {s["key"] for s in d.get("slots") or []}}

    for zone, subs in yaml.safe_load((ROOT / "data/catalog/tasks.yaml").read_text()).items():
        for sub, items in subs.items():
            for item in items:
                slug = next(k for k in item if k != "children")
                take(slug, item[slug], zone, sub)
                for ch in item.get("children") or []:
                    take(*next(iter(ch.items())), zone, sub)
    return cards


CARDS = catalog()
OPTS = {k: {c["opt"] for c in CARDS.values() if c["kind"] == k and c["opt"] and c["status"] != "archived"} for k in ("role", "stat", "fieldopt")}
LEVEL_KEYS = {"title", "description", "stats", "claims"} | {x["key"] for x in vocab.LEVEL} | {x["key"] for x in vocab.FIELD}


def check_word(dic, item, names, sides, where, problems):
    spec = dic.get(item.get("kind"))
    if not spec:
        problems.append(f"{where}: невідоме слово «{item.get('kind')}»")
        return
    known = {a["name"] for a in spec["args"]}
    for k in item:
        if k not in known and k not in ("kind", "not"):
            problems.append(f"{where} «{item['kind']}»: зайвий аргумент «{k}» (є: {', '.join(known) or '—'})")
    for a in spec["args"]:
        v = item.get(a["name"])
        if v is None or v == "":
            if a["required"]:
                problems.append(f"{where} «{item['kind']}»: нема «{a['name']}»")
            continue
        t = a["type"]
        if t == "entity" and str(v) not in sides and str(v).lower() not in names:
            problems.append(f"{where} «{item['kind']}»: «{v}» — не сутність еталона")
        elif t == "window" and str(v).lower() not in names:
            problems.append(f"{where} «{item['kind']}»: «{v}» — не вікно еталона")
        elif t == "int" and not isinstance(v, int):
            problems.append(f"{where} «{item['kind']}»: «{a['name']}» = {v!r} — має бути число")
        elif t.startswith("choice:") and str(v) not in vocab.OPTIONS[t[7:]]:
            problems.append(f"{where} «{item['kind']}»: «{a['name']}» = {v!r} — зі списку {list(vocab.OPTIONS[t[7:]])}")


def check_claim(x, where: str, label: str, has_field: bool, problems):
    """`where` — a part's kind, "rule", or "game" for the top-level claims."""
    slug = x if isinstance(x, str) else x.get("slug")
    if slug not in CARDS:
        return problems.append(f"{label}: картки «{slug}» нема в каталозі")
    if CARDS[slug]["status"] == "archived":
        return problems.append(f"{label}: «{slug}» — картка в архіві")
    if extra := set(x.get("params") or {} if isinstance(x, dict) else {}) - CARDS[slug]["slots"]:
        problems.append(f"{label}: «{slug}» не має параметрів {sorted(extra)}")
    kind = CARDS[slug]["kind"]
    if where != "game":
        why = zones.misplaced(kind, where)
    elif kind in zones.AUTO_KINDS:
        why = zones.AUTO
    elif kind == "field":
        why = "" if has_field else "картка поля, а поля в еталоні нема — ляже в «📥 Чернетки»"
    else:
        why = "" if kind in ("level", "game") else f"ляже студентові в «📥 Чернетки»: {zones.HOMES[kind][1]}"
    if why:
        problems.append(f"{label}: «{slug}» ({zones.KINDS[kind]}) — {why}")


def check_props(props: dict, specs: list[dict], where: str, problems):
    for spec in specs:
        v = props.get(spec["key"])
        if spec["type"] != "choice" or v in (None, "", []):
            continue
        values = v if isinstance(v, list) else [v]
        if len(values) > 1 and not spec.get("multi"):
            problems.append(f"{where}.{spec['key']} = {v!r} — одне значення")
        allowed = spec.get("options") or {o.split(":", 1)[1] for o in OPTS["fieldopt"] if o.startswith(spec["key"] + ":")}
        for x in values:
            if str(x) == "none":
                problems.append(f"{where}.{spec['key']} = none — прибери: не задано — це і є «нема»")
            elif str(x) not in allowed:
                problems.append(f"{where}.{spec['key']} = {x!r} — зі списку {sorted(allowed)}")


def check_stats(stats: list, where: str, problems):
    taken = set()
    for s in stats:
        if not s.get("key") or s.get("value") in (None, ""):
            problems.append(f"{where}: stat без key/value: {s}")
        names = {str(s.get("key", "")).lower(), str(s.get("label") or "").lower()} - {""}
        if names & taken:
            problems.append(f"{where}: параметр «{s.get('key')}» двічі")
        taken |= names


def validate(path: Path) -> list[str]:
    t = yaml.safe_load(path.read_text()) or {}
    problems = []
    for key in t:
        if key not in ("field", "entities", "rules", "windows", "levels", "claims"):
            problems.append(f"зайва секція «{key}»")
    field = t.get("field") or {}
    specs = {f["key"] for f in vocab.FIELD}
    problems += [f"field: невідома властивість «{k}»" for k in field if k not in specs]
    check_props(field, vocab.FIELD, "field", problems)
    entities = {str(e.get("title", "")).lower() for e in t.get("entities") or []}
    windows = {str(w.get("title", "")).lower() for w in t.get("windows") or []}
    for e in t.get("entities") or []:
        where = f"entity «{e.get('title')}»"
        if not e.get("title"):
            problems.append("entity без title")
        if e.get("role") not in OPTS["role"]:
            problems.append(f"{where}: тип «{e.get('role')}» — не картка типу сутності")
        if len(str(e.get("icon") or "")) > 16:
            problems.append(f"{where}: іконка задовга")
        check_stats(e.get("stats") or [], where, problems)
        for x in e.get("claims") or []:
            check_claim(x, "entity", where, bool(field), problems)
    for w in t.get("windows") or []:
        task = CARDS.get(w.get("task"))
        if not task or task["kind"] != "window" or task["status"] == "archived":
            problems.append(f"window «{w.get('title')}»: «{w.get('task')}» — не картка типу вікна (або вона в архіві)")
        for x in w.get("claims") or []:
            check_claim(x, "window", f"window «{w.get('title')}»", bool(field), problems)
        for it in w.get("items") or []:
            if it.get("window") and str(it["window"]).lower() not in windows:
                problems.append(f"window «{w.get('title')}»: пункт «{it.get('title')}» веде на невідоме вікно «{it['window']}»")
            if it.get("task") and it["task"] not in CARDS:
                problems.append(f"window «{w.get('title')}»: пункт «{it.get('title')}» веде на невідому картку «{it['task']}»")
    for lv in t.get("levels") or []:
        where = f"level «{lv.get('title')}»"
        if not lv.get("title"):
            problems.append("level без title")
        problems += [f"{where}: невідома властивість «{k}»" for k in lv if k not in LEVEL_KEYS]
        check_props(lv, vocab.LEVEL + vocab.FIELD, where, problems)
        check_stats(lv.get("stats") or [], where, problems)
        for x in lv.get("claims") or []:
            check_claim(x, "level", where, bool(field), problems)
    names = entities | windows
    for i, r in enumerate(t.get("rules") or [], 1):
        when = r.get("when") or {}
        check_word(vocab.TRIGGERS, when, names, {"*"}, f"правило {i} КОЛИ", problems)
        sides = {"*"} | {s for s in ("@a", "@b") if s[1:] in when} | ({"@both"} if "a" in when and "b" in when else set())
        for c in r.get("cond") or []:
            check_word(vocab.CONDITIONS, c, names, sides, f"правило {i} ЯКЩО", problems)
        if not r.get("then"):
            problems.append(f"правило {i}: нема ТО")
        for e in r.get("then") or []:
            check_word(vocab.EFFECTS, e, names, sides, f"правило {i} ТО", problems)
        for x in r.get("claims") or []:
            check_claim(x, "rule", f"правило {i}", bool(field), problems)
    for x in t.get("claims") or []:
        check_claim(x, "game", "claims", bool(field), problems)
    return problems


if __name__ == "__main__":
    bad = 0
    for arg in sys.argv[1:]:
        p = Path(arg)
        problems = validate(p)
        bad += bool(problems)
        print(f"{p.name}: {'ok' if not problems else f'{len(problems)} проблем'}")
        for x in problems:
            print("  -", x)
    sys.exit(1 if bad else 0)
