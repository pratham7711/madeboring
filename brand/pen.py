"""Pen paths taken from the real outlines, not guessed.

For a mask, a pen that is too wide costs nothing (ink only appears where the
glyph is) while a pen that is too narrow leaves holes. So: measure the widest
point of each letter with a distance transform and use that, and take the
bowl's centreline as the true midline between its counter and its outside.
"""
import json, math, os, pathlib

os.environ.setdefault('GLYPHS', 'plex600.json')
import centerline as CL

G = json.loads(pathlib.Path(os.environ['GLYPHS']).read_text())
GL = G['glyphs']
RES = CL.RES


def dist_field(ch):
    """distance from every ink pixel to the nearest edge, in pixels"""
    polys = CL.flatten(GL[ch]['path'])
    grid, W, H = CL.raster(polys, GL[ch]['bbox'])
    INF = 1e9
    d = [[0.0 if not grid[y][x] else INF for x in range(W)] for y in range(H)]
    for y in range(H):
        for x in range(W):
            if d[y][x]:
                v = d[y][x]
                if y: v = min(v, d[y-1][x] + 1)
                if x: v = min(v, d[y][x-1] + 1)
                if y and x: v = min(v, d[y-1][x-1] + 1.4142)
                if y and x < W-1: v = min(v, d[y-1][x+1] + 1.4142)
                d[y][x] = v
    for y in range(H-1, -1, -1):
        for x in range(W-1, -1, -1):
            if d[y][x]:
                v = d[y][x]
                if y < H-1: v = min(v, d[y+1][x] + 1)
                if x < W-1: v = min(v, d[y][x+1] + 1)
                if y < H-1 and x < W-1: v = min(v, d[y+1][x+1] + 1.4142)
                if y < H-1 and x: v = min(v, d[y+1][x-1] + 1.4142)
                d[y][x] = v
    return d, W, H, GL[ch]['bbox']


def sample(d, W, H, bb, x, y):
    """distance-to-edge at a font-space point, 0 outside the letter"""
    px = (x - bb[0]) / RES + 4
    py = (y - bb[1]) / RES + 4
    i, j = int(px), int(py)
    if not (0 <= i < W and 0 <= j < H):
        return 0.0
    return d[j][i]


def snap(pts, ch, steps=8):
    """walk each point onto the ridge of the distance field: the true midline"""
    d, W, H, bb = dist_field(ch)
    out, thick = [], []
    for x, y in pts:
        for _ in range(steps):
            here = sample(d, W, H, bb, x, y)
            best, bx, by = here, x, y
            for ax in (-1, 0, 1):
                for ay in (-1, 0, 1):
                    nx, ny = x + ax * RES * .6, y + ay * RES * .6
                    v = sample(d, W, H, bb, nx, ny)
                    if v > best:
                        best, bx, by = v, nx, ny
            if (bx, by) == (x, y):
                break
            x, y = bx, by
        out.append((x, y))
        thick.append(2 * sample(d, W, H, bb, x, y) * RES)
    return out, max(thick)


def thickness(ch):
    d, W, H, _ = dist_field(ch)
    return 2 * max(max(r) for r in d) * RES


def ray_hits(polys, cx, cy, ux, uy):
    """distances along the ray where it crosses these polylines"""
    hits = []
    for p in polys:
        for i in range(len(p) - 1):
            ax, ay = p[i][0] - cx, p[i][1] - cy
            bx, by = p[i+1][0] - cx, p[i+1][1] - cy
            da = ax * uy - ay * ux
            db = bx * uy - by * ux
            if (da > 0) == (db > 0) or da == db:
                continue
            t = da / (da - db)
            r = (ax + (bx - ax) * t) * ux + (ay + (by - ay) * t) * uy
            if r > 0:
                hits.append(r)
    return sorted(hits)


def bowl_ring(ch, start_deg=200, step=4):
    """midline between the counter and the outside, all the way round"""
    polys = CL.flatten(GL[ch]['path'])
    areas = [(abs(sum(p[i][0]*p[i+1][1] - p[i+1][0]*p[i][1]
                      for i in range(len(p)-1))) / 2, p) for p in polys]
    areas.sort(key=lambda a: -a[0])
    outer, inner = areas[0][1], areas[1][1]
    xs = [q[0] for q in inner]; ys = [q[1] for q in inner]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    pts, thick = [], []
    for k in range(0, 360 // step):
        a = math.radians(start_deg + k * step)
        ux, uy = math.cos(a), math.sin(a)
        hi = ray_hits([inner], cx, cy, ux, uy)
        ho = ray_hits([outer], cx, cy, ux, uy)
        if not hi:
            continue
        r_in = hi[0]
        beyond = [h for h in ho if h > r_in]
        if not beyond:
            continue
        r_out = beyond[0]
        r = (r_in + r_out) / 2
        pts.append((cx + ux * r, cy + uy * r))
        thick.append(r_out - r_in)
    return pts, max(thick), (cx, cy)


def to_path(pts, close=True):
    d = 'M%.1f,%.1f' % pts[0] + ''.join(' L%.1f,%.1f' % p for p in pts[1:])
    return d + (' Z' if close else '')


if __name__ == '__main__':
    out = {}
    mb, bb = GL['m']['bbox'], GL['b']['bbox']
    pb = GL['.']['bbox']
    stem = sum(b - a for a, b in CL.stem_width('m', G['xheight'] * .45)) / 3

    tm, tb = thickness('m'), thickness('b')
    ring, _, c = bowl_ring('b')
    ring, ring_t = snap(ring, 'b')
    print('stem %.1f | m widest %.1f | b widest %.1f | bowl thickest %.1f'
          % (stem, tm, tb, ring_t))
    print('bowl centre (%.1f, %.1f)  ring pts %d' % (c[0], c[1], len(ring)))

    h = stem / 2
    sx = [mb[0] + h, (mb[0] + mb[2]) / 2, mb[2] - h]
    r = (sx[1] - sx[0]) / 2
    top = mb[3] - h
    spring = top - r
    out['m'] = ['M%.1f,%.1f L%.1f,0' % (sx[0], top, sx[0]),
                'M%.1f,%.1f A%.1f,%.1f 0 0 0 %.1f,%.1f L%.1f,0'
                % (sx[0], spring, r, r, sx[1], spring, sx[1]),
                'M%.1f,%.1f A%.1f,%.1f 0 0 0 %.1f,%.1f L%.1f,0'
                % (sx[1], spring, r, r, sx[2], spring, sx[2])]
    out['mWidth'] = round(tm * 1.04, 1)
    out['b'] = ['M%.1f,%.1f L%.1f,0' % (bb[0] + h, bb[3], bb[0] + h),
                to_path(ring)]
    out['bWidth'] = round(ring_t * 1.06, 1)
    out['dotWidth'] = round(max(pb[2] - pb[0], pb[3] - pb[1]) * 1.45, 1)
    out['stem'] = round(stem, 2)
    pathlib.Path('pen-plex.json').write_text(json.dumps(out, indent=1))
    print('pen widths  m %.1f  b %.1f  dot %.1f'
          % (out['mWidth'], out['bWidth'], out['dotWidth']))
    print('ring starts (%.1f,%.1f) ends (%.1f,%.1f)'
          % (ring[0][0], ring[0][1], ring[-1][0], ring[-1][1]))
