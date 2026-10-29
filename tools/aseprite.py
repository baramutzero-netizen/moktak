"""Minimal .aseprite writer (RGBA, multi-frame, tags, palette) + reader for verification.
Spec: https://github.com/aseprite/aseprite/blob/main/docs/ase-file-specs.md
"""
import struct, zlib
from PIL import Image


def _string(s):
    b = s.encode("utf-8")
    return struct.pack("<H", len(b)) + b


def _chunk(ctype, data):
    return struct.pack("<IH", len(data) + 6, ctype) + data


def write_aseprite(path, frames, durations=None, tags=None, palette=None,
                   layer_name="Layer 1", grid=16):
    """frames: list of PIL RGBA images (same size). tags: list of (name, from, to)."""
    w, h = frames[0].size
    durations = durations or [100] * len(frames)
    body = b""
    for i, im in enumerate(frames):
        im = im.convert("RGBA")
        chunks = []
        if i == 0:
            # color profile: sRGB
            chunks.append(_chunk(0x2007, struct.pack("<HHI", 1, 0, 0) + b"\0" * 8))
            if palette:
                n = len(palette)
                pd = struct.pack("<III", n, 0, n - 1) + b"\0" * 8
                for (r, g, b, a) in palette:
                    pd += struct.pack("<HBBBB", 0, r, g, b, a)
                chunks.append(_chunk(0x2019, pd))
            # layer
            ld = struct.pack("<HHHHHH", 3, 0, 0, 0, 0, 0) + struct.pack("<B", 255) + b"\0" * 3 + _string(layer_name)
            chunks.append(_chunk(0x2004, ld))
            if tags:
                td = struct.pack("<H", len(tags)) + b"\0" * 8
                for name, f, t in tags:
                    td += struct.pack("<HHBH", f, t, 0, 0) + b"\0" * 6 + b"\0\0\0" + b"\0" + _string(name)
                chunks.append(_chunk(0x2018, td))
        # cel (compressed image)
        raw = im.tobytes()
        cd = struct.pack("<HhhBHh", 0, 0, 0, 255, 2, 0) + b"\0" * 5 + struct.pack("<HH", w, h) + zlib.compress(raw, 9)
        chunks.append(_chunk(0x2005, cd))
        cbytes = b"".join(chunks)
        n = len(chunks)
        fh = struct.pack("<IHHH", 16 + len(cbytes), 0xF1FA, n if n < 0xFFFF else 0xFFFF, durations[i]) + b"\0\0" + struct.pack("<I", n)
        body += fh + cbytes
    header = struct.pack("<IHHHHHIH", 128 + len(body), 0xA5E0, len(frames), w, h, 32, 1, 100)
    header += struct.pack("<II", 0, 0) + struct.pack("<B", 0) + b"\0" * 3
    header += struct.pack("<H", len(palette) if palette else 0)
    header += struct.pack("<BB", 1, 1)
    header += struct.pack("<hhHH", 0, 0, grid, grid)
    header += b"\0" * 84
    assert len(header) == 128
    with open(path, "wb") as f:
        f.write(header + body)


def read_aseprite(path):
    """Returns (frames as PIL images, tags) — enough to verify our own files."""
    d = open(path, "rb").read()
    size, magic, nframes, w, h, depth = struct.unpack_from("<IHHHHH", d, 0)
    assert magic == 0xA5E0 and size == len(d) and depth == 32
    off = 128
    frames, tags = [], []
    for _ in range(nframes):
        fsize, fmagic, old_n, dur = struct.unpack_from("<IHHH", d, off)
        assert fmagic == 0xF1FA
        n = struct.unpack_from("<I", d, off + 12)[0] or old_n
        p = off + 16
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        for _ in range(n):
            csize, ctype = struct.unpack_from("<IH", d, p)
            data = d[p + 6:p + csize]
            if ctype == 0x2005:
                li, x, y, op, ct, z = struct.unpack_from("<HhhBHh", data, 0)
                cw, ch = struct.unpack_from("<HH", data, 16)
                assert ct == 2
                px = zlib.decompress(data[20:])
                assert len(px) == cw * ch * 4
                img.paste(Image.frombytes("RGBA", (cw, ch), px), (x, y))
            elif ctype == 0x2018:
                nt = struct.unpack_from("<H", data, 0)[0]
                q = 10
                for _ in range(nt):
                    f, t = struct.unpack_from("<HH", data, q)
                    q += 17
                    ln = struct.unpack_from("<H", data, q)[0]
                    tags.append((data[q + 2:q + 2 + ln].decode(), f, t))
                    q += 2 + ln
            p += csize
        assert p == off + fsize
        frames.append(img)
        off += fsize
    assert off == len(d)
    return frames, tags
