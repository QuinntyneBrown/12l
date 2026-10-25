import { ChangeDetectionStrategy, Component } from '@angular/core';

/** Polite live region for toasts (design system: Toast). Empty until ToastService is implemented by responsive-accessible-shell. */
@Component({
  selector: 'tl-toast-region',
  templateUrl: './toast-region.html',
  styleUrl: './toast-region.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ToastRegionComponent {}
