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
  QuoteComponent,
  TrackingLinkComponent,
} from '@12l/components';

import { AddTrackingData, AddTrackingDialog } from '../add-tracking/add-tracking-dialog';
import { CancelOrderData, CancelOrderDialog } from '../cancel-order/cancel-order-dialog';
import { RelistData, RelistDialog } from '../relist/relist-dialog';
import {
  RespondCancellationData,
  RespondCancellationDialog,
} from '../respond-cancellation/respond-cancellation-dialog';
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
 * buyer's address while Paid, with Add tracking and Cancel order; the buyer's request to cancel
 * with Respond; the timeline and tracking link once shipped; the payout after the 12L fee once
 * Completed (L2-031); and Relist item once Cancelled (L2-035).
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
    QuoteComponent,
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

  /** A Paid sale the buyer asked to cancel and the seller has not answered (mocks sale-detail/cancel-requested). */
  readonly requested = computed(
    () => this.sale()?.status === 'Paid' && this.sale()?.cancellationRequest?.status === 'Pending',
  );
  readonly heading = computed(() =>
    this.requested() ? 'Buyer asked to cancel' : HEADINGS[this.sale()?.status ?? 'Paid'],
  );
  readonly endedNote = computed(() => {
    const sale = this.sale();
    if (sale?.canRelist || sale?.status !== 'Cancelled')
      return 'The listing stays off the catalog until you relist it.';
    return 'The listing is back in the catalog.';
  });
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

  async cancelOrder(): Promise<void> {
    const sale = this.sale();
    if (!sale) return;
    const ref = this.dialogs.open<CancelOrderDialog, CancelOrderData, Sale>(CancelOrderDialog, {
      orderId: sale.id,
      buyerDisplayName: sale.buyerDisplayName,
      total: sale.total,
    });
    const cancelled = await ref.closed;
    if (cancelled) this.sale.set(cancelled);
  }

  async respond(): Promise<void> {
    const sale = this.sale();
    if (!sale) return;
    const ref = this.dialogs.open<RespondCancellationDialog, RespondCancellationData, Sale>(RespondCancellationDialog, {
      orderId: sale.id,
      buyerDisplayName: sale.buyerDisplayName,
      message: sale.cancellationRequest?.message ?? null,
      total: sale.total,
      shipBy: sale.shipBy,
    });
    const answered = await ref.closed;
    if (answered) this.sale.set(answered);
  }

  async relist(): Promise<void> {
    const sale = this.sale();
    if (!sale) return;
    const ref = this.dialogs.open<RelistDialog, RelistData, boolean>(RelistDialog, {
      item: sale.item,
      itemPrice: sale.itemPrice,
      shippingCost: sale.shippingCost,
    });
    if (await ref.closed) this.sale.set({ ...sale, canRelist: false });
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
