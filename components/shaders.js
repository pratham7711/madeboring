const LIB = `
precision highp float;
uniform vec2 u_res;
uniform float u_time;
uniform vec2 u_mouse;
uniform float u_m;
uniform vec3 u_bg,u_brand,u_lift,u_deep;
float hash(vec2 p){p=fract(p*vec2(123.34,456.21));p+=dot(p,p+45.32);return fract(p.x*p.y);}
float noise(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);float a=hash(i),b=hash(i+vec2(1.,0.)),c=hash(i+vec2(0.,1.)),d=hash(i+vec2(1.,1.));return mix(mix(a,b,f.x),mix(c,d,f.x),f.y);}
float fbm(vec2 p){float v=0.,a=.5;for(int i=0;i<5;i++){v+=a*noise(p);p=mat2(1.6,1.2,-1.2,1.6)*p;a*=.5;}return v;}
float grain(vec2 p,float t){return (hash(p+fract(t)*vec2(17.,29.))-.5)*.02;}
`;

export const FRAG = {
  current:
    LIB +
    `
void main(){
  vec2 uv=gl_FragCoord.xy/u_res;
  vec2 p=vec2(uv.x*2.2,uv.y*5.0);
  float t=u_time*.05;
  float md=length(uv-u_mouse);
  vec2 bend=normalize(uv-u_mouse+1e-4)*exp(-md*md*9.)*.55*u_m;
  vec2 q=vec2(fbm(p+vec2(t*1.4,0.)),fbm(p+vec2(0.,t)+5.2));
  float v=fbm(p+2.0*q+bend+vec2(t*3.,0.));
  float fil=smoothstep(.42,.62,v)*smoothstep(.95,.62,v);
  float glow=fbm(p*.5+q)*.22;
  vec3 col=u_bg;
  col=mix(col,u_deep,glow*.9);
  col=mix(col,u_brand,fil*(.5+.4*noise(p*3.+t*8.)));
  col=mix(col,u_lift,pow(fil,3.)*.5);
  float vig=smoothstep(1.25,.45,length(uv-vec2(.5,.45)));
  col=mix(u_bg,col,vig);
  col+=grain(gl_FragCoord.xy,u_time);
  gl_FragColor=vec4(col,1.);
}`,

  grid:
    LIB +
    `
void main(){
  vec2 uv=gl_FragCoord.xy/u_res;
  float ar=u_res.x/u_res.y;
  vec2 suv=vec2(uv.x*ar,uv.y);
  float N=24.;
  vec2 g=suv*N;
  vec2 id=floor(g),f=fract(g)-.5;
  float t=u_time;
  float w=sin(id.x*.55+t*1.1)*sin(id.y*.38-t*.7);
  float n=noise(id*.23+vec2(t*.15,-t*.11));
  vec2 muv=vec2(u_mouse.x*ar,u_mouse.y);
  float md=length(suv-muv);
  float lens=exp(-md*md*14.)*u_m;
  float r=.11+.15*n+.09*w+.27*lens;
  float d=length(f);
  float dm=smoothstep(r,r-.09,d);
  vec3 col=mix(u_bg*1.5,u_brand,dm*(.3+.7*clamp(n+.4,0.,1.)));
  col=mix(col,u_lift,dm*lens*.9);
  col+=grain(gl_FragCoord.xy,u_time);
  gl_FragColor=vec4(col,1.);
}`,

  forge:
    LIB +
    `
void main(){
  vec2 uv=gl_FragCoord.xy/u_res;
  float ar=u_res.x/u_res.y;
  vec2 p=vec2((uv.x-.28)*ar,uv.y-.5);
  float t=u_time*.22;
  float fsum=0.;
  for(int i=0;i<5;i++){
    float fi=float(i);
    vec2 c=vec2(sin(t*(.61+.13*fi)+fi*1.7)*(.34+.06*fi),cos(t*(.47+.11*fi)+fi*2.3)*.17);
    fsum+=(.05+.028*fi)/max(length(p-c),1e-3);
  }
  float body=smoothstep(1.05,1.3,fsum);
  float core=smoothstep(1.55,2.3,fsum);
  vec3 col=u_deep*(.6+.3*fbm(p*3.+t));
  col=mix(col,u_brand,body);
  col=mix(col,u_lift,core*.85);
  col+=u_lift*pow(smoothstep(.85,1.3,fsum),4.)*.25;
  col+=grain(gl_FragCoord.xy,u_time);
  gl_FragColor=vec4(col,1.);
}`,

  ember:
    LIB +
    `
void main(){
  vec2 uv=gl_FragCoord.xy/u_res;
  float ar=u_res.x/u_res.y;
  vec2 p=vec2(uv.x*ar*1.4,uv.y*2.6);
  float t=u_time*.09;
  vec2 q=vec2(fbm(p+vec2(0.,-t*2.2)),fbm(p+vec2(3.1,-t*1.7)));
  float s=fbm(p+1.7*q+vec2(0.,-t*3.));
  float smoke=smoothstep(.35,.85,s);
  vec2 sg=uv*vec2(60.*ar,16.);
  vec2 sid=floor(sg);
  float ph=hash(sid);
  float tw=pow(max(0.,sin(u_time*(.6+ph*1.4)+ph*6.28)),24.);
  float sd=length(fract(sg)-.5);
  float spark=tw*smoothstep(.18,.02,sd)*step(.85,hash(sid+7.));
  vec3 col=u_bg;
  col+=u_deep*smoke*.7+u_brand*smoke*smoke*.8;
  col+=u_lift*spark;
  col+=grain(gl_FragCoord.xy,u_time);
  gl_FragColor=vec4(col,1.);
}`,

  flatline:
    LIB +
    `
void main(){
  vec2 uv=gl_FragCoord.xy/u_res;
  float t=u_time;
  float calm=exp(-pow(abs(uv.x-u_mouse.x)*2.6,2.))*u_m;
  float amp=mix(1.,.05,clamp(calm,0.,1.));
  float x=uv.x*7.;
  float y=.5
    +amp*.10*sin(x*2.1+t*1.9)
    +amp*.07*sin(x*3.7-t*2.6)
    +amp*.05*sin(x*5.3+t*3.4)
    +amp*.12*(noise(vec2(x*1.5,t*.7))-.5);
  float d=abs(uv.y-y);
  float line=exp(-d*140.);
  float glow=exp(-d*22.)*.5;
  vec3 col=u_bg;
  col+=u_deep*glow+u_brand*line;
  col+=u_lift*pow(line,3.)*.6;
  col+=grain(gl_FragCoord.xy,u_time);
  gl_FragColor=vec4(col,1.);
}`,
};
