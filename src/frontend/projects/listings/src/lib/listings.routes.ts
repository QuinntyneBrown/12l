import { Routes } from '@angular/router';

/** Lazy routes of the listings feature area, mounted at /: the sell form and the seller's listings. */
export const routes: Routes = [
  {
    path: 'sell',
    loadComponent: () => import('./sell/sell-page').then((m) => m.SellPage),
    title: 'Sell an item · 12L',
  },
  {
    path: 'sell/:reference',
    loadComponent: () => import('./sell/sell-page').then((m) => m.SellPage),
    title: 'Sell an item · 12L',
  },
  {
    path: 'account/listings',
    loadComponent: () => import('./my-listings/my-listings-page').then((m) => m.MyListingsPage),
    title: 'Your listings · 12L',
  },
];
