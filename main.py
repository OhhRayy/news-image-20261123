"""News-image entry runner for 23 Nov 2026.

The finished picture already lives in this repo as entry.png.
This script's only job is to place an exact copy of it where the
judge expects the output: /output/entry.png.

No network, no randomness, no extra dependencies — just the
standard library, so the result is byte-for-byte identical on
every run.
"""

import hashlib
import os
import shutil
import sys

SOURCE_NAME = "entry.png"
DEST_DIR = "/output"
DEST_NAME = "entry.png"


def locate_picture():
    """Return the absolute path of the picture bundled with this repo."""
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, SOURCE_NAME)


def make_destination_folder():
    """Create /output when it is missing and return its path."""
    os.makedirs(DEST_DIR, exist_ok=True)
    return DEST_DIR


def fingerprint(path):
    """Compute the SHA-256 hex digest of a file, chunk by chunk."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            block = handle.read(65536)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def place_picture():
    """Copy the bundled picture into /output and report both hashes."""
    origin = locate_picture()
    if not os.path.isfile(origin):
        print("entry.png tidak ditemukan di folder repo", file=sys.stderr)
        return 1
    folder = make_destination_folder()
    target = os.path.join(folder, DEST_NAME)
    shutil.copyfile(origin, target)
    source_hash = fingerprint(origin)
    target_hash = fingerprint(target)
    print("Disalin: %s -> %s" % (origin, target))
    print("sha256 sumber : %s" % source_hash)
    print("sha256 keluaran: %s" % target_hash)
    if source_hash != target_hash:
        print("GALAT: hash keluaran berbeda dari sumber", file=sys.stderr)
        return 2
    print("OK: keluaran identik dengan sumber")
    return 0


if __name__ == "__main__":
    sys.exit(place_picture())
