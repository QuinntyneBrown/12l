import { ChangeDetectionStrategy, Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { FooterComponent, TopBarComponent } from '@12l/components';

/** App shell: top bar, main#main with the router outlet, footer. Auth, admin and bare shells come later. */
@Component({
  selector: 'tl-app-shell',
  imports: [RouterOutlet, TopBarComponent, FooterComponent],
  templateUrl: './app-shell.html',
  styleUrl: './app-shell.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class AppShellComponent {}
