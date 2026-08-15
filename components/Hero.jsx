'use client';

import React, { useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import { motion, useReducedMotion } from 'motion/react';
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
        <video
          className="hero-film-layer"
          src="/video/nobody.mp4"
          poster="/video/nobody-poster.jpg"
          autoPlay
          muted
          loop
          playsInline
          preload="auto"
          aria-hidden="true"
        />
        <div className="grid-lines" aria-hidden="true" />
        <div className="veil veil-film" aria-hidden="true" />
      </div>
      <div className="shell hero-in">
        <div className="sheet-top hf">
          <span className="lbl accent">AI &amp; software studio</span>
        </div>

        <h1 className="display">
          <span className="rl">
            <span>{'We make '}</span>
          </span>
          <span className="rl">
            <span>
              it <em>boring</em>
            </span>
          </span>
        </h1>

        <div className="hero-grid">
          <div>
            <p className="lede hf">
              Interesting software pages you at 3am. We build the other kind &mdash; and you keep
              every key.
            </p>
            <div className="hero-cta hf">
              <a className="btn" href="#contact">
                <span>Start the pilot</span>
              </a>
              <a className="btn-txt" href="#contact">
                <span>Or just tell us what keeps breaking →</span>
              </a>
            </div>
            <p className="hero-risk hf">
              Hearing &ldquo;no&rdquo; is free · <b>One reply, from Pratham, usually the same day</b>
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
