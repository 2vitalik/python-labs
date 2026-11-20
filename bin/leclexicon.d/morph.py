"""Cyrillic words → lemma groups with every form of the paradigm (pymorphy3, Ukrainian dictionary)."""
from __future__ import annotations

from collections import Counter

import pymorphy3

import names
from corpus import WORD, norm

SERVICE = {"PREP", "CONJ", "PRCL", "NPRO"}
PROPER = {"Name", "Surn", "Patr"}
MIN_SCORE = 0.15


def analyzer() -> pymorphy3.MorphAnalyzer:
    m = pymorphy3.MorphAnalyzer(lang="uk")
    if m.lang != "uk" or "pymorphy3_dicts_uk" not in m.dictionary.path or not m.word_is_known("дисперсія"):
        raise SystemExit(f"не той словник pymorphy3: {m.lang} · {m.dictionary.path}")
    return m


def lemmas(m: pymorphy3.MorphAnalyzer, word: str, looks: set[str]) -> dict[tuple, list]:
    """(lemma, part of speech) → its parses of the word."""
    parses = m.parse(word)
    service = any(p.tag.POS in SERVICE for p in parses)
    found: dict[tuple, list] = {}
    for p in parses:
        if p.tag.POS in SERVICE or p.tag.POS is None or (looks == {"lower"} and PROPER & p.tag.grammemes):
            continue  # "тома" read in "тому" is a name, and the lectures never write it with a capital
        lemma = norm(p.normal_form)
        if service and lemma != word:  # "тому" is not a form of "том", but "коло" stays a noun
            continue
        found.setdefault((lemma, p.normalized.tag.POS), []).append(p)
    return {key: ps for key, ps in found.items() if sum(p.score for p in ps) >= MIN_SCORE}


def groups(words: dict[str, set[str]]) -> tuple[dict[tuple, set[str]], dict[str, str]]:
    """Lemma groups of the Cyrillic words, and notes on the rest: 'caps' and 'unknown' got no lemma,
    'service' can be a service word (and may still have a content lemma of its own form: "коло")."""
    m, out, paradigms, left = analyzer(), {}, {}, {}

    def forms(parses: list) -> set[str]:
        got: set[str] = set()
        for p in parses:
            if p.normalized not in paradigms:
                paradigms[p.normalized] = {norm(f.word) for f in p.lexeme if WORD.fullmatch(f.word)}
            got |= paradigms[p.normalized]
        return got

    readings: dict[str, dict[tuple, set[str]]] = {}
    for word, looks in words.items():
        if looks == {"caps"} and (len(word) <= 3 or not m.word_is_known(word)):  # abbreviations stay as written
            left[word] = "caps"
            continue
        found = {key: forms(ps) for key, ps in lemmas(m, word, looks).items()}
        if looks == {"title"} and not m.word_is_known(word):
            found = names.guess(word, found)
        if any(p.tag.POS in SERVICE for p in m.parse(word)):
            left[word] = "service"
        elif not found:
            left[word] = "unknown"
        readings[word] = found
    support = Counter(key for found in readings.values() for key in found)
    for found in readings.values():
        best = max((support[key] for key in found), default=0)
        for key, fs in found.items():
            if support[key] > 1 or support[key] == best:  # "осі" is "вісь" all over the lectures, never "оса"
                out.setdefault(key, {key[0]}).update(fs)
    return out, left
