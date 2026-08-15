import ast, pathlib

data = ast.literal_eval(pathlib.Path('_inline.py').read_text())
S, V = data['svgs'], data['vids']

CONCEPTS = [
 (2, "Flatline", "A panicking pulse that resolves into a dead-flat line.",
  "The only mark here that says something. Flat means nothing is happening, and nothing happening is the whole pitch. It is also the one that animates naturally — the line can draw itself.",
  "recommended", "Reads as a wordmark-width lockup, not a square. Needs a square crop for the favicon."),
 (4, "Notched square", "A solid square with a pin-one orientation notch.",
  "The boldest mark and the best small-size survivor — still legible at 16px, which is where most logos die. Closest to a real component marking.",
  "strong", "The silhouette reads a little like a luggage tag or a bookmark icon."),
 (1, "Registration mark", "A target square with four alignment ticks.",
  "Clean, scales cleanly, and ties directly to the crosshair already running on the live site. Competent but not distinctive.",
  "safe", "Generic — a hundred technical brands use a reticle."),
 (6, "Tolerance target", "Three concentric squares, innermost solid.",
  "Perfectly balanced and it scales without losing anything. The most conservative option on the sheet.",
  "safe", "Reads as a stop or record button before it reads as a brand."),
 (5, "Chip footprint", "An IC package seen from above, pin one marked.",
  "The most literal expression of the engineering register, and the most detailed thing here.",
  "weak", "The legs merge into grey mush below about 32px. Fails the favicon test."),
 (3, "Order from disorder", "A field of ticks resolving from scatter into lattice.",
  "Genuinely beautiful and exactly on-thesis, but this is a texture, not a mark.",
  "weak", "Unreadable at any size a logo is actually used. Keep it as a background asset."),
]

VERDICT = {
 "recommended": ("Recommended", "var(--green)"),
 "strong": ("Strong", "var(--ink)"),
 "safe": ("Safe", "var(--muted)"),
 "weak": ("Not for a logo", "var(--alert)"),
}

rows = []
for n, name, sub, why, verd, risk in CONCEPTS:
    label, col = VERDICT[verd]
    rows.append(
        '<article class="row" id="c%d">'
        '<div class="meta"><div class="idx">%02d</div><h3>%s</h3>'
        '<p class="sub">%s</p><p class="why">%s</p>'
        '<p class="risk"><span>Watch out</span>%s</p>'
        '<div class="verdict" style="--vc:%s">%s</div></div>'
        '<div class="tests"><div class="big paper">%s</div>'
        '<div class="strip">'
        '<div class="t"><div class="box paper"><div class="sz s26">%s</div></div><span>26px &middot; nav</span></div>'
        '<div class="t"><div class="box paper"><div class="sz s16">%s</div></div><span>16px &middot; favicon</span></div>'
        '<div class="t"><div class="box ink"><div class="sz s26 inv">%s</div></div><span>26px &middot; inverted</span></div>'
        '<div class="t"><div class="box ink"><div class="sz s44 inv">%s</div></div><span>44px &middot; inverted</span></div>'
        '</div></div></article>'
        % (n, n, name, sub, why, risk, col, label, S[n], S[n], S[n], S[n], S[n])
    )


def vid(b64, title, note, tone=''):
    return (
        '<figure class="clip %s"><video src="data:video/mp4;base64,%s" '
        'autoplay loop muted playsinline></video>'
        '<figcaption><b>%s</b><span>%s</span></figcaption></figure>'
        % (tone, b64, title, note)
    )


CSS = """
:root {
  --paper:#f4f3ef; --paper2:#eceae4; --ink:#101010; --green:#1b6b45;
  --rule:#cfcec7; --rule2:#e2e0d9; --muted:#6e6d66; --alert:#c2410c;
  --mono: ui-monospace,"SF Mono",SFMono-Regular,Menlo,monospace;
  --sans: system-ui,-apple-system,"Segoe UI",sans-serif;
}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--paper);color:var(--ink);font-family:var(--sans);
  font-size:16px;line-height:1.6;font-variant-numeric:tabular-nums;-webkit-font-smoothing:antialiased}
.wrap{max-width:1080px;margin:0 auto;padding:clamp(24px,5vw,64px) clamp(18px,4vw,44px) 90px}
.lbl{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.top{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;
  border-bottom:2px solid var(--ink);padding-bottom:12px}
h1{font-family:var(--mono);font-size:clamp(26px,4.4vw,44px);line-height:1.05;
  letter-spacing:-.03em;font-weight:500;margin-top:34px;text-wrap:balance}
.intro{max-width:60ch;margin-top:18px;color:var(--muted);font-size:16.5px}
.intro b{color:var(--ink);font-weight:600}
.live{margin-top:44px;border:2px solid var(--ink);display:grid;grid-template-columns:1.1fr 1fr}
@media(max-width:760px){.live{grid-template-columns:1fr}}
.live-a{padding:clamp(24px,4vw,40px);border-right:2px solid var(--ink);
  display:flex;flex-direction:column;justify-content:center;gap:22px}
@media(max-width:760px){.live-a{border-right:0;border-bottom:2px solid var(--ink)}}
.live-b{padding:clamp(24px,4vw,40px);background:var(--ink);color:var(--paper);
  display:flex;flex-direction:column;justify-content:center;gap:22px}
.live-b .lbl{color:#8a8880}
.mark-live svg{display:block;overflow:visible;width:190px;height:auto}
.mark-live path{stroke:currentColor;fill:none;stroke-width:3.2;
  stroke-linecap:square;animation:draw 4.6s cubic-bezier(.4,0,.2,1) infinite}
@keyframes draw{
  0%{stroke-dashoffset:100} 34%{stroke-dashoffset:0}
  76%{stroke-dashoffset:0} 100%{stroke-dashoffset:-100} }
@media(prefers-reduced-motion:reduce){
  .mark-live path{animation:none;stroke-dashoffset:0}
  video{display:none}}
.note{font-size:14px;line-height:1.55;color:var(--muted);max-width:38ch}
.live-b .note{color:#a3a19a}
h2{font-family:var(--mono);font-size:13px;letter-spacing:.14em;text-transform:uppercase;
  font-weight:500;margin-top:74px;padding-bottom:10px;border-bottom:2px solid var(--ink)}
.row{display:grid;grid-template-columns:1fr 1.35fr;gap:clamp(20px,4vw,52px);
  padding:clamp(26px,3.4vw,40px) 0;border-bottom:1px solid var(--rule)}
@media(max-width:820px){.row{grid-template-columns:1fr}}
.idx{font-family:var(--mono);font-size:11px;letter-spacing:.14em;color:var(--muted)}
.row h3{font-size:23px;letter-spacing:-.02em;font-weight:600;margin-top:8px}
.sub{font-family:var(--mono);font-size:12.5px;color:var(--muted);margin-top:7px;line-height:1.5}
.why{font-size:15px;line-height:1.6;margin-top:16px;max-width:44ch}
.risk{font-size:13.5px;line-height:1.55;margin-top:14px;color:var(--muted);
  padding-left:13px;border-left:2px solid var(--alert);max-width:44ch}
.risk span{display:block;font-family:var(--mono);font-size:10px;letter-spacing:.13em;
  text-transform:uppercase;color:var(--alert);margin-bottom:3px}
.verdict{display:inline-block;margin-top:18px;font-family:var(--mono);font-size:10.5px;
  letter-spacing:.13em;text-transform:uppercase;border:1px solid var(--vc);color:var(--vc);padding:5px 10px}
.big{border:1px solid var(--rule2);aspect-ratio:16/8;display:grid;place-items:center;padding:22px}
.big svg{width:auto;height:100%;max-width:100%;display:block}
.paper{background:var(--paper2)}
.ink{background:var(--ink)}
.strip{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:12px}
.t{display:flex;flex-direction:column;gap:7px;align-items:center}
.t span{font-family:var(--mono);font-size:9.5px;letter-spacing:.07em;color:var(--muted);text-align:center}
.box{width:100%;aspect-ratio:1;display:grid;place-items:center;border:1px solid var(--rule2)}
.box.ink{border-color:var(--ink)}
.sz svg{display:block;width:100%;height:100%}
.s16{width:16px;height:16px} .s26{width:26px;height:26px} .s44{width:44px;height:44px}
.inv{filter:invert(1) hue-rotate(180deg)}
.clips{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px;margin-top:26px}
.clip{border:1px solid var(--rule)}
.clip video{width:100%;display:block;background:var(--paper2)}
.clip figcaption{padding:12px 14px;border-top:1px solid var(--rule);display:flex;flex-direction:column;gap:4px}
.clip b{font-size:14.5px;font-weight:600}
.clip span{font-family:var(--mono);font-size:11px;line-height:1.5;color:var(--muted)}
.clip.good{border-color:var(--ink)}
.clip.good figcaption{border-top-color:var(--ink)}
.foot{margin-top:70px;border-top:2px solid var(--ink);padding-top:16px;
  display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap;
  font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
"""

MARK = ('<svg viewBox="0 0 64 40" fill="none"><path pathLength="100" stroke-dasharray="100" '
        'd="M1 20 H13 L17 20 L20 8 L24 33 L28 14 L31 20 H63"/></svg>')

html = (
 '<title>made boring — pick a mark</title>\n<style>' + CSS + '</style>\n'
 '<div class="wrap">'
 '<div class="top"><span class="lbl">made boring &middot; brand</span>'
 '<span class="lbl">6 marks &middot; 12 aug 2026</span></div>'
 '<h1>Pick a mark.</h1>'
 '<p class="intro">Six concepts, generated as real vector. Each is shown at the sizes that '
 '<b>actually decide a logo</b> — 26px in a nav bar and 16px as a favicon — because that is '
 'where marks fail, not in a hero. Every mark is also shown reversed on ink, since half the site '
 'is a dark section.</p>'
 '<div class="live">'
 '<div class="live-a"><span class="lbl">01 &middot; Flatline, animated in code</span>'
 '<div class="mark-live" style="color:#101010">' + MARK + '</div>'
 '<p class="note">This is the live component, not a video — an animated SVG that draws itself '
 'and settles flat. About 1KB, sharp at any size, and it inherits text colour.</p></div>'
 '<div class="live-b"><span class="lbl">Reversed on ink</span>'
 '<div class="mark-live" style="color:#f4f3ef">' + MARK + '</div>'
 '<p class="note">Same file, no second asset. An MP4 logo could not do this — it would carry '
 'its own background and stay the wrong colour.</p></div>'
 '</div>'
 '<h2>The six marks</h2>' + ''.join(rows) +
 '<h2>Motion assets</h2>'
 '<p class="intro" style="margin-top:18px">Generated with Higgsfield. These are for '
 '<b>section backgrounds</b>, not for the logo. Two drifted off the cream ground into khaki — '
 'fixable, but flagged rather than hidden.</p>'
 '<div class="clips">' +
 vid(V['asset-connect'], 'Connect — best of the set',
     'Two boxes, a line draws, data flows. Belongs directly above “your two systems are '
     'integrated by a person with a spreadsheet.” Background drifted khaki.', 'good') +
 vid(V['asset-untangle'], 'Untangle',
     'A tangle resolving into parallel lines. Visually the strongest. Background drifted khaki.') +
 vid(V['logo-reticle'], 'Reticle in motion',
     'Ticks converge and lock on. Usable, but busy in the middle where it sprouts extra diagonals.') +
 '</div>'
 '<div class="foot"><span>Nothing here is live on madeboring.com yet</span>'
 '<span>Reply with a number</span></div>'
 '</div>'
)

pathlib.Path('chooser.html').write_text(html)
print('written', round(len(html) / 1024 / 1024, 2), 'MB')
