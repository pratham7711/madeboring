import json, math, pathlib, re

G = json.loads(pathlib.Path('glyphs.json').read_text())
GL, MBP = G['glyphs'], G['mbpos']

TOK = re.compile(r'([MLQCZHV])([^MLQCZHV]*)')
NUM = re.compile(r'-?\d+(?:\.\d+)?')


def flatten(d, steps=28):
    """SVGPathPen output -> list of closed polygons"""
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
        elif cmd == 'Q':
            for i in range(0, len(v), 4):
                c, e = (v[i], v[i + 1]), (v[i + 2], v[i + 3])
                for k in range(1, steps + 1):
                    t = k / steps; u = 1 - t
                    cur.append((u * u * pt[0] + 2 * u * t * c[0] + t * t * e[0],
                                u * u * pt[1] + 2 * u * t * c[1] + t * t * e[1]))
                pt = e
        elif cmd == 'C':
            for i in range(0, len(v), 6):
                c1, c2, e = (v[i], v[i+1]), (v[i+2], v[i+3]), (v[i+4], v[i+5])
                for k in range(1, steps + 1):
                    t = k / steps; u = 1 - t
                    cur.append((u**3*pt[0] + 3*u*u*t*c1[0] + 3*u*t*t*c2[0] + t**3*e[0],
                                u**3*pt[1] + 3*u*u*t*c1[1] + 3*u*t*t*c2[1] + t**3*e[1]))
                pt = e
        elif cmd == 'H':
            for x in v:
                pt = (x, pt[1]); cur.append(pt)
        elif cmd == 'V':
            for y in v:
                pt = (pt[0], y); cur.append(pt)
        elif cmd == 'Z':
            if cur:
                cur.append(start); polys.append(cur); cur = []
            pt = start
    if cur:
        polys.append(cur)
    return polys


def runs(polys, y):
    """ink spans along the horizontal line at y, using the even-odd rule"""
    xs = []
    for p in polys:
        for i in range(len(p) - 1):
            (x0, y0), (x1, y1) = p[i], p[i + 1]
            if (y0 <= y < y1) or (y1 <= y < y0):
                xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
    xs.sort()
    return [(xs[i], xs[i + 1]) for i in range(0, len(xs) - 1, 2)]


def vruns(polys, x):
    ys = []
    for p in polys:
        for i in range(len(p) - 1):
            (x0, y0), (x1, y1) = p[i], p[i + 1]
            if (x0 <= x < x1) or (x1 <= x < x0):
                ys.append(y0 + (x - x0) * (y1 - y0) / (x1 - x0))
    ys.sort()
    return [(ys[i], ys[i + 1]) for i in range(0, len(ys) - 1, 2)]


M = flatten(GL['m']['path'])
B = flatten(GL['b']['path'])

mr = runs(M, 200)
STEM = sum(b - a for a, b in mr) / len(mr)
MX = [(a + b) / 2 for a, b in mr]
M_TOP = GL['m']['bbox'][3]

br600 = runs(B, 600)                      # b's stem, above the bowl
BX = (br600[0][0] + br600[0][1]) / 2
BSTEM = br600[0][1] - br600[0][0]
# the bowl's true vertical diameter, taken down its own centre line
_probe = (BX + GL['b']['bbox'][2]) / 2
bowl_v = vruns(B, _probe)
BOWL_TOP = max(b for a, b in bowl_v)
BOWL_BOT = min(a for a, b in bowl_v)
BOWL_CY = (BOWL_TOP + BOWL_BOT) / 2
bmr = runs(B, BOWL_CY)
BOWL_R_X = (bmr[-1][0] + bmr[-1][1]) / 2     # centre of the bowl's right stroke
BOWL_CX = (BX + BOWL_R_X) / 2
BOWL_R = (BOWL_R_X - BX) / 2
BOWL_RY = (BOWL_TOP - BOWL_BOT) / 2 - BSTEM / 2   # Jost's bowl is not a true circle

print('m stem width %.1f  stems at %s  top %.0f' % (STEM, [round(v) for v in MX], M_TOP))
print('b stem width %.1f  at x %.1f' % (BSTEM, BX))
print('bowl  top %.0f bot %.0f  cx %.1f cy %.1f  rx %.1f ry %.1f'
      % (BOWL_TOP, BOWL_BOT, BOWL_CX, BOWL_CY, BOWL_R, BOWL_RY))

# --- m: left stem, then two shoulders, each springing into the next stem
ARCH_R = (MX[1] - MX[0]) / 2
ARCH_Y = M_TOP - STEM / 2 - ARCH_R
m_paths = [
    'M%.1f,0 L%.1f,%.1f' % (MX[0], MX[0], ARCH_Y),
    'M%.1f,%.1f A%.1f,%.1f 0 0 0 %.1f,%.1f L%.1f,0'
    % (MX[0], ARCH_Y, ARCH_R, ARCH_R, MX[1], ARCH_Y, MX[1]),
    'M%.1f,%.1f A%.1f,%.1f 0 0 0 %.1f,%.1f L%.1f,0'
    % (MX[1], ARCH_Y, ARCH_R, ARCH_R, MX[2], ARCH_Y, MX[2]),
]
# --- b: stem down from the ascender, then the bowl round from where they meet
b_paths = [
    'M%.1f,%.1f L%.1f,0' % (BX, GL['b']['bbox'][3], BX),
    'M%.1f,%.1f A%.1f,%.1f 0 1 0 %.1f,%.1f A%.1f,%.1f 0 1 0 %.1f,%.1f'
    % (BOWL_CX - BOWL_R, BOWL_CY, BOWL_R, BOWL_RY, BOWL_CX + BOWL_R, BOWL_CY,
       BOWL_R, BOWL_RY, BOWL_CX - BOWL_R, BOWL_CY),
]
D_R = (GL['.']['bbox'][2] - GL['.']['bbox'][0]) / 2
D_X = MBP['2']['x'] + (GL['.']['bbox'][0] + GL['.']['bbox'][2]) / 2
D_Y = (GL['.']['bbox'][1] + GL['.']['bbox'][3]) / 2
dot_path = ('M%.1f,%.1f A%.1f,%.1f 0 1 0 %.1f,%.1f A%.1f,%.1f 0 1 0 %.1f,%.1f'
            % (D_X - D_R / 2, D_Y, D_R / 2, D_R / 2, D_X + D_R / 2, D_Y,
               D_R / 2, D_R / 2, D_X - D_R / 2, D_Y))

out = {'stem': round(STEM, 1), 'bstem': round(BSTEM, 1),
       'm': m_paths, 'b': b_paths, 'dot': dot_path,
       'dotStroke': round(D_R, 1), 'bx': MBP['1']['x']}
pathlib.Path('skeleton.json').write_text(json.dumps(out, indent=1))
print('\narch r %.1f springs at y %.1f' % (ARCH_R, ARCH_Y))
print('skeleton.json written')
