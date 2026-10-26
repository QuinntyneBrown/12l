import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: 'welcome', loadChildren: () => import('@12l/marketing').then((m) => m.routes) },
  { path: '', loadChildren: () => import('@12l/catalog').then((m) => m.routes) },
  { path: '', loadChildren: () => import('@12l/listings').then((m) => m.routes) },
  { path: '', loadChildren: () => import('@12l/orders').then((m) => m.routes) },
  { path: 'members', loadChildren: () => import('@12l/reviews').then((m) => m.routes) },
  { path: 'privacy', loadChildren: () => import('@12l/privacy').then((m) => m.routes) },
  { path: '', loadChildren: () => import('@12l/accounts').then((m) => m.routes) },
];
