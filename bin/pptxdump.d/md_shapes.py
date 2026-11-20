"""Shape dicts → layout.md lines: «- kind «name» · frame · …», the paragraphs of a text one indented under it."""
from md_text import paragraph_md, runs_md

GEOM_UA = {"rect": "прямокутник", "roundRect": "закруглений прямокутник", "ellipse": "еліпс", "line": "лінія",
           "rightArrow": "стрілка →", "leftArrow": "стрілка ←", "downArrow": "стрілка ↓", "upArrow": "стрілка ↑",
           "straightConnector1": "пряма", "bentConnector3": "ламана", "curvedConnector3": "крива", "custom": "довільна"}
FRAMES = {"chart": "діаграма (chart)", "smartart": "SmartArt"}


def media_md(m: dict | None) -> str:
    if m is None:
        return "—"
    if "missing" in m:
        return f"?{m['missing']}"
    if "url" in m:
        return f"зовнішнє посилання {m['url']}"
    s = f"`{m['file']}` ({m['ext']}" + (f", {m['px'][0]}×{m['px'][1]} px" if "px" in m else "") + ")"
    if t := " ".join(m.get("emfText", [])):
        s += f" · текст у EMF: «{t[:400]}{'…' if len(t) > 400 else ''}»"
    return s


def frame_md(f: dict | None) -> str:
    if f is None:
        return "рамка ?"
    s = f"рамка {f['x']:.1f}, {f['y']:.1f} · {f['w']:.1f}×{f['h']:.1f} %"
    s += f" · поворот {f['rot']:g}°" if "rot" in f else ""
    return s + (" · дзеркально ↔" if f.get("flipH") else "") + (" · дзеркально ↕" if f.get("flipV") else "")


def paint_md(s: dict) -> str:
    fill, out = s["fill"], []
    if fill:
        kind = fill["type"]
        out.append(f"заливка {fill['color']}" if kind == "solid" else f"заливка-картинка {media_md(fill['media'])}"
                   if kind == "picture" else f"заливка {'градієнт' if kind == 'gradient' else 'візерунок'}")
    if s["outline"]:
        out.append(f"контур {s['outline']}")
    return " · ".join(out)


def fallback_md(s: dict) -> str:
    fb = s.get("fallback")
    if not fb:
        return ""
    if all(m and "missing" in m for m in fb):
        return " · запасної картинки в pptx немає (звʼязок на NULL) — у знімку цей блок порожній"
    return f" · запасна картинка {', '.join(map(media_md, fb))} — її показує Quick Look"


def shape_md(s: dict, indent: str, lines: list[str]) -> None:
    k, d = s["kind"], s["descr"] or ""
    name = f"«{s['name']}»{' (прихована)' if s['hidden'] else ''}" if s["name"] is not None else ""
    head = f"{name} · {frame_md(s['frame'])}"
    descr = f" · опис «{d[:100]}{'…' if len(d) > 100 else ''}»" if d else ""
    if k == "group":
        lines.append(f"{indent}- група {head}{descr}")
        for c in s["children"]:
            shape_md(c, indent + "  ", lines)
    elif k == "picture":
        lines.append(f"{indent}- картинка {head} · {media_md(s['media'])}{' · обрізано' if s['crop'] else ''}{descr}{fallback_md(s)}")
    elif k == "line":
        g = GEOM_UA.get(s["geom"], s["geom"]) if s["geom"] else "лінія"
        lines.append(f"{indent}- {'лінія' if g == 'лінія' else f'лінія ({g})'} {head} · {paint_md(s)}".rstrip(" ·"))
    elif k == "ink":
        lines.append(f"{indent}- рукописне (ink) {head}")
    elif k == "table":
        lines.append(f"{indent}- таблиця {len(s['rows'])}×{s['cols']} {head}{descr}")
        for i, row in enumerate(s["rows"], 1):
            cells = ("⟵" if c["merge"] == "h" else "↑" if c["merge"] else (f"(×{c['span']}) " if c["span"] else "")
                     + " ⏎ ".join(runs_md(p) for p in c["paragraphs"]) for c in row)
            lines.append(f"{indent}  - р{i}: " + " | ".join(cells))
    elif k == "ole":
        lines.append(f"{indent}- OLE-обʼєкт {s['prog']} {head} · знімок-заміна {', '.join(map(media_md, s['previews'])) or '—'}{descr}")
    elif k in FRAMES or k == "frame":
        lines.append(f"{indent}- {FRAMES.get(k) or 'graphicFrame ' + s['uri']} {head}{descr}")
    else:
        kind = ("текст" if k == "text" else "фігура") + (f" ({GEOM_UA.get(s['geom'], s['geom'])})" if s["geom"] not in (None, "rect") else "")
        heads = [f"колір {s['color']}" if s["color"] else "", f"шрифт {s['size']:g}pt" if s["size"] is not None else ""]
        extra = " · ".join(x for x in [paint_md(s), " · ".join(h for h in heads if h)] if x)
        ph = f" (плейсхолдер {s['placeholder']})" if s["placeholder"] else ""
        lines.append(f"{indent}- {kind}{ph} {head}" + (f" · {extra}" if extra else "") + descr + fallback_md(s))
        lines.extend(f"{indent}  - {paragraph_md(p, s['color'], s['size'] is not None)}" for p in s["paragraphs"])
