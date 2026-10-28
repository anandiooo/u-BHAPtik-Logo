"""Round 5b: rigid furoshiki x parang x seigaiha, merged like logo-idea-1.
Built as one luminance mask over a single ink colour (painter order = folds overlap cleanly),
constant stroke and gap everywhere, straight-edged ears, exact 45deg parang, regular seigaiha grid.
  M1 Crest   round bundle, V opening: parang S-chains above, seigaiha rows below
  M2 Box     square bundle, parang S-chains cut into both flaps, seigaiha in the opening
  M3 Diamond flat-wrap diamond, four folded flaps around a window of parang over seigaiha
Run: python r5b.py v1 -> out/m*-symbol-r5b<v>.svg, out/m*-lockup-r5b<v>.svg
Production note: flatten mask -> Pathfinder/Expand before embroidery or cutting.
"""
import math, os, sys
import build as b
import r2

INK, GAP, W = "#000", 8, 8          # ink colour, gap between folds, pattern stroke

def P(pts):
    return "M" + " L".join(f"{x:g} {y:g}" for x, y in pts) + " Z"

def mx(pts):
    return [(256 - x, y) for x, y in pts][::-1]

def white(d, gap=True, extra=""):
    s = f' stroke="#000" stroke-width="{2 * GAP}" paint-order="stroke" stroke-linejoin="miter"' if gap else ""
    return f'<path d="{d}" fill="#fff"{s}{extra}/>'

def circ(cx, cy, r):
    return f"M{cx - r} {cy} A{r} {r} 0 1 0 {cx + r} {cy} A{r} {r} 0 1 0 {cx - r} {cy} Z"

def chains(starts, n=12, r=6, w=None):
    """Parang band on an exact 45deg: a bold S-chain (semicircles of one radius) between two
    straight rails, like a lereng stripe. Rails give it the same ring-like rhythm as seigaiha."""
    w = w or W + 2
    L = 2 * r * n
    off = r + w / 2 + 6
    seg = "".join(f" a{r} {r} 0 0 {k % 2} {2 * r} 0" for k in range(n))
    d = f"M0 0{seg} M0 {-off:g} H{L} M0 {off:g} H{L}"
    return "".join(f'<path d="{d}" transform="translate({x} {y}) rotate(-45)" fill="none" '
                   f'stroke="#fff" stroke-width="{w}"/>' for x, y in starts)

def seigaiha(x0, y0, R, rows, cols):
    """Seigaiha: regular grid, dx 2R, dy R/2, odd rows offset R; later rows overlap earlier ones."""
    out = []
    for i in range(rows):
        for j in range(-1, cols + 1):
            cx, cy = x0 + j * 2 * R + (i % 2) * R, y0 + i * R / 2
            out.append(f'<circle cx="{cx:g}" cy="{cy:g}" r="{R}" fill="#000"/>')
            for rr in (R - 7, R - 19):
                out.append(f'<circle cx="{cx:g}" cy="{cy:g}" r="{rr}" fill="none" stroke="#fff" stroke-width="{W}"/>')
            out.append(f'<circle cx="{cx:g}" cy="{cy:g}" r="{R - 29}" fill="#fff"/>')
    return "".join(out)

def cloth(key, d, xs, y, r=10, w=None):
    """Parang printed on the cloth itself: bands cut out of the solid flaps."""
    bands = chains([(x, y) for x in xs], n=14, r=r, w=w).replace('stroke="#fff"', 'stroke="#000"')
    rim = f'<path d="{d}" fill="none" stroke="#fff" stroke-width="24"/>'   # 12-unit solid hem keeps the silhouette
    return f'<clipPath id="{key}"><path d="{d}"/></clipPath><g clip-path="url(#{key})">{bands}{rim}</g>'

EAR = [(140, 56), (212, 14), (224, 34), (148, 78)]
def tie(cy=62):
    ears = white(P(EAR)) + white(P(mx(EAR)))
    return ears + white(circ(128, cy, 18))

def window(key, shape, inner):
    """Opening: cut a gap around `shape`, then paint `inner` clipped to it."""
    return (f'<clipPath id="{key}"><path d="{shape}"/></clipPath>'
            f'<path d="{shape}" fill="#000" stroke="#000" stroke-width="{2 * GAP}"/>'
            f'<g clip-path="url(#{key})">{inner}</g>')

def m1():
    body = circ(128, 150, 90)
    # opening = V from the knot, bounded by the body circle (intersect via nested clip)
    v = P([(128, 96), (238, 300), (18, 300)])
    inner = (f'<clipPath id="c1"><path d="{circ(128, 150, 90 - GAP)}"/></clipPath><g clip-path="url(#c1)">'
             + seigaiha(128, 128, 36, 7, 2) + "</g>")
    return white(body, gap=False) + cloth("f1", body, range(-90, 340, 76), 250) + window("o1", v, inner) + tie()

def m2():
    body = P([(44, 92), (212, 92), (212, 236), (44, 236)])
    v = P([(128, 100), (200, 236), (56, 236)])
    flap = cloth("f2", body, range(-90, 340, 76), 250)
    inner = seigaiha(128, 168, 36, 5, 2)
    return white(body, gap=False) + flap + window("o2", v, inner) + tie(66)

def m3():
    body = P([(128, 58), (228, 150), (128, 242), (28, 150)])
    win = P([(128, 104), (178, 150), (128, 196), (78, 150)])
    folds = "".join(f'<path d="M{a} L{c}" stroke="#000" stroke-width="{GAP}"/>' for a, c in
                    (("78 150", "28 150"), ("178 150", "228 150"), ("128 196", "128 242")))
    inner = seigaiha(128, 118, 26, 7, 2)
    return white(body, gap=False) + cloth("f3", body, range(-60, 340, 64), 250, r=8, w=10) + folds + window("o3", win, inner) + tie(56)


def parang(x0, y0, nb=9, nk=3, s=26, per=76, L=26, b=14, w=10, bw=13, ds=4, dsp=26):
    """Parang rusak: diagonal bands of upright S-blades, split by a solid bar with mlinjo diamonds.
    Blades and bars are ink, gaps are cloth; bands run at an exact 45deg."""
    u, n = (0.70711, 0.70711), (-0.70711, 0.70711)
    out = []
    for k in range(-nk, nk + 1):
        ox, oy = x0 + k * per * n[0], y0 + k * per * n[1]
        for j in range(-nb, nb + 1):
            cx, cy = ox + j * s * u[0], oy + j * s * u[1]
            # blade axis runs across the band (perpendicular), so neighbours nest with a constant gap
            out.append(f'<path d="M0 {-L} Q{b} {-L / 2} 0 0 T0 {L}" transform="translate({cx:.1f} {cy:.1f}) rotate(45)" '
                       f'fill="none" stroke="#fff" stroke-width="{w}" stroke-linecap="round"/>')
        bx, by = ox + per / 2 * n[0], oy + per / 2 * n[1]
        out.append(f'<path d="M{bx - 300 * u[0]:.1f} {by - 300 * u[1]:.1f} L{bx + 300 * u[0]:.1f} {by + 300 * u[1]:.1f}" '
                   f'stroke="#fff" stroke-width="{bw}"/>')
        for j in range(-16, 17):
            dx, dy = bx + j * dsp * u[0], by + j * dsp * u[1]
            out.append(f'<path d="{P([(dx - ds, dy), (dx, dy - ds), (dx + ds, dy), (dx, dy + ds)])}" fill="#000"/>')
    return "".join(out)

def rrect_d(x0, y0, x1, y1, r):
    return (f"M{x0 + r} {y0} H{x1 - r} A{r} {r} 0 0 1 {x1} {y0 + r} V{y1 - r} A{r} {r} 0 0 1 {x1 - r} {y1} "
            f"H{x0 + r} A{r} {r} 0 0 1 {x0} {y1 - r} V{y0 + r} A{r} {r} 0 0 1 {x0 + r} {y0} Z")

def m1b():
    """M1 refined: parang-rusak cloth, hemmed edges, gathered pleats, cloth-corner ears, tied knot."""
    body = circ(128, 152, 90)
    v = P([(128, 98), (192, 306), (64, 306)])
    cloth = (f'<clipPath id="f1"><path d="{body}"/></clipPath><g clip-path="url(#f1)">'
             f'<path d="{body}" fill="#000"/>{parang(128, 152)}'
             f'<path d="{body}" fill="none" stroke="#fff" stroke-width="18"/>'          # outer hem
             f'<path d="{v}" fill="none" stroke="#fff" stroke-width="{2 * (GAP + 6)}"/>'  # hem along the opening
             + "".join(f'<path d="M128 92 L{128 + 70 * sx:.1f} {92 + 70 * sy:.1f}" stroke="#000" stroke-width="5"/>'
                       for sx, sy in ())  # pleats
             + "</g>")
    inner = (f'<clipPath id="c1"><path d="{circ(128, 152, 90 - GAP)}"/></clipPath><g clip-path="url(#c1)">'
             + seigaiha(128, 130, 36, 7, 2) + "</g>")
    ear = "M140 62 L222 20 A70 70 0 0 1 150 88 Z"            # cloth corner: one straight edge, one arc
    ears = white(ear) + f'<g transform="translate(256 0) scale(-1 1)">{white(ear)}</g>'
    knot = white(rrect_d(106, 50, 150, 88, 14))
    return white(body, gap=False) + cloth + window("o1", v, inner) + ears + knot

def m1c():
    """Furoshiki read first: wide wrapped box, big knot + leaf ears (as in furoshiki.png).
    Gathered cloth under the knot = parang rusak; folded front corner (reverse face) = seigaiha."""
    body = "M28 132 A20 20 0 0 1 48 112 H208 A20 20 0 0 1 228 132 V204 L128 240 L28 204 Z"
    U = P([(128, 86), (228, 164), (28, 164)])          # gathered cloth from knot to the side corners
    F = P([(28, 164), (228, 164), (128, 240)])         # folded front corner
    def panel(key, d, inner):
        return (f'<clipPath id="{key}"><path d="{d}"/></clipPath>'
                f'<path d="{d}" fill="#000" stroke="#000" stroke-width="{2 * GAP}"/>'
                f'<g clip-path="url(#{key})">{inner}<path d="{d}" fill="none" stroke="#fff" stroke-width="14"/></g>')
    par = parang(128, 150, nb=14, nk=4, s=24, per=64, L=18, b=10, w=12, bw=10, ds=3.5, dsp=20)
    sei = seigaiha(8, 162, 34, 6, 4)
    ear = "M146 72 A73 73 0 0 1 226 28 A73 73 0 0 1 146 72 Z"
    ears = white(ear) + f'<g transform="translate(256 0) scale(-1 1)">{white(ear)}</g>'
    knot = white(rrect_d(104, 58, 152, 94, 14))
    folds = f'<path d="M28 164 L128 86 L228 164" fill="none" stroke="#000" stroke-width="{GAP}"/>'
    whole = f'<path d="{body}"/><path d="{U}"/>'
    cloth = (f'<clipPath id="pb">{whole}</clipPath><g clip-path="url(#pb)"><rect width="256" height="256" fill="#000"/>{par}'
             f'<path d="{body}" fill="none" stroke="#fff" stroke-width="16"/><path d="{U}" fill="none" stroke="#fff" stroke-width="16"/></g>')
    return (white(body, gap=False) + white(U, gap=False) + cloth + folds + panel("pf", F, sei)
            + ears + knot)

def m1d():
    """Two big uninterrupted fields so each pattern reads: parang cloth on top, seigaiha below the fold."""
    body = P([(28, 236), (28, 128), (100, 94), (156, 94), (228, 128), (228, 236)])
    top = P([(20, 166), (20, 128), (100, 86), (156, 86), (236, 128), (236, 166)])
    bot = P([(20, 174), (236, 174), (236, 250), (20, 250)])
    par = parang(128, 128, nb=14, nk=3, s=24, per=62, L=20, b=11, w=13, bw=10, ds=3.5, dsp=20)
    sei = seigaiha(0, 190, 32, 4, 4)
    def field(key, clip, inner):
        return (f'<clipPath id="{key}"><path d="{body}"/></clipPath><clipPath id="{key}2"><path d="{clip}"/></clipPath>'
                f'<g clip-path="url(#{key})"><g clip-path="url(#{key}2)"><rect width="256" height="256" fill="#000"/>{inner}</g>'
                f'<path d="{body}" fill="none" stroke="#fff" stroke-width="18"/></g>')
    fold = f'<path d="M20 170 H236" stroke="#000" stroke-width="{GAP}"/>'
    ear = "M146 72 A73 73 0 0 1 226 28 A73 73 0 0 1 146 72 Z"
    ears = white(ear) + f'<g transform="translate(256 0) scale(-1 1)">{white(ear)}</g>'
    knot = white(rrect_d(104, 56, 152, 92, 14))
    return (white(body, gap=False) + field("ft", top, par) + field("fb", bot, sei) + fold
            + f'<path d="M20 170 H236" stroke="#fff" stroke-width="0"/>' + ears + knot)

def m1e():
    """Pillow-shaped bundle gathered into the knot; parang cloth, seigaiha waves rising into it (no fold gap)."""
    body = ("M104 88 Q42 100 32 166 L30 212 Q30 238 56 238 L200 238 Q226 238 226 212 "
            "L224 166 Q214 100 152 88 Z")
    par = parang(128, 118, nb=14, nk=3, s=20, per=72, L=18, b=12, w=14, bw=12, ds=4, dsp=22)
    pleats = "".join(f'<path d="M{128 + 30 * sx} 96 L{128 + 92 * sx} {96 + 46 * k}" stroke="#000" stroke-width="5"/>'
                     for sx in (-1, 1) for k in (0.55, 1.1))
    sei = seigaiha(0, 202, 32, 4, 4)
    cloth = (f'<clipPath id="b1"><path d="{body}"/></clipPath><g clip-path="url(#b1)">'
             f'<rect width="256" height="256" fill="#000"/>{par}{pleats}{sei}'
             f'<path d="{body}" fill="none" stroke="#fff" stroke-width="18"/></g>')
    ear = "M148 70 A70 70 0 0 1 220 18 A70 70 0 0 1 148 70 Z"
    ears = white(ear) + f'<g transform="translate(256 0) scale(-1 1)">{white(ear)}</g>'
    knot = white(rrect_d(104, 54, 152, 92, 14))
    return white(body, gap=False) + cloth + ears + knot

def blade_d(L, b, wmax, wmin, n=20):
    """Filled parang blade (local coords, axis vertical): S-centreline, two swelling lobes,
    a narrower waist at the crossing and pointed tips."""
    left, right = [], []
    for i in range(n + 1):
        t = -1 + 2 * i / n
        cx, cy = b * math.sin(math.pi * t), L * t
        dx, dy = b * math.pi * math.cos(math.pi * t), L
        m = math.hypot(dx, dy)
        nx, ny = dy / m, -dx / m
        hw = (wmin + (wmax - wmin) * abs(math.sin(math.pi * t))) * math.cos(math.pi * t / 2) ** 0.3 / 2
        left.append((cx + nx * hw, cy + ny * hw))
        right.append((cx - nx * hw, cy - ny * hw))
    pts = left + right[::-1]
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"

def parang2(x0, y0, nb=14, nk=3, s=19, per=70, L=19, b=6, wmax=15, wmin=11, bw=12, ds=4, dsp=22, bars=True):
    """Parang rusak with filled lobed blades nested across each 45deg band, mlinjo bars between bands."""
    u, n = (0.70711, 0.70711), (-0.70711, 0.70711)
    bd = blade_d(L, b, wmax, wmin)
    out = []
    for k in range(-nk, nk + 1):
        ox, oy = x0 + k * per * n[0], y0 + k * per * n[1]
        for j in range(-nb, nb + 1):
            cx, cy = ox + j * s * u[0], oy + j * s * u[1]
            out.append(f'<path d="{bd}" transform="translate({cx:.1f} {cy:.1f}) rotate(45)" fill="#fff"/>')
        if bars:
            bx, by = ox + per / 2 * n[0], oy + per / 2 * n[1]
            out.append(f'<path d="M{bx - 300 * u[0]:.1f} {by - 300 * u[1]:.1f} L{bx + 300 * u[0]:.1f} {by + 300 * u[1]:.1f}" '
                       f'stroke="#fff" stroke-width="{bw}"/>')
            for j in range(-16, 17):
                dx, dy = bx + j * dsp * u[0], by + j * dsp * u[1]
                out.append(f'<path d="{P([(dx - ds, dy), (dx, dy - ds), (dx + ds, dy), (dx, dy + ds)])}" fill="#000"/>')
    return "".join(out)

BODY = ("M104 88 Q42 100 32 166 L30 212 Q30 238 56 238 L200 238 Q226 238 226 212 "
        "L224 166 Q214 100 152 88 Z")
EAR2 = "M146 74 A64 64 0 0 1 212 36 A64 64 0 0 1 146 74 Z"     # shorter, angled further out

def bundle(pattern, pleats=True):
    """Shared furoshiki: hem (ink) + cream keyline + pattern field, tied knot, cloth-corner ears."""
    pl = "".join(f'<path d="M{128 + 30 * sx} 98 L{128 + 92 * sx} {98 + 46 * k}" stroke="#000" stroke-width="6"/>'
                 for sx in (-1, 1) for k in (0.55, 1.1)) if pleats else ""
    cloth = (f'<clipPath id="b1"><path d="{BODY}"/></clipPath><g clip-path="url(#b1)">'
             f'<rect width="256" height="256" fill="#000"/>{pattern}{pl}'
             f'<path d="{BODY}" fill="none" stroke="#000" stroke-width="32"/>'      # cream keyline (6) inside the hem
             f'<path d="{BODY}" fill="none" stroke="#fff" stroke-width="20"/></g>')  # ink hem (10)
    ears = white(EAR2) + f'<g transform="translate(256 0) scale(-1 1)">{white(EAR2)}</g>'
    knot = (white(rrect_d(104, 54, 152, 94, 14))
            + '<path d="M104 68 H152 M104 80 H152" stroke="#000" stroke-width="4"/>')  # wrap band across the knot
    return white(BODY, gap=False) + cloth + ears + knot

def m1f():
    """A3 refined: filled lobed parang blades, clean hem keyline, banded knot, shorter outward ears."""
    return bundle(parang(128, 118, nb=14, nk=3, s=20, per=72, L=18, b=12, w=14, bw=12, ds=4, dsp=22) + seigaiha(0, 202, 32, 4, 4))

def m1s():
    """Small-size version (16-48 px, favicon, woven label): one parang band, one row of waves, no pleats."""
    return bundle(parang(118, 150, nb=6, nk=0, s=30, per=400, L=26, b=16, w=20, bw=0, ds=0, dsp=400)
                  + seigaiha(0, 226, 44, 1, 3), pleats=False)

def bundle2(pattern):
    """Minimal, fully connected: body, ears and knot are one ink shape (no cream gaps or keyline)."""
    cloth = (f'<clipPath id="b2"><path d="{BODY}"/></clipPath><g clip-path="url(#b2)">'
             f'<rect width="256" height="256" fill="#000"/>{pattern}'
             f'<path d="{BODY}" fill="none" stroke="#fff" stroke-width="22"/></g>')   # solid hem (11)
    ears = white(EAR2, gap=False) + f'<g transform="translate(256 0) scale(-1 1)">{white(EAR2, gap=False)}</g>'
    knot = white(rrect_d(104, 54, 152, 98, 14), gap=False)
    return white(BODY, gap=False) + cloth + ears + knot

def m1g():
    """Minimal A: two large parang bands with one mlinjo bar, two rows of big seigaiha."""
    return bundle2(parang(128, 140, nb=8, nk=1, s=28, per=96, L=24, b=16, w=18, bw=14, ds=5, dsp=30)
                   + seigaiha(0, 214, 40, 2, 3))

def m1gs():
    """Minimal small-size A: one parang band, one row of waves."""
    return bundle2(parang(118, 150, nb=6, nk=0, s=30, per=400, L=26, b=16, w=20, bw=0, ds=0, dsp=400)
                   + seigaiha(0, 226, 44, 1, 3))

def _body_poly(n=24):
    """Polygon approximation of BODY (for keeping pattern pieces clear of the hem)."""
    q = lambda a, c, e, t: ((1 - t) ** 2 * a[0] + 2 * (1 - t) * t * c[0] + t * t * e[0],
                            (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * c[1] + t * t * e[1])
    segs = [((104, 88), (42, 100), (32, 166)), ((30, 212), (30, 238), (56, 238)),
            ((200, 238), (226, 238), (226, 212)), ((224, 166), (214, 100), (152, 88))]
    pts = []
    for a, c, e in segs:
        pts += [q(a, c, e, i / n) for i in range(n + 1)]
    return pts

def _clear(p, poly, m):
    """True if p is inside poly and at least m from every edge."""
    x, y = p
    inside = False
    for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]):
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            inside = not inside
        dx, dy = x2 - x1, y2 - y1
        t = max(0, min(1, ((x - x1) * dx + (y - y1) * dy) / (dx * dx + dy * dy or 1)))
        if math.hypot(x - x1 - t * dx, y - y1 - t * dy) < m:
            return False
    return inside

def m1h():
    """Most minimal A: one parang band of whole blades between two plain bars, one row of three waves."""
    poly = _body_poly()
    u, n = (0.70711, 0.70711), (-0.70711, 0.70711)
    L, bb, w, s, cx0, cy0, half = 22, 13, 16, 26, 136, 146, 40
    blades = []
    for j in range(-5, 6):
        cx, cy = cx0 + j * s * u[0], cy0 + j * s * u[1]
        tips = [(cx + k * L * n[0], cy + k * L * n[1]) for k in (-1, 0, 1)]
        if all(_clear(p, poly, 4) for p in tips) and cy + L < 200:      # whole blades only, clear of the waves
            blades.append(f'<path d="M0 {-L} Q{bb} {-L / 2} 0 0 T0 {L}" transform="translate({cx:.1f} {cy:.1f}) rotate(45)" '
                          f'fill="none" stroke="#fff" stroke-width="{w}" stroke-linecap="round"/>')
    bars = "".join(f'<path d="M{cx0 + k * half * n[0] - 300 * u[0]:.1f} {cy0 + k * half * n[1] - 300 * u[1]:.1f} '
                   f'L{cx0 + k * half * n[0] + 300 * u[0]:.1f} {cy0 + k * half * n[1] + 300 * u[1]:.1f}" '
                   f'stroke="#fff" stroke-width="14"/>' for k in (-1, 1))
    waves = "".join(f'<circle cx="{x}" cy="227" r="38" fill="#000"/>'
                    f'<circle cx="{x}" cy="227" r="30" fill="none" stroke="#fff" stroke-width="9"/>'
                    f'<circle cx="{x}" cy="227" r="13" fill="none" stroke="#fff" stroke-width="9"/>' for x in (62, 128, 194))
    return bundle2("".join(blades) + bars + waves)

def doc(w, h, mask, extra="", sym_tf=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" width="{w:g}" height="{h:g}" role="img" '
            f'aria-labelledby="t"><title id="t">BHAPtik</title><defs><mask id="m" maskUnits="userSpaceOnUse" '
            f'x="0" y="0" width="256" height="256"><rect width="256" height="256" fill="#000"/>{mask}</mask></defs>'
            f'<g{sym_tf}><rect width="256" height="256" fill="{INK}" mask="url(#m)"/></g>{extra}</svg>\n')

if __name__ == "__main__":
    V = "r5b" + (sys.argv[1] if len(sys.argv) > 1 else "v1")
    word, ww, di = r2.fashion_wordmark()
    wsubs, lw = b.lockup([], word, ww)
    wpath = f'<path fill="{INK}" d="{b.d_of(wsubs)}"/>'
    for k, f in {"m1": m1h}.items():
        mk = f()
        for name, txt in ((f"{k}-symbol", doc(256, 256, mk)),
                          (f"{k}-lockup", doc(lw, 256, mk, wpath, f' transform="translate(40 53) scale({150 / 256:.6f})"'))):
            p = os.path.join(b.OUT, f"{name}-{V}.svg")
            open(p, "w", encoding="utf-8").write(txt)
            print(p)
