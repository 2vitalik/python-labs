"""OOXML basics for bin/pptxdump: namespaced tags, the theme's colours, the media part behind a relationship id."""
from emf import emf_text
from lxml import etree
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.parts.image import Image

NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "mc": "http://schemas.openxmlformats.org/markup-compatibility/2006",
    "a14": "http://schemas.microsoft.com/office/drawing/2010/main",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
}


def q(path: str) -> str:
    pre, name = path.split(":")
    return f"{{{NS[pre]}}}{name}"


def loc(e) -> str:
    return e.tag.rsplit("}", 1)[-1] if isinstance(e.tag, str) else ""


class Theme:
    """The first master's colour scheme, looked up through its colour map (tx1 → dk1 …)."""

    def __init__(self, prs):
        master = prs.slide_masters[0]
        scheme = etree.fromstring(master.part.part_related_by(RT.THEME).blob).find(".//" + q("a:clrScheme"))
        self.scheme = {}
        for c in scheme:
            v, s = c.find(q("a:srgbClr")), c.find(q("a:sysClr"))
            self.scheme[loc(c)] = (v.get("val") if v is not None else s.get("lastClr") if s is not None else "?").upper()
        cmap = master._element.find(q("p:clrMap"))
        self.cmap = dict(cmap.attrib) if cmap is not None else {}

    def color(self, holder) -> str | None:
        """'#RRGGBB'; '≈' — modified by brightness / alpha (the real shade differs); '(тема accent1)' — a scheme colour."""
        if holder is None:
            return None
        for c in holder:
            n, mods = loc(c), "≈" if len(c) else ""
            if n == "srgbClr":
                return f"#{c.get('val').upper()}{mods}"
            if n == "schemeClr":
                v = c.get("val")
                return f"#{self.scheme.get(self.cmap.get(v, v), v)}{mods} (тема {v})"
            if n == "sysClr":
                return f"#{c.get('lastClr', '?').upper()}"
            if n == "prstClr":
                return c.get("val")
        return None


def media(part, rid: str | None) -> dict | None:
    """A picture behind a relationship id: its file inside the pptx, size in px, the strings an EMF draws."""
    if not rid:
        return None
    rel = part.rels.get(rid)
    if rel is None:
        return {"missing": rid}
    if rel.is_external:
        return {"url": rel.target_ref}
    tp = rel.target_part
    name = str(tp.partname).lstrip("/")
    m = {"file": name.replace("ppt/", ""), "ext": name.rsplit(".", 1)[-1].lower()}
    try:
        m["px"] = list(Image.from_blob(tp.blob).size)
    except Exception:  # noqa: BLE001, S110 — EMF / WMF: python-pptx cannot measure them
        pass
    if m["ext"] == "emf" and (t := emf_text(tp.blob)):
        m["emfText"] = t
    return m
