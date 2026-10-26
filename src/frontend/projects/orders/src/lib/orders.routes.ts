import { Routes } from '@angular/router';

/** Lazy routes of the orders feature area, mounted at /: checkout and the order confirmation. */
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
];
