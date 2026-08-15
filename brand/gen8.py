import base64, pathlib

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
                                 'DrawSVGPlugin.min.js', 'TextPlugin.min.js'])

SEAL_SVG = ('<svg class="sealring" viewBox="0 0 100 100" aria-hidden="true">'
            '<circle class="sr" cx="50" cy="50" r="44" fill="none" '
            'stroke-width="7"/></svg>')


def mark(opt):
    if opt == 'expand':
        return '<span class="mk">mb</span>'
    if opt == 'ligature':
        return '<span class="mk lig"><i class="lm">M</i><i class="lb">B</i></span>'
    if opt == 'stack':
        return '<span class="mk stk"><i class="sm">M</i><i class="sb">B</i></span>'
    if opt == 'slash':
        return ('<span class="mk sl"><i class="a">m</i><i class="sls">/</i>'
                '<i class="b">b</i></span>')
    if opt == 'seal':
        return '<span class="mk seal">' + SEAL_SVG + '<i>MB</i></span>'
    if opt == 'tile':
        return '<span class="mk tl">MB</span>'
    if opt == 'byte':
        return '<span class="mk chip">MB</span>'
    return '<span class="mk term">mb<i class="cur"></i></span>'


def stage(opt):
    if opt == 'expand':
        return ('<div class="xp"><span class="w"><span class="k">m</span>'
                '<span class="rest">ade</span></span><span class="w w2">'
                '<span class="k">b</span><span class="rest">oring</span></span></div>')
    if opt == 'ligature':
        return ('<div class="big">' + mark('ligature') + '</div>')
    if opt == 'stack':
        return ('<div class="big">' + mark('stack') + '</div>')
    if opt == 'slash':
        return ('<div class="big">' + mark('slash') + '</div>')
    if opt == 'seal':
        return ('<div class="big"><span class="mk seal">' + SEAL_SVG +
                '<i>MB</i></span></div>')
    if opt == 'tile':
        return ('<div class="big"><span class="mk tl"><i class="tm">M</i>'
                '<i class="tb">B</i></span></div>')
    if opt == 'byte':
        return ('<div class="big"><span class="mk chip chipa">'
                '<span class="lay">MB</span>'
                '<span class="fillwrap"><span class="lay inv">MB</span></span>'
                '</span></div>')
    return ('<div class="big"><span class="mk term"><span class="pr">$</span>'
            '<span class="cmd">mb</span><i class="cur"></i></span>'
            '<div class="out">made boring</div></div>')


OPTS = [
 ('expand', 'Expand', 'm becomes made, b becomes boring',
  'truth-preserving compression',
  'The monogram is not an abbreviation of the name, it <b>is</b> the name with the '
  'middle removed. On play the <b>m</b> and the <b>b</b> stay exactly where they are '
  'and the rest of each word grows out of them. Nothing moves that should not move, '
  'because the two letters really are the first letters of the two words.',
  'The strongest concept here and the one that justifies a monogram at all. '
  'Most MB marks are a shorthand somebody agreed to; this one is provably the same '
  'object as the full name, and the animation is the proof. Use it as the loading '
  'state and the name assembles itself every time the app opens.'),
 ('ligature', 'Ligature', 'one stem, shared',
  'measured overlap &middot; merge',
  'The M and the B are set so they share a single vertical stem &mdash; one stroke '
  'doing two jobs. The overlap is not eyeballed: it is computed at runtime from the '
  'measured stem width and both side bearings, so the join is exact at any size.',
  'The most typographically serious option and the best one to put on a business '
  'card. It also performs the thesis without saying anything: two things merged '
  'until they are simpler than they were apart.'),
 ('stack', 'Stack', 'M over B',
  'vertical close &middot; tight leading',
  'The two letters stacked rather than set side by side, with the leading pulled in '
  'until they read as one block. On play they arrive from above and below and the '
  'gap closes to nothing.',
  'The only option with a square silhouette rather than a wide one, which means it '
  'fills an avatar crop instead of floating in the middle of it. Reads as a '
  'publisher&rsquo;s colophon &mdash; serious, quiet, a little institutional.'),
 ('slash', 'Slash', 'm/b',
  'device carries the brand',
  'A slash between the letters, in the accent colour, doing all the work. On play it '
  'sweeps down and pushes the two letters apart into their final positions.',
  'This is the Wellfound move applied to your name: they have no icon at all, just a '
  'wordmark and a coloured colon, and that colon is the entire brand. A slash also '
  'reads as a path in a URL, which is the right register for infrastructure. '
  'Cheapest of all of these to own and to reproduce.'),
 ('seal', 'Roundel', 'MB in a badge',
  'DrawSVG &middot; circular container',
  'The monogram inside a drawn circular badge. The circle is a container, not a '
  'concept &mdash; it exists to give the mark a fixed outer silhouette at every size.',
  'The best app icon and avatar here by a distance, because a roundel is what every '
  'circular profile crop actually wants. It also reads as a stamp, which is the '
  'visual grammar of a guarantee &mdash; and the guarantee is the most distinctive '
  'thing you sell.'),
 ('tile', 'Tile', 'the app icon first',
  '3D flip &middot; opposed entry',
  'Designed at 16px and scaled up rather than the other way round. The two letters '
  'enter from opposite edges and the tile lands with a slight turn.',
  'The most practical and the least interesting. Reads instantly at every size and '
  'will never be anybody&rsquo;s favourite thing about the company.'),
 ('byte', 'Megabyte', 'MB is already a unit',
  'clip wipe &middot; knockout',
  'MB is the most boring unit in software &mdash; the number next to a file nobody '
  'thinks about. The mark is set as a unit badge and a fill wipes through it, the '
  'letters knocking out to paper as it passes, the way a disk usage bar fills.',
  'The only one of the eight that arrives with a meaning already attached, because '
  'MB is <em>already</em> a real thing in software. Everything else here has to be '
  'taught. Risk is that MB is a unit of storage, and you do not sell storage.'),
 ('term', 'Terminal', 'mb as a command',
  'typed reveal &middot; caret',
  'A prompt, the command <b>mb</b>, and the output. The mark is what you would type '
  'to make something boring.',
  'Speaks directly to the person who actually evaluates you &mdash; the engineer in '
  'the room. It is also the narrowest: it says developer tool, and it will look '
  'wrong on a pitch deck to a real estate company.'),
]

cards = []
for i, (o, name, kick, tech, story, take) in enumerate(OPTS):
    star = ' star' if o == 'expand' else ''
    cards.append(f'''
<section class="card{star}" id="opt-{o}">
  <div class="chead"><div><span class="num">{i+1:02d}</span><h2>{name}</h2>
    <span class="kick">{kick}</span><span class="tech">{tech}</span></div></div>
  <p class="story">{story}</p>
  <div class="stage" data-opt="{o}" tabindex="0" role="button"
    aria-label="Replay the {name} animation">{stage(o)}</div>
  <div class="ctrl"><button class="rp" data-opt="{o}">Replay</button>
    <button class="rp lp" data-opt="{o}" aria-pressed="false">Loop</button>
    <input class="scrub" type="range" min="0" max="1000" value="1000" data-opt="{o}"
      aria-label="Scrub {name}"><span class="tc" data-opt="{o}">0.00s</span></div>
  <div class="assets">
    <div class="ab"><div class="tabs">
      <div class="tab on"><span class="mkbox f16">{mark(o)}</span>
        <span>madeboring.com</span></div>
      <div class="tab"><i class="ph"></i><span>Gmail</span></div></div>
      <div class="tabb"></div><span class="cap">favicon, 16px</span></div>
    <div class="ab szrow">
      <div class="sz"><span class="mkbox f16">{mark(o)}</span><span>16</span></div>
      <div class="sz"><span class="mkbox f32">{mark(o)}</span><span>32</span></div>
      <div class="sz"><span class="mkbox f64">{mark(o)}</span><span>64</span></div>
      <div class="sz"><span class="apptile">{mark(o)}</span><span>app</span></div>
      <div class="sz"><span class="apptile solid">{mark(o)}</span><span>1&nbsp;col</span></div>
    </div>
    <div class="ab"><div class="lock"><span class="mkbox f40">{mark(o)}</span>
        <span class="wdm">made boring</span></div>
      <div class="lock ink"><span class="mkbox f40">{mark(o)}</span>
        <span class="wdm">made boring</span></div>
      <span class="cap">horizontal lockup &mdash; mark beside the wordmark</span></div>
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
.lbl,.cap,.tech,.num,.tc,.sz>span:last-child,.kick{font-family:var(--mono);letter-spacing:.13em;
 text-transform:uppercase}
.top{display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap;
 border-bottom:2px solid var(--ink);padding-bottom:11px}
.lbl{font-size:10px;color:var(--muted)}
h1{font-family:var(--disp);font-weight:700;font-size:clamp(30px,5.6vw,58px);line-height:.99;
 letter-spacing:-.035em;margin-top:26px;text-wrap:balance}
h1 em{font-style:normal;color:var(--mk)}
.intro{max-width:63ch;margin-top:16px;color:var(--muted);font-size:16px}
.intro b{color:var(--ink);font-weight:600}
.verdict{margin-top:22px;border-left:3px solid var(--mk);padding:2px 0 2px 15px;
 max-width:68ch;font-size:15px;color:var(--muted);line-height:1.62}
.verdict b{color:var(--ink);font-weight:600}
.bar{position:sticky;top:0;z-index:20;display:flex;gap:8px;align-items:center;flex-wrap:wrap;
 background:var(--paper);border-bottom:1px solid var(--line);padding:11px 0;margin-top:30px}
.bar button{font-family:var(--mono);font-size:10px;letter-spacing:.11em;text-transform:uppercase;
 border:1px solid var(--line);background:transparent;color:var(--ink);padding:6px 10px;cursor:pointer}
.bar button[aria-pressed=true]{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.bar button:hover{border-color:var(--ink)}
.bar button:focus-visible,.rp:focus-visible,.scrub:focus-visible{outline:2px solid var(--mk);
 outline-offset:2px}
.card{margin-top:50px;border-top:2px solid var(--ink);padding-top:15px}
.card.star{border-top-color:var(--mk);border-top-width:4px}
.chead>div{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
.num{font-size:11px;color:var(--muted)}
.card h2{font-family:var(--disp);font-size:29px;font-weight:600;letter-spacing:-.03em}
.card.star h2{color:var(--mk)}
.kick{font-size:9.5px;color:var(--muted)}
.tech{font-size:9.5px;color:var(--mk);border:1px solid var(--mk);padding:3px 7px}
.story{max-width:68ch;margin-top:10px;font-size:15px;line-height:1.62;color:var(--muted)}
.story b{color:var(--ink);font-weight:600}
.craft{margin-top:15px;font-size:14.5px;line-height:1.58;color:var(--muted);padding-left:13px;
 border-left:2px solid var(--mk);max-width:70ch}
.craft span{display:block;font-family:var(--mono);font-size:9.5px;letter-spacing:.13em;
 text-transform:uppercase;color:var(--mk);margin-bottom:2px}
.craft em{font-style:italic;color:var(--ink)}
.stage{margin-top:14px;background:var(--swl);border:1px solid var(--line2);height:230px;
 display:grid;place-items:center;overflow:hidden;--mk:var(--green);--tx:#0e0e0d;
 color:var(--tx);position:relative;cursor:pointer}
.stage.ink{background:var(--swd);border-color:#000;--mk:var(--mint);--tx:#f4f3ef}
.stage:after{content:"Click to replay";position:absolute;right:9px;bottom:7px;
 font-family:var(--mono);font-size:9px;letter-spacing:.12em;text-transform:uppercase;
 color:var(--tx);opacity:0;transition:opacity .25s;pointer-events:none}
.stage:hover:after,.stage:focus-visible:after{opacity:.42}
.stage:focus-visible{outline:2px solid var(--mk);outline-offset:2px}

.mk{font-family:var(--disp);font-weight:600;letter-spacing:-.045em;color:var(--mk);
 display:inline-flex;align-items:center;line-height:1;font-style:normal}
.mk i{font-style:normal;display:inline-block}
.lig .lb{margin-left:-.30em}
.stk{flex-direction:column;align-items:center;line-height:.84;letter-spacing:0}
.sl .sls{color:var(--mk);margin:0 -.02em}
.sl .a,.sl .b{color:var(--tx)}
.apptile .sl .a,.apptile .sl .b,.f16 .sl .a,.f16 .sl .b,.f32 .sl .a,.f32 .sl .b,
.f64 .sl .a,.f64 .sl .b,.lock .sl .a,.lock .sl .b{color:var(--mk)}
.f16 .mk{font-size:11px}.f32 .mk{font-size:22px}.f64 .mk{font-size:44px}
.apptile .mk{font-size:30px}
.f16 .lig{font-size:10px}.f32 .lig{font-size:20px}.f64 .lig{font-size:40px}
.apptile .lig{font-size:27px}
.f16 .stk{font-size:8px}.f32 .stk{font-size:16px}.f64 .stk{font-size:32px}
.apptile .stk{font-size:23px}
.f16 .sl{font-size:8.5px}.f32 .sl{font-size:17px}.f64 .sl{font-size:34px}
.apptile .sl{font-size:24px}
.f16 .seal{font-size:9.5px}.f32 .seal{font-size:19px}.f64 .seal{font-size:38px}
.apptile .seal{font-size:26px}
.f16 .tl{font-size:10.5px}.f32 .tl{font-size:21px}.f64 .tl{font-size:42px}
.apptile .tl{font-size:28px}
.f16 .chip{font-size:7px}.f32 .chip{font-size:14px}.f64 .chip{font-size:28px}
.apptile .chip{font-size:17px}
.f16 .term{font-size:11px}.f32 .term{font-size:22px}.f64 .term{font-size:44px}
.apptile .term{font-size:26px}
.seal{position:relative;justify-content:center;width:1.62em;height:1.62em}
.seal i{font-size:.56em;letter-spacing:-.04em;position:relative;top:.01em}
.sealring{position:absolute;inset:0;width:100%;height:100%}
.sealring .sr{stroke:var(--mk)}
.tl{background:var(--mk);color:var(--swl);border-radius:.24em;width:1.5em;height:1.5em;
 justify-content:center;overflow:hidden}
.stage.ink .tl,.apptile .tl{color:#0e0e0d}
.tl i{font-size:.62em}
.chip{border:.085em solid var(--mk);padding:.16em .3em .2em;border-radius:.1em;
 position:relative;overflow:hidden}
.chip .lay{display:block}
.chip .fillwrap{position:absolute;left:0;top:0;bottom:0;width:0;overflow:hidden;
 background:var(--mk)}
.chip .fillwrap .inv{position:absolute;left:0;top:0;padding:.16em .3em .2em;
 white-space:nowrap;color:var(--swl)}
.stage.ink .chip .fillwrap .inv,.apptile .chip .fillwrap .inv{color:#0e0e0d}
.term{font-family:var(--mono);font-weight:400;letter-spacing:0;gap:.34em}
.term .pr{opacity:.45}
.cur{width:.52em;height:1em;background:var(--mk);margin-left:.1em;animation:bl 1.05s steps(1) infinite}
@keyframes bl{50%{opacity:0}}
.big{font-size:clamp(46px,10vw,104px);display:flex;flex-direction:column;
 align-items:center;gap:.16em}
.out{font-family:var(--mono);font-size:.19em;letter-spacing:.1em;text-transform:uppercase;
 color:var(--muted);opacity:0}
.xp{font-family:var(--disp);font-weight:600;font-size:clamp(30px,7vw,72px);
 letter-spacing:-.04em;display:flex;color:var(--tx);white-space:nowrap}
.xp .w{display:inline-flex}
.xp .w2{margin-left:0}
.xp .k{display:inline-block}
.xp .rest{display:inline-block;overflow:hidden;white-space:nowrap;vertical-align:top}

.ctrl{display:flex;align-items:center;gap:11px;border:1px solid var(--line2);border-top:0;
 padding:9px 12px}
.rp{font-family:var(--mono);font-size:10px;letter-spacing:.11em;text-transform:uppercase;
 border:1px solid var(--line);background:transparent;color:var(--ink);padding:6px 11px;cursor:pointer}
.rp:hover{border-color:var(--ink)}
.rp[aria-pressed=true]{background:var(--mk);border-color:var(--mk);color:var(--paper)}
.scrub{flex:1;accent-color:var(--mk);height:3px;cursor:pointer}
.tc{font-size:10px;color:var(--muted);min-width:48px;text-align:right;
 font-variant-numeric:tabular-nums}
.assets{display:grid;grid-template-columns:1fr 1fr;gap:13px;margin-top:13px}
@media(max-width:820px){.assets{grid-template-columns:1fr}}
.ab{border:1px solid var(--line2);padding:13px}
.ab.szrow{display:flex;gap:16px;align-items:flex-end;justify-content:center;flex-wrap:wrap}
.assets .ab:last-child{grid-column:1/-1}
.cap{display:block;font-size:9px;color:var(--muted);margin-top:11px}
.tabs{display:flex;gap:4px;align-items:flex-end}
.tab{display:flex;align-items:center;gap:7px;background:var(--surf);border:1px solid var(--line2);
 border-bottom:0;border-radius:7px 7px 0 0;padding:6px 11px;font-size:11.5px;color:var(--muted);
 white-space:nowrap;font-family:var(--body)}
.tab.on{background:var(--paper);color:var(--ink);font-weight:500}
.tab .ph{width:15px;height:15px;flex:0 0 15px;background:var(--line);border-radius:3px}
.tabb{height:22px;background:var(--paper);border:1px solid var(--line2);border-radius:0 5px 0 0}
.mkbox{display:inline-flex;align-items:center;justify-content:center;--mk:var(--green)}
.f16{font-size:13px;width:16px;height:16px}
.f32{font-size:26px;width:32px;height:32px}
.f64{font-size:52px;width:64px;height:64px}
.f40{font-size:30px}
.mkbox .term{gap:0}
.mkbox .term .pr,.mkbox .cur{display:none}
.sz{display:flex;flex-direction:column;align-items:center;gap:6px}
.sz>span:last-child{font-size:9px;color:var(--muted)}
.apptile{width:58px;height:58px;border-radius:13px;background:var(--ink);
 display:inline-flex;align-items:center;justify-content:center;font-size:34px;
 --mk:var(--mint)}
.apptile .tl{background:var(--mint)}
.apptile.solid{background:var(--green);--mk:#f4f3ef}
.apptile.solid .tl{background:#f4f3ef;color:var(--green)}
.apptile.solid .chip .fillwrap,.apptile.solid .chip{border-color:#f4f3ef}
.apptile .term .pr,.apptile .cur{display:none}
.lock{padding:16px 14px;background:var(--surf);border:1px solid var(--line2);
 display:flex;align-items:center;justify-content:center;gap:.5em;--mk:var(--green);
 --tx:#0e0e0d;color:var(--tx)}
.lock+.lock{margin-top:8px}
.lock.ink{background:var(--swd);border-color:#000;--mk:var(--mint);--tx:#f4f3ef}
.wdm{font-family:var(--disp);font-weight:600;font-size:27px;letter-spacing:-.035em}
.foot{margin-top:50px;border-top:2px solid var(--ink);padding-top:14px;display:flex;
 justify-content:space-between;gap:12px;flex-wrap:wrap}
"""

JSCODE = r"""
gsap.registerPlugin(CustomEase,DrawSVGPlugin,TextPlugin);
CustomEase.create('io','M0,0 C0.16,0.02 0.06,1 1,1');
CustomEase.create('settle','M0,0 C0.2,0 0.13,1.06 1,1');
CustomEase.create('heavy','M0,0 C0.62,0 0.1,1 1,1');
var RM=window.matchMedia('(prefers-reduced-motion: reduce)').matches,TLS={};

/* exact ligature overlap from measured metrics, applied to every .lig on the page */
(function(){
  var probe=document.createElement('canvas').getContext('2d');
  function metrics(px){
    probe.font='600 '+px+'px Jost';
    var M=probe.measureText('M'),B=probe.measureText('B'),I=probe.measureText('I');
    return {mAdv:M.width,mRight:M.actualBoundingBoxRight,
            bLeft:B.actualBoundingBoxLeft,stem:I.actualBoundingBoxRight+
            I.actualBoundingBoxLeft};
  }
  var m=metrics(1000);
  /* overlap = M right sidebearing + B left sidebearing + one stem */
  var overlap=((m.mAdv-m.mRight)+(-m.bLeft)+m.stem)/1000;
  document.querySelectorAll('.lig .lb').forEach(function(el){
    el.style.marginLeft=(-overlap).toFixed(4)+'em';});
  window.__ligOverlap=overlap;
})();

function build(opt){
  var st=document.querySelector('.stage[data-opt="'+opt+'"]');
  var q=function(s){return st.querySelector(s);};
  var tl=gsap.timeline({paused:true});

  if(opt==='expand'){
    var rests=st.querySelectorAll('.rest'),w2=q('.w2');
    var widths=[];
    rests.forEach(function(r){widths.push(r.getBoundingClientRect().width);});
    var gap=parseFloat(getComputedStyle(q('.xp')).fontSize)*0.30;
    tl.fromTo(rests,{width:0,opacity:0},
        {width:function(i){return widths[i];},opacity:1,duration:1.05,
         ease:'io',stagger:.14},0)
      .fromTo(w2,{marginLeft:0},{marginLeft:gap,duration:1.05,ease:'io'},0);
  }
  else if(opt==='ligature'){
    var lb=q('.lb'),lm=q('.lm');
    tl.fromTo(lb,{x:130,opacity:0},{x:0,opacity:1,duration:1.15,ease:'settle'},0)
      .fromTo(lm,{x:-70,opacity:0},{x:0,opacity:1,duration:1.15,ease:'settle'},0)
      .fromTo(q('.mk'),{scale:1.14},{scale:1,duration:.85,ease:'settle'},.95);
  }
  else if(opt==='stack'){
    tl.fromTo(q('.sm'),{y:-120,opacity:0},{y:0,opacity:1,duration:1.05,
        ease:'settle'},0)
      .fromTo(q('.sb'),{y:120,opacity:0},{y:0,opacity:1,duration:1.05,
        ease:'settle'},0)
      .fromTo(q('.stk'),{scale:1.1},{scale:1,duration:.9,ease:'settle'},.85);
  }
  else if(opt==='slash'){
    tl.fromTo(q('.sls'),{y:-130,opacity:0,rotate:-24},{y:0,opacity:1,rotate:0,
        duration:.95,ease:'heavy'},0)
      .fromTo(q('.sl .a'),{x:46,opacity:0},{x:0,opacity:1,duration:.9,
        ease:'settle'},.5)
      .fromTo(q('.sl .b'),{x:-46,opacity:0},{x:0,opacity:1,duration:.9,
        ease:'settle'},.5);
  }
  else if(opt==='seal'){
    tl.fromTo(q('.sr'),{drawSVG:'0% 0%'},{drawSVG:'0% 100%',duration:1.3,ease:'io'},0)
      .fromTo(q('.seal i'),{opacity:0,scale:.72},{opacity:1,scale:1,duration:.9,
        ease:'settle'},.55)
      .fromTo(q('.seal'),{rotate:-14},{rotate:0,duration:1.4,ease:'settle'},0);
  }
  else if(opt==='tile'){
    gsap.set(q('.big'),{perspective:600});
    tl.fromTo(q('.tl'),{rotateY:-78,scale:.72,opacity:0},
        {rotateY:0,scale:1,opacity:1,duration:1.15,ease:'settle'},0)
      .fromTo(q('.tm'),{xPercent:-190,opacity:0},{xPercent:0,opacity:1,duration:.85,
        ease:'settle'},.35)
      .fromTo(q('.tb'),{xPercent:190,opacity:0},{xPercent:0,opacity:1,duration:.85,
        ease:'settle'},.35);
  }
  else if(opt==='byte'){
    tl.fromTo(q('.chip'),{scale:.86,opacity:0},{scale:1,opacity:1,duration:.6,
        ease:'settle'},0)
      .fromTo(q('.fillwrap'),{width:'0%'},{width:'100%',duration:1.05,
        ease:'io'},.45)
      .to(q('.fillwrap'),{width:'0%',duration:.85,ease:'io'},1.75);
  }
  else{
    var cmd=q('.cmd');
    tl.fromTo(q('.pr'),{opacity:0},{opacity:.45,duration:.3},0)
      .fromTo(cmd,{text:''},{text:'mb',duration:.5,ease:'none'},.35)
      .fromTo(q('.out'),{opacity:0,y:6},{opacity:1,y:0,duration:.5,ease:'io'},1.15);
  }
  TLS[opt]=tl;
  var scr=document.querySelector('.scrub[data-opt="'+opt+'"]'),
      tc=document.querySelector('.tc[data-opt="'+opt+'"]');
  tl.eventCallback('onUpdate',function(){scr.value=Math.round(tl.progress()*1000);
    tc.textContent=tl.time().toFixed(2)+'s';});
  scr.addEventListener('input',function(){tl.pause().progress(scr.value/1000);
    tc.textContent=tl.time().toFixed(2)+'s';});
}
['expand','ligature','stack','slash','seal','tile','byte','term'].forEach(build);

function play(o){if(TLS[o])TLS[o].restart();}
document.querySelectorAll('.rp:not(.lp)').forEach(function(b){
  b.addEventListener('click',function(){play(b.dataset.opt);});});
document.querySelectorAll('.rp.lp').forEach(function(b){
  b.addEventListener('click',function(){
    var o=b.dataset.opt,tl=TLS[o];if(!tl)return;
    var on=b.getAttribute('aria-pressed')==='true';
    b.setAttribute('aria-pressed',String(!on));
    tl.repeat(on?0:-1).repeatDelay(on?0:.7);
    if(on){tl.progress(1).pause();}else{tl.restart();}});});
document.querySelectorAll('.stage').forEach(function(s){
  s.addEventListener('click',function(){play(s.dataset.opt);});
  s.addEventListener('keydown',function(e){
    if(e.key==='Enter'||e.key===' '){e.preventDefault();play(s.dataset.opt);}});});
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
    {threshold:.4});
  document.querySelectorAll('.stage').forEach(function(s){io.observe(s);});
}
"""

html = (
 '<title>made boring &mdash; MB, eight monograms</title>\n'
 '<style>' + CSS.replace('__JOST__', JOST).replace('__PLEX__', PLEX) + '</style>\n'
 '<div class="wrap">'
 '<div class="top"><span class="lbl">made boring &middot; brand</span>'
 '<span class="lbl">round six &middot; MB &middot; 8 monograms</span></div>'
 '<h1>Two letters that <em>unfold</em><br>into the whole name.</h1>'
 '<p class="intro">MB buys you the one thing a mark living inside the word never '
 'could: <b>it detaches</b>. It is an app icon, an avatar, a favicon, a stamp on an '
 'invoice, and a symbol that sits <i>beside</i> the wordmark rather than trapped in '
 'the middle of it. Every option below is shown in exactly that lockup. And because '
 '<b>m</b> and <b>b</b> really are the first letters of <b>made</b> and <b>boring</b>, '
 'the monogram can expand into the full name without cheating &mdash; which is what '
 'the first one does.</p>'
 '<p class="verdict">The honest risk, stated once: <b>MB is contested territory.</b> '
 'Every second consultancy is an MB, and the shortform carries no meaning of its own '
 '&mdash; with a single exception, which is that MB is already a unit of data. Option '
 '07 is built on exactly that, and it is the only one of the eight that arrives with '
 'a meaning already attached rather than one you have to spend money teaching people. '
 'Options 02 and 04 are the ones that solve the sameness problem by construction '
 'instead: a merged stem and a coloured slash are both things a generic MB does not '
 'have.</p>'
 '<div class="bar"><span class="lbl">Controls</span>'
 '<button id="playall">Play all</button>'
 '<button id="gnd" aria-pressed="false">Ground: ink</button>'
 '<button id="slow" aria-pressed="false">0.35&times; speed</button></div>'
 + ''.join(cards) +
 '<div class="foot"><span class="lbl">Nothing here is live on madeboring.com yet</span>'
 '<span class="lbl">Name one and it ships</span></div></div>'
 '<script>' + GSAP + '</script>\n<script>' + JSCODE + '</script>'
)
html = html.encode('ascii', 'xmlcharrefreplace').decode()
pathlib.Path('mb.html').write_text(html)
print('written', round(len(html) / 1024, 1), 'KB')
