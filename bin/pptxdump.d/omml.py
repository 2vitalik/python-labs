"""OMML (Office Math) -> linear text: (a)/(b), x_{i}, x^{2}, √(…), ∑_{…}^{…}(…).

paint(run, text) -> text, when given, marks up what each m:r contributes (its colour, say)."""
M = "http://schemas.openxmlformats.org/officeDocument/2006/math"


def _l(e):
    return e.tag[len(M) + 2:] if isinstance(e.tag, str) and e.tag.startswith(f"{{{M}}}") else ""


def _kid(e, name):
    return e.find(f"{{{M}}}{name}")


def _val(e, path, default):
    x = e
    for name in path:
        x = _kid(x, name) if x is not None else None
    if x is None:
        return default
    return x.get(f"{{{M}}}val", default)


def lin(e, paint=None):
    if e is None:
        return ""
    t = _l(e)
    if t.endswith("Pr"):
        return ""
    L = lambda x: lin(x, paint)
    s = lambda name: L(_kid(e, name)) if _kid(e, name) is not None else ""
    if t == "t":
        return e.text or ""
    if t == "r" and paint:
        return paint(e, "".join(L(c) for c in e))
    if t == "f":
        return f"({s('num')})/({s('den')})"
    if t == "sSub":
        return f"{s('e')}_{{{s('sub')}}}"
    if t == "sSup":
        return f"{s('e')}^{{{s('sup')}}}"
    if t == "sSubSup":
        return f"{s('e')}_{{{s('sub')}}}^{{{s('sup')}}}"
    if t == "sPre":
        return f"_{{{s('sub')}}}^{{{s('sup')}}}{s('e')}"
    if t == "rad":
        deg = s("deg")
        return f"√{'[' + deg + ']' if deg else ''}({s('e')})"
    if t == "nary":
        lo, hi = s("sub"), s("sup")
        return _val(e, ["naryPr", "chr"], "∫") + (f"_{{{lo}}}" if lo else "") + (f"^{{{hi}}}" if hi else "") + f"({s('e')})"
    if t == "d":
        beg, end, sep = (_val(e, ["dPr", k], d) for k, d in (("begChr", "("), ("endChr", ")"), ("sepChr", "|")))
        return beg + sep.join(L(x) for x in e.findall(f"{{{M}}}e")) + end
    if t == "acc":
        return f"{s('e')}{_val(e, ['accPr', 'chr'], chr(0x302))}"
    if t == "bar":
        return f"{'underline' if _val(e, ['barPr', 'pos'], 'bot') == 'bot' else 'overline'}({s('e')})"
    if t == "groupChr":
        return f"{s('e')}{_val(e, ['groupChrPr', 'chr'], '⏟')}"
    if t == "func":
        return f"{s('fName')} {s('e')}"
    if t == "limLow":
        return f"{s('e')}_{{{s('lim')}}}"
    if t == "limUpp":
        return f"{s('e')}^{{{s('lim')}}}"
    if t == "eqArr":
        return "{ " + " ; ".join(L(x) for x in e.findall(f"{{{M}}}e")) + " }"
    if t == "m":
        rows = [", ".join(L(c) for c in r.findall(f"{{{M}}}e")) for r in e.findall(f"{{{M}}}mr")]
        return "[" + "; ".join(rows) + "]"
    if t == "oMathPara":
        return " ; ".join(L(x) for x in e.findall(f"{{{M}}}oMath"))
    return "".join(L(c) for c in e)
