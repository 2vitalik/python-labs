"""vocab/code-words.md from app/api/models/vocab.py: the words the site's forms offer today (roles, triggers, conditions,
effects, field props, stats) — for agents these are ✅ next to the corpus vocab files; lint and rule_words.py read them too."""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODE = ROOT.parents[1] / "app" / "api" / "models" / "vocab.py"


def load():
    spec = importlib.util.spec_from_file_location("site_vocab", CODE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def words() -> dict[str, set[str]]:
    v = load()
    return {"roles": set(v.ROLES), "triggers": set(v.TRIGGERS), "conditions": set(v.CONDITIONS), "effects": set(v.EFFECTS)}


def main():
    v = load()
    out = ["# Слова коду сайту (автоген)", "",
           f"`scripts/code_vocab.py` з `app/api/models/vocab.py` · ролей {len(v.ROLES)} · тригерів {len(v.TRIGGERS)} · умов {len(v.CONDITIONS)} · "
           f"ефектів {len(v.EFFECTS)}. Це словник форм «Моєї гри» (T259): у корпусі ці слова — ✅ нарівні зі словниками `vocab/*.md`; "
           "аргументи — як у шаблоні речення.", ""]
    out += ["## Ролі", "", "| slug | назва | група |", "|---|---|---|"] + [f"| `{k}` | {l} {i} | {g} |" for k, (l, i, g) in v.ROLES.items()] + [""]
    for title, dic in (("Тригери — КОЛИ", v.TRIGGERS), ("Умови — ЯКЩО", v.CONDITIONS), ("Ефекти — ТО", v.EFFECTS)):
        out += [f"## {title}", "", "| slug | речення | аргументи | група |", "|---|---|---|---|"]
        out += [f"| `{k}` | {w['label']} | {', '.join(a['name'] + ':' + a['type'] for a in w['args'])} | {w['group']} |" for k, w in dic.items()]
        out.append("")
    out += ["## Поле (`Part kind=field`)", ""] + [f"- `{p['key']}` — {p['label']}" + (f": {', '.join(p['options'])}" if p.get("options") else "") for p in v.FIELD]
    out += ["", "## Характеристики сутності", ""] + [f"- `{k}` — {l} {i}" + (f" ({u})" if u else "") for k, l, i, u in v.STATS]
    (ROOT / "vocab" / "code-words.md").write_text("\n".join(out) + "\n")
    print(f"code-words.md: {sum(len(s) for s in words().values())} words")


if __name__ == "__main__":
    sys.exit(main())
