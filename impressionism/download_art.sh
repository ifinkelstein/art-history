#!/usr/bin/env bash
# download_art.sh — fetch the real high-res paintings into ./images/ (run once, needs internet).
# macOS / Linux / Git Bash. Equivalent to download_art.py.
set -u
cd "$(dirname "$0")"
mkdir -p images
UA="ImpressionismLesson/1.0 (educational; offline classroom use)"
W="${1:-4000}"   # optional first arg = max width

# disk_name|Commons file name|width
ART=(
"starry-night.jpg|Vincent van Gogh - Starry Night - Google Art Project.jpg|4000"
"cabanel-birth-of-venus.jpg|1863 Alexandre Cabanel - The Birth of Venus.jpg|4000"
"grande-jatte.jpg|Georges Seurat - A Sunday on La Grande Jatte -- 1884 - Google Art Project.jpg|4000"
"haystack-end-of-summer.jpg|Claude Monet - Stacks of Wheat (End of Summer) - 1985.1103 - Art Institute of Chicago.jpg|3000"
"haystack-snow-overcast.jpg|Claude Monet - Stack of Wheat (Snow Effect, Overcast Day) - 1933.1155 - Art Institute of Chicago.jpg|3000"
"haystack-thaw-sunset.jpg|Claude Monet - Stack of Wheat (Thaw, Sunset) - 1983.166 - Art Institute of Chicago.jpg|3000"
"great-wave.jpg|Katsushika Hokusai - Thirty-Six Views of Mount Fuji- The Great Wave Off the Coast of Kanagawa - Google Art Project.jpg|4000"
"lapis-lazuli.jpg|Lump of raw lapis lazuli.jpg|3000"
"artist-palette.jpg|Paintbrush and palette.JPG|3000"
"oil-colors-ad-1915.jpg|“F. W. Devoe & C. T. Raynolds Co.” “Artists’ Oil Colors” “CADMIUM YELLOW” September 1915 ad - The International studio (IA internationalst5622unse 0) (page 14 crop).jpg|2000"
"old-palette-selfportrait.jpg|Self-portrait of Joseph Vivien with Palette, ca. 1715.jpg|2200"
)

urlencode(){ # encode spaces and specials for a URL path segment
  local s="$1" out="" c
  for ((i=0;i<${#s};i++)); do c="${s:$i:1}"
    case "$c" in [a-zA-Z0-9.~_-]) out+="$c";; *) printf -v h '%%%02X' "'$c"; out+="$h";; esac
  done
  printf '%s' "$out"
}

for row in "${ART[@]}"; do
  IFS='|' read -r disk file width <<<"$row"
  dest="images/$disk"
  if [[ -s "$dest" ]]; then echo "  skip (already have)  $disk"; continue; fi
  enc="$(urlencode "$file")"
  url="https://commons.wikimedia.org/wiki/Special:FilePath/${enc}?width=${width}"
  echo "  downloading          $disk  (<= ${width}px)"
  curl -L --fail --silent --show-error -A "$UA" -o "$dest" "$url" \
    && echo "    -> $(du -h "$dest" | cut -f1)" \
    || echo "    FAILED: $disk"
  sleep 0.4
done
echo
echo "Done. Now open impressionism-story.html in a browser."
