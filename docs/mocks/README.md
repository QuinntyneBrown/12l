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
and one component kit:

```
docs/mocks/
  assets/tokens.css    design tokens (12L palette, type, space, shape, motion); the only place colours live
  assets/ui.css        component kit, including the 12L brand layer (size tag, listing card, gallery…)
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
<!-- coverage:end -->
