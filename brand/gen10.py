import base64, json, pathlib

from gen9 import M, FAM, MARKCSS, JOST, PLEX

GEN = pathlib.Path('gen')
MAN = json.loads((GEN / 'manifest.json').read_text())
b64 = lambda p: base64.b64encode(pathlib.Path(p).read_bytes()).decode()

KEEP = {3, 4, 6, 12, 48, 50}

tiles = []
for x in MAN:
    n = x['n']
    src = b64(GEN / ('byid/%02d.webp' % n))
    k = ' keep' if n in KEEP else ''
    tiles.append(
        f'<figure class="shot{k}" data-n="{n}" tabindex="0" role="button">'
        f'<img src="data:image/webp;base64,{src}" alt="{x["t"]}" loading="lazy" '
        f'decoding="async" width="2048" height="2048">'
        f'<figcaption><b>{n:02d}</b><span>{x["t"]}</span></figcaption></figure>')

cells = []
for i, (name, fam, html, css, anim) in enumerate(M, 1):
    a = ' an-' + anim if anim else ''
    cells.append(
        f'<figure class="cell" data-fam="{fam}">'
        f'<div class="pad"><span class="mk k{i:02d}{a}">{html}</span></div>'
        f'<figcaption><b>{i:02d}</b> {name}<span>{FAM[fam]}</span></figcaption></figure>')

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
.intro{max-width:64ch;margin-top:16px;color:var(--muted)}
.intro b{color:var(--ink);font-weight:600}
h2{font-family:var(--disp);font-weight:600;font-size:clamp(21px,3vw,29px);line-height:1.06;
 letter-spacing:-.02em;margin-top:56px;display:flex;align-items:baseline;gap:11px}
h2 span{font-family:var(--mono);font-size:10px;letter-spacing:.13em;text-transform:uppercase;
 color:var(--muted);font-weight:400}
h2+p{max-width:66ch;margin-top:9px;color:var(--muted);font-size:15px}
h2+p b{color:var(--ink);font-weight:600}
.bar{position:sticky;top:0;z-index:20;display:flex;gap:7px;align-items:center;flex-wrap:wrap;
 background:var(--paper);border-bottom:1px solid var(--line);padding:11px 0;margin-top:20px}
.bar button{font-family:var(--mono);font-size:10px;letter-spacing:.11em;text-transform:uppercase;
 border:1px solid var(--line);background:transparent;color:var(--ink);padding:6px 10px;
 cursor:pointer}
.bar button[aria-pressed=true]{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.bar button:hover{border-color:var(--ink)}
.bar button:focus-visible,.shot:focus-visible{outline:2px solid var(--mk);outline-offset:2px}
.shots{display:grid;grid-template-columns:repeat(auto-fill,minmax(168px,1fr));gap:12px;
 margin-top:20px}
.shot{border:1px solid var(--line2);background:var(--surf);cursor:zoom-in;position:relative}
.shot.hide{display:none}
.shot img{display:block;width:100%;height:auto;aspect-ratio:1}
.shot.keep:before{content:"";position:absolute;left:8px;top:8px;width:7px;height:7px;
 border-radius:50%;background:var(--mk);z-index:2}
figcaption{font-family:var(--mono);font-size:9px;letter-spacing:.09em;text-transform:uppercase;
 color:var(--muted);padding:7px 8px;display:flex;gap:5px;align-items:baseline;
 border-top:1px solid var(--line2);background:var(--paper)}
figcaption b{color:var(--ink);font-weight:400;flex:0 0 auto}
.shot figcaption span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(146px,1fr));gap:12px;
 margin-top:20px}
.cell{border:1px solid var(--line2);background:var(--paper)}
.cell.hide{display:none}
.pad{aspect-ratio:1;display:grid;place-items:center;background:var(--surf);
 font-size:var(--ms);overflow:hidden;transition:font-size .35s}
body.ink .pad{background:var(--swd);--mk:var(--mint);--ac:#7ff0c0;--gd:#0e0e0d}
.cell figcaption span{margin-left:auto;opacity:.55}
.mk{font-family:var(--disp);font-weight:600;color:var(--mk);display:inline-flex;
 align-items:center;line-height:1;letter-spacing:-.03em}
.mk i{font-style:normal;display:inline-block}
.note{margin-top:26px;border:1px solid var(--line);padding:16px 18px;max-width:76ch}
.note b{font-family:var(--mono);font-size:10px;letter-spacing:.13em;text-transform:uppercase;
 color:var(--mk);display:block;margin-bottom:5px}
.note p{font-size:14.5px;color:var(--muted);line-height:1.62}
.note p+p{margin-top:9px}
.note em{font-style:normal;color:var(--ink);font-weight:600}
.lb{position:fixed;inset:0;z-index:60;background:rgba(14,14,13,.93);display:none;
 place-items:center;padding:26px;cursor:zoom-out}
.lb.on{display:grid}
.lb figure{max-width:min(720px,86vw);cursor:default}
.lb img{display:block;width:100%;height:auto;border:1px solid #2c2c28}
.lb figcaption{background:#0e0e0d;border-color:#2c2c28;color:#95948c;
 font-size:10px;padding:9px 2px;white-space:normal;display:block;line-height:1.7}
.lb figcaption b{color:#f2f1ec;margin-right:7px}
.lbnav{position:absolute;bottom:20px;left:0;right:0;display:flex;justify-content:center;gap:8px}
.lbnav button{font-family:var(--mono);font-size:10px;letter-spacing:.11em;
 text-transform:uppercase;border:1px solid #3a3a35;background:transparent;color:#f2f1ec;
 padding:7px 13px;cursor:pointer}
.lbnav button:hover{border-color:#f2f1ec}
.foot{margin-top:52px;border-top:2px solid var(--ink);padding-top:14px;display:flex;
 justify-content:space-between;gap:12px;flex-wrap:wrap}
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
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
__MARKS__
"""

JS = """
var b=document.body,DATA=__DATA__;
function tog(id,fn){var e=document.getElementById(id);if(!e)return;
 e.addEventListener('click',function(){var on=e.getAttribute('aria-pressed')==='true';
 e.setAttribute('aria-pressed',String(!on));fn(!on);});}
tog('ink',function(v){b.classList.toggle('ink',v);});
tog('tiny',function(v){b.style.setProperty('--ms',v?'13px':'34px');});
tog('keep',function(v){document.querySelectorAll('.shot').forEach(function(s){
 s.classList.toggle('hide',v&&!s.classList.contains('keep'));});});
document.querySelectorAll('[data-f]').forEach(function(btn){
 btn.addEventListener('click',function(){
  document.querySelectorAll('[data-f]').forEach(function(o){
   o.setAttribute('aria-pressed',String(o===btn));});
  var f=btn.dataset.f;
  document.querySelectorAll('.cell').forEach(function(c){
   c.classList.toggle('hide',f!=='*'&&c.dataset.fam!==f);});});});

var lb=document.getElementById('lb'),lbi=document.getElementById('lbi'),
    lbc=document.getElementById('lbc'),cur=0;
function open(n){cur=n;var s=document.querySelector('.shot[data-n="'+n+'"]');
 lbi.src=s.querySelector('img').src;
 lbc.innerHTML='<b>'+(n<10?'0':'')+n+'</b>'+DATA[n-1];
 lb.classList.add('on');}
function step(d){var n=cur+d;if(n<1)n=DATA.length;if(n>DATA.length)n=1;open(n);}
document.querySelectorAll('.shot').forEach(function(s){
 s.addEventListener('click',function(){open(+s.dataset.n);});
 s.addEventListener('keydown',function(e){
  if(e.key==='Enter'||e.key===' '){e.preventDefault();open(+s.dataset.n);}});});
lb.addEventListener('click',function(e){if(e.target===lb)lb.classList.remove('on');});
document.getElementById('prev').addEventListener('click',function(e){
 e.stopPropagation();step(-1);});
document.getElementById('next').addEventListener('click',function(e){
 e.stopPropagation();step(1);});
document.getElementById('close').addEventListener('click',function(e){
 e.stopPropagation();lb.classList.remove('on');});
document.addEventListener('keydown',function(e){
 if(!lb.classList.contains('on'))return;
 if(e.key==='Escape')lb.classList.remove('on');
 if(e.key==='ArrowLeft')step(-1);
 if(e.key==='ArrowRight')step(1);});
"""

fambtns = ''.join(
 '<button data-f="%s" aria-pressed="%s">%s</button>' % (k, 'true' if k == '*' else 'false', v)
 for k, v in [('*', 'All 50')] + list(FAM.items()))

esc = lambda s: s.replace('&', '&amp;').replace('<', '&lt;').replace('"', '&quot;')
DATA = json.dumps([esc(x['prompt']) for x in MAN])

html = (
 '<title>made boring &mdash; 101 MB marks</title>\n'
 '<style>' + CSS.replace('__JOST__', JOST).replace('__PLEX__', PLEX)
             .replace('__MARKS__', MARKCSS) + '</style>\n'
 '<div class="wrap">'
 '<div class="top"><span class="lbl">made boring &middot; brand</span>'
 '<span class="lbl">51 generated &middot; 50 coded</span></div>'
 '<h1>Everything the MB pass produced.<br><em>Generated above, shippable below.</em></h1>'
 '<p class="intro">The top half is the image model &mdash; 51 renders on '
 '<b>z_image</b>, 7.65 credits, already paid for and already downloaded at 2048px. The bottom '
 'half is the fifty marks built from live type and CSS, which cost nothing. They are on one '
 'page because they do different jobs: the renders are a mood board that tells you which '
 '<b>material and construction</b> you respond to, and the coded marks are the things that can '
 'actually ship as a favicon on Monday.</p>'

 '<h2>Generated<span>51 renders &middot; click any tile</span></h2>'
 '<p>Click for full size and the exact prompt that made it. The green dot marks the six I would '
 'keep. <b>Read them as direction, not as logos</b> &mdash; the honest verdict is under the grid.</p>'
 '<div class="bar"><span class="lbl">View</span>'
 '<button id="keep" aria-pressed="false">Only my six</button></div>'
 '<div class="shots">' + ''.join(tiles) + '</div>'

 '<div class="note"><b>What actually came back</b>'
 '<p><em>The recurring failure is the same one every time.</em> Ask a model to merge M and B '
 'onto a shared stem and it fuses the M&rsquo;s right leg into the B, which leaves a shape that '
 'reads <em>NB</em>, not MB. Look at 48, 41, 32, 27 &mdash; the construction is elegant and the '
 'letter is wrong. That is not a prompt you can fix; it is what a shared stem does to an M.</p>'
 '<p><em>It also ignored &ldquo;geometric sans-serif&rdquo; almost everywhere.</em> Nearly all '
 'of these are serifed or slabbed, which fights Jost on the rest of the site. The first twelve '
 'were generated before I added that phrase, and adding it moved the needle less than expected.</p>'
 '<p><em>What is genuinely useful:</em> 06 and 50, the blueprint pair, because the '
 'dimension-callout treatment is the spec-sheet voice the site already speaks in &mdash; that is '
 'worth stealing as a device even though the letterform under it is wrong. 12, letterpress, for '
 'the framing. 03 and 04 for the silhouette test. None of these are traceable into a mark '
 'without redrawing the letters, so treat the whole grid as reference.</p></div>'

 '<h2>Coded<span>50 marks &middot; live type, not pictures</span></h2>'
 '<p>Every one of these is real type and CSS in your palette, so anything you point at ships the '
 'same day. Hover a tile for its motion. <b>16px</b> drops all fifty to favicon size at once so '
 'you can see which ones die; <b>Ink</b> flips the ground.</p>'
 '<div class="bar"><span class="lbl">View</span>'
 '<button id="tiny" aria-pressed="false">16px</button>'
 '<button id="ink" aria-pressed="false">Ink</button>'
 '<span class="lbl" style="margin-left:8px">Family</span>' + fambtns + '</div>'
 '<div class="grid">' + ''.join(cells) + '</div>'

 '<div class="foot"><span class="lbl">Nothing here is live on madeboring.com yet</span>'
 '<span class="lbl">No further credits spent &middot; 164.74 remaining</span></div></div>'

 '<div class="lb" id="lb"><figure><img id="lbi" alt="">'
 '<figcaption id="lbc"></figcaption></figure>'
 '<div class="lbnav"><button id="prev">&larr; Prev</button>'
 '<button id="close">Close</button><button id="next">Next &rarr;</button></div></div>'
 '<script>' + JS.replace('__DATA__', DATA) + '</script>'
)
html = html.encode('ascii', 'xmlcharrefreplace').decode()
pathlib.Path('hundred.html').write_text(html)
print('written', round(len(html) / 1024 / 1024, 2), 'MB &middot;',
      len(MAN), 'renders +', len(M), 'coded')
