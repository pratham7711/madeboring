'use client';

import React, { useEffect, useId, useRef } from 'react';
import { gsap } from 'gsap';
import { CustomEase } from 'gsap/CustomEase';
import { DrawSVGPlugin } from 'gsap/DrawSVGPlugin';
import { MorphSVGPlugin } from 'gsap/MorphSVGPlugin';
import { MARK } from '@/lib/mark';

if (typeof window !== 'undefined') {
  gsap.registerPlugin(CustomEase, DrawSVGPlugin, MorphSVGPlugin);
  if (!CustomEase.get('mbIo')) {
    CustomEase.create('mbIo', 'M0,0 C0.16,0.02 0.06,1 1,1');
    CustomEase.create('mbUnpack', 'M0,0 C0.18,0 0.12,1.03 0.48,1.008 C0.68,0.996 0.84,1 1,1');
  }
}

export default function Logo({ play = 'hover', className = 'brandmark', speed = 1 }) {
  const svg = useRef(null);
  const tl = useRef(null);
  const drawn = useRef(0);
  const uid = useId().replace(/[^a-zA-Z0-9]/g, '');
  const v = MARK.view;

  useEffect(() => {
    const el = svg.current;
    if (!el) return;
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    const ctx = gsap.context(() => {
      const pens = gsap.utils.toArray('.mb-pen', el);
      const open = el.querySelector('.mb-open');
      const dot = el.querySelector('.mb-dot');
      const movers = gsap.utils
        .toArray('.mb-g', el)
        .filter((n) => n.dataset.x !== undefined && !n.classList.contains('mb-m'))
        .sort((a, b) => +a.dataset.x - +b.dataset.x);

      const t = gsap.timeline({ paused: true });
      const len = pens.map((p) => p.getTotalLength());
      const total = len.slice(0, -1).reduce((a, c) => a + c, 0);
      let at = 0;

      pens.forEach((p, i) => {
        const d = i === pens.length - 1 ? 0.22 : (1.6 * len[i]) / total;
        t.fromTo(p, { drawSVG: '0%' }, { drawSVG: '100%', duration: d, ease: 'none' }, at);
        at += d + 0.06;
      });
      t.fromTo(open, { opacity: 0 }, { opacity: 1, duration: 0.22, ease: 'mbIo' }, at);

      const go = at + 0.3;
      const S = 0.05;
      movers.forEach((n, i) => {
        const start = go + i * S;
        if (+n.dataset.from !== +n.dataset.x)
          t.fromTo(
            n,
            { x: +n.dataset.from },
            { x: +n.dataset.x, duration: 0.9, ease: 'mbUnpack' },
            start
          );
        if (n.dataset.mid)
          t.fromTo(n, { opacity: 0 }, { opacity: 1, duration: 0.28, ease: 'mbIo' }, start + 0.1);
      });

      const h = el.getBoundingClientRect().height || 34;
      const restW = (h * (MARK.mbW + 140)) / v.h;
      const fullW = (h * v.w) / v.h;
      gsap.set(el, { width: restW });
      t.fromTo(el, { width: restW }, { width: fullW, duration: 0.95, ease: 'mbUnpack' }, go);

      const dt = go + movers.length * S;
      t.fromTo(
        dot,
        { x: MARK.dot.x, y: 0 },
        { x: MARK.dot.x + MARK.move.x, duration: 0.9, ease: 'mbUnpack' },
        dt
      )
        .to(dot, { y: MARK.move.y, duration: 0.56, ease: 'power3.out' }, dt + 0.3)
        .to(dot, { morphSVG: MARK.tittle, duration: 0.36, ease: 'mbIo' }, dt + 0.5);

      t.addLabel('drawn', at + 0.24);
      t.timeScale(speed);
      tl.current = t;
      drawn.current = at + 0.24;

      if (reduce) t.pause('drawn');
      else if (play === 'still') t.pause('drawn');
      else if (play === 'auto') t.play(0);
      else t.tweenFromTo(0, 'drawn');
    }, el);

    return () => ctx.revert();
  }, [play, speed]);

  const enter = () => {
    const t = tl.current;
    if (!t || play === 'still') return;
    if (t.time() < drawn.current - 0.01) return;
    t.tweenTo(t.duration(), { ease: 'none' });
  };

  const leave = () => {
    const t = tl.current;
    if (!t || play !== 'hover') return;
    if (t.time() < drawn.current - 0.01) return;
    t.tweenTo(drawn.current, { ease: 'none', duration: 0.5 });
  };

  const m = `pen-mb${uid}`;

  return (
    <svg
      ref={svg}
      className={className}
      viewBox={`${v.x} ${v.y} ${v.w} ${v.h}`}
      preserveAspectRatio="xMinYMid slice"
      role="img"
      aria-label="made boring"
      onMouseEnter={enter}
      onFocus={enter}
      onMouseLeave={leave}
      onBlur={leave}
    >
      <defs>
        <mask
          id={m}
          maskUnits="userSpaceOnUse"
          x="-600"
          y="-1600"
          width={MARK.wordW + 1400}
          height="3200"
        >
          <g
            transform="scale(1,-1)"
            fill="none"
            stroke="#fff"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            {MARK.pen.m.map((d, i) => (
              <path className="mb-pen" key={`m${i}`} strokeWidth={MARK.pen.mW} d={d} />
            ))}
            {MARK.pen.b.map((d, i) => (
              <path
                className="mb-pen"
                key={`b${i}`}
                strokeWidth={MARK.pen.bW}
                d={d}
                transform={`translate(${MARK.pen.bx},0)`}
              />
            ))}
            <path
              className="mb-pen"
              strokeWidth={MARK.pen.dotW}
              d={`M${MARK.pen.dotX - 0.5},${MARK.pen.dotY} L${MARK.pen.dotX + 0.5},${MARK.pen.dotY}`}
            />
          </g>
          <rect
            className="mb-open"
            x="-400"
            y="-1400"
            width={MARK.wordW + 900}
            height="2400"
            fill="#fff"
            opacity="0"
          />
        </mask>
      </defs>
      <g mask={`url(#${m})`}>
        <g transform="scale(1,-1)" fill="currentColor">
          {MARK.letters.map((l, i) => (
            <path
              key={i}
              className={`mb-g${l.core && i === 0 ? ' mb-m' : ''}`}
              data-x={l.x}
              data-from={l.from}
              data-mid={l.core ? undefined : '1'}
              transform={`translate(${l.from},0)`}
              style={l.core ? undefined : { opacity: 0 }}
              d={l.d}
            />
          ))}
          <path className="mb-dot" fill="var(--brand)" transform={`translate(${MARK.dot.x},0)`}
            d={MARK.dot.d} />
        </g>
      </g>
    </svg>
  );
}

export function Mark({ className = 'brandmark' }) {
  const v = MARK.markView;
  return (
    <svg
      className={className}
      viewBox={`${v.x} ${v.y} ${v.w} ${v.h}`}
      role="img"
      aria-label="made boring"
      fill="currentColor"
    >
      <g transform="scale(1,-1)">
        {MARK.mark.map((p, i) => (
          <path
            key={i}
            d={p.d}
            fill={i === 2 ? 'var(--brand)' : 'currentColor'}
            transform={`translate(${p.x},0)`}
          />
        ))}
      </g>
    </svg>
  );
}
