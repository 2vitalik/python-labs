"""Which task each cell of a lab notebook is (T354 §2): `1.3` — a step, `★2` — a star with its own conclusion,
`1.5` — a case's conclusion (the number of its prompt), `report`, `ai`; "" — the template's own text and code."""
import re

import labs_nb

PROMPT = re.compile(r"\*\*(\d+\.\d+)\.?\s*([^*]*?)\.?\*\*")  # **1.2. Перевірка бібліотекою.** — the prompt above a cell
CASE = re.compile(r"^##\s+\S+\s+(\d+)", re.M)  # ## Справа 2. …


def key_of(role: str, mark: str, prompt, case: int | None) -> tuple[str, str, int | None]:
    """(key, title, case) of a marked cell."""
    if role == "task":
        return mark, prompt[2] if prompt and prompt[1] == mark else "", int(mark.split(".")[0])
    if role == "star":
        return f"★{mark}", f"зірочка {mark}", int(mark)
    if role in ("report", "ai"):
        return role, mark, None
    if role == "conclusion" and (star := re.search(r"\d+", mark)):  # «Висновок зірочки 2» is the star's
        return f"★{star[0]}", mark, int(star[0])
    if role in ("conclusion", "note"):
        if prompt:
            return prompt[1], prompt[2], int(prompt[1].split(".")[0])
        return f"{case}:{mark}", mark, case
    return "", "", None


def keyed(cells: list[dict]) -> list[dict]:
    """{kind, sig, role, key, title, case, names, source} per cell."""
    out, case, prev = [], None, None
    for c in cells:
        role, mark = labs_nb.role(c)
        prompt = PROMPT.match(prev["source"].strip()) if prev and prev["kind"] != "code" else None
        key, title, at = key_of(role, mark, prompt, case)
        names = labs_nb.NAMES.findall(c["source"]) if role in ("task", "star") else []
        out.append({"kind": c["kind"], "sig": labs_nb.sig(c), "role": role, "key": key, "title": title, "case": at,
                    "names": names, "source": c["source"]})
        if c["kind"] != "code" and (m := CASE.search(c["source"])):
            case = int(m[1])
        prev = c
    return out


def tasks(cells: list[dict]) -> list[dict]:
    """The template's tasks in order: {key, role, case, title, plot, names}; a task's cells share its key."""
    out: dict[str, dict] = {}
    for c in cells:
        if c["key"]:
            t = out.setdefault(c["key"], {"key": c["key"], "role": c["role"], "case": c["case"], "title": "", "plot": False, "names": []})
            t["title"] = t["title"] or c["title"]
            t["names"] += [n for n in c["names"] if n not in t["names"]]
    return list(out.values())
