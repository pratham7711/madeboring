import pathlib, re

ORDER = [
 ('geo-b', 'Split b', 'A bold bar and a circle, overlapping, with the overlap in mint.',
  'rec',
  'Reads as “b” in the first half-second, which none of the flowing marks manage. Two shapes, '
  'two tones, one letter — the construction language of Slack and Figma rather than a drawing. '
  'It is the only mark here that is simultaneously energetic and instantly legible at 16px.'),
 ('fold-arrow', 'Fold', 'A chevron made from one ribbon folded once, the fold catching a darker green.',
  'rec',
  'The most premium silhouette in the set and the best small-size survivor. Forward motion without '
  'an arrow cliché, and the single fold does all the work — one idea, executed once. This is the '
  'one I would put on a business card.'),
 ('overlap-b', 'Eclipse', 'Two rounded shapes overlapping, a b emerging from the gap.',
  'strong',
  'The boldest, simplest form here. Confident and modern, and it holds its shape reversed on ink. '
  'Slightly more abstract than Split b — you see the letter on the second look, not the first.'),
 ('knot-ribbon', 'Knot', 'A single flat ribbon tied into a clean symmetrical knot.',
  'strong',
  'The most ownable and distinctive mark on the sheet — nothing else in your category looks like '
  'this. Concept is exact: the tangle, tied off neatly. Watch that at small sizes it can start to '
  'read as a flower rather than a knot.'),
 ('gesture', 'Release', 'A tight spiral unwinding into one long smooth sweep.',
  'strong',
  'The purest expression of the brief — complexity releasing into ease, in a single gesture. It is '
  'also the most beautiful thing here. The cost is the tapering tail, which thins out and starts '
  'to disappear below about 26px.'),
 ('infinity', 'Unwind', 'Loops that unroll and flatten into a straight line.',
  'safe',
  'Elegant, and it carries real motion. The problem is legibility of meaning: at a glance it reads '
  'as cursive handwriting rather than as loops resolving.'),
 ('ribbon-b', 'Script b', 'A typographic b with a single ribbon loop through the bowl.',
  'safe',
  'Genuinely lovely letterform and the most classical option. Too delicate for the job — the fine '
  'strokes collapse at favicon size and it reads more like a publishing house than a software company.'),
 ('s-twist', 'Twist', 'Two twisting forms, one dark, one green.',
  'risk',
  'Off-concept. It reads as a leaf or a yin-yang, which points at wellness rather than at software. '
  'Included so you can see it and rule it out.'),
]

VERD = {'rec': ('Recommended', 'var(--green)'), 'strong': ('Strong', 'var(--ink)'),
        'safe': ('Safe', 'var(--muted)'), 'risk': ('Rule it out', 'var(--alert)')}

d = pathlib.Path('r3')
rows = []
for key, name, sub, verd, take in ORDER:
    t = (d / f'{key}.svg').read_text()
    t = re.sub(r'<\?xml[^>]*\?>', '', t).strip()
    t = re.sub(r'\s(width|height)="[^"]*"', '', t, count=2)
    label, col = VERD[verd]
    rows.append(f'''<article class="row">
<div class="meta">
  <h3>{name}</h3>
  <p class="sub">{sub}</p>
  <p class="take">{take}</p>
  <div class="verdict" style="--vc:{col}">{label}</div>
</div>
<div class="tests">
  <div class="big">{t}</div>
  <div class="strip">
    <div class="t"><div class="box"><i class="z44">{t}</i></div><span>44px</span></div>
    <div class="t"><div class="box"><i class="z26">{t}</i></div><span>26px &middot; nav</span></div>
    <div class="t"><div class="box"><i class="z16">{t}</i></div><span>16px &middot; favicon</span></div>
    <div class="t"><div class="box ink"><i class="z26">{t}</i></div><span>on ink</span></div>
  </div>
  <div class="lock"><i class="z26">{t}</i><b>made boring</b></div>
</div></article>''')

CSS = """
:root{--paper:#f4f3ef;--paper2:#eceae4;--ink:#101010;--green:#1b6b45;--rule:#cfcec7;
 --rule2:#e2e0d9;--muted:#6e6d66;--alert:#c2410c;
 --mono:ui-monospace,"SF Mono",SFMono-Regular,Menlo,monospace;
 --sans:system-ui,-apple-system,"Segoe UI",sans-serif}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--paper);color:var(--ink);font-family:var(--sans);font-size:16px;
 line-height:1.6;-webkit-font-smoothing:antialiased}
.wrap{max-width:1060px;margin:0 auto;padding:clamp(24px,5vw,60px) clamp(18px,4vw,42px) 90px}
.lbl{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.top{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;
 border-bottom:2px solid var(--ink);padding-bottom:12px}
h1{font-size:clamp(30px,5.2vw,54px);line-height:1.02;letter-spacing:-.035em;font-weight:700;
 margin-top:32px;text-wrap:balance}
h1 em{font-style:normal;color:var(--green)}
.intro{max-width:62ch;margin-top:20px;color:var(--muted);font-size:17px}
.intro b{color:var(--ink);font-weight:600}
h2{font-family:var(--mono);font-size:12px;letter-spacing:.14em;text-transform:uppercase;
 font-weight:500;margin-top:58px;padding-bottom:10px;border-bottom:2px solid var(--ink)}
.row{display:grid;grid-template-columns:1fr 1.25fr;gap:clamp(20px,4vw,50px);
 padding:clamp(26px,3.4vw,40px) 0;border-bottom:1px solid var(--rule)}
@media(max-width:820px){.row{grid-template-columns:1fr}}
.row h3{font-size:26px;letter-spacing:-.025em;font-weight:700}
.sub{font-family:var(--mono);font-size:12.5px;color:var(--muted);margin-top:8px;line-height:1.5}
.take{font-size:15px;line-height:1.62;margin-top:18px;max-width:46ch;color:#3a3a36}
.verdict{display:inline-block;margin-top:20px;font-family:var(--mono);font-size:10.5px;
 letter-spacing:.13em;text-transform:uppercase;border:1px solid var(--vc);color:var(--vc);padding:5px 10px}
.big{background:var(--paper2);border:1px solid var(--rule2);display:grid;place-items:center;
 padding:24px;aspect-ratio:16/8}
.big svg{width:auto;height:100%;max-height:150px;display:block}
.strip{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:12px}
.t{display:flex;flex-direction:column;gap:7px;align-items:center}
.t span{font-family:var(--mono);font-size:9.5px;letter-spacing:.06em;color:var(--muted);text-align:center}
.box{width:100%;aspect-ratio:1;display:grid;place-items:center;border:1px solid var(--rule2);
 background:var(--paper2)}
.box.ink{background:var(--ink);border-color:var(--ink)}
.box i,.lock i{display:block}
.box svg,.lock svg{width:100%;height:100%;display:block}
.z44{width:44px;height:44px}.z26{width:26px;height:26px}.z16{width:16px;height:16px}
.lock{display:flex;align-items:center;gap:11px;margin-top:16px;padding:14px 16px;
 border:1px solid var(--rule2)}
.lock b{font-size:18px;font-weight:700;letter-spacing:-.025em}
.foot{margin-top:64px;border-top:2px solid var(--ink);padding-top:16px;display:flex;
 justify-content:space-between;gap:14px;flex-wrap:wrap;font-family:var(--mono);font-size:10.5px;
 letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
"""

html = (
 '<title>made boring — marks, round three</title>\n<style>' + CSS + '</style>\n'
 '<div class="wrap">'
 '<div class="top"><span class="lbl">made boring &middot; brand</span>'
 '<span class="lbl">round three &middot; 8 marks</span></div>'
 '<h1>The name is deadpan.<br>The mark <em>should not be.</em></h1>'
 '<p class="intro">Rounds one and two took “boring” as a styling instruction and produced a '
 'minus sign and a square. Wrong: <b>“made boring” is the promise, not the look.</b> Nike’s mark '
 'is not shaped like a shoe. So these marks all say <b>complexity released into ease</b> — a knot '
 'tied off, a ribbon folded, a spiral unwinding — while being things you would actually want on a '
 'business card. Every one is real vector, and every one is shown at favicon size, because that '
 'is still where marks die.</p>'
 '<h2>Eight marks</h2>' + ''.join(rows) +
 '<div class="foot"><span>Nothing here is live on madeboring.com</span>'
 '<span>Reply with a name</span></div></div>'
)
pathlib.Path('chooser.html').write_text(html)
print('written', round(len(html) / 1024, 1), 'KB')
