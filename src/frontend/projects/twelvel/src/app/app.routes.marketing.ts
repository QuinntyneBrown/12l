import { Routes } from '@angular/router';

/**
 * Routes for the public marketing build (`ng build twelvel --configuration marketing`), served at
 * https://12l.ca while the marketplace is not open yet: the marketing page at / and every other
 * path redirected to it. Swapped in for app.routes.ts by angular.json fileReplacements.
 */
export const routes: Routes = [
  { path: '', loadChildren: () => import('@12l/marketing').then((m) => m.routes) },
  { path: '**', redirectTo: '' },
];
