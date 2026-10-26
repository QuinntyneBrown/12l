import { ChangeDetectionStrategy, Component, computed, effect, inject, input, signal, untracked } from '@angular/core';
import { RouterLink } from '@angular/router';
import { CheckoutApi, Purchase, shortRef } from '@12l/api';
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

import { formatMoney } from '../money';
import { formatDay, timelineSteps } from '../order-dates';
import { ConfirmReceiptData, ConfirmReceiptDialog } from '../confirm-receipt/confirm-receipt-dialog';
import { OrderPartyComponent } from '../order-party/order-party';
import {
  RequestCancellationData,
  RequestCancellationDialog,
} from '../request-cancellation/request-cancellation-dialog';

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
 * with the ship-by date, on its way with the tracking link, delivered with the automatic completion
 * date, completed, or cancelled and refunded with the seller's note. A Shipped or Delivered order
 * offers "I received it" (L2-034); a Paid order offers "Ask to cancel" once (L2-035).
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
    QuoteComponent,
    TrackingLinkComponent,
  ],
  templateUrl: './order-detail-page.html',
  styleUrl: './order-detail-page.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class OrderDetailPage {
  private readonly api = inject(CheckoutApi);
  private readonly dialogs = inject(DialogService);

  /** The order id, from the route parameter. */
  readonly id = input.required<string>();

  readonly order = signal<Purchase | null>(null);
  readonly view = signal<'loading' | 'loaded' | 'error'>('loading');
  readonly errorRef = signal('');

  readonly heading = computed(() => HEADINGS[this.order()?.status ?? 'Paid']);
  readonly canConfirm = computed(() => ['Shipped', 'Delivered'].includes(this.order()?.status ?? ''));
  readonly ended = computed(() => ['Cancelled', 'Refunded'].includes(this.order()?.status ?? ''));
  readonly canAskToCancel = computed(() => this.order()?.status === 'Paid' && !this.order()?.cancellationRequest);
  /** Where the buyer's request to cancel a Paid order stands (mocks order-detail/cancel-requested). */
  readonly requestNote = computed(() => {
    const order = this.order();
    if (order?.status !== 'Paid' || !order.cancellationRequest) return '';
    return order.cancellationRequest.status === 'Declined'
      ? `${order.sellerDisplayName} declined to cancel. They still ship by ${formatDay(order.shipBy)}.`
      : `You asked ${order.sellerDisplayName} to cancel. They haven’t answered yet.`;
  });
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

  async confirmReceipt(): Promise<void> {
    const order = this.order();
    if (!order) return;
    const ref = this.dialogs.open<ConfirmReceiptDialog, ConfirmReceiptData, Purchase>(ConfirmReceiptDialog, {
      orderId: order.id,
      item: order.item,
      sellerDisplayName: order.sellerDisplayName,
    });
    const completed = await ref.closed;
    if (completed) this.order.set(completed);
  }

  async askToCancel(): Promise<void> {
    const order = this.order();
    if (!order) return;
    const ref = this.dialogs.open<RequestCancellationDialog, RequestCancellationData, Purchase>(
      RequestCancellationDialog,
      { orderId: order.id, sellerDisplayName: order.sellerDisplayName },
    );
    const requested = await ref.closed;
    if (requested) this.order.set(requested);
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
