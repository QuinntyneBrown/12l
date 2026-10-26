import { ChangeDetectionStrategy, Component, OnDestroy, computed, inject } from '@angular/core';
import { Meta } from '@angular/platform-browser';
import { RouterLink } from '@angular/router';
import { AuthState } from '@12l/api';
import {
  ButtonDirective,
  DialogService,
  FeatureBandComponent,
  FeaturePoint,
  MarketingHeroComponent,
  Step,
  StepsComponent,
  VideoPosterComponent,
} from '@12l/components';

import { PitchVideoDialog } from './pitch-video-dialog';

const DESCRIPTION =
  'Big sizes, finally in one place: men’s US 12 shoes and men’s L clothing. Shop pieces that already fit, or sell yours to people your size.';

/**
 * Public marketing page at /welcome (L2-078 to L2-083). Static copy, no 12L API call of its own;
 * Start selling goes to /join for a visitor and /sell for a member. Copy follows ADR general/0005:
 * no "only", no sizes other than men's US 12 and men's L.
 */
@Component({
  selector: 'tl-welcome-page',
  imports: [
    RouterLink,
    ButtonDirective,
    MarketingHeroComponent,
    FeatureBandComponent,
    StepsComponent,
    VideoPosterComponent,
  ],
  templateUrl: './welcome-page.html',
  styleUrl: './welcome-page.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class WelcomePage implements OnDestroy {
  private readonly auth = inject(AuthState);
  private readonly dialogs = inject(DialogService);
  private readonly meta = inject(Meta);

  readonly sellHref = computed(() => (this.auth.member() ? '/sell' : '/join'));

  readonly shopperPoints: FeaturePoint[] = [
    { title: 'Every pair is a men’s US 12', text: 'Sneakers, boots and dress shoes, all in your size.' },
    { title: 'Every top, jacket and pant is a men’s L', text: 'Browse without a size filter.' },
    { title: 'Honest condition', text: 'Five grades, and flaws named up front.' },
  ];
  readonly sellerPoints: FeaturePoint[] = [
    { title: 'List in minutes', text: 'Photos, a price and the condition. The size is set for you.' },
    { title: 'Buyers already wear your size', text: 'Sell to people your size, not the whole internet.' },
    { title: '10% fee, only when it sells', text: 'Taken when the order completes. Listing is free.' },
  ];
  readonly steps: Step[] = [
    { title: 'List it', text: 'Add photos, a price and the condition.' },
    { title: 'Sell it', text: 'A buyer pays. You ship within 5 business days.' },
    { title: 'Get paid', text: 'The order completes and your payout is on its way.' },
  ];

  constructor() {
    this.meta.updateTag({ name: 'description', content: DESCRIPTION });
  }

  openVideo(): void {
    this.dialogs.open(PitchVideoDialog);
  }

  ngOnDestroy(): void {
    this.meta.removeTag('name="description"');
  }
}
