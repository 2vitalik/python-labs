"""A student's own notebook to start from (T354 §5, «мій ноутбук»): the lab's template with their card in place of `# ✂`."""
import json

import labs_marimo
from labs_nb import text

CUT = labs_marimo.CUT


def jupyter(tpl: bytes, card: list[str]) -> bytes:
    nb = json.loads(tpl)
    cell = next((c for c in nb["cells"] if c.get("cell_type") == "code" and text(c.get("source")).lstrip().startswith(CUT)), None)
    if not cell:
        raise ValueError("no `# ✂` cell in the template")
    lines = text(cell["source"]).split("\n")
    i = next(i for i, line in enumerate(lines) if line.lstrip().startswith(CUT))
    lines[i:i + 1] = card
    cell["source"] = "\n".join(lines).splitlines(keepends=True)
    return json.dumps(nb, ensure_ascii=False, indent=1).encode()


def made(kind: str, tpl: bytes | str, card: list[str]) -> bytes:
    """ValueError — the template has no `# ✂` line to put the card in."""
    return jupyter(tpl, card) if kind == "jupyter" else labs_marimo.paste(tpl, card).encode()
