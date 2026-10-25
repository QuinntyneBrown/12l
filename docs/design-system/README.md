# 12L design system

Extracted from [docs/mocks](../mocks/README.md) on 25 Oct 2026. Open [index.html](index.html) locally (no server needed); press `t` or use the toggle to switch themes.

Ink `#0B0B0B`, paper `#F4F1EA` and signal red `#E1251B` from the logo; square corners and one 45° chamfer; Archivo black-weight headings over Inter body text. Every page shows its tokens live in both themes and every colour pair is checked against WCAG 2.2 AA.

## Foundations

| Page | Covers |
|---|---|
| [Color](foundations/color.html) | Ink, paper, stone and signal ramps; semantic roles; status colours; both themes; every contrast pair live. |
| [Typography](foundations/typography.html) | Families, the nine-step scale, weights, line heights, tracking, twelve role shorthands, measure and responsive type. |
| [Spacing](foundations/spacing.html) | The 4px spacing scale, inside vs between rules, padding by component size and control heights. |
| [Layout](foundations/layout.html) | Breakpoints, columns, gutters and margins, the live grid, container and measure, page templates (catalog, detail, form, auth, account, admin). |
| [Elevation](foundations/elevation.html) | Four shadow levels, the surface hierarchy, the z-order scale and how the dark theme shows elevation. |
| [Shape](foundations/shape.html) | Radii (0, 2, 4, 6px and full), border widths, the 45° chamfer and which shape goes where. |
| [Motion](foundations/motion.html) | Durations and easings with replayable demos, choreography, loops and reduced motion. |
| [Iconography](foundations/iconography.html) | The icon set, style rules, sizes, colour, labelling and the full sheet of icons used in the mocks. |
| [Theming](foundations/theming.html) | How themes work, the token tiers, adding a theme, component re-skins and consuming tokens.json. |
| [Responsive](foundations/responsive.html) | Mobile-first rules, what each component does at each breakpoint, touch rules and the testing matrix. |
| [Accessibility](foundations/accessibility.html) | WCAG 2.2 AA commitments, focus, targets, testing procedure and the component contract. |
| [Content](foundations/content.html) | Voice and tone, sentence case, button verbs, numbers, money, dates and times, error and empty-state formulas, microcopy library. |

## Components

### Actions

| Component | Variants | States | Source mocks |
|---|---|---|---|
| [Button](components/button.html) | primary, secondary, ghost, link, danger; icon, icon-only, block | default, hover, focus, active, disabled, loading | [pages/listing-detail/default](../mocks/pages/listing-detail/default.html), [pages/sell/default](../mocks/pages/sell/default.html), [pages/checkout/submitting](../mocks/pages/checkout/submitting.html) +2 |
| [Button group](components/button-group.html) | segmented (single select, radio-based), toolbar (pressed toggles) | default, hover, focus, checked/pressed, invalid, disabled | [pages/sell/default](../mocks/pages/sell/default.html), [pages/sell/invalid](../mocks/pages/sell/invalid.html), [dialogs/report-problem/default](../mocks/dialogs/report-problem/default.html) +1 |
| [Link](components/link.html) | inline, standalone with icon, external | default, hover, focus, active, disabled (aria-disabled) | [pages/register/default](../mocks/pages/register/default.html), [pages/order-detail/default](../mocks/pages/order-detail/default.html), [pages/payouts/not-onboarded](../mocks/pages/payouts/not-onboarded.html) +1 |
| [Menu](components/menu.html) | with icons, with shortcut, with section label, danger item, checkable (radio) items; text or icon-only trigger | closed, open, item hover/focus, item disabled, item checked | [pages/listing-detail/own](../mocks/pages/listing-detail/own.html), [pages/catalog/default](../mocks/pages/catalog/default.html), [pages/sale-detail/default](../mocks/pages/sale-detail/default.html) |

### Inputs

| Component | Variants | States | Source mocks |
|---|---|---|---|
| [Checkbox](components/checkbox.html) | single, group in fieldset, with description | default, hover, focus, checked, indeterminate, invalid, disabled | [pages/register/default](../mocks/pages/register/default.html), [pages/register/invalid](../mocks/pages/register/invalid.html), [pages/sell/invalid](../mocks/pages/sell/invalid.html) +1 |
| [File upload](components/file-upload.html) | photo grid with cover, add tile, upload progress, rejected file | empty, hover, focus, dragging, uploading, rejected, invalid | [pages/sell/filled](../mocks/pages/sell/filled.html), [pages/sell/invalid](../mocks/pages/sell/invalid.html), [dialogs/report-problem/default](../mocks/dialogs/report-problem/default.html) |
| [Form field](components/form-field.html) | label + control, with help, with error, optional, with counter, choice field | default, invalid, read-only (submitting), disabled | [pages/register/default](../mocks/pages/register/default.html), [pages/register/invalid](../mocks/pages/register/invalid.html), [pages/edit-profile/default](../mocks/pages/edit-profile/default.html) +1 |
| [Form layout](components/form-layout.html) | single column, sections, two-column row, actions end / start / split / sticky, error summary | default, invalid (summary), submitting, success | [pages/sell/default](../mocks/pages/sell/default.html), [pages/sell/invalid](../mocks/pages/sell/invalid.html), [pages/sell/submitting](../mocks/pages/sell/submitting.html) +2 |
| [Radio group](components/radio-group.html) | vertical list, with descriptions, option cards; segmented (see button group) | default, hover, focus, checked, invalid, disabled | [dialogs/cancel-order/default](../mocks/dialogs/cancel-order/default.html), [dialogs/cancel-order/invalid](../mocks/dialogs/cancel-order/invalid.html), [dialogs/resolve-report/default](../mocks/dialogs/resolve-report/default.html) +1 |
| [Select](components/select.html) | native, with placeholder option, dependent (disabled until parent chosen), toolbar sort | default, hover, focus, invalid, disabled | [pages/sell/default](../mocks/pages/sell/default.html), [pages/checkout/new-address](../mocks/pages/checkout/new-address.html), [dialogs/add-tracking/default](../mocks/dialogs/add-tracking/default.html) +2 |
| [Switch](components/switch.html) | label right, label left (row, .switch--between), with description | off, on, hover, focus, disabled off, disabled on | [pages/notification-settings/default](../mocks/pages/notification-settings/default.html), [pages/notification-settings/submitting](../mocks/pages/notification-settings/submitting.html), [dialogs/cookie-settings/default](../mocks/dialogs/cookie-settings/default.html) +1 |
| [Text field](components/text-field.html) | text, email, password with show toggle, number/decimal, search, prefix/suffix addon, with icon, with counter | default, hover, focus, invalid, disabled, read-only, required | [pages/sign-in/default](../mocks/pages/sign-in/default.html), [pages/register/invalid](../mocks/pages/register/invalid.html), [pages/register/submitting](../mocks/pages/register/submitting.html) +3 |
| [Textarea](components/textarea.html) | default, auto-grow, with counter | default, hover, focus, invalid, disabled, read-only | [dialogs/reply-review/default](../mocks/dialogs/reply-review/default.html), [dialogs/reply-review/invalid](../mocks/dialogs/reply-review/invalid.html), [pages/sell/filled](../mocks/pages/sell/filled.html) +2 |

### Navigation

| Component | Variants | States | Source mocks |
|---|---|---|---|
| [Breadcrumb](components/breadcrumb.html) | category path, back to list | link default, hover, focus; current | [pages/listing-detail/default](../mocks/pages/listing-detail/default.html), [pages/order-detail/default](../mocks/pages/order-detail/default.html), [pages/report-detail/default](../mocks/pages/report-detail/default.html) |
| [Footer](components/footer.html) | simple | link default, hover, focus | [pages/catalog/default](../mocks/pages/catalog/default.html), [pages/privacy/default](../mocks/pages/privacy/default.html), [dialogs/cookie-settings/default](../mocks/dialogs/cookie-settings/default.html) |
| [Pagination](components/pagination.html) | load more (catalog), numbered, simple prev/next | default, hover, focus, current, disabled; load more busy | [pages/catalog/default](../mocks/pages/catalog/default.html), [pages/catalog/loading](../mocks/pages/catalog/loading.html), [pages/audit-log/default](../mocks/pages/audit-log/default.html) |
| [Sidebar navigation](components/sidebar-navigation.html) | grouped, with icons | default, hover, focus, current | [pages/account/default](../mocks/pages/account/default.html), [pages/my-listings/default](../mocks/pages/my-listings/default.html) |
| [Skip link](components/skip-link.html) | one | hidden, focused | [pages/catalog/default](../mocks/pages/catalog/default.html), [pages/sign-in/default](../mocks/pages/sign-in/default.html), [pages/audit-log/default](../mocks/pages/audit-log/default.html) |
| [Stepper](components/stepper.html) | order timeline, numbered stepper | complete, current, upcoming | [pages/order-detail/default](../mocks/pages/order-detail/default.html), [pages/order-detail/paid](../mocks/pages/order-detail/paid.html), [pages/order-detail/completed](../mocks/pages/order-detail/completed.html) +1 |
| [Tabs](components/tabs.html) | tab panel (role=tablist), link tabs (sub-nav), with counts, scrollable | default, hover, focus, selected/current, disabled | [pages/account/default](../mocks/pages/account/default.html), [pages/purchases/default](../mocks/pages/purchases/default.html), [pages/my-listings/default](../mocks/pages/my-listings/default.html) +1 |
| [Top bar](components/top-bar.html) | member, guest, admin, compact (mobile) | link default, hover, focus, current; menu expanded | [pages/catalog/default](../mocks/pages/catalog/default.html), [pages/catalog/guest](../mocks/pages/catalog/guest.html), [pages/catalog/category](../mocks/pages/catalog/category.html) +2 |

### Containers and overlays

| Component | Variants | States | Source mocks |
|---|---|---|---|
| [Card](components/card.html) | panel, panel sunken, card (with header/footer), interactive, selected, well, category tile | default, hover, focus, selected | [pages/account/default](../mocks/pages/account/default.html), [pages/order-detail/completed](../mocks/pages/order-detail/completed.html), [pages/checkout/default](../mocks/pages/checkout/default.html) +2 |
| [Dialog](components/dialog.html) | default, form, destructive (danger icon), small, large, bottom sheet | default, invalid, busy, failed, success | [dialogs/withdraw-listing/default](../mocks/dialogs/withdraw-listing/default.html), [dialogs/cancel-order/invalid](../mocks/dialogs/cancel-order/invalid.html), [dialogs/add-tracking/failed](../mocks/dialogs/add-tracking/failed.html) +3 |
| [Divider](components/divider.html) | horizontal, vertical, with label | none (static) | [dialogs/resolve-problem/default](../mocks/dialogs/resolve-problem/default.html), [pages/terms/default](../mocks/pages/terms/default.html) |
| [Drawer and sheet](components/drawer.html) | menu sheet (full screen), filter sheet (left, full screen on phones), right drawer, left drawer | default, busy | [dialogs/nav-menu/default](../mocks/dialogs/nav-menu/default.html), [dialogs/nav-menu/guest](../mocks/dialogs/nav-menu/guest.html), [dialogs/filters/default](../mocks/dialogs/filters/default.html) +2 |
| [Layout primitives](components/layout-primitives.html) | container, page (narrow, form), stack (sm, lg), cluster (between, end), grid (auto), split | none (static) | [pages/order-detail/default](../mocks/pages/order-detail/default.html), [pages/account/default](../mocks/pages/account/default.html), [pages/sell/default](../mocks/pages/sell/default.html) +2 |
| [Tooltip](components/tooltip.html) | text, with shortcut | hidden, hover, focus | [pages/listing-detail/default](../mocks/pages/listing-detail/default.html), [pages/sell/default](../mocks/pages/sell/default.html), [pages/moderation-queue/default](../mocks/pages/moderation-queue/default.html) |

### Data display

| Component | Variants | States | Source mocks |
|---|---|---|---|
| [Avatar](components/avatar.html) | initials, account link, group with overflow, with status dot | default, hover, focus, active (as link) | [pages/listing-detail/default](../mocks/pages/listing-detail/default.html), [pages/catalog/default](../mocks/pages/catalog/default.html), [pages/profile/default](../mocks/pages/profile/default.html) +1 |
| [Badge](components/badge.html) | badge neutral/info/success/warning/danger, solid, count; status (order and listing); pill count | static | [pages/my-listings/default](../mocks/pages/my-listings/default.html), [pages/purchases/default](../mocks/pages/purchases/default.html), [pages/moderation-queue/default](../mocks/pages/moderation-queue/default.html) +1 |
| [Chip](components/chip.html) | filter (toggle), applied filter (removable), small | default, hover, focus, active, disabled, selected (pressed) | [pages/catalog/filtered](../mocks/pages/catalog/filtered.html), [pages/catalog/category](../mocks/pages/catalog/category.html), [pages/catalog/no-results](../mocks/pages/catalog/no-results.html) |
| [Description list](components/description-list.html) | facts (listing detail), dl (admin), facts row (one pair, split) | static | [pages/listing-detail/default](../mocks/pages/listing-detail/default.html), [pages/order-detail/default](../mocks/pages/order-detail/default.html), [pages/sale-detail/shipped](../mocks/pages/sale-detail/shipped.html) |
| [List](components/list.html) | simple, order list (item rows), settings list, queue, rules (numbered); item row | default, hover, focus, active, selected (current), disabled | [pages/purchases/default](../mocks/pages/purchases/default.html), [pages/my-listings/default](../mocks/pages/my-listings/default.html), [pages/settings/default](../mocks/pages/settings/default.html) +3 |
| [Stat](components/stat.html) | stat, stats row, with delta, earnings line | default, loading | [pages/member-admin/default](../mocks/pages/member-admin/default.html), [pages/profile/default](../mocks/pages/profile/default.html), [pages/payouts/default](../mocks/pages/payouts/default.html) +2 |
| [Table](components/table.html) | default, dense, sortable, selectable with row actions, row headers | row hover, focus, selected; loading (skeleton rows), empty, error | [pages/audit-log/default](../mocks/pages/audit-log/default.html), [pages/audit-log/loading](../mocks/pages/audit-log/loading.html), [pages/audit-log/no-results](../mocks/pages/audit-log/no-results.html) +3 |

### Feedback

| Component | Variants | States | Source mocks |
|---|---|---|---|
| [Alert](components/alert.html) | info, success, warning, danger; with actions; dismissible; page banner; flaws note | default, dismissible, with actions, focus; role alert vs status | [pages/checkout/declined](../mocks/pages/checkout/declined.html), [pages/sign-in/invalid](../mocks/pages/sign-in/invalid.html), [pages/account/unverified](../mocks/pages/account/unverified.html) +5 |
| [Cookie consent](components/cookie-consent.html) | first visit panel; saved toast | default, hover, focus; saved | [notifications/cookie-consent/info](../mocks/notifications/cookie-consent/info.html), [notifications/cookie-consent/success](../mocks/notifications/cookie-consent/success.html), [dialogs/cookie-settings/default](../mocks/dialogs/cookie-settings/default.html) |
| [Empty state](components/empty-state.html) | first-run, no results, error (as empty), success (queue clear); compact | empty, no results, failed to load | [pages/purchases/empty](../mocks/pages/purchases/empty.html), [pages/catalog/no-results](../mocks/pages/catalog/no-results.html), [pages/purchases/error](../mocks/pages/purchases/error.html) +2 |
| [Error page](components/error-page.html) | 404, 403, 500, offline, maintenance; inline page errors (item unavailable, couldn’t load) | static; 500 shows a reference | [pages/not-found/default](../mocks/pages/not-found/default.html), [pages/forbidden/default](../mocks/pages/forbidden/default.html), [pages/server-error/default](../mocks/pages/server-error/default.html) +3 |
| [Inline message](components/inline-message.html) | field hint, field error, inline status (muted, success, danger), reservation timer (neutral, warning, danger), secure note | hint, invalid, success, timer warning, timer danger | [pages/sell/invalid](../mocks/pages/sell/invalid.html), [pages/edit-listing/invalid](../mocks/pages/edit-listing/invalid.html), [pages/checkout/default](../mocks/pages/checkout/default.html) +3 |
| [Progress bar](components/progress.html) | determinate, indeterminate, with label and value, success, danger | 0–100%, indeterminate, complete, failed | [pages/sell/default](../mocks/pages/sell/default.html), [dialogs/data-export/busy](../mocks/dialogs/data-export/busy.html) |
| [Skeleton](components/skeleton.html) | text, title, circle, rect, photo; composed listing card, list row, detail | shimmering; static under reduced motion | [pages/catalog/loading](../mocks/pages/catalog/loading.html), [pages/purchases/loading](../mocks/pages/purchases/loading.html), [pages/listing-detail/loading](../mocks/pages/listing-detail/loading.html) +1 |
| [Spinner](components/spinner.html) | sm (inline, 20px), lg (page, 40px), inside a button | spinning; reduced motion keeps it turning | [pages/verify-email/loading](../mocks/pages/verify-email/loading.html), [pages/order-confirmation/loading](../mocks/pages/order-confirmation/loading.html), [pages/checkout/submitting](../mocks/pages/checkout/submitting.html) |
| [Toast](components/toast.html) | info, success, warning, danger; with action (Undo, View, Try again); stacked | entering, visible, paused on hover/focus, leaving; errors persist | [notifications/toast/info](../mocks/notifications/toast/info.html), [notifications/toast/success](../mocks/notifications/toast/success.html), [notifications/toast/warning](../mocks/notifications/toast/warning.html) +4 |

### 12L brand

| Component | Variants | States | Source mocks |
|---|---|---|---|
| [Buy bar](components/buy-bar.html) | one action with total, two actions (total hidden), own listing (Edit / Withdraw), reserved/sold (no bar) | default, loading (Buy now busy), guest (Sign in to buy) | [pages/listing-detail/default](../mocks/pages/listing-detail/default.html), [pages/listing-detail/guest](../mocks/pages/listing-detail/guest.html), [pages/listing-detail/own](../mocks/pages/listing-detail/own.html) +1 |
| [Gallery](components/gallery.html) | with thumbnails (all widths), with dots (below 1024px), single photo | thumb default, hover, focus, current; loading | [pages/listing-detail/default](../mocks/pages/listing-detail/default.html), [pages/listing-detail/loading](../mocks/pages/listing-detail/loading.html), [pages/listing-detail/sold](../mocks/pages/listing-detail/sold.html) |
| [Listing card](components/listing-card.html) | default, reserved, sold; in .listing-grid (2/3/4 columns) and in the catalog with filters (2/3/4) | default, hover (photo zoom), focus, reserved, sold, loading skeleton | [pages/catalog/default](../mocks/pages/catalog/default.html), [pages/catalog/filtered](../mocks/pages/catalog/filtered.html), [pages/catalog/loading](../mocks/pages/catalog/loading.html) +2 |
| [Logo](components/logo.html) | sm (footer), md (top bar), lg (auth); inline SVG and static files for light and dark | default, hover, focus | [pages/catalog/default](../mocks/pages/catalog/default.html), [pages/sign-in/default](../mocks/pages/sign-in/default.html), [pages/moderation-queue/default](../mocks/pages/moderation-queue/default.html) |
| [Order summary](components/order-summary.html) | checkout summary, order detail summary, seller payout (with 10% fee) | default, free shipping, loading, payout held | [pages/checkout/default](../mocks/pages/checkout/default.html), [pages/order-detail/default](../mocks/pages/order-detail/default.html), [pages/sale-detail/completed](../mocks/pages/sale-detail/completed.html) +1 |
| [Photo](components/photo.html) | tones 1-6; portrait 4:5, square; stamps Reserved and Sold; thumb, large thumb; no photo | default, hover zoom (in cards), reserved, sold, loading, missing | [pages/catalog/default](../mocks/pages/catalog/default.html), [pages/listing-detail/reserved](../mocks/pages/listing-detail/reserved.html), [pages/listing-detail/sold](../mocks/pages/listing-detail/sold.html) +2 |
| [Price](components/price.html) | default (cards, rows), large (listing detail), muted (secondary amounts) | static; with shipping line, free shipping, loading | [pages/catalog/default](../mocks/pages/catalog/default.html), [pages/listing-detail/default](../mocks/pages/listing-detail/default.html), [pages/listing-detail/new-seller](../mocks/pages/listing-detail/new-seller.html) +1 |
| [Rating](components/rating.html) | summary (stars, value, count), compact (count only), no reviews yet, new seller; star input | display: rated, none; input: empty, hover, focus, selected, invalid | [pages/listing-detail/default](../mocks/pages/listing-detail/default.html), [pages/listing-detail/new-seller](../mocks/pages/listing-detail/new-seller.html), [pages/profile/default](../mocks/pages/profile/default.html) +2 |
| [Review](components/review.html) | review, review with reply, own review with Reply link; quote; thread | default, with reply, reply available, loading, empty (no reviews yet) | [pages/profile/default](../mocks/pages/profile/default.html), [pages/profile/own](../mocks/pages/profile/own.html), [dialogs/reply-review/default](../mocks/dialogs/reply-review/default.html) +2 |
| [Size tag](components/size-tag.html) | default (cards, photos), large (listing detail, category tiles) | static; on photo, on canvas, in tile | [pages/catalog/default](../mocks/pages/catalog/default.html), [pages/listing-detail/default](../mocks/pages/listing-detail/default.html), [pages/catalog/guest](../mocks/pages/catalog/guest.html) |

## Patterns

| Pattern | Covers |
|---|---|
| [Forms](patterns/forms.html) | Layout, labels, validation timing, error summary, submit and success states, drafts, destructive confirmations. |
| [Feedback and loading](patterns/feedback-and-loading.html) | Which feedback for which action; skeleton vs spinner vs progress; optimistic updates and undo. |
| [Empty and error states](patterns/empty-and-error-states.html) | First-run, no-results, error-as-empty and full error pages; copy formulas and when to use which. |
| [Navigation and page structure](patterns/navigation-and-page-structure.html) | App shell, page header, account tabs, breadcrumbs, mobile menu sheet, admin shell, back behaviour. |
| [Dialogs and overlays](patterns/dialogs-and-overlays.html) | Dialog vs sheet vs page vs inline; confirmations; busy, invalid and failed dialogs; stacking; mobile sheets. |
| [Data tables and lists](patterns/data-tables-and-lists.html) | Order and listing lists, settings rows, the admin queue and audit table, filtering, sorting, load more, responsive strategy. |
| [Notifications](patterns/notifications.html) | Toast vs banner vs inline alert; priority and persistence; stacking; the reservation timer; cookie consent. |
| [Content and tone](patterns/content-and-tone.html) | Voice, sentence case, button verbs, numbers, money, dates, error and empty formulas, microcopy library. |

## Tokens

- [`tokens/tokens.css`](tokens/tokens.css) — source of truth: primitives, semantic tokens, light and dark themes, reduced-motion, more-contrast and forced-colours overrides.
- [`tokens/tokens.json`](tokens/tokens.json) — W3C DTCG export generated from `tokens.css` (dark theme under `$extensions`).
- [`tokens/contrast-pairs.json`](tokens/contrast-pairs.json) — every foreground/background pair the components rely on, checked in both themes.
- [`assets/components.css`](assets/components.css) — the product stylesheet: every component class, token-driven, with `data-state` hooks.
- [`assets/ds.css`](assets/ds.css), [`assets/ds.js`](assets/ds.js) — documentation chrome only (theme toggle, live token values and contrast ratios).

## How the pages are built

The HTML is generated so that every page shares one shell, one navigation and the same section order:

```sh
python docs/design-system/_build/build.py
```

Component pages live in `_build/comp_*.py`, foundations in `_build/foundations.py`, patterns in `_build/patterns.py`, and component CSS added during extraction in `_build/css/*.css` (spliced into `assets/components.css`). Edit those, then rebuild.

## Changelog

- 25 Oct 2026 — first extraction from the mocks (v1.0).

## Drift found in the mocks

Values and markup in the mocks that disagreed with the system, and what was done. The mocks now load this system's CSS, so each fix applies there too.

| Mock | Issue | Resolution |
|---|---|---|
| pages/order-detail/default | External tracking link shows an icon but does not tell screen readers it leaves 12L. | Link page documents visually hidden destination text, e.g. “(opens USPS)”. |
| assets/ui.css (.size-tag, .photo__stamp, .topbar__admin) | The size tag, photo stamps and admin tag read --palette-ink-950, --palette-paper-100 and --palette-white directly, skipping the semantic tier. | Added semantic --color-size-tag-bg/-fg, --color-stamp-bg/-fg and --color-fg-on-brand; components.css reads only those. Values unchanged. |
| assets/tokens.css (--photo-bg-1..6) | Photo backdrops were declared as unprefixed --photo-bg-* custom properties, outside both the primitive and the semantic tier. | Renamed to primitives --palette-photo-1..6 with semantic --color-photo-bg-1..6; .photo--1..6 read the semantic tokens. |
| pages/account/default | Stat panels are links but have no hover or focus affordance beyond the browser default. | Documented as interactive containers; the system gives .panel links the hover border and the shared focus ring. |
| pages/listing-detail/default | Icon-only buttons (Share, Save, Remove photo, Close) carry aria-label but show no visible name on hover or focus. | Tooltip component specified; product builds add it to every icon-only button. |
| docs/mocks/assets/ui.css | Media queries used 36rem, 62rem and 75rem (plus 35.99rem), none of which were layout tokens (40/48/64/80/96rem). | Normalised to 40rem (sm), 64rem (lg) and 80rem (xl) in components.css; dialogs centre, form rows split and two-column layouts start 32–64px later. |
| pages/rules/default | Row headers (th scope=row) in the category table picked up the column-header style: sunken background, muted label, sticky. | Added .table tbody th as a plain label cell in components.css. |
| pages/audit-log/default | Time and Target cells used .num (tabular, right-aligned intent) on text, plus inline style white-space: nowrap. | Added .nowrap; .num is reserved for numbers. Target IDs are shown as code. |
| pages/rules/default | Each rules-list item carried inline padding-block and border-bottom (with a raw 1px) and borrowed .settings-list__body. | Added .rules-list > li with the same rhythm; the inline styles can be dropped. |
| pages/catalog/filtered | Applied-filter chips were : a toggle state on an element that cannot take focus. | Applied filters are plain chips with a labelled remove button; aria-pressed is only for  toggles. |
| pages/profile/default | Stats put stat__value before stat__label; member-admin and payouts put the label first. | Label first is the standard (read order and visual order agree); the profile markup should be reordered. |
| assets/ui.css (toast) | Toast icon colour was set twice: first to --color-*-icon (tuned for light surfaces, 2–3:1 on ink), then overridden with --color-inverse-*. | Kept only the inverse tokens, routed through the new --toast-edge component token. |
| pages/edit-profile/success, pages/notification-settings/success | Spacing under a success alert came from an empty . | Documented: alerts sit in a .stack and take the stack gap; no spacer elements. |
| assets/ui.css (spinner, skeleton, progress, pulse) | Loop durations were raw (0.8s, 1.4s, 1.6s) and the global reduced-motion rule stopped spinners too. | Added --duration-cycle-fast (800ms) and --duration-cycle (1400ms; pulse snapped from 1.6s); spinners and busy buttons keep turning under reduced motion. |
| notifications/cookie-consent/info | Secondary button edge (--color-border-inverse) on the inverse panel was 1.73:1 in light and 1.35:1 in dark, below the 3:1 for UI components (1.4.11). | --color-border-inverse now aliases --palette-stone-500 (light) and --palette-stone-600 (dark); both pass 3:1. Pair added to contrast-pairs.json. |
| pages/sign-in/default | Password fields have no show/hide toggle. | Text field page documents an input-group toggle button with aria-pressed and the label “Show password”. |
| dialogs/cookie-settings/default | Switch rows use inline style (justify-content: space-between; width: 100%). | Added .switch--between. |
| pages/sell/invalid | Error summary list styled inline (margin: 0; padding-left: var(--space-5)). | Added .form-summary ul rule. |
| pages/notification-settings/default | Start-aligned form actions use inline justify-content. | Added .form-actions--start. |
| assets/tokens.css | Radius comments said 2/4/8/12/16px while the values were 0/2/2/4/6px. | Documented the real values; comments fixed; five distinct radii kept. |
| assets/tokens.css | --layout-topbar-height comment said 56px, value 4rem (64px); --layout-container-max comment said 1280px, value 76rem (1216px). | Kept the values the mocks render with; comments fixed. |
| assets/tokens.css | The prefers-color-scheme dark block repeated the four --color-inverse-* lines and differed from the [data-theme=dark] block. | Both dark blocks are now generated identical. |
| assets/tokens.css | Dark --color-bg-surface-sunken was a raw #080808 inside the theme block. | Added primitive --palette-ink-1000 and aliased it. |
| assets/tokens.css | Dark --color-focus-ring-offset and --shadow-focus resolved against the light surface inside nested [data-theme=dark] containers. | Redeclared both in the dark theme. |
| assets/ui.css | Borders used raw 1px, 2px, 3px and 4px widths. | Added --border-width-accent (3px) and --border-width-heavy (4px) beside hairline and thick; components.css uses tokens only. |
| pages/listing-detail/default, pages/sell/default | Size tags were fixed ink on paper in both themes, so outside a photo (next to the listing title, in the sell form) they vanished into the dark-theme canvas (1.1:1). | Size tags use --color-accent / --color-fg-on-accent by default and switch to the fixed --color-size-tag-* only on photos. |

## Verification

Run on 25 Oct 2026 after the last rebuild:

| Check | Command | Result |
|---|---|---|
| Contrast, light and dark | `python .claude/skills/extracting-design-systems/scripts/check_contrast.py docs/design-system/tokens/tokens.css` | 156 pairs passed, 0 failed (78 pairs × 2 themes) |
| Structure, links, labels, raw colours | `python .claude/skills/extracting-design-systems/scripts/check_design_system.py docs/design-system` | 74 pages (53 components, 8 patterns, 12 foundations, index), 0 errors, 0 warnings |
| DTCG export | `python .claude/skills/extracting-design-systems/scripts/tokens_to_json.py docs/design-system/tokens/tokens.css` | 284 tokens written to `tokens/tokens.json` |
| Mocks on the system CSS | `python .claude/skills/writing-html-mocks/scripts/check_mocks.py docs/mocks` | 66 screens, 278 mocks, 0 errors, 0 warnings |
| Reflow at 360px | Playwright: `scrollWidth` of every page, both themes | No page scrolls sideways; no script errors |
| Screenshots | Index, button, dialog, listing card and color at 360 and 1280 px, light and dark; plus menu, file upload, text field, table, badge, toast, alert, error page, gallery, buy bar, top bar, layout primitives and the forms and dialogs patterns | Reviewed; fixed nav wrapping, anatomy overflow, unreadable ramp labels and the dark-theme size tag |
| Mocks before vs after | Pixel diff of catalog, listing detail and checkout at 360 and 1280 px against the mocks' own CSS | Identical; only the 992–1023 px range changes (breakpoint normalisation, see drift) |

Remaining differences, recorded rather than fixed in the mocks: components that no mock uses yet (sidebar navigation, numbered pagination, stepper, menu, button group, tooltip, progress bar, category tile) are documented from the kit and say so on their pages.
