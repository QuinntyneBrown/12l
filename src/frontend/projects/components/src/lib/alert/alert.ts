import { ChangeDetectionStrategy, Component, computed, input } from '@angular/core';

import { IconComponent, IconName } from '../icon/icon';

export type AlertTone = 'info' | 'success' | 'warning' | 'danger';

const ICONS: Record<AlertTone, IconName> = {
  info: 'info',
  success: 'check-circle',
  warning: 'alert',
  danger: 'x-circle',
};

/**
 * Inline message with an icon, a title and projected text (design system: Alert). Danger alerts
 * are announced with role="alert"; pass role="status" for a polite success message.
 */
@Component({
  selector: 'tl-alert',
  imports: [IconComponent],
  templateUrl: './alert.html',
  styleUrl: './alert.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class AlertComponent {
  readonly tone = input<AlertTone>('info');
  readonly heading = input.required<string>();
  readonly icon = input<IconName>();
  readonly role = input<'alert' | 'status' | null>();

  readonly iconName = computed(() => this.icon() ?? ICONS[this.tone()]);
  readonly ariaRole = computed(() => {
    const role = this.role();
    if (role !== undefined) return role;
    return this.tone() === 'danger' ? 'alert' : null;
  });
}
