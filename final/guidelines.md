# BHAPtik: Logo Guidelines (compact)

## 1. The logo
- **Idea**: a furoshiki cloth tied into a bundle. The cloth is printed with parang rusak (Indonesian batik), and it wraps a row of seigaiha waves (Japanese pattern). It is batik, wrapped the Japanese way.
- **Name**: always written **BHAPtik**: uppercase BHAP, lowercase tik. Never retype it; use the artwork files.
- **Versions**:

  | Version | File | Use it for |
  |---|---|---|
  | Horizontal (primary) | `svg/bhaptik-horizontal-*.svg` | Websites, packaging, labels wider than tall |
  | Stacked | `svg/bhaptik-stacked-*.svg` | Square and tall spaces: tote fronts, posters, shopping bags |
  | Symbol | `svg/bhaptik-symbol-*.svg` | Embroidery, caps, keychains, stamps, avatars |
  | Small-size symbol | `svg/bhaptik-symbol-small-*.svg` | Anything under 32 px or 10 mm: favicon, woven label, small tags |
  | Wordmark only | `svg/bhaptik-wordmark-*.svg` | When the symbol already appears nearby, such as on a care label or receipt |

- **Files**: `svg/` holds the masters (screens and print). `png/` holds 1024 px symbols and 1200 px lockups. `icons/` holds the favicon, app icons and web manifest.

## 2. Clear space
Keep a clear zone of **1 × K** on all sides of the logo. K is the width of the knot, which is about 0.19 × the symbol's height. The zone scales with the logo.

## 3. Minimum size
| Version | Screen | Print | Embroidery / woven |
|---|---|---|---|
| Horizontal | 120 px wide | 30 mm wide | 40 mm wide* |
| Symbol | 32 px | 10 mm | 25 mm tall* |
| Small-size symbol | 16 px | 6 mm | 12 mm tall* |

\*Starting points only. These sizes haven't been tested on a machine yet; confirm them with a stitch-out (see open items).

## 4. Colour
| Name | Role | HEX | RGB | CMYK (approx.) |
|---|---|---|---|---|
| Sumi Black | Primary ink | #1A1614 | 26 22 20 | 0 15 23 90 (use rich black on press) |
| Kain Cream | Ground | #F3EBDD | 243 235 221 | 0 3 9 5 |
| Soga Brown | Second ink | #6E4B36 | 110 75 54 | 0 32 51 57 |
| Sakura Pink | Accent only | #E9A3A6 | 233 163 166 | 0 30 29 9 |

The CMYK values are straight conversions from RGB. Match them on a printed proof, and have the printer pick Pantone equivalents.

**Approved logo/background pairs**:
- Black on cream or white (primary).
- Cream on black (reverse).
- Brown on cream.
- Cream on brown.
- Accent version on black: a cream mark with a pink knot and ears (`*-accent-on-black.svg`).

**Never** put pink on cream or white (contrast is 1.7:1), and never put brown on black (2.3:1). Pink is only an accent. Don't use it for the whole mark or the wordmark.

## 5. Typography
- **Wordmark**: custom drawing. Its leaf-shaped dot on the i belongs to the wordmark.
- **Companion typeface (suggested)**: Plus Jakarta Sans, an open-licence typeface designed in Indonesia. Use Bold for headlines and Regular/Medium for body text. The web fallback is `system-ui, sans-serif`. This choice isn't final yet.

## 6. Don'ts
- Don't stretch or squash the logo, and don't rotate it.
- Don't recolour it outside the pairs above, or put pink on light grounds.
- Don't add outlines, shadows, gradients or 3D effects.
- Don't add cream gaps between the knot, the ears and the cloth. The mark is one connected shape.
- Don't redraw the patterns, add more parang bands, or swap the seigaiha for other waves.
- Don't rearrange or resize the parts of a lockup, and don't retype the wordmark.
- On busy photos, place the logo on a calm area or on a solid black or cream panel.

## 7. Contact
For questions about usage, ask <name, email>. The master files are in `projects/bhaptik/final/`, and the source code is in `projects/bhaptik/src/r5b.py` and `src/kit.py`.
