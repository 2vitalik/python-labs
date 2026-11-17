"""A catalog card as the teacher (or an agent) writes it: checked against the zones, the coins, the kinds,
the slot specs, the vocab's words of a rule blank; aliases by language (T270 §13)."""
from fastapi import HTTPException
from pydantic import BaseModel

from models.task import PROOFS, Task, langs
from models.vocab import CONDITIONS, EFFECTS, TRIGGERS
from pricing import clean_tiers
from zones import COINS, KINDS, STATUSES, ZONES, default_kind

SLOT_TYPES = ("int", "text", "bool", "choice")


class TaskIn(BaseModel):
    slug: str
    title: str
    description: str = ""
    zone: str
    subzone: str
    kind: str | None = None  # None = leave as is (as do the other fields of T270 below)
    icon: str | None = None
    opt: str | None = None
    tags: list[str] = []
    games: list[str] = []
    coin: str = ""
    amount: float = 1
    max_count: int = 1
    tiers: list | None = None  # price steps [[upto, factor], …] (T291 §13)
    parent: str = ""
    slots: list[dict] | None = None
    rule: dict | None = None
    aliases: list[str] | dict = []  # a plain list is Ukrainian
    proof: str | None = None
    status: str = "draft"
    core: bool | None = None  # in the core (T319); None — as it is: the card forms before it do not send it
    order: int = 0


def clean_slots(slots: list[dict]) -> list[dict]:
    """Claim param specs: {key, label, type, options (a choice's), unit?, required?}."""
    out = []
    for s in slots:
        key, label, kind = (str(s.get(k) or "").strip() for k in ("key", "label", "type"))
        if not key or not label or kind not in SLOT_TYPES or key in {x["key"] for x in out}:
            raise HTTPException(422, f"Параметр «{key or label}»: потрібні ключ (свій для кожного), підпис і тип {' / '.join(SLOT_TYPES)}.")
        spec = {"key": key, "label": label, "type": kind}
        if kind == "choice":
            if not (options := [str(o).strip() for o in s.get("options") or [] if str(o).strip()]):
                raise HTTPException(422, f"Параметр «{label}»: варіанти — хоч один.")
            spec["options"] = options
        if unit := str(s.get("unit") or "").strip():
            spec["unit"] = unit
        if s.get("required"):
            spec["required"] = True
        out.append(spec)
    return out


def clean_rule(rule: dict) -> dict:
    """A rule-card's blank: words from the dictionaries, their args as written (the student fills the rest)."""
    if set(rule) - {"when", "cond", "then"}:
        raise HTTPException(422, "Заготовка правила — when, cond, then.")
    items = [(TRIGGERS, rule["when"])] if rule.get("when") else []
    items += [(CONDITIONS, c) for c in rule.get("cond") or []] + [(EFFECTS, e) for e in rule.get("then") or []]
    for dic, item in items:
        if not isinstance(item, dict) or item.get("kind") not in dic:
            raise HTTPException(422, f"Заготовка правила: невідоме слово «{item.get('kind') if isinstance(item, dict) else item}».")
    return {k: v for k, v in rule.items() if v}


async def clean(data: TaskIn, was: Task | None = None) -> dict:
    """The card's fields as stored; `was` — the card being edited, whose price steps stay when none are sent."""
    d = data.model_dump(exclude_none=True)
    d["slug"], d["title"] = d["slug"].strip().lower(), d["title"].strip()
    d["aliases"] = {k: list(dict.fromkeys(" ".join(a.split()) for a in v if a.strip())) for k, v in langs(d["aliases"]).items()}
    if not d["slug"] or not d["title"]:
        raise HTTPException(422, "Slug і назва — обовʼязкові.")
    if d["zone"] not in ZONES or d["subzone"] not in ZONES[d["zone"]]["subzones"]:
        raise HTTPException(422, "Невідома зона або підзона.")
    if d["coin"] and d["coin"] not in COINS:
        raise HTTPException(422, "Невідомий тип монетки.")
    if d["status"] not in STATUSES:
        raise HTTPException(422, "Невідомий статус.")
    if "kind" in d:
        if d["kind"] and d["kind"] not in KINDS:
            raise HTTPException(422, "Невідомий тип картки.")
        if d["kind"] == default_kind(d["zone"], d["subzone"], d["tags"]):
            d["kind"] = ""  # the subzone's own: kept implicit, so a card follows its subzone
    for k in ("icon", "opt", "proof"):
        if k in d:
            d[k] = d[k].strip()
    if d.get("proof") and d["proof"] not in PROOFS:
        raise HTTPException(422, "Доказ — shot (скриншот), gif (гіфка), video (відео), code (посилання на код) або нічого.")
    if "slots" in d:
        d["slots"] = clean_slots(d["slots"])
    if "rule" in d:
        d["rule"] = clean_rule(d["rule"])
    if "tiers" in d:
        try:
            d["tiers"] = clean_tiers(d["tiers"])
        except ValueError as e:
            raise HTTPException(422, str(e))
    if tiers := d.get("tiers", was.tiers if was else []):
        d["max_count"] = tiers[-1][0]  # the last step says the cap
    if d["parent"]:
        parent = await Task.find_one(Task.slug == d["parent"])
        if not parent or parent.slug == d["slug"] or parent.parent:
            raise HTTPException(422, "Батько має існувати і сам бути кореневим завданням.")
    return d
