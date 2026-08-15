'use client';

import React, { useEffect, useRef, useState } from 'react';

export default function StickyCta() {
  const [on, setOn] = useState(false);
  const seen = useRef(false);

  useEffect(() => {
    const after = document.getElementById('warranty');
    const stop = document.getElementById('contact');
    if (!after || !stop) return;

    const check = () => {
      const paid = after.getBoundingClientRect().bottom < 0;
      const arrived = stop.getBoundingClientRect().top < window.innerHeight * 0.9;
      seen.current = paid;
      setOn(paid && !arrived);
    };

    check();
    window.addEventListener('scroll', check, { passive: true });
    window.addEventListener('resize', check);
    return () => {
      window.removeEventListener('scroll', check);
      window.removeEventListener('resize', check);
    };
  }, []);

  return (
    <div className="sticky-cta" data-on={String(on)} aria-hidden={!on}>
      <span className="sticky-cta-tx">
        Fixed date, fixed number. <b>110% back if we miss it.</b>
      </span>
      <a className="btn" href="#contact" tabIndex={on ? 0 : -1}>
        <span>Start the pilot</span>
      </a>
    </div>
  );
}
