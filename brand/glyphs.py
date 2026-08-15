import json, pathlib
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.boundsPen import BoundsPen

import os
SRC = os.environ.get('FONT', '/private/tmp/claude-502/-Users-pratham/'
                     '4eed19d0-0848-4e3a-a61e-012788cbfae7/scratchpad/jost.woff2')
OUT = os.environ.get('OUT', '')
WORD = 'madeboring'
import sys
WEIGHT = int(sys.argv[1]) if len(sys.argv)>1 else 600


def contours(pen_value):
    """split a RecordingPen's ops into one list per closed contour"""
    out, cur = [], []
    for op, args in pen_value:
        cur.append((op, args))
        if op in ('closePath', 'endPath'):
            out.append(cur)
            cur = []
    return out


def to_svg(ops, gs):
    p = SVGPathPen(gs)
    for op, args in ops:
        getattr(p, op)(*args)
    return p.getCommands()


def bounds(ops, gs):
    b = BoundsPen(gs)
    for op, args in ops:
        getattr(b, op)(*args)
    return b.bounds


_f = TTFont(SRC)
f = instantiateVariableFont(_f, {'wght': WEIGHT}, inplace=True) if 'fvar' in _f else _f
gs = f.getGlyphSet()
cmap = f.getBestCmap()
hmtx = f['hmtx']
upem = f['head'].unitsPerEm

G = {}
for ch in set(WORD + '.'):
    name = cmap[ord(ch)]
    rec = RecordingPen()
    gs[name].draw(rec)
    cs = contours(rec.value)
    entry = {'adv': hmtx[name][0], 'path': to_svg(rec.value, gs),
             'bbox': bounds(rec.value, gs), 'nc': len(cs)}
    if ch == 'i':
        # the tittle is the contour whose bbox sits highest; the stem is the rest
        bb = [bounds(c, gs) for c in cs]
        top = max(range(len(cs)), key=lambda k: bb[k][3])
        entry['stem'] = to_svg([o for k, c in enumerate(cs) if k != top for o in c], gs)
        entry['tittle'] = to_svg(cs[top], gs)
        entry['tittle_bbox'] = bb[top]
        entry['stem_bbox'] = [bounds([o for k, c in enumerate(cs) if k != top for o in c], gs)]
    G[ch] = entry

# lay the word out on a 1000-upem baseline, no kerning table in the subset
x, pos = 0, {}
for i, ch in enumerate(WORD):
    pos[i] = {'ch': ch, 'x': x, 'adv': G[ch]['adv']}
    x += G[ch]['adv']
WORD_W = x

# "mb." on its own baseline
x2, mbpos = 0, {}
for i, ch in enumerate('mb.'):
    mbpos[i] = {'ch': ch, 'x': x2, 'adv': G[ch]['adv']}
    x2 += G[ch]['adv']

out = {'upem': upem, 'weight': WEIGHT, 'word': WORD, 'glyphs': G,
       'pos': pos, 'wordW': WORD_W, 'mbpos': mbpos, 'mbW': x2,
       'asc': f['hhea'].ascent, 'desc': f['hhea'].descent,
       'xheight': f['OS/2'].sxHeight if hasattr(f['OS/2'], 'sxHeight') else None,
       'cap': f['OS/2'].sCapHeight if hasattr(f['OS/2'], 'sCapHeight') else None}
pathlib.Path(OUT or ('glyphs%d.json'%WEIGHT if WEIGHT!=600 else 'glyphs.json')).write_text(json.dumps(out))

print('upem', upem, 'wordW', WORD_W, 'mbW', x2)
print('x-height', out['xheight'], 'cap', out['cap'])
for ch in 'mb.i':
    g = G[ch]
    print(ch, 'adv', g['adv'], 'bbox', [round(v) for v in g['bbox']], 'contours', g['nc'])
print('i tittle bbox', [round(v) for v in G['i']['tittle_bbox']])
print('i stem bbox  ', [round(v) for v in G['i']['stem_bbox'][0]])
print('period bbox  ', [round(v) for v in G['.']['bbox']])
print('m x', pos[0]['x'], '| b x', pos[4]['x'], '| i x', pos[7]['x'])
