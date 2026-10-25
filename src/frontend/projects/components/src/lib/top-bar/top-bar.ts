import { ChangeDetectionStrategy, Component } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';

import { LogoComponent } from '../logo/logo';

/**
 * App-shell top bar, guest state (design system: Top bar). The member state arrives with
 * AuthState from @12l/api; the menu button opens the navigation sheet once SheetService exists.
 */
@Component({
  selector: 'tl-top-bar',
  imports: [RouterLink, RouterLinkActive, LogoComponent],
  templateUrl: './top-bar.html',
  styleUrl: './top-bar.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class TopBarComponent {
  readonly categories = [
    { label: 'Shoes', path: '/shoes' },
    { label: 'Tops', path: '/tops' },
    { label: 'Outerwear', path: '/outerwear' },
    { label: 'Bottoms', path: '/bottoms' },
  ] as const;
}
