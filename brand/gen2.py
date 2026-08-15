import pathlib
from marks import MARKS

ANIM = {
 'bore':
  '<mask id="mk-bore"><rect x="6" y="6" width="52" height="52" fill="#fff"/>'
  '<circle class="drill" cx="32" cy="32" r="12.5" fill="#000"/></mask>'
  '<rect x="6" y="6" width="52" height="52" fill="currentColor" mask="url(#mk-bore)"/>',
 'boreb':
  '<mask id="mk-boreb"><rect x="7" y="4" width="10" height="56" fill="#fff"/>'
  '<circle cx="33" cy="32" r="18" fill="#fff"/>'
  '<circle class="drill" cx="33" cy="32" r="8" fill="#000"/></mask>'
  '<rect x="0" y="0" width="64" height="64" fill="currentColor" mask="url(#mk-boreb)"/>',
 'equals':
  '<rect class="sl-l" x="6" y="22" width="52" height="9"/>'
  '<rect class="sl-r" x="6" y="38" width="52" height="9"/>',
 'reduce':
  '<rect class="rd rd1" x="6" y="10" width="52" height="8"/>'
  '<rect class="rd rd2" x="6" y="24" width="39" height="8"/>'
  '<rect class="rd rd3" x="6" y="38" width="26" height="8"/>'
  '<rect class="rd rd4" x="6" y="52" width="13" height="8"/>',
 'minus': '<rect class="mn" x="6" y="27" width="52" height="10"/>',
 'nest':
  '<path fill-rule="evenodd" d="M4 4h56v56H4V4Zm9 9v38h38V13H13Z"/>'
  '<rect class="ns" x="22" y="22" width="20" height="20"/>',
 'notch': '<path d="M6 6h52v34L40 58H6V6Z"/>',
 'through':
  '<path fill-rule="evenodd" d="M14 14h36v36H14V14Zm8 8v20h20V22H22Z"/>'
  '<rect class="th" x="0" y="28" width="64" height="8"/>',
}

REFS = [
 ("Paul Rand · IBM", "Eight stripes cut through three letters. Proof that a mark can be built "
  "from one repeated primitive and nothing else."),
 ("FedEx · negative space", "The arrow nobody draws. The idea lives in the gap between two "
  "letters, so the mark rewards a second look without demanding one."),
 ("Chermayeff &amp; Geismar · Chase", "Four identical shapes, rotated. A pure ideograph — it "
  "depicts nothing and means something anyway."),
 ("Mies van der Rohe", "“Less is more.” The dictum the whole modernist logo tradition runs on, "
  "and the literal product promise here."),
]

VERD = {
 'rec': ('Recommended', 'var(--green)'),
 'strong': ('Strong', 'var(--ink)'),
 'safe': ('Safe', 'var(--muted)'),
 'risk': ('Risky', 'var(--alert)'),
}

ORDER = [
 ('boreb', 'rec', 'Only mark that is a monogram, a pun and a machined object at once. '
  'Reads as “b” instantly, which no other option here does.'),
 ('bore', 'rec', 'The same idea without the letter. Cleaner, more universal, slightly less ownable.'),
 ('reduce', 'strong', 'The most literal statement of the service. Least likely to be mistaken '
  'for another company.'),
 ('equals', 'strong', 'Survives smaller than anything else here. Risk is that “=” belongs to '
  'everyone.'),
 ('notch', 'safe', 'Best small-size survivor from the first round, now drawn properly on the grid.'),
 ('nest', 'safe', 'Correct, balanced, and completely anonymous.'),
 ('minus', 'risk', 'The most committed version of the joke. Also nearly invisible at 16px — '
  'look at the favicon test before you fall for it.'),
 ('through', 'risk', 'Good idea, too many parts. It mushes below about 26px.'),
]


def svg(body, cls=''):
    return ('<svg class="%s" viewBox="0 0 64 64" fill="currentColor" '
            'xmlns="http://www.w3.org/2000/svg">%s</svg>' % (cls, body))


rows = []
for key, verd, take in ORDER:
    name, sub, why, kind, static = MARKS[key]
    label, col = VERD[verd]
    big = svg(ANIM[key], 'anim a-%s' % key)
    st = svg(static)
    rows.append(f'''<article class="row">
<div class="meta">
  <div class="kind">{kind}</div>
  <h3>{name}</h3>
  <p class="sub">{sub}</p>
  <p class="why">{why}</p>
  <p class="take"><span>My take</span>{take}</p>
  <div class="verdict" style="--vc:{col}">{label}</div>
</div>
<div class="tests">
  <div class="big">{big}</div>
  <div class="strip">
    <div class="t"><div class="box"><i class="z48">{st}</i></div><span>48px</span></div>
    <div class="t"><div class="box"><i class="z26">{st}</i></div><span>26px &middot; nav</span></div>
    <div class="t"><div class="box"><i class="z16">{st}</i></div><span>16px &middot; favicon</span></div>
    <div class="t"><div class="box ink"><i class="z26">{st}</i></div><span>reversed</span></div>
  </div>
  <div class="lock"><i class="z22">{st}</i><b>made boring</b></div>
</div>
</article>''')

refs = ''.join(
    '<div class="ref"><b>%s</b><p>%s</p></div>' % (t, d) for t, d in REFS
)

CSS = """
:root{--paper:#f4f3ef;--paper2:#eceae4;--ink:#101010;--green:#1b6b45;--rule:#cfcec7;
 --rule2:#e2e0d9;--muted:#6e6d66;--alert:#c2410c;
 --mono:ui-monospace,"SF Mono",SFMono-Regular,Menlo,monospace;
 --sans:system-ui,-apple-system,"Segoe UI",sans-serif}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--paper);color:var(--ink);font-family:var(--sans);font-size:16px;
 line-height:1.6;-webkit-font-smoothing:antialiased;font-variant-numeric:tabular-nums}
.wrap{max-width:1060px;margin:0 auto;padding:clamp(24px,5vw,60px) clamp(18px,4vw,42px) 90px}
.lbl{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.top{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;
 border-bottom:2px solid var(--ink);padding-bottom:12px}
h1{font-family:var(--mono);font-size:clamp(25px,4.2vw,42px);line-height:1.05;letter-spacing:-.03em;
 font-weight:500;margin-top:32px;text-wrap:balance}
.intro{max-width:62ch;margin-top:18px;color:var(--muted);font-size:16.5px}
.intro b{color:var(--ink);font-weight:600}
h2{font-family:var(--mono);font-size:12px;letter-spacing:.14em;text-transform:uppercase;font-weight:500;
 margin-top:62px;padding-bottom:10px;border-bottom:2px solid var(--ink)}
.refs{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:0;
 border-left:1px solid var(--rule2)}
.ref{border-right:1px solid var(--rule2);border-bottom:1px solid var(--rule2);padding:16px 18px}
.ref b{display:block;font-family:var(--mono);font-size:11px;letter-spacing:.08em;
 text-transform:uppercase;color:var(--green);margin-bottom:8px}
.ref p{font-size:13.5px;line-height:1.55;color:var(--muted)}
.row{display:grid;grid-template-columns:1fr 1.3fr;gap:clamp(20px,4vw,50px);
 padding:clamp(26px,3.4vw,40px) 0;border-bottom:1px solid var(--rule)}
@media(max-width:820px){.row{grid-template-columns:1fr}}
.kind{font-family:var(--mono);font-size:10.5px;letter-spacing:.13em;text-transform:uppercase;color:var(--muted)}
.row h3{font-size:24px;letter-spacing:-.02em;font-weight:600;margin-top:8px}
.sub{font-family:var(--mono);font-size:12.5px;color:var(--muted);margin-top:7px;line-height:1.5}
.why{font-size:15px;line-height:1.6;margin-top:16px;max-width:44ch}
.take{font-size:13.5px;line-height:1.55;margin-top:15px;color:var(--muted);padding-left:13px;
 border-left:2px solid var(--green);max-width:44ch}
.take span{display:block;font-family:var(--mono);font-size:10px;letter-spacing:.13em;
 text-transform:uppercase;color:var(--green);margin-bottom:3px}
.verdict{display:inline-block;margin-top:18px;font-family:var(--mono);font-size:10.5px;
 letter-spacing:.13em;text-transform:uppercase;border:1px solid var(--vc);color:var(--vc);padding:5px 10px}
.big{background:var(--paper2);border:1px solid var(--rule2);display:grid;place-items:center;
 padding:26px;aspect-ratio:16/7}
.big svg{width:auto;height:100%;max-height:130px;display:block}
.strip{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:12px}
.t{display:flex;flex-direction:column;gap:7px;align-items:center}
.t span{font-family:var(--mono);font-size:9.5px;letter-spacing:.06em;color:var(--muted);text-align:center}
.box{width:100%;aspect-ratio:1;display:grid;place-items:center;border:1px solid var(--rule2);
 background:var(--paper2)}
.box.ink{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.box i{display:block}
.box svg{width:100%;height:100%;display:block}
.z48{width:48px;height:48px}.z26{width:26px;height:26px}.z16{width:16px;height:16px}.z22{width:22px;height:22px}
.lock{display:flex;align-items:center;gap:10px;margin-top:16px;padding:14px 16px;
 border:1px solid var(--rule2)}
.lock i{display:block}.lock svg{width:100%;height:100%;display:block}
.lock b{font-size:17px;font-weight:600;letter-spacing:-.02em}
.foot{margin-top:66px;border-top:2px solid var(--ink);padding-top:16px;display:flex;
 justify-content:space-between;gap:14px;flex-wrap:wrap;font-family:var(--mono);font-size:10.5px;
 letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.drill{animation:drill 3.6s cubic-bezier(.65,0,.35,1) infinite}
@keyframes drill{0%,8%{r:0}42%,68%{r:12.5}100%{r:0}}
.a-boreb .drill{animation:drillb 3.6s cubic-bezier(.65,0,.35,1) infinite}
@keyframes drillb{0%,8%{r:0}42%,68%{r:8}100%{r:0}}
.sl-l{animation:slL 3.6s cubic-bezier(.65,0,.35,1) infinite}
.sl-r{animation:slR 3.6s cubic-bezier(.65,0,.35,1) infinite}
@keyframes slL{0%{transform:translateX(-60px)}30%,72%{transform:none}100%{transform:translateX(-60px)}}
@keyframes slR{0%{transform:translateX(60px)}30%,72%{transform:none}100%{transform:translateX(60px)}}
.rd{transform-origin:6px 50%;animation:rdA 3.6s cubic-bezier(.65,0,.35,1) infinite}
.rd2{animation-delay:.12s}.rd3{animation-delay:.24s}.rd4{animation-delay:.36s}
@keyframes rdA{0%{transform:scaleX(4)}26%,70%{transform:none}100%{transform:scaleX(4)}}
.mn{transform-origin:50% 50%;animation:mnA 3.6s cubic-bezier(.65,0,.35,1) infinite}
@keyframes mnA{0%{transform:scaleX(0)}26%,70%{transform:none}100%{transform:scaleX(0)}}
.ns{transform-origin:50% 50%;animation:nsA 3.6s cubic-bezier(.65,0,.35,1) infinite}
@keyframes nsA{0%{transform:scale(2.1)}30%,70%{transform:none}100%{transform:scale(2.1)}}
.th{transform-origin:50% 50%;animation:thA 3.6s cubic-bezier(.65,0,.35,1) infinite}
@keyframes thA{0%{transform:scaleX(0)}30%,70%{transform:none}100%{transform:scaleX(0)}}
@media(prefers-reduced-motion:reduce){.anim *{animation:none!important}}
"""

html = (
 '<title>made boring — marks, round two</title>\n<style>' + CSS + '</style>\n'
 '<div class="wrap">'
 '<div class="top"><span class="lbl">made boring &middot; brand</span>'
 '<span class="lbl">round two &middot; 8 marks</span></div>'
 '<h1>Made simple. Made easy.<br>Made boring.</h1>'
 '<p class="intro">Round one read “boring” as <b>uneventful</b> and produced heart monitors. '
 'This round reads it the way you meant it — <b>simple, easy, a non-issue</b> — and every mark '
 'below is constructed on a 64-unit grid in code rather than generated, which is why the edges '
 'are true and the small sizes hold. Two ideas recur: <b>subtraction</b> (something removed) and '
 '<b>the second meaning of “boring”</b> — what a machinist does when drilling a precise hole.</p>'
 '<h2>What the marks worth copying actually do</h2>'
 '<div class="refs">' + refs + '</div>'
 '<h2>Eight marks</h2>' + ''.join(rows) +
 '<div class="foot"><span>Nothing here is live on madeboring.com</span>'
 '<span>Reply with a name</span></div></div>'
)

pathlib.Path('chooser2.html').write_text(html)
print('written', round(len(html) / 1024, 1), 'KB')
