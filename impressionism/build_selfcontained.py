#!/usr/bin/env python3
"""Bake images/*.jpg into the HTML as base64 data URIs -> one offline file."""
import base64, os, re

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "impressionism-story.html")
out = os.path.join(here, "impressionism-story.SELF-CONTAINED.html")

with open(src, encoding="utf-8") as f:
    html = f.read()

missing = []

def repl(m):
    rel = m.group(1)
    p = os.path.join(here, rel)
    if not os.path.exists(p):
        missing.append(rel)
        return m.group(0)
    with open(p, "rb") as fh:
        b64 = base64.b64encode(fh.read()).decode("ascii")
    return 'src="data:image/jpeg;base64,%s"' % b64

html2 = re.sub(r'src="(images/[^"]+)"', repl, html)

with open(out, "w", encoding="utf-8") as f:
    f.write(html2)

print("missing:", missing)
print("wrote %s (%.1f MB)" % (out, os.path.getsize(out) / 1e6))
