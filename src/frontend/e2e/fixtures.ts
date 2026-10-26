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
    photos: [],
    ...fields,
  };
}

/** An uploaded photo as POST /api/photo-uploads returns it; the thumbnail is the 400 px WebP. */
export function photo(id: string): Record<string, unknown> {
  const hash = id.padEnd(64, '0').replace(/[^0-9a-f]/g, 'a');
  return {
    id,
    url: `/photos/${hash}/400.webp`,
    width: 1200,
    height: 1600,
    versions: [400, 800, 1600].flatMap((size) =>
      ['WebP', 'Jpeg'].map((format) => ({
        size,
        width: Math.min(size, 1200),
        height: Math.round((1600 * Math.min(size, 1200)) / 1200),
        format,
        url: `/photos/${hash}/${size}.${format === 'WebP' ? 'webp' : 'jpg'}`,
      })),
    ),
  };
}

/** A 1x1 PNG served for every photo version. */
const PIXEL = Buffer.from(
  'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4nGNgYGD4DwABBAEAwS2OUAAAAABJRU5ErkJggg==',
  'base64',
);

/**
 * Answers POST /api/photo-uploads with photos p-1, p-2... in upload order, and serves every
 * photo version. Returns the names of the uploaded files.
 */
export async function servePhotoUploads(page: Page): Promise<string[]> {
  const uploaded: string[] = [];
  await page.route('**/api/photo-uploads', async (route) => {
    const name = /filename="([^"]+)"/.exec(route.request().postDataBuffer()?.toString('latin1') ?? '')?.[1] ?? '';
    uploaded.push(name);
    await route.fulfill({ status: 201, json: photo(`p-${uploaded.length}`) });
  });
  await page.route('**/photos/**', (route) => route.fulfill({ contentType: 'image/png', body: PIXEL }));
  return uploaded;
}

/** A small file the uploader accepts; the fixtures decide what 12L API says about it. */
export function imageFile(name: string, bytes = 2048): { name: string; mimeType: string; buffer: Buffer } {
  return { name, mimeType: name.endsWith('.png') ? 'image/png' : 'image/jpeg', buffer: Buffer.alloc(bytes, 1) };
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
