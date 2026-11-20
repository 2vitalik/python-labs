"""Edits cut and joined beyond the token diff: an edit never crosses a table's cell border; a word moved within
its block is one edit, not a removal and an addition."""
from tok import inside


def cells(toks: list, i: int, j: int, spans: list) -> list[tuple[int, int]]:
    """A run of tokens cut before each border `|` of a table's cell (outside formulas)."""
    out, start = [], i
    for p in range(i, j):
        if p > start and toks[p][0].strip() == "|" and not inside(toks[p][1], spans):
            out.append((start, p))
            start = p
    return out + [(start, j)]


def split(x: list, y: list, mx: list, my: list, found: list[tuple]) -> list[tuple]:
    """An edit never crosses a cell's border: a translated header and a new column are two edits, the cells paired in order."""
    out = []
    for _, i, j, k, l in found:
        px, py = cells(x, i, j, mx), cells(y, k, l, my)
        for t in range(max(len(px), len(py))):
            a = px[t] if t < len(px) else (j, j)
            b = py[t] if t < len(py) else (l, l)
            if [z[0] for z in x[slice(*a)]] != [z[0] for z in y[slice(*b)]]:
                out.append((None, *a, *b))
    return out


def moved(found: list[dict]) -> list[dict]:
    """A word gone from one place of a block and come to another — one edit (`moved`), `a` where it was, `b` where it is."""
    out = list(found)
    for d in found:
        if d["ins"] or not any(c.isalpha() for c in d["del"]) or d not in out:
            continue
        i = next((i for i in out if not i["del"] and i["ins"] == d["del"]), None)
        if i:
            out[out.index(d)] = {"del": d["del"], "ins": i["ins"], "a": d["a"], "b": i["b"], "math": d["math"] and i["math"],
                                 "moved": True}
            out.remove(i)
    return out
