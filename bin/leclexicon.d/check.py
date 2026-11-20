"""search/thesaurus.json: every group must lead somewhere — its main or an also occurs in the lectures, in any form."""
from __future__ import annotations

import json

import pack
from corpus import SEARCH, norm, plain, texts, tokens

THESAURUS = SEARCH / "thesaurus.json"


class Corpus:
    def __init__(self):
        docs = texts()
        self.words = {slug: [norm(w) for w in tokens(plain(md))] for slug, md in docs.items()}
        self.raw = {slug: md.lower() for slug, md in docs.items()}
        self.forms = pack.index(pack.load())
        self.at: dict[str, list[tuple[str, int]]] = {}
        for slug, words in self.words.items():
            for i, w in enumerate(words):
                self.at.setdefault(w, []).append((slug, i))

    def where(self, phrase: str) -> list[str]:
        """Lectures holding the phrase: word after word, each in any of its forms; a phrase of no words — as typed."""
        need = [self.forms.get(norm(w), {norm(w)}) for w in tokens(phrase)]
        if not need:
            return [slug for slug, raw in self.raw.items() if phrase.strip().lower() in raw]
        found = set()
        for slug, i in (spot for form in need[0] for spot in self.at.get(form, ())):
            words = self.words[slug]
            if all(i + k < len(words) and words[i + k] in need[k] for k in range(1, len(need))):
                found.add(slug)
        return sorted(found)


def run(verbose: bool) -> int:
    if not THESAURUS.exists():
        print(f"нема {THESAURUS.relative_to(SEARCH.parent)} — перевіряти нічого")
        return 0
    groups = json.loads(THESAURUS.read_text(encoding="utf-8")).get("groups", [])
    c, dead, bad, seen = Corpus(), 0, 0, {}
    for n, g in enumerate(groups, 1):
        main, also = g.get("main"), g.get("also", [])
        if not isinstance(main, str) or not main.strip() or not isinstance(also, list):
            print(f"✗ група {n}: main — непорожній рядок, also — список")
            bad += 1
            continue
        hits = {p: c.where(p) for p in [main, *also]}
        for p in hits:
            if norm(p) in seen:
                print(f"· «{p}» уже є в групі {seen[norm(p)]}")
            seen.setdefault(norm(p), n)
        if not any(hits.values()):
            dead += 1
            print(f"✗ група {n} «{main}» нікуди не веде: {', '.join(also) or 'also порожній'}")
        elif verbose:
            print(f"✓ {main}: " + " · ".join(f"{p} → {', '.join(s[3:] for s in hits[p]) or '—'}" for p in hits))
    print(f"груп {len(groups)} · нікуди не ведуть {dead}" + (f" · хибних {bad}" if bad else ""))
    return 1 if dead or bad else 0
