"""BHAPtik round 2: Kawung Fold refinements (A1 Knot, A2 Folded Leaf, A3 Leaf B) + fashion wordmark.
Run:  python r2.py <version>      -> out/r2-*-<version>.svg
Reuses the primitives in build.py (cap 140, stem 24, fold line 56..78).
"""
import math, sys
import build as b
from build import rect, poly, lens, xf, svg, S, BASE, FT, FB

U = 0.70711

# ---------- fashion wordmark: wider spacing, 45° fold cut on the A apex, softer t foot ----------
def g_A2():
    t15 = math.tan(math.radians(15))
    run, top = BASE * t15, 25
    w = 2 * run + top
    lw = S / math.cos(math.radians(15))
    # 45° cut from the left leg to the right apex corner: x(y) + y = run + top
    yc = top / (1 - t15)
    xc = run - yc * t15
    outer = poly([(0, BASE), (xc, yc), (run + top, 0), (w, BASE), (w - lw, BASE),
                  (w - lw - (BASE - 112) * t15, 112), (lw + (BASE - 112) * t15, 112), (lw, BASE)])
    yb = 90
    xl, xr = lw + (BASE - yb) * t15, w - lw - (BASE - yb) * t15
    yapex = BASE - (w - 2 * lw) / (2 * t15)
    return [outer, poly([(xl, yb), ((xl + xr) / 2, yapex), (xr, yb)], hole=True)], w

def g_t2(x0=0, bar=True):
    st0, st1 = 14, 14 + S
    subs = [poly([(st0, 38), (st1, 14), (st1, 104), (st0, 104)])]   # stem stops where the foot arc starts (no lump)
    if bar:
        subs.append(rect(0, FT, 62, FB))
    subs.append([('M', st1, 102), ('A', 12, 0, 0, 50, 116), ('L', 62, 116), ('L', 62, BASE), ('L', 50, BASE),
                 ('A', 36, 0, 1, st0, 104), ('Z',)])
    return [xf(s, 1, x0) for s in subs], 62

def fashion_wordmark(bh=0):
    saved = (b.g_A, b.g_t, dict(b.GAP))
    b.g_A, b.g_t = g_A2, g_t2
    b.GAP.update({k: v + 7 for k, v in b.GAP.items()})
    b.GAP[('P', 't')] += 2
    b.GAP[('B', 'H')] += bh
    try:
        subs, w = b.wordmark("leaf")
        dot = b.DOT_INDEX[0]
    finally:
        b.g_A, b.g_t = saved[0], saved[1]
        b.GAP.clear(); b.GAP.update(saved[2])
    return subs, w, dot

# ---------- symbols ----------
def leaf(c, d, g, L, h):
    """Kawung leaf on direction d (unit vector) from centre c, starting g from centre, length L, half-width h."""
    p = (c[0] + d[0] * g, c[1] + d[1] * g)
    q = (c[0] + d[0] * (g + L), c[1] + d[1] * (g + L))
    return lens(p, q, h)

def half_leaf(p, q, h, side=1):
    """Leaf folded along its vein p->q: straight crease + one arc (radius of the full leaf)."""
    L = math.dist(p, q)
    r = (L * L / 4 + h * h) / (2 * h)
    return [('M', *p), ('A', r, 0, 1 if side > 0 else 0, *q), ('Z',)]

def fit(subs, box=224, extra=()):
    pts = [(c[1], c[2]) for s in subs for c in s if c[0] in 'ML'] + \
          [(c[4], c[5]) for s in subs for c in s if c[0] == 'A'] + list(extra)
    # include arc bulges approximately via sampling handled by caller margins
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    k = box / max(max(xs) - min(xs), max(ys) - min(ys))
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    return [xf(s, k, 128 - cx * k, 128 - cy * k) for s in subs]

def sym_folded():
    """A2: three kawung leaves + the top-right leaf folded in half along its 45° vein."""
    c, g, L, h = (128, 128), 21, 122, 40
    subs = [leaf(c, (U, U), g, L, h), leaf(c, (-U, U), g, L, h), leaf(c, (-U, -U), g, L, h)]
    p = (c[0] + U * g, c[1] - U * g)
    q = (c[0] + U * (g + L), c[1] - U * (g + L))
    subs.append(half_leaf(p, q, h, side=1))      # keeps the half toward the top
    return subs

def sym_knot():
    """A1: the furoshiki knot. The kawung's four leaves swing round to ±25° from horizontal and are tied
    through a centre knot: a square cloth knotted, seen from above (a bow made of batik leaves)."""
    c = (128, 128)
    g, L, h = 26, 100, 30
    subs = []
    for sx in (1, -1):
        for sy in (1, -1):
            a = math.radians(25)
            a = math.radians(30)
            subs.append(leaf((128, 128 + sy * 9), (sx * math.cos(a), sy * math.sin(a)), g, L, h))
    subs.append(lens((128, 128 - 34), (128, 128 + 34), 13))      # the knot: cloth pinched by the tie
    return fit(subs, 228)
def sym_leafb():
    """A3: a B whose two bowls are kawung leaves folded along the stem (half-leaves)."""
    st = 30
    gap = 8
    xs = 0
    sx = xs + st + gap
    upper = half_leaf((sx, 0), (sx, 104), 62, side=1)
    lower = half_leaf((sx, 92), (sx, 216), 76, side=1)
    stem = rect(xs, 0, xs + st, 216)
    return fit([stem, upper, lower], 216, [(sx + 51, 154)])

def g_Bleaf():
    """Leaf B for the wordmark: stem + two half-leaf bowls, gap 9."""
    sx = S + 6
    return [rect(0, 0, S, BASE), half_leaf((sx, 0), (sx, 68), 42, 1), half_leaf((sx, 58), (sx, BASE), 51, 1)], sx + 51

def leafb_wordmark():
    saved = b.g_B
    b.g_B = g_Bleaf
    try:
        return fashion_wordmark(bh=-12)
    finally:
        b.g_B = saved

def sym_kawung():
    return b.sym_kawung()

if __name__ == "__main__":
    V = sys.argv[1] if len(sys.argv) > 1 else "v1"
    b.V = "r2" + V
    word, ww, dot = fashion_wordmark()
    pad = 58
    out = [svg("wordmark-fashion", ww + 2 * pad, 256, [("#000", [xf(s, 1, pad, pad) for s in word])], "BHAPtik wordmark")]
    syms = {"a0": sym_kawung(), "a1": sym_knot(), "a2": sym_folded(), "a3": sym_leafb()}
    for k, s in syms.items():
        out.append(svg(f"{k}-symbol", 256, 256, [("#000", s)], "BHAPtik symbol"))
        if k == "a3":
            wl, wwl, _ = leafb_wordmark()
            out.append(svg("a3-lockup", wwl + 2 * pad, 256, [("#000", [xf(s2, 1, pad, pad) for s2 in wl])], "BHAPtik logo"))
            continue
        lk, lw = b.lockup(s, word, ww)
        out.append(svg(f"{k}-lockup", lw, 256, [("#000", lk)], "BHAPtik logo"))
    print("\n".join(out))
