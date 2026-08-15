import React from 'react';
import { IBM_Plex_Sans, IBM_Plex_Mono } from 'next/font/google';
import './globals.css';

const sans = IBM_Plex_Sans({
  subsets: ['latin'],
  weight: ['400', '500', '600'],
  variable: '--font-sans',
  display: 'swap',
});

const mono = IBM_Plex_Mono({
  subsets: ['latin'],
  weight: ['400', '500'],
  variable: '--font-mono',
  display: 'swap',
});

const DESC =
  'AI workflow automation, LLM integration, custom software, dashboards and rescues. A working pilot on the date we commit to, or 110% of your money back.';

export const metadata = {
  metadataBase: new URL('https://madeboring.com'),
  title: 'made boring — AI and software, boringly simple',
  description: DESC,
  keywords: [
    'AI workflow automation',
    'LLM integration',
    'RAG development',
    'n8n developer',
    'Zapier Make.com automation',
    'chatbot development',
    'custom software development',
    'dashboard development',
    'CRM development',
    'system integration',
    'automation audit',
  ],
  openGraph: {
    title: 'made boring — AI and software, boringly simple',
    description: DESC,
    url: 'https://madeboring.com',
    siteName: 'made boring',
    type: 'website',
    images: [{ url: '/og.png', width: 1200, height: 630, alt: 'made boring' }],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'made boring — AI and software, boringly simple',
    description: DESC,
    images: ['/og.png'],
  },
  alternates: { canonical: 'https://madeboring.com' },
};

export const viewport = { themeColor: '#17181a' };

const THEME_BOOT =
  "try{if(localStorage.getItem('mb-theme')==='paper')document.documentElement.dataset.theme='paper'}catch(e){}";

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={`${sans.variable} ${mono.variable}`} suppressHydrationWarning>
      <body>
        <script dangerouslySetInnerHTML={{ __html: THEME_BOOT }} />
        {children}
      </body>
    </html>
  );
}
