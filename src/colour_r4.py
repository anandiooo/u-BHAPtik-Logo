"""Round 4 colour hint (J1 Kawung Mon, recommended) + J4 stitch accent + J1 pattern swatch.
Batik = brown / cream leaves, Japan = pink (crest, seal, stitches). Pink never on cream (1.7:1).
Run: python colour_r4.py <v>
"""
import sys
import build as b
import r2, r4
from build import xf, rect, d_of, BASE
from r4 import CREAM, BLACK, BROWN, PINK

V = sys.argv[1] if len(sys.argv) > 1 else "v1"
b.V = "r4" + V
word, ww, di = r2.fashion_wordmark()
ks, kw, sh, cap = 150 / 256, 96 / BASE, 150, 96
wx = 40 + sh + sh * 0.32
W = round(wx + ww * kw + 40)
S_ = lambda subs, oy: [xf(s, ks, 40, oy + 128 - sh / 2) for s in subs]
T_ = lambda subs, oy: [xf(s, kw, wx, oy + 128 - cap / 2) for s in subs]
dot, letters = [word[di]], word[:di] + word[di + 1:]

mon = r4.j1_mon()
base4, st4 = r4.j4_sashiko()
groups = [
    (CREAM, [rect(0, 0, W, 256)]), (BROWN, S_(mon, 0) + T_(dot, 0)), (BLACK, T_(letters, 0)),
    (BLACK, [rect(0, 256, W, 512)]), (PINK, S_(mon, 256) + T_(dot, 256)), (CREAM, T_(letters, 256)),
    (BROWN, [rect(0, 512, W, 768)]), (CREAM, S_(base4, 512) + T_(letters, 512)), (PINK, S_(st4, 512) + T_(dot, 512)),
]
print(b.svg("j1-colour-hint", W, 768, groups, "BHAPtik colour hint"))

# pattern: J1 crests on a half-drop grid, each turned 90° from the last (the folded leaf travels)
def rot(sub, q):
    out = []
    for c in sub:
        def r(x, y):
            for _ in range(q % 4):
                x, y = 256 - y, x
            return x, y
        if c[0] in 'ML':
            out.append((c[0], *r(c[1], c[2])))
        elif c[0] == 'A':
            out.append(('A', c[1], c[2], c[3], *r(c[4], c[5])))
        else:
            out.append(c)
    return out

def panel(x0, bg, fg, cell=120, k=0.34):
    subs = []
    for row in range(-1, 6):
        for col in range(-1, 6):
            ox = x0 + col * cell + (cell / 2 if row % 2 else 0)
            q = (row + col) % 4
            off = (cell - 256 * k) / 2
            subs += [xf(rot(s, q), k, ox + off, row * cell + off) for s in mon]
    return f'<path fill="{bg}" d="{d_of([rect(x0, 0, x0 + 600, 600)])}"/><path fill="{fg}" d="{d_of(subs)}"/>'

doc = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 600" width="1200" height="600">'
       '<defs><clipPath id="l"><rect width="600" height="600"/></clipPath>'
       '<clipPath id="r"><rect x="600" width="600" height="600"/></clipPath></defs>'
       f'<g clip-path="url(#l)">{panel(0, CREAM, BROWN)}</g><g clip-path="url(#r)">{panel(600, BLACK, PINK)}</g></svg>\n')
p = f"out/pattern-r4{V}.svg"
open(p, "w").write(doc)
print(p)
