"""A marimo notebook (.py) read by `ast` only — a student's file is never imported or run.
A cell is a function under @app.cell: its body without the closing `return`; a lone `mo.md(…)` is a markdown cell."""
import ast
import textwrap

CUT = "# ✂"


def is_marimo(text: str) -> bool:
    return "import marimo" in text and "marimo.App(" in text


def is_cell(d: ast.expr) -> bool:
    f = d.func if isinstance(d, ast.Call) else d
    return isinstance(f, ast.Attribute) and f.attr == "cell"


def body_lines(node: ast.FunctionDef, lines: list[str]) -> list[str]:
    """From the line after `def …:` (comments before the first statement count) to the closing `return`."""
    depth, start = 0, node.lineno - 1
    for start in range(node.lineno - 1, node.end_lineno):  # a long signature spans lines: `def _(\n    a,\n):`
        depth += lines[start].count("(") - lines[start].count(")")
        if depth <= 0 and lines[start].rstrip().endswith(":"):
            break
    last = node.body[-1]
    end = last.lineno - 1 if isinstance(last, ast.Return) else node.end_lineno
    return lines[start + 1:end]


def markdown(node: ast.FunctionDef) -> str | None:
    """The text of `mo.md(r\"\"\"…\"\"\")`, the cell's only statement besides `return`."""
    body = [s for s in node.body if not isinstance(s, ast.Return)]
    if len(body) != 1 or not isinstance(body[0], ast.Expr) or not isinstance(call := body[0].value, ast.Call):
        return None
    f = call.func
    if isinstance(f, ast.Attribute) and f.attr == "md" and call.args and isinstance(arg := call.args[0], ast.Constant) \
            and isinstance(arg.value, str):
        return textwrap.dedent(arg.value).strip("\n")
    return None


def cells(text: str) -> list[dict]:
    """ValueError when this is not Python at all."""
    try:
        tree = ast.parse(text)
    except SyntaxError as e:
        raise ValueError(f"Файл marimo не читається як Python: рядок {e.lineno}") from None
    except (ValueError, RecursionError, MemoryError):
        raise ValueError("Файл marimo не читається як Python") from None
    lines, out = text.split("\n"), []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and any(map(is_cell, node.decorator_list)):
            md = markdown(node)
            source = md if md is not None else textwrap.dedent("\n".join(body_lines(node, lines))).strip("\n")
            out.append({"kind": "markdown" if md is not None else "code", "source": source, "outputs": [], "count": None, "meta": {}})
    return out


def paste(text: str, card: list[str]) -> str:
    """The card in place of the template's `# ✂` line, at that line's indentation: marimo reads the cell's names off its body."""
    lines = text.split("\n")
    i = next((i for i, line in enumerate(lines) if line.lstrip().startswith(CUT)), None)
    if i is None:
        raise ValueError("no `# ✂` line in the template")
    pad = lines[i][:len(lines[i]) - len(lines[i].lstrip())]
    lines[i:i + 1] = [pad + line if line.strip() else "" for line in card]
    return "\n".join(lines)
