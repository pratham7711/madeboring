import base64, pathlib

SCRATCH = pathlib.Path('/private/tmp/claude-502/-Users-pratham/'
                       '4eed19d0-0848-4e3a-a61e-012788cbfae7/scratchpad')
b64 = lambda p: base64.b64encode(pathlib.Path(p).read_bytes()).decode()
JOST, PLEX = b64(SCRATCH / 'jost.woff2'), b64(SCRATCH / 'plexmono.woff2')

MB = '<i class="a">M</i><i class="b">B</i>'
mb = '<i class="a">m</i><i class="b">b</i>'

# (name, family, html, css, anim)
M = [
 ('Ligature', 'A', MB, '.x{letter-spacing:0}.x .b{margin-left:-.256em}', 'merge'),
 ('Stack', 'A', MB, '.x{flex-direction:column;line-height:.84;letter-spacing:0}', 'close'),
 ('Slash', 'A', '<i class="a">m</i><i class="s">/</i><i class="b">b</i>',
  '.x .s{color:var(--ac);margin:0 -.02em}', 'drop'),
 ('Lowercase', 'A', mb, '.x{letter-spacing:-.06em}', 'rise'),
 ('Tracked', 'A', MB, '.x{letter-spacing:.22em;font-weight:400;text-indent:.22em}', 'track'),
 ('Full stop', 'A', mb + '<i class="s">.</i>', '.x .s{color:var(--ac)}', 'drop'),
 ('Overlap', 'A', MB,
  '.x{letter-spacing:0}.x .b{margin-left:-.42em;color:var(--ac);mix-blend-mode:multiply}',
  'merge'),
 ('Outline', 'A', MB,
  '.x{-webkit-text-stroke:.055em var(--mk);color:transparent;letter-spacing:-.02em}', 'rise'),
 ('Mixed case', 'A', '<i class="a">m</i><i class="b">B</i>', '.x{letter-spacing:-.05em}',
  'rise'),
 ('Mono', 'A', MB, '.x{font-family:var(--mono);font-weight:400;letter-spacing:-.02em}',
  'track'),

 ('Roundel', 'B', MB,
  '.x{border:.085em solid var(--mk);border-radius:50%;width:1.75em;height:1.75em;'
  'justify-content:center}.x i{font-size:.55em}', 'spin'),
 ('Squircle', 'B', MB,
  '.x{background:var(--mk);color:var(--gd);border-radius:.26em;width:1.5em;height:1.5em;'
  'justify-content:center}.x i{font-size:.6em}', 'flip'),
 ('Square', 'B', MB,
  '.x{background:var(--mk);color:var(--gd);width:1.5em;height:1.5em;'
  'justify-content:center}.x i{font-size:.6em}', 'flip'),
 ('Bracket', 'B', '<i class="s">[</i>' + MB + '<i class="s">]</i>',
  '.x .s{color:var(--ac);font-weight:400}', 'spread'),
 ('Chip', 'B', MB,
  '.x{border:.08em solid var(--mk);padding:.14em .28em .18em;border-radius:.08em}', 'fill'),
 ('Hexagon', 'B', MB,
  '.x{background:var(--mk);color:var(--gd);width:1.62em;height:1.44em;'
  'justify-content:center;clip-path:polygon(25% 0,75% 0,100% 50%,75% 100%,25% 100%,0 50%)}'
  '.x i{font-size:.52em}', 'flip'),
 ('Pill', 'B', MB,
  '.x{border:.075em solid var(--mk);border-radius:1em;padding:.12em .38em .16em}', 'spread'),
 ('Ruled', 'B', MB,
  '.x{flex-direction:column;line-height:1}'
  '.x:after{content:"";display:block;width:100%;height:.075em;background:var(--ac);'
  'margin-top:.14em}', 'wipe'),

 ('Chevrons', 'C', '<i class="a">M</i><i class="b">B</i>',
  '.x{letter-spacing:-.09em}.x .a{transform:scaleY(1.18)}', 'rise'),
 ('Modular', 'C', MB,
  '.x{letter-spacing:.04em;font-weight:700;font-stretch:100%}'
  '.x i{background:var(--mk);color:var(--gd);padding:.06em .1em;margin:0 .02em}', 'flip'),
 ('Knockout', 'C', MB,
  '.x{background:var(--mk);color:var(--gd);padding:.2em .3em;letter-spacing:-.03em}',
  'wipe'),
 ('Rotate', 'C', MB, '.x{transform:rotate(-90deg);letter-spacing:-.03em}', 'spin'),
 ('Nested', 'C', MB,
  '.x{letter-spacing:0;align-items:flex-end}'
  '.x .b{margin-left:-.3em;font-size:.68em;color:var(--ac)}', 'merge'),
 ('Ascend', 'C', MB,
  '.x{letter-spacing:-.02em;align-items:flex-end}.x .a{font-size:1.28em;line-height:.8}',
  'rise'),
 ('Stencil', 'C', MB,
  '.x{letter-spacing:-.02em;'
  '-webkit-mask-image:repeating-linear-gradient(0deg,#000 0 .2em,transparent .2em .27em);'
  'mask-image:repeating-linear-gradient(0deg,#000 0 .2em,transparent .2em .27em)}', 'wipe'),
 ('Split tone', 'C', MB,
  '.x{letter-spacing:-.03em}.x .b{color:var(--ac)}', 'spread'),
 ('Echo', 'C', MB,
  '.x{letter-spacing:-.03em;text-shadow:.1em .1em 0 var(--ac)}', 'drop'),
 ('Halved', 'C', MB,
  '.x{letter-spacing:-.03em;background:linear-gradient(90deg,var(--mk) 50%,var(--ac) 50%);'
  '-webkit-background-clip:text;color:transparent}', 'wipe'),

 ('Expand', 'D', '<i class="a">m</i><i class="g">ade</i><i class="sp"></i>'
  '<i class="b">b</i><i class="g">oring</i>',
  '.x{letter-spacing:-.04em}.x .g{max-width:0;overflow:hidden;white-space:nowrap;'
  'transition:max-width .7s cubic-bezier(.16,.02,.06,1)}'
  '.x .sp{width:0;transition:width .7s cubic-bezier(.16,.02,.06,1)}'
  '.cell:hover .x .g{max-width:4em}.cell:hover .x .sp{width:.3em}', ''),
 ('Collapse', 'D', mb,
  '.x{letter-spacing:-.05em;transition:letter-spacing .5s}'
  '.cell:hover .x{letter-spacing:-.16em}', ''),
 ('Progress', 'D', MB,
  '.x{position:relative;padding:.14em .26em .18em;border:.07em solid var(--mk)}'
  '.x:before{content:"";position:absolute;left:0;top:0;bottom:0;width:0;'
  'background:var(--ac);opacity:.3;transition:width .8s}'
  '.cell:hover .x:before{width:100%}', ''),
 ('Orbit', 'D', MB,
  '.x{position:relative;justify-content:center;width:1.8em;height:1.8em}'
  '.x i{font-size:.52em}'
  '.x:after{content:"";position:absolute;inset:0;border:.055em solid var(--ac);'
  'border-radius:50%;border-top-color:transparent;animation:sp 2.4s linear infinite}', ''),
 ('Caret', 'D', mb + '<i class="cr"></i>',
  '.x{font-family:var(--mono);font-weight:400}'
  '.x .cr{width:.5em;height:.95em;background:var(--ac);margin-left:.12em;'
  'animation:bl 1.05s steps(1) infinite}', ''),
 ('Flip', 'D', '<i class="a">M</i><i class="b">B</i>',
  '.x{letter-spacing:-.03em;perspective:400px}'
  '.x .b{transition:transform .6s;transform-origin:50% 50%}'
  '.cell:hover .x .b{transform:rotateY(360deg)}', ''),
 ('Shift', 'D', MB,
  '.x{letter-spacing:-.03em}.x i{transition:transform .45s}'
  '.cell:hover .x .a{transform:translateY(-.1em)}'
  '.cell:hover .x .b{transform:translateY(.1em)}', ''),
 ('Pulse', 'D', MB,
  '.x{letter-spacing:-.03em;animation:pu 2.6s ease-in-out infinite}', ''),

 ('Megabyte', 'E', '<i class="u">1.4</i>' + MB,
  '.x{align-items:baseline;gap:.18em}'
  '.x .u{font-family:var(--mono);font-size:.42em;color:var(--muted);font-weight:400}',
  'rise'),
 ('File', 'E', MB,
  '.x{border:.07em solid var(--mk);width:1.42em;height:1.72em;justify-content:center;'
  'border-radius:.06em}.x i{font-size:.46em}', 'drop'),
 ('Command', 'E', '<i class="s">$</i>' + mb,
  '.x{font-family:var(--mono);font-weight:400;gap:.3em}.x .s{color:var(--ac)}', 'track'),
 ('Check', 'E', MB + '<i class="s">&#10003;</i>',
  '.x{gap:.14em}.x .s{color:var(--ac);font-size:.72em}', 'drop'),
 ('Toggle', 'E', MB,
  '.x{background:var(--mk);color:var(--gd);border-radius:1em;padding:.12em .5em .16em .24em;'
  'position:relative}'
  '.x:after{content:"";position:absolute;right:.12em;top:50%;transform:translateY(-50%);'
  'width:.34em;height:.34em;border-radius:50%;background:var(--gd)}', 'spread'),
 ('Version', 'E', MB + '<i class="u">v1</i>',
  '.x{align-items:baseline;gap:.18em}'
  '.x .u{font-family:var(--mono);font-size:.4em;color:var(--ac);font-weight:400}', 'rise'),
 ('Key', 'E', MB,
  '.x{border:.06em solid var(--mk);border-bottom-width:.18em;border-radius:.14em;'
  'padding:.12em .24em .1em}', 'drop'),
 ('Barcode', 'E', MB,
  '.x{flex-direction:column;line-height:1}'
  '.x:after{content:"";display:block;width:100%;height:.22em;margin-top:.1em;'
  'background:repeating-linear-gradient(90deg,var(--mk) 0 .04em,transparent .04em .1em)}',
  'wipe'),

 ('Cut', 'F', MB,
  '.x{letter-spacing:-.03em;clip-path:polygon(0 0,100% 0,100% 78%,0 100%)}', 'wipe'),
 ('Soft', 'F', MB, '.x{font-weight:500;letter-spacing:.01em}', 'rise'),
 ('Heavy', 'F', MB, '.x{font-weight:900;letter-spacing:-.06em}', 'merge'),
 ('Light', 'F', MB, '.x{font-weight:200;letter-spacing:.03em}', 'track'),
 ('Condensed', 'F', MB, '.x{font-weight:700;transform:scaleX(.74);letter-spacing:.01em}',
  'close'),
 ('Accent dot', 'F', MB + '<i class="s">&#183;</i>',
  '.x{gap:.06em}.x .s{color:var(--ac);font-size:1.3em;line-height:.5}', 'drop'),
]

FAM = {'A': 'Typographic', 'B': 'Container', 'C': 'Construction',
       'D': 'Motion-native', 'E': 'Meta', 'F': 'Expressive'}

css_parts, cells = [], []
for i, (name, fam, html, css, anim) in enumerate(M, 1):
    cid = 'k%02d' % i
    css_parts.append(css.replace('.x', '.' + cid))
    a = ' an-' + anim if anim else ''
    cells.append(
        f'<figure class="cell" data-fam="{fam}">'
        f'<div class="pad"><span class="mk {cid}{a}">{html}</span></div>'
        f'<figcaption><b>{i:02d}</b> {name}<span>{FAM[fam]}</span></figcaption></figure>')

MARKCSS = '\n'.join(css_parts)

CSS = """
@font-face{font-family:Jost;src:url(data:font/woff2;base64,__JOST__) format('woff2');
 font-weight:100 900;font-style:normal;font-display:block}
@font-face{font-family:PlexMono;src:url(data:font/woff2;base64,__PLEX__) format('woff2');
 font-weight:400;font-style:normal;font-display:block}
:root{--paper:#f4f3ef;--surf:#eceae4;--ink:#0e0e0d;--line:#d5d3cc;--line2:#e4e2db;
 --muted:#6e6d66;--green:#1b6b45;--mint:#35d399;--swd:#0e0e0d;
 --mk:#1b6b45;--ac:#35d399;--gd:#eceae4;
 --mono:PlexMono,ui-monospace,Menlo,monospace;--disp:Jost,system-ui,sans-serif;
 --body:system-ui,-apple-system,"Segoe UI",sans-serif;--ms:34px}
@media(prefers-color-scheme:dark){:root:not([data-theme=light]){--paper:#0e0e0d;
 --surf:#171715;--ink:#f2f1ec;--line:#2c2c28;--line2:#232320;--muted:#95948c;
 --mk:#35d399;--ac:#1b6b45;--gd:#0e0e0d}}
:root[data-theme=dark]{--paper:#0e0e0d;--surf:#171715;--ink:#f2f1ec;--line:#2c2c28;
 --line2:#232320;--muted:#95948c;--mk:#35d399;--ac:#1b6b45;--gd:#0e0e0d}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--paper);color:var(--ink);font-family:var(--body);font-size:16px;
 line-height:1.6;-webkit-font-smoothing:antialiased}
.wrap{max-width:1120px;margin:0 auto;padding:clamp(22px,5vw,52px) clamp(16px,4vw,36px) 100px}
.lbl{font-family:var(--mono);font-size:10px;letter-spacing:.13em;text-transform:uppercase;
 color:var(--muted)}
.top{display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap;
 border-bottom:2px solid var(--ink);padding-bottom:11px}
h1{font-family:var(--disp);font-weight:700;font-size:clamp(30px,5.6vw,58px);line-height:.99;
 letter-spacing:-.035em;margin-top:26px;text-wrap:balance}
h1 em{font-style:normal;color:var(--mk)}
.intro{max-width:64ch;margin-top:16px;color:var(--muted);font-size:16px}
.intro b{color:var(--ink);font-weight:600}
.bar{position:sticky;top:0;z-index:20;display:flex;gap:7px;align-items:center;flex-wrap:wrap;
 background:var(--paper);border-bottom:1px solid var(--line);padding:11px 0;margin-top:28px}
.bar button{font-family:var(--mono);font-size:10px;letter-spacing:.11em;text-transform:uppercase;
 border:1px solid var(--line);background:transparent;color:var(--ink);padding:6px 10px;
 cursor:pointer}
.bar button[aria-pressed=true]{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.bar button:hover{border-color:var(--ink)}
.bar button:focus-visible{outline:2px solid var(--mk);outline-offset:2px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(146px,1fr));gap:12px;
 margin-top:22px}
.cell{border:1px solid var(--line2);background:var(--paper)}
.cell.hide{display:none}
.pad{aspect-ratio:1;display:grid;place-items:center;background:var(--surf);
 font-size:var(--ms);overflow:hidden;transition:font-size .35s}
body.ink .pad{background:var(--swd);--mk:var(--mint);--ac:#7ff0c0;--gd:#0e0e0d}
figcaption{font-family:var(--mono);font-size:9px;letter-spacing:.09em;text-transform:uppercase;
 color:var(--muted);padding:7px 8px;display:flex;gap:5px;align-items:baseline;
 border-top:1px solid var(--line2)}
figcaption b{color:var(--ink);font-weight:400}
figcaption span{margin-left:auto;opacity:.55}
.mk{font-family:var(--disp);font-weight:600;color:var(--mk);display:inline-flex;
 align-items:center;line-height:1;letter-spacing:-.03em}
.mk i{font-style:normal;display:inline-block}
@keyframes sp{to{transform:rotate(360deg)}}
@keyframes bl{50%{opacity:0}}
@keyframes pu{0%,100%{transform:scale(1)}50%{transform:scale(1.07)}}
.cell:hover .an-merge .b{animation:amerge .7s cubic-bezier(.16,.02,.06,1)}
@keyframes amerge{0%{transform:translateX(.5em);opacity:0}}
.cell:hover .an-close{animation:aclose .7s cubic-bezier(.16,.02,.06,1)}
@keyframes aclose{0%{transform:scale(1.22)}}
.cell:hover .an-drop{animation:adrop .6s cubic-bezier(.2,0,.13,1.06)}
@keyframes adrop{0%{transform:translateY(-.5em);opacity:0}}
.cell:hover .an-rise{animation:arise .6s cubic-bezier(.2,0,.13,1.06)}
@keyframes arise{0%{transform:translateY(.4em);opacity:0}}
.cell:hover .an-track{animation:atrack .8s cubic-bezier(.16,.02,.06,1)}
@keyframes atrack{0%{letter-spacing:.5em;opacity:.3}}
.cell:hover .an-spin{animation:aspin .8s cubic-bezier(.16,.02,.06,1)}
@keyframes aspin{0%{transform:rotate(-160deg) scale(.7);opacity:0}}
.cell:hover .an-flip{animation:aflip .75s cubic-bezier(.2,0,.13,1.06)}
@keyframes aflip{0%{transform:rotateY(-90deg)}}
.cell:hover .an-spread .a{animation:asl .6s cubic-bezier(.2,0,.13,1.06)}
.cell:hover .an-spread .b{animation:asr .6s cubic-bezier(.2,0,.13,1.06)}
@keyframes asl{0%{transform:translateX(.4em)}}
@keyframes asr{0%{transform:translateX(-.4em)}}
.cell:hover .an-wipe{animation:awipe .7s cubic-bezier(.16,.02,.06,1)}
@keyframes awipe{0%{clip-path:inset(0 100% 0 0)}}
.cell:hover .an-fill{animation:afill .7s cubic-bezier(.16,.02,.06,1)}
@keyframes afill{0%{transform:scale(.84);opacity:.2}}
.note{margin-top:40px;border:1px solid var(--line);padding:16px 18px;max-width:76ch}
.note b{font-family:var(--mono);font-size:10px;letter-spacing:.13em;text-transform:uppercase;
 color:var(--mk);display:block;margin-bottom:5px}
.note p{font-size:14.5px;color:var(--muted);line-height:1.6}
.note p+p{margin-top:9px}
.foot{margin-top:44px;border-top:2px solid var(--ink);padding-top:14px;display:flex;
 justify-content:space-between;gap:12px;flex-wrap:wrap}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
__MARKS__
"""

JS = """
var b=document.body;
function tog(id,fn){var e=document.getElementById(id);
 e.addEventListener('click',function(){var on=e.getAttribute('aria-pressed')==='true';
 e.setAttribute('aria-pressed',String(!on));fn(!on);});}
tog('ink',function(v){b.classList.toggle('ink',v);});
tog('tiny',function(v){b.style.setProperty('--ms',v?'13px':'34px');});
document.querySelectorAll('[data-f]').forEach(function(btn){
 btn.addEventListener('click',function(){
  document.querySelectorAll('[data-f]').forEach(function(o){
   o.setAttribute('aria-pressed',String(o===btn));});
  var f=btn.dataset.f;
  document.querySelectorAll('.cell').forEach(function(c){
   c.classList.toggle('hide',f!=='*'&&c.dataset.fam!==f);});
 });});
"""

fambtns = ''.join(
 '<button data-f="%s" aria-pressed="%s">%s</button>' % (k, 'true' if k == '*' else 'false', v)
 for k, v in [('*', 'All 50')] + list(FAM.items()))

html = (
 '<title>made boring &mdash; 50 MB marks</title>\n'
 '<style>' + CSS.replace('__JOST__', JOST).replace('__PLEX__', PLEX)
             .replace('__MARKS__', MARKCSS) + '</style>\n'
 '<div class="wrap">'
 '<div class="top"><span class="lbl">made boring &middot; brand</span>'
 '<span class="lbl">50 MB marks &middot; contact sheet</span></div>'
 '<h1>Fifty MB marks.<br><em>Hover any of them.</em></h1>'
 '<p class="intro">Every one is live type and CSS in your brand palette, not a picture of '
 'a logo &mdash; so anything you point at can be shipped the same day. Hover a tile to see '
 'its motion. The two controls that matter are <b>16px</b>, which drops all fifty to favicon '
 'size at once so you can see which ones die, and <b>ink</b>, which flips the ground. Filter '
 'by family to compare like with like.</p>'
 '<div class="bar"><span class="lbl">View</span>'
 '<button id="tiny" aria-pressed="false">16px</button>'
 '<button id="ink" aria-pressed="false">Ink</button>'
 '<span class="lbl" style="margin-left:8px">Family</span>' + fambtns + '</div>'
 '<div class="grid">' + ''.join(cells) + '</div>'
 '<div class="note"><b>Why these are code and not generated images</b>'
 '<p>Your account has no free image model &mdash; the unlimited tier is part of the ULTRA '
 'upgrade offer, not your current plan, so all fifty would have billed against the 172.39 '
 'credits you have left. These cost nothing.</p>'
 '<p>The bigger reason: an image model returns a picture. It cannot be recoloured for the ink '
 'ground, cannot be set beside a wordmark in the same typeface, and has to be traced before '
 'it becomes a favicon. Every mark here is already the shippable artefact.</p></div>'
 '<div class="foot"><span class="lbl">Nothing here is live on madeboring.com yet</span>'
 '<span class="lbl">Shortlist any numbers and they get built out</span></div></div>'
 '<script>' + JS + '</script>'
)
html = html.encode('ascii', 'xmlcharrefreplace').decode()
pathlib.Path('fifty.html').write_text(html)
print('written', round(len(html) / 1024, 1), 'KB &middot;', len(M), 'marks')
