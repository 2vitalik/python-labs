"""Guide snapshot: Mongo ↔ data/guide/*.md. Truth lives in Mongo; files are the seed (slugs missing at startup)
and a git-diffable export. Usage: uv run python guide_io.py export|import"""
import asyncio
import re
import sys
from pathlib import Path

from db import init_db
from models.guide import DRAFT, Guide, save
from models.history import record_new

ROOT = Path(__file__).resolve().parents[2] / "data" / "guide"


def files() -> dict[str, tuple[str, str]]:  # slug → (title, body); README is not a page
    pages = {}
    for path in sorted(ROOT.glob("*.md")):
        if re.fullmatch(r"[a-z0-9-]+", path.stem):
            title, _, body = path.read_text().partition("\n")
            pages[path.stem] = (title.lstrip("# ").strip(), body.strip())
    return pages


async def seed() -> int:
    """Insert the pages Mongo does not have yet (first run, new files)."""
    have = {g.slug for g in await Guide.find_all().to_list()}
    new = [Guide(slug=s, title=t, body=b, updated_by="seed") for s, (t, b) in files().items() if s not in have]
    for g in new:
        await g.insert()
        await record_new(g, actor="seed")
    return len(new)


async def import_():
    added = await seed()
    updated = 0
    for slug, (title, body) in files().items():
        updated += await save(await Guide.find_one(Guide.slug == slug), title, body, actor="import")
    print(f"guide: додано {added} · оновлено {updated}")


async def export():
    ROOT.mkdir(parents=True, exist_ok=True)
    pages = await Guide.find(Guide.slug != DRAFT).to_list()
    for g in pages:
        (ROOT / f"{g.slug}.md").write_text(f"# {g.title}\n\n{g.body}\n")
    print(f"guide: {len(pages)} сторінок → {ROOT}")


async def main():
    await init_db()
    await {"export": export, "import": import_}[sys.argv[1]]()


if __name__ == "__main__":
    asyncio.run(main())
