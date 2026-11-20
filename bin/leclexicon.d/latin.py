"""English words: the word is its own lemma; a plural in -s / -es / -ies joins its singular."""
from __future__ import annotations


def singular(word: str, known: set[str]) -> str:
    for cut, tail in (("ies", "y"), ("es", ""), ("s", "")):
        if word.endswith(cut) and word[: -len(cut)] + tail in known:
            return word[: -len(cut)] + tail
    if len(word) <= 3 or word.endswith(("ss", "is", "us", "ics", "series", "species")):  # "analysis", "statistics"
        return word
    if word.endswith("ies"):
        return word[:-3] + "y"
    if word.endswith(("sses", "xes", "ches", "shes")):
        return word[:-2]
    return word[:-1] if word.endswith("s") else word  # "algorithms" alone still gets "algorithm"


def groups(words: dict[str, set[str]]) -> dict[tuple, set[str]]:
    """Abbreviations ("PCA", "SSE") stay as written; a singular never written in the plural stays alone."""
    known = set(words)
    out: dict[tuple, set[str]] = {}
    for word in sorted(known):
        lemma = word if words[word] == {"caps"} else singular(word, known)
        out.setdefault((lemma, "LATN"), {lemma}).add(word)
    return out
