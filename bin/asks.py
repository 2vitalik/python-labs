"""The requests for bin/catalog (T319): cards outside the core that students put in their games with a line why —
read them, open cards for everyone, answer one."""
import json
import sys

from siteapi import call, pull

STATUS = {"claimed": "заявлено", "accepted": "зараховано", "returned": "повернуто"}


def show(to: str, find: str, raw: bool):
    groups = [g for g in call(to, "GET", "/asks") if find in json.dumps(g, ensure_ascii=False).lower()]
    if raw:
        return print(json.dumps(groups, ensure_ascii=False, indent=1))
    for g in groups:
        t = g["task"]
        print(f"\n{t['icon'] or '·'} {t['title']} · {t['slug']} · {t['zone']}/{t['subzone']} · {t['coin'] or '—'} × {t['amount']}"
              f" — ігор {g['games']}, запитів {len(g['claims'])}")
        for r in g["claims"]:
            whose = f"{r['name']} ({r['nick']}{', тест' if r['test'] else ''}) · «{r['game']}»"
            place = f" · {r['where']}" if r["where"] else ""
            print(f"  {r['id']}  {STATUS[r['status']]:<10} {whose}{place}{' · сам опис' if r['auto'] else ''}")
            for mark, line in (("🙋", r["why"]), ("💬", r["verdict"])):
                if line:
                    print(f"      {mark} {line}")
    print(f"\nкарток {len(groups)} · запитів {sum(len(g['claims']) for g in groups)}")


def open_cards(to: str, slugs: list[str], text) -> bool:
    """`core: true` on the named cards — an edit of the card like any other: in its history, undone by `undo`. True — something opened."""
    site = {c["slug"]: c for c in call(to, "GET", "/tasks")}
    if bad := [s for s in slugs if s not in site]:
        sys.exit(f"нема таких карток: {', '.join(bad)}")
    done = False
    for slug in slugs:
        if site[slug].get("core"):
            print(f"tasks/{slug}: уже в основі")
            continue
        card = call(to, "PUT", f"/tasks/{site[slug]['id']}", site[slug] | {"core": True})
        pull(to, "tasks", card, text)
        print(f"tasks/{slug}: відкрито для всіх · {card['title']}")
        done = True
    return done


def reply(to: str, names: list[str], line: str | None, back: bool, card: str | None):
    if len(names) != 1:
        sys.exit("reply <id запиту> -m «…» [--return] [--to <slug>]")
    data = {k: v for k, v in (("verdict", line), ("status", "returned" if back else None), ("task", card)) if v is not None}
    if not data:
        sys.exit("reply: що зробити? -m «відповідь», --return чи --to <slug>")
    r = call(to, "PUT", f"/asks/{names[0]}", data)
    print(f"{r['id']}  {STATUS[r['status']]} · {r['task']} · {r['name']} · «{r['game']}»" + (f"\n  💬 {r['verdict']}" if r["verdict"] else ""))
