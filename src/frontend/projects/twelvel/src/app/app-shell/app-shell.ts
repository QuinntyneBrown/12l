import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { ActivatedRouteSnapshot, ResolveEnd, Router, RouterOutlet } from '@angular/router';
import { filter, map } from 'rxjs';
import { AuthState } from '@12l/api';
import { FooterComponent, LogoComponent, TopBarComponent } from '@12l/components';
import { PayoutBannerComponent } from '@12l/orders';

/** Shell named by the deepest route's data.shell: 'app' (default) or 'auth'. */
type Shell = 'app' | 'auth';

function shellOf(route: ActivatedRouteSnapshot): Shell {
  let deepest = route;
  while (deepest.firstChild) deepest = deepest.firstChild;
  return deepest.data['shell'] === 'auth' ? 'auth' : 'app';
}

/**
 * App shell: the payout banner, top bar with the member from AuthState, main#main with the router
 * outlet and the footer. Routes with data.shell 'auth' render in the auth shell: large logo above a centred card.
 */
@Component({
  selector: 'tl-app-shell',
  imports: [RouterOutlet, TopBarComponent, FooterComponent, LogoComponent, PayoutBannerComponent],
  templateUrl: './app-shell.html',
  styleUrl: './app-shell.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class AppShellComponent {
  private readonly router = inject(Router);
  readonly auth = inject(AuthState);

  readonly shell = toSignal(
    this.router.events.pipe(
      filter((event) => event instanceof ResolveEnd),
      map((event) => shellOf(event.state.root)),
    ),
    { initialValue: 'app' as Shell },
  );

  constructor() {
    void this.auth.load();
  }
}
