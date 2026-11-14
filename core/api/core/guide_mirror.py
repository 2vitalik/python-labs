"""A site's guide as a mirror of another site's (T291 §16): every page takes the other site's text, and that site's
history of edits is appended to ours — nothing is deleted. The dump is `bin/guide dump`; what the pages were and which
history rows came in goes to an undo file beside the dump.
Usage, in the site's folder: uv run python -m core.guide_mirror apply <dump.json> | undo <dump.undo.json>"""
import asyncio
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from beanie import PydanticObjectId

from core.db import init_db
from core.models.guide import Guide
from core.models.history import Change
from core.models.user import User

NOTE = "дзеркало з сервера: локальна версія була іншою"


def at(iso: str) -> datetime:
    return datetime.fromisoformat(iso).astimezone(timezone.utc).replace(tzinfo=None)  # Mongo's naive UTC


async def apply(path: Path):
    dump = json.loads(path.read_text())
    # the API names an author by the part before «@»: our user of that name gets the row, else an agent of that name
    who = {u.email.split("@")[0]: u.email for u in await User.find_all().to_list()}

    def email(name: str) -> str:
        return name if name in ("seed", "import") else who.get(name, f"{name}@agent")

    undo = {"pages": [], "created": [], "changes": []}
    for p in dump["pages"]:
        g = await Guide.find_one(Guide.slug == p["slug"])
        if g:
            undo["pages"].append({"slug": g.slug, "title": g.title, "body": g.body, "rev": g.rev,
                                  "updated_at": g.updated_at.isoformat(), "updated_by": g.updated_by})
        else:
            g = await Guide(slug=p["slug"], title=p["title"], body=p["body"]).insert()
            undo["created"].append(g.slug)
        edits = [e for e in dump["history"].get(p["slug"], []) if e["old"] is not None or e["old_title"] is not None]  # not the page's birth there
        have = {c.at.replace(microsecond=0) for c in await Change.find({"coll": "guide", "doc_id": g.id}).to_list()}
        rows = [Change(coll="guide", doc_id=g.id, actor=email(e["actor"]), at=at(e["at"]), note=e["note"], changes={
                    k: {"old": e[old], "new": e[new]} for k, old, new in (("body", "old", "new"), ("title", "old_title", "new_title"))
                    if e[new] is not None})
                for e in edits if at(e["at"]).replace(microsecond=0) not in have]
        known = {x for e in edits for x in (e["old"], e["new"])}
        if g.body != p["body"] and g.body not in known:  # a text the other site never had: one more row keeps it in the history
            rows.append(Change(coll="guide", doc_id=g.id, actor="mirror@agent", note=NOTE,
                               changes={"body": {"old": g.body, "new": p["body"]}}))
        for row in rows:
            undo["changes"].append(str((await row.insert()).id))
        g.title, g.body, g.rev = p["title"], p["body"], p["rev"]
        g.updated_at, g.updated_by = at(p["updated"]), email(p["updated_by"])
        await g.save()
        print(f"{g.slug:<16} rev {g.rev:<3} +{len(rows)} правок")
    out = path.with_suffix(".undo.json")
    out.write_text(json.dumps(undo, ensure_ascii=False, indent=1))
    print(f"відкат: uv run python -m core.guide_mirror undo {out}")


async def undo(path: Path):
    was = json.loads(path.read_text())
    for p in was["pages"]:
        g = await Guide.find_one(Guide.slug == p["slug"])
        g.title, g.body, g.rev, g.updated_by = p["title"], p["body"], p["rev"], p["updated_by"]
        g.updated_at = datetime.fromisoformat(p["updated_at"])
        await g.save()
    for slug in was["created"]:
        await Guide.find_one(Guide.slug == slug).delete()
    await Change.find({"_id": {"$in": [PydanticObjectId(i) for i in was["changes"]]}}).delete()
    print(f"повернуто {len(was['pages'])} сторінок, прибрано {len(was['created'])} нових і {len(was['changes'])} правок історії")


async def main():
    await init_db()
    await {"apply": apply, "undo": undo}[sys.argv[1]](Path(sys.argv[2]))


if __name__ == "__main__":
    asyncio.run(main())
