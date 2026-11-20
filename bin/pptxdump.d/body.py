"""A text body's paragraphs: level, alignment, an explicit bullet, the runs; the look its runs share."""
from ooxml import q
from text import pieces, run


def bullet(pPr) -> dict | None:
    if pPr is None:
        return None
    if (bc := pPr.find(q("a:buChar"))) is not None:
        font = pPr.find(q("a:buFont"))
        return {"char": bc.get("char") or "", "font": font.get("typeface") if font is not None else None}
    if (ba := pPr.find(q("a:buAutoNum"))) is not None:
        return {"autonum": ba.get("type")}
    return None


def paragraph(theme, p) -> dict:
    glued = []
    for kind, t, extra in pieces(theme, p):
        if glued and kind == "text" and glued[-1][0] == "text" and glued[-1][2] == extra:
            glued[-1] = (kind, glued[-1][1] + t, extra)
        else:
            glued.append((kind, t, extra))
    pPr = p.find(q("a:pPr"))
    return {"level": int(pPr.get("lvl", "0")) if pPr is not None else 0, "align": pPr.get("algn") if pPr is not None else None,
            "bullet": bullet(pPr), "runs": [run(*g) for g in glued]}


def paragraphs(theme, txBody) -> list[dict]:
    """Paragraphs with something to show: a non-blank run, a line break, a field or a formula."""
    paras = (paragraph(theme, p) for p in txBody.findall(q("a:p")))
    return [p for p in paras if any(r["kind"] != "text" or r["text"].strip() for r in p["runs"])]


def uniform(paras: list[dict], key: str):
    """The colour / size all the non-blank runs share; None when they differ or some lack it."""
    vals = {r[key] for p in paras for r in p["runs"] if r["kind"] == "text" and r["text"].strip()}
    return next(iter(vals)) if len(vals) == 1 and None not in vals else None
