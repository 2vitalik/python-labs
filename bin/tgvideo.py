"""A video into the group's Telegram topic by an uploader bot over MTProto (T335): the cloud Bot API takes 50 MB, a bot
that speaks MTProto itself — about 2000 MiB. Run by lessonvideo.py in its own environment:

  uv run --no-project --with kurigram python bin/tgvideo.py <file.mp4> "<caption>"

Reads TG_API_ID, TG_API_HASH, TG_UPLOADER_TOKEN, TG_CHAT, TG_TOPIC from the environment; the session lives in
~/.config/python-labs (outside Dropbox). The last line it prints is the message's link."""
import asyncio
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from pyrogram import Client  # the package is kurigram

WORK = Path.home() / ".config" / "python-labs"


def probe(file: Path) -> dict:
    got = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height:format=duration", "-of", "json", str(file)],
                         capture_output=True, text=True, check=True)
    data = json.loads(got.stdout)
    return {"duration": round(float(data["format"]["duration"])), **{k: data["streams"][0][k] for k in ("width", "height")}}


async def main(file: Path, caption: str):
    WORK.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        fast, thumb = Path(tmp) / "video.mp4", Path(tmp) / "thumb.jpg"
        # the index goes to the head of the file — the video plays before it is downloaded; no re-encoding
        subprocess.run(["ffmpeg", "-v", "error", "-i", str(file), "-c", "copy", "-movflags", "+faststart", str(fast)], check=True)
        subprocess.run(["ffmpeg", "-v", "error", "-ss", "5", "-i", str(file), "-frames:v", "1", "-vf", "scale=320:-2", str(thumb)], check=True)
        app = Client("uploader", api_id=int(os.environ["TG_API_ID"]), api_hash=os.environ["TG_API_HASH"],
                     bot_token=os.environ["TG_UPLOADER_TOKEN"], workdir=str(WORK), no_updates=True)
        async with app:
            topic = int(os.environ.get("TG_TOPIC") or 0)
            msg = await app.send_video(int(os.environ["TG_CHAT"]), str(fast), caption=caption, thumb=str(thumb), supports_streaming=True,
                                       **({"message_thread_id": topic} if topic else {}), **probe(file),
                                       progress=lambda done, total: print(f"\r{done * 100 // total} %", end="", file=sys.stderr))
            print(msg.link)


if __name__ == "__main__":
    asyncio.run(main(Path(sys.argv[1]), sys.argv[2]))
