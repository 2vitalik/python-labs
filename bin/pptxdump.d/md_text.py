"""Runs and paragraphs → layout.md's inline notation: **bold**, *italic*, [колір #…]…[/], [18pt]…[/], ^{…}, ⏎."""
from md_glyphs import prefix, pua


def wrap(r: dict, outer: str | None, drop_size: bool) -> str:
    """outer — the colour already stated around this run (the shape's, the paragraph's): not repeated."""
    if r["kind"] == "br":
        return " ⏎ "
    if r["kind"] == "field":
        label = "№ слайда" if r["field"] == "slidenum" else f"поле {r['field'] or 'поле'}"
        return f"[{label}: {r['text']}]"
    if r["kind"] == "formula":
        s = f"[формула: {r['colored'] or r['text']}]"
        return f"[колір {r['color']}]{s}[/]" if r["color"] and r["color"] != outer else s
    t = r["text"]
    core = t.strip()
    if not core:
        return t
    s = pua(core, r["font"])
    if r["font"]:
        s = f"[шрифт {r['font']}]{s}[/]"
    if r["script"]:
        s = f"{'^' if r['script'] == 'sup' else '_'}{{{s}}}"
    if r["underline"]:
        s = f"[підкр]{s}[/]"
    if r["italic"]:
        s = f"*{s}*"
    if r["bold"]:
        s = f"**{s}**"
    if r["highlight"]:
        s = f"[тло {r['highlight']}]{s}[/]"
    if r["color"] and r["color"] != outer:
        s = f"[колір {r['color']}]{s}[/]"
    if r["size"] is not None and not drop_size:
        s = f"[{r['size']:g}pt]{s}[/]"
    return t[: len(t) - len(t.lstrip())] + s + t[len(t.rstrip()):]


def join_marked(pieces) -> str:
    """Glue neighbour runs: `*x*` + `*^{1}*` -> `*x^{1}*`, `**a**` + `**b**` -> `**ab**` (no `*x**y*` ambiguity)."""
    out = ""
    for piece in pieces:
        if out.endswith("**") and piece.startswith("**") and not out.endswith("***") and not piece.startswith("***"):
            out, piece = out[:-2], piece[2:]
        elif out.endswith("*") and not out.endswith("**") and piece.startswith("*") and not piece.startswith("**"):
            out, piece = out[:-1], piece[1:]
        out += piece
    return out


def runs_md(p: dict, outer=None, drop_size=False) -> str:
    return join_marked(wrap(r, outer, drop_size) for r in p["runs"]).strip()


def paragraph_md(p: dict, shape_color: str | None, shape_size: bool) -> str:
    """The colour / size shared by a whole paragraph (of 2+ runs) wraps it once instead of every run."""
    rs = [r for r in p["runs"] if r["kind"] == "text" and r["text"].strip()]
    whole = lambda key, done: None if done or len(rs) < 2 or len(v := {r[key] for r in rs}) != 1 or None in v else v.pop()
    color, size = whole("color", shape_color is not None), whole("size", shape_size)
    body = runs_md(p, shape_color or color, shape_size or size is not None)
    if color is not None:
        body = f"[колір {color}]{body}[/]"
    if size is not None:
        body = f"[{size:g}pt]{body}[/]"
    return prefix(p) + body
