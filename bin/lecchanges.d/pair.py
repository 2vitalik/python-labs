"""The blocks of a slide then and now, paired (contract §3.2.3): the same bare form — a pair; alike ≥ 0.5 — a pair;
a block merged into a neighbour (or split off one) joins its pair; what is left between the same two pairs (a paragraph
translated from Russian, a heading reworded, five lines made one) — one group; the rest — removed or added.
A group is (base indices, now indices); one side may be empty."""
from difflib import SequenceMatcher

LIKE, JOIN, GAP = 0.5, 0.05, 0.25


def words(blocks: list[dict], idx: list[int]) -> list[str]:
    """Words and numbers only, in lower case, decimal commas as dots: the signs and LaTeX of an added formula, a table
    with its numbers in the other notation would make a block unlike its old self."""
    return [w.lower().replace(",", ".") for i in idx for t in blocks[i]["tokens"] if (w := t[0].strip())[0].isalnum()]


def ratio(x: list[str], y: list[str]) -> float:
    return SequenceMatcher(None, x, y, autojunk=False).ratio() if x or y else 1.0


def pairs(base: list[dict], now: list[dict]) -> list[tuple[list[int], list[int]]]:
    def take(bi, ni):
        groups.append((bi, ni))
        left.difference_update(bi)
        right.difference_update(ni)

    def like(bi, ni):
        return ratio(words(base, bi), words(now, ni))

    groups, left, right = [], set(range(len(base))), set(range(len(now)))
    sm = SequenceMatcher(None, [b["bare"] for b in base], [b["bare"] for b in now], autojunk=False)
    for i, k, n in sm.get_matching_blocks():
        for d in range(n):
            take([i + d], [k + d])
    for i in sorted(left):  # moved within the slide, word for word
        if (k := next((k for k in sorted(right) if now[k]["bare"] == base[i]["bare"]), None)) is not None:
            take([i], [k])
    for r, i, k in sorted(((like([i], [k]), -i, -k) for i in left for k in right), reverse=True):
        if r >= LIKE and -i in left and -k in right:
            take([-i], [-k])
    for side, rest in ((0, left), (1, right)):
        for x in sorted(rest):
            best, gain = None, JOIN
            for g in groups:
                grown = sorted(g[side] + [x])
                r = like(grown, g[1]) if side == 0 else like(g[0], grown)
                if r - like(*g) > gain:
                    best, gain = (g, grown), r - like(*g)
            if best:
                best[0][side][:] = best[1]
                rest.discard(x)
    for bi, ni in gaps(groups, sorted(left), sorted(right)):
        bi, ni = [i for i in bi if i in left], [k for k in ni if k in right]
        one = len(bi) == len(ni) == 1 and base[bi[0]]["kind"] == now[ni[0]]["kind"]
        if bi and ni and (one or like(bi, ni) >= GAP):
            take(bi, ni)
    return groups + [([i], []) for i in sorted(left)] + [([], [k]) for k in sorted(right)]


def gaps(groups: list, left: list[int], right: list[int]) -> list[tuple[list[int], list[int]]]:
    """Leftovers on both sides that stand between the same two pairs."""
    anchors = sorted((min(b), min(n)) for b, n in groups)
    out = []
    for lo, hi in zip([(-1, -1)] + anchors, anchors + [(10**9, 10**9)]):
        bi = [i for i in left if lo[0] < i < hi[0]]
        ni = [k for k in right if lo[1] < k < hi[1]]
        if bi and ni:
            out.append((bi, ni))
    return out
