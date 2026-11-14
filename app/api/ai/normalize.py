"""The model's answer → proposals (AI-CONTRACT §2, §3): each thing in the form of a template's node, checked against the base
by the rules of templates/validate.py. What fails goes to «не розпізнано» with the reason; a bad card alone leaves its thing
standing; what the game has already is «exists». Entities, windows, levels — parts.py; rules — rules.py."""
from fastapi import HTTPException

from ai.check import card
from ai.context import Ctx
from ai.out import Out, quote, text
from ai.parts import entity, level, windows
from ai.rules import rule
from models.vocab import FIELD
from parts_clean import kind_fields
from zones import kind_of


def field(out: Out, x: dict) -> None:
    raw = {f["key"]: x.get(f["key"]) for f in FIELD if f["key"] != "layers"} | {"wrap": True if x.get("wrap") == "on" else None}
    try:
        props = kind_fields("field", {"props": raw}, out.ctx.cat)["props"]
    except HTTPException as e:
        return out.unknown(quote(x), f"Поле: {e.detail}")
    if props and out.ctx.field:
        out.add("field", props, quote(x), "поле вже є — зміни його у формі поля", state="exists")
    elif props:
        out.keys[("field", "")] = out.add("field", props, quote(x))


def claim(out: Out, x: dict, seen: set) -> None:
    """A card of the game at large; one of kind field lies on the field — the game's or the proposed one."""
    data, why = card(out.ctx, x, "game", bool(out.ctx.field) or ("field", "") in out.keys)
    if not data:
        return out.unknown(quote(x), why, [str(x.get("slug", ""))])
    if data["slug"] in seen:
        return
    seen.add(data["slug"])
    on_field = kind_of(out.ctx.cards[data["slug"]]) == "field"
    old = (data["slug"], out.ctx.field if on_field else "", "") in out.ctx.claimed
    out.add("claim", data, quote(x), needs=[("field", "")] if on_field else [], state="exists" if old else "open")


def items(answer: dict, ctx: Ctx) -> list[dict]:
    out = Out(ctx)
    field(out, answer.get("field") or {})
    taken = set()
    for x in answer.get("entities") or []:
        entity(out, x, taken)
    windows(out, answer.get("windows") or [])
    taken = set()
    for x in answer.get("levels") or []:
        level(out, x, taken)
    for x in answer.get("rules") or []:
        rule(out, x)
    seen = set()
    for x in answer.get("claims") or []:
        claim(out, x, seen)
    for x in answer.get("unknown") or []:
        if quote(x) or x.get("why"):
            out.unknown(quote(x), text(x, "why"), [str(c) for c in x.get("candidates") or []])
    return out.finish()
