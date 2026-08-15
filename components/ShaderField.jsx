'use client';

import React, { useEffect, useRef } from 'react';

const VERT = 'attribute vec2 a;void main(){gl_Position=vec4(a,0.,1.);}';

function rgb(v) {
  const n = parseInt(v.trim().slice(1), 16);
  return [((n >> 16) & 255) / 255, ((n >> 8) & 255) / 255, (n & 255) / 255];
}

export default function ShaderField({ frag, still = 20 }) {
  const ref = useRef(null);

  useEffect(() => {
    const canvas = ref.current;
    if (!canvas) return;
    const gl = canvas.getContext('webgl', {
      antialias: false,
      alpha: false,
      powerPreference: 'low-power',
    });
    if (!gl) return;

    const compile = (type, src) => {
      const s = gl.createShader(type);
      gl.shaderSource(s, src);
      gl.compileShader(s);
      return s;
    };
    const prog = gl.createProgram();
    gl.attachShader(prog, compile(gl.VERTEX_SHADER, VERT));
    gl.attachShader(prog, compile(gl.FRAGMENT_SHADER, frag));
    gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) return;
    gl.useProgram(prog);

    gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
    const loc = gl.getAttribLocation(prog, 'a');
    gl.enableVertexAttribArray(loc);
    gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);

    const U = (n) => gl.getUniformLocation(prog, n);
    const loadTokens = () => {
      const css = getComputedStyle(document.documentElement);
      const tok = (n, fb) => rgb(css.getPropertyValue(n).trim() || fb);
      gl.uniform3fv(U('u_bg'), tok('--ground', '#0a0a0b'));
      gl.uniform3fv(U('u_brand'), tok('--brand', '#ff4d1c'));
      gl.uniform3fv(U('u_lift'), tok('--brand-lift', '#ff6a3d'));
      gl.uniform3fv(U('u_deep'), tok('--brand-deep', '#c1330c'));
    };
    loadTokens();
    const uRes = U('u_res');
    const uTime = U('u_time');
    const uMouse = U('u_mouse');
    const uM = U('u_m');

    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const size = () => {
      const w = canvas.clientWidth;
      const h = canvas.clientHeight;
      if (!w || !h) return;
      canvas.width = Math.round(w * dpr);
      canvas.height = Math.round(h * dpr);
      gl.viewport(0, 0, canvas.width, canvas.height);
      gl.uniform2f(uRes, canvas.width, canvas.height);
    };
    size();
    const ro = new ResizeObserver(size);
    ro.observe(canvas);

    const m = { x: 0.5, y: 0.5, tx: 0.5, ty: 0.5, p: 0, tp: 0 };
    const host = canvas.closest('.hero') || canvas.parentElement;
    const move = (e) => {
      const b = host.getBoundingClientRect();
      m.tx = (e.clientX - b.left) / b.width;
      m.ty = 1 - (e.clientY - b.top) / b.height;
      m.tp = 1;
    };
    const leave = () => {
      m.tp = 0;
    };
    host.addEventListener('mousemove', move);
    host.addEventListener('mouseleave', leave);

    const t0 = performance.now();
    let raf = 0;
    let live = true;
    let extra = null;

    const frame = () => {
      raf = 0;
      if (!live || gl.isContextLost()) return;
      m.x += (m.tx - m.x) * 0.08;
      m.y += (m.ty - m.y) * 0.08;
      m.p += (m.tp - m.p) * 0.05;
      gl.uniform1f(uTime, (performance.now() - t0) / 1000);
      gl.uniform2f(uMouse, m.x, m.y);
      gl.uniform1f(uM, m.p);
      gl.drawArrays(gl.TRIANGLES, 0, 3);
      raf = requestAnimationFrame(frame);
    };

    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const mo = new MutationObserver(() => {
      if (gl.isContextLost()) return;
      loadTokens();
      if (reduced) gl.drawArrays(gl.TRIANGLES, 0, 3);
    });
    mo.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });

    if (reduced) {
      gl.uniform1f(uTime, still);
      gl.uniform2f(uMouse, 0.5, 0.5);
      gl.uniform1f(uM, 0);
      gl.drawArrays(gl.TRIANGLES, 0, 3);
    } else {
      const wake = () => {
        if (live && !raf) raf = requestAnimationFrame(frame);
      };
      const halt = () => {
        cancelAnimationFrame(raf);
        raf = 0;
      };
      const io = new IntersectionObserver((es) => {
        if (es.some((e) => e.isIntersecting)) wake();
        else halt();
      });
      io.observe(canvas);
      const vis = () => (document.hidden ? halt() : wake());
      document.addEventListener('visibilitychange', vis);
      extra = () => {
        io.disconnect();
        document.removeEventListener('visibilitychange', vis);
      };
      raf = requestAnimationFrame(frame);
    }

    return () => {
      live = false;
      cancelAnimationFrame(raf);
      ro.disconnect();
      mo.disconnect();
      host.removeEventListener('mousemove', move);
      host.removeEventListener('mouseleave', leave);
      if (extra) extra();
    };
  }, [frag, still]);

  return <canvas ref={ref} className="sf" aria-hidden="true" />;
}
