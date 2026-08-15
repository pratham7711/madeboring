import React from 'react';
import { UI, UI_VIEW, STACK, STACK_VIEW } from '@/lib/icon-paths';

export default function Ic({ name, size = 18, className = 'ic' }) {
  const d = UI[name];
  if (!d) return null;
  return (
    <svg
      className={className}
      width={size}
      height={size}
      viewBox={`0 0 ${UI_VIEW} ${UI_VIEW}`}
      fill="currentColor"
      aria-hidden="true"
      focusable="false"
    >
      {d.map((p, i) => (
        <path key={i} d={p} />
      ))}
    </svg>
  );
}

export function StackIc({ name, size = 15 }) {
  const d = STACK[name];
  if (!d) {
    return (
      <svg
        className="stack-ic stack-ic-none"
        width={size}
        height={size}
        viewBox="0 0 24 24"
        fill="currentColor"
        aria-hidden="true"
        focusable="false"
      >
        <circle cx="12" cy="12" r="4.5" />
      </svg>
    );
  }
  return (
    <svg
      className="stack-ic"
      width={size}
      height={size}
      viewBox={`0 0 ${STACK_VIEW} ${STACK_VIEW}`}
      fill="currentColor"
      aria-hidden="true"
      focusable="false"
    >
      <path d={d} />
    </svg>
  );
}

export const hasStackIcon = (name) => Boolean(STACK[name]);
