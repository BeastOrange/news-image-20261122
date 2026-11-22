#!/usr/bin/env python3
"""Copy the finished front page into the grader's output folder.

The picture itself is baked into entry.png by build_image.py; this
entrypoint only moves those bytes to /output/entry.png, so repeated
runs of the entry agree byte for byte.
"""
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent
DEST = Path("/output/entry.png")


def run() -> int:
    DEST.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / "entry.png", DEST)
    print(f"entry.png -> {DEST} ({DEST.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
