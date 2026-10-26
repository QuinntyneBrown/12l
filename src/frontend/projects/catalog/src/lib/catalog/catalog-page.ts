import { DecimalPipe } from '@angular/common';
import { ChangeDetectionStrategy, Component, OnInit, computed, inject, input } from '@angular/core';
import { RouterLink } from '@angular/router';
import {
  AlertComponent,
  ButtonDirective,
  EmptyStateComponent,
  IconComponent,
  ListingGridComponent,
  LoadMoreComponent,
  SizeTagComponent,
} from '@12l/components';

import { CatalogStore } from './catalog-store';

import { toCardView } from '../card-view';

const SIZE_LABELS: Record<string, string> = { Shoes: 'US 12', Tops: 'L', Outerwear: 'L', Bottoms: 'L' };

/**
 * The catalog at / and a category page at /shoes, /tops... (mocks pages/catalog): hero or
 * category header, the item count, the listing grid with Load more, and the loading, empty,
 * error and offline states. Search, filters and sort are search-and-filter-catalog.
 */
@Component({
  selector: 'tl-catalog-page',
  imports: [
    DecimalPipe,
    RouterLink,
    AlertComponent,
    ButtonDirective,
    EmptyStateComponent,
    IconComponent,
    ListingGridComponent,
    LoadMoreComponent,
    SizeTagComponent,
  ],
  providers: [CatalogStore],
  templateUrl: './catalog-page.html',
  styleUrl: './catalog-page.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class CatalogPage implements OnInit {
  readonly store = inject(CatalogStore);
  /** From the route data of a category page; absent at /. */
  readonly category = input<string>();

  readonly sizeLabel = computed(() => SIZE_LABELS[this.category() ?? ''] ?? '');
  readonly cards = computed(() => this.store.items().map(toCardView));

  ngOnInit(): void {
    void this.store.load(this.category() ?? null);
  }
}
