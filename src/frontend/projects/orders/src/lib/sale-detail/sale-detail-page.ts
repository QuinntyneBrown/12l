import { ChangeDetectionStrategy, Component, computed, effect, inject, input, signal, untracked } from '@angular/core';
import { RouterLink } from '@angular/router';
import { OrdersApi, Sale, shortRef } from '@12l/api';
import {
  AlertComponent,
  ButtonDirective,
  CenterStateComponent,
  DialogService,
  IconComponent,
  OrderSummaryComponent,
  OrderSummaryItem,
  OrderTimelineComponent,
  TrackingLinkComponent,
} from '@12l/components';

import { AddTrackingData, AddTrackingDialog } from '../add-tracking/add-tracking-dialog';
import { formatMoney } from '../money';
import { formatDay, timelineSteps } from '../order-dates';
import { OrderPartyComponent } from '../order-party/order-party';

const HEADINGS: Record<string, string> = {
  Paid: 'You made a sale',
  Shipped: 'Shipped',
  Delivered: 'Delivered',
  Completed: 'Completed',
  Cancelled: 'Cancelled',
  Refunded: 'Refunded',
};

/**
 * The seller's sale at /sales/{id} (mocks pages/sale-detail, L2-033): the ship-by date and the
 * buyer's address while Paid, with Add tracking; the timeline and tracking link once shipped; the
 * payout after the 12L fee once Completed (L2-031).
 */
@Component({
  selector: 'tl-sale-detail-page',
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
  templateUrl: './sale-detail-page.html',
  styleUrl: './sale-detail-page.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SaleDetailPage {
  private readonly api = inject(OrdersApi);
  private readonly dialogs = inject(DialogService);

  /** The order id, from the route parameter. */
  readonly id = input.required<string>();

  readonly sale = signal<Sale | null>(null);
  readonly view = signal<'loading' | 'loaded' | 'error'>('loading');
  readonly errorRef = signal('');

  readonly heading = computed(() => HEADINGS[this.sale()?.status ?? 'Paid']);
  readonly ended = computed(() => ['Cancelled', 'Refunded'].includes(this.sale()?.status ?? ''));
  readonly steps = computed(() => timelineSteps(this.sale()?.timeline ?? []));
  readonly summaryItem = computed<OrderSummaryItem | null>(() => {
    const item = this.sale()?.item;
    return item ? { title: item.title, meta: `${item.brand} · ${item.size}`, photo: item.photo } : null;
  });

  /** Where the payout of a Completed sale is (mocks sale-detail/completed). */
  readonly payoutNote = computed(() => {
    const payout = this.sale()?.payout;
    if (!payout) return '';
    const bank = payout.bankDisplay ?? 'your bank';
    if (payout.status === 'Paid' || (payout.status === 'Sent' && payout.sentAt)) {
      return `Sent ${formatDay(payout.sentAt!)} to ${bank}.`;
    }
    if (payout.status === 'Failed') return 'Your bank returned this payout.';
    return payout.status === 'Held' ? 'Held until you set up payouts.' : 'On its way soon.';
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

  async addTracking(): Promise<void> {
    const sale = this.sale();
    if (!sale) return;
    const ref = this.dialogs.open<AddTrackingDialog, AddTrackingData, Sale>(AddTrackingDialog, {
      orderId: sale.id,
      buyerDisplayName: sale.buyerDisplayName,
    });
    const shipped = await ref.closed;
    if (shipped) this.sale.set(shipped);
  }

  private async load(id: string): Promise<void> {
    this.view.set('loading');
    const result = await this.api.sale(id);
    if (!result.ok) {
      this.errorRef.set(shortRef(result.problem.correlationId));
      this.view.set('error');
      return;
    }
    this.sale.set(result.value);
    this.view.set('loaded');
  }
}
