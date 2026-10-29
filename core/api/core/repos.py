"""Student repositories on disk (T235): clone or fetch one, read its log, cut it at a moment. Plain subprocess git and the
standard library only — bin/repos runs this with the system python, the server will run the same."""
import os
import re
import subprocess
from pathlib import Path

GITHUB = re.compile(r"^https://github\.com/([\w.-]+)/([\w.-]+?)(?:\.git)?/?$")
STAT = re.compile(r"(\d+) files? changed(?:, (\d+) insertions?\(\+\))?(?:, (\d+) deletions?\(-\))?")
OFFLINE, TIMEOUT, EMPTY = "нема звʼязку з GitHub", "git не відповів за 3 хвилини", "репозиторій порожній: жодного коміту"
TRANSIENT = {OFFLINE, TIMEOUT}  # this machine's trouble, not the student's: says nothing about access
REASONS = (("Repository not found", "репозиторій не знайдено або нема доступу"), ("Permission denied", "GitHub не прийняв SSH-ключ"),
           ("Could not resolve host", OFFLINE), ("Network is unreachable", OFFLINE), ("Connection timed out", OFFLINE),
           ("Cannot determine remote HEAD", EMPTY), ("invalid reference", EMPTY))
SEP, REC = "\x1f", "\x1e"


def ssh_url(url: str) -> str:
    m = GITHUB.match(url.strip())
    return f"git@github.com:{m[1]}/{m[2]}.git" if m else url


def git(*args: str, cwd: Path | None = None, timeout: int = 180) -> subprocess.CompletedProcess:
    env = {**os.environ, "GIT_TERMINAL_PROMPT": "0", "GIT_SSH_COMMAND": "ssh -o BatchMode=yes"}  # never wait for a password
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, timeout=timeout, env=env)


def reason(stderr: str) -> str:
    text = stderr.strip()
    return next((why for key, why in REASONS if key in text), text.splitlines()[-1][:200] if text else "git: невідома помилка")


def pull(url: str, folder: Path) -> str:
    """Clone into an empty folder or fetch; the work tree ends detached at origin's default branch. "" or why it failed."""
    try:
        if not (folder / ".git").exists():
            r = git("clone", "-q", ssh_url(url), str(folder))
        else:
            if git("remote", "get-url", "origin", cwd=folder).stdout.strip() != ssh_url(url):
                git("remote", "set-url", "origin", ssh_url(url), cwd=folder)  # the student renamed or moved it
            r = git("fetch", "-q", "--prune", "origin", cwd=folder)
        if r.returncode == 0:
            r = git("remote", "set-head", "origin", "-a", cwd=folder)  # fails only when there is no branch yet
        if r.returncode == 0:
            r = git("checkout", "-q", "--force", "--detach", "origin/HEAD", cwd=folder)
    except subprocess.TimeoutExpired:
        return TIMEOUT
    return "" if r.returncode == 0 else reason(r.stderr)


def head(folder: Path) -> tuple[str, str]:
    """(branch, sha) of origin's default branch; ("", "") in an empty repository."""
    branch = git("symbolic-ref", "-q", "--short", "refs/remotes/origin/HEAD", cwd=folder).stdout.strip().removeprefix("origin/")
    return branch, git("rev-parse", "-q", "--verify", "origin/HEAD", cwd=folder).stdout.strip()


def log(folder: Path) -> list[dict]:
    """Every commit of the default branch, newest first: when (committer, author), who, the first line, how big."""
    r = git("log", "origin/HEAD", f"--format={REC}%H{SEP}%cI{SEP}%aI{SEP}%an{SEP}%s", "--shortstat", cwd=folder)
    out = []
    for block in r.stdout.split(REC)[1:]:
        line, _, stat = block.strip("\n").partition("\n")
        sha, at, authored, author, msg = line.split(SEP, 4)
        m = STAT.search(stat)  # a merge has no stat line
        out.append({"sha": sha, "at": at, "authored": authored if authored != at else None, "author": author, "msg": msg[:120],
                    "files": int(m[1]) if m else 0, "add": int(m[2] or 0) if m else 0, "rm": int(m[3] or 0) if m else 0})
    return out


def cut(folder: Path, before: str) -> str:
    """The last commit of the default branch at or before the moment (ISO), by the committer's clock; "" when none."""
    return git("rev-list", "-1", f"--before={before}", "origin/HEAD", cwd=folder).stdout.strip()


def checkout(folder: Path, sha: str, dest: Path) -> str:
    """A second work tree at that commit — what a review reads. "" or the error."""
    if (dest / ".git").exists():  # a work tree's .git is a file
        r = git("checkout", "-q", "--force", "--detach", sha, cwd=dest)
    else:
        dest.parent.mkdir(parents=True, exist_ok=True)
        r = git("worktree", "add", "-f", "--detach", str(dest), sha, cwd=folder)
    return "" if r.returncode == 0 else reason(r.stderr)
