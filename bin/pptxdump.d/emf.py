"""Text strings drawn by an EMF picture (EMR_EXTTEXTOUTW records), in drawing order."""
import struct


def emf_text(d):
    out, off = [], 0
    while off + 8 <= len(d):
        typ, size = struct.unpack_from("<II", d, off)
        if size < 8:
            break
        if typ == 84 and size >= 76:  # EMR_EXTTEXTOUTW
            n, offs = struct.unpack_from("<II", d, off + 44)
            s = d[off + offs: off + offs + 2 * n].decode("utf-16-le", "replace")
            if s.strip():
                out.append(s)
        off += size
    return out
