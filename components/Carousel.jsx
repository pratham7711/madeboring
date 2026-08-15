'use client';

import React, { useCallback, useEffect, useRef, useState } from 'react';
import Ic from '@/components/Icons';

export default function Carousel({ children, label, className = '' }) {
  const track = useRef(null);
  const [edge, setEdge] = useState({ start: true, end: true });

  const sync = useCallback(() => {
    const el = track.current;
    if (!el) return;
    const max = el.scrollWidth - el.clientWidth;
    setEdge({ start: el.scrollLeft <= 2, end: max <= 2 || el.scrollLeft >= max - 2 });
  }, []);

  useEffect(() => {
    const el = track.current;
    if (!el) return;
    sync();
    el.addEventListener('scroll', sync, { passive: true });
    const ro = new ResizeObserver(sync);
    ro.observe(el);
    return () => {
      el.removeEventListener('scroll', sync);
      ro.disconnect();
    };
  }, [sync]);

  const nudge = (dir) => {
    const el = track.current;
    if (!el) return;
    const first = el.firstElementChild;
    const step = first ? first.getBoundingClientRect().width + 20 : el.clientWidth * 0.85;
    el.scrollBy({ left: dir * step, behavior: 'smooth' });
  };

  return (
    <div className={`car ${className}`.trim()}>
      <div
        className="car-track"
        ref={track}
        tabIndex={0}
        role="group"
        aria-label={label}
        onKeyDown={(e) => {
          if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
          e.preventDefault();
          nudge(e.key === 'ArrowRight' ? 1 : -1);
        }}
      >
        {children}
      </div>
      <div className="car-nav">
        <button
          type="button"
          className="car-btn car-prev"
          onClick={() => nudge(-1)}
          disabled={edge.start}
          aria-label="Previous"
        >
          <Ic name="arrow" size={16} />
        </button>
        <button
          type="button"
          className="car-btn"
          onClick={() => nudge(1)}
          disabled={edge.end}
          aria-label="Next"
        >
          <Ic name="arrow" size={16} />
        </button>
      </div>
    </div>
  );
}
