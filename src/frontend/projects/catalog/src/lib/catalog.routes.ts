import { Routes } from '@angular/router';

const page = () => import('./catalog/catalog-page').then((m) => m.CatalogPage);

/** Lazy routes of the catalog feature area, mounted at /: the catalog, one page per category and the listing detail. */
export const routes: Routes = [
  { path: '', pathMatch: 'full', loadComponent: page, title: '12L' },
  { path: 'shoes', loadComponent: page, data: { category: 'Shoes' }, title: 'Shoes · 12L' },
  { path: 'tops', loadComponent: page, data: { category: 'Tops' }, title: 'Tops · 12L' },
  { path: 'outerwear', loadComponent: page, data: { category: 'Outerwear' }, title: 'Outerwear · 12L' },
  { path: 'bottoms', loadComponent: page, data: { category: 'Bottoms' }, title: 'Bottoms · 12L' },
  {
    path: 'items/:reference',
    loadComponent: () => import('./listing-detail/listing-detail-page').then((m) => m.ListingDetailPage),
    title: 'Item · 12L',
  },
];
