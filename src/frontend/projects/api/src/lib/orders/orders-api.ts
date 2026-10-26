import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';

import { API_BASE_URL } from '../api-base-url';
import { ApiResult, toResult } from '../api-result';
import { CheckoutItem, ShippingAddress } from './checkout-api';

export type OrderStatus = 'Paid' | 'Shipped' | 'Delivered' | 'Completed' | 'Cancelled' | 'Refunded';

/** One step of the order timeline (Paid, Shipped, Delivered, Completed) and when it was reached. */
export interface OrderTimelineStep {
  status: string;
  at: string | null;
}

/** The carrier, the tracking number as stored and the carrier's tracking page. */
export interface Tracking {
  carrier: string;
  number: string;
  url: string;
}

/** One order as its seller's sale page shows it (L2-033): ship-by date, buyer's address and tracking. */
export interface Sale {
  id: string;
  reference: string;
  status: OrderStatus;
  paidAt: string;
  shipBy: string;
  item: CheckoutItem;
  itemPrice: string;
  shippingCost: string;
  salesTax: string;
  total: string;
  buyerDisplayName: string;
  shipTo: ShippingAddress;
  timeline: OrderTimelineStep[];
  tracking: Tracking | null;
}

/** The carriers a seller can choose in Add tracking. */
export const CARRIERS = ['USPS', 'UPS', 'FedEx', 'DHL'] as const;

/** Typed client for the seller's side of an order (ship-order). */
@Injectable({ providedIn: 'root' })
export class OrdersApi {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = inject(API_BASE_URL);

  /** 404 ORDER_NOT_FOUND for anyone but the order's seller. */
  sale(id: string): Promise<ApiResult<Sale>> {
    return toResult(this.http.get<Sale>(`${this.baseUrl}/sales/${id}`));
  }

  /**
   * Ships a Paid order. 422 TRACKING_INVALID with a carrier or trackingNumber field error; 409
   * ORDER_INVALID_TRANSITION when the order is no longer Paid.
   */
  addTracking(id: string, carrier: string, trackingNumber: string): Promise<ApiResult<Sale>> {
    return toResult(this.http.post<Sale>(`${this.baseUrl}/orders/${id}/shipment`, { carrier, trackingNumber }));
  }
}
