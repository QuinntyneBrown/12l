import { Routes } from '@angular/router';

/**
 * Lazy routes of the accounts feature area, mounted at the root because /join, /verify and
 * /sign-in are top-level paths. They render in the auth shell; the Emails settings page renders in
 * the app shell.
 */
export const routes: Routes = [
  {
    path: 'join',
    loadComponent: () => import('./join/join-page').then((m) => m.JoinPage),
    title: 'Join 12L',
    data: { shell: 'auth' },
  },
  {
    path: 'verify',
    loadComponent: () => import('./verify-email/verify-email-page').then((m) => m.VerifyEmailPage),
    title: 'Verify your email · 12L',
    data: { shell: 'auth' },
  },
  {
    path: 'sign-in',
    loadComponent: () => import('./sign-in/sign-in-page').then((m) => m.SignInPage),
    title: 'Sign in · 12L',
    data: { shell: 'auth' },
  },
  {
    path: 'account/emails',
    loadComponent: () =>
      import('./notification-settings/notification-settings-page').then((m) => m.NotificationSettingsPage),
    title: 'Emails · 12L',
  },
];
