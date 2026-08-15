'use client';

import React, { useEffect, useRef, useState } from 'react';

export default function HeroFilm({ webm, mp4, poster }) {
  const ref = useRef(null);
  const [playing, setPlaying] = useState(true);

  useEffect(() => {
    const v = ref.current;
    if (!v) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      v.removeAttribute('autoplay');
      v.pause();
      setPlaying(false);
      return;
    }
    const play = () => v.play().then(() => setPlaying(true)).catch(() => setPlaying(false));
    if (v.readyState >= 2) play();
    else v.addEventListener('loadeddata', play, { once: true });
  }, []);

  const toggle = () => {
    const v = ref.current;
    if (!v) return;
    if (v.paused) v.play().then(() => setPlaying(true)).catch(() => {});
    else {
      v.pause();
      setPlaying(false);
    }
  };

  return (
    <div className="film">
      <video
        ref={ref}
        className="film-plate"
        poster={poster}
        muted
        loop
        playsInline
        preload="auto"
        aria-hidden="true"
      >
        <source src={webm} type="video/webm" />
        <source src={mp4} type="video/mp4" />
      </video>
      <button className="film-toggle" type="button" onClick={toggle} aria-pressed={!playing}>
        <span className="film-toggle-ic" aria-hidden="true">
          {playing ? (
            <svg viewBox="0 0 12 12" width="11" height="11">
              <rect x="2" y="1.5" width="2.6" height="9" rx="0.6" fill="currentColor" />
              <rect x="7.4" y="1.5" width="2.6" height="9" rx="0.6" fill="currentColor" />
            </svg>
          ) : (
            <svg viewBox="0 0 12 12" width="11" height="11">
              <path d="M3 1.6 10.2 6 3 10.4Z" fill="currentColor" />
            </svg>
          )}
        </span>
        <span className="film-toggle-tx">{playing ? 'Pause' : 'Play'}</span>
      </button>
    </div>
  );
}
