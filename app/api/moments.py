"""A game's moments drawn on the site (T276): the scenarios of a moments text and their frames, counted the way the editor
cuts the text (app/vue/src/momentsText.js) — a `### ` heading starts a scenario, a ```field (or a bare ```) block with cells
is a frame. The cards these drawings claim by themselves — auto_claims.py."""
import re

FRAMES, MAP = "moment-frames", "level-map-drawn"  # «Ігровий момент по кадрах» · «Мапа рівня на сайті»
GRID = re.compile(r"^```(field)?\s*$")
H3 = re.compile(r"^### \S")


def blocks(text: str) -> list[list[str]]:
    """Paragraphs and fenced blocks in order, each as its lines."""
    lines, out, i = text.replace("\r", "").split("\n"), [], 0
    while i < len(lines):
        if not lines[i].strip():
            i += 1
            continue
        start = i
        if lines[i].startswith("```"):
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                i += 1
            i += 1
        else:
            while i < len(lines) and lines[i].strip() and not lines[i].startswith("```"):
                i += 1
        out.append(lines[start:i])
    return out


def scenes(text: str) -> list[int]:
    """How many frames each scenario has; the text before the first heading is a scenario too."""
    out = [0]
    for b in blocks(text or ""):
        if GRID.match(b[0]):
            out[-1] += any(line.strip() and not line.startswith("```") for line in b[1:])
        elif len(b) == 1 and H3.match(b[0]):
            out.append(0)
    return out


def full(text: str) -> int:
    """The scenarios worth a «moment-frames» claim: three frames and more."""
    return sum(n >= 3 for n in scenes(text))
