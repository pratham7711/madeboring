'use client';

import React, { useState } from 'react';
import Ic from '@/components/Icons';

export default function ContactForm() {
  const [state, setState] = useState('idle');
  const [error, setError] = useState('');

  const onSubmit = async (e) => {
    e.preventDefault();
    if (state === 'sending') return;
    setState('sending');
    setError('');
    const data = Object.fromEntries(new FormData(e.currentTarget));
    try {
      const res = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      const out = await res.json();
      if (out.ok) setState('sent');
      else {
        setState('idle');
        setError(out.error || 'Sending failed. Try again in a minute.');
      }
    } catch {
      setState('idle');
      setError('Sending failed. Try again in a minute.');
    }
  };

  if (state === 'sent') {
    return (
      <div className="form-done" role="status">
        <Ic name="check" size={22} />
        <div>
          <strong>Received.</strong>
          <p>A real answer is on its way — worth building or not, roughly what it costs, and how long.</p>
        </div>
      </div>
    );
  }

  return (
    <form className="cform" onSubmit={onSubmit}>
      <input type="text" name="company_website" tabIndex="-1" autoComplete="off" aria-hidden="true" className="hp" />
      <div className="cform-row">
        <label>
          <span className="lbl">Name</span>
          <input name="name" type="text" required autoComplete="name" placeholder="Your name" />
        </label>
        <label>
          <span className="lbl">Email</span>
          <input name="email" type="email" required autoComplete="email" placeholder="you@company.com" />
        </label>
      </div>
      <label>
        <span className="lbl">What keeps breaking</span>
        <textarea
          name="message"
          required
          rows={4}
          placeholder="Two or three sentences is plenty. What is the thing, and how often does it bite?"
        />
      </label>
      <p className="cform-err" role="alert" aria-live="assertive" hidden={!error}>
        {error}
      </p>
      <button className="btn" type="submit" disabled={state === 'sending'}>
        <Ic name="arrow" size={16} />
        <span>{state === 'sending' ? 'Sending…' : 'Send it'}</span>
      </button>
    </form>
  );
}
