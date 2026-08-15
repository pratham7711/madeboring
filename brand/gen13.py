import base64, json, os, pathlib, re

os.environ.setdefault('GLYPHS', 'plex600.json')
import centerline as CL

NM = pathlib.Path('/Users/pratham/madeboring/site/node_modules/gsap/dist')
b64 = lambda p: base64.b64encode(pathlib.Path(p).read_bytes()).decode()
GSAP = '\n'.join((NM / n).read_text() for n in
                 ['gsap.min.js', 'CustomEase.min.js',
                  'DrawSVGPlugin.min.js', 'MorphSVGPlugin.min.js'])
SANS = b64('fonts/plexsans-var.woff2')
MONO = b64('fonts/plexmono.woff2')

P = json.loads(pathlib.Path('plex600.json').read_text())
J = json.loads(pathlib.Path('glyphs.json').read_text())

TOK = re.compile(r'([MLQCZHV])([^MLQCZHV]*)')
NUM = re.compile(r'-?\d+(?:\.\d+)?')


def shift(d, tx, ty):
    """move absolute path data; H/V become L so the shift can't be lost"""
    out, pt = [], (0.0, 0.0)
    for cmd, args in TOK.findall(d):
        v = [float(x) for x in NUM.findall(args)]
        if cmd == 'Z':
            out.append('Z'); continue
        if cmd == 'H':
            cmd, v = 'L', [x for n in v for x in (n, pt[1])]
        elif cmd == 'V':
            cmd, v = 'L', [x for n in v for x in (pt[0], n)]
        if v:
            pt = (v[-2], v[-1])
        out.append(cmd + ' '.join('%.3f,%.3f' % (v[i] + tx, v[i + 1] + ty)
                                  for i in range(0, len(v), 2)))
    return ''.join(out)


def geom(G):
    GL, POS, MBP = G['glyphs'], G['pos'], G['mbpos']
    pb, tb = GL['.']['bbox'], GL['i']['tittle_bbox']
    d = dict(GL=GL, POS=POS, MBP=MBP, WORD=G['word'], W=G['wordW'],
             dotx=MBP['2']['x'], titx=POS['7']['x'], tit=GL['i']['tittle'])
    d['pc'] = (d['dotx'] + (pb[0] + pb[2]) / 2, (pb[1] + pb[3]) / 2)
    d['tc'] = (d['titx'] + (tb[0] + tb[2]) / 2, (tb[1] + tb[3]) / 2)
    return d


PG, JG = geom(P), geom(J)
NIB = json.loads(pathlib.Path('pen-plex.json').read_text())
STEM = NIB['stem']
PEN = ([('m', d, NIB['mWidth']) for d in NIB['m']]
       + [('b', d, NIB['bWidth']) for d in NIB['b']])
DOT_W = NIB['dotWidth']
VB = '-70 -840 %d 1120' % (PG['W'] + 140)
MORPH = shift(PG['tit'], PG['titx'] - PG['dotx'] - (PG['tc'][0] - PG['pc'][0]),
              -(PG['tc'][1] - PG['pc'][1]))


def word_svg(uid):
    g, GL, POS, MBP = PG, PG['GL'], PG['POS'], PG['MBP']
    o = ['<svg class="lg" viewBox="%s" aria-hidden="true">' % VB,
         '<defs><mask id="pen-%s" maskUnits="userSpaceOnUse" x="-600" y="-1600" '
         'width="%d" height="3200">'
         '<g transform="scale(1,-1)" fill="none" stroke="#fff" '
         'stroke-linecap="round" stroke-linejoin="round">'
         % (uid, PG['W'] + 1400)]
    for who, d, w in PEN:
        o.append('<path class="pen" stroke-width="%s" d="%s"%s/>'
                 % (w, d, ' transform="translate(%d,0)"' % MBP['1']['x']
                    if who == 'b' else ''))
    o.append('<path class="pen pendot" stroke-width="%s" d="M%.1f,%.1f L%.1f,%.1f"/>'
             % (DOT_W, g['pc'][0] - .5, g['pc'][1], g['pc'][0] + .5, g['pc'][1]))
    o.append('</g><rect class="open" x="-400" y="-1400" width="%d" height="2400" '
             'fill="#fff" opacity="0"/></mask></defs>' % (g['W'] + 900))
    o.append('<g mask="url(#pen-%s)"><g class="w" transform="scale(1,-1)">' % uid)
    for i, ch in enumerate(g['WORD']):
        d = GL[ch]['stem'] if ch == 'i' else GL[ch]['path']
        core = i == 0 or i == 4
        packed = 0 if i == 0 else MBP['1']['x'] if i <= 4 else MBP['2']['x']
        o.append('<path class="g %s g%d" data-x="%d" data-from="%d" '
                 'transform="translate(%s,0)"%s d="%s"/>'
                 % ('core' if core else 'mid', i, POS[str(i)]['x'], packed, packed,
                    '' if core else ' style="opacity:0"', d))
    o.append('<path class="dot" transform="translate(%d,0)" d="%s"/>'
             % (g['dotx'], GL['.']['path']))
    o.append('</g></g></svg>')
    return ''.join(o)


def mark_only(g):
    GL, MBP = g['GL'], g['MBP']
    x0, x1 = GL['m']['bbox'][0], g['dotx'] + GL['.']['bbox'][2]
    y0, y1 = min(GL['b']['bbox'][1], GL['.']['bbox'][1]), GL['b']['bbox'][3]
    p = ''.join('<path d="%s" transform="translate(%d,0)"/>' % (GL[c]['path'], x)
                for c, x in (('m', 0), ('b', MBP['1']['x']), ('.', g['dotx'])))
    return ('<svg viewBox="%.0f %.0f %.0f %.0f" fill="currentColor">'
            '<g transform="scale(1,-1)">%s</g></svg>'
            % (x0 - 40, -(y1 + 40), x1 - x0 + 80, y1 - y0 + 80, p))


CSS = """
@font-face{font-family:PlexS;src:url(data:font/woff2;base64,__S__) format('woff2');
 font-weight:100 700;font-display:block}
@font-face{font-family:PlexM;src:url(data:font/woff2;base64,__M__) format('woff2');
 font-weight:400;font-display:block}
:root{--mono:PlexM,ui-monospace,Menlo,monospace;--sans:PlexS,system-ui,sans-serif;
 --pg:#f3f0e7;--tx:#131c18;--mut:#5a655e;--ln:#ccd1c8;--ln2:#e0e4da;
 --brand:#12523a;--ac:#d99a2b;--stg:#12523a;--stgtx:#f3f0e7;--btx:#f3f0e7}
body[data-pal=forest]{--pg:#f4f3ef;--tx:#0e0e0d;--mut:#5f5e58;--ln:#d5d3cc;--ln2:#e4e2db;
 --brand:#1b6b45;--ac:#35d399;--stg:#e9e7e0;--stgtx:#1b6b45}
body[data-pal=bone]{--pg:#f6f5f1;--tx:#0b0b0b;--mut:#63625d;--ln:#d2d1cb;--ln2:#e6e5df;
 --brand:#0b0b0b;--ac:#d8331f;--stg:#0b0b0b;--stgtx:#f6f5f1}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--pg);color:var(--tx);font-family:var(--sans);font-size:18px;
 line-height:1.6;-webkit-font-smoothing:antialiased;transition:background .25s}
.wrap{max-width:1040px;margin:0 auto;padding:clamp(22px,5vw,52px) clamp(18px,4vw,36px) 100px}
.lbl{font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;
 color:var(--mut)}
.top{display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap;
 border-bottom:2px solid var(--tx);padding-bottom:12px}
h1{font-weight:600;font-size:clamp(31px,5.6vw,58px);line-height:1.03;letter-spacing:-.025em;
 margin-top:26px;text-wrap:balance}
h1 em{font-style:normal;color:var(--brand)}
.intro{max-width:62ch;margin-top:17px;font-size:19px;color:var(--mut)}
.intro b{color:var(--tx);font-weight:600}
h2{font-weight:600;font-size:clamp(22px,3.3vw,30px);letter-spacing:-.018em;margin-top:60px;
 padding-bottom:10px;border-bottom:2px solid var(--tx);display:flex;align-items:baseline;
 gap:12px;flex-wrap:wrap}
h2 span{font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;
 color:var(--mut);font-weight:400}
.sub{max-width:66ch;margin-top:13px;color:var(--mut);font-size:17px}
.sub b{color:var(--tx);font-weight:600}
.bar{position:sticky;top:0;z-index:30;display:flex;gap:8px;align-items:center;flex-wrap:wrap;
 background:var(--pg);border-bottom:1px solid var(--ln);padding:12px 0;margin-top:24px}
.bar button{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;
 border:1px solid var(--ln);background:transparent;color:var(--tx);padding:8px 12px;cursor:pointer}
.bar button[aria-pressed=true]{background:var(--tx);color:var(--pg);border-color:var(--tx)}
.bar button:hover{border-color:var(--tx)}
:focus-visible{outline:2px solid var(--ac);outline-offset:2px}
.stage{margin-top:16px;background:var(--stg);border:1px solid var(--ln2);
 padding:34px clamp(16px,4vw,44px);cursor:pointer;position:relative;color:var(--stgtx);
 display:grid;place-items:center}
.stage:after{content:"Hover or click";position:absolute;right:12px;bottom:9px;
 font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;
 opacity:0;transition:opacity .25s}
.stage:hover:after{opacity:.45}
.lg{width:100%;height:auto;max-height:132px;display:block;overflow:visible}
.g,.dot{fill:currentColor}
.ctrl{display:flex;align-items:center;gap:11px;border:1px solid var(--ln2);border-top:0;
 padding:10px 13px}
.rp{font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;
 border:1px solid var(--ln);background:transparent;color:var(--tx);padding:7px 12px;cursor:pointer}
.rp[aria-pressed=true]{background:var(--brand);border-color:var(--brand);color:var(--btx)}
.scrub{flex:1;accent-color:var(--brand);height:3px;cursor:pointer}
.tc{font-family:var(--mono);font-size:10px;color:var(--mut);min-width:52px;text-align:right;
 font-variant-numeric:tabular-nums}
.cmp{display:grid;gap:1px;background:var(--ln);border:1px solid var(--ln);margin-top:20px}
.cmp>div{background:var(--pg);padding:17px 20px;display:flex;align-items:center;gap:22px;
 flex-wrap:wrap}
.cmp svg{height:60px;width:auto;color:var(--brand);overflow:visible}
.cmp .tag{font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;
 color:var(--mut);flex:0 0 104px}
.cmp .txt{font-size:28px;font-weight:600;letter-spacing:-.02em;color:var(--brand)}
.specs{display:grid;grid-template-columns:repeat(auto-fit,minmax(138px,1fr));gap:1px;
 margin-top:20px;background:var(--ln);border:1px solid var(--ln)}
.specs div{background:var(--pg);padding:12px 14px}
.specs dt{font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;
 color:var(--mut)}
.specs dd{font-family:var(--mono);font-size:17px;margin-top:5px;font-variant-numeric:tabular-nums}
.fav{display:flex;gap:18px;flex-wrap:wrap;align-items:flex-end;margin-top:20px}
.fv{display:flex;flex-direction:column;align-items:center;gap:8px}
.fv .box{background:var(--brand);color:var(--btx);display:grid;place-items:center;
 overflow:hidden}
.fv .box svg{width:84%;height:auto;overflow:visible}
.fv span{font-family:var(--mono);font-size:9px;letter-spacing:.1em;color:var(--mut)}
.nav{margin-top:20px;border:1px solid var(--ln);background:var(--pg);display:flex;
 align-items:center;gap:26px;padding:14px 20px;flex-wrap:wrap}
.nav .brand{height:26px;color:var(--brand);display:block}
.nav .brand svg{height:100%;width:auto}
.nav a{color:var(--mut);text-decoration:none;font-size:16px}
.nav a:last-child{margin-left:auto;color:var(--btx);background:var(--brand);padding:8px 16px;
 font-weight:600}
.note{margin-top:26px;border:1px solid var(--ln);padding:18px 21px;max-width:74ch}
.note b{font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;
 color:var(--brand);display:block;margin-bottom:7px}
.note p{font-size:16.5px;color:var(--mut)}
.note p+p{margin-top:10px}
.note em{font-style:normal;color:var(--tx);font-weight:600}
.foot{margin-top:54px;border-top:2px solid var(--tx);padding-top:15px;display:flex;
 justify-content:space-between;gap:12px;flex-wrap:wrap}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
"""

JS = r"""
gsap.registerPlugin(CustomEase,DrawSVGPlugin,MorphSVGPlugin);
CustomEase.create('io','M0,0 C0.16,0.02 0.06,1 1,1');
CustomEase.create('unpack','M0,0 C0.18,0 0.12,1.03 0.48,1.008 C0.68,0.996 0.84,1 1,1');
var RM=matchMedia('(prefers-reduced-motion: reduce)').matches,D=__D__,TLS={};
document.body.dataset.pal='field';

function build(st){
  var pens=[].slice.call(st.querySelectorAll('.pen')),
      open=st.querySelector('.open'),
      moving=[].slice.call(st.querySelectorAll('.g[data-from]'))
        .filter(function(e){return !e.classList.contains('g0');}),
      mids=st.querySelectorAll('.mid'),dot=st.querySelector('.dot');
  var tl=gsap.timeline({paused:true}),
      L=pens.map(function(p){return p.getTotalLength();}),
      tot=L.slice(0,-1).reduce(function(a,c){return a+c;},0),t=0;
  pens.forEach(function(p,i){
    var d=i===pens.length-1?.22:1.6*L[i]/tot;
    tl.fromTo(p,{drawSVG:'0%'},{drawSVG:'100%',duration:d,ease:'none'},t);
    t+=d+.06;
  });
  tl.fromTo(open,{opacity:0},{opacity:1,duration:.22,ease:'io'},t);
  var at=t+.3,SL=.9,S=.05;
  moving.sort(function(a,b){return +a.dataset.x-(+b.dataset.x);});
  moving.forEach(function(el,i){
    var at2=at+i*S;
    if(+el.dataset.from!==+el.dataset.x)
      tl.fromTo(el,{x:+el.dataset.from},{x:+el.dataset.x,duration:SL,ease:'unpack'},at2);
    if(el.classList.contains('mid'))
      tl.fromTo(el,{opacity:0},{opacity:1,duration:.28,ease:'io'},at2+.1);
  });
  var dt=at+moving.length*S;
  tl.fromTo(dot,{x:D.dx,y:0},{x:D.dx+D.mx,duration:SL,ease:'unpack'},dt)
    .to(dot,{y:D.my,duration:.56,ease:'power3.out'},dt+.3)
    .to(dot,{morphSVG:D.tit,duration:.36,ease:'io'},dt+.5);
  return tl;
}
document.querySelectorAll('.stage').forEach(function(st){
  var tl=build(st),id=st.dataset.opt;TLS[id]=tl;
  var scr=document.querySelector('.scrub[data-opt="'+id+'"]'),
      tc=document.querySelector('.tc[data-opt="'+id+'"]');
  tl.eventCallback('onUpdate',function(){
    if(scr)scr.value=Math.round(tl.progress()*1000);
    if(tc)tc.textContent=tl.time().toFixed(2)+'s';});
  if(scr)scr.addEventListener('input',function(){
    tl.pause().progress(scr.value/1000);tc.textContent=tl.time().toFixed(2)+'s';});
  st.addEventListener('click',function(){tl.restart();});
  st.addEventListener('mouseenter',function(){if(!RM&&!tl.isActive())tl.restart();});
  st.addEventListener('keydown',function(e){
    if(e.key==='Enter'||e.key===' '){e.preventDefault();tl.restart();}});
  tl.progress(1).pause();
});
document.querySelectorAll('.rp:not(.lp)').forEach(function(b){
  b.addEventListener('click',function(e){e.stopPropagation();TLS[b.dataset.opt].restart();});});
document.querySelectorAll('.rp.lp').forEach(function(b){
  b.addEventListener('click',function(e){e.stopPropagation();
    var tl=TLS[b.dataset.opt],on=b.getAttribute('aria-pressed')==='true';
    b.setAttribute('aria-pressed',String(!on));
    tl.repeat(on?0:-1).repeatDelay(on?0:.9);
    if(on)tl.progress(1).pause();else tl.restart();});});
document.querySelectorAll('[data-pal]').forEach(function(btn){
  btn.addEventListener('click',function(){
    document.querySelectorAll('[data-pal]').forEach(function(o){
      o.setAttribute('aria-pressed',String(o===btn));});
    document.body.dataset.pal=btn.dataset.pal;});});
var slow=document.getElementById('slow');
slow.addEventListener('click',function(){
  var on=slow.getAttribute('aria-pressed')==='true';
  slow.setAttribute('aria-pressed',String(!on));
  gsap.globalTimeline.timeScale(on?1:.32);});
"""

D = json.dumps({'dx': PG['dotx'], 'mx': PG['tc'][0] - PG['pc'][0],
                'my': PG['tc'][1] - PG['pc'][1], 'tit': MORPH})

html = (
 '<title>mb. &mdash; drawn in the site&rsquo;s own font</title>\n'
 '<style>' + CSS.replace('__S__', SANS).replace('__M__', MONO) + '</style>\n'
 '<div class="wrap">'
 '<div class="top"><span class="lbl">made boring &middot; brand</span>'
 '<span class="lbl">IBM Plex Sans 600 &middot; the site&rsquo;s own face</span></div>'
 '<h1>One font, everywhere.<br><em>The pen now draws the real letter.</em></h1>'
 '<p class="intro">Two faults, both real. The mark was set in <b>Jost</b> while '
 'madeboring.com is set in <b>IBM Plex Sans</b>, so it could never match the page it sits '
 'on. And the pen was tracing a geometric <b>approximation</b> of the letters rather than the '
 'letters themselves. Both are fixed below. This page is set in Plex, so you are reading the '
 'argument in the font it makes.</p>'

 '<div class="bar"><span class="lbl">Palette</span>'
 '<button data-pal="field" aria-pressed="true">Field</button>'
 '<button data-pal="forest" aria-pressed="false">Forest</button>'
 '<button data-pal="bone" aria-pressed="false">Bone</button>'
 '<span class="lbl" style="margin-left:8px">Motion</span>'
 '<button id="slow" aria-pressed="false">Slow</button></div>'

 '<h2>The font was wrong<span>jost against the real thing</span></h2>'
 '<p class="sub">Top is what I had been showing you. Bottom is the site&rsquo;s actual face, '
 'beside real page text so you can see it sit correctly. Plex carries a taller x-height, a '
 'wider m, and flat-cut terminals &mdash; it is a grotesque, not a geometric sans. Nothing '
 'about the two is interchangeable.</p>'
 '<div class="cmp">'
 '<div><span class="tag">Jost 600</span>' + mark_only(JG)
 + '<span class="txt" style="font-family:system-ui">never the site font</span></div>'
 '<div><span class="tag">Plex 600</span>' + mark_only(PG)
 + '<span class="txt">we make it boring</span></div></div>'
 '<div class="specs">'
 '<div><dt>x-height</dt><dd>460 &rarr; 522</dd></div>'
 '<div><dt>m advance</dt><dd>808 &rarr; 888</dd></div>'
 '<div><dt>stem</dt><dd>' + str(STEM) + '</dd></div>'
 '<div><dt>pen</dt><dd>' + str(NIB['mWidth']) + '</dd></div>'
 '<div><dt>period</dt><dd>rounded square</dd></div>'
 '</div>'

 '<h2>The mark<span>drawn, then opened</span></h2>'
 '<p class="sub">The pen no longer draws a copy of the letter &mdash; it drives a '
 '<b>mask</b>. What appears under the nib is the real Plex glyph at every single frame, so '
 'there is no approximation on screen and no moment where one shape swaps for another. Six '
 'strokes, in the order a hand would make them: down the m&rsquo;s stem, over each arch, down '
 'the b, round its bowl, then the full stop. That stop is Plex&rsquo;s own period &mdash; not '
 'a circle, it is a rounded square &mdash; and it <b>morphs into Plex&rsquo;s own tittle</b> '
 'as it lands, because the two are genuinely different shapes.</p>'
 '<div class="stage" data-opt="final" tabindex="0" role="button" '
 'aria-label="Play the mark animation">' + word_svg('a') + '</div>'
 '<div class="ctrl"><button class="rp" data-opt="final">Replay</button>'
 '<button class="rp lp" data-opt="final" aria-pressed="false">Loop</button>'
 '<input class="scrub" type="range" min="0" max="1000" value="1000" data-opt="final" '
 'aria-label="Scrub the timeline"><span class="tc" data-opt="final">0.00s</span></div>'

 '<h2>Where it will live<span>nav and favicon</span></h2>'
 '<div class="nav"><span class="brand">' + mark_only(PG) + '</span>'
 '<a href="#">Work</a><a href="#">How we work</a><a href="#">Writing</a>'
 '<a href="#">Start a project</a></div>'
 '<div class="fav">'
 + ''.join('<div class="fv"><div class="box" style="width:%dpx;height:%dpx">%s</div>'
           '<span>%d</span></div>' % (s, s, mark_only(PG), s)
           for s in (16, 32, 48, 64, 96))
 + '</div>'

 '<div class="note"><b>On using Higgsfield for this</b>'
 '<p>I checked the model list rather than guessing. Every image model on the account is '
 '<em>generative and raster</em> &mdash; nano banana, gpt image 2, seedream, flux, z image. '
 'None of them takes &ldquo;here is IBM Plex Sans&rsquo;s m, return its centreline&rdquo;, and '
 'none emits a vector tied to a real font. The video models animate a picture, so they would '
 're-draw the letterform and destroy the exact glyph &mdash; precisely the thing you have just '
 'asked me to fix.</p>'
 '<p><em>The list still reports unlim: available false</em>, so anything I ran would spend '
 'credits, and we already spent 7.65 establishing that this class of model cannot render MB '
 'without turning it into NB.</p>'
 '<p>You still get the video. It is <em>recorded</em> from this animation rather than '
 'generated &mdash; 76 KB of mp4, 94 KB of animated webp, pixel-identical to what is on '
 'screen, and rebuilt by one command whenever the colour or timing changes.</p></div>'

 '<div class="foot"><span class="lbl">Not live on madeboring.com yet</span>'
 '<span class="lbl">Zero credits spent</span></div></div>'
 '<script>' + GSAP + '</script>\n<script>' + JS.replace('__D__', D) + '</script>'
).encode('ascii', 'xmlcharrefreplace').decode()

pathlib.Path('logo2.html').write_text(html)
print('logo2.html', round(len(html) / 1024, 1), 'KB')
print('stem %.2f  pen m %.1f  pen b %.1f  dot %.1f  strokes %d'
      % (STEM, NIB['mWidth'], NIB['bWidth'], DOT_W, len(PEN) + 1))
print('dot journey dx %.1f dy %.1f' % (PG['tc'][0] - PG['pc'][0],
                                       PG['tc'][1] - PG['pc'][1]))
