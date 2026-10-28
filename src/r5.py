"""Round 5: furoshiki x parang x seigaiha (no kawung). Quick concept peek.
  K1 Wrapped Wave  square bundle, leaf-tip ears; two parang blades + a row of three seigaiha arcs cut into the cloth
  K2 Parang Tie    rounded bundle; the tie is one parang blade through the knot; two nested seigaiha arcs
  K3 Wave Bundle   round bundle; S-curved parang ears; a three-ring seigaiha fan
Run: python r5.py <version> -> out/k*-r5<v>.svg
"""
import math, sys
import build as b
import r2
from build import circle, svg
from r4 import reverse, mirror_x, rrect, half

def _area(sub):
    """Signed area (positive = clockwise on screen), arcs included."""
    a, cur, start = 0.0, None, None
    for c in sub:
        if c[0] == 'M':
            cur = start = (c[1], c[2])
        elif c[0] in 'LA':
            nxt = (c[1], c[2]) if c[0] == 'L' else (c[4], c[5])
            a += (cur[0] * nxt[1] - nxt[0] * cur[1]) / 2
            if c[0] == 'A':
                r, ch = c[1], math.dist(cur, nxt)
                th = 2 * math.asin(min(1, ch / (2 * r)))
                if c[2]:
                    th = 2 * math.pi - th
                seg = r * r / 2 * (th - math.sin(th))
                a += seg if c[3] else -seg
            cur = nxt
        elif c[0] == 'Z':
            a += (cur[0] * start[1] - start[0] * cur[1]) / 2
    return a

def orient(sub, hole=False):
    return reverse(sub) if (_area(sub) > 0) == hole else sub

def _r(p, q, h):
    c = math.dist(p, q)
    return (c * c / 4 + h * h) / (2 * h)

def ring(cx, by, R, r):
    """Seigaiha half-ring sitting on y=by (r=0 gives a half disc)."""
    if r <= 0:
        return [('M', cx - R, by), ('A', R, 0, 1, cx + R, by), ('Z',)]
    return [('M', cx - R, by), ('A', R, 0, 1, cx + R, by), ('L', cx + r, by),
            ('A', r, 0, 0, cx - r, by), ('Z',)]

def blade(p, q, w, h):
    """Parang blade: S-shaped, tapered at both ends, max width w at the middle."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy)
    n = (-dy / L, dx / L)
    m = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
    m1 = (m[0] + n[0] * w / 2, m[1] + n[1] * w / 2)
    m2 = (m[0] - n[0] * w / 2, m[1] - n[1] * w / 2)
    return [('M', *p), ('A', _r(p, m1, h), 0, 1, *m1), ('A', _r(m1, q, h), 0, 0, *q),
            ('A', _r(q, m2, h), 0, 1, *m2), ('A', _r(m2, p, h), 0, 0, *p), ('Z',)]

def ears(p, ang, L, h):
    a = math.radians(ang)
    q = (p[0] + L * math.cos(a), p[1] - L * math.sin(a))
    right = orient(half(q, p, h))
    return [right, orient(mirror_x(right))]

def k1():
    body = orient(rrect(28, 104, 228, 232, 22))
    knot = orient(circle(128, 98, 18))
    holes = [blade((60, 190), (124, 126), 28, 10), blade((132, 190), (196, 126), 28, 10)]
    holes += [ring(cx, 220, 22, 10) for cx in (72, 128, 184)]
    return [body, knot] + ears((138, 96), 30, 92, 26) + [orient(h, True) for h in holes]

def k2():
    body = orient([('M', 20, 222), ('A', 108, 0, 1, 236, 222), ('Z',)])
    knot = orient(circle(128, 104, 18))
    r_ear = orient(blade((136, 104), (228, 62), 30, 10))
    holes = [ring(128, 210, 76, 60), ring(128, 210, 48, 32), ring(128, 210, 18, 0)]
    return [body, knot, r_ear, orient(mirror_x(r_ear))] + [orient(h, True) for h in holes]

def k3():
    body = orient(rrect(28, 104, 228, 232, 30))
    knot = orient(circle(128, 98, 18))
    holes = [blade((64, 216), (190, 122), 40, 16), ring(190, 218, 22, 10), ring(66, 150, 22, 10)]
    return [body, knot] + ears((138, 96), 30, 92, 26) + [orient(h, True) for h in holes]

if __name__ == "__main__":
    V = sys.argv[1] if len(sys.argv) > 1 else "v1"
    b.V = "r5" + V
    word, ww, di = r2.fashion_wordmark()
    for k, s in {"k1": k1(), "k2": k2(), "k3": k3()}.items():
        s = [b.xf(p, 1, 0, -10) for p in s]
        print(svg(f"{k}-symbol", 256, 256, [("#000", s)], "BHAPtik symbol"))
        lk, lw = b.lockup(s, word, ww)
        print(svg(f"{k}-lockup", lw, 256, [("#000", lk)], "BHAPtik logo"))
