import json, pathlib, struct

G = json.loads(pathlib.Path('glyphs.json').read_text())
GL, POS, MBP, WORD = G['glyphs'], G['pos'], G['mbpos'], G['word']

DOT_R = (GL['.']['bbox'][2] - GL['.']['bbox'][0]) / 2
DOT_X = MBP['2']['x'] + (GL['.']['bbox'][0] + GL['.']['bbox'][2]) / 2
DOT_Y = (GL['.']['bbox'][1] + GL['.']['bbox'][3]) / 2
TIT = GL['i']['tittle_bbox']
TIT_R = (TIT[2] - TIT[0]) / 2
TIT_X = POS['7']['x'] + (TIT[0] + TIT[2]) / 2
TIT_Y = (TIT[1] + TIT[3]) / 2

# ink bounds of the resting mark "mb."
MB_X0 = GL['m']['bbox'][0]
MB_X1 = MBP['2']['x'] + GL['.']['bbox'][2]
MB_Y0 = min(GL['b']['bbox'][1], GL['.']['bbox'][1])
MB_Y1 = GL['b']['bbox'][3]
MB_W, MB_H = MB_X1 - MB_X0, MB_Y1 - MB_Y0

# ink bounds of the full wordmark
W_X0 = GL['m']['bbox'][0]
W_X1 = POS['9']['x'] + GL['g']['bbox'][2]
W_Y0 = min(GL[c]['bbox'][1] for c in WORD)
W_Y1 = max(GL[c]['bbox'][3] for c in WORD)
W_W, W_H = W_X1 - W_X0, W_Y1 - W_Y0

PAL = {
 'field':  {'brand': '#12523a', 'ground': '#f3f0e7', 'contrast': '#f3f0e7',
            'ink': '#131c18', 'ac': '#d99a2b'},
 'forest': {'brand': '#1b6b45', 'ground': '#f4f3ef', 'contrast': '#f4f3ef',
            'ink': '#0e0e0d', 'ac': '#35d399'},
}

HEAD = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s"%s>'

H = json.loads(pathlib.Path('glyphs700.json').read_text())
HGL, HMBP = H['glyphs'], H['mbpos']
H_DOT_R = (HGL['.']['bbox'][2] - HGL['.']['bbox'][0]) / 2
H_DOT_X = HMBP['2']['x'] + (HGL['.']['bbox'][0] + HGL['.']['bbox'][2]) / 2
H_DOT_Y = (HGL['.']['bbox'][1] + HGL['.']['bbox'][3]) / 2
H_X0, H_X1 = HGL['m']['bbox'][0], HMBP['2']['x'] + HGL['.']['bbox'][2]
H_Y0, H_Y1 = min(HGL['b']['bbox'][1], HGL['.']['bbox'][1]), HGL['b']['bbox'][3]
H_W, H_H = H_X1 - H_X0, H_Y1 - H_Y0


def heavy_tile(fg, bg, size=1024, cover=.9):
    s = (size * cover) / H_W
    bx, by = (size - H_W * s) / 2, (size - H_H * s) / 2
    paths = ''.join('<path d="%s" transform="translate(%d,0)" fill="%s"/>'
                    % (HGL[c]['path'], x, fg)
                    for c, x in (('m', 0), ('b', HMBP['1']['x'])))
    paths += ('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s"/>'
              % (H_DOT_X, H_DOT_Y, H_DOT_R, fg))
    return (HEAD % ('0 0 %d %d' % (size, size), ' width="%d" height="%d"' % (size, size))
            + '<rect width="%d" height="%d" fill="%s"/>' % (size, size, bg)
            + '<g transform="%s">' % place(H_X0, H_Y1, s, bx, by) + paths + '</g></svg>')


def place(x0, y1, s, bx, by):
    """map font-space ink (y up) into a box, flipping y"""
    return 'translate(%.4f,%.4f) scale(%.6f,%.6f)' % (bx - x0 * s, by + y1 * s, s, -s)


def mb_paths(fill):
    p = [('<path d="%s" transform="translate(%d,0)" fill="%s"/>'
          % (GL[c]['path'], x, fill)) for c, x in (('m', 0), ('b', MBP['1']['x']))]
    p.append('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s"/>'
             % (DOT_X, DOT_Y, DOT_R, fill))
    return ''.join(p)


def word_paths(fill, dotless=False):
    p = []
    for i, ch in enumerate(WORD):
        d = GL[ch]['stem'] if (ch == 'i' and dotless) else GL[ch]['path']
        p.append('<path d="%s" transform="translate(%d,0)" fill="%s"/>'
                 % (d, POS[str(i)]['x'], fill))
    if dotless:
        p.append('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s"/>'
                 % (TIT_X, TIT_Y, TIT_R, fill))
    return ''.join(p)


def mark_svg(fill='currentColor', pad=0.06):
    """the resting mark, tight-cropped with even optical padding"""
    px, py = MB_W * pad, MB_H * pad
    vb = '%.1f %.1f %.1f %.1f' % (MB_X0 - px, -(MB_Y1 + py),
                                  MB_W + px * 2, MB_H + py * 2)
    return (HEAD % (vb, ' role="img" aria-label="mb."')
            + '<g transform="scale(1,-1)">' + mb_paths(fill) + '</g></svg>')


def wordmark_svg(fill='currentColor', pad=0.04):
    px, py = W_W * pad * .25, W_H * pad
    vb = '%.1f %.1f %.1f %.1f' % (W_X0 - px, -(W_Y1 + py),
                                  W_W + px * 2, W_H + py * 2)
    return (HEAD % (vb, ' role="img" aria-label="madeboring"')
            + '<g transform="scale(1,-1)">' + word_paths(fill) + '</g></svg>')


def tile_svg(fg, bg, size=1024, cover=.76, radius=None):
    """the mark centred on a solid ground — app icons, favicons, maskable"""
    s = (size * cover) / MB_W
    bx = (size - MB_W * s) / 2
    by = (size - MB_H * s) / 2
    r = '' if radius is None else ' rx="%.1f" ry="%.1f"' % (radius, radius)
    return (HEAD % ('0 0 %d %d' % (size, size), ' width="%d" height="%d"' % (size, size))
            + '<rect width="%d" height="%d" fill="%s"%s/>' % (size, size, bg, r)
            + '<g transform="%s">' % place(MB_X0, MB_Y1, s, bx, by)
            + mb_paths(fg) + '</g></svg>')


def banner_svg(fg, bg, w, h, cover=.52, sub=None, subcol=None):
    """og / twitter cards — wordmark centred on a solid ground"""
    s = (w * cover) / W_W
    bx = (w - W_W * s) / 2
    by = (h - W_H * s) / 2 - (0 if sub is None else h * .045)
    out = [HEAD % ('0 0 %d %d' % (w, h), ' width="%d" height="%d"' % (w, h)),
           '<rect width="%d" height="%d" fill="%s"/>' % (w, h, bg),
           '<g transform="%s">' % place(W_X0, W_Y1, s, bx, by),
           word_paths(fg), '</g>']
    if sub:
        out.append('<text x="%d" y="%d" text-anchor="middle" fill="%s" '
                   'font-family="ui-monospace,Menlo,monospace" font-size="%d" '
                   'letter-spacing="%.1f" opacity=".7">%s</text>'
                   % (w // 2, int(by + W_H * s + h * .105), subcol or fg,
                      int(h * .036), h * .0055, sub))
    out.append('</svg>')
    return ''.join(out)


def animated_svg(fg, bg, w=1200, h=300):
    """self-contained SMIL loop — works where JS is blocked (README, email, notion)"""
    s = (w * .78) / W_W
    bx = (w - W_W * s) / 2
    by = (h - W_H * s) / 2
    dx, dy = TIT_X - DOT_X, TIT_Y - DOT_Y
    mid = 'M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f' % (
        DOT_X, DOT_Y, (DOT_X + TIT_X) / 2, DOT_Y + dy * 1.5, TIT_X, TIT_Y)
    T, HOLD = 1.15, 3.4          # animation length, then hold before the loop
    kt = '0;%.4f;1' % (T / HOLD)
    out = [HEAD % ('0 0 %d %d' % (w, h), ' width="%d" height="%d"' % (w, h)),
           '<rect width="%d" height="%d" fill="%s"/>' % (w, h, bg),
           '<g transform="%s">' % place(W_X0, W_Y1, s, bx, by)]
    for i, ch in enumerate(WORD):
        x = POS[str(i)]['x']
        d = GL[ch]['stem'] if ch == 'i' else GL[ch]['path']
        if i == 0:
            out.append('<path d="%s" fill="%s"/>' % (d, fg))
        elif i == 4:
            out.append(
                '<g transform="translate(%d,0)"><path d="%s" fill="%s"/>'
                '<animateTransform attributeName="transform" type="translate" '
                'values="%d,0;%d,0;%d,0" keyTimes="%s" dur="%.2fs" '
                'calcMode="spline" keySplines="0.16 0.02 0.06 1;0 0 1 1" '
                'repeatCount="indefinite"/></g>'
                % (MBP['1']['x'], d, fg, MBP['1']['x'], x, x, kt, HOLD))
        else:
            f = max(0., min(1., (x - DOT_X) / dx))
            b = (f * T * .8) / HOLD
            out.append(
                '<path d="%s" transform="translate(%d,0)" fill="%s" opacity="0">'
                '<animate attributeName="opacity" values="0;0;1;1" '
                'keyTimes="0;%.4f;%.4f;1" dur="%.2fs" repeatCount="indefinite"/>'
                '</path>' % (d, x, fg, b, min(.999, b + .09), HOLD))
    out.append(
        '<g><circle cx="0" cy="0" r="%.1f" fill="%s">'
        '<animate attributeName="r" values="%.1f;%.1f;%.1f" keyTimes="%s" '
        'dur="%.2fs" repeatCount="indefinite"/></circle>'
        '<animateMotion path="%s" keyPoints="0;1;1" keyTimes="%s" dur="%.2fs" '
        'calcMode="spline" keySplines="0.16 0.02 0.06 1;0 0 1 1" '
        'repeatCount="indefinite" rotate="0"/></g>'
        % (DOT_R, fg, DOT_R, TIT_R, TIT_R, kt, HOLD, mid, kt, HOLD))
    out.append('</g></svg>')
    return ''.join(out)


def ico(pngs):
    """multi-resolution .ico container around already-encoded PNGs"""
    n = len(pngs)
    head = struct.pack('<HHH', 0, 1, n)
    off = 6 + 16 * n
    dirs, blobs = b'', b''
    for size, data in pngs:
        dirs += struct.pack('<BBBBHHII', size % 256, size % 256, 0, 0, 1, 32,
                            len(data), off)
        off += len(data)
        blobs += data
    return head + dirs + blobs


ROOT = pathlib.Path('assets')
jobs = []
for pal, C in PAL.items():
    d = ROOT / pal
    (d / 'png').mkdir(parents=True, exist_ok=True)
    (d / 'svg').mkdir(parents=True, exist_ok=True)
    br, gr, ct, ink = C['brand'], C['ground'], C['contrast'], C['ink']

    W = lambda name, body: (d / 'svg' / name).write_text(body)
    W('mark.svg', mark_svg())                       # inherits currentColor
    W('mark-brand.svg', mark_svg(br))
    W('mark-ink.svg', mark_svg(ink))
    W('mark-cream.svg', mark_svg(ct))
    W('wordmark.svg', wordmark_svg())
    W('wordmark-brand.svg', wordmark_svg(br))
    W('wordmark-ink.svg', wordmark_svg(ink))
    W('wordmark-cream.svg', wordmark_svg(ct))
    W('icon-tile.svg', tile_svg(ct, br))
    W('icon-tile-light.svg', tile_svg(br, gr))
    W('icon-rounded.svg', tile_svg(ct, br, radius=1024 * .2237))
    W('icon-maskable.svg', tile_svg(ct, br, cover=.56))
    W('favicon.svg', tile_svg(ct, br, cover=.86))
    W('favicon-light.svg', tile_svg(br, gr, cover=.86))
    W('favicon-small.svg', heavy_tile(ct, br))
    W('favicon-small-light.svg', heavy_tile(br, gr))
    W('og.svg', banner_svg(ct, br, 1200, 630, sub='WE MAKE IT BORING'))
    W('twitter.svg', banner_svg(ct, br, 1200, 600, sub='WE MAKE IT BORING'))
    W('logo-animated.svg', animated_svg(ct, br))
    W('logo-animated-light.svg', animated_svg(br, gr))

    for n in (16, 32, 48, 64, 96, 128, 180, 192, 256, 384, 512, 1024):
        src = 'favicon-small.svg' if n <= 32 else 'favicon.svg'
        jobs.append({'src': str(d / 'svg' / src),
                     'out': str(d / 'png' / ('icon-%d.png' % n)), 'w': n, 'h': n})
    jobs += [
     {'src': str(d / 'svg' / 'icon-rounded.svg'),
      'out': str(d / 'png' / 'apple-touch-icon.png'), 'w': 180, 'h': 180},
     {'src': str(d / 'svg' / 'icon-maskable.svg'),
      'out': str(d / 'png' / 'maskable-192.png'), 'w': 192, 'h': 192},
     {'src': str(d / 'svg' / 'icon-maskable.svg'),
      'out': str(d / 'png' / 'maskable-512.png'), 'w': 512, 'h': 512},
     {'src': str(d / 'svg' / 'og.svg'),
      'out': str(d / 'png' / 'og.png'), 'w': 1200, 'h': 630},
     {'src': str(d / 'svg' / 'twitter.svg'),
      'out': str(d / 'png' / 'twitter.png'), 'w': 1200, 'h': 600},
     {'src': str(d / 'svg' / 'wordmark-brand.svg'),
      'out': str(d / 'png' / 'wordmark-2400.png'), 'w': 2400, 'h': 0},
     {'src': str(d / 'svg' / 'wordmark-cream.svg'),
      'out': str(d / 'png' / 'wordmark-cream-2400.png'), 'w': 2400, 'h': 0},
     {'src': str(d / 'svg' / 'mark-brand.svg'),
      'out': str(d / 'png' / 'mark-1200.png'), 'w': 1200, 'h': 0},
    ]

    (d / 'site.webmanifest').write_text(json.dumps({
        'name': 'made boring', 'short_name': 'mb.',
        'icons': [
            {'src': '/icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
            {'src': '/icon-512.png', 'sizes': '512x512', 'type': 'image/png'},
            {'src': '/maskable-512.png', 'sizes': '512x512', 'type': 'image/png',
             'purpose': 'maskable'}],
        'theme_color': br, 'background_color': gr, 'display': 'standalone',
        'start_url': '/'}, indent=2))

    (d / 'head.html').write_text(
        '<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n'
        '<link rel="icon" href="/favicon.ico" sizes="32x32">\n'
        '<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n'
        '<link rel="manifest" href="/site.webmanifest">\n'
        '<meta name="theme-color" content="%s">\n'
        '<meta property="og:image" content="https://madeboring.com/og.png">\n'
        '<meta name="twitter:card" content="summary_large_image">\n'
        '<meta name="twitter:image" content="https://madeboring.com/twitter.png">\n'
        % br)

pathlib.Path('assets/jobs.json').write_text(json.dumps(jobs))
print('svg written for', len(PAL), 'palettes &middot;', len(jobs), 'raster jobs queued')
