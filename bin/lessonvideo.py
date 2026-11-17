"""bin/lesson video (T335): the recording pieces of a day → Google Drive (rclone) and the group's Telegram topic (an
uploader bot over MTProto, tgvideo.py); the links → the parts on the site. What is not set up is skipped and said so;
--dry only tells what would go where. Settings — ~/.config/python-labs/video.env (outside Dropbox: it holds a bot's token):

  DRIVE=gdrive:Записи пар        rclone remote and folder; the folder is shared once by hand — the files inherit it
  DRIVE_PRIVATE=gdrive:Захисти   for parts with `only`: a folder nobody is given, each file gets a link of its own
  TG_API_ID=  TG_API_HASH=       my.telegram.org → API development tools
  TG_UPLOADER_TOKEN=             a bot of its own from @BotFather, an admin of the group (not the site's bot)
  TG_CHAT=-100…  TG_TOPIC=12     the group and its topic for recordings

A private part never goes to Telegram; a break and a part «поза заняттям» go nowhere."""
import json
import os
import subprocess
import sys
from pathlib import Path

import yaml

from siteapi import call

HOME = Path(os.environ.get("VIDEO_ENV", Path.home() / ".config" / "python-labs" / "video.env"))
KINDS = {"pz": "ПЗ", "def": "Захист", "lec": "Лекція", "cons": "Додатковий час", "x": "Запис"}


def settings() -> dict:
    lines = HOME.read_text().splitlines() if HOME.exists() else []
    return {k.strip(): v.strip() for k, v in (l.split("=", 1) for l in lines if "=" in l and not l.strip().startswith("#")) if v.strip()}


def rclone(*args: str) -> str:
    got = subprocess.run(["rclone", *args], capture_output=True, text=True)
    if got.returncode:
        sys.exit(f"rclone {args[0]}: {got.stderr.strip()[-300:]}")
    return got.stdout


def drive(file: Path, where: str, name: str, own_link: bool) -> str:
    """Upload and give the file's link: in a shared Drive folder — by its ID (the folder's access is the file's);
    elsewhere — a link made for this one file."""
    rclone("copyto", str(file), f"{where}/{name}", "--progress")
    kind = json.loads(rclone("config", "dump")).get(where.split(":")[0], {}).get("type")
    if own_link or kind != "drive":
        return rclone("link", f"{where}/{name}").strip()
    return f"https://drive.google.com/file/d/{json.loads(rclone('lsjson', f'{where}/{name}'))[0]['ID']}/view"


def telegram(file: Path, caption: str, cfg: dict) -> str:
    """tgvideo.py in an environment of its own (kurigram is not the site's dependency); it prints the message's link."""
    env = os.environ | {k: cfg[k] for k in ("TG_API_ID", "TG_API_HASH", "TG_UPLOADER_TOKEN", "TG_CHAT")} | {"TG_TOPIC": cfg.get("TG_TOPIC", "0")}
    got = subprocess.run(["uv", "run", "--no-project", "--isolated", "--with", "kurigram", "--with", "tgcrypto", "python",  # tgcrypto: the upload is many times faster
                          str(Path(__file__).with_name("tgvideo.py")), str(file), caption],
                         env=env, capture_output=True, text=True)
    if got.returncode:
        sys.exit(f"Telegram: {got.stderr.strip()[-400:]}")
    return got.stdout.strip().splitlines()[-1]


def publish(to: str, slug: str, folder: Path, dry: bool):
    cfg, manifest = settings(), folder / "pieces.yml"
    if not manifest.exists():
        sys.exit(f"нема {manifest} — спершу bin/lesson collect {slug}")
    cur = call(to, "GET", f"/lessons/{slug}")
    parts = {p["key"]: p for p in cur["parts"] if not p.get("site")}
    tg = all(cfg.get(k) for k in ("TG_API_ID", "TG_API_HASH", "TG_UPLOADER_TOKEN", "TG_CHAT"))
    print(f"{slug}: Drive — {cfg.get('DRIVE') or 'не налаштовано'} · приватне — {cfg.get('DRIVE_PRIVATE') or 'не налаштовано'} · Telegram — {'так' if tg else 'не налаштовано'} ({HOME})")
    day = f"{slug} {cur['title']}".strip().replace("/", "-").replace(":", " —")
    for n, piece in enumerate(yaml.safe_load(manifest.read_text()), 1):
        p, file = parts.get(piece["part"]), Path(piece["file"])
        if not p or p["kind"] in ("break", "off") or not file.exists():
            print(f"  {file.name}: пропущено — {'нема файла' if p and not file.exists() else 'перерва або поза заняттям' if p else 'нема частини заняття'}")
            continue
        title = f"{KINDS.get(p['kind'], 'Запис')} {piece['start'][:5].replace(':', '.')}–{piece['end'][:5].replace(':', '.')} {p['title']}".strip().replace("/", "-")
        where = cfg.get("DRIVE_PRIVATE" if p["only"] else "DRIVE")
        plan = [f"Drive → {where}/{'' if p['only'] else day + '/'}{n} {title}.mp4" if where else "", "" if p["only"] or not tg else "Telegram → топік"]
        print(f"  {file.name} · {file.stat().st_size // 2**20} МБ · {' · '.join(x for x in plan if x) or 'нікуди: нічого не налаштовано'}{' · приватна частина' if p['only'] else ''}")
        if dry:
            continue
        links = [drive(file, where if p["only"] else f"{where}/{day}", f"{n} {title}.mp4", bool(p["only"]))] if where else []
        if tg and not p["only"]:
            links.append(telegram(file, f"{slug} · {title}", cfg))
        p["links"] += [{"label": "", "url": u} for u in links if u not in [x["url"] for x in p["links"]]]
    if not dry:
        got = call(to, "PUT", f"/lessons/{slug}", {"rev": cur["rev"], "parts": list(parts.values()), "note": "відео частин"})
        print(f"{slug}: rev {got['rev']} · посилання на сайті — {sum(len(p['links']) for p in got['parts'])}")
