"""A graphic frame: a table cell by cell, an OLE object with its preview pictures, a chart, SmartArt."""
import json

from body import paragraphs
from ooxml import q


def cell(theme, tc) -> dict:
    if tc.get("hMerge") == "1" or tc.get("vMerge") == "1":
        return {"merge": "h" if tc.get("hMerge") == "1" else "v", "span": None, "paragraphs": []}
    tx = tc.find(q("a:txBody"))
    span = tc.get("gridSpan")
    return {"merge": None, "span": int(span) if span else None, "paragraphs": paragraphs(theme, tx) if tx is not None else []}


def graphic(ctx, el, s: dict) -> None:
    gd = el.find(".//" + q("a:graphicData"))
    uri = gd.get("uri", "") if gd is not None else ""
    if uri.endswith("/table"):
        tbl = gd.find(q("a:tbl"))
        s.update(kind="table", cols=len(tbl.find(q("a:tblGrid")).findall(q("a:gridCol"))),
                 rows=[[cell(ctx.theme, tc) for tc in tr.findall(q("a:tc"))] for tr in tbl.findall(q("a:tr"))])
    elif uri.endswith("/ole"):
        ole = gd.find(".//" + q("p:oleObj"))
        pics = (ctx.media(bp.get(q("r:embed"))) for bp in gd.iter(q("a:blip")))
        s.update(kind="ole", prog=ole.get("progId") if ole is not None else "?",
                 previews=list({json.dumps(m, sort_keys=True): m for m in pics}.values()))
    elif "chart" in uri:
        s["kind"] = "chart"
    elif "diagram" in uri:
        s["kind"] = "smartart"
    else:
        s.update(kind="frame", uri=uri)
