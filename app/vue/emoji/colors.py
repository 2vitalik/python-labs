"""The colours of every emoji, as this Mac draws them → colors.json, which build.mjs puts into the picker's data (T309).

    uv run --no-project --with pillow python app/vue/emoji/colors.py     (after build.mjs: it reads src/emoji/data.json)

Chrome draws all of them on one sheet twice — black on black and white on white: what is the same on both is the emoji's
own paint. A colour is kept when it covers a fifth of that paint, three at most, the largest first. The letters:
r o y g b p k n d s w — red, orange, yellow, green, blue, purple, pink, brown, dark, silver (grey), white."""
import colorsys
import json
import subprocess
import tempfile
import time
from collections import Counter
from pathlib import Path

from PIL import Image

HERE = Path(__file__).parent
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
COLS, CELL = 40, 48
SHARE, MOST = 0.2, 3


def bucket(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    h *= 360
    if v < 0.24:
        return 'd'
    if s < 0.16:
        return 'w' if v > 0.8 else 's' if v > 0.42 else 'd'
    if (h < 48 or h >= 345) and v < 0.66 and s > 0.3:
        return 'n'
    if h < 14 or h >= 345:
        return 'k' if s < 0.5 and v > 0.8 else 'r'
    if h < 40:
        return 'n' if s < 0.5 and v < 0.85 else 'o'
    if h < 68:
        return 'y'
    if h < 165:
        return 'g'
    if h < 258:
        return 'b'
    if h < 292:
        return 'p'
    return 'k' if v > 0.8 and (h >= 315 or s < 0.55) else 'p'


def shot(sheet, ink, out, size):
    with tempfile.TemporaryDirectory() as profile:
        chrome = subprocess.Popen([CHROME, '--headless=new', f'--user-data-dir={profile}', f'--screenshot={out}', '--hide-scrollbars',
                                   '--force-device-scale-factor=1', f'--window-size={size[0]},{size[1]}', f'file://{sheet}?{ink}'],
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(120):  # the headless Chrome does not always leave by itself
            time.sleep(0.5)
            if out.exists() and out.stat().st_size and chrome.poll() is not None:
                break
        chrome.kill()
    return Image.open(out).convert('RGB')


def colours(dark, light, x, y):
    seen = Counter()
    for i in range(x, x + CELL):
        for j in range(y, y + CELL):
            a, b = dark.getpixel((i, j)), light.getpixel((i, j))
            if max(abs(p - q) for p, q in zip(a, b)) < 40:  # the same on both grounds: opaque
                seen[bucket(*a)] += 1
    total = sum(seen.values())
    return ''.join(c for c, n in seen.most_common(MOST) if n >= total * SHARE) if total > 40 else ''


def main():
    chars = [i[0] for i in json.loads((HERE / '../src/emoji/data.json').read_text())['items'] if i[7]]
    cells = ''.join(f'<i>{c}</i>' for c in chars)
    size = (COLS * CELL, (len(chars) // COLS + 1) * CELL)
    with tempfile.TemporaryDirectory() as tmp:
        sheet = Path(tmp) / 'sheet.html'
        sheet.write_text(f'''<!doctype html><meta charset="utf-8"><style>
            html {{ background: #000; color: #000 }} html.fff {{ background: #fff; color: #fff }}
            body {{ margin: 0; width: {size[0]}px; display: flex; flex-wrap: wrap; font: 36px/{CELL}px "Apple Color Emoji" }}
            i {{ width: {CELL}px; height: {CELL}px; overflow: hidden; text-align: center; font-style: normal }}
            </style><script>document.documentElement.className = location.search.slice(1)</script>{cells}''')
        dark, light = (shot(sheet, ink, Path(tmp) / f'{ink}.png', size) for ink in ('000', 'fff'))
    out = {c: colours(dark, light, n % COLS * CELL, n // COLS * CELL) for n, c in enumerate(chars)}
    blank = [c for c, v in out.items() if not v]
    (HERE / 'colors.json').write_text(json.dumps({c: v for c, v in out.items() if v}, ensure_ascii=False, indent=0) + '\n')
    print(f'{len(out) - len(blank)} of {len(out)} coloured; not drawn here: {" ".join(blank)}')


main()
