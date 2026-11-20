"""A whole pptx → one dict: the template (master, the layouts in use) and every slide with its shapes."""
from pathlib import Path

from frame import placeholder
from ooxml import Theme, loc, media, q
from pptx import Presentation
from shapes import shapes

ABOUT = ("bin/pptxdump: what is set on each slide itself (nothing inherited from the layout / master). frame — percent of "
         "the slide's width / height, already in slide space inside groups; size — pt; colour — '#RRGGBB' first, then "
         "'≈' (a theme colour with a brightness modifier: the real shade differs) and '(тема accent1)' (from the theme); "
         "shape colour / size — what all its non-blank text runs share; runs: text · br · field · formula (OMML in linear "
         "form; color — the colour all its runs share; colored — when they differ, the text with [колір #…]…[/] marks); "
         "fallback — the picture PowerPoint keeps for old viewers instead of an OMML block (Quick Look shows it); "
         "crop — srcRect, percent cut from each side; shot / shotFixed — notes on the Quick Look snapshot sKK.png.")


class Ctx:
    def __init__(self, theme, W, H, part, layout_part=None, master_part=None):
        self.theme, self.W, self.H, self.part = theme, W, H, part
        self.layout_part, self.master_part = layout_part, master_part

    def media(self, rid):
        return media(self.part, rid)


def tree(ctx, root, skip_ph=False) -> list[dict]:
    els = root.find(q("p:cSld") + "/" + q("p:spTree"))
    keep = (c for c in els if not (skip_ph and loc(c) == "sp" and placeholder(c) is not None))
    return [s for c in keep for s in shapes(ctx, c, lambda b: b)]


def background(ctx, root) -> dict | None:
    bg = root.find(q("p:cSld") + "/" + q("p:bg"))
    if bg is None:
        return None
    if (pr := bg.find(q("p:bgPr"))) is not None:
        if (blip := pr.find(".//" + q("a:blip"))) is not None:
            return {"type": "picture", "media": ctx.media(blip.get(q("r:embed"))), "tile": pr.find(".//" + q("a:tile")) is not None}
        if (sf := pr.find(q("a:solidFill"))) is not None:
            return {"type": "solid", "color": ctx.theme.color(sf)}
        if pr.find(q("a:gradFill")) is not None:
            return {"type": "gradient"}
    return {"type": "theme" if bg.find(q("p:bgRef")) is not None else "unknown"}


def read(path: Path, lec: str, shots: dict) -> dict:
    """shots — {"K": {"shot": …, "fixed": …}}: notes on the Quick Look snapshots, kept beside them in render/lecNN/."""
    prs = Presentation(path)
    theme, W, H = Theme(prs), prs.slide_width, prs.slide_height
    master = prs.slide_masters[0]
    mctx = Ctx(theme, W, H, master.part)
    used = {}
    for k, s in enumerate(prs.slides, 1):
        used.setdefault(str(s.slide_layout.part.partname), (s.slide_layout, []))[1].append(k)
    layouts = []
    for lay, ks in used.values():
        lctx = Ctx(theme, W, H, lay.part)
        layouts.append({"name": lay.name, "slides": ks, "bg": background(lctx, lay._element),
                        "masterShapes": lay._element.get("showMasterSp") != "0", "shapes": tree(lctx, lay._element, True)})
    slides = []
    for k, s in enumerate(prs.slides, 1):
        ctx = Ctx(theme, W, H, s.part, s.slide_layout.part, master.part)
        note = shots.get(str(k), {})
        slides.append({"n": k, "layout": s.slide_layout.name, "bg": background(ctx, s._element),
                       "masterShapes": s._element.get("showMasterSp") != "0", "hidden": s._element.get("show") == "0",
                       "shot": note.get("shot"), "shotFixed": note.get("fixed"), "shapes": tree(ctx, s._element)})
    return {"about": ABOUT, "lec": lec, "file": path.name, "size": {"w": W, "h": H},
            "hidden": [s["n"] for s in slides if s["hidden"]],
            "template": {"master": {"name": master.name, "bg": background(mctx, master._element),
                                    "shapes": tree(mctx, master._element, True)}, "layouts": layouts},
            "slides": slides}
