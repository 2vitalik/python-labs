"""Course guide pages: data/guide/<slug>.md → {title, brief, body}. Files in git are the truth for now;
an on-site editor may replace them later behind the same contract (T115 §4)."""
import re
from datetime import date
from pathlib import Path

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/guide")
ROOT = Path(__file__).resolve().parents[3] / "data" / "guide"
MORE = "<!-- more -->"  # above it — the brief for the home page, below — the rest of the page
_cache: dict[str, tuple[float, dict]] = {}


def load(slug: str) -> dict | None:
    path = ROOT / f"{slug}.md"
    if not re.fullmatch(r"[a-z0-9-]+", slug) or not path.is_file():
        return None
    mtime = path.stat().st_mtime
    if slug not in _cache or _cache[slug][0] != mtime:
        title, _, rest = path.read_text().partition("\n")
        brief, _, body = rest.partition(MORE)
        page = {"slug": slug, "title": title.lstrip("# ").strip(), "brief": brief.strip(), "body": body.strip(),
                "updated": date.fromtimestamp(mtime).isoformat()}
        _cache[slug] = (mtime, page)
    return _cache[slug][1]


@router.get("")
async def list_pages():
    pages = (load(p.stem) for p in sorted(ROOT.glob("*.md")) if p.stem.islower())  # README is not a page
    return [{k: v for k, v in page.items() if k != "body"} for page in pages if page]


@router.get("/{slug}")
async def get_page(slug: str):
    page = load(slug)
    if not page:
        raise HTTPException(404)
    return page
