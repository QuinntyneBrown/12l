import { Locator, Page } from '@playwright/test';

/** The buyer's order page at /orders/{id} (mocks pages/order-detail). */
export class OrderDetailPage {
  readonly heading: Locator;
  readonly eyebrow: Locator;
  readonly timeline: Locator;
  readonly currentStep: Locator;
  readonly shipNote: Locator;
  readonly tracking: Locator;
  readonly alert: Locator;
  readonly summary: Locator;
  readonly loading: Locator;
  readonly centerState: Locator;

  constructor(private readonly page: Page) {
    const main = page.locator('main');
    this.heading = main.getByRole('heading', { level: 1 });
    this.eyebrow = main.locator('.eyebrow');
    this.timeline = main.getByRole('list', { name: 'Order progress' });
    this.currentStep = this.timeline.locator('[aria-current="step"]');
    this.shipNote = main.locator('.order__note');
    this.tracking = main.locator('.facts-row');
    this.alert = main.locator('.alert');
    this.summary = main.getByRole('complementary', { name: 'Order summary' });
    this.loading = main.locator('[aria-busy="true"]');
    this.centerState = main.locator('.center-state');
  }

  async goto(id = 'o-1'): Promise<void> {
    await this.page.goto(`/orders/${id}`);
  }
}
