"""search/keys/lecNN.json — "how a student would ask" per slide, written by agents → search/keys.json."""
from __future__ import annotations

import json
import re
from pathlib import Path

from corpus import SEARCH, texts

KEYS = SEARCH / "keys"
OUT = SEARCH / "keys.json"
SLIDE = re.compile(r"<!-- слайд (\d+) -->")


def layout(out: dict) -> str:
    """Compact JSON, a slide a line: small for the browser, readable in git diffs."""
    def line(value) -> str:
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))

    lectures = [f'{line(slug)}:{{\n' + ",\n".join(f"{line(s)}:{line(k)}" for s, k in slides.items()) + "}"
                for slug, slides in out.items() if slug != "v"]
    return "{" + ",\n".join(['"v":1', *lectures]) + "}\n"


def lecture(path: Path, slides: set[str]) -> tuple[dict[str, list[str]], list[str]]:
    """Slide → its keys, cleaned; and what is wrong with the file."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as e:
        return {}, [f"не JSON — {e}"]
    wrong = [] if data.get("lec") == int(path.stem[3:]) else [f"lec = {data.get('lec')!r}"]
    clean = {}
    for slide, keys in sorted((data.get("slides") or {}).items(), key=lambda kv: int(kv[0]) if kv[0].isdigit() else -1):
        if slide in slides and isinstance(keys, list) and all(isinstance(k, str) for k in keys):
            clean[slide] = list(dict.fromkeys(k.strip() for k in keys if k.strip()))
        else:
            wrong.append(f"слайд {slide!r} — нема в лекції або ключі не список рядків")
    return clean, wrong


def collect() -> int:
    sources = sorted(KEYS.glob("lec[0-9][0-9].json"))
    if not sources:
        print(f"нема {KEYS.relative_to(SEARCH.parent)}/lecNN.json — збирати нічого, keys.json не чіпаю")
        return 0
    docs, out, bad = texts(), {"v": 1}, 0
    for path in sources:
        slides = set(SLIDE.findall(docs.get(path.stem, "")))
        clean, wrong = lecture(path, slides)
        out[path.stem], bad = clean, bad + len(wrong)
        few = [f"{s}:{len(k)}" for s, k in clean.items() if not 3 <= len(k) <= 8]
        print(f"{path.stem}: слайдів з ключами {len(clean)} / {len(slides)}, ключів {sum(map(len, clean.values()))}"
              + (f" · не 3–8: {', '.join(few)}" if few else "") + "".join(f"\n  ✗ {w}" for w in wrong))
    OUT.write_text(layout(out), encoding="utf-8")
    errors = f" · помилок {bad}" if bad else ""
    print(f"→ {OUT.relative_to(SEARCH.parent)} · {OUT.stat().st_size // 1024} КБ{errors}")
    return 1 if bad else 0
