'use client';

import React, { useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import { motion, useReducedMotion } from 'motion/react';
import HeroFilm from '@/components/HeroFilm';
import { SPEC } from '@/lib/content';

export default function Hero() {
  const root = useRef(null);
  const reduce = useReducedMotion();

  useEffect(() => {
    const ctx = gsap.context(() => {
      const lines = root.current.querySelectorAll('.rl > span');
      if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        gsap.set([lines, '.hf'], { y: 0, yPercent: 0, opacity: 1 });
        return;
      }
      gsap.set(lines, { yPercent: 145 });
      gsap
        .timeline({ delay: 0.15 })
        .to(lines, { yPercent: 0, duration: 1.1, stagger: 0.09, ease: 'power4.out' })
        .fromTo(
          '.hf',
          { y: 16, opacity: 0 },
          { y: 0, opacity: 1, duration: 0.75, stagger: 0.09, ease: 'power2.out' },
          '-=0.55'
        );
    }, root);
    return () => ctx.revert();
  }, []);

  return (
    <section className="hero hero-film" id="top" ref={root}>
      <div className="hero-bg">
        <HeroFilm
          webm="/video/desk.webm"
          mp4="/video/desk.mp4"
          poster="/video/desk-poster.jpg"
        />
        <div className="grid-lines" aria-hidden="true" />
        <div className="veil veil-film" aria-hidden="true" />
      </div>
      <div className="shell hero-in">
        <div className="sheet-top hf">
          <span className="lbl accent">Fixed date. Fixed price.</span>
        </div>

        <h1 className="display">
          <span className="rl">
            <span>{'Your month-end,'}</span>
          </span>
          <span className="rl">
            <span>
              <em>in one click.</em>
            </span>
          </span>
        </h1>

        <div className="hero-grid">
          <div>
            <p className="lede hf">
              The job someone does by hand every month becomes a button, whether that is
              one person or five hundred. Priced and dated on day five, or 110% back.
            </p>
            <div className="hero-cta hf">
              <a className="btn" href="#contact">
                <span>Start the pilot</span>
              </a>
              <a className="btn-txt" href="#contact">
                <span>What keeps breaking? →</span>
              </a>
            </div>
            <p className="hero-risk hf">
              <b>One reply, from Pratham</b>, usually the same day
            </p>
          </div>

          <motion.div
            className="hf"
            initial={{ opacity: 0, y: 18 }}
            animate={{ opacity: 1, y: 0 }}
            transition={reduce ? { duration: 0 } : { delay: 0.85, duration: 0.7, ease: [0.16, 1, 0.3, 1] }}
          >
            <div className="bench">
              <span className="lbl">What we build</span>
              <div className="bench-set">
                {SPEC.map((s, i) => (
                  <motion.span
                    className="bench-chip"
                    key={s.id}
                    initial={{ opacity: 0, y: 8 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={reduce ? { duration: 0 } : { delay: 1.05 + i * 0.08, duration: 0.45 }}
                  >
                    {s.name}
                  </motion.span>
                ))}
              </div>
            </div>
          </motion.div>
        </div>

        <dl className="stats hf">
          {[
            ['5', 'Days to a fixed number and a date'],
            ['110%', 'Back if we miss that date'],
          ].map(([v, l]) => (
            <div key={l}>
              <dt>{v}</dt>
              <dd>{l}</dd>
            </div>
          ))}
        </dl>
      </div>
    </section>
  );
}
