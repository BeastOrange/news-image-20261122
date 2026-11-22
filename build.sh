#!/bin/sh
# Regenerate entry.png deterministically from build_image.py.
set -e
cd "$(dirname "$0")"
python3 build_image.py entry.png
python3 build_image.py /tmp/news-image-20261122-second.png
if cmp -s entry.png /tmp/news-image-20261122-second.png; then
  echo "deterministic: identical bytes across two runs"
else
  echo "ERROR: runs differ" >&2
  exit 1
fi
md5sum entry.png
ls -l entry.png
