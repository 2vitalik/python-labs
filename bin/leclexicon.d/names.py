"""Surnames the dictionary lacks: the lectures mostly write them in the genitive ("критерій Кендалла")."""
from __future__ import annotations

VOWELS = set("аеєиіїоуюяьй'")
HARD = ("", "а", "у", "ові", "ом", "і", "е")  # Кендалл, Кендалла, Кендаллу, Кендаллові, Кендаллом, Кендаллі
SLAVIC = ("", "а", "у", "ові", "им", "і")  # Чебишов, Чебишова, Чебишову, Чебишові, Чебишовим
SLAVIC_ENDS = ("ов", "ев", "єв", "ін", "ин", "їн")


def genitive(word: str) -> tuple[str, set[str]] | None:
    """'кендалла' → ('кендалл', its forms); pymorphy takes such a word for a feminine noun or worse."""
    stem = word[:-1]
    if len(word) < 4 or not word.endswith("а") or stem[-1] in VOWELS or "-" in word:
        return None
    return stem, {stem + end for end in (SLAVIC if stem.endswith(SLAVIC_ENDS) else HARD)}


def guess(word: str, found: dict[tuple, set[str]]) -> dict[tuple, set[str]]:
    """Lemma groups of a capitalised word the dictionary does not know: a name is a noun."""
    if any(pos == "NOUN" for _, pos in found):  # "Краскала" is not a verb, "Уітні" not an adjective
        found = {key: forms for key, forms in found.items() if key[1] == "NOUN"}
    masc = genitive(word)
    if masc:  # kept next to pymorphy's guess: a nominative in -а ("Сковорода") is a name too
        found.setdefault((masc[0], "NOUN"), set()).update(masc[1])
    return found
