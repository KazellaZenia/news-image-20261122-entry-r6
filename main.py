#!/usr/bin/env python3
"""Round 6 entrypoint for news-image-20261122.

The front page is already drawn (entry.png sits next to this file).
This program only hands those exact bytes to the grader: it copies
entry.png into $MAKEFUN_OUTPUT_DIR and checks the copy byte for byte
before exiting. It reads nothing else and writes nowhere else.
The copy is deterministic: the same entry.png bytes land in the
output directory on every run, so the grader's two runs agree.
Standard library only.
"""
import hashlib
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            chunk = handle.read(65536)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def main():
    source = HERE / "entry.png"
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / "entry.png"
    shutil.copyfile(source, target)
    if sha256_of(target) != sha256_of(source):
        raise SystemExit("entry.png copy failed checksum")


if __name__ == "__main__":
    main()
    sys.exit(0)
