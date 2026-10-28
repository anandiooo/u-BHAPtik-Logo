"""Pattern preview: A2 Folded Leaf as a ceplok-style repeat. Each tile turns 90° from its neighbour,
so the folded leaf travels round the grid. Writes out/pattern-<v>.svg (two colourways side by side)."""
import sys
import build as b
import r2
from build import xf, d_of, rect

V = sys.argv[1] if len(sys.argv) > 1 else "v1"
sym = r2.sym_folded()
CREAM, BLACK, BROWN, PINK = "#F3EBDD", "#1A1614", "#6E4B36", "#E9A3A6"

def rot(sub, q):
    """rotate a 256-canvas subpath by q*90° about (128,128)."""
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

def panel(x0, w, h, bg, fg, accent=None, cell=100, k=0.37):
    parts = [f'<path fill="{bg}" d="{d_of([rect(x0, 0, x0 + w, h)])}"/>']
    main, acc = [], []
    for row in range(h // cell + 1):
        for col in range(w // cell + 1):
            q = (row + col) % 4
            off = (cell - 256 * k) / 2
            subs = [xf(rot(s, q), k, x0 + col * cell + off, row * cell + off) for s in sym]
            if accent and (row * 3 + col) % 7 == 0:
                acc += subs[3:]; main += subs[:3]
            else:
                main += subs
    parts.append(f'<path fill="{fg}" d="{d_of(main)}"/>')
    if acc:
        parts.append(f'<path fill="{accent}" d="{d_of(acc)}"/>')
    return "".join(parts)

W, H = 600, 600
doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {2 * W} {H}" width="{2 * W}" height="{H}">'
       f'<defs><clipPath id="l"><rect width="{W}" height="{H}"/></clipPath>'
       f'<clipPath id="r"><rect x="{W}" width="{W}" height="{H}"/></clipPath></defs>'
       f'<g clip-path="url(#l)">{panel(0, W, H, CREAM, BROWN)}</g>'
       f'<g clip-path="url(#r)">{panel(W, W, H, BLACK, CREAM, PINK)}</g></svg>\n')
open(f"out/pattern-{V}.svg", "w").write(doc)
print(f"out/pattern-{V}.svg")
