import { ChangeDetectionStrategy, Component, computed, input } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';

import { IconComponent } from '../icon/icon';
import { LogoComponent } from '../logo/logo';

/** The member the top bar shows; null for a visitor. */
export interface TopBarMember {
  displayName: string;
}

/**
 * App-shell top bar in its guest and member states (design system: Top bar). The application
 * passes the member from AuthState; the menu button opens the navigation sheet once SheetService exists.
 */
@Component({
  selector: 'tl-top-bar',
  imports: [RouterLink, RouterLinkActive, IconComponent, LogoComponent],
  templateUrl: './top-bar.html',
  styleUrl: './top-bar.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class TopBarComponent {
  readonly member = input<TopBarMember | null>(null);

  readonly initials = computed(() => this.member()?.displayName.slice(0, 2).toUpperCase() ?? '');

  readonly categories = [
    { label: 'Shoes', path: '/shoes' },
    { label: 'Tops', path: '/tops' },
    { label: 'Outerwear', path: '/outerwear' },
    { label: 'Bottoms', path: '/bottoms' },
  ] as const;
}
