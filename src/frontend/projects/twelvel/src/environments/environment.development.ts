/** Development: ng serve proxies /api to TwelveL.Api (projects/twelvel/proxy.conf.json), so cookies stay same-origin. */
export const environment = {
  apiBaseUrl: '/api',
  analytics: { scriptUrl: 'https://analytics.12l.invalid/script.js', cookieNames: ['_12la'] },
};
