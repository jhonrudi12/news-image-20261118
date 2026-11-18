#!/usr/bin/env python3
"""news-image-20261118 entry (Python 3.13, standard library only).

The program copies the pre-rendered poster in assets/poster.png to
/output/entry.png. The poster itself is drawn by tools/render_poster.py
(Pillow) from the verified news of Wednesday 18 November 2026; the image
counts as the entry, and this one-line program is the simplest entry the
competition rules explicitly allow.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "assets", "poster.png")
OUT = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
shutil.copyfile(SRC, OUT)
print("wrote", OUT)
