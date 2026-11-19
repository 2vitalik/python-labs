"""Invented notebooks of an invented lab for the smokes (T354): a template, its solved twin, a student's ones, marimo files.
Nothing here comes from the real labs."""
import base64
import json
import struct
import zlib

CARD = 'VARIANT = "{vid}"\nX = [1, 2,\n     3]'
LINE = 'print("LAB{lab}", VARIANT, *[f"{{k}}={{v:g}}" for k, v in ANSWERS.items()])'
HEAD = ("markdown", "# Лабораторна. Вигадана\n\n## Крок 0. Картка")
TEMPLATE = [HEAD, ("code", "# ✂ встав сюди свою картку"), ("code", 'def check(name, value):\n    print("✅", name, "=", value)'),
            ("markdown", "## Справа 1. Перша"), ("markdown", "**1.1. Порахуй.** Знайди x."), ("code", '# ✍ 1.1 порахуй x\ncheck("x", ...)'),
            ("markdown", "**1.2. Графік.** Намалюй."), ("code", "# ✍ 1.2 намалюй графік"),
            ("markdown", "**1.3. Висновок.** Що вийшло?"), ("markdown", "✍ *Висновок:* "),
            ("code", '# ✍ ★ зірочка 1: спробуй інше\ncheck("y", ...)'), ("markdown", "✍ *Висновок зірочки 1:* "),
            ("markdown", "## Рапорт"), ("markdown", "✍ *Рапорт:* "), ("markdown", "✍ *Про ШІ:* "), ("code", LINE.format(lab=9))]
WORDS = {9: "✍ *Висновок:* x вийшов рівно два, як і обіцяла формула.", 11: "✍ *Висновок зірочки 1:* інший шлях дав те саме число три.",
         13: "✍ *Рапорт:* усе пораховано, графік намальовано, висновки записано.", 14: "✍ *Про ШІ:* не користувався"}


def png() -> str:
    """A real 1×1 PNG, base64."""
    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))
    raw = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 0, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(b"\x00\x00")) + chunk(b"IEND", b"")
    return base64.b64encode(raw).decode()


def say(text: str) -> dict:
    return {"output_type": "stream", "name": "stdout", "text": text}


def picture() -> dict:
    return {"output_type": "display_data", "data": {"image/png": png(), "text/plain": "<Figure>"}, "metadata": {}}


HTML = {"output_type": "display_data", "data": {"text/html": "<script>alert(1)</script>"}, "metadata": {}}
ERROR = {"output_type": "error", "ename": "ZeroDivisionError", "evalue": "division by zero", "traceback": ["\x1b[31mTraceback\x1b[0m", "1/0"]}


def student(vid: str = "КН-1-01", lab: int = 9, line: str = "x=2 y=3", star_out=None) -> list:
    """(kind, source, outputs, count): every step done — 1.1 split in two cells, 1.2 without its `# ✍` mark."""
    code = [("code", CARD.format(vid=vid), [], 1), ("code", TEMPLATE[2][1], [], 2),
            ("code", "# ✍ 1.1 порахуй x\nx = 1 + 1", [say("\x1b[31mпроміжне\x1b[0m\n")], 3), ("code", 'check("x", x)', [say("✅ x = 2\n")], 4),
            ("code", "import matplotlib.pyplot as plt\nplt.plot([1, 2])\nplt.show()", [picture(), HTML], 5),
            ("code", '# ✍ ★ зірочка 1: спробуй інше\ny = 3\ncheck("y", y)', star_out or [say("✅ y = 3\n")], 6),
            ("code", LINE.format(lab=lab), [say(f"LAB{lab} {vid} {line}\n")] if line else [], 7)]
    t = TEMPLATE
    return [t[0], code[0], code[1], t[3], t[4], code[2], code[3], t[6], code[4], t[8], ("markdown", WORDS[9]), code[5],
            ("markdown", WORDS[11]), t[12], ("markdown", WORDS[13]), ("markdown", WORDS[14]), code[6]]


def solved() -> list:
    """The teacher's twin of the template: the star draws too — a star's picture is not a plot level 14 waits for."""
    cells = student("ДЕМО-00")
    cells[11] = ("code", cells[11][1] + "\nplt.show()", [picture()], 6)
    return cells


def notebook(cells: list, colab: bool = False) -> bytes:
    out = []
    for i, (kind, src, *rest) in enumerate(cells):
        c = {"cell_type": kind, "metadata": {}, "source": src.splitlines(keepends=True)}
        if kind == "code":
            outputs, count = (list(rest) + [[], None])[:2]
            c |= {"outputs": outputs, "execution_count": count}
            if colab and count:
                c["metadata"] = {"id": f"c{i}", "executionInfo": {"timestamp": 1_763_000_000_000 + i * 1000, "user": {"displayName": "x"}}}
        out.append(c)
    meta = {"kernelspec": {"name": "python3"}} | ({"colab": {"provenance": []}} if colab else {})
    return json.dumps({"cells": out, "metadata": meta, "nbformat": 4, "nbformat_minor": 4}, ensure_ascii=False).encode()


def marimo(cells: list) -> str:
    """marimo's own layout: a function per cell; a markdown cell is mo.md; the service cell's signature spans lines."""
    parts = ['import marimo\n\n__generated_with = "0.1"\napp = marimo.App()\n', "@app.cell\ndef _():\n    import marimo as mo\n    return (mo,)\n"]
    for kind, src, *_ in cells:
        body = "\n".join("    " + x if x.strip() else "" for x in src.split("\n"))
        if kind == "markdown":
            parts.append(f'@app.cell(hide_code=True)\ndef _(mo):\n    mo.md(r"""\n{body}\n    """)\n    return\n')
        elif "def check(" in src:
            parts.append(f"@app.cell\ndef _(\n    VARIANT,\n):\n{body}\n    return (check,)\n")
        else:
            parts.append(f"@app.cell\ndef _():\n{body}\n    return\n")
    parts.append('if __name__ == "__main__":\n    app.run()\n')
    return "\n\n".join(parts)
