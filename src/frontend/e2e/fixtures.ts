import { Page, Route, test as base, expect } from '@playwright/test';

/** The signed-in member as GET /api/auth/me returns it. */
export interface MemberFixture {
  displayName: string;
  email: string;
  emailVerified: boolean;
}

export const marcus: MemberFixture = {
  displayName: 'marcus_12',
  email: 'marcus.bell@example.com',
  emailVerified: true,
};

/** An RFC 9457 problem body as 12L API writes it (L2-068). */
export function problem(
  status: number,
  code: string,
  title: string,
  errors?: Record<string, { code: string; message: string }>,
): { status: number; contentType: string; body: string } {
  return {
    status,
    contentType: 'application/problem+json',
    body: JSON.stringify({ title, status, code, correlationId: '5c1d0e7a9b2f4c3d', errors }),
  };
}

/** Answers GET /api/auth/me and POST /api/auth/refresh with this member. */
export async function signInAs(page: Page, member: MemberFixture): Promise<void> {
  const answer = (route: Route) => route.fulfill({ json: member });
  await page.route('**/api/auth/me', answer);
  await page.route('**/api/auth/refresh', answer);
}

/**
 * Every test gets a page whose calls to 12L API are answered by fixtures. The session endpoints
 * answer 401 (a visitor) unless a test signs a member in. Other unfixtured API calls are answered
 * 501 and recorded so a test can assert none happened.
 */
export const test = base.extend<{ unfixturedApiCalls: string[] }>({
  unfixturedApiCalls: async ({ page }, use) => {
    const calls: string[] = [];
    await page.route('**/api/**', (route) => {
      calls.push(route.request().url());
      return route.fulfill({ status: 501, json: { error: 'no fixture for this request' } });
    });
    const visitor = (route: Route) => route.fulfill(problem(401, 'UNAUTHENTICATED', 'Sign in to continue'));
    await page.route('**/api/auth/me', visitor);
    await page.route('**/api/auth/refresh', visitor);
    await use(calls);
  },
});

export { expect };
