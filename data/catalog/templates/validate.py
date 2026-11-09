"""Check a reference description against the vocab and the catalog before it reaches the site.
Run from the repo root: cd app/api && uv run python -I ../../data/catalog/templates/validate.py <template.yaml> [more…]"""
import importlib.util
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location("vocab", ROOT / "app/api/models/vocab.py")
vocab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vocab)


def catalog() -> tuple[set, set]:
    tree = yaml.safe_load((ROOT / "data/catalog/tasks.yaml").read_text())
    slugs, windows = set(), set()

    def take(slug, node):
        slugs.add(slug)
        if (isinstance(node, str) and "#window" in node) or (isinstance(node, dict) and "window" in node.get("tags", [])):
            windows.add(slug)

    for subs in tree.values():
        for items in subs.values():
            for item in items:
                slug = next(k for k in item if k != "children")
                take(slug, item[slug])
                for ch in item.get("children") or []:
                    take(*next(iter(ch.items())))
    return slugs, windows


SLUGS, WINDOWS = catalog()


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


def check_claim(x, where, problems):
    slug = x if isinstance(x, str) else x.get("slug")
    if slug not in SLUGS:
        problems.append(f"{where}: картки «{slug}» нема в каталозі")


def validate(path: Path) -> list[str]:
    t = yaml.safe_load(path.read_text()) or {}
    problems = []
    for key in t:
        if key not in ("field", "entities", "rules", "windows", "claims"):
            problems.append(f"зайва секція «{key}»")
    field = t.get("field") or {}
    specs = {f["key"]: f for f in vocab.FIELD}
    for k, v in field.items():
        if k not in specs:
            problems.append(f"field: невідома властивість «{k}»")
        elif specs[k]["type"] == "choice" and str(v) not in specs[k]["options"]:
            problems.append(f"field.{k} = {v!r} — зі списку {list(specs[k]['options'])}")
    entities = {str(e.get("title", "")).lower() for e in t.get("entities") or []}
    windows = {str(w.get("title", "")).lower() for w in t.get("windows") or []}
    for e in t.get("entities") or []:
        if not e.get("title"):
            problems.append("entity без title")
        if e.get("role") not in vocab.ROLES:
            problems.append(f"entity «{e.get('title')}»: роль «{e.get('role')}» не зі словника")
        for s in e.get("stats") or []:
            if not s.get("key") or s.get("value") in (None, ""):
                problems.append(f"entity «{e.get('title')}»: stat без key/value: {s}")
        for x in e.get("claims") or []:
            check_claim(x, f"entity «{e.get('title')}»", problems)
    for w in t.get("windows") or []:
        if w.get("task") not in WINDOWS:
            problems.append(f"window «{w.get('title')}»: «{w.get('task')}» — не картка типу вікна")
        for x in w.get("claims") or []:
            check_claim(x, f"window «{w.get('title')}»", problems)
        for it in w.get("items") or []:
            if it.get("window") and str(it["window"]).lower() not in windows:
                problems.append(f"window «{w.get('title')}»: пункт «{it.get('title')}» веде на невідоме вікно «{it['window']}»")
            if it.get("task") and it["task"] not in SLUGS:
                problems.append(f"window «{w.get('title')}»: пункт «{it.get('title')}» веде на невідому картку «{it['task']}»")
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
    for x in t.get("claims") or []:
        check_claim(x, "claims", problems)
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
