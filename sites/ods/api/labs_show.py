"""A notebook for showing on the site (T354 §3, NOTEBOOK.cells): built from the stored file on request, never run."""
import labs_align
import labs_nb
import labs_out
from labs_facts import template


def cells(nb: dict, shape: dict | None) -> list[dict]:
    """{i, kind, source, role, key, task, given, h, count, out}: given — the template's cell untouched; h — to compare versions."""
    marks = labs_align.assign(nb["cells"], template(shape, nb["kind"]))
    return [{"i": i, "kind": c["kind"], "source": c["source"], "role": m["role"], "key": m["key"], "task": m["task"],
             "given": m["given"], "h": labs_nb.h(c), "count": c["count"],
             "out": [labs_out.show(o) for o in c["outputs"] if isinstance(o, dict)]}
            for i, (c, m) in enumerate(zip(nb["cells"], marks))]
