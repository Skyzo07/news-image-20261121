#!/usr/bin/env python3
"""Deliver the news-image-20261121 front page.

The picture itself is baked into the repository as entry.png (rendered
ahead of time by render.py). All this script does is carry that file,
byte for byte, into the directory the harness points at with
MAKEFUN_OUTPUT_DIR, checking the bytes on both sides of the move.

Standard library only, no network, no randomness: the same input file
always produces the same output file.
"""

import binascii
import hashlib
import hmac
import os
import struct
import sys

# The harness contract for this bounty.
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
SIZE_LIMIT = 1_048_576  # 1 MiB
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
SOURCE_NAME = "entry.png"


def fail(reason):
    """Abort with a message the harness can show, and a nonzero status."""
    print(f"main.py: FAILED: {reason}", file=sys.stderr)
    raise SystemExit(1)


def read_source():
    """Load the repo-side image, rejecting anything that is not our PNG."""
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, SOURCE_NAME)
    try:
        with open(path, "rb") as handle:
            blob = handle.read()
    except OSError as exc:
        fail(f"cannot read {SOURCE_NAME}: {exc}")
    check_size(blob, SOURCE_NAME)
    check_signature(blob, SOURCE_NAME)
    check_dimensions(blob, SOURCE_NAME)
    check_ihdr_crc(blob, SOURCE_NAME)
    check_trailer(blob, SOURCE_NAME)
    return blob


def check_ihdr_crc(blob, label):
    """The IHDR chunk ends with a CRC over its type name + data.

    A wrong CRC means the header bytes were damaged in transit, even if
    the dimensions still happen to read as 1024x1024.
    """
    chunk_type_and_data = blob[12:29]  # "IHDR" + 13 data bytes
    (stored_crc,) = struct.unpack(">I", blob[29:33])
    computed = binascii.crc32(chunk_type_and_data) & 0xFFFFFFFF
    if computed != stored_crc:
        fail(
            f"{label} IHDR CRC mismatch: "
            f"stored {stored_crc:#010x}, computed {computed:#010x}"
        )


def check_trailer(blob, label):
    """A well-formed PNG ends with a zero-length IEND chunk.

    The last 12 bytes must be: length 0, the letters IEND, and the CRC
    of the letters IEND (0xAE426082). Anything else means the file was
    cut short or had junk appended.
    """
    if len(blob) < 12:
        fail(f"{label} is too short to hold an IEND chunk")
    tail = blob[-12:]
    length, chunk_type = struct.unpack(">I4s", tail[:8])
    (stored_crc,) = struct.unpack(">I", tail[8:12])
    expected_crc = binascii.crc32(b"IEND") & 0xFFFFFFFF
    if length != 0 or chunk_type != b"IEND" or stored_crc != expected_crc:
        fail(f"{label} is missing a valid IEND trailer")


def check_size(blob, label):
    if len(blob) > SIZE_LIMIT:
        fail(f"{label} is {len(blob)} bytes, over the {SIZE_LIMIT} byte cap")


def check_signature(blob, label):
    if blob[: len(PNG_SIGNATURE)] != PNG_SIGNATURE:
        fail(f"{label} does not start with the PNG signature")


def check_dimensions(blob, label):
    # The IHDR chunk starts right after the 8-byte signature: 4 bytes of
    # length, 4 bytes spelling "IHDR", then width and height as big-endian.
    if len(blob) < 33:
        fail(f"{label} is too short to hold an IHDR chunk")
    if blob[12:16] != b"IHDR":
        fail(f"{label} has no IHDR chunk where one belongs")
    width, height = struct.unpack(">II", blob[16:24])
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        fail(
            f"{label} is {width}x{height}, "
            f"expected {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}"
        )


def digest(blob):
    return hashlib.sha256(blob).hexdigest()


def run():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    blob = read_source()
    before = digest(blob)
    os.makedirs(out_dir, exist_ok=True)
    destination = os.path.join(out_dir, SOURCE_NAME)
    try:
        with open(destination, "wb") as handle:
            handle.write(blob)
        with open(destination, "rb") as handle:
            written = handle.read()
    except OSError as exc:
        fail(f"cannot write {destination}: {exc}")
    check_size(written, "output entry.png")
    check_signature(written, "output entry.png")
    check_dimensions(written, "output entry.png")
    check_ihdr_crc(written, "output entry.png")
    check_trailer(written, "output entry.png")
    after = digest(written)
    if not hmac.compare_digest(after, before):
        fail(
            "output sha256 does not match the source file "
            f"({after} != {before})"
        )
    print(
        f"entry.png delivered: {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}, "
        f"{len(written)} bytes, sha256 {after}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
