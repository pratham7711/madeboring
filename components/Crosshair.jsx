'use client';

import React, { useEffect, useRef } from 'react';

const HOT = 'a, button, [role="tab"], .chip, input, textarea';

export default function Crosshair() {
  const el = useRef(null);
  const ring = useRef(null);
  const dot = useRef(null);

  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    if (!window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;

    const node = el.current;
    const r = { x: innerWidth / 2, y: innerHeight / 2 };
    const p = { x: r.x, y: r.y };
    let raf;
    let shown = false;

    const move = (e) => {
      p.x = e.clientX;
      p.y = e.clientY;
      if (!shown) {
        shown = true;
        node.style.opacity = '1';
      }
      node.dataset.hot = String(!!e.target.closest?.(HOT));
    };

    const tick = () => {
      r.x += (p.x - r.x) * 0.18;
      r.y += (p.y - r.y) * 0.18;
      dot.current.style.transform = `translate3d(${p.x}px, ${p.y}px, 0)`;
      ring.current.style.transform = `translate3d(${r.x}px, ${r.y}px, 0)`;
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);

    const hide = () => (node.style.opacity = '0');
    window.addEventListener('mousemove', move, { passive: true });
    document.addEventListener('mouseleave', hide);

    return () => {
      cancelAnimationFrame(raf);
      window.removeEventListener('mousemove', move);
      document.removeEventListener('mouseleave', hide);
    };
  }, []);

  return (
    <div className="cursor" ref={el} aria-hidden="true" style={{ opacity: 0 }}>
      <div className="cursor-ring" ref={ring} />
      <div className="cursor-dot" ref={dot} />
    </div>
  );
}
