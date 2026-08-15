import base64, pathlib, math

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
                                 'DrawSVGPlugin.min.js', 'MorphSVGPlugin.min.js'])

N = {'n': 0}


def uid():
    N['n'] += 1
    return 'g%d' % N['n']


def teeth():
    out = []
    for i in range(10):
        a = math.radians(i * 36)
        x, y = 50 + 45.5 * math.cos(a), 50 + 45.5 * math.sin(a)
        out.append('<rect class="tooth" x="%.2f" y="%.2f" width="7" height="7" '
                   'transform="rotate(%.1f %.2f %.2f)"/>' % (x - 3.5, y - 3.5,
                                                             i * 36, x, y))
    return ''.join(out)


def ring(opt, static):
    u = uid()
    base = ('<circle class="trk" cx="50" cy="50" r="37" fill="none" '
            'stroke-width="14"/>')
    if opt == 'oring':
        b = ('<rect class="pl pt" x="-14" y="%s" width="128" height="8"/>'
             '<rect class="pl pb" x="-14" y="%s" width="128" height="8"/>'
             % ('-2' if static else '-40', '94' if static else '132')) + base + \
            ('<path class="gloss" d="M28 32A26 26 0 0 1 62 25" fill="none" '
             'stroke-width="5" stroke-linecap="round" opacity=".55"/>')
    elif opt == 'converge':
        b = base
    elif opt == 'exploded':
        b = ('<g class="lay l1"><circle cx="50" cy="50" r="37" fill="none" '
             'stroke-width="14" opacity=".28"/></g>'
             '<g class="lay l2"><circle cx="50" cy="50" r="37" fill="none" '
             'stroke-width="14" opacity=".55"/></g>'
             '<g class="lay l3">' + base + '</g>'
             '<g class="dim" opacity="%s"><path d="M50 -8h0M6 -8H94" '
             'stroke-width="1.4" fill="none"/><path d="M6 -12v8M94 -12v8" '
             'stroke-width="1.4"/></g>' % ('1' if static else '0'))
    elif opt == 'ripple':
        b = ''.join('<circle class="rp r%d" cx="50" cy="50" r="37" fill="none" '
                    'stroke-width="6" opacity="0"/>' % i for i in range(3)) + base
    elif opt == 'growth':
        b = (''.join('<circle class="gr" cx="50" cy="50" r="%d" fill="none" '
                     'stroke-width="3" opacity=".3"/>' % r for r in (11, 19, 27))
             + base)
    elif opt == 'bore':
        b = ('<g class="cut" opacity="%s">%s<circle cx="50" cy="50" r="45.5" '
             'fill="none" stroke-width="2" stroke-dasharray="4 4"/></g>'
             % ('0' if not static else '0', teeth())) + base
    elif opt == 'signet':
        b = ('<g class="imp" opacity="0"><circle cx="50" cy="50" r="37" '
             'fill="none" stroke-width="15" stroke-dasharray="3 5" '
             'opacity=".45"/></g>') + base
    else:
        b = ('<defs><radialGradient id="%s" cx="34%%" cy="26%%" r="78%%">'
             '<stop offset="0" class="gs0"/><stop offset=".52" class="gs1"/>'
             '<stop offset="1" class="gs2"/></radialGradient></defs>'
             '<circle class="tor" cx="50" cy="50" r="37" fill="none" '
             'stroke-width="14" stroke="url(#%s)"/>'
             '<path class="hl" d="M25 34A28 28 0 0 1 58 22" fill="none" '
             'stroke-width="4.5" stroke-linecap="round" opacity=".7"/>' % (u, u))
    return ('<svg class="rg rg-%s" viewBox="0 0 100 100" aria-hidden="true">%s</svg>'
            % (opt, b))


def wordmark(opt, static=False):
    pre = ''.join('<span class="ch">%s</span>' % c for c in 'madeb')
    rng = ''.join('<span class="ch">%s</span>' % c for c in 'ring')
    return ('<div class="wm"><span class="pre">%s</span>'
            '<span class="oring"><span class="oslot">%s</span>'
            '<span class="rng">%s</span></span>'
            '<span class="tld"><span class="ch">.</span><span class="ch">c</span>'
            '<span class="ch">o</span><span class="ch">m</span></span></div>'
            % (pre, ring(opt, static), rng))


OPTS = [
 ('oring', 'O-Ring', 'the seal', 'SVG mask &middot; compression',
  'The mark is an actual O-ring, and the animation is what an O-ring does for a '
  'living: two faces close on it, it takes the squeeze, and the joint is sealed. '
  'The plates retract and the ring stays &mdash; still holding.',
  'The most complete idea on this page. The mark is a real object with a real name '
  'that is already inside your domain, and its entire job is to be the unremarkable '
  'part that stops everything else leaking. That is the company.'),
 ('converge', 'Converge', 'the assembly', 'opposed travel &middot; magnetic settle',
  'Your idea, executed literally: the circle comes in from one side, the letters '
  'r-i-n-g come in from the other, and they snap together into one word. Then '
  'madeb slides in front and the reading flips from &ldquo;O-ring&rdquo; to '
  '&ldquo;madeboring&rdquo; in a single beat.',
  'This is the only one that shows the audience the pun instead of hoping they '
  'find it. Whether that is a strength depends on whether you want the joke '
  'explained every single time it plays.'),
 ('exploded', 'Exploded', 'the drawing', 'staged convergence &middot; dimension lines',
  'A technical drawing that assembles itself. Three ring sections stand apart in '
  'section view, slide together into one solid part, and the dimension line and '
  'callout snap in underneath as if the part had just been specified.',
  'The closest to the voice you already write in &mdash; the spec sheet, the '
  'part number, the tolerance. It extends the site instead of decorating it.'),
 ('ripple', 'Ripple', 'the signal', 'staggered propagation',
  'Ring in the other sense. A tap at the centre and the signal goes out in rings, '
  'each one weaker than the last, until the outermost stops expanding and becomes '
  'the letter.',
  'Reads as monitoring, uptime, a heartbeat, a system answering &mdash; the '
  'infrastructure meaning rather than the hardware one. Least dependent on anyone '
  'getting the wordplay.'),
 ('growth', 'Growth', 'the record', 'DrawSVG &middot; inside-out accretion',
  'Tree rings. The mark builds from the centre outward, one ring at a time, each '
  'drawn rather than faded, until the outer ring closes and holds.',
  'The only option that says <em>time</em>. Boring compounding, one unremarkable '
  'year at a time. Strong for a company that intends to still be here in ten '
  'years and weak for one that needs to look new.'),
 ('bore', 'Bore', 'the verb', 'rotational cut &middot; mask reveal',
  'Boring as the thing machinists do. A toothed cutter drops onto the face, spins '
  'up, drives through, and lifts away leaving a hole with a perfect edge.',
  'Owns the other meaning of the word, which nobody else in your category can '
  'claim. Boring is not an apology here, it is the operation being performed.'),
 ('signet', 'Signet', 'the guarantee', 'squash and release &middot; impression',
  'A signet ring comes down, presses, and lifts &mdash; leaving an impression '
  'behind it that settles into the mark. Something has been stamped and it is '
  'now binding.',
  'This is the one that carries the 110% promise. A seal is the visual language '
  'of a guarantee, and you are the only agency in the market making one.'),
 ('torus', 'Torus', 'the object', 'radial shading &middot; specular travel',
  'The same O-ring, but rendered as a physical object rather than a diagram &mdash; '
  'shaded, dimensional, with a highlight that travels the surface as it turns.',
  'The premium option and the only dimensional one. It will look expensive on a '
  'dark landing page and it is the first thing that will break when someone has '
  'to reproduce it in one colour on an invoice.'),
]

cards = []
for i, (opt, name, kicker, tech, story, take) in enumerate(OPTS):
    cards.append(f'''
<section class="card">
  <div class="chead"><div><span class="num">{i+1:02d}</span><h2>{name}</h2>
    <span class="kick">{kicker}</span><span class="tech">{tech}</span></div></div>
  <p class="story">{story}</p>
  <div class="stage" data-opt="{opt}">{wordmark(opt)}</div>
  <div class="ctrl"><button class="rp" data-opt="{opt}">Replay</button>
    <input class="scrub" type="range" min="0" max="1000" value="1000" data-opt="{opt}"
      aria-label="Scrub {name}"><span class="tc" data-opt="{opt}">0.00s</span></div>
  <div class="assets">
    <div class="ab"><div class="tabs">
      <div class="tab on">{ring(opt, True)}<span>madeboring.com</span></div>
      <div class="tab"><i class="ph"></i><span>Gmail</span></div></div>
      <div class="tabb"></div><span class="cap">favicon, 16px</span></div>
    <div class="ab szrow">
      <div class="sz"><div class="sb s16">{ring(opt, True)}</div><span>16</span></div>
      <div class="sz"><div class="sb s32">{ring(opt, True)}</div><span>32</span></div>
      <div class="sz"><div class="sb s64">{ring(opt, True)}</div><span>64</span></div>
      <div class="sz"><div class="tile">{ring(opt, True)}</div><span>app</span></div>
      <div class="sz"><div class="tile solid">{ring(opt, True)}</div><span>1&nbsp;colour</span></div>
    </div>
    <div class="ab"><div class="lock">{wordmark(opt, True)}</div>
      <div class="lock ink">{wordmark(opt, True)}</div>
      <span class="cap">lockup, both grounds</span></div>
  </div>
  <p class="craft"><span>Read on this one</span>{take}</p>
</section>''')

CSS = """
@font-face{font-family:Jost;src:url(data:font/woff2;base64,__JOST__) format('woff2');
 font-weight:100 900;font-style:normal;font-display:block}
@font-face{font-family:PlexMono;src:url(data:font/woff2;base64,__PLEX__) format('woff2');
 font-weight:400;font-style:normal;font-display:block}
:root{--paper:#f4f3ef;--surf:#eceae4;--ink:#0e0e0d;--line:#d5d3cc;--line2:#e4e2db;
 --muted:#6e6d66;--mk:#1b6b45;--tx:#0e0e0d;--green:#1b6b45;--mint:#35d399;
 --swl:#eceae4;--swd:#0e0e0d;--mono:PlexMono,ui-monospace,Menlo,monospace;
 --disp:Jost,system-ui,sans-serif;--body:system-ui,-apple-system,"Segoe UI",sans-serif}
@media(prefers-color-scheme:dark){:root:not([data-theme=light]){--paper:#0e0e0d;
 --surf:#171715;--ink:#f2f1ec;--line:#2c2c28;--line2:#232320;--muted:#95948c;
 --mk:#35d399;--tx:#f2f1ec;--green:#35d399}}
:root[data-theme=dark]{--paper:#0e0e0d;--surf:#171715;--ink:#f2f1ec;--line:#2c2c28;
 --line2:#232320;--muted:#95948c;--mk:#35d399;--tx:#f2f1ec;--green:#35d399}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--paper);color:var(--ink);font-family:var(--body);font-size:16px;
 line-height:1.6;-webkit-font-smoothing:antialiased}
.wrap{max-width:1000px;margin:0 auto;padding:clamp(22px,5vw,52px) clamp(16px,4vw,36px) 100px}
.lbl,.cap,.tech,.num,.tc,.sz span,.kick{font-family:var(--mono);letter-spacing:.13em;
 text-transform:uppercase}
.top{display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap;
 border-bottom:2px solid var(--ink);padding-bottom:11px}
.lbl{font-size:10px;color:var(--muted)}
h1{font-family:var(--disp);font-weight:700;font-size:clamp(30px,5.6vw,58px);line-height:.99;
 letter-spacing:-.035em;margin-top:26px;text-wrap:balance}
h1 em{font-style:normal;color:var(--mk)}
.intro{max-width:63ch;margin-top:16px;color:var(--muted);font-size:16px}
.intro b{color:var(--ink);font-weight:600}
.reveal{margin-top:28px;border:1px solid var(--line);background:var(--surf);
 padding:clamp(22px,4vw,40px) 18px 20px;text-align:center;--mk:var(--green);--tx:#0e0e0d}
.reveal .wm{justify-content:center;font-size:clamp(30px,6.4vw,64px)}
.reveal .pre,.reveal .tld{opacity:.34}
.brk{margin:6px auto 0;width:min(320px,54%);border-top:2px solid var(--green);
 border-left:2px solid var(--green);border-right:2px solid var(--green);height:11px}
.brklbl{font-family:var(--mono);font-size:10px;letter-spacing:.2em;text-transform:uppercase;
 color:var(--green);margin-top:8px}
.revtxt{max-width:56ch;margin:14px auto 0;font-size:14.5px;color:#4a4a45;line-height:1.6}
.bar{position:sticky;top:0;z-index:20;display:flex;gap:8px;align-items:center;flex-wrap:wrap;
 background:var(--paper);border-bottom:1px solid var(--line);padding:11px 0;margin-top:32px}
.bar button{font-family:var(--mono);font-size:10px;letter-spacing:.11em;text-transform:uppercase;
 border:1px solid var(--line);background:transparent;color:var(--ink);padding:6px 10px;cursor:pointer}
.bar button[aria-pressed=true]{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.bar button:hover{border-color:var(--ink)}
.bar button:focus-visible,.rp:focus-visible,.scrub:focus-visible{outline:2px solid var(--mk);
 outline-offset:2px}
.card{margin-top:52px;border-top:2px solid var(--ink);padding-top:15px}
.chead>div{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
.num{font-size:11px;color:var(--muted)}
.card h2{font-family:var(--disp);font-size:29px;font-weight:600;letter-spacing:-.03em}
.kick{font-size:9.5px;color:var(--muted)}
.tech{font-size:9.5px;color:var(--mk);border:1px solid var(--mk);padding:3px 7px}
.story{max-width:68ch;margin-top:10px;font-size:15px;line-height:1.62;color:var(--muted)}
.craft{margin-top:15px;font-size:14.5px;line-height:1.58;color:var(--muted);padding-left:13px;
 border-left:2px solid var(--mk);max-width:70ch}
.craft span{display:block;font-family:var(--mono);font-size:9.5px;letter-spacing:.13em;
 text-transform:uppercase;color:var(--mk);margin-bottom:2px}
.craft em{font-style:italic;color:var(--ink)}
.stage{margin-top:14px;background:var(--swl);border:1px solid var(--line2);height:222px;
 display:grid;place-items:center;overflow:hidden;--mk:var(--green);--tx:#0e0e0d}
.stage.ink{background:var(--swd);border-color:#000;--mk:var(--mint);--tx:#f4f3ef}
.wm{display:flex;align-items:baseline;font-family:var(--disp);font-weight:600;
 font-size:clamp(26px,5.4vw,54px);letter-spacing:-.028em;color:var(--tx);white-space:nowrap}
.wm .ch{display:inline-block}
.pre,.rng{display:inline-flex}
.oring{display:inline-flex;align-items:baseline}
.wm .tld{display:inline-flex;color:var(--muted);font-weight:400}
.stage.ink .wm .tld,.lock.ink .wm .tld{color:#8a8981}
.oslot{display:inline-block;position:relative;width:.598em;height:.598em;
 margin:0 -.017em;align-self:baseline;top:.0665em}
.oslot .rg{position:absolute;inset:0;width:100%;height:100%;overflow:visible}
.rg .trk,.rg .rp,.rg .gr,.rg .gloss,.rg .hl,.rg .imp circle,.rg .cut circle{stroke:var(--mk)}
.rg .lay circle{stroke:var(--mk);fill:none}
.rg .dim path{stroke:var(--mk)}
.rg .pl,.rg .tooth{fill:var(--mk)}
.rg .hl{stroke:#fff}
.rg .gs0{stop-color:#7ff0c0}.rg .gs1{stop-color:var(--mk)}.rg .gs2{stop-color:#06301d}
.ctrl{display:flex;align-items:center;gap:11px;border:1px solid var(--line2);border-top:0;
 padding:9px 12px}
.rp{font-family:var(--mono);font-size:10px;letter-spacing:.11em;text-transform:uppercase;
 border:1px solid var(--line);background:transparent;color:var(--ink);padding:6px 11px;cursor:pointer}
.rp:hover{border-color:var(--ink)}
.scrub{flex:1;accent-color:var(--mk);height:3px;cursor:pointer}
.tc{font-size:10px;color:var(--muted);min-width:48px;text-align:right;
 font-variant-numeric:tabular-nums}
.assets{display:grid;grid-template-columns:1fr 1fr;gap:13px;margin-top:13px}
@media(max-width:820px){.assets{grid-template-columns:1fr}}
.ab{border:1px solid var(--line2);padding:13px}
.ab.szrow{display:flex;gap:14px;align-items:flex-end;justify-content:center;flex-wrap:wrap}
.assets .ab:last-child{grid-column:1/-1}
.cap{display:block;font-size:9px;color:var(--muted);margin-top:11px}
.tabs{display:flex;gap:4px;align-items:flex-end}
.tab{display:flex;align-items:center;gap:7px;background:var(--surf);border:1px solid var(--line2);
 border-bottom:0;border-radius:7px 7px 0 0;padding:6px 11px;font-size:11.5px;color:var(--muted);
 white-space:nowrap;font-family:var(--body)}
.tab.on{background:var(--paper);color:var(--ink);font-weight:500}
.tab .rg,.tab .ph{width:15px;height:15px;flex:0 0 15px}
.tab .ph{background:var(--line);border-radius:3px}
.tabb{height:22px;background:var(--paper);border:1px solid var(--line2);border-radius:0 5px 0 0}
.sz{display:flex;flex-direction:column;align-items:center;gap:6px}
.sz span{font-size:9px;color:var(--muted)}
.sb .rg,.tile .rg{width:100%;height:100%;position:static}
.s16{width:16px;height:16px}.s32{width:32px;height:32px}.s64{width:64px;height:64px}
.tile{width:58px;height:58px;border-radius:13px;background:var(--ink);padding:13px;
 display:grid;place-items:center;--mk:var(--mint)}
.tile.solid{background:var(--green);--mk:#f4f3ef}
.tile.solid .rg .gs0,.tile.solid .rg .gs1,.tile.solid .rg .gs2{stop-color:#f4f3ef}
.lock{padding:16px 14px;background:var(--surf);border:1px solid var(--line2);
 display:grid;place-items:center;--mk:var(--green);--tx:#0e0e0d}
.lock+.lock{margin-top:8px}
.lock.ink{background:var(--swd);border-color:#000;--mk:var(--mint);--tx:#f4f3ef}
.lock .wm{font-size:clamp(20px,3.4vw,30px)}
.note{margin-top:46px;border:1px solid var(--line);padding:16px 18px;max-width:74ch}
.note b{font-family:var(--mono);font-size:10px;letter-spacing:.13em;text-transform:uppercase;
 color:var(--mk);display:block;margin-bottom:5px}
.note p{font-size:14.5px;color:var(--muted);line-height:1.6}
.foot{margin-top:52px;border-top:2px solid var(--ink);padding-top:14px;display:flex;
 justify-content:space-between;gap:12px;flex-wrap:wrap}
"""

JSCODE = r"""
gsap.registerPlugin(CustomEase,DrawSVGPlugin,MorphSVGPlugin);
CustomEase.create('io','M0,0 C0.16,0.02 0.06,1 1,1');
CustomEase.create('settle','M0,0 C0.2,0 0.13,1.06 1,1');
CustomEase.create('heavy','M0,0 C0.62,0 0.1,1 1,1');
var RM=window.matchMedia('(prefers-reduced-motion: reduce)').matches,TLS={};

function build(opt){
  var st=document.querySelector('.stage[data-opt="'+opt+'"]');
  var chs=st.querySelectorAll('.ch'),slot=st.querySelector('.oslot'),
      pre=st.querySelector('.pre'),rng=st.querySelector('.rng'),
      tld=st.querySelector('.tld'),wm=st.querySelector('.wm'),
      q=function(s){return st.querySelector(s);},
      qa=function(s){return st.querySelectorAll(s);};
  var tl=gsap.timeline({paused:true});
  gsap.set(chs,{opacity:0});

  if(opt==='oring'){
    tl.fromTo(slot,{scale:2.2},{scale:1,duration:1.5,ease:'settle'},0)
      .fromTo(q('.pt'),{attr:{y:-40}},{attr:{y:-2},duration:.7,ease:'heavy'},.15)
      .fromTo(q('.pb'),{attr:{y:132}},{attr:{y:94},duration:.7,ease:'heavy'},.15)
      .fromTo(q('.trk'),{scaleY:1,transformOrigin:'50px 50px'},
        {scaleY:.8,duration:.16,ease:'power2.in'},.85)
      .to(q('.trk'),{scaleY:1,duration:.9,ease:'elastic.out(1,0.45)'},1.01)
      .fromTo(q('.gloss'),{opacity:0},{opacity:.55,duration:.5},1.1)
      .to(q('.pt'),{attr:{y:-46},duration:.75,ease:'io'},1.15)
      .to(q('.pb'),{attr:{y:138},duration:.75,ease:'io'},1.15)
      .to(chs,{opacity:1,duration:.45,stagger:{each:.026,from:'center'},
        ease:'power2.out'},1.2);
  }
  else if(opt==='converge'){
    tl.fromTo(slot,{x:-210,rotate:-90},{x:0,rotate:0,duration:1.25,ease:'settle'},0)
      .fromTo(rng,{x:230},{x:0,duration:1.25,ease:'settle'},0)
      .to(rng.querySelectorAll('.ch'),{opacity:1,duration:.35,stagger:.04},.15)
      .fromTo(pre,{x:-150,opacity:0},{x:0,opacity:1,duration:.85,ease:'io'},1.15)
      .to(pre.querySelectorAll('.ch'),{opacity:1,duration:.4,stagger:.035},1.15)
      .to(tld.querySelectorAll('.ch'),{opacity:1,duration:.4,stagger:.03},1.6);
  }
  else if(opt==='exploded'){
    tl.fromTo(q('.l1'),{y:-46,transformOrigin:'50px 50px'},
        {y:0,duration:1.2,ease:'settle'},0)
      .fromTo(q('.l2'),{y:-23},{y:0,duration:1.2,ease:'settle'},.1)
      .fromTo(q('.l3'),{y:34},{y:0,duration:1.2,ease:'settle'},.2)
      .fromTo(slot,{scale:1.75},{scale:1,duration:1.5,ease:'settle'},0)
      .fromTo(q('.dim'),{opacity:0,scaleX:.3,transformOrigin:'50px 50px'},
        {opacity:1,scaleX:1,duration:.6,ease:'io'},1.25)
      .to(chs,{opacity:1,duration:.42,stagger:{each:.028,from:'center'},
        ease:'power2.out'},1.05);
  }
  else if(opt==='ripple'){
    tl.fromTo(qa('.rp'),{scale:.12,opacity:.85,transformOrigin:'50px 50px'},
        {scale:2.5,opacity:0,duration:1.5,ease:'power2.out',stagger:.19},0)
      .fromTo(q('.trk'),{scale:.12,opacity:0,transformOrigin:'50px 50px'},
        {scale:1,opacity:1,duration:1.25,ease:'settle'},.42)
      .fromTo(slot,{scale:1.5},{scale:1,duration:1.4,ease:'settle'},.42)
      .to(chs,{opacity:1,duration:.45,stagger:{each:.028,from:'center'},
        ease:'power2.out'},1.15);
  }
  else if(opt==='growth'){
    var gr=qa('.gr');
    tl.fromTo(gr,{drawSVG:'50% 50%',opacity:0},
        {drawSVG:'0% 100%',opacity:.3,duration:.62,ease:'io',stagger:.19},0)
      .fromTo(q('.trk'),{drawSVG:'50% 50%'},
        {drawSVG:'0% 100%',duration:.85,ease:'io'},.62)
      .fromTo(slot,{scale:1.45},{scale:1,duration:1.5,ease:'settle'},0)
      .to(chs,{opacity:1,duration:.45,stagger:{each:.03,from:'center'},
        ease:'power2.out'},1.25);
  }
  else if(opt==='bore'){
    tl.fromTo(q('.cut'),{opacity:0,scale:2.3,rotate:0,transformOrigin:'50px 50px'},
        {opacity:1,scale:1,duration:.75,ease:'heavy'},0)
      .to(q('.cut'),{rotate:640,duration:1.7,ease:'io'},0)
      .fromTo(q('.trk'),{drawSVG:'0% 0%'},{drawSVG:'0% 100%',duration:1.15,
        ease:'io'},.5)
      .to(q('.cut'),{opacity:0,scale:.55,duration:.55,ease:'power2.in'},1.35)
      .fromTo(slot,{scale:1.9},{scale:1,duration:1.7,ease:'settle'},0)
      .to(chs,{opacity:1,duration:.45,stagger:{each:.028,from:'center'},
        ease:'power2.out'},1.2);
  }
  else if(opt==='signet'){
    tl.fromTo(slot,{scale:3.1,y:-38,rotate:-14},{scale:1.12,y:0,rotate:0,
        duration:.85,ease:'heavy'},0)
      .to(q('.trk'),{scaleY:.84,scaleX:1.06,transformOrigin:'50px 50px',
        duration:.14,ease:'power2.in'},.85)
      .to(q('.trk'),{scaleY:1,scaleX:1,duration:.85,
        ease:'elastic.out(1,0.5)'},.99)
      .to(slot,{scale:1,duration:.95,ease:'settle'},.99)
      .fromTo(q('.imp'),{opacity:0,scale:1},{opacity:1,duration:.12},.92)
      .to(q('.imp'),{opacity:0,scale:1.5,transformOrigin:'50px 50px',
        duration:.9,ease:'power2.out'},1.04)
      .to(chs,{opacity:1,duration:.45,stagger:{each:.028,from:'center'},
        ease:'power2.out'},1.02);
  }
  else{
    gsap.set(q('.rg'),{transformPerspective:460});
    tl.fromTo(q('.tor'),{rotateY:-250,transformOrigin:'50px 50px'},
        {rotateY:0,duration:1.85,ease:'io'},0)
      .fromTo(slot,{scale:1.6},{scale:1,duration:1.6,ease:'settle'},0)
      .fromTo(q('.hl'),{opacity:0,rotate:-120,transformOrigin:'50px 50px'},
        {opacity:.7,rotate:0,duration:1.3,ease:'io'},.5)
      .fromTo(chs,{filter:'blur(8px)'},{filter:'blur(0px)',opacity:1,duration:.8,
        ease:'io',stagger:{each:.028,from:'center'}},1.05);
  }

  TLS[opt]=tl;
  var scr=document.querySelector('.scrub[data-opt="'+opt+'"]'),
      tc=document.querySelector('.tc[data-opt="'+opt+'"]');
  tl.eventCallback('onUpdate',function(){scr.value=Math.round(tl.progress()*1000);
    tc.textContent=tl.time().toFixed(2)+'s';});
  scr.addEventListener('input',function(){tl.pause().progress(scr.value/1000);
    tc.textContent=tl.time().toFixed(2)+'s';});
}
['oring','converge','exploded','ripple','growth','bore','signet','torus'].forEach(build);

function play(o){if(TLS[o])TLS[o].restart();}
document.querySelectorAll('.rp').forEach(function(b){
  b.addEventListener('click',function(){play(b.dataset.opt);});});
document.getElementById('playall').addEventListener('click',function(){
  Object.keys(TLS).forEach(play);});
var gnd=document.getElementById('gnd');
gnd.addEventListener('click',function(){
  var on=gnd.getAttribute('aria-pressed')==='true';
  gnd.setAttribute('aria-pressed',String(!on));
  document.querySelectorAll('.stage').forEach(function(s){s.classList.toggle('ink',!on);});});
var slow=document.getElementById('slow');
slow.addEventListener('click',function(){
  var on=slow.getAttribute('aria-pressed')==='true';
  slow.setAttribute('aria-pressed',String(!on));
  gsap.globalTimeline.timeScale(on?1:.35);});

Object.keys(TLS).forEach(function(k){TLS[k].progress(1).pause();});
if(!RM){
  var io=new IntersectionObserver(function(es){es.forEach(function(e){
    if(e.isIntersecting&&!e.target._s){e.target._s=1;play(e.target.dataset.opt);}});},
    {threshold:.45});
  document.querySelectorAll('.stage').forEach(function(s){io.observe(s);});
}
"""

hero = ('<div class="reveal">' + wordmark('oring', True) +
        '<div class="brk"></div><div class="brklbl">O-ring</div>'
        '<p class="revtxt">An O-ring is a plain rubber circle that costs a few '
        'rupees and does exactly one job: sit in a groove and stop things leaking. '
        'Nobody photographs one. Nobody has ever been excited about one. Every '
        'engine, pump, tap and spacecraft has them, and you only ever learn the '
        'name when one fails.</p></div>')

html = (
 '<title>made boring &mdash; O-ring, eight executions</title>\n'
 '<style>' + CSS.replace('__JOST__', JOST).replace('__PLEX__', PLEX) + '</style>\n'
 '<div class="wrap">'
 '<div class="top"><span class="lbl">made boring &middot; brand</span>'
 '<span class="lbl">round five &middot; the o-ring</span></div>'
 '<h1>The word was already<br>in the name. <em>O&#8209;ring.</em></h1>'
 '<p class="intro">You spotted it: the circle and the letters <b>r-i-n-g</b> come '
 'together. They already do &mdash; madeb<b>oring</b>.com has <b>O&#8209;ring</b> '
 'sitting inside it, and an O-ring is the single most boring object in engineering. '
 'That gives the mark something almost no logo gets: <b>a real name, a real job, and '
 'a reason to be a circle</b>. Eight executions below &mdash; four that take the '
 'O-ring literally, four that take the other meanings of <b>ring</b>: a signal, a '
 'record of years, a cut, a seal.</p>'
 + hero +
 '<div class="bar"><span class="lbl">Controls</span>'
 '<button id="playall">Play all</button>'
 '<button id="gnd" aria-pressed="false">Ground: ink</button>'
 '<button id="slow" aria-pressed="false">0.35&times; speed</button></div>'
 + ''.join(cards) +
 '<div class="note"><b>One thing you should decide with your eyes open</b>'
 '<p>The most famous O-ring in history is the one that failed on Challenger in 1986. '
 'It is not the first association for most people &mdash; the word mainly reads as '
 'plumbing &mdash; but it is a real association, and it attaches to a seal failing '
 'rather than holding. Worth knowing before you put it on the door, not after.</p>'
 '</div>'
 '<div class="foot"><span class="lbl">Nothing here is live on madeboring.com yet</span>'
 '<span class="lbl">Name one and it ships</span></div></div>'
 '<script>' + GSAP + '</script>\n<script>' + JSCODE + '</script>'
)
html = html.encode('ascii', 'xmlcharrefreplace').decode()
pathlib.Path('oring.html').write_text(html)
print('written', round(len(html) / 1024, 1), 'KB')
