'use client';

import React, { useEffect } from 'react';

export default function Glow() {
  useEffect(() => {
    if (window.matchMedia('(hover: none)').matches) return;
    const move = (e) => {
      const el = e.target.closest?.('[data-glow]');
      if (!el) return;
      const r = el.getBoundingClientRect();
      el.style.setProperty('--mx', `${e.clientX - r.left}px`);
      el.style.setProperty('--my', `${e.clientY - r.top}px`);
    };
    document.addEventListener('mousemove', move, { passive: true });
    return () => document.removeEventListener('mousemove', move);
  }, []);
  return null;
}
