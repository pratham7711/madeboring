import React from 'react';

export function ChatMock() {
  return (
    <div className="mock mock-chat" aria-hidden="true">
      <div className="mk-bar">
        <span className="mk-dot" />
        21:04
      </div>
      <div className="mk-body">
        <div className="bub bub-in">Open Sunday? What does it cost?</div>
        <div className="bub bub-out">Sundays 10–4. First session $60.</div>
        <div className="bub bub-in">Book me 11am.</div>
        <div className="bub bub-out">Done. Confirmation sent.</div>
      </div>
    </div>
  );
}

export function FlowMock() {
  return (
    <div className="mock mock-flow" aria-hidden="true">
      <div className="mk-bar">
        <span className="mk-dot" />
        Lead intake
      </div>
      <div className="fl">
        <div className="fl-col">
          <span className="fl-node">Form</span>
          <span className="fl-node">Inbox</span>
        </div>
        <span className="fl-link" />
        <div className="fl-col">
          <span className="fl-node">Classify</span>
          <span className="fl-node">Enrich</span>
        </div>
        <span className="fl-link" />
        <div className="fl-col">
          <span className="fl-node fl-hot">Route</span>
        </div>
      </div>
    </div>
  );
}

export function DashMock() {
  const bars = [38, 52, 30, 64, 48, 72, 41, 58, 88, 35, 61, 44];
  return (
    <div className="mock mock-dash" aria-hidden="true">
      <div className="mk-bar">
        <span className="mk-dot" />
        Exceptions
      </div>
      <div className="mk-figures">
        <div>
          <strong>3</strong>
          <span>stuck</span>
        </div>
      </div>
      <div className="mk-bars">
        {bars.map((h, i) => (
          <i key={i} style={{ height: `${h}%` }} className={h > 80 ? 'hot' : undefined} />
        ))}
      </div>
    </div>
  );
}

export function BrowserMock() {
  const bars = [42, 61, 35, 74, 55, 83, 48, 66];
  return (
    <div className="brw" aria-hidden="true">
      <div className="brw-bar">
        <span className="brw-dots">
          <i />
          <i />
          <i />
        </span>
        <span className="brw-url">yourco.app / ops</span>
      </div>
      <div className="brw-body">
        <div className="brw-side">
          <span className="brw-nav on">Queue</span>
          <span className="brw-nav">Exceptions</span>
          <span className="brw-nav">Sources</span>
          <span className="brw-nav">Log</span>
        </div>
        <div className="brw-main">
          <div className="brw-kpis">
            <div className="brw-kpi">
              <strong>1,204</strong>
              <span className="brw-lab">processed</span>
            </div>
            <div className="brw-kpi">
              <strong>3</strong>
              <span className="brw-lab">stuck</span>
            </div>
          </div>
          <div className="brw-chart">
            {bars.map((h, i) => (
              <i key={i} style={{ height: `${h}%` }} className={h > 80 ? 'hot' : undefined} />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export function ReplyMock() {
  return (
    <div className="brw rep" aria-hidden="true">
      <div className="brw-bar">
        <span className="brw-dots">
          <i />
          <i />
          <i />
        </span>
        <span className="brw-url">re: your enquiry</span>
      </div>
      <div className="rep-body">
        <span className="rep-from">made boring</span>
        <p>Read it. Two of the three are worth building.</p>
        <p>The third one your CRM already does — I will show you where.</p>
        <p className="rep-hot">Fixed number and a date on Friday.</p>
        <span className="rep-sig">— Pratham</span>
      </div>
    </div>
  );
}
