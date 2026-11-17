"""Values of a game's history in words (T278 §12): names instead of ids and slugs, a rule as its sentence, lists in a line."""
from types import SimpleNamespace

from models.vocab import FIELD, LEVEL, sentence

PARTS = {"field": "поле", "level": "рівень", "entity": "сутність", "window": "вікно", "menu": "переходи"}
STATUS = {"claimed": "заявлено", "accepted": "зараховано", "returned": "повернуто"}
PROPS = {p["key"]: p for p in FIELD + LEVEL} | {"map": {"label": "мапа рівня"}}  # a level drawn in cells (T276)
EMPTY = (None, "", [], {})


def plain(v) -> str:
    if isinstance(v, bool):
        return "так" if v else "ні"
    if isinstance(v, list):
        return ", ".join(map(plain, v))
    if isinstance(v, dict):
        return ", ".join(f"{k}: {plain(x)}" for k, x in v.items())
    return str(v)


class Names:
    """Ids and slugs of one game's history → what people call them."""

    def __init__(self, parts: dict, rules: dict, cards: dict, bases: dict, roles: dict, opts: dict):
        self.parts, self.rules, self.cards, self.bases, self.roles, self.opts = parts, rules, cards, bases, roles, opts

    def part(self, pid: str) -> str:
        return self.parts.get(pid, {}).get("title") or "?"

    def where(self, pid: str) -> str:
        p = self.parts.get(pid)
        return f"{PARTS.get(p.get('kind'), '')} «{p.get('title')}»".strip() if p else "?"

    def card(self, slug: str) -> str:
        return self.cards[slug].title if slug in self.cards else slug

    def sentence(self, rule: dict) -> str:
        r = SimpleNamespace(when=rule.get("when") or {}, cond=rule.get("cond") or [], then=rule.get("then") or [])
        return sentence(r, self.part)

    def clause(self, key: str, v, when: dict) -> str:
        """КОЛИ, ЯКЩО or ТО alone, in the sentence's own words: sentence() of a rule that has only it (and its КОЛИ — the sides)."""
        r = SimpleNamespace(when=v if key == "when" else when or {}, cond=v if key == "cond" else [], then=v if key == "then" else [])
        head, _, then = sentence(r, self.part).partition(" → ТО ")
        head, _, cond = head.partition(" → ЯКЩО ")
        return {"when": head.removeprefix("КОЛИ "), "cond": cond, "then": then}[key]

    def prop(self, key: str, v) -> str:
        spec = PROPS.get(key, {})

        def one(x) -> str:
            return plain(x) if isinstance(x, bool) else self.opts.get(f"{key}:{x}") or spec.get("options", {}).get(x) or str(x)
        return f"{spec.get('label', key).split(':')[0]}: {', '.join(map(one, v)) if isinstance(v, list) else one(v)}"

    def item(self, it: dict) -> str:
        to = f" → 🪟 {self.part(it['window'])}" if it.get("window") else f" → ⚙ {self.card(it['task'])}" if it.get("task") else ""
        return (it.get("title") or "без назви") + to + (f" ({it['note']})" if it.get("note") else "")

    def text(self, key: str, v, snap: dict) -> str | None:
        """A field's value in words; None — empty. `snap` — the object: a claim's card names its params, a rule's КОЛИ its sides."""
        if v in EMPTY:
            return None
        slots = {s["key"]: s.get("label", s["key"]) for s in getattr(self.cards.get(snap.get("task")), "slots", [])}
        words = {
            "status": lambda: STATUS.get(v, v), "base_game": lambda: self.bases.get(v, v), "task": lambda: self.card(v),
            "role": lambda: self.roles.get(v, v), "window": lambda: self.part(v), "part": lambda: self.where(v),
            "rule": lambda: self.sentence(self.rules.get(v, {})), "screenshots": lambda: str(len(v)), "shots": lambda: str(len(v)),
            "phases": lambda: " → ".join(v), "when": lambda: self.clause("when", v, {}),
            "cond": lambda: self.clause("cond", v, snap.get("when")), "then": lambda: self.clause("then", v, snap.get("when")),
            "items": lambda: "; ".join(map(self.item, v)), "props": lambda: "; ".join(self.prop(k, x) for k, x in v.items()),
            "stats": lambda: ", ".join(f"{s.get('label') or s.get('key')} {s.get('value', '')} {s.get('unit', '')}".strip() for s in v),
            "params": lambda: ", ".join(f"{slots.get(k, k)}: {plain(x)}" for k, x in v.items()),
        }
        return words[key]() if key in words else plain(v)
