import { test as base, expect } from '@playwright/test';

/**
 * Every test gets a page whose calls to 12L API are answered by fixtures.
 * Unfixtured API calls are answered 501 and recorded so a test can assert none happened.
 */
export const test = base.extend<{ unfixturedApiCalls: string[] }>({
  unfixturedApiCalls: async ({ page }, use) => {
    const calls: string[] = [];
    await page.route('**/api/**', (route) => {
      calls.push(route.request().url());
      return route.fulfill({ status: 501, json: { error: 'no fixture for this request' } });
    });
    await use(calls);
  },
});

export { expect };
