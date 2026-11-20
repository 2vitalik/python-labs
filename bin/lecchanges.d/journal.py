"""The journal fixes/lecNN.md → its entries (contract §3.2.8–9): A — fixed errors (`Було` / `Стало` / `Чому певен` /
`Звідки помилка`), B — doubts (free text), G — restored from the slides, H — layout cases (§2). An entry is
`### NN-Xk · слайд(и) N[, M] · title`; one «перенесено в …» is left out, so is a section «Нічого»."""
import re

HEAD = re.compile(r"^### (\d{2}-([ABGH])\d+)\s*·\s*([^·]*?)\s*·\s*(.+?)\s*$")
FIELD = re.compile(r"(?:(?:\A|\n)- |\s·\s)\*\*([^*\n]+?):\*\*\s*")
LETTERS = {"A": "error", "B": "doubt", "G": "restored", "H": "layout"}


def entries(text: str) -> list[dict]:
    out, cur = [], None
    for line in text.splitlines():
        if line.startswith("#"):
            cur = None
            m = HEAD.match(line)
            if m and not m.group(4).startswith("перенесено"):
                cur = {"id": m.group(1), "letter": m.group(2), "slides": slides(m.group(3)), "title": m.group(4), "body": []}
                out.append(cur)
        elif cur is not None:
            cur["body"].append(line)
    for e in out:
        e["body"] = "\n".join(e["body"]).strip()
        e["fields"] = fields(e["body"])
    return out


def slides(text: str) -> list[int]:
    """«слайд 5», «слайди 16, 18», «слайди 3–5»."""
    out = []
    for a, b in re.findall(r"(\d+)(?:\s*[–-]\s*(\d+))?", text):
        out += list(range(int(a), int(b) + 1)) if b and int(b) - int(a) < 50 else [int(a)]
    return out


def fields(body: str) -> dict[str, str]:
    """`- **Name:** value` — a value runs to the next field, on its line (`· **Name:**`) or the lines below."""
    parts = FIELD.split(body)
    return {k.strip(): v.strip() for k, v in zip(parts[1::2], parts[2::2])}


def origin(text: str) -> str:
    """«на слайді так» — slide; the conversion — convert; the move to the site — site."""
    t = text.lower()
    if "перенесення на сайт" in t or t.startswith("сайт"):
        return "site"
    return "convert" if "конверт" in t and not t.startswith("на слайді") else "slide"


def importance(text: str) -> str:
    """H's «Важить: так | частково | ні» → open or noted."""
    return "noted" if re.match(r"\s*ні\b", text.lower()) else "open"
