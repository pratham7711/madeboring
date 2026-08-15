'use client';

import React, { useEffect, useState } from 'react';
import Nav from '@/components/Nav';
import Crosshair from '@/components/Crosshair';
import { CONCEPTS, HEROES } from '@/components/heroes';

export default function HeroLab() {
  const [i, setI] = useState(0);
  const [note, setNote] = useState(false);
  const c = CONCEPTS[i];
  const Hero = HEROES[c.id];

  useEffect(() => {
    const onKey = (e) => {
      if (e.key === 'ArrowRight') setI((n) => (n + 1) % CONCEPTS.length);
      if (e.key === 'ArrowLeft') setI((n) => (n - 1 + CONCEPTS.length) % CONCEPTS.length);
      if (e.key === 'i') setNote((v) => !v);
      const n = parseInt(e.key, 10);
      if (n >= 1 && n <= CONCEPTS.length) setI(n - 1);
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, []);

  return (
    <>
      <Crosshair />
      <Nav />
      <main key={c.id} className="fade-swap lab">
        <Hero clip={c.clip} />
      </main>

      {note && (
        <aside className="concept-note">
          <span className="lbl">
            Concept {c.n} &mdash; {c.name}
          </span>
          <span className="tech">{c.tech}</span>
          <span className="thesis">{c.thesis}</span>
        </aside>
      )}

      <nav className="switch" aria-label="Hero concepts">
        {CONCEPTS.map((x, n) => (
          <button
            key={x.id}
            aria-current={String(n === i)}
            onClick={() => setI(n)}
            title={x.tech}
          >
            <span className="sw-n">{x.n}</span>
            {x.name}
          </button>
        ))}
        <button
          className="sw-i"
          aria-pressed={String(note)}
          onClick={() => setNote((v) => !v)}
          title="Concept notes (i)"
        >
          i
        </button>
      </nav>
    </>
  );
}
