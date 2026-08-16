'use client';

import React, { useEffect, useRef, useState } from 'react';

const STEPS = ['Received', 'Read', 'Matched', 'Filed'];

const SOURCES = [
  'Enquiry · WhatsApp',
  'Invoice #4471',
  'New lead · webform',
  'PO 22-118',
  'Refund request',
  'Enquiry · email',
  'Invoice #4472',
  'Delivery note',
  'Quote request',
  'Payment received',
];

const SEED = [
  { id: 0, src: SOURCES[0], step: 3, held: false },
  { id: 1, src: SOURCES[1], step: 2, held: false },
  { id: 2, src: SOURCES[2], step: 1, held: false },
  { id: 3, src: SOURCES[3], step: 1, held: false },
  { id: 4, src: SOURCES[4], step: 0, held: false },
];

const START = 1204;

export default function HeroConsole() {
  const [rows, setRows] = useState(SEED);
  const [done, setDone] = useState(START);
  const st = useRef(null);

  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    st.current = { rows: SEED, done: START, next: SEED.length };

    const id = setInterval(() => {
      const s = st.current;
      let completed = 0;
      const kept = [];

      for (const r of s.rows) {
        if (r.held) {
          kept.push({ ...r, held: false });
        } else if (r.step >= STEPS.length - 1) {
          completed += 1;
        } else {
          kept.push({ ...r, step: r.step + 1 });
        }
      }

      while (kept.length < SEED.length) {
        const i = s.next;
        s.next += 1;
        kept.push({
          id: i,
          src: SOURCES[i % SOURCES.length],
          step: 0,
          held: i % 7 === 3,
        });
      }

      s.rows = kept;
      s.done += completed;
      setRows(kept);
      setDone(s.done);
    }, 1400);

    return () => clearInterval(id);
  }, []);

  const held = rows.filter((r) => r.held).length;

  return (
    <div className="con" aria-hidden="true">
      <div className="con-bar">
        <span className="con-dots">
          <i />
          <i />
          <i />
        </span>
        <span className="con-url">yourco.app / queue</span>
        <span className="con-live">
          <i />
          live
        </span>
      </div>

      <div className="con-head">
        <span>Source</span>
        <span>Step</span>
      </div>

      <ul className="con-rows">
        {rows.map((r) => (
          <li className="con-row" key={r.id} data-held={String(r.held)}>
            <span className="con-src">{r.src}</span>
            <span className="con-step">
              <span className="con-track">
                {STEPS.map((s, i) => (
                  <i key={s} data-on={String(i <= r.step)} />
                ))}
              </span>
              <em>{r.held ? 'Held' : STEPS[r.step]}</em>
            </span>
          </li>
        ))}
      </ul>

      <div className="con-foot">
        <span>
          <b>{done.toLocaleString('en-US')}</b> processed today
        </span>
        <span className={held ? 'con-flag on' : 'con-flag'}>
          {held} waiting on you
        </span>
      </div>
    </div>
  );
}
