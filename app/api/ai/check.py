"""The checks of data/catalog/templates/validate.py, made against the base: a card, its place and its params; an answer's
word turned into the template's form. Each says the reason in words, "" when fine."""
from fastapi import HTTPException

from ai.context import Ctx
from claims_clean import clean_params
from zones import AUTO, AUTO_KINDS, HOMES, kind_of, misplaced

YES = {"true", "так", "yes", "1", "on"}


def args(items: list[dict]) -> dict[str, str]:
    """[{name, value}] → {name: value}, the empty ones left out."""
    return {str(a.get("name", "")).strip(): str(a.get("value", "")).strip() for a in items or [] if str(a.get("value", "")).strip()}


def params(task, values: dict[str, str]) -> dict:
    """The answer's strings → the slots' types, then the slots' own check (claims_clean)."""
    specs = {s["key"]: s for s in task.slots}
    out = {}
    for k, v in values.items():
        t = specs.get(k, {}).get("type", "text")  # a key it lacks: clean_params names it
        if t == "int":
            try:
                v = int(v)
            except ValueError:
                raise HTTPException(422, f"«{specs[k]['label']}» — число.")
        out[k] = v.lower() in YES if t == "bool" else v
    return clean_params(task, out, loose=True)


def card(ctx: Ctx, x: dict, where: str, field: bool) -> tuple[dict | None, str]:
    """A claim of the answer on `where` (a part's kind, "rule", or "game") → {slug, params?}, or None and why not.
    `field` — the game has a field or one is proposed: a card of kind field at the game's level lies on it."""
    slug = str(x.get("slug", "")).strip()
    task = ctx.cards.get(slug)
    if not task:
        return None, f"картки «{slug}» нема в каталозі"
    kind = kind_of(task)
    if where != "game":
        why = misplaced(kind, where)
    elif kind in AUTO_KINDS:
        why = AUTO
    elif kind == "field":
        why = "" if field else "Картка про поле, а поля в грі ще нема — спершу опиши поле."
    else:
        why = "" if kind in ("level", "game") else HOMES[kind][1]
    if why:
        return None, f"«{task.title}»: {why}"
    try:
        values = params(task, args(x.get("params")))
    except HTTPException as e:
        return None, f"«{task.title}»: {e.detail}"
    return {"slug": slug} | ({"params": values} if values else {}), ""


def word(dic: dict, x: dict) -> tuple[dict, str]:
    """{kind, args: [{name, value}], not} → the template's {kind, name: value, not: true}; an argument the word lacks is a
    reason (validate.py says so too — my_rules.clean_item would drop it silently)."""
    d, spec = {"kind": x.get("kind")}, dic.get(x.get("kind"))
    known = {a["name"] for a in spec["args"]} if spec else set()
    for k, v in args(x.get("args")).items():
        if spec and k not in known:
            return d, f"«{spec['label']}»: зайвий аргумент «{k}»"
        d[k] = v
    if x.get("not"):
        d["not"] = True
    return d, ""
