"""Where a shape sits: its own xfrm, else a placeholder's from the layout / master; a group's child space → the slide's."""
from ooxml import loc, q

SAME = {"ctrTitle": "title", "subTitle": "body"}


def placeholder(el) -> tuple | None:
    ph = el.find(".//" + q("p:nvPr") + "/" + q("p:ph"))
    return None if ph is None else (ph.get("type", "body"), ph.get("idx"))


def inherited(ctx, ph: tuple):
    """A placeholder without its own xfrm: the layout's (same idx, else type), then the master's (type)."""
    typ, idx = ph
    for part, by_idx in ((ctx.layout_part, True), (ctx.master_part, False)):
        if part is None:
            continue
        for sp in part._element.iter(q("p:sp")):
            pi = placeholder(sp)
            if pi is None:
                continue
            same = (by_idx and idx is not None and pi[1] == idx) or SAME.get(pi[0], pi[0]) == SAME.get(typ, typ)
            x = sp.find(q("p:spPr") + "/" + q("a:xfrm"))
            if same and x is not None:
                return x
    return None


def own(el):
    t = loc(el)
    if t == "grpSp":
        return el.find(q("p:grpSpPr") + "/" + q("a:xfrm"))
    if t in ("graphicFrame", "contentPart"):
        return next((x for x in el if loc(x) == "xfrm"), None)
    return el.find(q("p:spPr") + "/" + q("a:xfrm"))


def box(x) -> tuple | None:
    """xfrm → (x, y, cx, cy) in EMU."""
    off, ext = (x.find(q("a:off")), x.find(q("a:ext"))) if x is not None else (None, None)
    if off is None or ext is None:
        return None
    return int(off.get("x")), int(off.get("y")), int(ext.get("cx")), int(ext.get("cy"))


def frame(ctx, b: tuple | None, x) -> dict | None:
    """A box already in slide EMU → percent of the slide's width / height, plus rotation and mirroring."""
    if b is None:
        return None
    f = {"x": 100 * b[0] / ctx.W, "y": 100 * b[1] / ctx.H, "w": 100 * b[2] / ctx.W, "h": 100 * b[3] / ctx.H}
    if x is not None:
        if rot := int(x.get("rot", "0")):
            f["rot"] = rot / 60000
        if x.get("flipH") == "1":
            f["flipH"] = True
        if x.get("flipV") == "1":
            f["flipV"] = True
    return f


def child_space(x, b: tuple, T):
    """A group's xfrm maps its children's chOff / chExt space onto its own box; T then maps that onto the slide."""
    ox, oy, cx, cy = b
    choff, chext = x.find(q("a:chOff")), x.find(q("a:chExt"))
    chx, chy = int(choff.get("x")), int(choff.get("y"))
    sx = cx / int(chext.get("cx")) if int(chext.get("cx")) else 1
    sy = cy / int(chext.get("cy")) if int(chext.get("cy")) else 1
    return lambda cb: T((ox + (cb[0] - chx) * sx, oy + (cb[1] - chy) * sy, cb[2] * sx, cb[3] * sy))
