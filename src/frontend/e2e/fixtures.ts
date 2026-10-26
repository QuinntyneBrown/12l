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

/** One catalog card as GET /api/catalog/listings returns it; n picks the reference and title. */
export function catalogCard(n: number, fields: Record<string, unknown> = {}): Record<string, unknown> {
  const hash = String(n).padStart(64, 'c');
  const srcset = (ext: string) =>
    `/photos/${hash}/400.${ext} 400w, /photos/${hash}/800.${ext} 800w, /photos/${hash}/1600.${ext} 1200w`;
  return {
    id: `00000000-0000-0000-0000-${String(n).padStart(12, '0')}`,
    reference: `L-${10000 + n}`,
    title: `Air Max 90 no. ${n}`,
    brand: 'Nike',
    category: 'Shoes',
    subcategory: 'Sneakers',
    sizeLabel: 'US 12',
    condition: 'Used - Excellent',
    price: '85.00',
    status: 'Active',
    publishedAt: '2026-10-25T12:00:00Z',
    coverPhoto: {
      width: 1200,
      height: 1600,
      alt: `Photo 1 of Nike Air Max 90 no. ${n}`,
      src: `/photos/${hash}/400.jpg`,
      webp: srcset('webp'),
      jpeg: srcset('jpg'),
    },
    ...fields,
  };
}

/** A catalog page of cards numbered from (page - 1) * 24 + 1, out of total. */
export function catalogPage(total: number, page = 1, pageSize = 24): Record<string, unknown> {
  const first = (page - 1) * pageSize + 1;
  const count = Math.max(0, Math.min(pageSize, total - first + 1));
  return { items: Array.from({ length: count }, (_, i) => catalogCard(first + i)), page, pageSize, totalCount: total };
}

/**
 * Answers GET /api/catalog/listings with pages of `total` cards and serves the photos. Returns
 * the query strings of the requests, in order.
 */
export async function serveCatalog(page: Page, total: number): Promise<URLSearchParams[]> {
  const requests: URLSearchParams[] = [];
  await page.route('**/api/catalog/listings**', (route) => {
    const query = new URL(route.request().url()).searchParams;
    requests.push(query);
    return route.fulfill({ json: catalogPage(total, Number(query.get('page') ?? 1)) });
  });
  await page.route('**/photos/**', (route) => route.fulfill({ contentType: 'image/png', body: PIXEL }));
  return requests;
}

/** A listing as GET /api/catalog/listings/{reference} returns it, seen by another member. */
export function listingDetail(fields: Record<string, unknown> = {}, photos = 3): Record<string, unknown> {
  const photo = (i: number) => {
    const hash = String(i).padStart(64, 'd');
    const srcset = (ext: string) =>
      `/photos/${hash}/400.${ext} 400w, /photos/${hash}/800.${ext} 800w, /photos/${hash}/1600.${ext} 1200w`;
    return {
      width: 1200,
      height: 1600,
      alt: `Photo ${i} of Nike Air Max 90, white`,
      src: `/photos/${hash}/400.jpg`,
      webp: srcset('webp'),
      jpeg: srcset('jpg'),
    };
  };
  return {
    id: '00000000-0000-0000-0000-000000010001',
    reference: 'L-10001',
    title: 'Air Max 90, white',
    brand: 'Nike',
    category: 'Shoes',
    subcategory: 'Sneakers',
    sizeLabel: 'US 12',
    condition: 'Used - Excellent',
    flaws: null,
    description: 'Worn a handful of times. No creases on the toe box, soles clean. Original box included.',
    price: '85.00',
    shippingCost: '9.00',
    total: '94.00',
    status: 'Active',
    publishedAt: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
    photos: Array.from({ length: photos }, (_, i) => photo(i + 1)),
    seller: { displayName: 'kicks_12', completedSalesCount: 0, ratingAverage: null, publishedReviewCount: 0 },
    viewer: { relation: 'OtherMember' },
    ...fields,
  };
}

/** Answers GET /api/catalog/listings/L-10001 with this body and serves the photos. */
export async function serveListing(page: Page, body: Record<string, unknown>): Promise<void> {
  await page.route('**/api/catalog/listings/L-10001', (route) => route.fulfill({ json: body }));
  await page.route('**/photos/**', (route) => route.fulfill({ contentType: 'image/png', body: PIXEL }));
}

/** The saved address of marcus_12 as 12L API returns it. */
export const brooklyn = {
  fullName: 'Marcus Bell',
  line1: '214 Kent Ave',
  line2: 'Apt 3R',
  city: 'Brooklyn',
  state: 'NY',
  zip: '11249',
  country: 'US',
};

/** When the fixtures' checkouts start; tests install the page clock at this time. */
export const checkoutStart = new Date('2026-10-25T12:00:00Z');

/** A checkout of L-10001 as /api/checkouts returns it: 9:41 left, priced for the saved address. */
export function checkout(fields: Record<string, unknown> = {}): Record<string, unknown> {
  const hash = '1'.padStart(64, 'd');
  return {
    id: 'c-1',
    status: 'Open',
    expiresAt: new Date(checkoutStart.getTime() + (9 * 60 + 41) * 1000).toISOString(),
    item: {
      reference: 'L-10001',
      title: 'Air Max 90, white',
      brand: 'Nike',
      size: "Men's US 12",
      condition: 'Used - Excellent',
      photo: {
        width: 1200,
        height: 1600,
        alt: '',
        src: `/photos/${hash}/400.jpg`,
        webp: `/photos/${hash}/400.webp 400w`,
        jpeg: `/photos/${hash}/400.jpg 400w`,
      },
    },
    itemPrice: '85.00',
    shippingCost: '9.00',
    salesTax: null,
    total: null,
    address: null,
    savedAddress: brooklyn,
    lastDeclineReason: null,
    orderId: null,
    ...fields,
  };
}

/** The checkout once an address is set: $8.34 tax, $102.34 total. */
export function pricedCheckout(fields: Record<string, unknown> = {}): Record<string, unknown> {
  return checkout({ address: brooklyn, salesTax: '8.34', total: '102.34', ...fields });
}

/** GET /api/purchases/o-1. */
export const purchase = {
  id: 'o-1',
  reference: '12L-48377',
  status: 'Paid',
  item: checkout()['item'],
  total: '102.34',
  cardBrand: 'Visa',
  cardLast4: '4242',
  sellerDisplayName: 'kicks_12',
  paidAt: '2026-10-25T12:01:00Z',
};

/** One request the checkout page sent, with its body and headers. */
export interface SentRequest {
  method: string;
  url: string;
  body: unknown;
  headers: Record<string, string>;
}

/**
 * Answers the checkout endpoints for c-1 and serves the photos. start answers POST /api/checkouts;
 * the PUT address answers the priced checkout unless `address` is given; payments answer 202; each
 * GET of the checkout answers the next of `polls` (the last repeats). Returns every request sent.
 */
export async function serveCheckout(
  page: Page,
  options: {
    start?: { status: number; contentType?: string; body: string } | Record<string, unknown>;
    address?: { status: number; contentType: string; body: string };
    pay?: { status: number; contentType: string; body: string };
    polls?: Record<string, unknown>[];
  } = {},
): Promise<SentRequest[]> {
  const sent: SentRequest[] = [];
  const record = (route: Route) => {
    const request = route.request();
    sent.push({
      method: request.method(),
      url: request.url(),
      body: request.postDataJSON(),
      headers: request.headers(),
    });
  };
  const polls = [...(options.polls ?? [pricedCheckout({ status: 'Paid', orderId: 'o-1' })])];
  await page.route('**/api/checkouts', (route) => {
    record(route);
    const start = options.start ?? checkout();
    return route.fulfill('status' in start && 'body' in start ? (start as never) : { status: 201, json: start });
  });
  await page.route('**/api/checkouts/c-1/address', (route) => {
    record(route);
    return route.fulfill(options.address ?? { json: pricedCheckout() });
  });
  await page.route('**/api/checkouts/c-1/payments', (route) => {
    record(route);
    return route.fulfill(options.pay ?? { status: 202, json: { id: 'p-1', status: 'Pending' } });
  });
  await page.route('**/api/checkouts/c-1', (route) => {
    record(route);
    if (route.request().method() === 'DELETE') return route.fulfill({ status: 204 });
    const next = polls.length > 1 ? polls.shift()! : polls[0];
    return route.fulfill({ json: next });
  });
  await page.route('**/photos/**', (route) => route.fulfill({ contentType: 'image/png', body: PIXEL }));
  return sent;
}

/** The order timeline as the order endpoints return it: Paid on Sat 24 Oct, later steps as given. */
export function timeline(shipped: string | null = null, delivered: string | null = null): Record<string, unknown>[] {
  return [
    { status: 'Paid', at: '2026-10-24T15:00:00Z' },
    { status: 'Shipped', at: shipped },
    { status: 'Delivered', at: delivered },
    { status: 'Completed', at: null },
  ];
}

export const uspsTracking = {
  carrier: 'USPS',
  number: '9400111899223456120477',
  url: 'https://tools.usps.com/go/TrackConfirmAction?tLabels=9400111899223456120477',
};

/** GET /api/sales/o-1: a Paid sale of the hoodie to tall_tom, ship by Fri 30 Oct (mocks pages/sale-detail). */
export function sale(fields: Record<string, unknown> = {}): Record<string, unknown> {
  return {
    id: 'o-1',
    reference: '12L-48302',
    status: 'Paid',
    paidAt: '2026-10-24T15:00:00Z',
    shipBy: '2026-10-30T15:00:00Z',
    item: {
      ...(checkout()['item'] as object),
      title: 'Reverse Weave hoodie, grey',
      brand: 'Champion',
      size: "Men's L",
    },
    itemPrice: '38.00',
    shippingCost: '7.00',
    salesTax: '3.15',
    total: '48.15',
    buyerDisplayName: 'tall_tom',
    shipTo: {
      fullName: 'Tom Reyes',
      line1: '1450 Larimer St',
      line2: 'Apt 6B',
      city: 'Denver',
      state: 'CO',
      zip: '80202',
      country: 'US',
    },
    timeline: timeline(),
    tracking: null,
    ...fields,
  };
}

/** GET /api/purchases/o-1 as the buyer's order page reads it: the Paid order from kicks_12. */
export function buyerOrder(fields: Record<string, unknown> = {}): Record<string, unknown> {
  return {
    ...purchase,
    paidAt: '2026-10-24T15:00:00Z',
    shipBy: '2026-10-30T15:00:00Z',
    itemPrice: '85.00',
    shippingCost: '9.00',
    salesTax: '8.34',
    timeline: timeline(),
    tracking: null,
    ...fields,
  };
}
