# 12L HTML mocks

Static HTML mocks of every 12L page, dialog and notification, in every state,
light and dark, from 320 px phones to desktop. They are the product on disk
before the Angular app exists: open them, click through them, tab through them.

## Open the mocks

- Open [`index.html`](index.html) from disk (no server needed). It lists every screen and links each state.
- Every mock has a bar at the bottom with its sibling states and a theme toggle (or press `t`).
- `?theme=dark` or `?theme=light` forces a theme; `?chrome=0` hides the mock bar and notes so the page looks exactly like the product.

## Design direction

Taken from the logo in [`docs/design-system/assets/`](../design-system/assets/logo.svg):

| From the logo | In the mocks |
| --- | --- |
| Ink `#0B0B0B` | Text, primary buttons, size tags. Dark theme flips to an ink canvas. |
| Paper `#F4F1EA` | Warm canvas and sunken surfaces; the text colour in dark theme. |
| Signal red `#E1251B` (the L) | Used sparingly: the logo, the current-page bar, the hero's last words. Never body text and never an error colour. |
| Sharp corners, one 45° cut on the L | Square controls and photos; the `.size-tag` (US **12** / **L**) carries the same chamfer. |
| Heavy, tight numerals | Black-weight, tightly tracked headings. |

Principles: lots of white space, one primary action per screen, short real copy
and nothing that fills space. Product photos keep a light studio backdrop in both
themes, the way real photos would.

## Cast and catalog

"Today" is **Sun 25 Oct 2026**. Every mock uses this data (source: [`_build/data.py`](_build/data.py)).

| Member | Real name | City | Role in the story |
| --- | --- | --- | --- |
| `marcus_12` | Marcus Bell | Brooklyn, NY | The signed-in member. Buys and sells. 4.8 (23 reviews), 19 sales. |
| `kicks_12` | Dre Okafor | Atlanta, GA | Top sneaker seller. 4.9 (128 reviews), 141 sales. |
| `vintage_lou` | Lou Ferreira | Portland, OR | Workwear and outerwear seller. 4.7 (41 reviews). |
| `tall_tom` | Tom Reyes | Denver, CO | Buyer of Marcus's hoodie. No listings. |
| `jaybird` | Jay Park | Chicago, IL | New seller, no completed sales ("New seller"). |
| Ana Ruiz | — | — | Administrator (moderation, audit log). |

Fourteen listings, all men's US 12 or men's L: Nike Air Max 90, New Balance 990v6,
Adidas Samba OG, Red Wing Iron Ranger, Allen Edmonds Park Avenue, Birkenstock Arizona
(Used - Fair, with flaws), Patagonia Better Sweater, Champion Reverse Weave hoodie,
Uniqlo Oxford shirt, Everlane tee, Carhartt Detroit jacket, Barbour Bedale (Reserved),
Arc'teryx Gamma LT pants, Nike Tech Fleece shorts.

Orders: `12L-48213` (Marcus buys the Red Wings, Shipped), `12L-48140` (Patagonia, Delivered),
`12L-47790` (Samba, Completed), `12L-48302` (Marcus sells the hoodie to Tom, Paid, ship by Fri 30 Oct),
`12L-47511` (Tech Fleece shorts, Completed, payout $33.30 after the 10% fee of $3.70).

## How the mocks are built

The HTML files are generated so that ~250 mocks share one shell, one token file
and one component kit. Since 25 Oct 2026 the tokens and kit live in the
[design system](../design-system/README.md); every mock loads
`docs/design-system/tokens/tokens.css` and `docs/design-system/assets/components.css`
directly, so a change there shows up here.

```
docs/mocks/
  assets/tokens.css    forwards to docs/design-system/tokens/tokens.css (kept for the gallery page)
  assets/ui.css        forwards to docs/design-system/assets/components.css
  assets/mock.css      mock chrome only (state bar, notes); never part of the product
  assets/items/*.svg   product illustrations used as listing photos
  _build/mk.py         shell, components and helpers
  _build/data.py       cast and catalog
  _build/screens_*.py  one module per area: catalog, accounts, selling, orders, system
  _build/build.py      renders every state, writes manifest.json, validates links
```

Change a screen in its `screens_*.py`, then rebuild and re-check:

```sh
python3 docs/mocks/_build/build.py
python3 .claude/skills/writing-html-mocks/scripts/check_mocks.py docs/mocks --write
python3 .claude/skills/writing-html-mocks/scripts/screenshot_mocks.py docs/mocks   # PNGs in docs/mocks/.cache (not committed)
```

## Open questions and assumptions

- **Notifications are email only** (L1-011, L2-042). There is no in-app notification centre, so none is mocked; in-app feedback is toasts and banners. Email templates are not mocked here.
- **Home is the catalog.** `/` shows a one-line hero above the catalog rather than a separate landing page.
- **Payment provider UI** is shown as hosted card fields inside checkout; the provider's own pages (payout onboarding, 3-D Secure) are out of scope.
- **Sales tax** is shown as a single line computed at checkout; rates come from the provider.
- **Category pages** share the catalog template; only Shoes is mocked as its own state.
- **Admin sign-in** is the member sign-in followed by the TOTP step (`admin-verify`).
- **Legal copy** on Terms and Privacy summarises the rules in the specs; final wording comes from counsel.
- **Fonts**: headings ask for Archivo then Inter, falling back to the system sans. Mocks load no web fonts so they open offline.

## Coverage

<!-- coverage:start -->

Legend: ✅ mock exists · ➖ not applicable (reason in manifest) · ❌ missing

### Pages

| Screen | default | loading | empty | error | unverified | suspended | invalid | submitting | success | own | unavailable | long | expired | return | locked | used | guest | category | search | filtered | no-results | offline | new-seller | reserved | sold | new-address | non-us | declined | conflict | paid | delivered | completed | cancelled | refunded | problem | shipped | cancel-requested | address-hidden | not-onboarded | filled | draft-saved | limited | forbidden | resolved | hidden | Requirements |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Account (`account`) | [✅](pages/account/default.html) | [✅](pages/account/loading.html) | [✅](pages/account/empty.html) | [✅](pages/account/error.html) | [✅](pages/account/unverified.html) | [✅](pages/account/suspended.html) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `L2-003`, `L2-002`, `L2-046` |
| Edit profile (`edit-profile`) | [✅](pages/edit-profile/default.html) | [✅](pages/edit-profile/loading.html) | ➖ | [✅](pages/edit-profile/error.html) |  |  | [✅](pages/edit-profile/invalid.html) | [✅](pages/edit-profile/submitting.html) | [✅](pages/edit-profile/success.html) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `L2-004`, `L2-017` |
| Forgot password (`forgot-password`) | [✅](pages/forgot-password/default.html) | ➖ | ➖ | [✅](pages/forgot-password/error.html) |  |  | [✅](pages/forgot-password/invalid.html) | [✅](pages/forgot-password/submitting.html) | [✅](pages/forgot-password/success.html) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `L2-009` |
| Email settings (`notification-settings`) | [✅](pages/notification-settings/default.html) | [✅](pages/notification-settings/loading.html) | ➖ | [✅](pages/notification-settings/error.html) |  |  |  | [✅](pages/notification-settings/submitting.html) | [✅](pages/notification-settings/success.html) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `L2-042`, `L2-043` |
| Member profile (`profile`) | [✅](pages/profile/default.html) | [✅](pages/profile/loading.html) | [✅](pages/profile/empty.html) | [✅](pages/profile/error.html) |  |  |  |  |  | [✅](pages/profile/own.html) | [✅](pages/profile/unavailable.html) | [✅](pages/profile/long.html) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `L2-041`, `L2-040`, `L2-039`, `L2-044`, `L2-054` |
| Join (`register`) | [✅](pages/register/default.html) | ➖ | ➖ | [✅](pages/register/error.html) |  |  | [✅](pages/register/invalid.html) | [✅](pages/register/submitting.html) | [✅](pages/register/success.html) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `L2-001`, `L2-002`, `L2-051`, `L2-065` |
| Reset password (`reset-password`) | [✅](pages/reset-password/default.html) | ➖ | ➖ | [✅](pages/reset-password/error.html) |  |  | [✅](pages/reset-password/invalid.html) | [✅](pages/reset-password/submitting.html) | [✅](pages/reset-password/success.html) |  |  |  | [✅](pages/reset-password/expired.html) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `L2-009`, `L2-001` |
| Session expired (`session-expired`) | [✅](pages/session-expired/default.html) | ➖ | ➖ | ➖ |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `L2-008` |
| Settings (`settings`) | [✅](pages/settings/default.html) | [✅](pages/settings/loading.html) | ➖ | [✅](pages/settings/error.html) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `L2-005`, `L2-008`, `L2-009`, `L2-055`, `L2-056` |
| Sign in (`sign-in`) | [✅](pages/sign-in/default.html) | ➖ | ➖ | [✅](pages/sign-in/error.html) |  |  | [✅](pages/sign-in/invalid.html) | [✅](pages/sign-in/submitting.html) |  |  |  |  |  | [✅](pages/sign-in/return.html) | [✅](pages/sign-in/locked.html) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `L2-006`, `L2-007`, `L2-026`, `L2-065` |
| Verify email (`verify-email`) | [✅](pages/verify-email/default.html) | [✅](pages/verify-email/loading.html) | ➖ | [✅](pages/verify-email/error.html) |  |  |  |  |  |  |  |  | [✅](pages/verify-email/expired.html) |  |  | [✅](pages/verify-email/used.html) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `L2-002` |
| Catalog (`catalog`) | [✅](pages/catalog/default.html) | [✅](pages/catalog/loading.html) | [✅](pages/catalog/empty.html) | [✅](pages/catalog/error.html) |  |  |  |  |  |  |  |  |  |  |  |  | [✅](pages/catalog/guest.html) | [✅](pages/catalog/category.html) | [✅](pages/catalog/search.html) | [✅](pages/catalog/filtered.html) | [✅](pages/catalog/no-results.html) | [✅](pages/catalog/offline.html) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `L2-022`, `L2-023`, `L2-024`, `L2-059`, `L2-061`, `L2-062` |
| Listing detail (`listing-detail`) | [✅](pages/listing-detail/default.html) | [✅](pages/listing-detail/loading.html) | ➖ | [✅](pages/listing-detail/error.html) |  |  |  |  |  | [✅](pages/listing-detail/own.html) | [✅](pages/listing-detail/unavailable.html) |  |  |  |  |  | [✅](pages/listing-detail/guest.html) |  |  |  |  |  | [✅](pages/listing-detail/new-seller.html) | [✅](pages/listing-detail/reserved.html) | [✅](pages/listing-detail/sold.html) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `L2-025`, `L2-026`, `L2-028`, `L2-016`, `L2-063`, `L2-065` |
| Checkout (`checkout`) | [✅](pages/checkout/default.html) | [✅](pages/checkout/loading.html) | ➖ | [✅](pages/checkout/error.html) |  |  | [✅](pages/checkout/invalid.html) | [✅](pages/checkout/submitting.html) |  |  |  |  | [✅](pages/checkout/expired.html) |  |  |  |  |  |  |  |  |  |  |  |  | [✅](pages/checkout/new-address.html) | [✅](pages/checkout/non-us.html) | [✅](pages/checkout/declined.html) | [✅](pages/checkout/conflict.html) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `L2-027`, `L2-028`, `L2-029`, `L2-030`, `L2-063`, `L2-065` |
| Order confirmed (`order-confirmation`) | [✅](pages/order-confirmation/default.html) | [✅](pages/order-confirmation/loading.html) | ➖ | [✅](pages/order-confirmation/error.html) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `L2-030`, `L2-033` |
| Order (buyer) (`order-detail`) | [✅](pages/order-detail/default.html) | [✅](pages/order-detail/loading.html) | ➖ | [✅](pages/order-detail/error.html) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | [✅](pages/order-detail/paid.html) | [✅](pages/order-detail/delivered.html) | [✅](pages/order-detail/completed.html) | [✅](pages/order-detail/cancelled.html) | [✅](pages/order-detail/refunded.html) | [✅](pages/order-detail/problem.html) |  |  |  |  |  |  |  |  |  |  | `L2-032`, `L2-033`, `L2-034`, `L2-035`, `L2-036`, `L2-038`, `L2-039` |
| Purchases (`purchases`) | [✅](pages/purchases/default.html) | [✅](pages/purchases/loading.html) | [✅](pages/purchases/empty.html) | [✅](pages/purchases/error.html) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `L2-037` |
| Sale (seller) (`sale-detail`) | [✅](pages/sale-detail/default.html) | [✅](pages/sale-detail/loading.html) | ➖ | [✅](pages/sale-detail/error.html) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | [✅](pages/sale-detail/completed.html) | [✅](pages/sale-detail/cancelled.html) |  | [✅](pages/sale-detail/problem.html) | [✅](pages/sale-detail/shipped.html) | [✅](pages/sale-detail/cancel-requested.html) | [✅](pages/sale-detail/address-hidden.html) |  |  |  |  |  |  |  | `L2-031`, `L2-032`, `L2-033`, `L2-035`, `L2-036`, `L2-037` |
| Sales (`sales`) | [✅](pages/sales/default.html) | [✅](pages/sales/loading.html) | [✅](pages/sales/empty.html) | [✅](pages/sales/error.html) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `L2-037`, `L2-033` |
| Edit listing (`edit-listing`) | [✅](pages/edit-listing/default.html) | [✅](pages/edit-listing/loading.html) | ➖ | [✅](pages/edit-listing/error.html) |  |  | [✅](pages/edit-listing/invalid.html) | [✅](pages/edit-listing/submitting.html) | [✅](pages/edit-listing/success.html) |  |  |  |  |  | [✅](pages/edit-listing/locked.html) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `L2-015`, `L2-016`, `L2-017`, `L2-018`, `L2-020`, `L2-013` |
| Your listings (`my-listings`) | [✅](pages/my-listings/default.html) | [✅](pages/my-listings/loading.html) | [✅](pages/my-listings/empty.html) | [✅](pages/my-listings/error.html) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | [✅](pages/my-listings/filtered.html) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `L2-019`, `L2-021` |
| Payouts (`payouts`) | [✅](pages/payouts/default.html) | [✅](pages/payouts/loading.html) | [✅](pages/payouts/empty.html) | [✅](pages/payouts/error.html) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | [✅](pages/payouts/not-onboarded.html) |  |  |  |  |  |  | `L2-031` |
| Sell an item (`sell`) | [✅](pages/sell/default.html) | ➖ | ➖ | [✅](pages/sell/error.html) | [✅](pages/sell/unverified.html) | [✅](pages/sell/suspended.html) | [✅](pages/sell/invalid.html) | [✅](pages/sell/submitting.html) | [✅](pages/sell/success.html) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | [✅](pages/sell/filled.html) | [✅](pages/sell/draft-saved.html) | [✅](pages/sell/limited.html) |  |  |  | `L2-003`, `L2-011`, `L2-012`, `L2-014`, `L2-015`, `L2-016`, `L2-017`, `L2-018`, `L2-019`, `L2-031`, `L2-051`, `L2-063` |
| Admin verification (`admin-verify`) | [✅](pages/admin-verify/default.html) | ➖ | ➖ | [✅](pages/admin-verify/error.html) |  |  | [✅](pages/admin-verify/invalid.html) | [✅](pages/admin-verify/submitting.html) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `L2-047`, `L2-006` |
| Audit log (`audit-log`) | [✅](pages/audit-log/default.html) | [✅](pages/audit-log/loading.html) | [✅](pages/audit-log/empty.html) | [✅](pages/audit-log/error.html) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | [✅](pages/audit-log/no-results.html) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `L2-047` |
| Forbidden (`forbidden`) | [✅](pages/forbidden/default.html) | ➖ | ➖ | ➖ |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `L2-010`, `L2-068` |
| Maintenance (`maintenance`) | [✅](pages/maintenance/default.html) | ➖ | ➖ | ➖ |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `L2-066` |
| Member admin (`member-admin`) | [✅](pages/member-admin/default.html) | [✅](pages/member-admin/loading.html) | ➖ | [✅](pages/member-admin/error.html) |  | [✅](pages/member-admin/suspended.html) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `L2-046`, `L2-047` |
| Moderation queue (`moderation-queue`) | [✅](pages/moderation-queue/default.html) | [✅](pages/moderation-queue/loading.html) | [✅](pages/moderation-queue/empty.html) | [✅](pages/moderation-queue/error.html) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | [✅](pages/moderation-queue/forbidden.html) |  |  | `L2-045`, `L2-036`, `L2-044`, `L2-010` |
| Not found (`not-found`) | [✅](pages/not-found/default.html) | ➖ | ➖ | ➖ |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `L2-068` |
| Offline (`offline`) | [✅](pages/offline/default.html) | ➖ | ➖ | ➖ |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `L2-068` |
| Privacy (`privacy`) | [✅](pages/privacy/default.html) | ➖ | ➖ | ➖ |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `L2-054`, `L2-055`, `L2-056`, `L2-005` |
| Problem detail (`problem-detail`) | [✅](pages/problem-detail/default.html) | [✅](pages/problem-detail/loading.html) | ➖ | [✅](pages/problem-detail/error.html) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | [✅](pages/problem-detail/resolved.html) |  | `L2-036`, `L2-045`, `L2-047` |
| Report detail (`report-detail`) | [✅](pages/report-detail/default.html) | [✅](pages/report-detail/loading.html) | ➖ | [✅](pages/report-detail/error.html) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | [✅](pages/report-detail/resolved.html) | [✅](pages/report-detail/hidden.html) | `L2-044`, `L2-045`, `L2-047` |
| Marketplace rules (`rules`) | [✅](pages/rules/default.html) | ➖ | ➖ | ➖ |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `L2-011`, `L2-014`, `L2-016`, `L2-031`, `L2-033`, `L2-044` |
| Server error (`server-error`) | [✅](pages/server-error/default.html) | ➖ | ➖ | ➖ |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `L2-068` |
| Terms (`terms`) | [✅](pages/terms/default.html) | ➖ | ➖ | ➖ |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `L2-001`, `L2-036`, `L2-031` |

### Dialogs

| Screen | default | busy | invalid | failed | blocked | success | sent | limited | guest | already | analytics-on | order-warning | reinstate | Requirements |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Change password (`change-password`) | [✅](dialogs/change-password/default.html) | [✅](dialogs/change-password/busy.html) | [✅](dialogs/change-password/invalid.html) | [✅](dialogs/change-password/failed.html) |  |  |  |  |  |  |  |  |  | `L2-009`, `L2-001`, `L2-008` |
| Close account (`close-account`) | [✅](dialogs/close-account/default.html) | [✅](dialogs/close-account/busy.html) | [✅](dialogs/close-account/invalid.html) |  | [✅](dialogs/close-account/blocked.html) |  |  |  |  |  |  |  |  | `L2-005` |
| Download your data (`data-export`) | [✅](dialogs/data-export/default.html) | [✅](dialogs/data-export/busy.html) | ➖ |  |  | [✅](dialogs/data-export/success.html) |  |  |  |  |  |  |  | `L2-055` |
| Reply to review (`reply-review`) | [✅](dialogs/reply-review/default.html) | [✅](dialogs/reply-review/busy.html) | [✅](dialogs/reply-review/invalid.html) |  |  |  |  |  |  |  |  |  |  | `L2-039` |
| Report member (`report-member`) | [✅](dialogs/report-member/default.html) | [✅](dialogs/report-member/busy.html) | [✅](dialogs/report-member/invalid.html) |  |  | [✅](dialogs/report-member/success.html) |  |  |  |  |  |  |  | `L2-044` |
| Sign out everywhere (`sign-out-everywhere`) | [✅](dialogs/sign-out-everywhere/default.html) | [✅](dialogs/sign-out-everywhere/busy.html) | ➖ | [✅](dialogs/sign-out-everywhere/failed.html) |  |  |  |  |  |  |  |  |  | `L2-008` |
| Verify email prompt (`verify-email-prompt`) | [✅](dialogs/verify-email-prompt/default.html) | [✅](dialogs/verify-email-prompt/busy.html) | ➖ |  |  |  | [✅](dialogs/verify-email-prompt/sent.html) | [✅](dialogs/verify-email-prompt/limited.html) |  |  |  |  |  | `L2-002`, `L2-003` |
| Filters (`filters`) | [✅](dialogs/filters/default.html) | [✅](dialogs/filters/busy.html) | [✅](dialogs/filters/invalid.html) |  |  |  |  |  |  |  |  |  |  | `L2-024`, `L2-062` |
| Menu (`nav-menu`) | [✅](dialogs/nav-menu/default.html) | ➖ | ➖ |  |  |  |  |  | [✅](dialogs/nav-menu/guest.html) |  |  |  |  | `L2-062`, `L2-065` |
| Add tracking (`add-tracking`) | [✅](dialogs/add-tracking/default.html) | [✅](dialogs/add-tracking/busy.html) | [✅](dialogs/add-tracking/invalid.html) | [✅](dialogs/add-tracking/failed.html) |  |  |  |  |  |  |  |  |  | `L2-033` |
| Cancel order (`cancel-order`) | [✅](dialogs/cancel-order/default.html) | [✅](dialogs/cancel-order/busy.html) | [✅](dialogs/cancel-order/invalid.html) | [✅](dialogs/cancel-order/failed.html) |  |  |  |  |  |  |  |  |  | `L2-035` |
| Confirm receipt (`confirm-receipt`) | [✅](dialogs/confirm-receipt/default.html) | [✅](dialogs/confirm-receipt/busy.html) | ➖ | [✅](dialogs/confirm-receipt/failed.html) |  |  |  |  |  |  |  |  |  | `L2-034` |
| Leave a review (`leave-review`) | [✅](dialogs/leave-review/default.html) | [✅](dialogs/leave-review/busy.html) | [✅](dialogs/leave-review/invalid.html) |  |  | [✅](dialogs/leave-review/success.html) |  |  |  |  |  |  |  | `L2-038`, `L2-039`, `L2-040` |
| Relist item (`relist`) | [✅](dialogs/relist/default.html) | [✅](dialogs/relist/busy.html) | ➖ |  |  |  |  |  |  |  |  |  |  | `L2-035` |
| Report a problem (`report-problem`) | [✅](dialogs/report-problem/default.html) | [✅](dialogs/report-problem/busy.html) | [✅](dialogs/report-problem/invalid.html) | [✅](dialogs/report-problem/failed.html) |  |  |  |  |  |  |  |  |  | `L2-036` |
| Ask to cancel (`request-cancellation`) | [✅](dialogs/request-cancellation/default.html) | [✅](dialogs/request-cancellation/busy.html) | ➖ | [✅](dialogs/request-cancellation/failed.html) |  |  |  |  |  |  |  |  |  | `L2-035` |
| Respond to cancellation (`respond-cancellation`) | [✅](dialogs/respond-cancellation/default.html) | [✅](dialogs/respond-cancellation/busy.html) | ➖ | [✅](dialogs/respond-cancellation/failed.html) |  |  |  |  |  |  |  |  |  | `L2-035` |
| Report listing (`report-listing`) | [✅](dialogs/report-listing/default.html) | [✅](dialogs/report-listing/busy.html) | [✅](dialogs/report-listing/invalid.html) |  |  | [✅](dialogs/report-listing/success.html) |  |  |  | [✅](dialogs/report-listing/already.html) |  |  |  | `L2-044` |
| Withdraw listing (`withdraw-listing`) | [✅](dialogs/withdraw-listing/default.html) | [✅](dialogs/withdraw-listing/busy.html) | ➖ | [✅](dialogs/withdraw-listing/failed.html) |  |  |  |  |  |  |  |  |  | `L2-020` |
| Cookie settings (`cookie-settings`) | [✅](dialogs/cookie-settings/default.html) | ➖ | ➖ |  |  |  |  |  |  |  | [✅](dialogs/cookie-settings/analytics-on.html) |  |  | `L2-056` |
| Resolve problem (`resolve-problem`) | [✅](dialogs/resolve-problem/default.html) | [✅](dialogs/resolve-problem/busy.html) | [✅](dialogs/resolve-problem/invalid.html) |  |  |  |  |  |  |  |  |  |  | `L2-036`, `L2-045`, `L2-047` |
| Resolve report (`resolve-report`) | [✅](dialogs/resolve-report/default.html) | [✅](dialogs/resolve-report/busy.html) | [✅](dialogs/resolve-report/invalid.html) | [✅](dialogs/resolve-report/failed.html) |  |  |  |  |  |  |  | [✅](dialogs/resolve-report/order-warning.html) |  | `L2-045`, `L2-046`, `L2-047` |
| Suspend member (`suspend-member`) | [✅](dialogs/suspend-member/default.html) | [✅](dialogs/suspend-member/busy.html) | [✅](dialogs/suspend-member/invalid.html) |  |  |  |  |  |  |  |  |  | [✅](dialogs/suspend-member/reinstate.html) | `L2-046`, `L2-047` |

### Notifications

| Screen | info | success | warning | danger | with-action | stacked | Requirements |
|---|---|---|---|---|---|---|---|
| Account banner (`account-banner`) | [✅](notifications/account-banner/info.html) | [✅](notifications/account-banner/success.html) | [✅](notifications/account-banner/warning.html) | [✅](notifications/account-banner/danger.html) |  |  | `L2-002`, `L2-046` |
| Reservation timer (`reservation-timer`) | [✅](notifications/reservation-timer/info.html) | [✅](notifications/reservation-timer/success.html) | [✅](notifications/reservation-timer/warning.html) | [✅](notifications/reservation-timer/danger.html) |  |  | `L2-028`, `L2-030` |
| Payout banner (`payout-banner`) | [✅](notifications/payout-banner/info.html) | [✅](notifications/payout-banner/success.html) | [✅](notifications/payout-banner/warning.html) | [✅](notifications/payout-banner/danger.html) |  |  | `L2-031` |
| Toasts (`toast`) | [✅](notifications/toast/info.html) | [✅](notifications/toast/success.html) | [✅](notifications/toast/warning.html) | [✅](notifications/toast/danger.html) | [✅](notifications/toast/with-action.html) | [✅](notifications/toast/stacked.html) | `L2-019`, `L2-020`, `L2-068` |
| Cookie consent (`cookie-consent`) | [✅](notifications/cookie-consent/info.html) | [✅](notifications/cookie-consent/success.html) | ➖ | ➖ |  |  | `L2-056` |
| System notices (`system-banner`) | [✅](notifications/system-banner/info.html) | [✅](notifications/system-banner/success.html) | [✅](notifications/system-banner/warning.html) | [✅](notifications/system-banner/danger.html) |  |  | `L2-066`, `L2-068` |

<!-- coverage:end -->
