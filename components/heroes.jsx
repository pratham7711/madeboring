'use client';

import React, { useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import ShaderField from '@/components/ShaderField';
import { FRAG } from '@/components/shaders';

export const CONCEPTS = [
  {
    id: 'current',
    n: '01',
    name: 'Current',
    tech: 'WebGL flow field · full-bleed · cursor bends the current',
    thesis:
      'A field of drifting filaments, all moving one way. The motion is generated live, so it never repeats and never cuts — order without stillness.',
  },
  {
    id: 'grid',
    n: '02',
    name: 'Grid',
    tech: 'Dot-matrix shader · specimen panel · cursor lens',
    thesis:
      'A precision instrument on the bench. The dot grid breathes in slow interference waves; your cursor reads it like a loupe.',
  },
  {
    id: 'forge',
    n: '03',
    name: 'Forge',
    tech: 'Molten metaballs · rendered inside the letterforms',
    thesis:
      'The word is the window. Molten metal circulates inside the headline on orbits that never line up, so no frame ever repeats.',
  },
  {
    id: 'ember',
    n: '04',
    name: 'Ember',
    tech: 'Ember band · horizon seam · type rests on the edge',
    thesis:
      'Heat contained under a line. Smoke rises and sparks fire on their own clocks below the text, steady and controlled.',
  },
  {
    id: 'flatline',
    n: '05',
    name: 'Flatline',
    tech: 'Live trace · the chaos goes quiet at your cursor',
    thesis:
      'A live signal, jagged everywhere except where you are. Wherever your cursor rests, the trace settles flat — boring, delivered locally.',
  },
];

function useIntro(root) {
  useEffect(() => {
    const ctx = gsap.context(() => {
      const lines = root.current.querySelectorAll('.rl > span');
      if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        gsap.set([lines, '.hf'], { y: 0, yPercent: 0, opacity: 1 });
        return;
      }
      gsap.set(lines, { yPercent: 145 });
      gsap
        .timeline({ delay: 0.1 })
        .to(lines, { yPercent: 0, duration: 1.05, stagger: 0.08, ease: 'power4.out' })
        .fromTo(
          '.hf',
          { y: 15, opacity: 0 },
          { y: 0, opacity: 1, duration: 0.7, stagger: 0.08, ease: 'power2.out' },
          '-=0.5'
        );
    }, root);
    return () => ctx.revert();
  }, [root]);
}

function Eyebrow() {
  return (
    <div className="sheet-top hf">
      <span className="lbl">Software studio &middot; clients worldwide</span>
      <span className="lbl hide-sm">Rev 2026.08</span>
    </div>
  );
}

function Headline() {
  return (
    <h1 className="display">
      <span className="rl">
        <span>We make</span>
      </span>
      <span className="rl">
        <span>
          it <em>boring.</em>
        </span>
      </span>
    </h1>
  );
}

function Body() {
  return (
    <p className="lede hf">
      Interesting software pages you at 3am. We build the other kind &mdash; apps, AI workflows and
      dashboards that run the same way every time, and you keep every key.
    </p>
  );
}

function Cta() {
  return (
    <div className="hero-cta hf">
      <a className="btn" href="#contact">
        <span>Get a working pilot in 7 days</span>
      </a>
      <a className="btn btn-o" href="#warranty">
        <span>Or 110% of your money back</span>
      </a>
    </div>
  );
}

function Stats() {
  return (
    <dl className="stats hf">
      {[
        ['3+', 'Years shipping production'],
        ['16', 'Services under one roof'],
        ['0', 'Invented data, by design'],
      ].map(([v, l]) => (
        <div key={l}>
          <dt>{v}</dt>
          <dd>{l}</dd>
        </div>
      ))}
    </dl>
  );
}

export function HeroCurrent() {
  const root = useRef(null);
  useIntro(root);
  return (
    <section className="hero hero-settle" ref={root} id="top">
      <div className="hero-bg">
        <ShaderField frag={FRAG.current} />
        <div className="grid-lines" aria-hidden="true" />
        <div className="veil veil-radial" aria-hidden="true" />
      </div>
      <div className="shell hero-in">
        <Eyebrow />
        <Headline />
        <div className="hero-foot">
          <div>
            <Body />
            <Cta />
          </div>
          <Stats />
        </div>
      </div>
    </section>
  );
}

export function HeroGrid() {
  const root = useRef(null);
  useIntro(root);
  useEffect(() => {
    const el = root.current?.querySelector('.panel-media');
    if (!el) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    let raf;
    const onScroll = () => {
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(() => {
        const y = Math.min(160, window.scrollY * 0.12);
        el.style.transform = `translate3d(0, ${y}px, 0) scale(1.06)`;
      });
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => {
      window.removeEventListener('scroll', onScroll);
      cancelAnimationFrame(raf);
    };
  }, []);
  return (
    <section className="hero hero-machine" ref={root}>
      <div className="shell hero-in">
        <Eyebrow />
        <div className="split">
          <div className="split-type">
            <Headline />
            <Body />
            <Cta />
          </div>
          <figure className="panel">
            <div className="panel-media">
              <ShaderField frag={FRAG.grid} />
            </div>
            <figcaption className="lbl">Instrument &middot; MB-04 signal grid, live</figcaption>
          </figure>
        </div>
        <Stats />
      </div>
    </section>
  );
}

export function HeroForge() {
  const root = useRef(null);
  useIntro(root);
  return (
    <section className="hero hero-blueprint" ref={root}>
      <div className="hero-bg">
        <div className="grid-lines" aria-hidden="true" />
      </div>
      <div className="shell hero-in">
        <Eyebrow />
        <div className="type-window">
          <div className="tw-media" aria-hidden="true">
            <ShaderField frag={FRAG.forge} />
          </div>
          <h1 className="display tw-mask" aria-label="We make it boring.">
            <span aria-hidden="true">We make</span>
            <span aria-hidden="true">it boring.</span>
          </h1>
        </div>
        <div className="hero-foot">
          <div>
            <Body />
            <Cta />
          </div>
          <Stats />
        </div>
      </div>
    </section>
  );
}

export function HeroEmber() {
  const root = useRef(null);
  useIntro(root);
  return (
    <section className="hero hero-pour" ref={root}>
      <div className="shell hero-in">
        <Eyebrow />
        <Headline />
        <div className="hero-foot">
          <div>
            <Body />
            <Cta />
          </div>
          <Stats />
        </div>
      </div>
      <div className="band">
        <ShaderField frag={FRAG.ember} />
        <div className="veil veil-band" aria-hidden="true" />
        <div className="band-rule" aria-hidden="true" />
      </div>
    </section>
  );
}

export function HeroFlatline() {
  const root = useRef(null);
  useIntro(root);
  return (
    <section className="hero hero-flatline" ref={root}>
      <div className="hero-bg">
        <ShaderField frag={FRAG.flatline} />
        <div className="grid-lines" aria-hidden="true" />
      </div>
      <div className="shell hero-in">
        <Eyebrow />
        <Headline />
        <div className="hero-foot">
          <div>
            <Body />
            <Cta />
          </div>
          <Stats />
        </div>
        <span className="hint lbl hf">The trace goes quiet at your cursor</span>
      </div>
    </section>
  );
}

export const HEROES = {
  current: HeroCurrent,
  grid: HeroGrid,
  forge: HeroForge,
  ember: HeroEmber,
  flatline: HeroFlatline,
};
