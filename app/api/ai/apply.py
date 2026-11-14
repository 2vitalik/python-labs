"""The student's click on proposals (AI-CONTRACT §4): they and what they need become a piece of a template, templates.pour()
puts it into the game; each proposal that is there now is «added», with the place it went to for jump()."""
from fastapi import HTTPException

import templates
from core.models.user import User
from models.draft import Draft
from models.game import Claim, Game, Part
from models.rule import Rule
from models.task import Task
from models.vocab import CONDITIONS, EFFECTS, TRIGGERS
from routes.my_rules import RuleIn, clean
from template_rules import sentence_key
from zones import kind_of

SECTION = {"entity": "entities", "window": "windows", "level": "levels", "rule": "rules", "claim": "claims"}


def chosen(draft: Draft, keys: list[str]) -> list[dict]:
    """The open ones named, and every proposal they need — a rejected one too: the rule cannot stand without it."""
    by_key = {it["key"]: it for it in draft.items}
    todo = [k for k in keys if by_key.get(k, {}).get("state") == "open"]
    picked = set()
    while todo:
        it = by_key.get(todo.pop())
        if it and it["key"] not in picked and it["group"] != "unknown" and it["state"] in ("open", "rejected"):
            picked.add(it["key"])
            todo += it["needs"]
    return [it for it in draft.items if it["key"] in picked]


def piece(items: list[dict]) -> dict:
    out = {}
    for it in items:
        if it["group"] == "field":
            out["field"] = it["data"]
        else:
            out.setdefault(SECTION[it["group"]], []).append(it["data"])
    return out


async def places(game: Game, items: list[dict]) -> dict[str, str]:
    """key → "p-<id>" | "r-<id>" | "c-<id>": where each proposal is in the game now; one not found is not there."""
    parts = await Part.find(Part.game == game.id).to_list()
    by_title = {(p.kind, p.title.lower()): p for p in parts}
    field = next((p for p in parts if p.kind == "field"), None)
    names = {k[1]: str(p.id) for k, p in by_title.items() if k[0] in ("entity", "window")}
    rules = {sentence_key(r.when, r.cond, r.then): r for r in await Rule.find(Rule.game == game.id).to_list()}

    def resolve(dic, d):  # titles → ids, as template_rules does
        refs = {a["name"] for a in (dic.get(d.get("kind")) or {"args": []})["args"] if a["type"] in ("entity", "window")}
        return {k: names.get(str(v).lower(), v) if k in refs and isinstance(v, str) else v for k, v in d.items()}

    out = {}
    for it in items:
        g, d = it["group"], it["data"]
        if g == "field" and field:
            out[it["key"]] = f"p-{field.id}"
        elif g in ("entity", "window", "level") and (p := by_title.get((g, d["title"].lower()))):
            out[it["key"]] = f"p-{p.id}"
        elif g == "rule":
            try:
                c = await clean(RuleIn(when=resolve(TRIGGERS, d["when"]), cond=[resolve(CONDITIONS, x) for x in d.get("cond", [])],
                                       then=[resolve(EFFECTS, x) for x in d["then"]]), game)
            except HTTPException:
                continue
            if r := rules.get(sentence_key(c["when"], c["cond"], c["then"])):
                out[it["key"]] = f"r-{r.id}"
        elif g == "claim":
            task = await Task.find_one(Task.slug == d["slug"])
            part = str(field.id) if field and task and kind_of(task) == "field" else ""
            if c := await Claim.find_one(Claim.game == game.id, Claim.task == d["slug"], Claim.part == part, Claim.rule == ""):
                out[it["key"]] = f"c-{c.id}"
    return out


async def apply(draft: Draft, game: Game, user: User, keys: list[str]) -> dict:
    items = chosen(draft, keys)
    res = await templates.pour(game, user, piece(items))
    made = await places(game, items)
    for it in items:
        if it["key"] in made:
            it["state"], it["made"] = "added", made[it["key"]]
    await draft.save()
    return {"draft": draft.api(), "added": res["added"], "skipped": res["skipped"]}
