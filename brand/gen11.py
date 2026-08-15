import base64, json, pathlib

SCRATCH = pathlib.Path('/private/tmp/claude-502/-Users-pratham/'
                       '4eed19d0-0848-4e3a-a61e-012788cbfae7/scratchpad')
NM = pathlib.Path('/Users/pratham/madeboring/site/node_modules/gsap/dist')
b64 = lambda p: base64.b64encode(pathlib.Path(p).read_bytes()).decode()


def js(n):
    t = (NM / n).read_text()
    assert '</script' not in t.lower(), n
    return t


JOST, PLEX = b64(SCRATCH / 'jost.woff2'), b64(SCRATCH / 'plexmono.woff2')
GSAP = '\n'.join(js(n) for n in ['gsap.min.js', 'CustomEase.min.js',
                                 'DrawSVGPlugin.min.js', 'MotionPathPlugin.min.js'])

G = json.loads(pathlib.Path('glyphs.json').read_text())
SK = json.loads(pathlib.Path('skeleton.json').read_text())
GL, POS, MBP = G['glyphs'], G['pos'], G['mbpos']
WORD = G['word']

DOT_R = (GL['.']['bbox'][2] - GL['.']['bbox'][0]) / 2
DOT_X = MBP['2']['x'] + (GL['.']['bbox'][0] + GL['.']['bbox'][2]) / 2
DOT_Y = (GL['.']['bbox'][1] + GL['.']['bbox'][3]) / 2
TIT = GL['i']['tittle_bbox']
TIT_R = (TIT[2] - TIT[0]) / 2
TIT_X = POS['7']['x'] + (TIT[0] + TIT[2]) / 2
TIT_Y = (TIT[1] + TIT[3]) / 2

VB = '-70 -830 %d 1080' % (G['wordW'] + 140)
MBVB = '30 -826 1660 890'


def word_svg(vb, cls=''):
    """every glyph of madeboring, parked at its mb. position, plus the flying dot"""
    out = ['<svg class="lg %s" viewBox="%s" aria-hidden="true">'
           '<g class="w" transform="scale(1,-1)">' % (cls, vb)]
    for i, ch in enumerate(WORD):
        p = GL[ch]
        d = p['stem'] if ch == 'i' else p['path']
        # m and b are present from the start; everything else grows in
        role = 'core' if (i == 0 or i == 4) else 'mid'
        mbx = MBP['1']['x'] if i == 4 else POS[str(i)]['x']
        out.append('<path class="g %s g%d" data-ch="%s" data-x="%d" data-mbx="%s" '
                   'transform="translate(%s,0)" style="%s" d="%s"/>'
                   % (role, i, ch, POS[str(i)]['x'], mbx, mbx,
                      '' if role == 'core' else 'opacity:0', d))
    out.append('<circle class="dot" cx="%.1f" cy="%.1f" r="%.1f"/>'
               % (DOT_X, DOT_Y, DOT_R))
    out.append('<g class="sk">')
    for d in SK['m']:
        out.append('<path d="%s" stroke-width="%s"/>' % (d, SK['stem']))
    for d in SK['b']:
        out.append('<path d="%s" stroke-width="%s" transform="translate(%d,0)"/>'
                   % (d, SK['bstem'], SK['bx']))
    out.append('<path class="skdot" d="%s" stroke-width="%s"/>'
               % (SK['dot'], SK['dotStroke']))
    out.append('</g>')
    out.append('</g></svg>')
    return ''.join(out)


def mech_svg():
    """the annotated diagram: full word, dot parked on the i, flight path drawn"""
    out = ['<svg class="lg mechsvg" viewBox="-70 -960 %d 1210" aria-hidden="true">'
           '<g transform="scale(1,-1)">' % (G['wordW'] + 140)]
    for i, ch in enumerate(WORD):
        d = GL[ch]['stem'] if ch == 'i' else GL[ch]['path']
        out.append('<path class="g" transform="translate(%d,0)" d="%s"/>'
                   % (POS[str(i)]['x'], d))
    mid_x, mid_y = (DOT_X + TIT_X) / 2, DOT_Y + (TIT_Y - DOT_Y) * 1.46
    out.append('<path class="flight" d="M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f"/>'
               % (DOT_X, DOT_Y, mid_x, mid_y, TIT_X, TIT_Y))
    out.append('<circle class="ghost" cx="%.1f" cy="%.1f" r="%.1f"/>'
               % (DOT_X, DOT_Y, DOT_R))
    out.append('<circle class="dot" cx="%.1f" cy="%.1f" r="%.1f"/>'
               % (TIT_X, TIT_Y, TIT_R))
    out.append('</g></svg>')
    return ''.join(out)


def mb_svg(cls=''):
    """the resting mark on its own: m, b, dot"""
    out = ['<svg class="mbm %s" viewBox="%s" aria-hidden="true">'
           '<g transform="scale(1,-1)">' % (cls, MBVB)]
    for ch, x in (('m', 0), ('b', MBP['1']['x'])):
        out.append('<path d="%s" transform="translate(%d,0)"/>' % (GL[ch]['path'], x))
    out.append('<circle cx="%.1f" cy="%.1f" r="%.1f"/>' % (DOT_X, DOT_Y, DOT_R))
    out.append('</g></svg>')
    return ''.join(out)


OPTS = [
 ('trace', 'Trace', 'the mark draws itself, then opens',
  '1.15s draw &middot; 0.95s open',
  'The longest, most deliberate draw of the five &mdash; a full 1.15s with a wide gap between '
  'the m and the b, so you watch each letter being made. Afterwards the word opens gently and '
  'the dot takes the highest arc. This is the one for a loading state or the first paint of '
  'the homepage, where you have the time to spend.'),
 ('unpack', 'Unpack', 'the letters were hiding behind m and b',
  '0.85s draw &middot; 0.90s open',
  'A quick, even draw, then the opposite idea: <b>ade</b> and <b>oring</b> are uncovered by a '
  'wipe that opens outward from the '
  'seam between the two letters, so it reads as though the full name was always there and '
  '<b>mb.</b> was just the closed state. The dot takes the flattest path of the five.'),
 ('typeset', 'Typeset', 'letter by letter, mechanical',
  '0.90s draw &middot; 1.05s open',
  'The draw itself is linear &mdash; no easing at all &mdash; and the m and b are spaced a '
  'clear beat apart, so it reads as a plotter rather than a hand. The middle letters then land '
  'one at a time on that same fixed beat. This is '
  'the most <em>boring</em> of the five in the way the brand means it &mdash; it looks like a '
  'machine setting type, not a designer showing off. Pairs with the spec-sheet voice already '
  'on the site.'),
 ('pivot', 'Pivot', 'the dot leads and the word appears under it',
  '0.95s draw &middot; 1.10s open',
  'The draw is tight and the letters come almost together, because the interest is in what '
  'happens next: the dot launches and every letter resolves as the dot passes over it, so '
  'the dot is doing the work rather than arriving as an afterthought. It is the one execution '
  'where the payoff and the mechanism are the same gesture.'),
 ('stamp', 'Stamp', 'one beat, no ceremony',
  '0.45s draw &middot; 0.55s open',
  'The draw is compressed to 0.45s and the open to 0.55s, so the whole thing is done in a '
  'second flat. Everything arrives together and the dot lands last with a single squash. This '
  'is the one that survives being triggered forty times a session in a sticky nav without '
  'becoming irritating.'),
]

PALS = [
 ('forest', 'Forest', 'shipping now',
  'The palette already on madeboring.com. Nothing here is wrong &mdash; it is just quiet '
  'enough that the site reads as a document rather than a product.'),
 ('field', 'Field', 'recommended',
  'The green stops being an accent and becomes the ground. Cream type on a deep field, amber '
  'only on things you can click. Almost nobody in this category commits to a coloured field, '
  'which is exactly why it will not read as another AI landing page.'),
 ('signal', 'Signal', 'replit energy',
  'Near-black with one hot orange. It is the most immediately modern and the most dangerous '
  '&mdash; orange on black over a dev-tool site is Replit&rsquo;s exact signature, and you '
  'will be read as derivative by the audience you most want.'),
 ('bone', 'Bone', 'the pure version',
  'Bone, ink, and a single vermilion hairline. The most literal reading of the name and the '
  'hardest to get wrong. It asks the typography and the spacing to carry everything, with '
  'nothing to hide behind.'),
]

stages = []
for i, (o, name, kick, timing, body) in enumerate(OPTS):
    star = ' star' if o == 'pivot' else ''
    stages.append(f'''
<section class="card{star}" id="opt-{o}">
  <div class="chead"><span class="num">{i+1:02d}</span><h3>{name}</h3>
    <span class="kick">{kick}</span><span class="timing">{timing}</span></div>
  <p class="body">{body}</p>
  <div class="stage" data-opt="{o}" tabindex="0" role="button"
    aria-label="Play the {name} animation">{word_svg(VB)}</div>
  <div class="ctrl"><button class="rp" data-opt="{o}">Replay</button>
    <button class="rp lp" data-opt="{o}" aria-pressed="false">Loop</button>
    <input class="scrub" type="range" min="0" max="1000" value="1000" data-opt="{o}"
      aria-label="Scrub {name}"><span class="tc" data-opt="{o}">0.00s</span></div>
</section>''')

pal_btns = ''.join(
 '<button class="pb" data-pal="%s" aria-pressed="%s"><i></i>%s</button>'
 % (k, 'true' if k == 'field' else 'false', n) for k, n, _, _ in PALS)
pal_notes = ''.join(
 '<div class="pn" data-pal="%s"><b>%s <span>%s</span></b><p>%s</p></div>'
 % (k, n, tag, body) for k, n, tag, body in PALS)

CSS = """
@font-face{font-family:Jost;src:url(data:font/woff2;base64,__JOST__) format('woff2');
 font-weight:100 900;font-style:normal;font-display:block}
@font-face{font-family:PlexMono;src:url(data:font/woff2;base64,__PLEX__) format('woff2');
 font-weight:400;font-style:normal;font-display:block}
:root{--mono:PlexMono,ui-monospace,Menlo,monospace;--disp:Jost,system-ui,sans-serif;
 --body:system-ui,-apple-system,"Segoe UI",sans-serif;
 --pg:#f4f3ef;--tx:#0e0e0d;--mut:#5f5e58;--ln:#d5d3cc;--ln2:#e4e2db;
 --brand:#1b6b45;--ac:#35d399;--stg:#eceae4;--stgtx:#1b6b45;--btx:#f4f3ef}
body[data-pal=field]{--pg:#f3f0e7;--tx:#131c18;--mut:#5a6660;--ln:#cfd3cb;--ln2:#e2e5dd;
 --brand:#12523a;--ac:#d99a2b;--stg:#12523a;--stgtx:#f3f0e7;--btx:#f3f0e7}
body[data-pal=signal]{--pg:#0d0d0e;--tx:#f2f1ec;--mut:#918f89;--ln:#2b2b2d;--ln2:#1e1e20;
 --brand:#ff5b22;--ac:#ff5b22;--stg:#151517;--stgtx:#ff5b22;--btx:#0d0d0e}
body[data-pal=bone]{--pg:#f6f5f1;--tx:#0b0b0b;--mut:#63625d;--ln:#d2d1cb;--ln2:#e6e5df;
 --brand:#0b0b0b;--ac:#d8331f;--stg:#0b0b0b;--stgtx:#f6f5f1;--btx:#f6f5f1}
@media(prefers-color-scheme:dark){body:not([data-theme=light])[data-pal=forest]{
 --pg:#0e0e0d;--tx:#f2f1ec;--mut:#96958d;--ln:#2c2c28;--ln2:#232320;
 --brand:#35d399;--ac:#1b6b45;--stg:#171715;--stgtx:#35d399;--btx:#0e0e0d}
 body:not([data-theme=light])[data-pal=field]{--pg:#0d1a14;--tx:#eef2ea;--mut:#8fa096;
 --ln:#22332a;--ln2:#182620;--brand:#7fd6a8;--ac:#e5b356;--stg:#12523a;--stgtx:#f3f0e7;
 --btx:#0d1a14}
 body:not([data-theme=light])[data-pal=bone]{--pg:#0b0b0b;--tx:#f6f5f1;--mut:#8b8a85;
 --ln:#282826;--ln2:#1b1b1a;--brand:#f6f5f1;--ac:#ff5540;--stg:#f6f5f1;--stgtx:#0b0b0b;
 --btx:#0b0b0b}}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--pg);color:var(--tx);font-family:var(--body);font-size:17px;
 line-height:1.62;-webkit-font-smoothing:antialiased;
 transition:background .35s,color .35s}
.wrap{max-width:1080px;margin:0 auto;padding:clamp(22px,5vw,54px) clamp(18px,4vw,38px) 110px}
.lbl,.num,.kick,.timing,.cap,.tc{font-family:var(--mono);letter-spacing:.13em;
 text-transform:uppercase}
.lbl{font-size:11px;color:var(--mut)}
.top{display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap;
 border-bottom:2px solid var(--tx);padding-bottom:12px}
h1{font-family:var(--disp);font-weight:700;font-size:clamp(34px,6.4vw,68px);line-height:.98;
 letter-spacing:-.035em;margin-top:30px;text-wrap:balance}
h1 em{font-style:normal;color:var(--brand)}
.intro{max-width:62ch;margin-top:18px;font-size:19px;color:var(--mut);line-height:1.6}
.intro b{color:var(--tx);font-weight:600}
h2{font-family:var(--disp);font-weight:600;font-size:clamp(24px,3.5vw,34px);line-height:1.04;
 letter-spacing:-.022em;margin-top:70px;padding-bottom:11px;border-bottom:2px solid var(--tx);
 display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}
h2 span{font-family:var(--mono);font-size:11px;letter-spacing:.13em;text-transform:uppercase;
 color:var(--mut);font-weight:400}
h2+.sub{max-width:66ch;margin-top:14px;color:var(--mut);font-size:17px}
h2+.sub b{color:var(--tx);font-weight:600}

.bar{position:sticky;top:0;z-index:30;display:flex;gap:8px;align-items:center;flex-wrap:wrap;
 background:var(--pg);border-bottom:1px solid var(--ln);padding:12px 0;margin-top:26px}
.bar button,.pb{font-family:var(--mono);font-size:11px;letter-spacing:.1em;
 text-transform:uppercase;border:1px solid var(--ln);background:transparent;color:var(--tx);
 padding:8px 12px;cursor:pointer;display:inline-flex;align-items:center;gap:7px}
.bar button:hover,.pb:hover{border-color:var(--tx)}
.bar button[aria-pressed=true],.pb[aria-pressed=true]{background:var(--tx);color:var(--pg);
 border-color:var(--tx)}
.pb i{width:11px;height:11px;border-radius:50%;display:block;border:1px solid rgba(0,0,0,.14)}
.pb[data-pal=forest] i{background:#1b6b45}
.pb[data-pal=field] i{background:#12523a}
.pb[data-pal=signal] i{background:#ff5b22}
.pb[data-pal=bone] i{background:#0b0b0b}
:focus-visible{outline:2px solid var(--ac);outline-offset:2px}

.mech{margin-top:22px;border:1px solid var(--ln);background:var(--stg);padding:26px 22px;
 color:var(--stgtx)}
.mech .lg{width:100%;height:auto;max-height:250px}
.mech .g{fill:currentColor}
.mech .dot{fill:currentColor}
.mechsvg .flight{fill:none;stroke:currentColor;stroke-width:7;stroke-dasharray:26 20;
 opacity:.5}
.mechsvg .ghost{fill:none;stroke:currentColor;stroke-width:7;stroke-dasharray:14 12;
 opacity:.5}
.mechsvg .flight{stroke-linecap:round}
.specs{display:grid;grid-template-columns:repeat(auto-fit,minmax(148px,1fr));gap:1px;
 margin-top:20px;background:var(--ln);border:1px solid var(--ln)}
.specs div{background:var(--pg);padding:12px 14px}
.specs dt{font-family:var(--mono);font-size:10px;letter-spacing:.13em;text-transform:uppercase;
 color:var(--mut)}
.specs dd{font-family:var(--mono);font-size:19px;margin-top:5px;font-variant-numeric:tabular-nums}

.card{margin-top:34px;border-top:1px solid var(--ln);padding-top:20px}
.card.star{border-top:2px solid var(--brand)}
.chead{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}
.num{font-size:11px;color:var(--mut)}
.chead h3{font-family:var(--disp);font-weight:600;font-size:27px;letter-spacing:-.02em}
.kick{font-size:11px;color:var(--brand)}
.timing{font-size:11px;color:var(--mut);margin-left:auto}
.card .body{max-width:70ch;margin-top:10px;color:var(--mut);font-size:16.5px}
.card .body b{color:var(--tx);font-weight:600}
.card .body em{font-style:italic}
.stage{margin-top:16px;background:var(--stg);border:1px solid var(--ln2);
 padding:34px clamp(16px,4vw,44px);cursor:pointer;position:relative;color:var(--stgtx);
 min-height:170px;display:grid;place-items:center;transition:background .35s,color .35s}
.stage:after{content:"Hover or click to play";position:absolute;right:12px;bottom:9px;
 font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;
 opacity:0;transition:opacity .25s;pointer-events:none}
.stage:hover:after{opacity:.45}
.lg{width:100%;height:auto;max-height:150px;display:block;overflow:visible}
.g{fill:currentColor}
.dot{fill:currentColor}
.sk{opacity:0}
.sk path{fill:none;stroke:currentColor;stroke-linecap:butt;stroke-linejoin:round}
.sk .skdot{stroke-linecap:round}
.ctrl{display:flex;align-items:center;gap:11px;border:1px solid var(--ln2);border-top:0;
 padding:10px 13px}
.rp{font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;
 border:1px solid var(--ln);background:transparent;color:var(--tx);padding:7px 12px;
 cursor:pointer}
.rp:hover{border-color:var(--tx)}
.rp[aria-pressed=true]{background:var(--brand);border-color:var(--brand);color:var(--btx)}
.scrub{flex:1;accent-color:var(--brand);height:3px;cursor:pointer}
.tc{font-size:10px;color:var(--mut);min-width:50px;text-align:right;
 font-variant-numeric:tabular-nums}

.nav{margin-top:22px;border:1px solid var(--ln);background:var(--pg);display:flex;
 align-items:center;gap:20px;padding:15px 20px}
.nav .navlogo{cursor:pointer;flex:0 0 auto;width:210px}
.nav .lg{max-height:26px}
.nav .links{margin-left:auto;display:flex;gap:22px;flex-wrap:wrap}
.nav .links a{font-size:14.5px;color:var(--mut);text-decoration:none}
.nav .links a:hover{color:var(--tx)}
.nav .cta{background:var(--ac);color:var(--btx);padding:9px 16px;font-size:14.5px;
 font-weight:600;text-decoration:none}
body[data-pal=bone] .nav .cta,body[data-pal=signal] .nav .cta{color:#fff}

.fav{display:flex;gap:16px;flex-wrap:wrap;align-items:flex-end;margin-top:22px}
.fv{display:flex;flex-direction:column;align-items:center;gap:8px}
.fv .box{background:var(--stg);border:1px solid var(--ln2);display:grid;place-items:center;
 color:var(--stgtx)}
.fv .box.solid{background:var(--brand);color:var(--btx);border-color:var(--brand)}
.fv .box .mbm{width:78%;height:auto}
.fv .mbm path,.fv .mbm circle{fill:currentColor}
.f16 .box{width:16px;height:16px}.f32 .box{width:32px;height:32px}
.f48 .box{width:48px;height:48px}.f64 .box{width:64px;height:64px}
.f96 .box{width:96px;height:96px;border-radius:20px}
.fv span{font-family:var(--mono);font-size:9px;letter-spacing:.1em;text-transform:uppercase;
 color:var(--mut)}
.tabsim{margin-top:24px;display:flex;align-items:center;gap:9px;border:1px solid var(--ln);
 padding:9px 13px;max-width:330px;background:var(--stg);color:var(--stgtx)}
.tabsim .box{width:16px;height:16px;display:grid;place-items:center;flex:0 0 16px}
.tabsim .mbm{width:100%;height:auto}
.tabsim .mbm path,.tabsim .mbm circle{fill:currentColor}
.tabsim b{font-size:13px;font-weight:400;white-space:nowrap;overflow:hidden;
 text-overflow:ellipsis;color:var(--stgtx);opacity:.85}

.pals{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px;
 margin-top:22px}
.pal{border:1px solid var(--ln);overflow:hidden}
.pal .sw{height:74px;display:flex}
.pal .sw i{flex:1}
.pal .cap{display:block;padding:9px 11px;font-size:10px;color:var(--mut);
 border-top:1px solid var(--ln)}
.pn{display:none;margin-top:20px;border-left:3px solid var(--brand);padding:4px 0 4px 16px;
 max-width:70ch}
.pn.on{display:block}
.pn b{font-family:var(--disp);font-size:21px;font-weight:600;letter-spacing:-.01em;
 display:flex;gap:10px;align-items:baseline}
.pn b span{font-family:var(--mono);font-size:10px;letter-spacing:.13em;text-transform:uppercase;
 color:var(--brand);font-weight:400}
.pn p{margin-top:7px;color:var(--mut);font-size:16.5px}

.note{margin-top:30px;border:1px solid var(--ln);padding:19px 21px;max-width:74ch}
.note b{font-family:var(--mono);font-size:11px;letter-spacing:.13em;text-transform:uppercase;
 color:var(--brand);display:block;margin-bottom:7px}
.note p{font-size:16px;color:var(--mut)}
.note p+p{margin-top:10px}
.note em{font-style:normal;color:var(--tx);font-weight:600}
.foot{margin-top:60px;border-top:2px solid var(--tx);padding-top:15px;display:flex;
 justify-content:space-between;gap:12px;flex-wrap:wrap}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
"""

JS = r"""
gsap.registerPlugin(CustomEase,DrawSVGPlugin,MotionPathPlugin);
CustomEase.create('io','M0,0 C0.16,0.02 0.06,1 1,1');
CustomEase.create('settle','M0,0 C0.2,0 0.13,1.06 1,1');
CustomEase.create('heavy','M0,0 C0.62,0 0.1,1 1,1');
var RM=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
var TLS={},D=__DOT__;
document.body.dataset.pal='field';
document.querySelectorAll('.pn').forEach(function(n){
  n.classList.toggle('on',n.dataset.pal==='field');});

function parts(st){
  return {mids:st.querySelectorAll('.mid'),m:st.querySelector('.g0'),
          b:st.querySelector('.g4'),dot:st.querySelector('.dot'),
          all:st.querySelectorAll('.g'),
          sk:st.querySelector('.sk'),
          skp:st.querySelectorAll('.sk path')};
}
/* every glyph starts parked where mb. puts it; mids are invisible */
function rest(st){
  var p=parts(st);
  gsap.set(p.all,{x:function(i,t){return +t.getAttribute('data-mbx');},
    fillOpacity:1,strokeOpacity:0,opacity:1});
  gsap.set(p.mids,{opacity:0});
  gsap.set(p.dot,{x:0,y:0,scale:1,transformOrigin:'50% 50%',opacity:1});
  if(p.sk)gsap.set(p.sk,{opacity:0});
}
function open(tl,st,cfg){
  var p=parts(st),dx=D.tx-D.x,dy=D.ty-D.y,s=D.tr/D.r;
  tl.to(p.b,{x:+p.b.getAttribute('data-x'),duration:cfg.slide,ease:cfg.ease},cfg.at);
  if(cfg.reveal==='stagger')
    tl.fromTo(p.mids,{opacity:0,y:14},{opacity:1,y:0,duration:.42,ease:'io',
      stagger:cfg.stagger},cfg.at+.06);
  else if(cfg.reveal==='steps')
    tl.fromTo(p.mids,{opacity:0},{opacity:1,duration:.01,
      stagger:{each:cfg.stagger,ease:'none'}},cfg.at+.1);
  else if(cfg.reveal==='wipe')
    tl.fromTo(p.mids,{opacity:0,scaleX:.2,transformOrigin:'0% 50%'},
      {opacity:1,scaleX:1,duration:.5,ease:'io',stagger:{each:.035,from:'center'}},cfg.at);
  else if(cfg.reveal==='chase'){
    /* each letter resolves as the dot sweeps past its own x */
    p.mids.forEach(function(el){
      var gx=+el.getAttribute('data-x'),f=(gx-D.x)/(D.tx-D.x);
      tl.fromTo(el,{opacity:0,y:9},{opacity:1,y:0,duration:.3,ease:'io'},
        cfg.at+Math.max(0,Math.min(1,f))*cfg.flight*.82);});
  }
  else tl.fromTo(p.mids,{opacity:0,scale:.94,transformOrigin:'50% 100%'},
      {opacity:1,scale:1,duration:.4,ease:'settle'},cfg.at);

  if(cfg.arc==='high')
    tl.to(p.dot,{motionPath:{path:[{x:dx*.42,y:dy*1.34},{x:dx,y:dy}],curviness:1.5},
      duration:cfg.flight,ease:'io'},cfg.at)
      .to(p.dot,{scale:s,duration:cfg.flight,ease:'io'},cfg.at);
  else if(cfg.arc==='flat')
    tl.to(p.dot,{x:dx,duration:cfg.flight,ease:'power2.inOut'},cfg.at)
      .to(p.dot,{y:dy,scale:s,duration:cfg.flight*.72,ease:'power3.out'},
        cfg.at+cfg.flight*.28);
  else if(cfg.arc==='lead')
    tl.to(p.dot,{y:dy*1.1,duration:cfg.flight*.3,ease:'power3.out'},cfg.at)
      .to(p.dot,{x:dx,duration:cfg.flight,ease:'power1.inOut'},cfg.at)
      .to(p.dot,{y:dy,scale:s,duration:cfg.flight*.34,ease:'settle'},
        cfg.at+cfg.flight*.66);
  else if(cfg.arc==='snap')
    tl.to(p.dot,{x:dx,y:dy,duration:cfg.flight,ease:'settle'},cfg.at)
      .to(p.dot,{scale:s,duration:.2,ease:'power2.out'},cfg.at+cfg.flight*.7)
      .fromTo(p.dot,{scaleY:s},{scaleY:s,duration:.34,ease:'elastic.out(1,.4)',
        startAt:{scaleY:s*.62,scaleX:s*1.3}},cfg.at+cfg.flight);
  else
    tl.to(p.dot,{x:dx,duration:cfg.flight,ease:'power2.inOut'},cfg.at)
      .to(p.dot,{y:dy,scale:s,duration:cfg.flight,ease:'power2.out'},cfg.at);
  return tl;
}

/* the shared prelude: one pen draws m, then b, then the dot, as a single monoline
   stroked at the letter's own stem weight. time is split by path length so the pen
   moves at a constant speed instead of every stroke taking the same slot. */
function drawIn(tl,st,c){
  var p=parts(st),ink=[p.m,p.b,p.dot],sk=[].slice.call(p.skp);
  var L=sk.map(function(el){return el.getTotalLength();});
  var tot=L.reduce(function(a,b){return a+b;},0);
  tl.set(ink,{fillOpacity:0}).set(p.sk,{opacity:1});
  var t=0;
  sk.forEach(function(el,i){
    var dur=c.d*L[i]/tot;
    tl.fromTo(el,{drawSVG:'0%'},{drawSVG:'100%',duration:dur,ease:'none'},t);
    t+=dur+c.gap;
  });
  tl.to(ink,{fillOpacity:1,duration:.26,ease:'io'},t+.04)
    .to(p.sk,{opacity:0,duration:.26,ease:'io'},t+.1);
  return t+.42;
}

var DRAWS={
  trace:  {d:1.5, gap:.05},   /* slowest pen, a clear pause between strokes */
  unpack: {d:1.1, gap:.02},
  typeset:{d:1.2, gap:.09},   /* plotter: a visible beat between every stroke */
  pivot:  {d:1.0, gap:.01},
  stamp:  {d:.55, gap:0}
};
var OPENS={
  trace:  {slide:.95,flight:.95,ease:'io',reveal:'stagger',stagger:.045,arc:'high'},
  unpack: {slide:.9, flight:.9, ease:'io',reveal:'wipe',arc:'flat'},
  typeset:{slide:1.05,flight:1.05,ease:'none',reveal:'steps',stagger:.075,arc:'linear'},
  pivot:  {slide:1.1,flight:1.1,ease:'io',reveal:'chase',arc:'lead'},
  stamp:  {slide:.55,flight:.55,ease:'settle',reveal:'pop',arc:'snap'}
};
var DRAWON=true;

function build(opt,st){
  var tl=gsap.timeline({paused:true}),cfg=Object.assign({},OPENS[opt]||OPENS.stamp);
  tl.eventCallback('onStart',function(){rest(st);});
  cfg.at=DRAWON?drawIn(tl,st,DRAWS[opt]||DRAWS.stamp):0;
  open(tl,st,cfg);
  return tl;
}

function wire(st){
  var opt=st.dataset.opt;
  if(TLS[opt])TLS[opt].kill();
  var tl=build(opt,st);TLS[opt]=tl;
  var scr=document.querySelector('.scrub[data-opt="'+opt+'"]'),
      tc=document.querySelector('.tc[data-opt="'+opt+'"]');
  tl.eventCallback('onUpdate',function(){
    if(scr)scr.value=Math.round(tl.progress()*1000);
    if(tc)tc.textContent=tl.time().toFixed(2)+'s';});
  if(scr&&!scr._w){scr._w=1;scr.addEventListener('input',function(){
    TLS[opt].pause().progress(scr.value/1000);
    tc.textContent=TLS[opt].time().toFixed(2)+'s';});}
  tl.progress(1).pause();
  return tl;
}
document.querySelectorAll('.stage').forEach(function(st){
  var opt=st.dataset.opt;
  wire(st);
  st.addEventListener('click',function(){TLS[opt].restart();});
  st.addEventListener('mouseenter',function(){
    if(!RM&&!TLS[opt].isActive())TLS[opt].restart();});
  st.addEventListener('keydown',function(e){
    if(e.key==='Enter'||e.key===' '){e.preventDefault();TLS[opt].restart();}});
});
var drawbtn=document.getElementById('draw');
drawbtn.addEventListener('click',function(){
  DRAWON=drawbtn.getAttribute('aria-pressed')!=='true';
  drawbtn.setAttribute('aria-pressed',String(DRAWON));
  document.querySelectorAll('.rp.lp[aria-pressed=true]').forEach(function(b){
    b.setAttribute('aria-pressed','false');});
  document.querySelectorAll('.stage').forEach(wire);});
document.querySelectorAll('.rp:not(.lp)').forEach(function(b){
  b.addEventListener('click',function(){TLS[b.dataset.opt].restart();});});
document.querySelectorAll('.rp.lp').forEach(function(b){
  b.addEventListener('click',function(){
    var tl=TLS[b.dataset.opt],on=b.getAttribute('aria-pressed')==='true';
    b.setAttribute('aria-pressed',String(!on));
    tl.repeat(on?0:-1).repeatDelay(on?0:.85);
    if(on)tl.progress(1).pause();else tl.restart();});});

/* nav lockup: hover expands, leaving collapses, and the dot is magnetic */
(function(){
  var nl=document.querySelector('.navlogo');
  /* the nav mark is already on screen, so it opens and collapses but never redraws */
  var was=DRAWON;DRAWON=false;var tl=build('stamp',nl);DRAWON=was;
  tl.progress(0).pause();
  var dot=nl.querySelector('.dot');
  nl.addEventListener('mouseenter',function(){if(!RM)tl.play();});
  nl.addEventListener('mouseleave',function(){if(!RM)tl.reverse();
    gsap.to(dot,{x:'-=0',duration:.3});});
  nl.addEventListener('mousemove',function(e){
    if(RM||tl.progress()>0)return;
    var r=nl.getBoundingClientRect();
    gsap.to(dot,{x:(e.clientX-r.left-r.width*.09)*.5,
      y:(e.clientY-r.top-r.height/2)*.5,duration:.5,ease:'power3.out',overwrite:'auto'});});
  nl.addEventListener('mouseleave',function(){
    if(tl.progress()===0)gsap.to(dot,{x:0,y:0,duration:.6,ease:'elastic.out(1,.5)'});});
})();

/* palette */
var body=document.body;
document.querySelectorAll('.pb').forEach(function(b){
  b.addEventListener('click',function(){
    document.querySelectorAll('.pb').forEach(function(o){
      o.setAttribute('aria-pressed',String(o===b));});
    body.dataset.pal=b.dataset.pal;
    document.querySelectorAll('.pn').forEach(function(n){
      n.classList.toggle('on',n.dataset.pal===b.dataset.pal);});});});
var slow=document.getElementById('slow');
slow.addEventListener('click',function(){
  var on=slow.getAttribute('aria-pressed')==='true';
  slow.setAttribute('aria-pressed',String(!on));
  gsap.globalTimeline.timeScale(on?1:.32);});
document.getElementById('playall').addEventListener('click',function(){
  Object.keys(TLS).forEach(function(k){TLS[k].restart();});});
"""

DOT = json.dumps({'x': DOT_X, 'y': DOT_Y, 'r': DOT_R,
                  'tx': TIT_X, 'ty': TIT_Y, 'tr': TIT_R})

SW = {'forest': ['#1b6b45', '#35d399', '#f4f3ef', '#0e0e0d'],
      'field': ['#12523a', '#d99a2b', '#f3f0e7', '#131c18'],
      'signal': ['#ff5b22', '#0d0d0e', '#f2f1ec', '#2b2b2d'],
      'bone': ['#0b0b0b', '#d8331f', '#f6f5f1', '#63625d']}
pal_cards = ''.join(
 '<div class="pal"><div class="sw">%s</div><span class="cap">%s &middot; %s</span></div>'
 % (''.join('<i style="background:%s"></i>' % c for c in SW[k]), n, tag)
 for k, n, tag, _ in PALS)

html = (
 '<title>made boring &mdash; mb. the final mark</title>\n'
 '<style>' + CSS.replace('__JOST__', JOST).replace('__PLEX__', PLEX) + '</style>\n'
 '<div class="wrap">'
 '<div class="top"><span class="lbl">made boring &middot; brand</span>'
 '<span class="lbl">mb. &rarr; madeboring &middot; five executions</span></div>'
 '<h1>The dot is the whole idea.<br><em>mb.</em> opens, and the full stop '
 'lands on the i.</h1>'
 '<p class="intro">One mark, two states. Resting, it is <b>mb.</b> &mdash; three characters, '
 'square enough for a favicon. Touched, it opens into <b>madeboring</b> and the full stop '
 'flies up to become the tittle over the <b>i</b>. Nothing is added and nothing is thrown '
 'away; the punctuation you already had turns out to have been part of the word the whole '
 'time. Below are five ways to time that, then the colour decision.</p>'

 '<div class="bar"><span class="lbl">Palette</span>' + pal_btns +
 '<span class="lbl" style="margin-left:10px">Motion</span>'
 '<button id="playall">Play all</button>'
 '<button id="draw" aria-pressed="true">Draw first</button>'
 '<button id="slow" aria-pressed="false">Slow</button></div>'

 '<h2>The mechanic<span>drawn from the real Jost outlines</span></h2>'
 '<p class="sub">Not a font setting with CSS on top. Every letter below is the actual Jost '
 '600 glyph outline pulled out of the font file, so the dot&rsquo;s flight path is measured '
 'against the real tittle rather than eyeballed. These are the numbers it travels.</p>'
 '<div class="mech">' + mech_svg() + '</div>'
 '<div class="specs">'
 '<div><dt>Dot travel, x</dt><dd>+%d</dd></div>'
 '<div><dt>Dot travel, y</dt><dd>+%d</dd></div>'
 '<div><dt>Dot radius</dt><dd>%.0f &rarr; %.0f</dd></div>'
 '<div><dt>b slides</dt><dd>+%d</dd></div>'
 '<div><dt>Units per em</dt><dd>1000</dd></div>'
 '</div>'
 % (TIT_X - DOT_X, TIT_Y - DOT_Y, DOT_R, TIT_R,
    POS['4']['x'] - MBP['1']['x']) +

 '<h2>Five executions<span>all five draw first &middot; pivot is my pick</span></h2>'
 '<p class="sub">Every one of these now opens the same way: <b>m</b> is drawn as an outline, '
 'then <b>b</b>, then the dot, and only once the mark has been built does it fill in and open '
 'into the word. What differs is the drawing speed, whether the beat is eased or mechanical, '
 'and what the letters and the dot do afterwards. Hover to play, click to replay, <b>Loop</b> '
 'to watch one on repeat, <b>Slow</b> to see what the eye is actually catching, and '
 '<b>Draw first</b> to switch the prelude off and compare against the straight open.</p>'
 + ''.join(stages) +

 '<h2>In the nav<span>where it will actually live</span></h2>'
 '<p class="sub">The real test is not the stage, it is a 26px logo in a header. Hover it: the '
 'dot is magnetic before you commit, then the word opens and collapses when you leave. The '
 'container reserves the full width so nothing else on the bar moves.</p>'
 '<div class="nav"><div class="navlogo" data-opt="nav">' + word_svg(VB) + '</div>'
 '<div class="links"><a href="#opt-trace">Work</a><a href="#opt-pivot">Method</a>'
 '<a href="#opt-stamp">Pricing</a></div>'
 '<a class="cta" href="#opt-trace">Book a call</a></div>'

 '<h2>At favicon size<span>the honest test</span></h2>'
 '<p class="sub">The resting mark is wide &mdash; roughly two to one &mdash; so in a square '
 'favicon it sits as a band rather than filling the tile. This is the truth at every size, '
 'including a real browser tab. If 16px is not good enough, the fix is a tighter lockup, not '
 'a different idea.</p>'
 '<div class="fav">'
 + ''.join('<div class="fv f%d"><div class="box">%s</div><span>%d px</span></div>'
           % (s, mb_svg(), s) for s in (16, 32, 48, 64))
 + '<div class="fv f96"><div class="box solid">' + mb_svg()
 + '</div><span>app</span></div></div>'
 '<div class="tabsim"><div class="box">' + mb_svg() + '</div>'
 '<b>made boring &mdash; we make it boring</b></div>'

 '<h2>The colour<span>pick one, the page changes</span></h2>'
 '<p class="sub">Use the palette buttons at the top &mdash; every mark, stage, button and '
 'ground on this page repaints, so you are judging real UI rather than four swatches. '
 '<b>Field is my recommendation</b> and the page is loaded in it.</p>'
 '<div class="pals">' + pal_cards + '</div>'
 + pal_notes +

 '<div class="note"><b>Why Field, in one paragraph</b>'
 '<p>The name is a joke about restraint, so the palette should not be shouting. But the live '
 'site is currently so quiet it reads as a document rather than a product &mdash; that is the '
 '<em>real</em> problem, and it is a contrast and type-size problem more than a hue problem. '
 'Field fixes it without volume: it takes the green you already own and makes it the ground '
 'instead of the trim, which reads as confident rather than loud. Amber appears only on things '
 'you can click, so the one warm colour on the page always means the same thing.</p>'
 '<p><em>Signal is the risk.</em> Orange on near-black over a dev-adjacent site is Replit&rsquo;s '
 'signature, and the engineers you are selling to will place it instantly. Borrow '
 'Replit&rsquo;s <em>type scale and density</em> &mdash; that is what actually makes their site '
 'feel expensive &mdash; not their hue.</p></div>'

 '<div class="note"><b>What happens after you pick</b>'
 '<p>Say a number and a palette and I cut the mark to <em>app/icon.svg</em>, a light and dark '
 'wordmark, the OG image, and wire the nav component with the collapse on scroll. The site '
 'rebuild &mdash; type scale, hero, WebGL, the lot &mdash; starts from there.</p></div>'

 '<div class="foot"><span class="lbl">Nothing here is live on madeboring.com yet</span>'
 '<span class="lbl">Zero credits spent &middot; all of this is code</span></div></div>'
 '<script>' + GSAP + '</script>\n'
 '<script>' + JS.replace('__DOT__', DOT) + '</script>'
)
html = html.encode('ascii', 'xmlcharrefreplace').decode()
pathlib.Path('logo.html').write_text(html)
print('written', round(len(html) / 1024, 1), 'KB &middot;', len(OPTS), 'executions')
