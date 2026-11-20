"""The deck dict → layout.md: a header with the notation, the template, then «## слайд K» per slide."""
from md_shapes import media_md, shape_md

NOTATION = (
    "Нотація. Рамка — `left, top · width×height` у відсотках ширини/висоти слайда (для фігур у групі — вже перераховано в координати слайда). "
    "Абзац — `[L<рівень> центр|право]`, далі маркер, якщо заданий явно. Виділення: `**жирний**`, `*курсив*`, `[підкр]…[/]`, "
    "`[колір #RRGGBB]…[/]` (`≈` — колір теми з модифікатором яскравості, `(тема accent1)` — колір зі схеми теми), `[18pt]…[/]` — розмір, "
    "`^{…}` / `_{…}` — верхній / нижній індекс, `[шрифт Symbol]…[/]` — символьний шрифт, ` ⏎ ` — розрив рядка. "
    "Колір / розмір, однаковий для всієї фігури, винесено в її рядок. Показано лише задане на самому слайді: успадковане від макета / майстра "
    "(кольори й розміри плейсхолдерів, маркери списків) не видно. `[формула: …]` — OMML-формула в лінійному записі "
    "(колір — як у тексту: `[колір #…][формула: …][/]`, а в різнобарвній — на частинах усередині запису); "
    "в Quick Look-знімку на її місці — «запасна картинка» (Fallback) того самого блока. "
    "`текст у EMF` — рядки, які малює векторна EMF-картинка (формули Cambria Math там — індекси гліфів, тобто «кракозябри»).")


def bg_md(bg: dict | None) -> str | None:
    if bg is None:
        return None
    kind = bg["type"]
    if kind == "picture":
        return f"картинка {media_md(bg['media'])}{' (плиткою)' if bg['tile'] else ''}"
    return f"колір {bg['color']}" if kind == "solid" else {"gradient": "градієнт", "theme": "стиль теми (bgRef)"}.get(kind, "?")


def shapes_md(shapes: list[dict], indent: str) -> list[str]:
    lines = []
    for s in shapes:
        shape_md(s, indent, lines)
    return lines


def render(d: dict) -> str:
    W, H = d["size"]["w"], d["size"]["h"]
    cm = f"{W / 360000:.2f}×{H / 360000:.2f} см"
    ratio = "4:3" if abs(W / H - 4 / 3) < .01 else f"{W / H:.3f}"
    hidden = ", ".join(map(str, d["hidden"])) or "немає"
    out = [f"# {d['lec']} — розкладка `{d['file']}`", "",
           f"Слайдів: {len(d['slides'])} · розмір {cm} ({W}×{H} EMU, {ratio}) · прихованих: {hidden}.", "",
           NOTATION, "", "## шаблон (майстер і макети; без плейсхолдерів)", ""]
    m = d["template"]["master"]
    out.append(f"- майстер{f' «{m['name']}»' if m['name'] else ''} · тло: {bg_md(m['bg']) or '—'}")
    out += shapes_md(m["shapes"], "  ")
    for lay in d["template"]["layouts"]:
        hide = "" if lay["masterShapes"] else " · фігури майстра приховано"
        out.append(f"- макет «{lay['name']}» (слайди {', '.join(map(str, lay['slides']))}) · тло: {bg_md(lay['bg']) or 'від майстра'}{hide}")
        out += shapes_md(lay["shapes"], "  ")
    out.append("")
    for s in d["slides"]:
        meta = [f"розмір {cm}", f"макет «{s['layout']}»"]
        meta += [f"тло: {bg_md(s['bg'])}"] if s["bg"] else []
        meta += [] if s["masterShapes"] else ["фігури майстра приховано"]
        meta += [f"знімок `s{s['n']:02d}.png`: {s['shot']}"] if s["shot"] else []
        out += [f"## слайд {s['n']}", "", " · ".join(meta)]
        out += ["", f"Знімок виправлено: {s['shotFixed']}"] if s["shotFixed"] else []
        out += ["", *(shapes_md(s["shapes"], "") or ["(порожньо)"]), ""]
    return "\n".join(out)
