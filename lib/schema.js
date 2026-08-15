import { SPEC } from '@/lib/content';

const SITE = 'https://madeboring.com';
const LINKEDIN = 'https://www.linkedin.com/in/pratham-sharma-a555b8207';
const PORTFOLIO = 'https://prathamsharma.in';

const DESC =
  'AI workflow automation, LLM and RAG integration, custom software, dashboards and integrations. A working pilot on the date we commit to, or 110% of your money back.';

export const SCHEMA = {
  '@context': 'https://schema.org',
  '@graph': [
    {
      '@type': 'ProfessionalService',
      '@id': `${SITE}/#organization`,
      name: 'made boring',
      alternateName: 'madeboring.com',
      url: SITE,
      logo: { '@type': 'ImageObject', url: `${SITE}/icon.svg` },
      image: `${SITE}/og.png`,
      description: DESC,
      slogan: 'We make it boring.',
      foundingDate: '2026-08',
      founder: { '@id': `${SITE}/#pratham` },
      address: {
        '@type': 'PostalAddress',
        addressLocality: 'Delhi',
        addressCountry: 'IN',
      },
      areaServed: { '@type': 'Place', name: 'Worldwide' },
      knowsAbout: [
        'AI workflow automation',
        'Large language model integration',
        'Retrieval augmented generation',
        'Custom web application development',
        'Systems integration',
        'Business intelligence dashboards',
        'Process automation',
      ],
      sameAs: [LINKEDIN, PORTFOLIO],
      hasOfferCatalog: {
        '@type': 'OfferCatalog',
        name: 'What we build',
        itemListElement: SPEC.map((s) => ({
          '@type': 'Offer',
          itemOffered: { '@type': 'Service', name: s.name, provider: { '@id': `${SITE}/#organization` } },
        })),
      },
    },
    {
      '@type': 'Person',
      '@id': `${SITE}/#pratham`,
      name: 'Pratham Sharma',
      jobTitle: 'Founder',
      url: PORTFOLIO,
      sameAs: [LINKEDIN, PORTFOLIO],
      worksFor: { '@id': `${SITE}/#organization` },
    },
    {
      '@type': 'WebSite',
      '@id': `${SITE}/#website`,
      url: SITE,
      name: 'made boring',
      description: DESC,
      publisher: { '@id': `${SITE}/#organization` },
      inLanguage: 'en',
    },
    {
      '@type': 'WebPage',
      '@id': `${SITE}/#webpage`,
      url: SITE,
      name: 'made boring — AI and software, boringly simple',
      description: DESC,
      isPartOf: { '@id': `${SITE}/#website` },
      about: { '@id': `${SITE}/#organization` },
      inLanguage: 'en',
    },
  ],
};
