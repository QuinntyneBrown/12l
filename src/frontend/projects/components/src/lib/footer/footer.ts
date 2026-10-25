import { ChangeDetectionStrategy, Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { LogoComponent } from '../logo/logo';

/** App-shell footer: small logo, legal links, cookie settings and the copyright year (design system: Footer). */
@Component({
  selector: 'tl-footer',
  imports: [RouterLink, LogoComponent],
  templateUrl: './footer.html',
  styleUrl: './footer.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class FooterComponent {
  readonly year = new Date().getFullYear();
}
