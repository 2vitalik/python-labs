"""A student's cells against the lab's template (T354 §3): signatures → difflib opcodes. A replaced run pairs cells
of one kind in order — a removed `# ✍` mark keeps its cell; what is left over is the student's own and belongs to the
task before it (a solution split into several cells)."""
from difflib import SequenceMatcher

import labs_keys
import labs_nb


def match(cells: list[dict], tmpl: list[dict]) -> list[int | None]:
    """Per student cell — the index of the template cell it stands for; None — a cell of the student's own."""
    at: list[int | None] = [None] * len(cells)
    ops = SequenceMatcher(None, [t["sig"] for t in tmpl], [labs_nb.sig(c) for c in cells], autojunk=False).get_opcodes()
    for op, i1, i2, j1, j2 in ops:
        if op == "equal":
            at[j1:j2] = range(i1, i2)
        elif op == "replace":
            i = i1
            for j in range(j1, j2):
                k = next((k for k in range(i, i2) if tmpl[k]["kind"] == cells[j]["kind"]), None)
                if k is not None:
                    at[j], i = k, k + 1
    return at


def assign(cells: list[dict], tmpl: list[dict] | None) -> list[dict]:
    """Per student cell: {t, role, key, task, given}. Without a template the cell's own marks say what it is
    and nothing counts as given."""
    own = tmpl is None
    tmpl = labs_keys.keyed(cells) if own else tmpl
    at = list(range(len(cells))) if own else match(cells, tmpl)
    out, last = [], ""
    for c, t in zip(cells, at):
        tc = tmpl[t] if t is not None else None
        key = tc["key"] if tc else ""
        last = key or last
        out.append({"t": t, "role": tc["role"] if tc else "extra", "key": key, "task": key or (last if not tc else ""),
                    "given": not own and tc is not None and labs_nb.norm(c["source"]) == labs_nb.norm(tc["source"])})
    return out
