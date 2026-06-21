#!/usr/bin/env python3
"""
download_art.py  —  fetch the real high-resolution paintings for the lesson.

Run once, with an internet connection:

    python3 download_art.py

It downloads each public-domain painting from Wikimedia Commons into ./images/.
After that, impressionism-story.html works fully offline (the browser reads the
local files). Re-running skips files you already have (use --force to refresh).

Every URL uses Wikimedia's official Special:FilePath endpoint, which redirects to
a freshly rendered JPEG at the requested width. Nothing here is hand-built or
guessed — each Commons filename was verified to exist.

Options:
    --force        re-download even if the file already exists
    --width N      max width in pixels (default 4000). Wikimedia returns the
                   original if it is smaller. Use a bigger number for more detail
                   (e.g. --width 6000) or smaller for lighter files.
"""

import argparse, os, sys, time, urllib.parse, urllib.request

# disk name  ->  (exact Wikimedia Commons file name, default width)
ART = {
    "starry-night.jpg": (
        "Vincent van Gogh - Starry Night - Google Art Project.jpg", 4000),
    "cabanel-birth-of-venus.jpg": (
        "1863 Alexandre Cabanel - The Birth of Venus.jpg", 4000),
    "grande-jatte.jpg": (
        "Georges Seurat - A Sunday on La Grande Jatte -- 1884 - Google Art Project.jpg", 4000),
    "haystack-end-of-summer.jpg": (
        "Claude Monet - Stacks of Wheat (End of Summer) - 1985.1103 - Art Institute of Chicago.jpg", 3000),
    "haystack-snow-overcast.jpg": (
        "Claude Monet - Stack of Wheat (Snow Effect, Overcast Day) - 1933.1155 - Art Institute of Chicago.jpg", 3000),
    "haystack-thaw-sunset.jpg": (
        "Claude Monet - Stack of Wheat (Thaw, Sunset) - 1983.166 - Art Institute of Chicago.jpg", 3000),
    "great-wave.jpg": (
        "Katsushika Hokusai - Thirty-Six Views of Mount Fuji- The Great Wave Off the Coast of Kanagawa - Google Art Project.jpg", 4000),

    # --- historical / real object photos (replace some hand-drawn diagrams) ---
    "lapis-lazuli.jpg": (
        "Lump of raw lapis lazuli.jpg", 3000),
    "artist-palette.jpg": (
        "Paintbrush and palette.JPG", 3000),
    "oil-colors-ad-1915.jpg": (
        "\u201cF. W. Devoe & C. T. Raynolds Co.\u201d \u201cArtists\u2019 Oil Colors\u201d \u201cCADMIUM YELLOW\u201d September 1915 ad - The International studio (IA internationalst5622unse 0) (page 14 crop).jpg", 2000),
    "old-palette-selfportrait.jpg": (
        "Self-portrait of Joseph Vivien with Palette, ca. 1715.jpg", 2200),
}

UA = "ImpressionismLesson/1.0 (educational; offline classroom use)"

def filepath_url(commons_name, width):
    # Special:FilePath/<file>?width=N  -> redirects to a rendered thumbnail JPEG
    quoted = urllib.parse.quote(commons_name)
    return "https://commons.wikimedia.org/wiki/Special:FilePath/%s?width=%d" % (quoted, width)

def fetch(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
        while True:
            chunk = r.read(1 << 16)
            if not chunk:
                break
            f.write(chunk)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--width", type=int, default=None)
    args = ap.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "images")
    os.makedirs(out, exist_ok=True)

    ok = skip = fail = 0
    for disk, (commons, default_w) in ART.items():
        dest = os.path.join(out, disk)
        if os.path.exists(dest) and os.path.getsize(dest) > 1000 and not args.force:
            print("  skip (already have)  %s" % disk); skip += 1; continue
        w = args.width or default_w
        url = filepath_url(commons, w)
        try:
            print("  downloading          %s  (<= %dpx)" % (disk, w))
            fetch(url, dest)
            size = os.path.getsize(dest)
            if size < 1000:
                raise IOError("file too small, likely an error page")
            print("    -> %.1f MB" % (size / 1e6)); ok += 1
        except Exception as e:
            print("    FAILED: %s" % e, file=sys.stderr); fail += 1
        time.sleep(0.4)  # be polite to Wikimedia

    print("\nDone. %d downloaded, %d already present, %d failed." % (ok, skip, fail))
    if fail:
        print("If something failed, re-run, or open SOURCES.txt and download by hand.")
    print("Now open impressionism-story.html in a browser.")

if __name__ == "__main__":
    main()
