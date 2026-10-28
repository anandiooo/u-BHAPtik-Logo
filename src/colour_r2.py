"""Colour hint for A2 Folded Leaf (round 2). Writes out/r2-a2-colour-hint-<v>.svg."""
import sys
import build as b
import r2
from build import xf, rect, BASE

V = sys.argv[1] if len(sys.argv) > 1 else "v1"
b.V = "r2" + V
CREAM, BLACK, BROWN, PINK = "#F3EBDD", "#1A1614", "#6E4B36", "#E9A3A6"
sym = r2.sym_folded()
word, ww, di = r2.fashion_wordmark()
dot, letters = [word[di]], word[:di] + word[di + 1:]
ks, kw, sh, cap = 150 / 256, 96 / BASE, 150, 96
wx = 40 + sh + sh * 0.32
W = round(wx + ww * kw + 40)

def place(oy):
    S_ = lambda subs: [xf(s, ks, 40, oy + 128 - sh / 2) for s in subs]
    T_ = lambda subs: [xf(s, kw, wx, oy + 128 - cap / 2) for s in subs]
    return S_(sym[:3]), S_(sym[3:]), T_(letters), T_(dot)

l3, lf, lw, ld = place(0)
d3, df, dw, dd = place(256)
groups = [(CREAM, [rect(0, 0, W, 256)]), (BROWN, l3 + lf + ld), (BLACK, lw),
          (BLACK, [rect(0, 256, W, 512)]), (CREAM, d3 + dw), (PINK, df + dd)]
print(b.svg("a2-colour-hint", W, 512, groups, "BHAPtik colour hint"))
