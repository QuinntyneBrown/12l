import { ChangeDetectionStrategy, Component } from '@angular/core';

/** Placeholder home page. Replaced by the catalog page when browse-catalog is built. */
@Component({
  selector: 'tl-home-placeholder',
  templateUrl: './home-placeholder.html',
  styleUrl: './home-placeholder.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class HomePlaceholderPage {}
