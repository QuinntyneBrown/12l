import { ChangeDetectionStrategy, Component, computed, effect, inject, input, signal, untracked } from '@angular/core';
import { RouterLink } from '@angular/router';
import { CheckoutApi, Purchase, shortRef } from '@12l/api';
import {
  AlertComponent,
  ButtonDirective,
  CenterStateComponent,
  IconComponent,
  OrderSummaryComponent,
  OrderSummaryItem,
  OrderTimelineComponent,
  TrackingLinkComponent,
} from '@12l/components';

import { formatMoney } from '../money';
import { formatDay, timelineSteps } from '../order-dates';
import { OrderPartyComponent } from '../order-party/order-party';

const HEADINGS: Record<string, string> = {
  Paid: 'Waiting to ship',
  Shipped: 'On its way',
  Delivered: 'Delivered',
  Completed: 'Completed',
  Cancelled: 'Cancelled',
  Refunded: 'Refunded',
};

/**
 * The buyer's order at /orders/{id} (mocks pages/order-detail, L2-032, L2-033): waiting to ship
 * with the ship-by date, on its way with the tracking link, delivered, or cancelled and refunded.
 */
@Component({
  selector: 'tl-order-detail-page',
  imports: [
    RouterLink,
    AlertComponent,
    ButtonDirective,
    CenterStateComponent,
    IconComponent,
    OrderPartyComponent,
    OrderSummaryComponent,
    OrderTimelineComponent,
    TrackingLinkComponent,
  ],
  templateUrl: './order-detail-page.html',
  styleUrl: './order-detail-page.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class OrderDetailPage {
  private readonly api = inject(CheckoutApi);

  /** The order id, from the route parameter. */
  readonly id = input.required<string>();

  readonly order = signal<Purchase | null>(null);
  readonly view = signal<'loading' | 'loaded' | 'error'>('loading');
  readonly errorRef = signal('');

  readonly heading = computed(() => HEADINGS[this.order()?.status ?? 'Paid']);
  readonly ended = computed(() => ['Cancelled', 'Refunded'].includes(this.order()?.status ?? ''));
  readonly steps = computed(() => timelineSteps(this.order()?.timeline ?? []));
  readonly refund = computed(() => {
    const order = this.order();
    if (!order) return '';
    const card = order.cardBrand && order.cardLast4 ? ` to ${order.cardBrand} ending ${order.cardLast4}` : '';
    return `${formatMoney(order.total)} back${card}. Allow 5–10 days.`;
  });
  readonly summaryItem = computed<OrderSummaryItem | null>(() => {
    const item = this.order()?.item;
    return item ? { title: item.title, meta: `${item.brand} · ${item.size}`, photo: item.photo } : null;
  });

  readonly day = formatDay;
  readonly money = formatMoney;

  constructor() {
    effect(() => {
      const id = this.id();
      untracked(() => void this.load(id));
    });
  }

  retry(): Promise<void> {
    return this.load(this.id());
  }

  private async load(id: string): Promise<void> {
    this.view.set('loading');
    const result = await this.api.purchase(id);
    if (!result.ok) {
      this.errorRef.set(shortRef(result.problem.correlationId));
      this.view.set('error');
      return;
    }
    this.order.set(result.value);
    this.view.set('loaded');
  }
}
