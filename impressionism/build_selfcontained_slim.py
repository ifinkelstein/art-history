#!/usr/bin/env python3
"""Bake DOWNSCALED images (images_slim/) into one offline HTML that fits GitHub's
100 MB file limit. Generate images_slim/ first with:

    magick mogrify -path images_slim -resize "2400x2400>" -quality 85 -strip images/*.jpg

The folder version (impressionism-story.html + images/) keeps full resolution; this
slim single file is for offline USB / local / email use.
"""
import base64, os, re

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "impressionism-story.html")
out = os.path.join(here, "impressionism-story.SELF-CONTAINED.html")
slim = os.path.join(here, "images_slim")

with open(src, encoding="utf-8") as f:
    html = f.read()

missing = []

def repl(m):
    name = os.path.basename(m.group(1))          # images/foo.jpg -> foo.jpg
    p = os.path.join(slim, name)
    if not os.path.exists(p):
        missing.append(name)
        return m.group(0)
    with open(p, "rb") as fh:
        b64 = base64.b64encode(fh.read()).decode("ascii")
    return 'src="data:image/jpeg;base64,%s"' % b64

html2 = re.sub(r'src="(images/[^"]+)"', repl, html)

with open(out, "w", encoding="utf-8") as f:
    f.write(html2)

print("missing:", missing)
print("wrote %s (%.1f MB)" % (out, os.path.getsize(out) / 1e6))
