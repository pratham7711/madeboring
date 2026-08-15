import json, pathlib

NM = pathlib.Path('/Users/pratham/madeboring/site/node_modules/gsap/dist')
js = lambda n: (NM / n).read_text()
GSAP = '\n'.join(js(n) for n in ['gsap.min.js', 'CustomEase.min.js',
                                 'DrawSVGPlugin.min.js', 'MotionPathPlugin.min.js'])

G = json.loads(pathlib.Path('glyphs.json').read_text())
SK = json.loads(pathlib.Path('skeleton.json').read_text())
GL, POS, MBP, WORD = G['glyphs'], G['pos'], G['mbpos'], G['word']

DOT_R = (GL['.']['bbox'][2] - GL['.']['bbox'][0]) / 2
DOT_X = MBP['2']['x'] + (GL['.']['bbox'][0] + GL['.']['bbox'][2]) / 2
DOT_Y = (GL['.']['bbox'][1] + GL['.']['bbox'][3]) / 2
TIT = GL['i']['tittle_bbox']
TIT_R = (TIT[2] - TIT[0]) / 2
TIT_X = POS['7']['x'] + (TIT[0] + TIT[2]) / 2
TIT_Y = (TIT[1] + TIT[3]) / 2

W = G['wordW'] + 140
H = W / 4.0                      # 4:1 frame, 1200x300
VB = '-70 %.2f %.2f %.2f' % (-270 - H / 2, W, H)

import os
FG, BG = ('#12523a', '#f3f0e7') if os.environ.get('LIGHT') else ('#f3f0e7', '#12523a')


def svg():
    out = ['<svg id="lg" xmlns="http://www.w3.org/2000/svg" viewBox="%s" '
           'width="1200" height="300"><rect x="-70" y="%.2f" width="%.2f" '
           'height="%.2f" fill="%s"/><g transform="scale(1,-1)">'
           % (VB, -270 - H / 2, W, H, BG)]
    for i, ch in enumerate(WORD):
        d = GL[ch]['stem'] if ch == 'i' else GL[ch]['path']
        role = 'core' if (i == 0 or i == 4) else 'mid'
        mbx = MBP['1']['x'] if i == 4 else POS[str(i)]['x']
        out.append('<path class="g %s g%d" data-x="%d" data-mbx="%s" fill="%s" '
                   'transform="translate(%s,0)" d="%s"/>'
                   % (role, i, POS[str(i)]['x'], mbx, FG, mbx, d))
    out.append('<circle class="dot" cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>'
               % (DOT_X, DOT_Y, DOT_R, FG))
    out.append('<g class="sk" opacity="0">')
    for d in SK['m']:
        out.append('<path d="%s" stroke-width="%s" fill="none" stroke="%s" '
                   'stroke-linecap="butt" stroke-linejoin="round"/>'
                   % (d, SK['stem'], FG))
    for d in SK['b']:
        out.append('<path d="%s" stroke-width="%s" transform="translate(%d,0)" '
                   'fill="none" stroke="%s" stroke-linecap="butt" '
                   'stroke-linejoin="round"/>' % (d, SK['bstem'], SK['bx'], FG))
    out.append('<path d="%s" stroke-width="%s" fill="none" stroke="%s" '
               'stroke-linecap="round"/>' % (SK['dot'], SK['dotStroke'], FG))
    out.append('</g></g></svg>')
    return ''.join(out)


JS = r"""
gsap.registerPlugin(CustomEase,DrawSVGPlugin,MotionPathPlugin);
CustomEase.create('io','M0,0 C0.16,0.02 0.06,1 1,1');
var D=__DOT__,svg=document.getElementById('lg');
var mids=svg.querySelectorAll('.mid'),b=svg.querySelector('.g4'),
    dot=svg.querySelector('.dot'),sk=svg.querySelector('.sk'),
    skp=[].slice.call(svg.querySelectorAll('.sk path')),
    ink=[svg.querySelector('.g0'),b,dot];
var tl=gsap.timeline({paused:true});
(function(){
  var L=skp.map(function(e){return e.getTotalLength();});
  var tot=L.reduce(function(a,c){return a+c;},0),t=0;
  tl.set(ink,{fillOpacity:0}).set(sk,{opacity:1});
  skp.forEach(function(e,i){
    var d=1.1*L[i]/tot;
    tl.fromTo(e,{drawSVG:'0%'},{drawSVG:'100%',duration:d,ease:'none'},t);
    t+=d+.02;
  });
  tl.to(ink,{fillOpacity:1,duration:.26,ease:'io'},t+.04)
    .to(sk,{opacity:0,duration:.26,ease:'io'},t+.1);
  var at=t+.42,dx=D.tx-D.x,dy=D.ty-D.y,s=D.tr/D.r;
  tl.to(b,{x:+b.getAttribute('data-x'),duration:.9,ease:'io'},at)
    .fromTo(mids,{opacity:0,scaleX:.2,transformOrigin:'0% 50%'},
      {opacity:1,scaleX:1,duration:.5,ease:'io',stagger:{each:.035,from:'center'}},at)
    .to(dot,{x:dx,duration:.9,ease:'power2.inOut'},at)
    .to(dot,{y:dy,scale:s,duration:.65,ease:'power3.out'},at+.25);
})();
gsap.set(mids,{opacity:0});
window.DUR=tl.duration();
var cv=document.createElement('canvas');cv.width=1200;cv.height=300;
var cx=cv.getContext('2d');
window.grab=async function(from,to,fps){
  for(var i=from;i<to;i++){
    tl.pause().time(Math.min(i/fps,tl.duration()));
    var s=new XMLSerializer().serializeToString(svg);
    var url='data:image/svg+xml;base64,'+btoa(unescape(encodeURIComponent(s)));
    await new Promise(function(res,rej){
      var im=new Image();
      im.onload=function(){cx.clearRect(0,0,1200,300);cx.drawImage(im,0,0,1200,300);res();};
      im.onerror=rej;im.src=url;});
    await fetch('http://127.0.0.1:4900/frame/'+i,
      {method:'POST',body:cv.toDataURL('image/png')});
  }
  return to-from;
};
"""

DOT = json.dumps({'x': DOT_X, 'y': DOT_Y, 'r': DOT_R,
                  'tx': TIT_X, 'ty': TIT_Y, 'tr': TIT_R})

html = ('<!doctype html><meta charset="utf-8"><title>capture</title>'
        '<style>body{margin:0;background:#222}svg{display:block}</style>'
        + svg() + '<script>' + GSAP + '</script><script>'
        + JS.replace('__DOT__', DOT) + '</script>')
pathlib.Path('capture.html').write_text(html)
print('capture.html written', round(len(html) / 1024), 'KB  viewBox', VB)
