import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';

import { API_BASE_URL } from '../api-base-url';
import { ApiResult, toResult } from '../api-result';

/** The cover photo of a card: WebP and JPEG srcsets of the 400, 800 and 1600 px versions (L2-059). */
export interface CardPhoto {
  width: number;
  height: number;
  alt: string;
  src: string;
  webp: string;
  jpeg: string;
}

/** One catalog card. price is a two-place decimal string such as "85.00" (L2-018). */
export interface ListingCard {
  id: string;
  reference: string;
  title: string;
  brand: string;
  category: string;
  subcategory: string | null;
  sizeLabel: string;
  condition: string;
  price: string;
  status: 'Active' | 'Reserved';
  publishedAt: string;
  coverPhoto: CardPhoto | null;
}

export interface CatalogPage {
  items: ListingCard[];
  page: number;
  pageSize: number;
  totalCount: number;
}

/** How the person viewing relates to a listing; decides whether the page offers Buy now (L2-026). */
export type ViewerRelation = 'Anonymous' | 'Seller' | 'OtherMember';

/** One listing as its detail page shows it (L2-025). Money values are two-place decimal strings. */
export interface ListingDetail {
  id: string;
  reference: string;
  title: string;
  brand: string;
  category: string;
  subcategory: string | null;
  sizeLabel: string;
  condition: string;
  flaws: string | null;
  description: string;
  price: string;
  shippingCost: string;
  total: string;
  status: 'Draft' | 'Active' | 'Reserved' | 'Sold' | 'Removed';
  publishedAt: string;
  photos: CardPhoto[];
  seller: {
    displayName: string;
    completedSalesCount: number;
    ratingAverage: number | null;
    publishedReviewCount: number;
  };
  viewer: { relation: ViewerRelation };
}

/** Typed client for the public catalog: GET /api/catalog/listings and /api/catalog/listings/{reference}. */
@Injectable({ providedIn: 'root' })
export class CatalogApi {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = inject(API_BASE_URL);

  /** One page of Active and Reserved listings, newest first, optionally in one category. */
  listings(page: number, category: string | null = null): Promise<ApiResult<CatalogPage>> {
    let params = new HttpParams();
    if (page > 1) params = params.set('page', page);
    if (category) params = params.set('category', category);
    return toResult(this.http.get<CatalogPage>(`${this.baseUrl}/catalog/listings`, { params }));
  }

  /** One listing; 404 LISTING_NOT_FOUND when it is unknown or hidden from this viewer. */
  listing(reference: string): Promise<ApiResult<ListingDetail>> {
    return toResult(this.http.get<ListingDetail>(`${this.baseUrl}/catalog/listings/${encodeURIComponent(reference)}`));
  }
}
