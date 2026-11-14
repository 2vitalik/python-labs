"""A rule of the answer → a proposal (T289 §4): its words checked like the student's own (my_rules.clean_item), the names
pointing at the game's entities and windows or at the proposals; an entity only mentioned gets a proposal of its own."""
from fastapi import HTTPException

from ai.check import word
from ai.out import Out, quote
from models.vocab import CONDITIONS, EFFECTS, SIDES, TRIGGERS
from routes.my_rules import clean_item
from template_rules import sentence_key

MENTIONED = "у тексті лише згадана"


def refs(out: Out, dic: dict, d: dict, missing: dict) -> str:
    """Names → tokens in place; an entity nobody has goes to `missing`. The reason in words when a name cannot be."""
    for a in (dic.get(d["kind"]) or {"args": []})["args"]:
        v = d.get(a["name"])
        if a["type"] not in ("entity", "window") or not v or v in SIDES:
            continue
        ref = (a["type"], v.lower())
        if ref in out.failed:
            return f"«{v}» не розпізнано вище"
        if ref in out.names:
            d[a["name"]] = out.names[ref][0]
        elif a["type"] == "entity":
            d[a["name"]] = missing.setdefault(ref, (f"new:entity:{v.lower()}", v))[0]
        else:
            return f"вікна «{v}» нема ні в грі, ні серед пропозицій"
    return ""


def clean(out: Out, when: dict, cond: list, then: list, missing: dict) -> tuple:
    """my_rules.clean() over the tokens instead of the game's ids."""
    ids = {kind: {tok for (k, _), (tok, _) in [*out.names.items(), *missing.items()] if k == kind} for kind in ("entity", "window")}
    when = clean_item(TRIGGERS, when, ids, {"*"}, "КОЛИ")
    sides = {"*"} | {s for s in ("@a", "@b") if s[1:] in when} | ({"@both"} if "a" in when and "b" in when else set())
    cond = [clean_item(CONDITIONS, c, ids, sides, "ЯКЩО") for c in cond]
    then = [clean_item(EFFECTS, e, ids, sides, "ТО") for e in then]
    if not then:
        raise HTTPException(422, "Хоч один ефект ТО.")
    return when, cond, then


def rule(out: Out, x: dict) -> None:
    q, missing = quote(x), {}
    when, why = word(TRIGGERS, x.get("when") or {})
    cond = [word(CONDITIONS, c) for c in x.get("cond") or []]
    then = [word(EFFECTS, e) for e in x.get("then") or []]
    why = why or next((w for _, w in cond + then if w), "")
    cond, then = [d for d, _ in cond], [d for d, _ in then]
    why = why or refs(out, TRIGGERS, when, missing) or next((w for dic, ds in ((CONDITIONS, cond), (EFFECTS, then))
                                                              for d in ds if (w := refs(out, dic, d, missing))), "")
    if why:
        return out.unknown(q, f"Правило: {why}")
    try:
        when, cond, then = clean(out, when, cond, then, missing)
    except HTTPException as e:
        return out.unknown(q, f"Правило: {e.detail}")
    for _, name in missing.values():  # T289 §4: mentioned, not described
        out.keys[out.name("entity", name)] = out.add("entity", {"title": name, "role": "object"}, q, MENTIONED)
    titles = {tok: t for tok, t in out.names.values()}
    used = {v for it in [when, *cond, *then] for v in it.values() if isinstance(v, str)}
    back = lambda d: {k: titles.get(v, v) if isinstance(v, str) else v for k, v in d.items()}  # noqa: E731
    data = {"when": back(when)} | ({"cond": [back(c) for c in cond]} if cond else {}) | {"then": [back(e) for e in then]}
    if note := " ".join(str(x.get("note", "")).split()):
        data["note"] = note
    rid = out.ctx.rules.get(sentence_key(when, cond, then))  # names of proposals never match: a new rule
    claims, old = out.claims(x, "rule", "Правило", ("", rid) if rid else None)
    if claims:
        data["claims"] = claims
    needs = [ref for ref, (tok, _) in out.names.items() if tok in used]
    out.add("rule", data, q, "правило вже є — додадуться лише картки" if rid and not old else "", needs,
            "exists" if rid and old else "open")
