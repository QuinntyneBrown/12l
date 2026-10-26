# Screen composition

Sources: `docs/mocks/` (every page, dialog and notification in every state, see
[`docs/mocks/index.html`](mocks/index.html)) and the component catalogue in
[`docs/design-system/README.md`](design-system/README.md), which the `components` library
(`src/frontend/projects/components/`, alias `@12l/components`) implements one to one.

"Library" names the `tl-*` components, directives and services of `@12l/components` that a
screen is composed of. "Local UI" is markup a feature library builds itself because no
catalogue component covers it; it is listed here so that catalogue change control can pick
it up. Mock-only chrome (`mock-bar`, `mock-note`, the theme toggle) is excluded.

The catalogue holds the shell components (skip link, top bar, footer, toast, sheet, button,
link, form field) and the components create-listing added (alert, center state, choice,
dialog with `DialogService`, earnings, error summary, fixed size, icon, input group, item row,
segmented control, size tag, spinner) and the components browse-catalog added (empty
state, listing card with listing grid, load more). Feature screens not built yet are inventoried below
with their states and marked **not yet composed**; each is composed when its journey is
implemented, and the catalogue grows in the same change.

## Shell

| Part | Library components | Local UI |
|---|---|---|
| App shell (`shell: 'app'`) | `tl-skip-link`, `tl-top-bar` (guest, member), `tl-footer`, `tl-toast-region` | `<main id="main" tabindex="-1">` with the router outlet, in `projects/twelvel` |
| Auth shell (`shell: 'auth'`) | `tl-skip-link`, `tl-logo` (lg), `tl-toast-region` | `.auth-layout` with `<main id="main" class="auth-card" tabindex="-1">` and the router outlet, in `projects/twelvel`; chosen by route `data.shell = 'auth'` |
| Admin shell (`shell: 'admin'`) | `tl-skip-link`, `tl-top-bar` (admin variant), `tl-toast-region` | Not yet composed |
| Bare shell (`shell: 'bare'`) | `tl-skip-link`, `tl-top-bar` (bare variant), `tl-toast-region` | Not yet composed |
| Nav-menu sheet (`dialogs/nav-menu`: default, guest) | `tl-sheet`, `tl-button`, `tl-link` | Not yet composed |
| Toast region (`notifications/toast`: info, success, warning, danger, with-action, stacked) | `tl-toast-region`, `tl-toast`, `ToastService` | None |
| System banner (`notifications/system-banner`: info, success, warning, danger) | `tl-system-banner` (not in the catalogue yet) | Not yet composed |

## Shared local components

| Item | Used by | Notes |
|---|---|---|
| Logo (inline SVG) | top bar, footer, sheet, auth shell | Lives in `@12l/components` as `tl-logo`; sizes sm, md, lg |

## Pages

### Account — `/account` (`pages/account`: default, loading, empty, error, unverified)

- Library: not yet composed
- Local: not yet composed

### Edit profile — `/account/profile` (`pages/edit-profile`: default, invalid, submitting, success, loading, error)

- Library: not yet composed
- Local: not yet composed

### Forgot password — `/forgot-password` (`pages/forgot-password`: default, invalid, submitting, success, error)

- Library: not yet composed
- Local: not yet composed

### Email settings — `/account/emails` (`pages/notification-settings`: default, submitting, success, loading, error)

- Library: not yet composed
- Local: not yet composed

### Member profile — `/members/{displayName}` (`pages/profile`: default, own, empty, loading, error, unavailable, long)

- Library: not yet composed
- Local: not yet composed

### Join — `/join` (`pages/register`: default, invalid, submitting, success, error)

Auth shell. `@12l/accounts` `JoinPage`.

- Library: `tl-form-field` (display name, email, password), `tl-choice` (age, terms), `tl-error-summary` (invalid), `tl-alert` (error with reference; success "Link sent" and warning "Too many requests" after Resend email), `tl-button` (Join 12L primary lg block with busy; Browse while you wait; Resend email link), `tl-icon` (mail)
- Local: heading block with the lead line; the mail icon circle and "We sent a link to …" paragraph of the success state

### Reset password — `/reset-password` (`pages/reset-password`: default, invalid, submitting, success, expired, error)

- Library: not yet composed
- Local: not yet composed

### Session expired — `/sign-in?expired=1` (`pages/session-expired`: default)

- Library: not yet composed
- Local: not yet composed

### Settings — `/account/settings` (`pages/settings`: default, loading, error)

- Library: not yet composed
- Local: not yet composed

### Sign in — `/sign-in` (`pages/sign-in`: default, return, invalid, submitting, locked, error)

Auth shell. `@12l/accounts` `SignInPage`; `returnUrl` keeps the page the member came from.
When `returnUrl` is a listing (`/items/{id}`) the heading reads "Sign in to buy" with the line
"You’ll go straight back to the item." (state return). The
`locked` state and the "Forgot password?" link arrive with account lockout and password reset.

- Library: `tl-form-field` (email, password), `tl-alert` (invalid: "Email or password is incorrect"; error with reference), `tl-button` (Sign in primary lg block with busy)
- Local: heading block; "New to 12L? Join" line

### Verify email — `/verify` (`pages/verify-email`: default, loading, expired, used, error)

Auth shell. `@12l/accounts` `VerifyEmailPage` reads `token` from the query string.

- Library: `tl-spinner` (loading), `tl-button` (Start shopping, Sell an item, Send a new link, Sign in, Try again), `tl-alert` (Link sent, Too many requests), `tl-icon` (refresh)
- Local: heading block with the lead line; the reference line of the error state

### Catalog — `/` (`pages/catalog`: default, guest, category, search, filtered, loading, empty, no-results, error, offline)

Built by browse-catalog in `@12l/catalog` (`src/lib/catalog/`) for the states default, guest,
category (`/shoes`, `/tops`, `/outerwear`, `/bottoms`), loading, empty, error and offline. The
states search, filtered and no-results, the filter sidebar, the filters toggle, the sort select
and the subcategory chips belong to search-and-filter-catalog and are not yet composed.

- Library: `tl-listing-grid` (cards and the 8-card loading skeleton) with `tl-listing-card`,
  `tl-size-tag` (lg, category header), `tl-load-more`, `tl-empty-state` (empty: icon `tag`,
  "Sell an item" as `tlButton="primary"`; error: tone error, icon `refresh`, "Try again"),
  `tl-alert` (warning banner with icon `wifi-off` for offline; danger "Couldn’t load more items"
  with a `tlButton="link"` Try again when a next page fails), `tlButton`, `tl-icon`
- Local: the hero (`.hero`, h1 "Size 12. Size L. *Nothing else.*" and lead), the category
  `.page-header`, the `.toolbar` with the polite item count and its text skeleton. The offline
  banner renders at the top of `main`, not above the top bar as in the mock, until
  `tl-system-banner` exists. A failed next page shows an inline danger alert instead of the
  toast in the design, until `ToastService` exists (responsive-accessible-shell).

### Listing detail — `/items/{id}` (`pages/listing-detail`: default, guest, new-seller, reserved, sold, own, loading, error, unavailable)

Built by view-listing-detail in `@12l/catalog` (`src/lib/listing-detail/`) for every state. The
own state shows "Edit listing" only; "Withdraw" and its dialog arrive with
edit-and-withdraw-listing. Sellers show no city until member profiles record one.

- Library: `tl-gallery` (main photo track, dots, thumbnails), `tl-size-tag` (lg), `tl-buy-bar`
  (default and guest: "Buy now" as `tlButton="primary"` lg; own: "Edit listing" with icon
  `edit`; absent for Reserved and Sold), `tl-alert` (reserved: warning, icon `clock`, "In
  someone’s checkout"), `tl-seller-summary` (rating or "New seller"), `tl-listing-grid` (sold:
  "More in size 12" or "More in size L"), `tl-center-state` (unavailable: code "404" and "Shop
  similar items"; error: reference, "Try again" with icon `refresh` and "Back to shop"),
  `tlButton`, `tl-icon`
- Local: the breadcrumb, the info column (`.photo__stamp` Reserved or Sold, `.eyebrow` brand,
  `h1.detail__title`, `.detail__price` line, `.flaws`, description, `dl.facts` with the
  relative `time`), the two-column `.detail` layout and the loading skeleton

### Checkout — `/checkout/{id}` (`pages/checkout`: default, new-address, invalid, non-us, submitting, declined, expired, conflict, loading, error)

Built by checkout-and-pay in `@12l/orders` (`src/lib/checkout/`) for every state; `{id}` is
the listing reference. A refused start for the seller's own, a sold or a missing listing goes
back to `/items/{id}`, and a visitor goes to sign in with checkout as the return URL.

- Library: `tl-reservation-timer` (under the title; its phase drives the banners),
  `tl-alert` (banner warning "Less than a minute left to pay…" and danger "Your reservation
  ended…" with "Start again", both icon `clock`; non-us, declined, total changed and payment
  failure alerts in the form), `tl-error-summary` (invalid), `tl-form-field` (Full name,
  Street address, Apartment, suite (optional), City, State, ZIP code with `inputmode="numeric"`,
  Country), `tl-order-summary`, `tlButton` (primary lg block "Pay $102.34", or "Continue" before
  a total exists, busy while submitting and disabled at zero; ghost "Cancel and release item"),
  `tl-center-state` (conflict: icon `lock`; expired: icon `clock`; error: reference and "Try
  again" with icon `refresh`), `tl-icon`
- Local: `.page-header`, the `.split` layout, the `.checkout-step` sections, the saved-address
  radios (`.option`, `address.address`), `HostedCardFieldsComponent` (the "Card" field, the
  provider's hosted fields from `PAYMENT_FIELDS` in `@12l/api` and the `.secure-note`), the
  "Confirming with your bank…" status line and the loading skeleton

### Order confirmed — `/orders/{id}/confirmed` (`pages/order-confirmation`: default, loading, error)

Built by checkout-and-pay in `@12l/orders` (`src/lib/order-confirmation/`). The "Payment
confirmed" toast of `notifications/reservation-timer` success waits for `ToastService`
(responsive-accessible-shell); the page itself shows the amount and card.

- Library: `tl-item-row` ("Paid $102.34 · Visa ending 4242"), `tlButton` ("View order",
  "Keep shopping"), `tl-center-state` (error: reference, "Try again" and "Go to purchases"),
  `tl-icon` (`check`, `refresh`)
- Local: the `.confirm` block (mark, `.eyebrow` order reference, heading), the
  `ol.next-steps` list and the loading center state with the large spinner

### Order (buyer) — `/orders/{id}` (`pages/order-detail`: default, paid, delivered, completed, cancelled, refunded, problem, loading, error)

Built by ship-order in `@12l/orders` (`src/lib/order-detail/`) for paid ("Waiting to ship"),
default ("On its way"), delivered, cancelled, loading and error. "Ask to cancel", "Report a
problem", "I received it", the expected delivery date, the seller's cancellation reason and the
completed, refunded and problem states are composed by cancel-order, complete-order and
resolve-order-problems.

- Library: `tl-order-timeline`, `tl-tracking-link` (once shipped), `tl-alert` (info "Refunded in
  full" with the amount and card when cancelled), `tl-order-summary` (no visible heading; labelled
  "Order summary"), `tl-center-state` (error, with `tl-button` "Try again" and "Back to purchases")
- Local: the breadcrumb, eyebrow and heading block, the ship-by note ("{seller} ships by {date}.
  If not, you’re refunded automatically."), `OrderPartyComponent` (avatar, "Seller", profile link)
  projected into the summary, and the two-column loading skeleton

### Purchases — `/account/purchases` (`pages/purchases`: default, loading, empty, error)

- Library: not yet composed
- Local: not yet composed

### Sale (seller) — `/sales/{id}` (`pages/sale-detail`: default, shipped, cancel-requested, problem, completed, address-hidden, cancelled, loading, error)

Built by ship-order in `@12l/orders` (`src/lib/sale-detail/`) for default (Paid), shipped,
cancelled, loading and error. "Cancel order", "Relist item", cancel-requested, problem, completed
and address-hidden are composed by cancel-order, complete-order, resolve-order-problems and
protect-personal-data.

- Library: `tl-button` (primary "Add tracking" with icon `truck`, opening the Add tracking
  dialog through `DialogService`), `tl-order-timeline` and `tl-tracking-link` (once shipped),
  `tl-alert` (info "Cancelled · Buyer refunded in full"), `tl-order-summary` (no visible
  heading), `tl-center-state` (error, with "Try again" and "Back to sales")
- Local: the breadcrumb, eyebrow and heading block, "Ship by {date}." lead, the "Ship to"
  address block with its caption, `OrderPartyComponent` ("Buyer") projected into the summary, and
  the loading skeleton

### Sales — `/account/sales` (`pages/sales`: default, loading, empty, error)

- Library: not yet composed
- Local: not yet composed

### Edit listing — `/items/{id}/edit` (`pages/edit-listing`: default, loading, error, invalid, submitting, success, locked)

- Library: not yet composed
- Local: not yet composed

### Your listings — `/account/listings` (`pages/my-listings`: default, filtered, loading, empty, error)

- Library: not yet composed
- Local: not yet composed

### Payouts — `/account/payouts` (`pages/payouts`: default, not-onboarded, loading, empty, error)

- Library: not yet composed
- Local: not yet composed

### Sell an item — `/sell` (`pages/sell`: default, filled, invalid, submitting, draft-saved, success, unverified, limited, error)

App shell. `@12l/listings` `SellPage` at `/sell` and `/sell/{reference}` (continue a draft).
Visitors are sent to `/sign-in?returnUrl=/sell`. The Photos section comes first; each chosen file
uploads at once and a save sends the photo IDs in order. The footer stays visible under the form.

- Library: `tl-photo-uploader` (photos with cover, uploading and rejected tiles, add tile, help and error), `tl-error-summary` (invalid), `tl-alert` (draft-saved success, save or publish failure), `tl-form-field` (category, type, title with counter, brand, flaws, description with counter, price, shipping), `tl-input-group` (`$` addon), `tl-fixed-size` with `tl-size-tag` (after a category is chosen), `tl-segmented` (condition), `tl-earnings`, `tl-choice` (size confirmation), `tl-button` (Save draft, Publish with busy), `tl-center-state` (success, unverified, limited, error) with `tl-item-row` (success panel) and `tl-icon`, `DialogService` (opens the verify-email prompt)
- Local: `.page-header` with the h1, `.sell-form` sections (Photos, Item, Price, confirmation: `.form-section`, `.form-row`), the upload state of each tile and its client size check, the brand `<datalist>`, the sticky `.form-actions` bar, the success panel wrapper and the payouts line

### Forbidden — `/403` (`pages/forbidden`: default)

- Library: not yet composed
- Local: not yet composed

### Maintenance — `(any)` (`pages/maintenance`: default)

- Library: not yet composed
- Local: not yet composed

### Not found — `/*` (`pages/not-found`: default)

- Library: not yet composed
- Local: not yet composed

### Offline — `(any)` (`pages/offline`: default)

- Library: not yet composed
- Local: not yet composed

### Privacy — `/privacy` (`pages/privacy`: default)

- Library: not yet composed
- Local: not yet composed

### Problem detail — `/admin/problems/{id}` (`pages/problem-detail`: default, resolved, loading, error)

- Library: not yet composed
- Local: not yet composed

### Marketplace rules — `/rules` (`pages/rules`: default)

- Library: not yet composed
- Local: not yet composed

### Server error — `/error` (`pages/server-error`: default)

- Library: not yet composed
- Local: not yet composed

### Terms — `/terms` (`pages/terms`: default)

- Library: not yet composed
- Local: not yet composed


## Dialogs

| Dialog (mock folder: states) | Overlay surface | Library components | Local UI |
|---|---|---|---|
| Change password (`dialogs/change-password`: default, invalid, busy, failed) | `DialogService` | not yet composed | not yet composed |
| Close account (`dialogs/close-account`: default, invalid, busy, blocked) | `DialogService` | not yet composed | not yet composed |
| Sign out everywhere (`dialogs/sign-out-everywhere`: default, busy, failed) | `DialogService` | not yet composed | not yet composed |
| Verify email prompt (`dialogs/verify-email-prompt`: default, busy, sent, limited) | `DialogService` | `tl-dialog` (mail icon, description with the email), `tl-alert` (sent success, limited warning) in the top slot, `tl-button` (Not now, Resend link with busy, Done) | `VerifyEmailPromptComponent` in `@12l/listings`; it moves to a shared place when checkout also opens it |
| Filters (`dialogs/filters`: default, invalid, busy) | `tl-sheet` | not yet composed | not yet composed |
| Menu (`dialogs/nav-menu`: default, guest) | `tl-sheet` | `tl-sheet`, `tl-button`, `tl-link` | not yet composed |
| Add tracking (`dialogs/add-tracking`: default, invalid, busy, failed) | `DialogService` | `tl-dialog` (description "We’ll email {buyer} the tracking link."), `tl-form-field` (Carrier select, focused on open; Tracking number with the inline error), `tl-alert` (danger "That didn’t go through" in the top slot), `tl-button` (Cancel, disabled while busy; primary "Mark as shipped" with busy, "Try again" after a failure) | `AddTrackingDialog` in `@12l/orders` |
| Cancel order (`dialogs/cancel-order`: default, invalid, busy, failed) | `DialogService` | not yet composed | not yet composed |
| Confirm receipt (`dialogs/confirm-receipt`: default, busy, failed) | `DialogService` | not yet composed | not yet composed |
| Relist item (`dialogs/relist`: default, busy) | `DialogService` | not yet composed | not yet composed |
| Report a problem (`dialogs/report-problem`: default, invalid, busy, failed) | `DialogService` | not yet composed | not yet composed |
| Ask to cancel (`dialogs/request-cancellation`: default, busy, failed) | `DialogService` | not yet composed | not yet composed |
| Respond to cancellation (`dialogs/respond-cancellation`: default, busy, failed) | `DialogService` | not yet composed | not yet composed |
| Withdraw listing (`dialogs/withdraw-listing`: default, busy, failed) | `DialogService` | not yet composed | not yet composed |
| Cookie settings (`dialogs/cookie-settings`: default, analytics-on) | `DialogService` | not yet composed | not yet composed |
| Resolve problem (`dialogs/resolve-problem`: default, invalid, busy) | `DialogService` | not yet composed | not yet composed |

## Notifications

| Notification (mock folder: states) | Surface | Library components | Local UI |
|---|---|---|---|
| Account banner (`notifications/account-banner`: info, success, warning) | banner above the top bar | not yet composed | not yet composed |
| Reservation timer (`notifications/reservation-timer`: info, warning, danger, success) | timer under the checkout title; warning and danger banners at the top of checkout | `tl-reservation-timer`, `tl-alert` (banner, icon `clock`) | None; success is the confirmation page until `ToastService` exists |
| Payout banner (`notifications/payout-banner`: info, success, warning, danger) | banner above the top bar | not yet composed | not yet composed |
| Toasts (`notifications/toast`: info, success, warning, danger, with-action, stacked) | toast region | `tl-toast-region`, `tl-toast`, `ToastService` | None |
| Cookie consent (`notifications/cookie-consent`: info, success) | fixed bottom panel | not yet composed | not yet composed |
| System notices (`notifications/system-banner`: info, success, warning, danger) | banner above the top bar | not yet composed | not yet composed |

## Summary of local UI to build

1. `main#main` with the router outlet and the home placeholder (`projects/twelvel`).
2. The auth layout of the auth shell (`projects/twelvel`).
3. Heading blocks of the auth pages and the sell page header, form sections and sticky actions bar.
4. Everything marked "not yet composed" is composed, and its library components added to the catalogue, when its journey is implemented.
