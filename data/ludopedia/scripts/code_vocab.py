"""vocab/code-words.md: the words the site's forms offer today — triggers, conditions, effects and the field's properties from
app/api/models/vocab.py; entity roles, stats and the field's options from data/catalog/tasks.yaml (cards with `opt`, T270).
For agents these are ✅ next to the corpus vocab files; lint and rule_words.py read them too.
Run: cd app/api && uv run python ../../data/ludopedia/scripts/code_vocab.py"""
import importlib.util
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
API = REPO / "app" / "api"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    sys.modules[name] = mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def cards() -> list[dict]:
    """The catalog's cards with an `opt`, not archived: {opt, kind, title, icon, unit, group} — group is the family's title."""
    zones = load("zones", API / "zones.py")
    taskline = load("taskline", API / "taskline.py")  # after zones: it imports it
    out = []

    def take(slug, node, zone, sub, family=""):
        d = taskline.parse_line(slug, node, zone, sub, 0) if isinstance(node, str) else {"kind": "", "tags": [], "status": "draft"} | node
        if d.get("opt") and d["status"] != "archived":
            out.append({"opt": d["opt"], "kind": d["kind"] or zones.default_kind(zone, sub, d["tags"]), "title": d["title"],
                        "icon": d.get("icon", ""), "unit": (d.get("slots") or [{}])[0].get("unit", ""), "group": family})
        return d["title"]

    for zone, subs in yaml.safe_load((REPO / "data" / "catalog" / "tasks.yaml").read_text()).items():
        for sub, items in subs.items():
            for item in items:
                slug = next(k for k in item if k != "children")
                family = take(slug, item[slug], zone, sub)
                for ch in item.get("children") or []:
                    take(*next(iter(ch.items())), zone, sub, family)
    return out


def words() -> dict[str, set[str]]:
    v = load("site_vocab", API / "models" / "vocab.py")
    roles = {c["opt"] for c in cards() if c["kind"] == "role"}
    return {"roles": roles, "triggers": set(v.TRIGGERS), "conditions": set(v.CONDITIONS), "effects": set(v.EFFECTS)}


def main():
    v = load("site_vocab", API / "models" / "vocab.py")
    by_kind = {k: [c for c in cards() if c["kind"] == k] for k in ("role", "stat", "fieldopt")}
    out = ["# Слова коду сайту (автоген)", "",
           f"`scripts/code_vocab.py` з `app/api/models/vocab.py` і карток `data/catalog/tasks.yaml` з `opt` · ролей {len(by_kind['role'])} · "
           f"тригерів {len(v.TRIGGERS)} · умов {len(v.CONDITIONS)} · ефектів {len(v.EFFECTS)}. Це словник форм «Моєї гри» (T259, T270): "
           "у корпусі ці слова — ✅ нарівні зі словниками `vocab/*.md`; аргументи — як у шаблоні речення.", ""]
    out += ["## Ролі", "", "| slug | назва | група |", "|---|---|---|"]
    out += [f"| `{c['opt']}` | {c['title']} {c['icon']} | {c['group']} |" for c in by_kind["role"]] + [""]
    for title, dic in (("Тригери — КОЛИ", v.TRIGGERS), ("Умови — ЯКЩО", v.CONDITIONS), ("Ефекти — ТО", v.EFFECTS)):
        out += [f"## {title}", "", "| slug | речення | аргументи | група |", "|---|---|---|---|"]
        out += [f"| `{k}` | {w['label']} | {', '.join(a['name'] + ':' + a['type'] for a in w['args'])} | {w['group']} |" for k, w in dic.items()]
        out.append("")
    options = {}
    for c in by_kind["fieldopt"]:
        key, _, value = c["opt"].partition(":")
        options.setdefault(key, []).append(value)
    out += ["## Поле (`Part kind=field`)", ""]
    out += [f"- `{p['key']}` — {p['label']}" + (f": {', '.join(options[p['key']])}" if p["key"] in options else "") for p in v.FIELD]
    out += ["", "## Характеристики сутності", ""]
    out += [f"- `{c['opt']}` — {c['title']} {c['icon']}" + (f" ({c['unit']})" if c["unit"] else "") for c in by_kind["stat"]]
    (ROOT / "vocab" / "code-words.md").write_text("\n".join(out) + "\n")
    print(f"code-words.md: {sum(len(s) for s in words().values())} words · полів {len(v.FIELD)} · варіантів поля {len(by_kind['fieldopt'])} · "
          f"характеристик {len(by_kind['stat'])}")


if __name__ == "__main__":
    sys.exit(main())
