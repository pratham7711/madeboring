"""True monoline centreline of a glyph, taken from its own outline.

Rasterise the filled outline, thin it to a one-pixel skeleton (Zhang-Suen),
trace that into ordered strokes, push the terminals back out to the real ink
edge, and emit paths in font units. Nothing about the letterform is assumed.
"""
import json, math, os, pathlib, re, sys

SRC = os.environ.get('GLYPHS', 'plex600.json')
OUT = os.environ.get('OUT', 'skeleton-plex.json')
G = json.loads(pathlib.Path(SRC).read_text())
GL, MBP = G['glyphs'], G['mbpos']

TOK = re.compile(r'([MLQCZHV])([^MLQCZHV]*)')
NUM = re.compile(r'-?\d+(?:\.\d+)?')
RES = 3.0          # font units per raster pixel


def flatten(d, steps=24):
    polys, cur, start, pt = [], [], None, (0, 0)
    for cmd, args in TOK.findall(d):
        v = [float(x) for x in NUM.findall(args)]
        if cmd == 'M':
            if cur:
                polys.append(cur)
            pt = (v[0], v[1]); start = pt; cur = [pt]
        elif cmd == 'L':
            for i in range(0, len(v), 2):
                pt = (v[i], v[i + 1]); cur.append(pt)
        elif cmd == 'H':
            for x in v:
                pt = (x, pt[1]); cur.append(pt)
        elif cmd == 'V':
            for y in v:
                pt = (pt[0], y); cur.append(pt)
        elif cmd == 'Q':
            for i in range(0, len(v), 4):
                c, e = (v[i], v[i+1]), (v[i+2], v[i+3])
                for k in range(1, steps + 1):
                    t = k / steps; u = 1 - t
                    cur.append((u*u*pt[0] + 2*u*t*c[0] + t*t*e[0],
                                u*u*pt[1] + 2*u*t*c[1] + t*t*e[1]))
                pt = e
        elif cmd == 'C':
            for i in range(0, len(v), 6):
                c1, c2, e = (v[i], v[i+1]), (v[i+2], v[i+3]), (v[i+4], v[i+5])
                for k in range(1, steps + 1):
                    t = k / steps; u = 1 - t
                    cur.append((u**3*pt[0] + 3*u*u*t*c1[0] + 3*u*t*t*c2[0] + t**3*e[0],
                                u**3*pt[1] + 3*u*u*t*c1[1] + 3*u*t*t*c2[1] + t**3*e[1]))
                pt = e
        elif cmd == 'Z':
            if cur:
                cur.append(start); polys.append(cur); cur = []
            pt = start
    if cur:
        polys.append(cur)
    return polys


def raster(polys, bbox, pad=4):
    x0, y0, x1, y1 = bbox
    W = int((x1 - x0) / RES) + pad * 2
    H = int((y1 - y0) / RES) + pad * 2
    grid = [bytearray(W) for _ in range(H)]
    for j in range(H):
        y = y0 + (j - pad + .5) * RES
        xs = []
        for p in polys:
            for i in range(len(p) - 1):
                (ax, ay), (bx, by) = p[i], p[i + 1]
                if (ay <= y < by) or (by <= y < ay):
                    xs.append(ax + (y - ay) * (bx - ax) / (by - ay))
        xs.sort()
        for k in range(0, len(xs) - 1, 2):
            a = int((xs[k] - x0) / RES) + pad
            b = int((xs[k + 1] - x0) / RES) + pad
            for i in range(max(0, a), min(W, b + 1)):
                grid[j][i] = 1
    return grid, W, H


N8 = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]


def thin(g, W, H):
    """Zhang-Suen: erode to a one-pixel skeleton without breaking connectivity"""
    def nb(x, y):
        return [g[y + dy][x + dx] if 0 <= x + dx < W and 0 <= y + dy < H else 0
                for dx, dy in N8]
    changed = True
    while changed:
        changed = False
        for step in (0, 1):
            kill = []
            for y in range(1, H - 1):
                row = g[y]
                for x in range(1, W - 1):
                    if not row[x]:
                        continue
                    p = nb(x, y)
                    B = sum(p)
                    if B < 2 or B > 6:
                        continue
                    A = sum(1 for i in range(8)
                            if p[i] == 0 and p[(i + 1) % 8] == 1)
                    if A != 1:
                        continue
                    if step == 0:
                        if p[0] * p[2] * p[4] or p[2] * p[4] * p[6]:
                            continue
                    else:
                        if p[0] * p[2] * p[6] or p[0] * p[4] * p[6]:
                            continue
                    kill.append((x, y))
            for x, y in kill:
                g[y][x] = 0
            if kill:
                changed = True
    return g


def trace(g, W, H):
    px = {(x, y) for y in range(H) for x in range(W) if g[y][x]}

    def deg(p):
        x, y = p
        return sum(1 for dx, dy in N8 if (x + dx, y + dy) in px)

    ends = [p for p in px if deg(p) == 1]
    nodes = {p for p in px if deg(p) >= 3} | set(ends)
    used, strokes = set(), []

    def walk(start, first):
        path, cur, prev = [start, first], first, start
        used.add((start, first)); used.add((first, start))
        while cur not in nodes:
            nxt = None
            for dx, dy in N8:
                c = (cur[0] + dx, cur[1] + dy)
                if c in px and c != prev and (cur, c) not in used:
                    nxt = c; break
            if nxt is None:
                break
            used.add((cur, nxt)); used.add((nxt, cur))
            path.append(nxt); prev, cur = cur, nxt
        return path

    for s in sorted(nodes):
        for dx, dy in N8:
            n = (s[0] + dx, s[1] + dy)
            if n in px and (s, n) not in used:
                strokes.append(walk(s, n))
    # closed loops have no nodes at all — start anywhere on the ring
    seen_edges = {e for e in used}
    for s in sorted(px):
        for dx, dy in N8:
            n = (s[0] + dx, s[1] + dy)
            if n in px and (s, n) not in seen_edges:
                w = walk(s, n)
                if len(w) > 6:
                    strokes.append(w)
                seen_edges = {e for e in used}
    return [s for s in strokes if len(s) > 3]


def rdp(pts, eps):
    if len(pts) < 3:
        return pts
    a, b = pts[0], pts[-1]
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy) or 1e-9
    worst, wi = 0, 0
    for i in range(1, len(pts) - 1):
        d = abs(dy * (pts[i][0] - a[0]) - dx * (pts[i][1] - a[1])) / n
        if d > worst:
            worst, wi = d, i
    if worst > eps:
        return rdp(pts[:wi + 1], eps)[:-1] + rdp(pts[wi:], eps)
    return [a, b]


def build(ch, order_key=None, prune=None, extend=True):
    g = GL[ch]
    polys = flatten(g['path'])
    bbox = g['bbox']
    grid, W, H = raster(polys, bbox)
    ink = sum(sum(r) for r in grid)
    thin(grid, W, H)
    strokes = trace(grid, W, H)
    if prune:
        strokes = [s for s in strokes if len(s) >= prune]

    def to_font(p):
        return (bbox[0] + (p[0] - 4 + .5) * RES, bbox[1] + (p[1] - 4 + .5) * RES)

    out = []
    for s in strokes:
        pts = [to_font(p) for p in s]
        pts = rdp(pts, RES * .9)
        if extend and len(pts) >= 2:
            pts = extend_ends(pts, g, polys)
        out.append(pts)
    out.sort(key=order_key or (lambda p: (min(q[0] for q in p), -p[0][1])))
    return out, ink


def extend_ends(pts, g, polys):
    """the skeleton stops half a stem short of a terminal — push it back out"""
    def push(a, b):
        dx, dy = a[0] - b[0], a[1] - b[1]
        n = math.hypot(dx, dy) or 1e-9
        ux, uy = dx / n, dy / n
        best = 0
        for t in range(1, 90):
            d = t * (RES / 2)
            if inside((a[0] + ux * d, a[1] + uy * d), polys):
                best = d
            else:
                break
        return (a[0] + ux * best, a[1] + uy * best)
    p = list(pts)
    if math.dist(p[0], p[-1]) > RES * 2:          # not a closed ring
        p[0] = push(p[0], p[1])
        p[-1] = push(p[-1], p[-2])
    return p


def inside(pt, polys):
    x, y = pt
    c = 0
    for poly in polys:
        for i in range(len(poly) - 1):
            (ax, ay), (bx, by) = poly[i], poly[i + 1]
            if (ay > y) != (by > y):
                xx = ax + (y - ay) * (bx - ax) / (by - ay)
                if xx > x:
                    c += 1
    return c % 2 == 1


def to_path(pts):
    d = 'M%.1f,%.1f' % pts[0]
    for p in pts[1:]:
        d += ' L%.1f,%.1f' % p
    return d


def stem_width(ch, y):
    polys = flatten(GL[ch]['path'])
    xs = []
    for p in polys:
        for i in range(len(p) - 1):
            (ax, ay), (bx, by) = p[i], p[i + 1]
            if (ay <= y < by) or (by <= y < ay):
                xs.append(ax + (y - ay) * (bx - ax) / (by - ay))
    xs.sort()
    runs = [(xs[i], xs[i + 1]) for i in range(0, len(xs) - 1, 2)]
    return runs


if __name__ == '__main__':
    xh = G['xheight']
    mr = stem_width('m', xh * .42)
    STEM = sum(b - a for a, b in mr) / len(mr)
    br = stem_width('b', GL['b']['bbox'][3] * .82)
    BSTEM = br[0][1] - br[0][0]
    print('stem %.1f (m, %d runs)   b stem %.1f' % (STEM, len(mr), BSTEM))

    res = {}
    for ch in ('m', 'b'):
        strokes, ink = build(ch, prune=4)
        res[ch] = [to_path(s) for s in strokes]
        print('%s -> %d strokes, ink %d px' % (ch, len(strokes), ink))
        for s in strokes:
            print('    %2d pts  x %4.0f..%-4.0f  y %4.0f..%-4.0f'
                  % (len(s), min(p[0] for p in s), max(p[0] for p in s),
                     min(p[1] for p in s), max(p[1] for p in s)))
    res['stem'] = round(STEM, 1)
    res['bstem'] = round(BSTEM, 1)
    res['bx'] = MBP['1']['x']
    res['period'] = GL['.']['path']
    res['tittle'] = GL['i']['tittle']
    res['dotx'] = MBP['2']['x']
    pathlib.Path(OUT).write_text(json.dumps(res, indent=1))
    print('written', OUT)
