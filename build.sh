#!/bin/sh
# Rebuild entry.png from build_image.py and confirm both runs agree.
set -eu
cd "$(dirname "$0")"
python3 build_image.py entry.png
python3 build_image.py /tmp/news-image-20261122-check.png
cmp entry.png /tmp/news-image-20261122-check.png
echo "deterministic: two runs, identical bytes"
md5sum entry.png
ls -l entry.png
