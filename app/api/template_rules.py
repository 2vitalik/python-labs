"""The rules of a reference description (templates.py): entity and window titles become ids, the words are checked
like the student's own (my_rules.clean), a sentence the game already has is not added twice."""
from fastapi import HTTPException

from core.models.history import record_new
from core.models.user import User
from models.game import Game, Part
from models.rule import Rule
from models.vocab import CONDITIONS, EFFECTS, TRIGGERS
from routes.my_rules import RuleIn, clean


def sentence_key(when, cond, then) -> str:
    return repr((when, cond, then))


async def pour_rules(game: Game, user: User, rules: list[dict], by_title: dict[tuple, Part], added: dict,
                     skipped: list[str]) -> list[tuple[Rule, list]]:
    """Each rule of the template that stands in the game now — new or found — with the claims written on it."""
    names = {k[1]: str(p.id) for k, p in by_title.items() if k[0] in ("entity", "window")}
    existing = {sentence_key(r.when, r.cond, r.then): r for r in await Rule.find(Rule.game == game.id).to_list()}

    def resolve(dic, d):  # titles → ids, only where the word expects an entity or a window
        spec = dic.get(d.get("kind")) or {"args": []}
        refs = {a["name"] for a in spec["args"] if a["type"] in ("entity", "window")}
        return {k: (names.get(str(v).lower(), v) if k in refs and isinstance(v, str) else v) for k, v in d.items()}

    out = []
    for r in rules:
        data = RuleIn(when=resolve(TRIGGERS, r.get("when") or {}), cond=[resolve(CONDITIONS, c) for c in r.get("cond") or []],
                      then=[resolve(EFFECTS, e) for e in r.get("then") or []], note=r.get("note", ""))
        try:
            d = await clean(data, game)
        except HTTPException as e:
            skipped.append(f"правило: {e.detail}")
            continue
        key = sentence_key(d["when"], d["cond"], d["then"])
        if not (rule := existing.get(key)):
            rule = Rule(game=game.id, **d)
            await rule.insert()
            await record_new(rule, actor=user.email)
            existing[key] = rule
            added["rules"] += 1
        out.append((rule, r.get("claims") or []))
    return out
