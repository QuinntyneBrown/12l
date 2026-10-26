import { ChangeDetectionStrategy, Component, OnInit, computed, inject, input, signal } from '@angular/core';
import { takeUntilDestroyed, toSignal } from '@angular/core/rxjs-interop';
import { NonNullableFormBuilder, ReactiveFormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { map } from 'rxjs';
import {
  ApiProblem,
  AuthState,
  Category,
  ListingsApi,
  MyListing,
  Photo,
  PhotosApi,
  SellingApi,
  SellingOptions,
  shortRef,
} from '@12l/api';
import {
  AlertComponent,
  ButtonDirective,
  CenterStateComponent,
  ChoiceComponent,
  DialogService,
  EarningsComponent,
  ErrorSummaryComponent,
  FixedSizeComponent,
  FormFieldComponent,
  IconComponent,
  InputGroupComponent,
  ItemRowComponent,
  PhotoUploaderComponent,
  SegmentedComponent,
  SummaryError,
  UploaderMove,
  UploaderTile,
} from '@12l/components';

import { VerifyEmailPromptComponent } from '../verify-email-prompt/verify-email-prompt';
import {
  FIELD_IDS,
  FieldErrors,
  ListingFormValue,
  MAX_PHOTO_BYTES,
  SERVER_FIELDS,
  checkListing,
  confirmLabel,
  estimateEarnings,
  formatFileSize,
  formatUsd,
  toDetails,
} from './listing-rules';

type View = 'loading' | 'form' | 'success' | 'unverified' | 'limited' | 'error';

/** What the success panel shows after publishing. */
interface Published {
  reference: string;
  title: string;
  meta: string;
  payoutOnboardingRequired: boolean;
}

/** An uploader tile with the uploaded photo's ID and, for a refused file, why. */
interface PhotoTile extends UploaderTile {
  id?: string;
  message?: string;
}

/**
 * Sell an item at /sell and continue a draft at /sell/{reference} (create-listing, mocks
 * pages/sell). There is no size input: the size shown comes from the category and 12L API sets
 * the stored size (L2-012, L2-013). Photos upload one file per request as soon as they are chosen;
 * a save sends the uploaded IDs in display order (upload-listing-photos, L2-017).
 */
@Component({
  selector: 'tl-sell-page',
  imports: [
    ReactiveFormsModule,
    RouterLink,
    AlertComponent,
    ButtonDirective,
    CenterStateComponent,
    ChoiceComponent,
    EarningsComponent,
    ErrorSummaryComponent,
    FixedSizeComponent,
    FormFieldComponent,
    IconComponent,
    InputGroupComponent,
    ItemRowComponent,
    PhotoUploaderComponent,
    SegmentedComponent,
  ],
  templateUrl: './sell-page.html',
  styleUrl: './sell-page.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SellPage implements OnInit {
  private readonly auth = inject(AuthState);
  private readonly selling = inject(SellingApi);
  private readonly listings = inject(ListingsApi);
  private readonly photoUploads = inject(PhotosApi);
  private readonly dialogs = inject(DialogService);
  private readonly router = inject(Router);

  /** The draft to continue, bound from /sell/:reference. */
  readonly reference = input<string>();

  readonly form = inject(NonNullableFormBuilder).group({
    category: '',
    subcategory: { value: '', disabled: true },
    title: '',
    brand: '',
    condition: '',
    flaws: '',
    description: '',
    price: '',
    shipping: '',
    confirm: false,
  });

  readonly view = signal<View>('loading');
  readonly busy = signal<'draft' | 'publish' | null>(null);
  readonly errors = signal<FieldErrors>({});
  readonly draftSaved = signal(false);
  readonly failure = signal<{ heading: string; text: string; ref: string } | null>(null);
  readonly loadRef = signal('');
  readonly published = signal<Published | null>(null);
  readonly categories = signal<Category[]>([]);
  readonly options = signal<SellingOptions | null>(null);
  readonly email = computed(() => this.auth.member()?.email ?? '');
  readonly photos = signal<PhotoTile[]>([]);
  readonly maxPhotos = computed(() => this.options()?.maxPhotos ?? 8);
  /** The field error, then why the last refused file was refused: "Add at least one photo. Photos must be 10 MB or smaller." */
  readonly photoError = computed(() => {
    const rejected = this.photos().filter((p) => p.state === 'rejected');
    const parts = [this.errors().photos, rejected.at(-1)?.message].filter((m): m is string => !!m);
    const unique = [...new Set(parts)];
    return unique.length > 1 ? unique.map((m) => `${m}.`).join(' ') : (unique[0] ?? null);
  });

  private readonly savedReference = signal<string | null>(null);
  private nextPhotoKey = 0;

  readonly value = toSignal(this.form.valueChanges.pipe(map(() => this.form.getRawValue() as ListingFormValue)), {
    initialValue: this.form.getRawValue() as ListingFormValue,
  });
  readonly category = computed(() => this.categories().find((c) => c.name === this.value().category) ?? null);
  readonly confirmText = computed(() => confirmLabel(this.value().category));
  readonly isUsedFair = computed(() => this.value().condition === 'Used - Fair');
  readonly titleCount = computed(() => `${this.value().title.length} / 80`);
  readonly descriptionCount = computed(() => `${this.value().description.length.toLocaleString('en-US')} / 2,000`);
  readonly earnings = computed(() =>
    estimateEarnings(this.value().price, this.value().shipping, this.options()?.feePercent ?? 0),
  );
  readonly summary = computed<SummaryError[]>(() =>
    FIELD_IDS.filter((id) => this.errors()[id]).map((id) => ({ fieldId: id, message: this.errors()[id]! })),
  );

  constructor() {
    this.form.controls.category.valueChanges.pipe(takeUntilDestroyed()).subscribe((name) => {
      const subcategory = this.form.controls.subcategory;
      const category = this.categories().find((c) => c.name === name);
      if (!category) {
        subcategory.setValue('');
        subcategory.disable();
        return;
      }
      if (!category.subcategories.includes(subcategory.value)) subcategory.setValue('');
      subcategory.enable();
    });
  }

  ngOnInit(): void {
    void this.open();
  }

  async open(): Promise<void> {
    this.view.set('loading');
    await this.auth.load();
    const member = this.auth.member();
    if (!member) {
      await this.router.navigate(['/sign-in'], { queryParams: { returnUrl: this.router.url }, replaceUrl: true });
      return;
    }
    if (!member.emailVerified) {
      this.view.set('unverified');
      return;
    }
    const catalogue = await this.selling.load();
    if (!catalogue.ok) {
      this.showLoadError(catalogue.problem);
      return;
    }
    this.categories.set(catalogue.value.categories);
    this.options.set(catalogue.value.options);
    const reference = this.reference();
    if (reference) {
      const draft = await this.listings.getMine(reference);
      if (!draft.ok) {
        this.showLoadError(draft.problem);
        return;
      }
      this.fill(draft.value);
    }
    this.view.set('form');
  }

  /** Uploads the chosen files into the free slots; files over 10 MB are refused before sending. */
  addPhotos(files: File[]): void {
    const free = this.maxPhotos() - this.photos().filter((p) => p.state !== 'rejected').length;
    for (const file of files.slice(0, Math.max(free, 0))) {
      const key = `photo-${this.nextPhotoKey++}`;
      if (file.size > MAX_PHOTO_BYTES) {
        this.photos.update((tiles) => [...tiles, this.rejectedTile(key, file, 'Photos must be 10 MB or smaller')]);
        continue;
      }
      this.photos.update((tiles) => [...tiles, { key, state: 'uploading', name: file.name }]);
      void this.photoUploads.upload(file).then((result) => {
        const tile: PhotoTile = result.ok
          ? { key, state: 'ready', id: result.value.id, src: result.value.url }
          : this.rejectedTile(key, file, this.uploadMessage(result.problem, file));
        this.photos.update((tiles) => tiles.map((t) => (t.key === key ? tile : t)));
      });
    }
  }

  removePhoto(key: string): void {
    this.photos.update((tiles) => tiles.filter((t) => t.key !== key));
  }

  /** Moves a photo among the photos; refused files stay after them. */
  movePhoto({ from, to }: UploaderMove): void {
    this.photos.update((tiles) => {
      const photos = tiles.filter((t) => t.state !== 'rejected');
      const [moved] = photos.splice(from, 1);
      photos.splice(to, 0, moved);
      return [...photos, ...tiles.filter((t) => t.state === 'rejected')];
    });
  }

  async saveDraft(): Promise<void> {
    if (this.busy()) return;
    const value = this.form.getRawValue() as ListingFormValue;
    if (!this.accept(this.check(value, 'draft'))) return;
    this.busy.set('draft');
    const saved = await this.save(value);
    this.busy.set(null);
    if (saved) this.draftSaved.set(true);
  }

  async publish(): Promise<void> {
    if (this.busy()) return;
    const value = this.form.getRawValue() as ListingFormValue;
    if (!this.accept(this.check(value, 'publish'))) return;
    this.busy.set('publish');
    const saved = await this.save(value);
    if (!saved) {
      this.busy.set(null);
      return;
    }
    const result = await this.listings.publish(saved.reference, value.confirm);
    this.busy.set(null);
    if (!result.ok) {
      this.showProblem(result.problem, 'Couldn’t publish your listing');
      return;
    }
    const size = saved.size.replace("'", '’');
    this.published.set({
      reference: saved.reference,
      title: saved.title ?? '',
      meta: [saved.brand, size, saved.price === null ? null : formatUsd(saved.price)].filter(Boolean).join(' · '),
      payoutOnboardingRequired: result.value.payoutOnboardingRequired,
    });
    this.view.set('success');
  }

  /** "Sell another": a blank form for a new listing. */
  reset(): void {
    this.form.reset();
    this.photos.set([]);
    this.savedReference.set(null);
    this.published.set(null);
    this.errors.set({});
    this.draftSaved.set(false);
    this.failure.set(null);
    this.view.set('form');
  }

  openVerifyPrompt(): void {
    this.dialogs.open(VerifyEmailPromptComponent, { email: this.email() });
  }

  /** Creates the draft the first time, then updates it in place. */
  private async save(value: ListingFormValue): Promise<MyListing | null> {
    const details = { ...toDetails(value), photoIds: this.photoIds() };
    const reference = this.savedReference();
    const result = reference
      ? await this.listings.updateDraft(reference, details)
      : await this.listings.createDraft(details);
    if (!result.ok) {
      this.showProblem(result.problem, 'Couldn’t save your draft');
      return null;
    }
    this.savedReference.set(result.value.reference);
    return result.value;
  }

  private photoIds(): string[] {
    return this.photos().flatMap((p) => (p.state === 'ready' && p.id ? [p.id] : []));
  }

  /** Client checks, plus a wait while photos are still uploading. */
  private check(value: ListingFormValue, mode: 'draft' | 'publish'): FieldErrors {
    const errors = checkListing(value, mode, this.photoIds().length);
    if (this.photos().some((p) => p.state === 'uploading')) {
      errors.photos = 'Wait for your photos to finish uploading';
    }
    return errors;
  }

  private rejectedTile(key: string, file: File, message: string): PhotoTile {
    return { key, state: 'rejected', name: file.name, size: formatFileSize(file.size), message };
  }

  /** 413, 415 and 422 carry the message to show; anything else is a failed upload. */
  private uploadMessage(problem: ApiProblem, file: File): string {
    if ([413, 415, 422].includes(problem.status)) return problem.title;
    return `Couldn’t upload ${file.name}. Try again.`;
  }

  /** Shows client errors; true when there are none. */
  private accept(errors: FieldErrors): boolean {
    this.errors.set(errors);
    this.draftSaved.set(false);
    this.failure.set(null);
    return Object.keys(errors).length === 0;
  }

  private showProblem(problem: ApiProblem, heading: string): void {
    if (problem.status === 422) {
      const errors: FieldErrors = {};
      for (const [field, error] of Object.entries(problem.errors)) {
        const id = SERVER_FIELDS[field];
        if (id) errors[id] ??= error.message;
      }
      this.errors.set(errors);
    } else if (problem.status === 429) {
      this.view.set('limited');
    } else if (problem.status === 403 && problem.code === 'EMAIL_NOT_VERIFIED') {
      this.view.set('unverified');
    } else if (problem.status === 401) {
      void this.router.navigate(['/sign-in'], { queryParams: { returnUrl: this.router.url } });
    } else {
      const network = problem.status === 0;
      this.failure.set({
        heading,
        text: network ? 'Check your connection.' : 'Something went wrong on our side.',
        ref: network ? '' : shortRef(problem.correlationId),
      });
    }
  }

  private showLoadError(problem: ApiProblem): void {
    this.loadRef.set(shortRef(problem.correlationId));
    this.view.set('error');
  }

  private fill(listing: MyListing): void {
    this.savedReference.set(listing.reference);
    this.photos.set(listing.photos.map((photo: Photo) => this.readyTile(photo)));
    this.form.patchValue({
      category: listing.category,
      subcategory: listing.subcategory ?? '',
      title: listing.title ?? '',
      brand: listing.brand ?? '',
      condition: listing.condition ?? '',
      flaws: listing.flaws ?? '',
      description: listing.description ?? '',
      price: listing.price === null ? '' : listing.price.toFixed(2),
      shipping: listing.shippingCost === null ? '' : listing.shippingCost.toFixed(2),
    });
  }

  private readyTile(photo: Photo): PhotoTile {
    return { key: `photo-${this.nextPhotoKey++}`, state: 'ready', id: photo.id, src: photo.url };
  }
}
