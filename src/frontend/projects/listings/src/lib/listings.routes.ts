import { Routes } from '@angular/router';

/** Lazy routes of the listings feature area, mounted at /sell. */
export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./sell/sell-page').then((m) => m.SellPage),
    title: 'Sell an item · 12L',
  },
  {
    path: ':reference',
    loadComponent: () => import('./sell/sell-page').then((m) => m.SellPage),
    title: 'Sell an item · 12L',
  },
];
