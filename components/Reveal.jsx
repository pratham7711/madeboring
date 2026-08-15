'use client';

import React, { useEffect, useRef } from 'react';

export default function Reveal({
  children,
  selector = ':scope > *',
  stagger = 0.07,
  y = 16,
  className,
  style,
  as: Tag = 'div',
}) {
  const root = useRef(null);

  useEffect(() => {
    const el = root.current;
    if (!el) return;
    const targets = [...el.querySelectorAll(selector)];
    if (!targets.length) return;

    const show = () => targets.forEach((t) => t.classList.add('rv-in'));

    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      show();
      return;
    }

    targets.forEach((t, i) => {
      t.style.setProperty('--rv-y', `${y}px`);
      t.style.transitionDelay = `${(i * stagger).toFixed(3)}s`;
      t.classList.add('rv-init');
    });

    const io = new IntersectionObserver(
      (entries) => {
        if (!entries.some((e) => e.isIntersecting)) return;
        io.disconnect();
        show();
      },
      { rootMargin: '0px 0px -10% 0px', threshold: 0 }
    );
    io.observe(el);

    const failsafe = setTimeout(show, 1600);

    return () => {
      io.disconnect();
      clearTimeout(failsafe);
    };
  }, [selector, stagger, y]);

  return (
    <Tag ref={root} className={className} style={style}>
      {children}
    </Tag>
  );
}
