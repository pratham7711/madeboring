'use client';

import React, { useEffect, useState } from 'react';
import Logo from '@/components/Logo';
import Ic from '@/components/Icons';

const LINKS = [
  ['#pain', 'Problems'],
  ['#build', 'What we build'],
  ['#engagement', 'How it works'],
  ['#warranty', 'Warranty'],
];

export default function Nav() {
  const [stuck, setStuck] = useState(false);
  const [paper, setPaper] = useState(false);

  useEffect(() => {
    const onScroll = () => setStuck(window.scrollY > 24);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    setPaper(document.documentElement.dataset.theme === 'paper');
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  return (
    <header className="nav" data-stuck={String(stuck)}>
      <div className="shell nav-in">
        <a href="#top" aria-label="made boring, home">
          <Logo />
        </a>
        <nav className="nav-links">
          {LINKS.map(([href, label]) => (
            <a className="hide-sm" key={href} href={href}>
              {label}
            </a>
          ))}
          <button
            className="theme-btn"
            type="button"
            aria-label="Paper theme"
            aria-pressed={paper}
            onClick={() => {
              const el = document.documentElement;
              const next = el.dataset.theme === 'paper' ? '' : 'paper';
              if (next) el.dataset.theme = next;
              else delete el.dataset.theme;
              setPaper(Boolean(next));
              try {
                localStorage.setItem('mb-theme', next);
              } catch {}
            }}
          >
            <Ic name="contrast" size={16} />
          </button>
          <a className="ghost" href="#contact">
            Start the pilot
          </a>
        </nav>
      </div>
    </header>
  );
}
