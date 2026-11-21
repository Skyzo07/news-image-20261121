# main.py — news-image-20261121 entrypoint (Python 3.13, stdlib only).
# Copies the repository's pre-rendered entry.png to $MAKEFUN_OUTPUT_DIR
# and validates it before and after the copy. No network, deterministic:
# the output bytes are exactly the repository file's bytes.
import hashlib
import os
import struct
import sys

MAX_BYTES = 1048576
EXPECTED_W, EXPECTED_H = 1024, 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def validate(data, where):
    if len(data) > MAX_BYTES:
        raise SystemExit(f"{where}: {len(data)} bytes exceeds 1 MiB cap")
    if not data.startswith(PNG_MAGIC):
        raise SystemExit(f"{where}: not a PNG (bad magic)")
    if len(data) < 24:
        raise SystemExit(f"{where}: file too short for an IHDR")
    w, h = struct.unpack(">II", data[16:24])
    if (w, h) != (EXPECTED_W, EXPECTED_H):
        raise SystemExit(f"{where}: size {w}x{h}, expected 1024x1024")
    return hashlib.sha256(data).hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        raise SystemExit("MAKEFUN_OUTPUT_DIR is not set")
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    with open(src, "rb") as f:
        data = f.read()
    src_sha = validate(data, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        out_data = f.read()
    out_sha = validate(out_data, "output entry.png")
    if out_sha != src_sha:
        raise SystemExit("post-copy sha256 mismatch")
    print(f"entry.png: {len(data)} bytes, sha256 {out_sha}")


if __name__ == "__main__":
    main()
