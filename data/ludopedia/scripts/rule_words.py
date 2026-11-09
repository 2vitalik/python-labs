"""index/rule-words.md: words used in rule sentences (КОЛИ / ЯКЩО / ТО) against vocab/triggers|conditions|effects.md.
Known = ✅, ⏳ and 🔥 words of the vocab files + `custom`; the rest are listed by frequency (rule of three → vocab candidates)
and per file (v2 review: a word outside the vocab should be `custom: «…»` + a proposal)."""
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLOTS = {"when": ("КОЛИ", "triggers"), "cond": ("ЯКЩО", "conditions"), "then": ("ТО", "effects")}
TERM = re.compile(r"`([^`]+)`")
NAME = re.compile(r"^\s*(?:not\s+)?!?([a-z_][a-z0-9_]*)")


def vocab(name: str) -> set[str]:
    """The corpus file's words (✅ ⏳ 🔥) plus the site's own words (code_vocab.py) — both count as known."""
    text = (ROOT / "vocab" / f"{name}.md").read_text()
    sys.path.insert(0, str(ROOT / "scripts"))
    from code_vocab import words  # noqa: PLC0415
    return {m.group(1) for m in re.finditer(r"`([a-z_][a-z0-9_]*)(?:\([^`]*\))?`", text)} | words()[name] | {"custom"}


def words(sentence: str, label: str) -> list[str]:
    out = []
    for m in re.finditer(rf"(?<!\w){label}\s+(.*?)(?=\s*→\s*(?:КОЛИ|ЯКЩО|ТО)\b|$)", sentence):
        for term in TERM.findall(m.group(1)):
            for piece in re.split(r"\s*[|;,]\s*(?![^(]*\))", term):  # `a | b`, `a; b` — several words in one backtick
                n = NAME.match(piece)
                if n:
                    out.append(n.group(1))
    return out


def main():
    known = {k: vocab(v[1]) for k, v in SLOTS.items()}
    unknown, per_file, total = {k: Counter() for k in SLOTS}, defaultdict(Counter), Counter()
    for f in sorted((ROOT / "games").glob("*/*.md")):
        body = f.read_text()
        m = re.search(r"^## Правила.*?\n(.*?)(?=^## |\Z)", body, re.S | re.M)
        if not m:
            continue
        for line in m.group(1).splitlines():
            if not line.startswith("- "):
                continue
            for key, (label, _) in SLOTS.items():
                for w in words(line[2:], label):
                    total[key] += 1
                    if w not in known[key]:
                        unknown[key][w] += 1
                        per_file[f.relative_to(ROOT).as_posix()][f"{key}:{w}"] += 1
    out = ["# Слова правил поза словниками (автоген)", "", f"`scripts/rule_words.py` · слів у правилах: " +
           " · ".join(f"{SLOTS[k][0]} {total[k]} (поза словником {sum(unknown[k].values())})" for k in SLOTS), ""]
    for key, (label, vfile) in SLOTS.items():
        out += [f"## {label} → `vocab/{vfile}.md` · невідомих слів {len(unknown[key])}", ""]
        out += [f"- `{w}` ×{n}{' 🔥' if n >= 3 else ''}" for w, n in unknown[key].most_common(80)]
        out.append("")
    out += ["## По файлах (для ревʼю v1→v2)", ""]
    for path, c in sorted(per_file.items(), key=lambda x: -sum(x[1].values()))[:120]:
        out.append(f"- `{path}` · {sum(c.values())}: " + ", ".join(f"{w}×{n}" for w, n in c.most_common(12)))
    (ROOT / "index" / "rule-words.md").write_text("\n".join(out) + "\n")
    print("rule-words: " + " · ".join(f"{k} {sum(unknown[k].values())}/{total[k]} unknown" for k in SLOTS))


if __name__ == "__main__":
    sys.exit(main())
