"""One element of a shape tree → shape dicts: text boxes, pictures, lines, groups (recursively), graphic frames."""
from body import paragraphs, uniform
from frame import box, child_space, frame, inherited, own, placeholder
from graphic import graphic
from ooxml import loc, q

SHAPE_TAGS = {"sp", "pic", "cxnSp", "graphicFrame", "grpSp", "contentPart", "AlternateContent"}


def names(el) -> dict:
    c = el.find(".//" + q("p:cNvPr"))
    if c is None:
        return {"name": None, "hidden": False, "descr": None}
    return {"name": c.get("name"), "hidden": c.get("hidden") == "1", "descr": c.get("descr") or None}


def paint(ctx, spPr) -> dict:
    fill = outline = None
    for c in spPr if spPr is not None else ():
        n = loc(c)
        if n == "solidFill":
            fill = {"type": "solid", "color": ctx.theme.color(c)}
        elif n in ("gradFill", "pattFill"):
            fill = {"type": "gradient" if n == "gradFill" else "pattern"}
        elif n == "blipFill":
            blip = c.find(q("a:blip"))
            fill = {"type": "picture", "media": ctx.media(blip.get(q("r:embed")) if blip is not None else None)}
        elif n == "ln" and (lf := c.find(q("a:solidFill"))) is not None:
            outline = ctx.theme.color(lf)
    return {"fill": fill, "outline": outline}


def shapes(ctx, el, T, fallback=None) -> list[dict]:
    """T maps an EMU box into slide EMU (identity at the top, a group's child space inside it)."""
    t = loc(el)
    if t == "AlternateContent":
        # the Choice is the shape (an OMML text box); the Fallback holds the picture old viewers show instead
        choice, fb = el.find(q("mc:Choice")), el.find(q("mc:Fallback"))
        pics = [ctx.media(b.get(q("r:embed"))) for b in fb.iter(q("a:blip"))] if fb is not None else []
        return [s for c in (choice if choice is not None else ()) if loc(c) in SHAPE_TAGS for s in shapes(ctx, c, T, pics)]
    if t not in SHAPE_TAGS:
        return []
    ph = placeholder(el) if t == "sp" else None
    x = own(el)
    if x is None and ph is not None:
        x = inherited(ctx, ph)
    b = box(x)
    s = {"kind": None, **names(el), "frame": frame(ctx, T(b) if b else None, x), "placeholder": ph[0] if ph else None}
    if fallback:
        s["fallback"] = fallback
    if t == "grpSp":
        Tc = child_space(x, b, T)
        s.update(kind="group", children=[k for c in el for k in shapes(ctx, c, Tc)])
    elif t == "pic":
        blip = el.find(".//" + q("a:blip"))
        rid = (blip.get(q("r:embed")) or blip.get(q("r:link"))) if blip is not None else None
        src = el.find(".//" + q("a:srcRect"))
        crop = {k: int(v) / 1000 for k, v in src.attrib.items()} if src is not None else {}
        s.update(kind="picture", media=ctx.media(rid), crop=crop or None)
    elif t == "cxnSp":
        geom = el.find(".//" + q("a:prstGeom"))
        s.update(kind="line", geom=geom.get("prst") if geom is not None else None, **paint(ctx, el.find(q("p:spPr"))))
    elif t == "contentPart":
        s["kind"] = "ink"
    elif t == "graphicFrame":
        graphic(ctx, el, s)
    else:
        spPr = el.find(q("p:spPr"))
        geom = spPr.find(q("a:prstGeom")) if spPr is not None else None
        custom = spPr is not None and spPr.find(q("a:custGeom")) is not None
        tx = el.find(q("p:txBody"))
        paras = paragraphs(ctx.theme, tx) if tx is not None else []
        s.update(kind="text" if paras else "shape", geom=geom.get("prst") if geom is not None else "custom" if custom else None,
                 **paint(ctx, spPr), color=uniform(paras, "color"), size=uniform(paras, "size"), paragraphs=paras)
    return [s]
