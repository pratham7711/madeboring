'use client';

import React, { useEffect, useRef, useState } from 'react';
import { gsap } from 'gsap';
import { SEGMENTS } from '@/lib/content';

export default function Segments() {
  const [active, setActive] = useState(0);
  const panel = useRef(null);
  const first = useRef(true);

  useEffect(() => {
    if (first.current) {
      first.current = false;
      return;
    }
    const el = panel.current;
    if (!el) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    const ctx = gsap.context(() => {
      gsap.fromTo(
        '[role="tabpanel"]:not([hidden]) .seg-item',
        { opacity: 0, y: 12 },
        { opacity: 1, y: 0, duration: 0.42, stagger: 0.055, ease: 'power2.out' }
      );
    }, el);
    return () => ctx.revert();
  }, [active]);

  return (
    <>
      <div className="seg-tabs" role="tablist" aria-label="Choose your situation">
        {SEGMENTS.map((s, i) => (
          <button
            key={s.key}
            role="tab"
            id={`tab-${s.key}`}
            aria-selected={i === active}
            aria-controls={`seg-panel-${s.key}`}
            tabIndex={i === active ? 0 : -1}
            className="seg-tab"
            onClick={() => setActive(i)}
            onKeyDown={(e) => {
              const last = SEGMENTS.length - 1;
              let next = null;
              if (e.key === 'ArrowRight') next = active === last ? 0 : active + 1;
              if (e.key === 'ArrowLeft') next = active === 0 ? last : active - 1;
              if (e.key === 'Home') next = 0;
              if (e.key === 'End') next = last;
              if (next === null) return;
              e.preventDefault();
              setActive(next);
              document.getElementById(`tab-${SEGMENTS[next].key}`)?.focus();
            }}
          >
            <span>{s.label}</span>
            <span className="sm">{s.scale}</span>
          </button>
        ))}
      </div>

      <div ref={panel}>
        {SEGMENTS.map((s, i) => (
          <div
            key={s.key}
            id={`seg-panel-${s.key}`}
            role="tabpanel"
            aria-labelledby={`tab-${s.key}`}
            hidden={i !== active}
          >
            <div className="seg-meta">
              <span className="lbl">{s.label}</span>
              <span className="lbl">{s.sub}</span>
            </div>
            <div className="seg-grid">
              {s.pains.slice(0, 3).map((p) => (
                <div className="seg-item" key={p.quote}>
                  <p className="q">&ldquo;{p.quote}&rdquo;</p>
                  <p className="cost">{p.cost}</p>
                  {p.href ? (
                    <a className="cite" href={p.href} target="_blank" rel="noopener nofollow">
                      {p.src}
                      {p.year ? `, ${p.year}` : ''} ↗
                    </a>
                  ) : null}
                  <div className="fx">
                    <span className="ar">→</span>
                    <span>{p.fix}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </>
  );
}
