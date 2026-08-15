const AI_SEARCH_CRAWLERS = ['GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot', 'PerplexityBot'];

export default function robots() {
  return {
    rules: [
      { userAgent: '*', allow: '/' },
      ...AI_SEARCH_CRAWLERS.map((userAgent) => ({ userAgent, allow: '/' })),
    ],
    sitemap: 'https://madeboring.com/sitemap.xml',
    host: 'https://madeboring.com',
  };
}
