"""The JSON schema of the model's answer (AI-CONTRACT §1): closed objects, every field required, empty is "" / [], values of
arguments are strings. The words, entity types, window types and field options are enums from the vocab and the catalog;
a card's slug is a free string — 400+ values are too many for an enum, the server checks it (normalize.py)."""
from ai.source import Source
from models.vocab import CONDITIONS, EFFECTS, FIELD, LEVEL, TRIGGERS

S = {"type": "string"}


def obj(**props) -> dict:
    return {"type": "object", "properties": props, "required": list(props), "additionalProperties": False}


def arr(x: dict) -> dict:
    return {"type": "array", "items": x}


def enum(values) -> dict:
    return {"type": "string", "enum": list(values)}


def prop(spec: dict, src: Source) -> dict:
    """A field property: one choice may be "" (not said), several — a list; the bool is "" or "on"."""
    if spec["type"] == "choice":
        values = src.values(spec["key"])
        return arr(enum(values)) if spec.get("multi") else enum(["", *values])
    return enum(["", "on"]) if spec["type"] == "bool" else S


def build(src: Source) -> dict:
    arg = obj(name=S, value=S)
    claim = obj(slug=S, params=arr(arg))
    field = obj(**{f["key"]: prop(f, src) for f in FIELD if f["key"] != "layers"}, quote=S)
    entity = obj(title=S, role=enum(src.opts("role")), icon=S, description=S, stats=arr(obj(key=S, value=S, unit=S)),
                 states=arr(S), claims=arr(claim), quote=S)
    rule = obj(when=obj(kind=enum(TRIGGERS), args=arr(arg)),
               cond=arr(obj(kind=enum(CONDITIONS), **{"not": {"type": "boolean"}}, args=arr(arg))),
               then=arr(obj(kind=enum(EFFECTS), args=arr(arg))), note=S, claims=arr(claim), quote=S)
    window = obj(title=S, task=enum(t.slug for t in src.of("window")), description=S, claims=arr(claim),
                 items=arr(obj(title=S, window=S, task=S, note=S)), quote=S)
    level = obj(title=S, description=S, mode=enum(["", *LEVEL[0]["options"]]), count=S, size=S, claims=arr(claim), quote=S)
    return obj(field=field, entities=arr(entity), rules=arr(rule), windows=arr(window), levels=arr(level),
               claims=arr(obj(slug=S, params=arr(arg), quote=S)), unknown=arr(obj(quote=S, why=S, candidates=arr(S))))


def mismatch(v, s: dict, at: str = "$") -> list[str]:
    """Where `v` breaks the schema — the subset build() uses; for the smoke and ai.replay, no library needed."""
    if "enum" in s:
        return [] if v in s["enum"] else [f"{at}: {v!r} — не з переліку"]
    kind = s["type"]
    if kind in ("string", "boolean"):
        return [] if isinstance(v, {"string": str, "boolean": bool}[kind]) else [f"{at}: має бути {kind}"]
    if kind == "array":
        return [p for i, x in enumerate(v) for p in mismatch(x, s["items"], f"{at}[{i}]")] if isinstance(v, list) else [f"{at}: має бути список"]
    if not isinstance(v, dict):
        return [f"{at}: має бути обʼєкт"]
    out = [f"{at}: зайве поле «{k}»" for k in v if k not in s["properties"]]
    out += [f"{at}: нема поля «{k}»" for k in s["required"] if k not in v]
    return out + [p for k, x in v.items() if k in s["properties"] for p in mismatch(x, s["properties"][k], f"{at}.{k}")]
