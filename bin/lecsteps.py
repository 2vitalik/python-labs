"""A lecture as the site's history wants it (T381): the versions of its text from the lectures' own git
(sites/ods/data/lectures — outside the project's), oldest first. The first is the text as it came from the lecturer's
slides, before any proof-reading; every commit that changed the text is a version with the commit's words and time."""
import re
import subprocess
from datetime import datetime, timedelta

import content_disk as disk

FIRST = "текст із презентації лектора, до вичитки"


def git(root, *args) -> str:
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, check=True).stdout


def steps(p: dict) -> list[dict]:
    """[{title, body, note, at}] by git; [] — the folder has no git or no commit of this file."""
    root = p["file"].parents[1]
    rel = p["file"].relative_to(root).as_posix()
    try:
        log = git(root, "log", "--reverse", "--format=%H%x09%cI%x09%s", "--", rel).splitlines()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []
    out = []
    for commit, at, subject in (line.split("\t", 2) for line in log):
        title, body, _ = disk.read(p["slug"], git(root, "show", f"{commit}:{rel}"))
        if out and (out[-1]["title"], out[-1]["body"]) == (title, body):
            continue  # the commit touched what is not the page: the converter's line, a picture's name
        at = datetime.fromisoformat(at)
        if out and at <= out[-1]["at"]:
            at = out[-1]["at"] + timedelta(seconds=1)  # two commits of one second: the history sorts by time
        out.append({"title": title, "body": body, "note": re.sub(rf"^{p['slug']}:\s*", "", subject) if out else FIRST, "at": at})
    return out


def unseen(p: dict, seen: str | None, title: str, body: str, sha, anew: bool = False) -> list[dict]:
    """What the site is to get: git's versions after the one it holds, then the disk's text when git has not got it yet.
    `seen` — sha1 of the site's text, None — no such page. A text git does not know (written on the site) gets the disk's
    text alone over it; `anew` — the whole history over it, from the lecturer's text."""
    every = steps(p)
    if not every or (every[-1]["title"], every[-1]["body"]) != (title, body):
        every.append({"title": title, "body": body, "note": "", "at": None})
    shas = [sha(f"{v['title']}\n{v['body']}".encode()) for v in every]
    if seen not in shas:
        return every if seen is None or anew else every[-1:]
    at = len(shas) - 1 - shas[::-1].index(seen)
    rest = every[at + 1:]
    if rest and at == 0:
        rest[0] = rest[0] | {"under": FIRST}  # the site holds the lecturer's text: its history is to say so
    return rest
