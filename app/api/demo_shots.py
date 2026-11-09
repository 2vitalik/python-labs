"""A screenshot for a demo game (demo_io.py): an ASCII map drawn as a field of squares, one character — one cell."""
import colorsys
import struct
import zlib

BASE = {".": "ece8d9", " ": "f8f6ef", "#": "44475a"}  # floor, nothing, wall; any other character gets a hue of its own
GRID = bytes.fromhex("d3cebd")


def colour(ch: str) -> bytes:
    if ch in BASE:
        return bytes.fromhex(BASE[ch])
    rgb = colorsys.hls_to_rgb(ord(ch) * 47 % 360 / 360, .55, .6)
    return bytes(int(x * 255) for x in rgb)


def chunk(tag: bytes, data: bytes) -> bytes:
    return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data))


def png(rows: list[str], cell: int = 16) -> bytes:
    width = max(map(len, rows))
    lines = []
    for row in rows:
        body = b"".join(colour(ch) * (cell - 1) + GRID for ch in row.ljust(width))
        lines += [b"\0" + body] * (cell - 1) + [b"\0" + GRID * width * cell]
    head = struct.pack(">IIBBBBB", width * cell, len(rows) * cell, 8, 2, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", head) + chunk(b"IDAT", zlib.compress(b"".join(lines))) + chunk(b"IEND", b"")
