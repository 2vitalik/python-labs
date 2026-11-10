"""The description's choices that are catalog cards (T270 §6): entity roles, stats and the field's options — cards of kinds
role · stat · fieldopt keyed by their `opt`. The forms get them through /api/vocab, the routes check against the same."""
from core.models.user import Status, User
from models.task import Task
from models.vocab import FIELD
from zones import kind_of

OPT_KINDS = ("role", "stat", "fieldopt")


def is_admin(user: User | None) -> bool:
    return bool(user and user.status == Status.admin)


async def catalog(admin: bool) -> dict[str, dict[str, Task]]:
    """{kind: {opt: card}}: active cards, everything but the archive for an admin."""
    statuses = ["active", "draft"] if admin else ["active"]
    out = {k: {} for k in OPT_KINDS}
    for t in await Task.find({"opt": {"$gt": ""}, "status": {"$in": statuses}}).sort("zone", "subzone", "order").to_list():
        if (kind := kind_of(t)) in out:
            out[kind].setdefault(t.opt, t)
    return out


def card(t: Task) -> dict:
    return {"label": t.title, "icon": t.icon, "desc": t.description, "slug": t.slug, "coin": t.coin}


def unit(t: Task) -> str:
    return t.slots[0].get("unit", "") if t.slots else ""


async def described(cat: dict) -> dict:
    """The roles grouped by their family card, the stats with units, the field's properties with their options."""
    roles = cat["role"].values()
    families = {f.slug: f for f in await Task.find({"slug": {"$in": [t.parent for t in roles if t.parent]}}).to_list()}
    rank = lambda t: (families[t.parent].order if t.parent in families else t.order, t.order)  # noqa: E731
    field = [spec | {"options": {o.split(":", 1)[1]: card(t) for o, t in cat["fieldopt"].items() if o.startswith(spec["key"] + ":")}}
             for spec in FIELD]
    return {
        "roles": {t.opt: card(t) | {"group": families[t.parent].title if t.parent in families else "", "amount": t.amount}
                  for t in sorted(roles, key=rank)},
        "stats": [{"key": t.opt, "label": t.title, "icon": t.icon, "unit": unit(t), "desc": t.description, "slug": t.slug, "coin": t.coin}
                  for t in cat["stat"].values()],
        "field": field,
    }
