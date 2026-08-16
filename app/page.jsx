import React from 'react';
import Nav from '@/components/Nav';
import Crosshair from '@/components/Crosshair';
import Hero from '@/components/Hero';
import Logo from '@/components/Logo';
import Segments from '@/components/Segments';
import Reveal from '@/components/Reveal';
import Ic, { StackIc, hasStackIcon } from '@/components/Icons';
import ContactForm from '@/components/ContactForm';
import Glow from '@/components/Glow';
import StickyCta from '@/components/StickyCta';
import Carousel from '@/components/Carousel';
import { BrowserMock, ChatMock, DashMock, FlowMock, ReplyMock } from '@/components/Mocks';
import {
  UNIVERSAL,
  GROUPS,
  WEEK_ONE,
  OWNERSHIP,
  STACK,
  PRICING,
  OBJECTIONS,
  WARRANTY,
  CAPACITY,
  REPLY,
  LEAD,
} from '@/lib/content';
import { SCHEMA } from '@/lib/schema';

const WA = process.env.NEXT_PUBLIC_WHATSAPP || '';
const CAL = process.env.NEXT_PUBLIC_CAL || '';

export default function Page() {
  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(SCHEMA) }}
      />
      <Crosshair />
      <Glow />
      <Nav />
      <main>
        <Hero />

        <section className="sec" id="warranty">
          <div className="shell">
            <Reveal className="war" selector=".war-main, .war-terms" stagger={0.12}>
              <div className="war-main">
                <h2>
                  A working pilot on the date we commit to, or{' '}
                  <b>110% of your money back.</b>
                </h2>
                <p>{WARRANTY.body}</p>
                <dl className="term-run">
                  {WARRANTY.terms.map(([k, v, ic]) => (
                    <div key={k}>
                      <dt>
                        <Ic name={ic} size={15} />
                        {k}
                      </dt>
                      <dd>{v}</dd>
                    </div>
                  ))}
                </dl>
                <div className="war-cta">
                  <a className="btn" href="#contact">
                    <span>Start the pilot</span>
                  </a>
                  <span className="war-risk">Nothing is built before you agree the number.</span>
                </div>
              </div>
              <div className="war-terms">
                <BrowserMock />
                <span className="lbl">The agreed date</span>
              </div>
            </Reveal>
          </div>
        </section>

        <section className="sec pain-sec" id="pain">
          <div className="shell">
            <Reveal className="sec-head" selector=".rv">
              <span className="lbl rv">What it costs you</span>
              <h2 className="h2 rv">Five things quietly true in almost every business.</h2>
            </Reveal>
            <Reveal className="bento" selector=".bn" stagger={0.08} y={18}>
              {[
                [UNIVERSAL[0], <ChatMock key="c" />],
                [UNIVERSAL[2], <DashMock key="d" />],
              ].map(([u, mock]) => (
                <article className="bn bn-lg" key={u.n} data-glow>
                  <div className="bn-fig">{mock}</div>
                  <div className="bn-tx">
                    <h3>{u.pain}</h3>
                    <p className="stat">{u.stat}</p>
                    <a className="src" href={u.href} target="_blank" rel="noopener nofollow">
                      {u.src} ↗<em>{u.year}</em>
                    </a>
                  </div>
                </article>
              ))}
              {[UNIVERSAL[1], UNIVERSAL[3], UNIVERSAL[4]].map((u) => (
                <article className="bn bn-sm" key={u.n} data-glow>
                  <h3>{u.pain}</h3>
                  <p className="stat">{u.stat}</p>
                  <a className="src" href={u.href} target="_blank" rel="noopener nofollow">
                    {u.src} ↗<em>{u.year}</em>
                  </a>
                </article>
              ))}
            </Reveal>
          </div>
        </section>

        <section className="sec" id="you">
          <div className="shell">
            <Reveal className="sec-head" selector=".rv">
              <span className="lbl rv">Find yourself</span>
              <h2 className="h2 rv">Whatever size you are, the problem has a shape.</h2>
              <p className="lede rv">Pick the one that sounds like you.</p>
            </Reveal>
            <Segments />
            <div className="seg-cta">
              <a className="btn" href="#contact">
                <span>Start the pilot</span>
              </a>
              <span>Or just ask. Hearing &ldquo;no&rdquo; is free.</span>
            </div>
          </div>
        </section>

        <section className="sec" id="build">
          <div className="shell">
            <Reveal className="sec-head" selector=".rv">
              <h2 className="h2 rv">We start with whatever can run itself.</h2>
            </Reveal>
            <Reveal className="build-split" selector=".bl" stagger={0.12} y={18}>
              <figure className="bl build-fig">
                <FlowMock />
                <figcaption className="lbl">
                  The shape of almost every job. Five steps, unwatched
                </figcaption>
              </figure>
            </Reveal>
            <Reveal className="cap-set" selector=".cap" stagger={0.1} y={18}>
              {GROUPS.map((g) => (
                <div className={`cap${g.lead ? ' cap-lead' : ''}`} key={g.title}>
                  <h3>
                    {g.title}
                    {g.lead ? <span className="tag">We lead here</span> : null}
                  </h3>
                  <ul>
                    {g.items.map(([it]) => (
                      <li key={it}>{it}</li>
                    ))}
                  </ul>
                  <a className="more-link" href="#contact">
                    +{g.more} more. Ask about yours
                  </a>
                </div>
              ))}
            </Reveal>
          </div>
        </section>

        <section className="sec" id="ownership">
          <div className="shell">
            <Reveal className="sec-head" selector=".rv">
              <h2 className="h2 rv">You keep the keys. Written down, not implied.</h2>
              <p className="lede rv">The most expensive system is one you cannot change yourself.</p>
            </Reveal>
            <Carousel label="What you own" className="own-car">
              {OWNERSHIP.map(([k, v, ic]) => (
                <article className="own-slide" key={k}>
                  <Ic name={ic} size={22} />
                  <h3>{k}</h3>
                  <p>{v}</p>
                </article>
              ))}
            </Carousel>
            <Reveal className="own-note" selector=".ownote-tx, .chips" stagger={0.1} y={14}>
              <div className="ownote-tx">
                <span className="lbl">Nothing exotic</span>
                <p>
                  Standard tools with large hiring pools. If you replace us, you are hiring for
                  these, not for us.
                </p>
              </div>
              <div className="chips">
                {STACK.map((s) => (
                  <span className="chip" key={s}>
                    {hasStackIcon(s) ? <StackIc name={s} /> : null}
                    {s}
                  </span>
                ))}
              </div>
            </Reveal>
          </div>
        </section>

        <section className="sec" id="engagement">
          <div className="shell">
            <Reveal className="sec-head" selector=".rv">
              <h2 className="h2 rv">Five days to a number and a date. Then we build to it.</h2>
            </Reveal>
            <Reveal className="tl" selector=".tl-item" stagger={0.09} y={16}>
              {WEEK_ONE.map((w) => (
                <div className="tl-item" key={w.d}>
                  <div className="tl-mark">
                    <Ic name={w.icon} size={17} />
                  </div>
                  <span className="lbl">{w.d}</span>
                  <h3>{w.t}</h3>
                </div>
              ))}
            </Reveal>
            <Reveal className="price" selector=".price-fig, .price-side" stagger={0.12} y={16}>
              <div className="price-fig">
                <span className="lbl">{PRICING.lbl}</span>
                <strong className="price-head">{PRICING.head}</strong>
              </div>
              <div className="price-side">
                <ul className="price-terms">
                  {PRICING.terms.map((t) => (
                    <li key={t}>
                      <Ic name="check" size={16} />
                      <span>{t}</span>
                    </li>
                  ))}
                </ul>
                <p className="price-after">{PRICING.after}</p>
                <a className="btn" href="#contact">
                  <span>Get the number and the date</span>
                </a>
              </div>
            </Reveal>
          </div>
        </section>

        <section className="sec" id="objections">
          <div className="shell">
            <Reveal className="sec-head" selector=".rv">
              <span className="lbl rv">Straight answers</span>
              <h2 className="h2 rv">The things you are already thinking.</h2>
            </Reveal>
            <div className="obj-who">
              <span className="lbl">Who you are dealing with</span>
              <p>
                <strong>{LEAD.name}</strong>, {LEAD.title}. {LEAD.line}{' '}
                <a className="uline" href={LEAD.href} target="_blank" rel="noopener">
                  {LEAD.hrefLabel} ↗
                </a>
              </p>
            </div>
            <Reveal className="obj-grid" selector=".obj" stagger={0.09} y={18}>
              {OBJECTIONS.map((o) => (
                <div className="obj" key={o.q}>
                  <h3>{o.q}</h3>
                  <p>{o.a}</p>
                </div>
              ))}
            </Reveal>
          </div>
        </section>

        <section className="sec" id="contact">
          <div className="shell">
            <div className="contact-grid">
              <Reveal className="cta" selector=".rv">
                <h2 className="h2 rv">Tell us the thing that keeps breaking.</h2>
                <p className="lede rv">
                  Worth building or not, what it costs, how long. You get all three back.
                </p>
                <div className="rv">
                  <ContactForm />
                </div>
                <dl className="cta-terms rv">
                  <div>
                    <dt>
                      <Ic name="mail" size={15} />
                      What happens next
                    </dt>
                    <dd>{REPLY}</dd>
                  </div>
                  <div>
                    <dt>
                      <Ic name="clock" size={15} />
                      Capacity
                    </dt>
                    <dd>{CAPACITY}</dd>
                  </div>
                </dl>
                {(WA || CAL) && (
                  <div className="chan rv">
                    <span className="lbl">Or skip the form</span>
                    <div className="chan-row">
                      {WA && (
                        <a
                          className="chan-btn"
                          href={`https://wa.me/${WA}?text=${encodeURIComponent(
                            'Hi, something in my business keeps breaking.'
                          )}`}
                          target="_blank"
                          rel="noopener"
                        >
                          <StackIc name="WhatsApp" size={17} />
                          <span>WhatsApp</span>
                        </a>
                      )}
                      {CAL && (
                        <a className="chan-btn" href={`https://cal.com/${CAL}`} target="_blank" rel="noopener">
                          <StackIc name="Cal.com" size={17} />
                          <span>Book a call</span>
                        </a>
                      )}
                    </div>
                  </div>
                )}
              </Reveal>
              <Reveal className="contact-panel" selector=".rep-body" as="figure">
                <ReplyMock />
              </Reveal>
            </div>
          </div>
        </section>
      </main>

      <StickyCta />

      <footer className="foot">
        <div className="shell">
          <div className="foot-grid">
            <div>
              <div className="brand">
                <Logo play="still" className="brandmark foot-mark" />
              </div>
              <p className="foot-about">
                AI and software, boringly simple. Delhi, working worldwide. Founded by{' '}
                <a className="uline" href="https://prathamsharma.in" target="_blank" rel="noopener">
                  Pratham Sharma
                </a>
                .
              </p>
              <address className="foot-addr">
                TA-327, II Floor, Tughlakabad Extension
                <br />
                Main Okhla Road, New Delhi 110019
                <br />
                <span className="foot-gst">GSTIN 07AAIHD6941F1ZB</span>
              </address>
            </div>
            <div>
              <h3>Site</h3>
              <ul>
                <li><a href="#pain">Problems</a></li>
                <li><a href="#you">Your situation</a></li>
                <li><a href="#build">What we build</a></li>
                <li><a href="#ownership">Ownership</a></li>
                <li><a href="#engagement">How it works</a></li>
                <li><a href="#warranty">Warranty</a></li>
              </ul>
            </div>
            <div>
              <h3>Elsewhere</h3>
              <ul>
                <li>
                  <a href="https://www.linkedin.com/in/pratham-sharma-a555b8207" target="_blank" rel="noopener">
                    LinkedIn
                  </a>
                </li>
                <li>
                  <a href="https://prathamsharma.in" target="_blank" rel="noopener">
                    prathamsharma.in
                  </a>
                </li>
                <li><a href="#contact">Start the pilot</a></li>
              </ul>
            </div>
          </div>
          <div className="foot-base">
            <span>© {new Date().getFullYear()} made boring</span>
            <span>Built to be forgotten about</span>
          </div>
        </div>
      </footer>
    </>
  );
}
