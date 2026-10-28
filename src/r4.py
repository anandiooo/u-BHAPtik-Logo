"""BHAPtik round 4: batik x Japanese merges on the Folded Leaf.
  J1 Kawung Mon     folded-leaf kawung cut out of a disc: a kamon crest that is also a four-hole button
  J2 Furoshiki Knot a wrapped cloth bundle; its tied corners are folded leaves; kawung cut into the body
  J3 Hanko Seal     the folded-leaf mark cut out of a square name seal (secondary stamp)
  J4 Sashiko Crease the folded leaf's crease mended with a sashiko running stitch (pink)
  J5 Tategaki Label vertical lockup for woven neck labels and hang tags
Japanese side = structure and technique only (crest, seal, stitch, knot, vertical setting); no Japanese imagery.
Run: python r4.py <version>  -> out/j*-r4<v>.svg
"""
import math, os, sys
import build as b
import r2
from build import rect, poly, lens, xf, circle, svg, d_of, BASE, S

U = 0.70711
TR, TL, BR, BL = (U, -U), (-U, -U), (U, U), (-U, U)
CREAM, BLACK, BROWN, PINK = "#F3EBDD", "#1A1614", "#6E4B36", "#E9A3A6"

# ---------- helpers ----------
def reverse(sub):
    """Reverse a closed subpath (turns a solid into a hole under the nonzero rule)."""
    segs, start, cur = [], None, None
    for c in sub:
        if c[0] == 'M':
            start = cur = (c[1], c[2])
        elif c[0] == 'L':
            segs.append(('L', cur, (c[1], c[2]))); cur = (c[1], c[2])
        elif c[0] == 'A':
            segs.append(('A', cur, (c[4], c[5]), c[1], c[2], c[3])); cur = (c[4], c[5])
        elif c[0] == 'Z' and math.dist(cur, start) > 0.01:
            segs.append(('L', cur, start))
    out = [('M', *segs[-1][2])]
    for s in reversed(segs):
        out.append(('L', *s[1]) if s[0] == 'L' else ('A', s[3], s[4], 1 - s[5], *s[1]))
    out.append(('Z',))
    return out

def mirror_x(sub, ax=128):
    out = []
    for c in sub:
        if c[0] in 'ML':
            out.append((c[0], 2 * ax - c[1], c[2]))
        elif c[0] == 'A':
            out.append(('A', c[1], c[2], 1 - c[3], 2 * ax - c[4], c[5]))
        else:
            out.append(c)
    return reverse(out)

def rrect(x0, y0, x1, y1, r):
    return [('M', x0 + r, y0), ('L', x1 - r, y0), ('A', r, 0, 1, x1, y0 + r), ('L', x1, y1 - r),
            ('A', r, 0, 1, x1 - r, y1), ('L', x0 + r, y1), ('A', r, 0, 1, x0, y1 - r), ('L', x0, y0 + r),
            ('A', r, 0, 1, x0 + r, y0), ('Z',)]

def tips(c, d, g, L):
    return (c[0] + d[0] * g, c[1] + d[1] * g), (c[0] + d[0] * (g + L), c[1] + d[1] * (g + L))

def half(p, q, h):
    """leaf folded along its vein p->q: crease + one arc, bulging to the left of p->q."""
    L = math.dist(p, q)
    r = (L * L / 4 + h * h) / (2 * h)
    return [('M', *p), ('A', r, 0, 1, *q), ('Z',)]

def folded(c=(128, 128), g=21, L=122, h=40):
    """the round-2 Folded Leaf: three kawung leaves + the top-right one folded along its 45° vein."""
    out = [lens(*tips(c, d, g, L), h) for d in (BR, BL, TL)]
    out.append(half(*tips(c, TR, g, L), h))
    return out

# ---------- J1 ----------
def j1_mon():
    return [circle(128, 128, 120)] + [reverse(s) for s in folded((128, 128), g=20, L=86, h=29)]

# ---------- J2 ----------
def j2_knot():
    """front view of a furoshiki bundle: the knot sits on the cloth, the two tied corners
    are folded leaves flying out at 30° above horizontal; a small kawung is cut into the body."""
    body = rrect(30, 116, 226, 232, 28)
    knot = circle(128, 110, 16)
    L, h, a = 98, 28, math.radians(15)
    p = (140, 104)
    q = (p[0] + math.cos(a) * L, p[1] - math.sin(a) * L)
    right_ear = half(p, q, h)                     # bulges upward
    left_ear = mirror_x(right_ear)
    holes = [reverse(s) for s in folded((128, 175), g=9, L=40, h=14)]
    return [xf(s, 1, 0, -5) for s in [body, knot, right_ear, left_ear] + holes]

# ---------- J3 ----------
def j3_seal():
    return [rrect(20, 20, 236, 236, 22)] + [reverse(s) for s in folded((128, 128), g=20, L=100, h=33)]

# ---------- J4 ----------
def j4_sashiko(off=14, w=3.5):
    """three running stitches sewn into the folded half, parallel to the crease (cut as holes in
    the mono master; drawn in pink on top in colour)."""
    base = folded()
    P = lambda s, o: (128 + TR[0] * s + TL[0] * o, 128 + TR[1] * s + TL[1] * o)
    stitches = []
    for i in range(3):
        s0 = 46 + i * 28
        s1 = s0 + 16
        stitches.append(poly([P(s0, off - w), P(s1, off - w), P(s1, off + w), P(s0, off + w)]))
    return base, stitches

# ---------- J5 ----------
def i_leaf():
    subs, w = b.g_i("none")
    subs.append(lens((S / 2 - 16, 24 + 16), (S / 2 + 16, 24 - 16), 16))   # label-size dot, 1.25x
    return subs, w

def j5_label(k=0.62, gap=26):
    """symbol on top, letters stacked top-to-bottom with equal optical gaps (tategaki setting)."""
    out = [xf(s, 0.66, 128 - 128 * 0.66, 30) for s in folded()]
    y = 30 + 256 * 0.66 - 22 + gap
    for (g, w), top in ((b.g_B(), 0), (b.g_H(), 0), (r2.g_A2(), 0), (b.g_P(), 0),
                        (r2.g_t2(), 14), (i_leaf(), 6), (b.g_k(), 0)):
        out += [xf(s, k, 128 - w * k / 2, y - top * k) for s in g]
        y += (BASE - top) * k + gap
    return out, round(y - gap + 40)

# ---------- shelf-test generics (test only) ----------
def make_refs():
    D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "refs")
    def save(n, subs):
        open(os.path.join(D, n + ".svg"), "w").write(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256"><path fill="#000" d="{d_of(subs)}"/></svg>\n')
    save("ref-button", [circle(128, 128, 116)] +
         [circle(128 + dx, 128 + dy, 18, hole=True) for dx, dy in ((-30, -30), (30, -30), (-30, 30), (30, 30))])
    ring = [circle(128, 128, 118), circle(128, 128, 104, hole=True)]
    petals = [circle(128 + 58 * math.cos(a), 128 + 58 * math.sin(a), 32)
              for a in (math.radians(-90 + 72 * i) for i in range(5))]
    save("ref-mon", ring + petals + [circle(128, 128, 28)])
    save("ref-seal", [rect(20, 20, 236, 236), poly([(40, 40), (216, 40), (216, 216), (40, 216)], hole=True),
                      rect(64, 64, 192, 192)])

if __name__ == "__main__":
    V = sys.argv[1] if len(sys.argv) > 1 else "v1"
    b.V = "r4" + V
    make_refs()
    word, ww, di = r2.fashion_wordmark()
    base4, st4 = j4_sashiko()
    syms = {"j1": j1_mon(), "j2": j2_knot(), "j3": j3_seal(), "j4": base4 + [reverse(s) for s in st4]}
    for k, s in syms.items():
        print(svg(f"{k}-symbol", 256, 256, [("#000", s)], "BHAPtik symbol"))
        lk, lw = b.lockup(s, word, ww)
        print(svg(f"{k}-lockup", lw, 256, [("#000", lk)], "BHAPtik logo"))
    print(svg("j4-symbol-small", 256, 256, [("#000", base4)], "BHAPtik symbol, small sizes"))
    # J3 as a stamp after the wordmark
    kw, cap = 96 / BASE, 96
    wsubs = [xf(s, kw, 40, 128 - cap / 2) for s in word]
    sx = 40 + ww * kw + 30
    seal = [xf(s, cap / 256, sx, 128 - cap / 2) for s in syms["j3"]]
    print(svg("j3-stamp-lockup", sx + cap + 40, 256, [("#000", wsubs + seal)], "BHAPtik logo with seal"))
    lab, lh = j5_label()
    print(svg("j5-label", 256, lh, [("#000", lab)], "BHAPtik vertical label"))
