"""What lexicon.json holds, and which words of the lectures it leaves out."""
from __future__ import annotations

import gzip
from collections import Counter

import pack
from corpus import CYRILLIC, norm, plain, texts, tokens


def run(listing: bool) -> int:
    data = pack.read()
    lemmas, stop = data["lemmas"], set(data.get("stop", []))
    if not lemmas:
        print("нема lexicon.json — спершу bin/leclexicon build")
        return 1
    raw = pack.LEXICON.read_bytes()
    forms = pack.index(lemmas)
    sizes = sorted(len(g) for g in lemmas)
    print(f"груп {len(lemmas)} · лем {len({g[0] for g in lemmas})} · форм {sum(sizes)}, різних {len(forms)}"
          f" · у групі {sizes[len(sizes) // 2]} (медіана), до {sizes[-1]} · stop {len(stop)}")
    print(f"файл {len(raw) / 1024:.0f} КБ · gzip {len(gzip.compress(raw)) / 1024:.0f} КБ")

    used = Counter(norm(w) for md in texts().values() for w in tokens(plain(md)))
    left = {w: n for w, n in used.items() if w not in forms}
    rest = {w: n for w, n in left.items() if w not in stop}
    total = sum(used.values())
    print(f"слів у лекціях {len(used)} різних, {total} усього · без леми {len(left)} різних"
          f" ({sum(left.values()) / total:.0%} слововживань)")
    print(f"  службових (stop) {len(left) - len(rest)} ({(sum(left.values()) - sum(rest.values())) / total:.0%})"
          f" · решта {len(rest)} ({sum(rest.values()) / total:.0%}): незмінні слова (прислівники, дієприслівники),"
          f" абревіатури, латиниця без множини ({sum(1 for w in rest if not CYRILLIC.search(w))}), нерозібрані")
    print(f"  найчастіші з решти: {', '.join(w for w, _ in Counter(rest).most_common(20))}")
    if listing:
        print("\n".join(f"  {w} {n}" for w, n in sorted(rest.items())))
    return 0
