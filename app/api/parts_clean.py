"""What a student writes about a part, cleaned: checked against the vocab and the catalog's role, stat and field-option
cards (`cat` — options.catalog()). Shared by the parts' routes, the templates and the demo seed."""
from fastapi import HTTPException

from models.vocab import FIELD, LEVEL
from options import unit

LEVEL_PROPS = LEVEL + [f for f in FIELD if f["key"] not in {x["key"] for x in LEVEL}]  # a level overrides the field's


def check_role(role: str, cat: dict) -> None:
    if role not in cat["role"]:
        raise HTTPException(422, "Тип сутності — зі списку типів.")


def clean_icon(icon: str) -> str:
    icon = str(icon or "").strip()
    if len(icon) > 16:
        raise HTTPException(422, "Іконка — один-два емодзі.")
    return icon


def choices(spec: dict, cat: dict) -> set[str]:
    key = spec["key"] + ":"
    return set(spec.get("options") or {o[len(key):] for o in cat["fieldopt"] if o.startswith(key)})


def clean_props(props: dict, specs: list[dict], cat: dict) -> dict:
    """Properties by their specs: unknown keys dropped, choices from the list (`multi` ones as lists), empty values left out."""
    out = {}
    for spec in specs:
        v = props.get(spec["key"])
        if v is None or v == "" or v == []:
            continue
        if spec["type"] == "bool":
            v = bool(v)
        elif spec["type"] == "choice":
            v = list(dict.fromkeys(str(x) for x in (v if isinstance(v, list) else [v]) if x not in (None, "", "none")))  # none — the old «нема»
            if bad := [x for x in v if x not in choices(spec, cat)]:
                raise HTTPException(422, f"«{spec['label']}»: «{bad[0]}» — не зі списку.")
            if len(v) > 1 and not spec.get("multi"):
                raise HTTPException(422, f"«{spec['label']}» — одне значення.")
            if not v:
                continue
            v = v if spec.get("multi") else v[0]
        elif spec["type"] == "tags":
            v = [str(x).strip() for x in (v if isinstance(v, list) else str(v).split(",")) if str(x).strip()]
            if not v:
                continue
        else:
            v = str(v).strip()
            if not v:
                continue
        out[spec["key"]] = v
    return out


def clean_stats(stats: list[dict], cat: dict | None, whose: str = "в цієї сутності") -> list[dict]:
    """Stats: a catalog stat takes its card's label, and its unit when the card has one (a price is «сонць» or «золота» —
    the student's); an own word keeps the student's label and unit; `cat` None — free rows (a level's).
    The same stat twice — by key or by label — is a mistake, not a silent merge."""
    known = cat["stat"] if cat else {}
    out, taken = [], set()
    for s in stats:
        key = str(s.get("key") or "").strip()
        if not key:
            continue
        value = str(s.get("value") if s.get("value") is not None else "").strip()
        card = known.get(key)
        label = card.title if card else str(s.get("label") or "").strip() or key
        names = {key.lower(), label.lower()}
        if names & taken:
            raise HTTPException(422, f"Параметр «{label}» уже є {whose}.")
        if not value:
            raise HTTPException(422, f"Параметр «{label}» — без значення.")
        own = str(s.get("unit") or "").strip()
        out.append({"key": key, "label": label, "value": value, "unit": (unit(card) if card else "") or own})
        taken |= names
    return out


def clean_states(states: list[str]) -> list[str]:
    out = []
    for s in states:
        s = " ".join(str(s).split())
        if s and s.lower() not in {x.lower() for x in out}:
            out.append(s)
    if len(out) > 12:
        raise HTTPException(422, "Станів забагато — до 12.")
    return out


def kind_fields(kind: str, d: dict, cat: dict) -> dict:
    """The fields of a part that depend on its kind; `d` — what came in."""
    if kind == "entity":
        check_role(d.get("role") or "", cat)
        return {"role": d["role"], "icon": clean_icon(d.get("icon")), "stats": clean_stats(d.get("stats") or [], cat),
                "states": clean_states(d.get("states") or [])}
    if kind == "field":
        return {"props": clean_props(d.get("props") or {}, FIELD, cat)}
    if kind == "level":
        props = clean_props(d.get("props") or {}, LEVEL_PROPS, cat)
        if drawn := clean_map((d.get("props") or {}).get("map")):
            props["map"] = drawn
        return {"props": props, "stats": clean_stats(d.get("stats") or [], None, "на цьому рівні")}
    return {}


def clean_map(text) -> str:
    """A level drawn in cells (T276): the lines of one ```field — emoji through spaces; "" — none."""
    text = "\n".join(line.rstrip() for line in str(text or "").replace("\r", "").split("\n")).strip("\n")
    if len(text) > 4000:
        raise HTTPException(422, "Мапа рівня завелика — до 4 000 знаків.")
    return text if text.strip() else ""
