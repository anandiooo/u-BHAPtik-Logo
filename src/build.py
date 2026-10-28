"""BHAPtik concept generator.

Glyphs are built from primitives in a local em: cap top y=0, baseline y=140.
Solids are clockwise, counters counter-clockwise; fill-rule nonzero gives a true union.
Construction:
  stem 24 · horizontal bars 22 (optical thinning) · bowls = straight + semicircle, inner circle shifted 2 left
  fold line: B waist, H bar, P bowl bottom, t crossbar all sit on y 56..78; x-height top = 56
  diagonals: A legs 15° off vertical, k arm/leg 45°
Run:  python build.py <version>   -> writes out/<name>-<version>.svg
"""
import math, os, sys

V = sys.argv[1] if len(sys.argv) > 1 else "v1"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "draft", "out")
os.makedirs(OUT, exist_ok=True)

S, T = 24, 22          # stem, bar
FT, FB = 56, 78        # fold line top/bottom (= x-height top)
BASE = 140

# ---------- path model: list of subpaths; each subpath = list of commands ----------
# ('M',x,y) ('L',x,y) ('A',r,large,sweep,x,y) ('Z',)

def rect(x0, y0, x1, y1):
    return [('M', x0, y0), ('L', x1, y0), ('L', x1, y1), ('L', x0, y1), ('Z',)]

def poly(pts, hole=False):
    a = sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))
    cw = a > 0                     # screen coords: positive shoelace = clockwise
    if cw == hole:
        pts = pts[::-1]
    return [('M', *pts[0])] + [('L', *p) for p in pts[1:]] + [('Z',)]

def dbowl(x0, xc, cy, r, hole=False):
    """D shape: straight from x0 to xc, semicircle to the right (centre xc,cy)."""
    if not hole:
        return [('M', x0, cy - r), ('L', xc, cy - r), ('A', r, 0, 1, xc, cy + r), ('L', x0, cy + r), ('Z',)]
    return [('M', x0, cy - r), ('L', x0, cy + r), ('L', xc, cy + r), ('A', r, 0, 0, xc, cy - r), ('Z',)]

def circle(cx, cy, r, hole=False):
    s = 0 if hole else 1
    return [('M', cx, cy - r), ('A', r, 0, s, cx, cy + r), ('A', r, 0, s, cx, cy - r), ('Z',)]

def lens(p, q, h, hole=False):
    """Leaf/lens with tips p,q and half-width h (two equal circular arcs)."""
    L = math.dist(p, q)
    r = (L * L / 4 + h * h) / (2 * h)
    s = 0 if hole else 1
    return [('M', *p), ('A', r, 0, s, *q), ('A', r, 0, s, *p), ('Z',)]

def xf(sub, k=1.0, dx=0.0, dy=0.0):
    out = []
    for c in sub:
        if c[0] in 'ML':
            out.append((c[0], c[1] * k + dx, c[2] * k + dy))
        elif c[0] == 'A':
            out.append(('A', c[1] * k, c[2], c[3], c[4] * k + dx, c[5] * k + dy))
        else:
            out.append(c)
    return out

def fmt(v):
    v = round(v, 2)
    return ('%g' % v)

def d_of(subs):
    parts = []
    for sub in subs:
        for c in sub:
            if c[0] in 'ML':
                parts.append(f"{c[0]}{fmt(c[1])} {fmt(c[2])}")
            elif c[0] == 'A':
                r = fmt(c[1])
                parts.append(f"A{r} {r} 0 {c[2]} {c[3]} {fmt(c[4])} {fmt(c[5])}")
            else:
                parts.append("Z")
    return "".join(parts)

def svg(name, w, h, groups, title):
    body = "".join(f'<path fill="{col}" d="{d_of(subs)}"/>' for col, subs in groups if subs)
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {round(w)} {round(h)}" width="{round(w)}" height="{round(h)}" '
           f'role="img" aria-labelledby="t"><title id="t">{title}</title>{body}</svg>\n')
    p = os.path.join(OUT, f"{name}-{V}.svg")
    open(p, "w", encoding="utf-8").write(doc)
    return p

# ---------- glyphs: return (subpaths, advance width) ----------
def g_B():
    return [rect(0, 0, S, BASE),
            dbowl(0, 44, 39, 39), dbowl(S, 42, 39, 17, hole=True),
            dbowl(0, 50, 98, 42), dbowl(S, 48, 98, 20, hole=True)], 92

def g_H():
    w = 98
    return [rect(0, 0, S, BASE), rect(w - S, 0, w, BASE), rect(S - 1, FT, w - S + 1, FB)], w

def g_A():
    t15 = math.tan(math.radians(15))
    run = BASE * t15                     # 37.51
    top = 25                             # flat apex
    w = 2 * run + top
    lw = S / math.cos(math.radians(15))  # horizontal leg width
    outer = poly([(0, BASE), (run, 0), (run + top, 0), (w, BASE), (w - lw, BASE),
                  (w - lw - (BASE - 112) * t15, 112), (lw + (BASE - 112) * t15, 112), (lw, BASE)])
    # counter above the bar: inner edges meet at the apex of the counter
    yb = 90
    xl = lw + (BASE - yb) * t15
    xr = w - lw - (BASE - yb) * t15
    yapex = BASE - (w - 2 * lw) / (2 * t15)
    counter = poly([(xl, yb), ((xl + xr) / 2, yapex), (xr, yb)], hole=True)
    return [outer, counter], w

def g_P(bar_to=None):
    subs = [rect(0, 0, S, BASE), dbowl(0, 46, 39, 39), dbowl(S, 44, 39, 17, hole=True)]
    if bar_to:                           # concept B: bowl's bottom bar runs on as the t crossbar
        subs.append(rect(40, FT, bar_to, FB))
    return subs, 85

def g_t(x0=0, bar=True):
    st0, st1 = 14, 14 + S
    subs = [poly([(st0, 30), (st1, 14), (st1, 112), (st0, 112)])]   # 33.7° cut top? -> keep exact 45° below
    subs = [poly([(st0, 38), (st1, 14), (st1, 112), (st0, 112)])]    # 45° slanted top (parang cut)
    if bar:
        subs.append(rect(0, FT, 62, FB))
    subs.append([('M', st1, 110), ('A', 6, 0, 0, 44, 116), ('L', 62, 116), ('L', 62, BASE), ('L', 44, BASE),
                 ('A', 30, 0, 1, st0, 110), ('Z',)])
    return [xf(s, 1, x0) for s in subs], 62

def g_i(dot="square"):
    subs = [rect(0, FT, S, BASE)]
    if dot == "square":
        subs.append(rect(0, 20, S, 44))
    return subs, S

def g_k():
    subs = [rect(0, 0, S, BASE),
            poly([(S - 1, 70), (38, FT), (72, FT), (S - 1, 104 + 1)]),
            poly([(S - 2, 102), (41, 87), (94, BASE), (60, BASE)])]
    return subs, 94

def leaf_dot(cx, cy, size):
    """45° leaf used as the i-dot (concept A)."""
    h = size / 2
    p, q = (cx - h * 0.7071 * 1.0, cy + h * 0.7071), (cx + h * 0.7071, cy - h * 0.7071)
    return lens(p, q, size * 0.30)

# ---------- wordmark assembly ----------
GAP = {('B', 'H'): 22, ('H', 'A'): 12, ('A', 'P'): 12, ('P', 't'): 14, ('t', 'i'): 14, ('i', 'k'): 22}

DOT_INDEX = [None]

def wordmark(variant="base"):
    order = ['B', 'H', 'A', 'P', 't', 'i', 'k']
    x, subs = 0, []
    adv = {}
    for i, ch in enumerate(order):
        if ch == 'B': g, w = g_B()
        elif ch == 'H': g, w = g_H()
        elif ch == 'A': g, w = g_A()
        elif ch == 'P':
            g, w = g_P()
            p_x = x
        elif ch == 't':
            if variant == "link":
                # P bowl bottom bar continues into the t crossbar
                g, w = g_t(bar=True)
                g = [xf(s, 1, x) for s in g]
                subs.append(rect(p_x + 40, FT, x + 2, FB))
                subs += g; adv[ch] = x; x += w
                x += GAP[('t', 'i')]
                continue
            g, w = g_t()
        elif ch == 'i':
            g, w = g_i("none" if variant in ("leaf",) else "square")
            if variant == "leaf":
                g.append(lens((S / 2 - 13, 26 + 13), (S / 2 + 13, 26 - 13), 13))
        elif ch == 'k': g, w = g_k()
        subs += [xf(s, 1, x) for s in g]
        if ch == 'i' and variant == "leaf":
            DOT_INDEX[0] = len(subs) - 1
        adv[ch] = x
        x += w
        if i < len(order) - 1:
            x += GAP[(ch, order[i + 1])]
    return subs, x

# ---------- symbols (256 canvas) ----------
def kawung_leaf(x0, y0, s, diag):
    """Leaf inside a square cell (x0,y0,s): two arcs of radius s centred on the cell's other two corners.
    diag='\\' -> tips at top-left & bottom-right; '/' -> tips at bottom-left & top-right."""
    if diag == '\\':
        p, q = (x0, y0), (x0 + s, y0 + s)
    else:
        p, q = (x0, y0 + s), (x0 + s, y0)
    return [('M', *p), ('A', s, 0, 1, *q), ('A', s, 0, 1, *p), ('Z',)]

def sym_kawung(g=21, L=122, h=40):
    """Four kawung leaves on the diagonals of a square cloth; the + between them is the fold crease."""
    c, u, subs = 128, 0.70711, []
    for sx, sy in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        p = (c + sx * g * u, c + sy * g * u)
        q = (c + sx * (g + L) * u, c + sy * (g + L) * u)
        subs.append(lens(p, q, h))
    return subs

def sym_kawung_square(s=100, gap=12):
    """Furoshiki square creased into four cells; each cell holds one kawung leaf pointing to the centre."""
    c = 128
    a, b = c - gap / 2 - s, c + gap / 2
    return [kawung_leaf(a, a, s, '\\'), kawung_leaf(b, a, s, '/'),
            kawung_leaf(a, b, s, '/'), kawung_leaf(b, b, s, '\\')]

def sym_bt():
    subs, _ = g_B()
    subs = [s for s in subs]
    tg, _ = g_t(bar=False)
    tx = 92 + 6
    subs += [xf(s, 1, tx) for s in tg]
    subs.append(rect(46, FT, tx + 62, FB))      # B's waist runs out as the t crossbar
    w = tx + 62
    k = 180 / BASE
    return [xf(s, k, (256 - w * k) / 2, (256 - BASE * k) / 2 - 2) for s in subs]

def sym_fold():
    """Square cloth, corners folded to the centre = diamond of 4 flaps; one flap opened outward."""
    c, R, gp = 128, 112, 7          # diamond half-diagonal, half gap
    subs = []
    # flaps: right triangles with the right angle at the diamond corner... use quadrants of diamond
    quads = [((c + gp, c - gp), (c + gp, c - R + gp * 1.0), (c + R - gp, c - gp)),   # top-right
             ((c + gp, c + gp), (c + R - gp, c + gp), (c + gp, c + R - gp)),
             ((c - gp, c + gp), (c - gp, c + R - gp), (c - R + gp, c + gp)),
             ((c - gp, c - gp), (c - R + gp, c - gp), (c - gp, c - R + gp))]
    tri = [list(q) for q in quads[1:]]
    # top-right flap unfolded across its crease (the 45° hypotenuse): reflect it, then push it out by t
    # along (1,-1) so the crease gap (t*sqrt2) matches the + gap (2*gp)
    t = 2 * gp / math.sqrt(2)
    (ix, iy), p1, p2 = quads[0]
    rx, ry = ix + (R - 2 * gp), iy - (R - 2 * gp)        # reflection of the inner corner
    tri.append([(p1[0] + t, p1[1] - t), (p2[0] + t, p2[1] - t), (rx + t, ry - t)])
    xs = [p[0] for q in tri for p in q]; ys = [p[1] for q in tri for p in q]
    dx = 128 - (min(xs) + max(xs)) / 2; dy = 128 - (min(ys) + max(ys)) / 2
    k = 228 / max(max(xs) - min(xs), max(ys) - min(ys))
    return [xf(poly(q), k, 128 - 128 * k + dx * k, 128 - 128 * k + dy * k) for q in tri]

def lockup(sym, word, ww, sym_h=150, cap=96, gap_ratio=0.32, pad=40):
    """Horizontal lockup, height 256: symbol (256 canvas) left, wordmark cap height `cap`, both centred on y=128."""
    ks = sym_h / 256
    kw = cap / BASE
    sx = pad
    wx = pad + sym_h + sym_h * gap_ratio
    subs = [xf(s, ks, sx, 128 - sym_h / 2) for s in sym]
    subs += [xf(s, kw, wx, 128 - cap / 2) for s in word]
    return subs, wx + ww * kw + pad

if __name__ == "__main__":
    files = []
    pad = 58
    wm, ww = wordmark("base")
    files.append(svg("wordmark-base", ww + 2 * pad, 256, [("#000", [xf(s, 1, pad, pad) for s in wm])], "BHAPtik wordmark"))
    syms = {"a": sym_kawung(), "b": sym_bt(), "c": sym_fold()}
    for nm, sub in syms.items():
        files.append(svg(f"{nm}-symbol", 256, 256, [("#000", sub)], "BHAPtik symbol"))
    # A: kawung symbol + wordmark with leaf i-dot
    wa, wwa = wordmark("leaf")
    la, lw = lockup(syms["a"], wa, wwa)
    files.append(svg("a-lockup", lw, 256, [("#000", la)], "BHAPtik logo"))
    # B: linked wordmark alone (the monogram is its avatar)
    wb, wwb = wordmark("link")
    files.append(svg("b-lockup", wwb + 2 * pad, 256, [("#000", [xf(s, 1, pad, pad) for s in wb])], "BHAPtik logo"))
    # C: fold symbol + base wordmark
    lc, lwc = lockup(syms["c"], wm, ww)
    files.append(svg("c-lockup", lwc, 256, [("#000", lc)], "BHAPtik logo"))
    # colour hint for A: light (cream) and dark (black) panels, stacked into one 2-row artboard
    CREAM, BLACK, BROWN, PINK = "#F3EBDD", "#1A1614", "#6E4B36", "#E9A3A6"
    di = DOT_INDEX[0]
    dot, word = [wa[di]], wa[:di] + wa[di + 1:]
    ks, kw, sh, cap = 150 / 256, 96 / BASE, 150, 96
    wx = 40 + sh + sh * 0.32
    def place(sym_subs, word_subs, dot_subs, oy):
        return ([xf(s, ks, 40, oy + 128 - sh / 2) for s in sym_subs],
                [xf(s, kw, wx, oy + 128 - cap / 2) for s in word_subs],
                [xf(s, kw, wx, oy + 128 - cap / 2) for s in dot_subs])
    W = round(lw)
    s1, w1, d1 = place(syms["a"], word, dot, 0)
    s2, w2, d2 = place(syms["a"][:1] + syms["a"][2:], word, dot, 256)
    pinkleaf = [xf(syms["a"][1], ks, 40, 256 + 128 - sh / 2)]          # top-right leaf
    groups = [(CREAM, [rect(0, 0, W, 256)]), (BROWN, s1), (BLACK, w1), (BROWN, d1),
              (BLACK, [rect(0, 256, W, 512)]), (CREAM, s2 + w2), (PINK, pinkleaf + d2)]
    files.append(svg("a-colour-hint", W, 512, groups, "BHAPtik colour hint"))
    print("\n".join(files))
