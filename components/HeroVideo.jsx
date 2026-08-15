'use client';

import React, { useEffect, useRef, useState } from 'react';

/**
 * Seamless looping video layer.
 *
 * Generated clips do not loop cleanly, so two copies run half a period out of
 * phase and cross-fade at the seam — the cut never lands while a layer is
 * visible. The clip is graded to the brand orange and composited with
 * `screen`, so its black falls away entirely and only the light lands on the
 * page ground. That is what makes it sit *in* the UI rather than on top of it.
 */
export default function HeroVideo({ src, blend = 'screen', opacity = 0.9, fade = 0.9 }) {
  const a = useRef(null);
  const b = useRef(null);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    const va = a.current;
    const vb = b.current;
    if (!va || !vb) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      va.pause();
      vb.pause();
      setReady(true);
      return;
    }

    let raf;
    const start = () => {
      const d = va.duration;
      if (!d || Number.isNaN(d)) return;
      vb.currentTime = d / 2;
      va.play().catch(() => {});
      vb.play().catch(() => {});
      setReady(true);

      const tick = () => {
        const d2 = va.duration || d;
        const half = d2 / 2;
        // cross-fade over `fade` seconds either side of each seam
        const ta = va.currentTime;
        const tb = vb.currentTime;
        const w = (t) => {
          const edge = Math.min(t, d2 - t);
          return Math.min(1, edge / fade);
        };
        const wa = w(ta);
        const wb = w(tb);
        const sum = wa + wb || 1;
        va.style.opacity = String((wa / sum) * opacity);
        vb.style.opacity = String((wb / sum) * opacity);
        if (half) raf = requestAnimationFrame(tick);
      };
      raf = requestAnimationFrame(tick);
    };

    if (va.readyState >= 1) start();
    else va.addEventListener('loadedmetadata', start, { once: true });

    return () => cancelAnimationFrame(raf);
  }, [opacity, fade]);

  const common = {
    muted: true,
    playsInline: true,
    loop: true,
    preload: 'auto',
    'aria-hidden': true,
    className: 'hv-layer',
  };

  return (
    <div className="hv" data-ready={String(ready)} style={{ mixBlendMode: blend }}>
      <div className="hv-inner">
        <video ref={a} src={src} {...common} />
        <video ref={b} src={src} {...common} />
        <div className="hv-tint" aria-hidden="true" />
      </div>
    </div>
  );
}
