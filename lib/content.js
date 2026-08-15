export const SPEC = [
  { id: 'MB-01', name: 'AI workflows & agents' },
  { id: 'MB-02', name: 'Custom apps & dashboards' },
  { id: 'MB-03', name: 'Integrations & APIs' },
  { id: 'MB-04', name: 'Audits & rescues' },
];

export const UNIVERSAL = [
  {
    n: '01',
    pain: 'You found out three days later. The customer told you.',
    stat: '23% never answer an inbound lead.',
    src: 'Harvard Business Review',
    year: '2011',
    href: 'https://hbr.org/2011/03/the-short-life-of-online-sales-leads',
  },
  {
    n: '02',
    pain: 'You pay people for judgment. They spend the day on copy-paste.',
    stat: 'Nine hours a week retyping data.',
    src: 'Parseur / QuestionPro',
    year: '2025 · n=500',
    href: 'https://parseur.com/blog/manual-data-entry-report',
  },
  {
    n: '03',
    pain: 'Nobody can say how the business is doing without building a report first.',
    stat: '72% lose half a day a month collating.',
    src: 'Wellingtone',
    year: '2026',
    href: 'https://wellingtone.co.uk/state-of-project-management/',
  },
  {
    n: '04',
    pain: 'The integration between your two systems is a person with a spreadsheet.',
    stat: 'Under 29% of business apps connect.',
    src: 'MuleSoft',
    year: '2021',
    href: 'https://resources.enterprisetalk.com/ebook/Mulesoft-50994-EN-1.pdf',
  },
  {
    n: '05',
    pain: 'Everyone says you are behind on AI. Nobody says what to do on Monday.',
    stat: '46% use AI. 7% have integrated it.',
    src: 'US Federal Reserve',
    year: '2026',
    href: 'https://www.fedsmallbusiness.org/reports/survey/2026/2026-report-on-employer-firms',
  },
];

export const SEGMENTS = [
  {
    key: 'solo',
    label: 'Solo / small vendor',
    sub: 'Shop, clinic, studio, independent seller',
    scale: '1–4 people',
    pains: [
      {
        quote: 'Someone messaged us at 9pm and I saw it two days later.',
        cost: 'The enquiry does not wait for office hours. It goes elsewhere.',
        src: null,
        year: null,
        href: null,
        fix: 'WhatsApp that answers fees.',
      },
      {
        quote: 'I wrote it in the diary and two people turned up for the same slot.',
        cost: '12.9% of appointments missed. Mostly forgotten.',
        src: 'British Journal of General Practice',
        year: '2021',
        href: 'https://bjgp.org/content/71/707/e406',
        fix: 'Booking that cannot double-book.',
      },
      {
        quote: 'Chasing people for money makes me feel like a beggar.',
        cost: 'Late payment is the default. You do the asking.',
        src: null,
        href: null,
        fix: 'Reminders that escalate on schedule.',
      },
      {
        quote: 'The whole business is in one phone.',
        cost: 'One lost handset erases the customers and the ledger.',
        src: null,
        href: null,
        fix: 'A web app that opens on any phone.',
      },
    ],
  },
  {
    key: 'freelancer',
    label: 'Freelancer / professional',
    sub: 'Designer, consultant, lawyer, CA, doctor',
    scale: 'Selling your own hours',
    pains: [
      {
        quote: 'I do the actual work at night because the day goes on admin.',
        cost: '2.9 billable hours in an eight-hour day.',
        src: 'Clio Legal Trends',
        year: '2024',
        href: 'https://www.clio.com/blog/how-to-calculate-utilization-rate/',
        fix: 'Intake to proposal to invoice, one flow.',
      },
      {
        quote: 'The invoice went out in March. It is now June.',
        cost: '$5,968 average loss to non-payment.',
        src: 'Freelancers Union',
        year: '2017',
        href: 'https://www.onlabor.org/wp-content/uploads/2017/05/FU_NonpaymentReport_r3.pdf',
        fix: 'Chasing that runs without you.',
      },
      {
        quote: 'They asked for one more small change. Then another.',
        cost: '42% work on a verbal agreement.',
        src: 'Freelancers Union',
        year: '2017',
        href: 'https://www.onlabor.org/wp-content/uploads/2017/05/FU_NonpaymentReport_r3.pdf',
        fix: 'Every request lands logged.',
      },
      {
        quote: 'Every project starts from a blank page.',
        cost: 'The same proposal, rewritten from scratch each time.',
        src: null,
        href: null,
        fix: 'Retrieval over your own past work.',
      },
    ],
  },
  {
    key: 'small',
    label: 'Small business',
    sub: 'Agency, D2C brand, broker, lab, manufacturer',
    scale: '5–50 people',
    pains: [
      {
        quote: 'Leads come in from six places and nobody owns them.',
        cost: 'Reaching customers is the #1 operational challenge firms report.',
        src: 'US Federal Reserve',
        year: '2026',
        href: 'https://www.fedsmallbusiness.org/reports/survey/2026/2026-report-on-employer-firms',
        fix: 'Six inboxes become one pipeline.',
      },
      {
        quote: 'Everything important is in one person’s head or one spreadsheet.',
        cost: 'One person, one spreadsheet, no backup.',
        src: null,
        href: null,
        fix: 'The process moves out of one head.',
      },
      {
        quote: 'We bought the software and nobody uses it.',
        cost: 'Paid for, rolled out, and quietly worked around.',
        src: null,
        year: null,
        href: null,
        fix: 'The tool you already pay for, actually used.',
      },
      {
        quote: 'I find out something went wrong when the customer complains.',
        cost: 'Nothing watches for the thing that did not happen.',
        src: null,
        href: null,
        fix: 'Dashboards that show only what is stuck.',
      },
    ],
  },
  {
    key: 'mid',
    label: 'Mid-market / scale-up',
    sub: 'SaaS, logistics, healthcare group, ecommerce',
    scale: '50–500 people',
    pains: [
      {
        quote: 'Ops headcount grows one-for-one with revenue.',
        cost: 'Every new customer adds a fraction of a person.',
        src: null,
        href: null,
        fix: 'Automate the repeat path.',
      },
      {
        quote: 'Every number in the board deck is assembled by hand and I don’t fully trust it.',
        cost: 'Half a day a month, assembled by hand, trusted by nobody.',
        src: null,
        year: null,
        href: null,
        fix: 'The board pack builds from source systems.',
      },
      {
        quote: 'We ran an AI pilot last year and nothing came of it.',
        cost: 'Most pilots die at proof of concept.',
        src: 'Gartner',
        year: '2024',
        href: 'https://campustechnology.com/articles/2024/08/06/gartner-predicts-wave-of-abandoned-ai-projects.aspx',
        fix: 'One AI idea, shipped, not piloted.',
      },
      {
        quote: 'Support answers the same forty questions four thousand times a month.',
        cost: 'Headcount, plus the attrition of the people doing it.',
        src: null,
        href: null,
        fix: 'Deflect the forty.',
      },
    ],
  },
  {
    key: 'enterprise',
    label: 'Enterprise / MNC',
    sub: 'Multiple systems, legacy, compliance, procurement',
    scale: '500+ people',
    pains: [
      {
        quote: 'Nothing talks to anything, and the thing connecting them is a person.',
        cost: 'Hundreds of applications. A minority of them connected.',
        src: null,
        year: null,
        href: null,
        fix: 'The two systems your vendor called impossible.',
      },
      {
        quote: 'The system that runs this was written by someone who left in 2011.',
        cost: '80% of IT budget keeps the lights on.',
        src: 'US GAO',
        year: '2025',
        href: 'https://files.gao.gov/reports/GAO-25-107795/index.html',
        fix: 'We wrap the system nobody will touch.',
      },
      {
        quote: 'Every AI initiative dies in security, legal or procurement.',
        cost: 'Months elapsed, budget line dead.',
        src: null,
        href: null,
        fix: 'Runs in your cloud.',
      },
      {
        quote: 'The vendor built it, then left, and nobody can change it.',
        cost: 'A licence to access your own system.',
        src: null,
        href: null,
        fix: 'You own the repo.',
      },
    ],
  },
];

export const GROUPS = [
  {
    title: 'Automation & AI',
    icon: 'bolt',
    lead: true,
    items: [
      ['AI workflow automation', 'bolt'],
      ['LLM & RAG integration', 'db'],
      ['Chatbots & voice agents', 'chat'],
      ['n8n · Zapier · Make.com', 'nodes'],
    ],
    more: 3,
  },
  {
    title: 'Software & systems',
    icon: 'box',
    items: [
      ['Custom web applications', 'code'],
      ['Integrations & APIs', 'plug'],
      ['Dashboards & reporting', 'chart'],
      ['CRM builds', 'users'],
    ],
    more: 5,
  },
  {
    title: 'Web & everything else',
    icon: 'globe',
    items: [
      ['Landing pages', 'layout'],
      ['E-commerce & payments', 'cart'],
      ['WordPress plugins', 'layers'],
      ['Game & interactive', 'pad'],
    ],
    more: 4,
  },
];

export const WEEK_ONE = [
  { d: 'DAY 1', icon: 'phone', t: 'A call, then a written summary' },
  { d: 'DAY 2–4', icon: 'doc', t: 'A spec, including what is out of scope' },
  { d: 'DAY 5', icon: 'hash', t: 'A fixed number and a date' },
  { d: 'ONGOING', icon: 'play', t: 'A demo every Friday' },
];

export const OWNERSHIP = [
  ['Repository', 'Your GitHub org.', 'branch'],
  ['Infrastructure', 'Your cloud, your keys.', 'server'],
  ['Intellectual property', 'Assigns each milestone.', 'seal'],
  ['Documentation', 'For whoever replaces us.', 'book'],
  ['AI usage', 'Logged, per call.', 'eye'],
  ['Exit', 'Any milestone. Keep it all.', 'key'],
];

export const PRICING = {
  lbl: 'How we price',
  head: 'Fixed, not hourly.',
  terms: [
    'You see the number and the date on day five, before anything is built.',
    'Both agreed in writing, then the clock starts.',
    'No hourly billing. No change-order surprises.',
    '110% back if we miss the date.',
  ],
  after:
    'Every engagement after the pilot is quoted the same way — one number, one date, in writing.',
};

export const OBJECTIONS = [
  {
    q: 'How big are you?',
    a: 'Small on purpose. made boring is led by Pratham Sharma, our founder and CEO, and he is on every engagement from the first call to handover — not an account manager relaying to people you never meet. When a build needs more hands we bring in senior specialists. Never juniors learning on your budget.',
  },
  {
    q: 'Where are the case studies?',
    a: 'made boring opened in August 2026. There is no client work to show yet and we are not going to invent any. That is exactly why the guarantee exists — we are asking you to go first, so we carry the risk instead of you.',
  },
  {
    q: 'Is a fixed date realistic?',
    a: 'It is realistic because we set it after the scope, not before. Five days of specification, then a number and a date you can hold us to. The pilot is not sized to finish everything — it is sized to prove the thing works on your data, which is the part most projects never reach.',
  },
  {
    q: 'Can you clear our procurement?',
    a: 'We sign your NDA, your MSA and your DPA. The work runs in your cloud under your keys, so there is no data-residency question to escalate. If legal or security need something specific, raise it on the first call — cheaper to find out on day one than on day thirty.',
  },
  {
    q: 'What if you disappear mid-build?',
    a: 'You hold the repository, the cloud account and the keys from day one, and the documentation is written for whoever picks it up next. Nothing we build needs us to keep running. That is the point of building it boring.',
  },
  {
    q: 'You are in Delhi. We are not.',
    a: 'Most of the work is written down, not spoken. Calls run in your hours. The commitment is the same from anywhere — and so is the refund.',
  },
];

export const STACK = [
  'TypeScript', 'React', 'Next.js', 'Node.js', 'Python', 'PostgreSQL', 'LangChain',
  'OpenAI', 'Anthropic', 'n8n', 'Zapier', 'Make.com', 'AWS', 'Vercel', 'Docker',
];

export const WARRANTY = {
  body: 'Not a slide deck. Something you open yourself, on a date fixed in writing before a line is built.',
  terms: [
    ['THE DATE', 'Fixed with the price, in writing.', 'clock'],
    ['CLOCK STARTS', 'The day you agree the scope.', 'play'],
    ['DELIVERED MEANS', 'Running on your data.', 'check'],
    ['WHO DECIDES', 'You do. No appeal.', 'eye'],
    ['IF WE MISS', '110% back within 7 days.', 'refund'],
    ['WHAT YOU KEEP', 'Everything, refund or not.', 'key'],
  ],
};

export const CAPACITY =
  'We run a small number of pilots at a time. Ask what the next open slot is.';

export const REPLY =
  'One reply, from Pratham, usually the same day. If it is not work for us, we say so and tell you who it is for.';

export const LEAD = {
  name: 'Pratham Sharma',
  title: 'Founder & CEO',
  line: 'on every engagement, from the first call to handover.',
  href: 'https://prathamsharma.in',
  hrefLabel: 'prathamsharma.in',
};
