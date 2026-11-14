"""What the claims of one card are worth in a game (T291 §13): the n-th claim (from 1) is worth amount × factor(n).
A card's price steps — `tiers` [[upto, factor], …], `upto` growing, 0 in the last one — «on with no end»; no steps —
`max_count` as before (1 — once · N — N times · 0 — no cap), each in full."""


def cap(task) -> int:
    """How many claims of the card count; 0 — no cap. With steps the last one says it."""
    return task.tiers[-1][0] if task.tiers else task.max_count


def repeatable(task) -> bool:
    return bool(task.tiers) or task.max_count != 1


def factor(task, n: int) -> float:
    """The n-th claim's share of the price; 0 past the cap."""
    if (c := cap(task)) and n > c:
        return 0
    return next((f for upto, f in task.tiers if not upto or n <= upto), 1)


def worth(task, count: int) -> float:
    """The first `count` claims together, in prices of one claim."""
    return sum(factor(task, n) for n in range(1, count + 1))


def clean_tiers(tiers) -> list[list]:
    """[[upto, factor], …] as the card keeps them, or ValueError with what is wrong, in words."""
    out = []
    for i, step in enumerate(tiers or []):
        if not isinstance(step, list | tuple) or len(step) != 2 or not all(num(x) for x in step):
            raise ValueError("Сходинки ціни — пари [до якої заявки, множник].")
        upto, f = step
        last = i == len(tiers) - 1
        if upto != int(upto) or upto < 0 or (not upto and not last) or (out and upto and upto <= out[-1][0]):
            raise ValueError("Сходинки ціни: межі — цілі числа більші за 0, за зростанням; 0 («далі без межі») — лише в останній.")
        if not 0 < f <= 1 or (out and f > out[-1][1]):
            raise ValueError("Сходинки ціни: множник — від 0 (не включно) до 1, і на кожній наступній сходинці не більший.")
        out.append([int(upto), int(f) if f == int(f) else float(f)])
    return out


def num(x) -> bool:
    return isinstance(x, int | float) and not isinstance(x, bool)
