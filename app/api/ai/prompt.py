"""The model's instruction (T291 §14): prompt.md with the vocab, the catalog's index and the examples put in — the same bytes
on every request, so the API caches it (no dates, the catalog's order); and the user's message — what the game has already
and the student's text."""
import json
import re
from pathlib import Path

from ai.source import CLAIMED, Source
from models.vocab import CONDITIONS, EFFECTS, FIELD, LEVEL, OPTIONS, TRIGGERS
from zones import ZONES, kind_of

DIR = Path(__file__).parent
TYPES = {"entity": "сутність", "window": "вікно", "int": "число", "text": "текст", "bool": "так/ні"}
EMPTY = {"base": "", "field": False, "entities": [], "windows": [], "levels": []}


def first(text: str, cap: int = 200) -> str:
    """A description's first sentence, on one line."""
    text = " ".join(text.split())
    m = re.search(r"[.!?](\s|$)", text)
    s = text[:m.end()].strip() if m else text
    return s if len(s) <= cap else s[:cap - 1].rstrip() + "…"


def arg(a: dict) -> str:
    t = a["type"]
    return f"{a['name']}{'' if a['required'] else '?'}: {TYPES.get(t) or 'вибір ' + t[7:]}"


def words(title: str, dic: dict) -> list[str]:
    out, group = [f"## {title}"], None
    for kind, spec in dic.items():
        if spec["group"] != group:
            group = spec["group"]
            out += ["", f"### {group}"]
        out.append(f"- `{kind}` — {spec['label']}" + (" · " + ", ".join(map(arg, spec["args"])) if spec["args"] else ""))
    return out + [""]


def prop(spec: dict, values: dict[str, str]) -> str:
    head = f"- `{spec['key']}` — {spec['label'].split(':')[0]}"
    if spec["type"] == "bool":
        return f'{head}: `"on"` — {spec["label"]}'
    if spec["type"] != "choice":
        return head + ", текст" + (f" ({spec['hint']})" if spec.get("hint") else "")
    many = "кілька значень" if spec.get("multi") else "одне значення"
    return f"{head}, {many}: " + " · ".join(f"`{v}` — {label}" for v, label in values.items())


def vocab(src: Source) -> str:
    out = ["Аргумент — `імʼя: тип`; `?` — необовʼязковий. Значення аргументу «вибір <список>» — з «Списків вибору».", ""]
    out += words("КОЛИ — тригери (`when.kind`)", TRIGGERS)
    out += words("ЯКЩО — умови (`cond[].kind`; `not: true` — заперечення)", CONDITIONS)
    out += words("ТО — ефекти (`then[].kind`)", EFFECTS)
    out += ["## Списки вибору", ""] + [f"- `{k}`: " + ", ".join(f"`{v}` — {label}" for v, label in o.items()) for k, o in OPTIONS.items()]
    opts = src.opts("fieldopt")
    out += ["", "## Поле (`field`)", ""] + [prop(f, {v: opts[f"{f['key']}:{v}"].title for v in src.values(f["key"])})
                                            for f in FIELD if f["key"] != "layers"]
    out += ["", "## Рівень (`levels[]`)", ""] + [prop(f, f.get("options") or {}) for f in LEVEL]
    out += ["", "## Типи сутностей (`entities[].role`)", ""] + [f"- `{o}` · {t.title} — {first(t.description)}" for o, t in src.opts("role").items()]
    out += ["", "## Параметри сутностей (`entities[].stats[].key`)", ""]
    out += [f"- `{o}` · {t.title}" + (f" · {t.slots[0]['unit']}" if t.slots and t.slots[0].get("unit") else "") for o, t in src.opts("stat").items()]
    out += ["", "## Типи вікон (`windows[].task`)", ""] + [f"- `{t.slug}` · {t.title} — {first(t.description)}" for t in src.of("window")]
    return "\n".join(out)


def slot(s: dict) -> str:
    t = s.get("type", "int")
    return f"{s['key']} (" + ("вибір: " + "|".join(s.get("options", [])) if t == "choice" else TYPES.get(t, t)) + ")"


def catalog(src: Source) -> str:
    out, head = [], None
    for t in src.of(*CLAIMED):
        if (t.zone, t.subzone) != head:
            head = (t.zone, t.subzone)
            zone = ZONES.get(t.zone, {"title": t.zone, "subzones": {}})
            out += ["", f"## {zone['title']} → {zone['subzones'].get(t.subzone, (t.subzone,))[0]}", ""]
        params = f" · [параметри: {', '.join(map(slot, t.slots))}]" if t.slots else ""
        out.append(f"- `{t.slug}` · {kind_of(t)} · {t.title} — {first(t.description)}{params}")
    return "\n".join(out).strip()


def message(have: dict, text: str) -> str:
    """The changing part of a request: what the game has (not to be proposed again) and the student's text."""
    names = lambda key: ", ".join(have.get(key) or []) or "—"  # noqa: E731
    return "\n".join([
        "Уже є в грі:", f"- основа: {have.get('base') or '—'}", f"- поле: {'є' if have.get('field') else 'нема'}",
        f"- сутності: {names('entities')}", f"- вікна: {names('windows')}", f"- рівні: {names('levels')}", "",
        "<text>", text.replace("</text>", "</ text>"), "</text>"])


def examples() -> str:
    out = []
    for i, x in enumerate(json.loads((DIR / "examples.json").read_text()), 1):
        out += [f"## Приклад {i}", "", "Повідомлення:", "", message(x["have"], x["text"]), "", "Відповідь:", "",
                "```json", json.dumps(x["answer"], ensure_ascii=False, indent=1), "```", ""]
    return "\n".join(out).strip()


def stable(src: Source) -> str:
    text = (DIR / "prompt.md").read_text()
    return text.replace("{{vocab}}", vocab(src)).replace("{{catalog}}", catalog(src)).replace("{{examples}}", examples())
