#!/usr/bin/env python3
"""
embed_images.py  —  OPTIONAL. Make one fully self-contained HTML file.

After you've run download_art.py, this bakes the images/*.jpg into the HTML as
base64 data URIs and writes:

    impressionism-story.SELF-CONTAINED.html

That single file needs no images/ folder and no internet — handy for emailing or
dropping on a USB stick. Trade-off: it's large (tens of MB) and slower to open,
so for everyday classroom use the normal folder version is smoother.

    python3 embed_images.py
"""
import base64, os, re, sys

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "impressionism-story.html")
out = os.path.join(here, "impressionism-story.SELF-CONTAINED.html")
imgdir = os.path.join(here, "images")

with open(src, "r", encoding="utf-8") as f:
    html = f.read()

def to_data_uri(path):
    with open(path, "rb") as fh:
        b64 = base64.b64encode(fh.read()).decode("ascii")
    return "data:image/jpeg;base64," + b64

missing = []
def repl(m):
    rel = m.group(1)              # e.g. images/starry-night.jpg
    p = os.path.join(here, rel)
    if not os.path.exists(p):
        missing.append(rel)
        return m.group(0)
    return 'src="%s"' % to_data_uri(p)

html2 = re.sub(r'src="(images/[^"]+)"', repl, html)

if missing:
    print("WARNING: these images are not downloaded yet, left as links:")
    for m in missing:
        print("   ", m)
    print("Run download_art.py first for a truly self-contained file.\n")

with open(out, "w", encoding="utf-8") as f:
    f.write(html2)

print("Wrote %s (%.1f MB)" % (out, os.path.getsize(out) / 1e6))
