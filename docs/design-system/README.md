# 12L design system

Extracted from [docs/mocks](../mocks/README.md) on 2026-10-25. Open [index.html](index.html) locally.

The first extraction covers the tokens, every foundation page and the components the
application shell needs. Components for feature screens are added as those screens are
built; until then their mocks remain the reference.

## Foundations

| Page | Covers |
|---|---|
| [Color](foundations/color.html) | Ramps, roles, status colours, both themes, contrast pairs |
| [Typography](foundations/typography.html) | Families, scale, roles, measure |
| [Spacing](foundations/spacing.html) | 4px scale, inside/between rules |
| [Layout](foundations/layout.html) | L2-061 breakpoints, grid, container, page templates |
| [Elevation](foundations/elevation.html) | Shadows, surfaces, z-order |
| [Shape](foundations/shape.html) | Radii, borders, chamfer |
| [Motion](foundations/motion.html) | Durations, easings, reduced motion |
| [Iconography](foundations/iconography.html) | Inline SVG set and sizes |
| [Theming](foundations/theming.html) | Token tiers, light/dark, adding a theme |
| [Responsive](foundations/responsive.html) | Per-component rules and testing matrix |
| [Accessibility](foundations/accessibility.html) | WCAG 2.2 AA commitments |
| [Content](foundations/content.html) | Voice, formulas, microcopy |

## Components

| Component | Variants | States | Source mocks |
|---|---|---|---|
| [Skip link](components/skip-link.html) | one | hidden, focused | every page |
| [Top bar](components/top-bar.html) | guest, member, admin, bare | default, current | catalog/guest, catalog/default, problem-detail, maintenance |
| [Footer](components/footer.html) | one | default, hover | catalog |
| [Toast](components/toast.html) | info, success, warning, danger | entering, leaving, paused | notifications/toast |
| [Sheet](components/sheet.html) | navigation, filter | open | dialogs/nav-menu, dialogs/filters |
| [Button](components/button.html) | primary, secondary, ghost, link, danger | default, hover, focus, active, disabled, loading | catalog/guest, nav-menu, toast |
| [Link](components/link.html) | inline, nav, footer | default, hover, focus, current | catalog, rules |
| [Form field](components/form-field.html) | input, textarea, select | default, hover, focus, invalid, disabled, read only | sign-in, sell |

## Patterns

| Pattern | Covers |
|---|---|
| [Navigation](patterns/navigation.html) | Skip link, top bar, sheet, subnav and footer together |

## Tokens

- `tokens/tokens.css` — source of truth; `tokens/tokens.json` — DTCG export; `tokens/contrast-pairs.json` — checked pairs.
- `assets/components.css` — component stylesheet extracted from the mocks' `ui.css`.

## Drift found in the mocks

| Mock | Issue | Resolution |
|---|---|---|
| `assets/tokens.css` | `--layout-breakpoint-sm` 40rem, `-lg` 64rem, `-xl` 80rem, plus a 2xl value, disagree with `L2-061` | Tokens set to 36rem, 48rem, 62rem, 75rem; 2xl removed; grid media queries moved to 48rem and 62rem |
| `assets/tokens.css` | Four `--color-inverse-*` lines duplicated inside the dark media block | Duplicates removed |
| `assets/ui.css` | Already uses the `L2-061` values in its media queries | None |

## Verification

- `python .claude/skills/extracting-design-systems/scripts/check_contrast.py docs/design-system/tokens/tokens.css` — see the latest run in the pull request.
- `python .claude/skills/extracting-design-systems/scripts/tokens_to_json.py docs/design-system/tokens/tokens.css`
- `python .claude/skills/extracting-design-systems/scripts/check_design_system.py docs/design-system`
