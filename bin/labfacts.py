"""Facts of a student's lab, measured rather than judged (T254): the code in a work tree — files, lines, functions, what it imports,
the syntax lab 1's extra tasks name, junk committed — and the shape of the commit log around the cut. Standard library only and
nothing of the student's runs: `ast.parse` reads the code, git is asked for the log. bin/repos facts writes it as lab<N>.facts.json."""
import ast
import builtins
import re
import subprocess
from collections import Counter
from datetime import datetime
from itertools import pairwise
from pathlib import Path

JUNK = {"venv", ".venv", "env", "__pycache__", ".idea", ".vscode", "node_modules", ".DS_Store", ".pytest_cache", "site-packages", "dist", "build"}
UI = {"pygame": "pygame", "arcade": "arcade", "tkinter": "tkinter", "curses": "curses", "pyxel": "pyxel", "turtle": "turtle", "rich": "rich"}
KEYS = ("msvcrt", "keyboard", "curses", "pynput", "getch", "readchar", "termios", "getkey", "sshkeyboard")
BUILTINS = set(dir(builtins)) - {"print", "input", "range"}  # the lab names these three itself
SYNTAX = ("str", "int", "float", "bool", "none", "elif", "else", "and", "or", "not", "chain", "for", "while", "range", "continue", "break",
          "loop_else", "kwdefault", "star", "slash", "lambda", "nested", "global", "nonlocal", "fstring", "input", "main_guard", "classes")
GENERIC = {"update", "upd", "fix", "fixes", "commit", "add", "init", "initial commit", "first commit", "lab1", "lab 1", "lab", "test", "changes",
           "upload", "add files via upload", "create", "new", "done", "final", "main", "code", "updated", "update main.py", "create main.py"}
SESSION_GAP = 2 * 3600  # seconds of silence that end a sitting at the keyboard


class Syntax(ast.NodeVisitor):
    """What lab 1's extra tasks name, counted over the modules of one tree."""

    def __init__(self):
        self.n, self.builtins, self.imports, self.names, self.depth = Counter(), set(), set(), [], 0

    def visit_Constant(self, node):
        v = node.value
        key = "bool" if isinstance(v, bool) else "none" if v is None else type(v).__name__ if isinstance(v, (str, int, float)) else ""
        self.n[key] += bool(key)

    def visit_If(self, node):
        t = node.test
        if isinstance(t, ast.Compare) and isinstance(t.left, ast.Name) and t.left.id == "__name__":
            self.n["main_guard"] += 1
        if node.orelse:
            self.n["elif" if len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If) else "else"] += 1
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        self.n["and" if isinstance(node.op, ast.And) else "or"] += 1
        self.generic_visit(node)

    def visit_UnaryOp(self, node):
        self.n["not"] += isinstance(node.op, ast.Not)
        self.generic_visit(node)

    def visit_Compare(self, node):
        self.n["chain"] += len(node.ops) > 1
        self.generic_visit(node)

    def loop(self, kind, node):
        self.n[kind] += 1
        self.n["loop_else"] += bool(node.orelse)
        self.generic_visit(node)

    visit_For = lambda self, node: self.loop("for", node)
    visit_While = lambda self, node: self.loop("while", node)

    def visit_Continue(self, node): self.n["continue"] += 1  # noqa: E704
    def visit_Break(self, node): self.n["break"] += 1  # noqa: E704
    def visit_Global(self, node): self.n["global"] += 1  # noqa: E704
    def visit_Nonlocal(self, node): self.n["nonlocal"] += 1  # noqa: E704

    def visit_Lambda(self, node):
        self.n["lambda"] += 1
        self.generic_visit(node)

    def visit_JoinedStr(self, node):
        self.n["fstring"] += 1
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.n["classes"] += 1
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        a = node.args
        self.n["functions"] += 1
        self.n["nested"] += self.depth > 0
        self.n["kwdefault"] += bool(a.defaults or any(a.kw_defaults))
        self.n["star"] += bool(a.kwonlyargs or a.vararg)
        self.n["slash"] += bool(a.posonlyargs)
        self.names.append(node.name)
        self.depth += 1
        self.generic_visit(node)
        self.depth -= 1

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            name = node.func.id
            if name in BUILTINS:
                self.builtins.add(name)
            elif name in ("input", "range", "print"):
                self.n[name] += 1
        self.generic_visit(node)

    def visit_Import(self, node):
        self.imports |= {a.name.split(".")[0] for a in node.names}

    def visit_ImportFrom(self, node):
        if node.module:
            self.imports.add(node.module.split(".")[0])


def code(tree: Path) -> dict:
    """The code of one work tree: what is there and what syntax it uses; junk is listed, not read."""
    files = [p for p in tree.rglob("*") if p.is_file() and ".git" not in p.parts]
    junk = sorted({part for p in files for part in p.relative_to(tree).parts if part in JUNK or part.endswith(".pyc")})
    py = [p for p in files if p.suffix == ".py" and not set(p.relative_to(tree).parts) & JUNK and p.stat().st_size < 1_000_000]
    s, lines, broken = Syntax(), {}, []
    for p in py:
        rel, text = str(p.relative_to(tree)), p.read_text(encoding="utf-8", errors="replace")
        lines[rel] = sum(1 for line in text.splitlines() if line.strip())
        try:
            s.visit(ast.parse(text))
        except (SyntaxError, ValueError) as e:
            broken.append(f"{rel}:{getattr(e, 'lineno', '?')}")
    others = Counter(p.suffix or p.name for p in files if p.suffix != ".py" and not set(p.relative_to(tree).parts) & JUNK)
    return {"files": len(files), "py_files": len(py), "py_lines": sum(lines.values()), "by_file": dict(sorted(lines.items(), key=lambda kv: -kv[1])[:15]),
            "functions": s.n["functions"], "names": s.names[:60], "imports": sorted(s.imports),
            "ui": next((UI[m] for m in UI if m in s.imports), "console"), "keys": sorted(k for k in KEYS if k in s.imports) + (["input"] if s.n["input"] else []),
            "syntax": {k: s.n[k] for k in SYNTAX}, "builtins": sorted(s.builtins), "broken": broken, "junk": junk,
            "readme": any(p.name.lower().startswith("readme") for p in files), "tests": any("test" in p.name.lower() for p in py),
            "gitignore": (tree / ".gitignore").exists(), "requirements": any(p.name in ("requirements.txt", "pyproject.toml", "Pipfile") for p in files),
            "others": dict(others.most_common(8))}


def run(cwd: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=False).stdout


def history(clone: Path, cut: str) -> dict:
    """The shape of the default branch's log: how many sittings, how big the biggest commit, whose clock, what the messages say."""
    rows = []
    for block in run(clone, "log", "origin/HEAD", "--format=%x1e%H%x1f%cI%x1f%aI%x1f%an%x1f%cn%x1f%ce%x1f%P%x1f%s", "--shortstat").split("\x1e")[1:]:
        line, _, stat = block.strip("\n").partition("\n")
        sha, at, authored, author, committer, email, parents, msg = line.split("\x1f", 7)
        add = int(m[1]) if (m := re.search(r"(\d+) insertions?", stat)) else 0
        rows.append({"sha": sha, "at": datetime.fromisoformat(at), "authored": datetime.fromisoformat(authored), "author": author, "committer": committer,
                     "email": email, "merge": len(parents.split()) > 1, "msg": msg.strip(), "add": add})
    rows.sort(key=lambda r: r["at"])
    before = set(run(clone, "rev-list", cut).split()) if cut else set()
    gaps = [(b["at"] - a["at"]).total_seconds() for a, b in pairwise(rows)]
    msgs = [r["msg"].lower().strip(" .!") for r in rows]
    total_add = sum(r["add"] for r in rows) or 1
    return {"commits": len(rows), "before": sum(r["sha"] in before for r in rows), "after": sum(r["sha"] not in before for r in rows),
            "first": rows[0]["at"].isoformat() if rows else None, "last": rows[-1]["at"].isoformat() if rows else None,
            "span_h": round((rows[-1]["at"] - rows[0]["at"]).total_seconds() / 3600, 1) if rows else 0,
            "sessions": 1 + sum(g > SESSION_GAP for g in gaps) if rows else 0, "max_in_10min": max((sum(1 for b in rows if 0 <= (b["at"] - a["at"]).total_seconds() <= 600) for a in rows), default=0),
            "largest_share": round(max((r["add"] for r in rows), default=0) / total_add, 2), "median_add": sorted(r["add"] for r in rows)[len(rows) // 2] if rows else 0,
            "author_ne_committer": sum(r["authored"] != r["at"] for r in rows), "tz": sorted({r["at"].isoformat()[-6:] for r in rows}),
            "web_commits": sum(r["email"].endswith("noreply@github.com") for r in rows), "merges": sum(r["merge"] for r in rows),
            "authors": sorted({r["author"] for r in rows}), "generic_msgs": sum(m in GENERIC or len(m) < 4 for m in msgs), "dup_msgs": len(msgs) - len(set(msgs)),
            "tags": len(run(clone, "tag").split()), "branch": run(clone, "symbolic-ref", "-q", "--short", "refs/remotes/origin/HEAD").strip().removeprefix("origin/"),
            "other_branches": branches(clone)}


def branches(clone: Path) -> dict:
    """Remote branches besides the default one → commits of theirs that the default branch does not have: work the facts would otherwise miss."""
    skip = {"", "refs/remotes/origin/HEAD", run(clone, "symbolic-ref", "-q", "refs/remotes/origin/HEAD").strip()}
    names = [b.strip() for b in run(clone, "branch", "-r", "--format=%(refname)").splitlines() if b.strip() not in skip]
    return {n.removeprefix("refs/remotes/origin/"): len(run(clone, "rev-list", n, "^origin/HEAD").split()) for n in names}


def measure(tree: Path, clone: Path, cut: str, head: str) -> dict:
    """Everything about one student × one lab that a script can see. `tree` is the cut's work tree, or the clone when nothing was committed before the deadline."""
    at = lambda sha: run(clone, "show", "-s", "--format=%cI", sha).strip() if sha else None
    return {"cut": {"sha": cut, "at": at(cut)}, "head": {"sha": head, "at": at(head)}, "code_at": "cut" if cut else "head",
            "measured": datetime.now().astimezone().isoformat(timespec="seconds"), "code": code(tree), "git": history(clone, cut)}
