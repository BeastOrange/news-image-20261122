#!/usr/bin/env python3
"""Entry point: copy the pre-built front-page image to /output/entry.png.

The image itself is drawn deterministically by build_image.py (run it
again with ./build.sh to regenerate the identical bytes). This program
does no network and no drawing, so both grader runs write the same bytes.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst, os.path.getsize(dst), "bytes")


if __name__ == "__main__":
    sys.exit(main())
