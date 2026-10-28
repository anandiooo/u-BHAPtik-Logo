"""BHAPtik logo kit (round 5b direction A - Furoshiki Bundle, minimal = r5b.m1g, small cut = r5b.m1gs).
Writes final/svg, final/png, final/icons, the web manifest + <head> snippet and the board spec.
The mark is one ink colour cut by a luminance mask, so every colour version is generated here
(export_variants.py would recolour the mask itself). Run: python kit.py
"""
import json, os
import build as b
import r2
import r5b

CREAM, BLACK, BROWN, PINK = "#F3EBDD", "#1A1614", "#6E4B36", "#E9A3A6"
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "final")
for d in ("svg", "png", "icons"):
    os.makedirs(os.path.join(ROOT, d), exist_ok=True)

MAIN, SMALL = r5b.m1g(), r5b.m1gs()
ACCENT = (f'<path d="{r5b.EAR2}"/><path d="{r5b.EAR2}" transform="translate(256 0) scale(-1 1)"/>'
          f'<path d="{r5b.rrect_d(104, 54, 152, 98, 14)}"/>')        # ears + knot, same geometry as the mask

word, ww, _ = r2.fashion_wordmark()
wsubs, LW = b.lockup([], word, ww)
WD = b.d_of(wsubs)                       # wordmark path in lockup space: x 238..238+WW, y 80..176
WX, WW, WY, WH = 238.0, LW - 238.0 - 40, 80.0, 96.0

def svg(w, h, body, bg=None, title="BHAPtik", radius=0):
    tile = f'<rect width="{w:g}" height="{h:g}" rx="{radius:g}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" width="{w:g}" height="{h:g}" '
            f'role="img" aria-labelledby="t"><title id="t">{title}</title>{tile}{body}</svg>\n')

def mark(mask, ink, key, tf="", accent=None):
    m = (f'<defs><mask id="{key}" maskUnits="userSpaceOnUse" x="0" y="0" width="256" height="256">'
         f'<rect width="256" height="256" fill="#000"/>{mask}</mask></defs>'
         f'<g{tf}><rect width="256" height="256" fill="{ink}" mask="url(#{key})"/>')
    if accent:
        m += f'<g fill="{accent}">{ACCENT}</g>'
    return m + "</g>"

def word_at(ink, dx, dy, k=1.0):
    return f'<g transform="translate({dx:g} {dy:g}) scale({k:g})"><path fill="{ink}" d="{WD}" transform="translate({-WX:g} {-WY:g})"/></g>'

def write(name, text):
    p = os.path.join(ROOT, "svg", name + ".svg")
    open(p, "w", encoding="utf-8").write(text)
    return p

HTF = ' transform="translate(40 40) scale(0.6875)"'          # horizontal: symbol 176 tall vs 96 cap (optical balance)
KS, SYM = 0.62, 180                                           # stacked: wordmark cap 60, symbol 180
SW, SH = WW * KS + 80, 40 + SYM + 28 + WH * KS + 40
def stacked(ink):
    return (mark(MAIN, ink, "m", f' transform="translate({(SW - SYM) / 2:g} 40) scale({SYM / 256:g})"')
            + word_at(ink, (SW - WW * KS) / 2, 40 + SYM + 28, KS))

COLS = {"black": (BLACK, None), "cream": (CREAM, None), "brown": (BROWN, None)}
files = []
for cname, (ink, _) in COLS.items():
    files.append(write(f"bhaptik-symbol-{cname}", svg(256, 256, mark(MAIN, ink, "m"))))
    files.append(write(f"bhaptik-symbol-small-{cname}", svg(256, 256, mark(SMALL, ink, "m"))))
    files.append(write(f"bhaptik-horizontal-{cname}",
                       svg(LW + 26, 256, mark(MAIN, ink, "m", HTF) + f'<path fill="{ink}" d="{WD}" transform="translate(26 0)"/>')))
    # stacked: symbol 150 tall centred on top, wordmark 96 cap below with a 30 gap
    files.append(write(f"bhaptik-stacked-{cname}", svg(SW, SH, stacked(ink))))
    files.append(write(f"bhaptik-wordmark-{cname}", svg(WW + 80, WH + 80, word_at(ink, 40, 40))))

# colour versions on black (pink only on dark grounds: pink on cream is 1.7:1)
files.append(write("bhaptik-symbol-accent-on-black", svg(256, 256, mark(MAIN, CREAM, "m", accent=PINK), bg=BLACK)))
files.append(write("bhaptik-horizontal-accent-on-black",
                   svg(LW + 26, 256, mark(MAIN, CREAM, "m", HTF, PINK)
                       + f'<path fill="{CREAM}" d="{WD}" transform="translate(26 0)"/>', bg=BLACK)))
files.append(write("bhaptik-stacked-cream-on-black",
                   svg(SW, SH, stacked(CREAM), bg=BLACK)))
# icons: favicon = small cut, black on transparent; app icon = cream small cut on black tile
files.append(write("favicon", svg(256, 256, mark(SMALL, BLACK, "m"))))
files.append(write("app-icon", svg(256, 256, mark(SMALL, CREAM, "m", ' transform="translate(38 34) scale(0.703)"'), bg=BLACK, radius=56)))
files.append(write("maskable-icon", svg(256, 256, mark(SMALL, CREAM, "m", ' transform="translate(51 47) scale(0.6)"'), bg=BLACK)))

json.dump({"name": "BHAPtik", "short_name": "BHAPtik", "theme_color": BLACK, "background_color": CREAM,
           "display": "standalone",
           "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"},
                     {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"},
                     {"src": "/maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]},
          open(os.path.join(ROOT, "icons", "site.webmanifest"), "w"), indent=2)
open(os.path.join(ROOT, "icons", "head-snippet.html"), "w").write(
    '<link rel="icon" href="/favicon.ico" sizes="any">\n<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n'
    '<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n<link rel="manifest" href="/site.webmanifest">\n'
    f'<meta name="theme-color" content="{BLACK}">\n')
print("\n".join(files))
print(f"horizontal {LW:.0f}x256, wordmark width {WW:.0f}")
