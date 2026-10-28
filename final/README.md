# BHAPtik logo kit: handover notes

**Direction**: round 5b, A "Furoshiki Bundle, minimal". The symbol is `r5b.m1g()` and the small-size cut is `r5b.m1gs()`. Run `python src/kit.py` from `projects/bhaptik` to rebuild everything in `final/svg`.

## Contents
- `svg/`: the master files.
  - **Symbols**: `bhaptik-symbol-{black,cream,brown}`, `bhaptik-symbol-small-{black,cream,brown}`, `bhaptik-symbol-accent-on-black`.
  - **Lockups**: `bhaptik-horizontal-{black,cream,brown}`, `bhaptik-horizontal-accent-on-black`, `bhaptik-stacked-{black,cream,brown}`, `bhaptik-stacked-cream-on-black`.
  - **Wordmark**: `bhaptik-wordmark-{black,cream,brown}`.
  - **Icon sources**: `favicon`, `app-icon`, `maskable-icon`.
- `png/`: every symbol at 1024 px, and every lockup and wordmark at 1200 px wide, all with transparent backgrounds.
- `icons/`: `favicon.ico` (16/32/48), `favicon.svg`, `favicon-16/32/48.png`, `apple-touch-icon.png` (180), `icon-192.png`, `icon-512.png`, `maskable-512.png`, `site.webmanifest` and `head-snippet.html`.
- `board.html` and `slides/slide-01..05.png`: the presentation, covering the brief, the final design and six mockups (tote, shopping bag, T-shirt, packaging, sticker, social).
- `guidelines.md`: clear space, minimum sizes, colours, approved pairs and don'ts.

## Rationale
- **Furoshiki**: the Japanese wrapping cloth matches the product world of totes, bags and packaging.
- **Parang**: one band of S-blades between two bars of small diamonds (the mlinjo row). This is the Indonesian side, kept bold rather than intricate.
- **Seigaiha**: two rows of waves wrapped inside the cloth. This is the Japanese pattern side.
- **One connected ink shape**: the mark works in pure black and white, in one colour for stamps and screen printing, and on fabric.

## Test results
- `svg_audit.py` scored the symbol 97/100, the small-size cut 98/100 and the horizontal lockup 96/100, with no warnings or failures.
- I visually checked the 16/24/32/64 px renders. The main mark holds at 32 px. At 16 px only the outline and ears survive, which is why the favicon uses the small-size cut.

## Open items (do these before production)
1. **Flatten the artwork.** Each mark is one ink colour cut by an SVG mask. Browsers and most renderers handle this correctly, but embroidery software, vinyl and die cutters, and some print workflows don't. Open each master in Illustrator or Inkscape and expand it into plain shapes (Pathfinder → Unite / Minus Front), then save it as PDF/EPS for printers. `export_variants.py` was not used because it would recolour the mask itself, so `kit.py` generates the colour versions.
2. **Small partial blades.** A few parang blades are cut off along the left and right hem. Remove them during the flattening pass if you want a cleaner edge.
3. **Embroidery and woven-label test.** Do a stitch-out at the minimum sizes in `guidelines.md` before ordering labels.
4. **Trademark search.** None has been done. Search DJKI (Indonesia) and any export markets before launch.
5. **Typeface.** Plus Jakarta Sans is only a suggestion, and the tagline on the board ("Batik, wrapped the Japanese way") is a placeholder. Both need your decision.
6. **Colour on press.** The CMYK values are straight conversions from RGB. Proof them, and have the printer choose Pantone matches.
