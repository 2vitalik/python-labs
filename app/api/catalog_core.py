"""The catalog's core (T319, T320) as data/catalog/core.yaml: zone → subzone → [slug, …] in catalog order — the cards a student
claims at once; the other active ones are «за запитом». Family headings are never written. catalog_io.py reads and writes it;
`catalog_io.py core` puts only it onto the cards in Mongo — for the server, where the full import must not run."""
import sys
from pathlib import Path

import yaml

from core.models.history import record
from models.task import Task
from zones import ZONES

CORE_HEAD = (
    "# Основа каталогу (T319, T320): картки, які студент заявляє одразу. Решта активних карток — «за запитом»: їх видно,\n"
    "# ними можна описати гру, але монетка зарахується, коли викладач відкриє картку (перенесе її сюди).\n"
    "# Категорія → підкатегорія → картки в порядку каталогу; сімʼя в основі, коли в основі хоч одна її картка.\n"
    "# import ставить `core` за цим файлом (картки, якої тут нема, — «за запитом»); без файла `core` не чіпає.\n")


def render(tasks: list[Task]) -> str:
    """`tasks` in catalog order (zone, subzone, order, slug); a subzone's slugs on one line."""
    heads = {t.parent for t in tasks if t.parent}
    found = {}
    for t in tasks:
        if t.core and t.status != "archived" and t.slug not in heads:
            found.setdefault((t.zone, t.subzone), []).append(t.slug)
    tree = {z: {s: found[z, s] for s in ZONES[z]["subzones"] if (z, s) in found} for z in ZONES}
    tree = {z: subs for z, subs in tree.items() if subs}
    text = yaml.dump(tree, allow_unicode=True, sort_keys=False, default_flow_style=None, width=10**6) if tree else ""
    return CORE_HEAD + text


def slugs(path: Path) -> set[str] | None:
    """The cards the file names; None — no file."""
    if not path.is_file():
        return None
    tree = yaml.safe_load(path.read_text()) or {}
    return {s for subs in tree.values() for items in (subs or {}).values() for s in items or []}


def unknown(named: set[str], known: set[str]) -> None:
    if bad := named - known:
        sys.exit(f"core.yaml: нема таких карток — {', '.join(sorted(bad))}")


async def apply(path: Path) -> None:
    """`core` of every card by the file, nothing else; each change in history as the import's."""
    named = slugs(path)
    if named is None:
        sys.exit(f"нема {path}")
    tasks = await Task.find_all().sort("zone", "subzone", "order", "slug").to_list()
    unknown(named, {t.slug for t in tasks})
    n = 0
    for t in tasks:
        if await record(t, {"core": t.slug in named}, actor="import"):
            n += 1
            print(f"{'в основі' if t.core else 'за запитом'}: {t.slug} · {t.title}")
    print(f"tasks: основа {sum(t.core for t in tasks)} · змінено {n}")
