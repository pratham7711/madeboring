import { readFileSync, writeFileSync, existsSync } from 'node:fs';

const PH = 'node_modules/@phosphor-icons/core/assets/bold';
const SI = 'node_modules/simple-icons/icons';

const UI = {
  bolt: 'lightning',
  box: 'package',
  globe: 'globe-hemisphere-west',
  branch: 'git-branch',
  server: 'hard-drives',
  seal: 'seal-check',
  book: 'book-open-text',
  eye: 'eye',
  key: 'key',
  clock: 'clock-countdown',
  check: 'check-circle',
  refund: 'arrow-u-up-left',
  phone: 'phone-call',
  doc: 'file-text',
  hash: 'hash',
  play: 'play-circle',
  mail: 'envelope-simple',
  arrow: 'arrow-right',
  contrast: 'circle-half',
  chat: 'chat-teardrop-dots',
  db: 'database',
  nodes: 'tree-structure',
  code: 'code',
  plug: 'plugs-connected',
  chart: 'chart-bar',
  users: 'users-three',
  layout: 'layout',
  cart: 'shopping-cart-simple',
  layers: 'stack-simple',
  pad: 'game-controller',
  table: 'table',
};

const STACK = {
  TypeScript: 'typescript',
  React: 'react',
  'Next.js': 'nextdotjs',
  'Node.js': 'nodedotjs',
  Python: 'python',
  PostgreSQL: 'postgresql',
  LangChain: 'langchain',
  OpenAI: 'openai',
  Anthropic: 'anthropic',
  n8n: 'n8n',
  Zapier: 'zapier',
  'Make.com': 'make',
  AWS: 'amazonwebservices',
  Vercel: 'vercel',
  Docker: 'docker',
  WhatsApp: 'whatsapp',
  'Cal.com': 'caldotcom',
};

const paths = (svg) => [...svg.matchAll(/<path[^>]*\sd="([^"]+)"/g)].map((m) => m[1]);

const ui = {};
const missUi = [];
for (const [name, ph] of Object.entries(UI)) {
  const f = `${PH}/${ph}-bold.svg`;
  if (!existsSync(f)) { missUi.push(`${name} -> ${ph}`); continue; }
  const d = paths(readFileSync(f, 'utf8'));
  if (!d.length) { missUi.push(`${name} (no path)`); continue; }
  ui[name] = d;
}

const stack = {};
const missStack = [];
for (const [label, slug] of Object.entries(STACK)) {
  const f = `${SI}/${slug}.svg`;
  if (!existsSync(f)) { missStack.push(`${label} -> ${slug}`); continue; }
  const d = paths(readFileSync(f, 'utf8'));
  if (!d.length) { missStack.push(`${label} (no path)`); continue; }
  stack[label] = d[0];
}

writeFileSync(
  'lib/icon-paths.js',
  `export const UI_VIEW = 256;\nexport const UI = ${JSON.stringify(ui)};\nexport const STACK_VIEW = 24;\nexport const STACK = ${JSON.stringify(stack)};\n`
);

console.log('ui ok:', Object.keys(ui).length, 'of', Object.keys(UI).length);
if (missUi.length) console.log('UI MISSING:', missUi);
console.log('stack ok:', Object.keys(stack).length, 'of', Object.keys(STACK).length);
if (missStack.length) console.log('STACK MISSING:', missStack);
