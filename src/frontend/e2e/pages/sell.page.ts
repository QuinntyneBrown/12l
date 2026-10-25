import { Locator, Page } from '@playwright/test';

/** Sell an item at /sell (mocks pages/sell) and the verify-email-prompt dialog it opens. */
export class SellPage {
  readonly heading: Locator;
  readonly category: Locator;
  readonly type: Locator;
  readonly fixedSize: Locator;
  readonly title: Locator;
  readonly brand: Locator;
  readonly condition: Locator;
  readonly flaws: Locator;
  readonly description: Locator;
  readonly price: Locator;
  readonly shipping: Locator;
  readonly earnings: Locator;
  readonly confirm: Locator;
  readonly saveDraft: Locator;
  readonly publish: Locator;
  readonly errorSummary: Locator;
  readonly dialog: Locator;

  constructor(private readonly page: Page) {
    this.heading = page.getByRole('heading', { level: 1 });
    this.category = page.getByLabel('Category');
    this.type = page.getByLabel('Type');
    this.fixedSize = page.locator('#size');
    this.title = page.getByLabel('Title');
    this.brand = page.getByLabel('Brand');
    this.condition = page.getByRole('group', { name: 'Condition' });
    this.flaws = page.getByLabel('Describe the flaws');
    this.description = page.getByLabel('Description');
    this.price = page.locator('#price');
    this.shipping = page.getByLabel('Shipping');
    this.earnings = page.locator('.earnings');
    this.confirm = page.locator('#confirm');
    this.saveDraft = page.getByRole('button', { name: 'Save draft' });
    this.publish = page.getByRole('button', { name: 'Publish' });
    this.errorSummary = page.getByRole('alert').filter({ hasText: 'Fix these to continue' });
    this.dialog = page.getByRole('dialog');
  }

  async goto(path = '/sell'): Promise<void> {
    await this.page.goto(path);
  }

  async fillComplete(): Promise<void> {
    await this.category.selectOption('Shoes');
    await this.type.selectOption('Sneakers');
    await this.title.fill("Air Force 1 '07, white");
    await this.brand.fill('Nike');
    await this.condition.getByLabel('Used - Good').check();
    await this.description.fill('Light creasing, soles have plenty left. Cleaned and ready to wear.');
    await this.price.fill('60.00');
    await this.shipping.fill('8.00');
    await this.confirm.check();
  }

  fieldError(id: string): Locator {
    return this.page.locator(`#${id}-error`);
  }
}
