"""Coins → a grade (T284 §4). The course has no fixed scale yet (grading T08 Q3): this is a draft to look at numbers with.
Coins double from kind to kind, so a wallet is one number in the cheapest of them — 🌱; the scale maps that number to a
grade, straight lines between its points. Who sees the estimate is the site's `GRADE_SCALE`: draft — the teacher only."""
WOOD = {"wood": 1, "tin": 2, "bronze": 4, "silver": 8, "gold": 16, "crown": 32}
# (🌱 accepted, grade): 60 — the least of the labs' tasks · 70 — a base game with the labs' musts · then ever slower
SCALE = [(0, 0), (30, 60), (110, 70), (190, 80), (300, 90), (480, 100)]


def wood(coins: dict) -> float:
    """A wallet {coin: amount} in 🌱."""
    return round(sum(n * WOOD.get(c, 0) for c, n in coins.items()), 1)


def grade(w: float) -> int:
    for (w0, g0), (w1, g1) in zip(SCALE, SCALE[1:]):
        if w < w1:
            return int(g0 + (g1 - g0) * (w - w0) / (w1 - w0))
    return SCALE[-1][1]
