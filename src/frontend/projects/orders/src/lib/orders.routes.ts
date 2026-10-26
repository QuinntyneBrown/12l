import { Routes } from '@angular/router';

/** Lazy routes of the orders feature area, mounted at /: checkout, the order confirmation, purchases and sales, the buyer's order, the seller's sale, payouts and the administrator's problem page (admin shell). */
export const routes: Routes = [
  {
    path: 'checkout/:reference',
    loadComponent: () => import('./checkout/checkout-page').then((m) => m.CheckoutPage),
    title: 'Checkout · 12L',
  },
  {
    path: 'orders/:id/confirmed',
    loadComponent: () => import('./order-confirmation/order-confirmation-page').then((m) => m.OrderConfirmationPage),
    title: 'Order confirmed · 12L',
  },
  {
    path: 'orders/:id',
    loadComponent: () => import('./order-detail/order-detail-page').then((m) => m.OrderDetailPage),
    title: 'Order · 12L',
  },
  {
    path: 'sales/:id',
    loadComponent: () => import('./sale-detail/sale-detail-page').then((m) => m.SaleDetailPage),
    title: 'Sale · 12L',
  },
  {
    path: 'account/purchases',
    loadComponent: () => import('./order-history/order-history-page').then((m) => m.OrderHistoryPage),
    title: 'Purchases · 12L',
    data: { list: 'purchases' },
  },
  {
    path: 'account/sales',
    loadComponent: () => import('./order-history/order-history-page').then((m) => m.OrderHistoryPage),
    title: 'Sales · 12L',
    data: { list: 'sales' },
  },
  {
    path: 'account/payouts',
    loadComponent: () => import('./payouts/payouts-page').then((m) => m.PayoutsPage),
    title: 'Payouts · 12L',
  },
  {
    path: 'admin/problems/:reference',
    loadComponent: () => import('./problem-detail/problem-detail-page').then((m) => m.ProblemDetailPage),
    title: 'Order problem · 12L admin',
    data: { shell: 'admin' },
  },
];
