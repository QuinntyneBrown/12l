import { ChangeDetectionStrategy, Component } from '@angular/core';
import { SkipLinkComponent, ToastRegionComponent } from '@12l/components';

import { AppShellComponent } from './app-shell/app-shell';

/** Root component: skip link, the app shell and the toast region (responsive-accessible-shell). */
@Component({
  selector: 'tl-root',
  imports: [SkipLinkComponent, AppShellComponent, ToastRegionComponent],
  templateUrl: './app.html',
  styleUrl: './app.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class App {}
