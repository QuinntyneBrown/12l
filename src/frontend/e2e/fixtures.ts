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

export const unverifiedMarcus: MemberFixture = { ...marcus, emailVerified: false };

/** GET /api/categories: the L2-011 table. */
export const categories = [
  {
    name: 'Shoes',
    subcategories: ['Sneakers', 'Boots', 'Dress shoes', 'Sandals'],
    acceptedSize: "Men's US 12",
    sizeLabel: 'US 12',
  },
  {
    name: 'Tops',
    subcategories: ['Shirts', 'T-shirts', 'Sweaters', 'Hoodies'],
    acceptedSize: "Men's L",
    sizeLabel: 'L',
  },
  { name: 'Outerwear', subcategories: ['Jackets', 'Coats'], acceptedSize: "Men's L", sizeLabel: 'L' },
  { name: 'Bottoms', subcategories: ['Pants', 'Shorts'], acceptedSize: "Men's L", sizeLabel: 'L' },
];

/** GET /api/selling/options. */
export const sellingOptions = {
  feePercent: 10,
  conditions: ['New with tags', 'New without tags', 'Used - Excellent', 'Used - Good', 'Used - Fair'],
  suggestedBrands: ['Nike', 'Adidas', 'New Balance'],
  maxPhotos: 8,
};

/** Answers the two catalogue calls the sell form needs. */
export async function serveCatalogue(page: Page): Promise<void> {
  await page.route('**/api/categories', (route) => route.fulfill({ json: categories }));
  await page.route('**/api/selling/options', (route) => route.fulfill({ json: sellingOptions }));
}

/** A listing as the listings endpoints return it to its seller. */
export function myListing(fields: Record<string, unknown>): Record<string, unknown> {
  const category = (fields['category'] as string) ?? 'Shoes';
  return {
    reference: 'L-10001',
    status: 'Draft',
    category,
    subcategory: null,
    size: category === 'Shoes' ? "Men's US 12" : "Men's L",
    title: null,
    description: null,
    brand: null,
    condition: null,
    flaws: null,
    price: null,
    shippingCost: null,
    createdAt: '2026-10-25T12:00:00Z',
    updatedAt: '2026-10-25T12:00:00Z',
    publishedAt: null,
    ...fields,
  };
}

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
 * Every test gets a page whose calls to 12L API are answered by fixtures (an auto fixture, so it
 * is in place before any beforeEach hook adds its own routes). The session endpoints
 * answer 401 (a visitor) unless a test signs a member in. Other unfixtured API calls are answered
 * 501 and recorded so a test can assert none happened.
 */
export const test = base.extend<{ unfixturedApiCalls: string[] }>({
  unfixturedApiCalls: [
    async ({ page }, use) => {
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
    { auto: true },
  ],
});

export { expect };
