# Art history for kids — offline, zoomable, cast-to-screen lessons

A growing set of single-page, offline art lessons built for casting onto a big
screen (projector, TV, or Amazon Fire Stick) and reading aloud to ~10-year-olds.
Every visual is a real, high-resolution public-domain museum scan or photograph.
Tap (or select with a remote) any picture to open it full-screen and zoom into the
real brushstrokes. After a one-time image download each lesson runs fully offline.

The first lesson is **Impressionism** (`impressionism/`). This README is the master
doc: it records every design choice and gives a repeatable recipe so you (or an AI
assistant) can build out **other periods** in the same style — including periods
that intersect with Impressionism (see "Building other periods" below).

---

## Repo layout

```
art-history/
├── README.md                       this file — design system + build recipe
└── impressionism/                  the first lesson (reference implementation)
    ├── impressionism-story.html        the lesson — open/host THIS (folder version, full-res)
    ├── impressionism-story.SELF-CONTAINED.html   one offline file, images baked in (slimmed to fit GitHub)
    ├── images/                         35 high-res public-domain JPEGs
    │   └── SOURCES.txt                 every image: source URL + license
    ├── download_art.py / .sh           fetch the paintings into images/
    ├── build_selfcontained.py          bake full-res images into one offline HTML
    ├── build_selfcontained_slim.py     bake downscaled images into a <100 MB offline HTML
    ├── FACT-CHECK.md                   every claim, with sources + flagged nuances
    └── LINKS.md                        every external link, confirmed live
```

Two builds, on purpose:
- **Folder version** (`impressionism-story.html` + `images/`) — full resolution. This is
  what you host (GitHub Pages) and cast. Images lazy-load one at a time.
- **Self-contained version** (`impressionism-story.SELF-CONTAINED.html`) — one file with
  every image base64-embedded, **downscaled** (max ~1800 px, JPEG q82) so the whole file
  stays under GitHub's 100 MB limit. For offline USB / local / email use. The full-res
  single file would be ~205 MB (over the limit), so the committed one is the slim build.

---

## What's in the Impressionism lesson

One long, deliberately ordered scroll with a sticky color-dot navigator:

1. **Music** — Debussy as the Impressionist of sound (Hokusai's *Great Wave* hook).
2. **Before** — the smooth Salon style (Cabanel's *Birth of Venus*).
3. **The Rebels** — four personality cards (Monet, Degas, Van Gogh, Seurat) + Seurat's *Grande Jatte*.
4. **Painter galleries** — a deep-dive section per rebel: portrait, lede, "what he was
   like" facts, a read-aloud box, and **5 zoomable signature works** each.
5. **Haystacks** — Monet's same-subject-25-times series experiment.
6. **How it grew** — the staircase from Realism to abstraction.
7. **Color & tubes** — why bright paint + the metal tube made Impressionism possible.
8. **Your turn** — "which painter are you" + make-your-own challenges.

35 images total: 7 famous paintings, 4 painter self-portraits, 20 signature works,
and 4 historical object photos (lapis lazuli, an 18th-c. palette self-portrait, a
modern palette, a 1915 oil-paint advert).

---

## Design choices (the house style)

These are the decisions worth copying verbatim into every future lesson.

### Hard constraints (non-negotiable for "offline + castable")
- **Single self-contained HTML.** No build step to view, no framework. One `.html`
  file plus an `images/` folder.
- **No external loads.** No web fonts, no CDNs, no `<link>`/`<script src>`, no `@import`,
  no remote `url()`. System fonts and inline CSS/JS only. External `<a href>` links are
  fine (they're the optional "needs internet" buttons).
- **No SVG, no canvas, no cartoons.** Every visual is a real photograph/scan in an
  `<img>`. (The lightbox is image-only by design.)
- **Graceful image fallback.** Each `<img>` has `onerror="imgFail(this)"`, which hides
  the broken image, shows a "run download_art" placeholder, and disables that figure's
  zoom — so the page is usable before the download runs.
- **Big tap targets, large type.** It's operated from a phone and read from across a room.

### Visual system (CSS tokens — reuse these exact variables)
```
--ink:#241f1a  --paper:#f4ecdb  --paper2:#efe5d0      /* text + page backgrounds */
--night:#0e1838                                        /* dark "Starry Night" band  */
--cobalt:#2a4bd7 --cad:#f4b400 --viridian:#1f8f6a      /* accent palette = real     */
--vermilion:#e1492e --cerulean:#2e9bd6 --violet:#6a4c9c/* pigment names             */
--serif: Iowan Old Style / Palatino / Georgia stack    /* headings + captions       */
--sans:  system-ui stack                               /* body                      */
```
- **Color-blocked bands.** One mood/color per section (`.band--paper`, `--paper2`,
  `--night`, `--gold`, `--salon`). Band color can echo the subject.
- **Each painter gets one accent color**, used for its eyebrow, fact box border, and
  nav dot: Monet=`--cad`, Van Gogh=`--vermilion`, Seurat=`--viridian`, Degas=`--cerulean`.
- **Spend boldness in one place** (the palette nav + tap-to-zoom); keep everything else quiet.

### Reusable components (class names in `impressionism-story.html`)
- `.nav` + `.blob` — sticky top bar of colored dots that jump to each `#section`.
- `.band` / `.wrap` / `.split` (+ `.flip`) — section + centered column + 2-up portrait/text layout.
- `.eyebrow` `.lede` `.read` — section kicker, intro paragraph, read-aloud callout (colored left border).
- `.epithet` — one-line italic painter tagline.
- `.facts` — "what he was like" bullet card with accent left-border.
- `.gallery` / `.three` / `.cards` — responsive auto-fit image grids.
- `figure.zoomable` → `.frame` → `<img>` + `.zoomhint` + `.dl-note` — the standard
  zoomable artwork unit. **Copy this structure exactly**; the lightbox depends on it.
- The **lightbox** (`#lightbox` / `#zoomPane` + the inline `<script>`) — copy verbatim.

### Content choices
- **Personality first, then the art.** Kids remember "Van Gogh wrote hundreds of letters
  to his brother" over dates. Lead every painter with a hook.
- **Read-aloud boxes** (`.read`) mark the lines the adult says out loud.
- **Zoom-hunts in captions.** Every gallery caption ends with a "find the X" game
  (the white iris, one dot of true black, the dancer fixing her shoe).
- **Section order carries meaning.** The spine here: paint real → paint light → paint
  time → paint dots → paint feelings.

---

## Build pipeline (how this lesson was actually made)

The steps that keep a lesson accurate, richly illustrated, and genuinely offline.

1. **Draft content, personality-first.** One job for the page; an ordered spine; a
   cross-art hook if possible (here, Debussy).
2. **Research with parallel agents.** For the painter galleries, one research agent
   per painter ran in parallel. Each returned: a one-paragraph lede, 6–8 fact bullets,
   2–3 sourced read-aloud quotes, a nickname, verified museum links, a SOURCES list,
   and a NOTES list flagging shaky claims — plus, for every image, the **exact
   Wikimedia Commons filename, verified to exist** (no guessed filenames).
3. **Fact-check before building.** Treat "first/only/biggest" and round numbers with
   suspicion; soften or source them. Record everything in `FACT-CHECK.md`. Notable
   nuances baked in: the Van Gogh ear is "part of his ear" (illness, not gore);
   Seurat's cause of death is "doctors were never sure"; *Impression, Sunrise*
   "gave the movement its name" (not "invented it").
4. **Verify every link by opening it.** Keep them in `LINKS.md`.
5. **Source super-high-res public-domain art.** Best wells: Wikimedia Commons, Art
   Institute of Chicago (CC0), the Met Open Access, National Gallery of Art, Rijksmuseum.
   Works by artists dead 95+ years are public domain. Download via the official endpoint:
   ```
   https://commons.wikimedia.org/wiki/Special:FilePath/<EXACT FILE NAME>?width=4000
   ```
   `Special:FilePath` redirects to a freshly rendered JPEG and avoids hand-built hash
   paths; Wikimedia returns the original if it's smaller than the requested width.
   List every source + license in `images/SOURCES.txt`.
6. **Assemble the HTML** by reusing the components above.
7. **Review with parallel agents.** Three independent reviewers — an **art historian**
   (facts/dates/attributions), a **children's-museum educator** (engagement, voice,
   age-appropriateness, read-aloud quality), and a **technical front-end reviewer**
   (every image present/accessible locally, no SVG/external loads, no duplicate IDs,
   nav⇄section parity, Fire TV/perf) — then synthesize their fixes.
8. **De-LLM pass.** Strip AI writing tells (false-suspense "Here's the…" openers,
   stacked negative parallelism, doubled em-dashes) while keeping the read-aloud
   devices that are features for kids.
9. **Bake the offline files.** Full-res single file via `build_selfcontained.py`; the
   committed slim single file (<100 MB) via `build_selfcontained_slim.py`.

### Rebuilding from scratch
```
cd impressionism
python3 download_art.py              # fills images/ from Wikimedia (one-time, needs internet)
python3 build_selfcontained_slim.py  # the committed <100 MB offline single file
python3 build_selfcontained.py       # optional full-res single file (~205 MB, not committed)
```

---

## Hosting & casting (Amazon Fire Stick, phones, projectors)

Fire TV is **not** a Chromecast — you can't "cast a Chrome tab" to it. Two real paths:

- **Best — host the folder version and open the URL on the device.** The **folder
  version** (`impressionism-story.html` + `images/`) is on GitHub Pages; open
  `https://ifinkelstein.github.io/art-history/impressionism/impressionism-story.html`
  directly in the Fire TV browser (Amazon Silk / Firefox for Fire TV). Images lazy-load
  one at a time, which the low-RAM Silk browser needs.
- **Phone → Fire TV screen mirroring.** Open the page on an Android phone (URL or local
  file) and use Display Mirroring / Miracast. The phone does the rendering; drive it by touch.
- **Fully offline.** Use `impressionism-story.SELF-CONTAINED.html` from a USB stick or
  local file. One file, no folder, no internet (slightly lower-res images to fit GitHub).

### Remote-control support (added for Fire TV)
The lightbox works without touch: every figure is focusable (`tabindex`), **OK/Enter**
opens and toggles zoom, **arrow keys pan**, **+ / −** zoom, **Back/Esc** closes. Touch
(pinch, drag, double-tap) still works for phones/tablets.

---

## Building other periods (and periods that intersect this one)

To add a new lesson (e.g. Post-Impressionism, Japonisme, Fauvism, the Dutch Golden Age):

1. Copy `impressionism/` to a new folder (e.g. `post-impressionism/`) and reuse the
   whole CSS/JS shell and component classes verbatim. Keep the hard constraints and
   the visual system above.
2. Pick the period's spine and 4–6 personalities. Run the **per-figure research-agent**
   pattern (step 2) and the **three-reviewer** pattern (step 7).
3. Source art the same way (Special:FilePath, public domain, exact verified filenames,
   `SOURCES.txt`), keep a `FACT-CHECK.md` and `LINKS.md`, run the de-LLM pass, and bake
   the offline files.
4. Add the new lesson to the repo and link it from this README.

### Cross-period intersection hooks (already seeded in the Impressionism lesson)
These are the threads to **link between lessons** so periods connect rather than repeat:

- **Japonisme / Hokusai** — *The Great Wave* (already here via Debussy's *La Mer* and as
  an influence on Van Gogh). A Japanese-prints lesson should link back here; this lesson
  should link forward to it.
- **The Salon "before"** — Cabanel/academic art is the foil. A 19th-c. academic-art or
  Romanticism lesson shares this pivot point.
- **Post-Impressionism** — Van Gogh and Seurat already sit on the "staircase" leading out
  of Impressionism toward modern art; a Post-Impressionism lesson is the natural sequel
  (Cézanne, Gauguin, the later Van Gogh).
- **Color & chemistry** — the new 19th-c. pigments + the metal paint tube (the "Color &
  tubes" section) connect to any lesson about materials/technology in art.
- **Abstraction** — the lesson ends pointing at Kandinsky (a haystack reportedly dazzled
  him in 1896); an abstract-art lesson picks the torch up there.

Keep a shared accent palette and nav style across lessons so the whole `art-history`
set feels like one project, and cross-link intersecting sections with plain `<a href>`
links between the lesson files.

---

## Credits & license

All artworks are public domain (Van Gogh, Monet, Seurat, Degas, Cabanel, Hokusai),
scanned by Wikimedia Commons contributors, Google Arts & Culture, the Art Institute of
Chicago, and national galleries; each file's source and license is listed in
`impressionism/images/SOURCES.txt`. The layout, code, and text are yours to adapt freely
for teaching.
