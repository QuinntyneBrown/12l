"""Foundation pages: color, typography, spacing, layout, elevation, shape, motion,
iconography, theming, responsive, accessibility, content.

Every token in tokens/tokens.css appears in exactly one #tokens table here;
TOKEN_PAGE assigns each prefix to its page and build fails on an orphan.
"""
import re

from ds import *

CSS = (ROOT / "tokens" / "tokens.css").read_text(encoding="utf-8")
_root = CSS[CSS.index(":root {"):CSS.index("color-scheme: light;")]
TOKENS = []          # [(name, comment)] in source order, :root scope only
for m in re.finditer(r"^\s*(--[\w-]+)\s*:\s*[^;]+;\s*(?:/\*\s*(.*?)\s*\*/)?", _root, re.M):
    TOKENS.append((m.group(1), (m.group(2) or "").strip()))

TOKEN_PAGE = [("--palette-", "color"), ("--color-", "color"), ("--font-", "typography"), ("--line-height-", "typography"),
              ("--letter-spacing-", "typography"), ("--text-", "typography"), ("--space-", "spacing"), ("--control-height-", "spacing"),
              ("--layout-", "layout"), ("--radius-", "shape"), ("--border-width-", "shape"), ("--chamfer", "shape"),
              ("--shadow-", "elevation"), ("--z-", "elevation"), ("--duration-", "motion"), ("--ease-", "motion"),
              ("--target-", "accessibility"), ("--focus-ring-", "accessibility")]


def page_of(name: str) -> str:
    for prefix, pg in TOKEN_PAGE:
        if name.startswith(prefix):
            return pg
    raise ValueError(f"token {name} has no foundation page")


def tokens_for(pg: str, prefixes: tuple[str, ...] | None = None) -> list[tuple[str, str]]:
    return [(n, c) for n, c in TOKENS if page_of(n) == pg and (prefixes is None or n.startswith(prefixes))]


def token_rows(pg: str, prefixes=None, colour=False) -> str:
    rows = []
    for n, c in tokens_for(pg, prefixes):
        if colour or n.startswith(("--color-", "--palette-")):
            rows.append(f"<tr><td><code>{n}</code></td><td>{swatch(n, 'light')}</td><td>{swatch(n, 'dark')}</td><td>{esc(c)}</td></tr>")
        else:
            rows.append(f'<tr><td><code>{n}</code></td><td colspan="2"><span data-token="{n}"></span></td><td>{esc(c)}</td></tr>')
    return ('<div class="ds-table-wrap"><table class="ds-table"><thead><tr><th scope="col">Token</th><th scope="col">Light</th>'
            f'<th scope="col">Dark</th><th scope="col">Use</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>')


def all_tokens(pg: str) -> str:
    groups = {}
    for n, _ in tokens_for(pg):
        key = re.match(r"--([a-z]+(?:-[a-z]+)?)", n).group(1)
        groups.setdefault(key, None)
    return p(f"Every <code>{pg}</code> token in <code>tokens/tokens.css</code>, with its live value in each theme.") + token_rows(pg)


# Every token must belong to a page.
for _n, _c in TOKENS:
    page_of(_n)


def ramp(name: str, steps: list[str]) -> str:
    spans = "".join(f'<span style="--swatch: var(--palette-{name}-{s});" data-step="{s}"></span>' for s in steps)
    return f'<h3>{name.title()}</h3><div class="ds-ramp" role="img" aria-label="{name} ramp, steps {", ".join(steps)}">{spans}</div>'


def role_swatches(names: list[str]) -> str:
    out = []
    for n in names:
        out.append(f'<div class="ds-swatch"><div class="ds-swatch__chip" style="--swatch: var({n});" data-token="{n}" data-swatch></div>'
                   f'<div class="ds-swatch__body"><span class="ds-swatch__name">{n}</span><span class="ds-swatch__value" data-token="{n}"></span></div></div>')
    return f'<div class="ds-swatches">{"".join(out)}</div>'


# ---------------------------------------------------------------------------
# Color
# ---------------------------------------------------------------------------
_pairs = __import__("json").loads((ROOT / "tokens" / "contrast-pairs.json").read_text())["pairs"]
_pair_rows = [(x["note"], x["fg"], x["bg"], x["min"]) for x in _pairs]

foundation("color", "Color",
    lead="Three colours from the logo carry the brand: ink, paper and one signal red. Everything else is a warm grey or a status tint, and every pairing is checked for WCAG 2.2 AA in both themes.",
    covers="Ink, paper, stone and signal ramps; semantic roles; status colours; both themes; every contrast pair live.",
    sections=[
        ("overview", "Overview", p(
            "12L is ink on paper. Primary actions are solid ink (the logo's black), the canvas is warm paper, and secondary text and control edges come from a warm <i>stone</i> grey so nothing turns blue-grey. "
            "Signal red, the logo's L, is an indicator only: the logo, the current-page bar, the active timeline step, the hero's last words and the admin tag. It is never body text and never an error colour; errors use the separate red status ramp.",
            "Colours are used through semantic tokens (<code>--color-*</code>). Components never read a <code>--palette-*</code> primitive, so the dark theme only has to remap roles.")
            + themes(f'<div class="cluster">{btn("Buy now", "primary")}{btn("Make an offer")}<span class="size-tag" aria-label="Size US 12">US <b>12</b></span><span class="badge badge--success">Active</span><span class="status status--reserved">Reserved</span></div>')),
        ("primitives", "Primitive ramps", p("Raw values, taken from the logo and the mocks. Only semantic tokens read them.")
            + ramp("ink", ["1000", "950", "900", "850", "800", "700", "600"]) + ramp("paper", ["25", "50", "100", "200", "300", "400"])
            + ramp("stone", ["300", "400", "500", "550", "600", "700"]) + ramp("signal", ["300", "500"])
            + ramp("green", ["50", "300", "500", "700", "950"]) + ramp("amber", ["50", "300", "500", "700", "950"])
            + ramp("blue", ["50", "300", "500", "700", "950"]) + ramp("red", ["50", "300", "500", "700", "800", "950"])
            + "<h3>Photo backdrops</h3>" + p("Six light studio backdrops behind product photos. They stay light in the dark theme, the way real photos would.")
            + '<div class="ds-ramp" role="img" aria-label="Photo backdrops 1 to 6">' + "".join(f'<span style="--swatch: var(--palette-photo-{i});" data-step="{i}"></span>' for i in range(1, 7)) + "</div>"),
        ("roles", "Semantic roles", p("Backgrounds rise from canvas to surface to raised; sunken wells sit below the surface. Swatches show the current theme; toggle the theme to compare.")
            + "<h3>Backgrounds</h3>" + role_swatches(["--color-bg-canvas", "--color-bg-surface", "--color-bg-surface-raised", "--color-bg-surface-sunken", "--color-bg-subtle", "--color-bg-subtle-hover", "--color-bg-inverse", "--color-bg-backdrop"])
            + "<h3>Text</h3>" + role_swatches(["--color-fg-default", "--color-fg-muted", "--color-fg-subtle", "--color-fg-disabled", "--color-fg-inverse", "--color-fg-link", "--color-fg-on-accent", "--color-fg-on-danger"])
            + "<h3>Borders, accent and brand</h3>" + role_swatches(["--color-border-default", "--color-border-strong", "--color-border-inverse", "--color-accent", "--color-accent-hover", "--color-accent-subtle", "--color-focus-ring", "--color-brand"])
            + "<h3>Fixed brand blocks</h3>" + p("The size tag and photo stamps sit on photos, which stay light, so they keep the same colours in both themes.")
            + role_swatches(["--color-size-tag-bg", "--color-size-tag-fg", "--color-stamp-bg", "--color-stamp-fg"])),
        ("status", "Status colours", p("Four statuses, each with a tinted background, text, border, icon and solid colour. Status is never carried by colour alone: alerts have an icon and a title, order statuses have a word next to the dot.")
            + ex("".join(f'<div class="alert alert--{k}">{ic(i)}<div class="alert__body"><div class="alert__title">{t}</div><div>{d}</div></div></div>' for k, i, t, d in [
                ("info", "info", "Shipped", "Tracking 9400 1118 9922 3150 4821 06 was added on Fri 23 Oct."),
                ("success", "check-circle", "Payout sent", "$76.50 is on its way to your bank account ending 4417."),
                ("warning", "alert", "Reserved for you", "Complete checkout within 9:42 or the item goes back on sale."),
                ("danger", "x-circle", "Card declined", "Your bank declined the payment. Try another card.")]), stack=True, show_code=False)
            + themes('<div class="cluster"><span class="status status--active">Active</span><span class="status status--reserved">Reserved</span><span class="status status--info">Shipped</span><span class="status status--removed">Cancelled</span><span class="status status--draft">Draft</span></div>')),
        ("themes", "Both themes", p("Dark is not inverted light. Surfaces get lighter as they rise (ink-950 canvas, ink-900 surface, ink-850 raised), the accent flips to paper with an ink label, and status backgrounds become deep tints with light text.")
            + themes('<div class="stack stack--sm"><div class="card"><p class="eyebrow">Red Wing</p><p>Iron Ranger 8111 boots</p><p class="price">$210</p></div>'
                     f'<div class="cluster">{btn("Buy now", "primary")}{btn("Make an offer")}</div><div class="alert alert--warning">{ic("alert")}<div class="alert__body"><div class="alert__title">Used - Fair</div><div>Footbed worn at the heel.</div></div></div></div>')),
        ("usage", "Usage", ul(
            "Ink for primary actions, links, selected chips and checked controls. One ink primary button per screen.",
            "Signal red for indicators only: the logo, the current page, the current order step, the admin tag, one emphasised word in the hero. Never for text, never for errors, never for buttons.",
            "Stone greys for secondary text (<code>--color-fg-muted</code>), metadata and placeholders (<code>--color-fg-subtle</code>) and control edges (<code>--color-border-strong</code>).",
            "Status ramps only for status: success for completed and paid out, warning for reserved and flaws, info for shipped and neutral notices, danger for errors and destructive actions.",
            "Never place text on a photo backdrop; use a size tag or stamp, which bring their own background.",
            "To add a brand theme, add a <code>[data-theme=\"name\"]</code> block that overrides semantic tokens only, then add its pairs to <code>contrast-pairs.json</code> and run the checker. See " + found("theming") + ".")),
        ("accessibility", "Contrast pairs", p(f"Every foreground/background pair the components rely on ({len(_pair_rows)} pairs, from <code>tokens/contrast-pairs.json</code>), measured live in each theme. 4.5:1 is the minimum for text (1.4.3); 3:1 for large text, control edges and focus indicators (1.4.11, 2.4.11). <code>scripts/check_contrast.py</code> checks the same list in CI.")
            + '<div class="ds-themes"><div data-theme="light">' + pairs(_pair_rows) + '</div><div data-theme="dark">' + pairs(_pair_rows) + "</div></div>"),
        ("tokens", "Tokens", all_tokens("color")),
    ])

# ---------------------------------------------------------------------------
# Typography
# ---------------------------------------------------------------------------
ROLES = [("--text-display", "display", "Size 12. Finally easy.", "Hero headline; black weight, -0.035em"),
         ("--text-h1", "h1", "Iron Ranger 8111 boots", "Page titles"),
         ("--text-h2", "h2", "$210", "Section titles, detail price, stat values"),
         ("--text-h3", "h3", "Cancel this order?", "Dialog titles, empty-state titles"),
         ("--text-h4", "h4", "Shipping address", "Card and section heads, form sections"),
         ("--text-body-lg", "body-lg", "Buy and sell men's shoes in US 12 and clothes in L.", "Lead paragraphs"),
         ("--text-body", "body", "Footbed worn at the heel. Small scuff on the left strap.", "Body text, inputs, listing titles"),
         ("--text-body-sm", "body-sm", "Ships from Portland, OR · Listed yesterday", "Metadata, help text, table cells"),
         ("--text-label", "label", "Email address", "Field labels, buttons, nav links, tabs"),
         ("--text-caption", "caption", "Shipping is calculated at checkout.", "Captions, counters, timeline dates"),
         ("--text-overline", "overline", "Red Wing", "Brand line on cards, eyebrows, badges, size tags"),
         ("--text-code", "code", "12L-48213", "Order and listing references")]

spec = "".join(f'<div class="ds-specimen"><div class="ds-specimen__meta">{t}<br>{u}</div><div style="font: var({t});{" letter-spacing: var(--letter-spacing-display);" if k in ("display", "h1", "h2") else ""}{" letter-spacing: var(--letter-spacing-wide); text-transform: uppercase;" if k == "overline" else ""}">{s}</div></div>'
               for t, k, s, u in ROLES)

foundation("typography", "Typography",
    lead="Black-weight Archivo headings, tightly tracked like the logo's numerals, over Inter for everything people read and type. Nine sizes, twelve roles.",
    covers="Families, the nine-step scale, weights, line heights, tracking, twelve role shorthands, measure and responsive type.",
    sections=[
        ("overview", "Overview", p("Two families. <b>Archivo</b> (display) at black and bold weights for display, headings and prices: heavy, tight, confident, like the 12 in the logo. <b>Inter</b> (sans) for body, labels and inputs. A monospace stack is reserved for order and listing references.",
            "Components set type with role shorthands (<code>font: var(--text-label)</code>) rather than individual properties, so a change of scale happens in one place.")),
        ("families", "Families", table(["Token", "Stack", "Use"], [
            ["<code>--font-family-display</code>", '<span style="font-family: var(--font-family-display); font-weight: var(--font-weight-black); font-size: var(--font-size-xl);">Archivo · 12L</span>', "Display, h1-h4, prices, stat values"],
            ["<code>--font-family-sans</code>", '<span style="font-family: var(--font-family-sans); font-size: var(--font-size-xl);">Inter · Size 12</span>', "Body, labels, buttons, inputs"],
            ["<code>--font-family-mono</code>", '<span style="font-family: var(--font-family-mono); font-size: var(--font-size-xl);">12L-48213</span>', "References and codes"]])
            + p("Fallbacks are system fonts, so pages render immediately while web fonts load.")),
        ("roles", "Roles", p("Each role is a <code>font</code> shorthand. Display, h1 and h2 add <code>--letter-spacing-display</code>; overlines add <code>--letter-spacing-wide</code> and uppercase.") + f'<div class="ds-example">{spec}</div>'),
        ("scale", "Scale, weights and line heights", p("A nine-step scale from 12px to 48px. Body text is 16px and nothing is smaller than 12px.")
            + '<div class="ds-example"><div class="ds-example__canvas ds-example__canvas--stack">' + "".join(
                f'<div class="ds-specimen"><div class="ds-specimen__meta">--font-size-{s} · <span data-token="--font-size-{s}"></span></div><div style="font-size: var(--font-size-{s}); line-height: var(--line-height-tight);">Size 12, finally easy</div></div>'
                for s in ["xs", "sm", "md", "lg", "xl", "2xl", "3xl", "4xl", "5xl"]) + "</div></div>"
            + table(["Weight", "Token", "Where"], [[f'<span style="font-weight: var(--font-weight-{w});">{w.title()}</span>', f"<code>--font-weight-{w}</code>", u] for w, u in [
                ("regular", "Body, help text, prices that are struck or muted"), ("medium", "Labels, buttons, nav links"), ("semibold", "Overlines, badges, step numbers"),
                ("bold", "Primary button labels, h3-h4, prices, rating values"), ("black", "Display, h1, h2 (the logo's weight)")]])
            + ul("<code>--line-height-tight</code> (1.2) for h2; display and h1 go tighter still inside their role (1.02 and 1.08).", "<code>--line-height-snug</code> (1.3) for h3-h4.",
                 "<code>--line-height-normal</code> (1.5) for body, labels and captions.", "<code>--line-height-relaxed</code> (1.65) for addresses and long-form legal pages.")),
        ("measure", "Measure and numbers", ul("Paragraphs are capped at <code>--layout-measure</code> (65ch). Empty-state text is capped at 36ch.",
            "Headings use <code>text-wrap: balance</code>; paragraphs use <code>text-wrap: pretty</code>.",
            "Prices, totals, counters, timers and table numbers use <code>font-variant-numeric: tabular-nums</code> (<code>.num</code>, <code>.price</code>) so columns align and timers don't jitter.",
            "Listing titles truncate to one line with an ellipsis on cards; the full title is on the detail page.")),
        ("usage", "Usage", ul("One h1 per page. Dialog titles use the h3 role even though they are <code>&lt;h2&gt;</code> elements.",
            "Overlines (uppercase) are for short labels only: brand names on cards, filter group legends, badges. Never a sentence.",
            "Responsive type: below 640px the display role drops to <code>--font-size-4xl</code> and h1 to <code>--font-size-3xl</code>; everything else keeps its size.",
            "Do not set <code>font-size</code> or <code>font-weight</code> ad hoc; pick a role. Buttons adjust size with <code>.btn--sm/lg</code>.")),
        ("accessibility", "Accessibility", ul("Text resizes to 200% without loss: sizes are in rem and containers wrap (1.4.4).",
            "Text spacing overrides (line height 1.5, paragraph spacing 2em, letter spacing 0.12em) do not clip content (1.4.12): no fixed heights on text containers.",
            "Muted and subtle text pass 4.5:1 on canvas, surface and sunken backgrounds in both themes; see " + found("color") + ".",
            "Uppercase is applied with CSS, so screen readers read the words, not letters.")),
        ("tokens", "Tokens", all_tokens("typography")),
    ])

# ---------------------------------------------------------------------------
# Spacing
# ---------------------------------------------------------------------------
_scale = "".join(f'<div class="ds-scale__row"><code>--space-{s}</code><span data-token="--space-{s}"></span><span class="ds-scale__bar" style="--size: var(--space-{s});"></span></div>'
                 for s in ["0-5", "1", "2", "3", "4", "5", "6", "8", "10", "12", "16", "20", "24"])
foundation("spacing", "Spacing",
    lead="A 4px scale from 2px to 96px. Small steps inside components, large steps between them, and lots of white space around everything.",
    covers="The 4px spacing scale, inside vs between rules, padding by component size and control heights.",
    sections=[
        ("overview", "Overview", p("Every margin, padding and gap is a <code>--space-*</code> token; the number is the multiple of 4px (<code>--space-6</code> is 24px). The mocks used the scale everywhere except a few hairline nudges, which are documented below.")),
        ("scale", "Scale", f'<div class="ds-scale">{_scale}</div>'),
        ("rules", "Inside and between", table(["Where", "Space", "Example"], [
            ["Icon to label", "<code>--space-1</code>–<code>--space-2</code>", "Button icons, status dots"],
            ["Label to control, control to help", "<code>--space-1</code>", "Form field parts"],
            ["Between inline items", "<code>--space-2</code>–<code>--space-3</code>", "Chips, button rows, cluster"],
            ["Inside compact components", "<code>--space-3</code>–<code>--space-4</code>", "Alerts, toasts, list rows, table cells"],
            ["Inside cards, panels, dialogs", "<code>--space-6</code> (<code>--space-8</code> panels from 768px)", "Cards, dialog header/body/footer"],
            ["Between fields in a form", "<code>--space-6</code>", "Form sections and rows"],
            ["Between sections", "<code>--space-8</code>–<code>--space-12</code>", "Page sections, profile head"],
            ["Page rhythm", "<code>--space-16</code>–<code>--space-24</code>", "Hero, bottom of page, above the footer"]])
            + p("Rule: components use <code>--space-6</code> or less inside; layout uses <code>--space-6</code> or more between. Listing grids use a larger row gap than column gap (32/16px on phones, 40/24px from 768px) so each card's text reads as belonging to its photo.")),
        ("sizes", "Padding by control size", table(["Size", "Height", "Inline padding", "Used by"], [
            ["Small", '<span data-token="--control-height-sm"></span>', "<code>--space-3</code>", "Small buttons, chips, pagination, menu items, small inputs"],
            ["Medium", '<span data-token="--control-height-md"></span>', "<code>--space-4</code> (inputs <code>--space-3</code>)", "Default buttons, inputs, selects"],
            ["Large", '<span data-token="--control-height-lg"></span>', "<code>--space-6</code>", "Buy bar, auth forms, menu-sheet footer, large inputs"]])
            + ex(btn("Small", "sm") + btn("Medium") + btn("Large", "lg") + '<label class="visually-hidden" for="sp-in">Example input</label><input class="input input--sm" id="sp-in" style="width: 10rem;" value="Medium input">', "Control heights align across buttons and inputs on one row.")),
        ("usage", "Usage", ul("Use stack (<code>.stack</code>, <code>--sm</code>, <code>--lg</code>) and cluster (<code>.cluster</code>) for gaps instead of margins on children. See " + comp("layout-primitives") + ".",
            "Hairline offsets (1-2px) that align a glyph or border are allowed inside component CSS; they are not spacing and do not get tokens.",
            "Don't invent half steps. If 12px is too tight and 16px too loose, the layout needs a different structure, not 14px.")),
        ("tokens", "Tokens", all_tokens("spacing")),
    ])

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
_bps = "".join(f'<div class="ds-bp__bar" style="--w: min(100%, {w});">{n} · {v}</div>' for n, v, w in [
    ("base", "0–639px", "6rem"), ("sm", "640px", "10rem"), ("md", "768px", "14rem"), ("lg", "1024px", "20rem"), ("xl", "1280px", "26rem"), ("2xl", "1536px", "32rem")])
foundation("layout", "Layout",
    lead="Mobile first, five breakpoints, a 4/8/12-column grid, and a 1216px container. Most 12L pages are one generous column; the grid earns its keep in the catalog and the listing detail.",
    covers="Breakpoints, columns, gutters and margins, the live grid, container and measure, page templates (catalog, detail, form, auth, account, admin).",
    sections=[
        ("overview", "Overview", p("Layout tokens grow with the viewport: <code>--layout-columns</code>, <code>--layout-gutter</code> and <code>--layout-margin</code> are redefined at 768px and 1024px, so a component that reads them adapts without its own media queries.")),
        ("breakpoints", "Breakpoints", f'<div class="ds-bp">{_bps}</div>' + table(["Name", "Min width", "What changes"], [
            ["base", "0", "One column, 16px margins, top-bar menu button, bottom-sheet dialogs, sticky buy bar."],
            ["sm", '<span data-token="--layout-breakpoint-sm"></span>', "Dialogs centre; form rows split into two; gallery stops bleeding to the edge; toasts dock bottom-right."],
            ["md", '<span data-token="--layout-breakpoint-md"></span>', "8 columns; top-bar category nav and Sell link appear; listing grid 3-up; panels pad 32px."],
            ["lg", '<span data-token="--layout-breakpoint-lg"></span>', "12 columns; catalog filters become a sticky sidebar; listing detail and checkout go two-column; top-bar search field."],
            ["xl", '<span data-token="--layout-breakpoint-xl"></span>', "Catalog grid with filters goes 4-up."],
            ["2xl", '<span data-token="--layout-breakpoint-2xl"></span>', "Nothing new: content stays at the container max and margins grow."]])
            + p("Media queries cannot read custom properties, so <code>components.css</code> writes the same values literally (<code>min-width: 48rem</code>). The mocks used 36rem, 62rem and 75rem in places; they were normalised to 40rem, 64rem and 80rem (see the README drift log).")),
        ("grid", "Columns, gutters and margins", table(["Range", "Columns", "Gutter", "Margin"], [
            ["0–767px", "4", "16px (<code>--space-4</code>)", "16px"], ["768–1023px", "8", "24px (<code>--space-6</code>)", "32px"], ["1024px+", "12", "32px (<code>--space-8</code>)", "48px"]])
            + p("The live grid below uses the current values; resize the window to watch it change.")
            + '<div class="ds-grid-demo" aria-hidden="true">' + "".join(f"<span>{i}</span>" for i in range(1, 13)) + "</div>"
            + p("On 4 and 8 columns the extra cells wrap; the demo shows them for reference.")),
        ("container", "Container and measure", ul("<code>.container</code> caps content at <code>--layout-container-max</code> (1216px) and pads it with <code>--layout-margin</code>.",
            "<code>.page--form</code> caps forms at 44rem; <code>.page--narrow</code> caps confirmations at 40rem; <code>.auth-card</code> caps sign-in at 24rem.",
            "Prose is capped at <code>--layout-measure</code> (65ch).",
            "The top bar is <code>--layout-topbar-height</code> (64px) and sticky; sticky sidebars offset themselves by it.")),
        ("templates", "Page templates", table(["Template", "Structure", "Example mocks"], [
            ["Catalog", "Top bar · toolbar (filters toggle, sort) · filters sidebar (14rem, sticky, from 1024px) + listing grid (2/3/3/4-up) · load more · footer", f'<a href="../../mocks/pages/catalog/default.html">catalog/default</a>'],
            ["Detail", "Breadcrumb · gallery (7fr) + sticky info column (5fr) from 1024px · sticky buy bar below 1024px", f'<a href="../../mocks/pages/listing-detail/default.html">listing-detail/default</a>'],
            ["Split", "Main column (3fr) + summary panel (2fr) from 1024px: checkout and order pages", f'<a href="../../mocks/pages/checkout/default.html">checkout/default</a>'],
            ["Form", "Single 44rem column of form sections, sticky actions bar", f'<a href="../../mocks/pages/sell/default.html">sell/default</a>'],
            ["Auth", "Logo centred above a 24rem card, no top bar", f'<a href="../../mocks/pages/sign-in/default.html">sign-in/default</a>'],
            ["Account", "Top bar · account subnav tabs · content column", f'<a href="../../mocks/pages/account/default.html">account/default</a>'],
            ["Admin", "Admin top bar (red Admin tag, Queue / Audit log) · lists and tables, no footer", f'<a href="../../mocks/pages/moderation-queue/default.html">moderation-queue/default</a>'],
            ["Centred state", "Top bar · left-aligned 32rem block with a giant code (404) and one action", f'<a href="../../mocks/pages/not-found/default.html">not-found/default</a>']])),
        ("usage", "Usage", ul("Build mobile first: write the base layout, then add <code>min-width</code> queries.", "Never put two columns side by side below 1024px except the 2-up listing grid and form rows from 640px.",
            "Sticky elements (top bar, filters, detail info, buy bar, form actions) use <code>--z-sticky</code> and must not cover focused content (2.4.11): leave scroll padding for them.")),
        ("tokens", "Tokens", all_tokens("layout")),
    ])

# ---------------------------------------------------------------------------
# Elevation
# ---------------------------------------------------------------------------
_shadows = "".join(f'<div style="--shadow: var(--shadow-{i});">--shadow-{i}</div>' for i in range(1, 5))
foundation("elevation", "Elevation",
    lead="12L is mostly flat: hairline borders on paper. Shadows are reserved for things that float above the page — menus, toasts, dialogs and sheets.",
    covers="Four shadow levels, the surface hierarchy, the z-order scale and how the dark theme shows elevation.",
    sections=[
        ("overview", "Overview", p("Listing cards have no shadow and no border; the photo is the card. Panels and cards sit on a 1px <code>--color-border-default</code> edge. Shadows start at level 3 for anything that floats.")),
        ("shadows", "Shadow levels", f'<div class="ds-shadow-grid">{_shadows}</div>' + themes(f'<div class="ds-shadow-grid">{_shadows}</div>')
            + table(["Level", "Use"], [["1", "Cards (<code>.card</code>), hovered primary button, switch thumb"], ["2", "Hovered interactive cards, tooltips"],
                                        ["3", "Menus, popovers, toasts, the skip link"], ["4", "Dialogs, drawers, filter sheet, cookie consent"]])),
        ("surfaces", "Surface hierarchy", p("Backgrounds encode height as well as shadows do. From low to high:")
            + themes('<div class="stack stack--sm"><div class="well">Sunken: wells, table headers, threads</div><div class="panel">Surface: cards, panels, inputs</div><div class="card" style="background: var(--color-bg-surface-raised); box-shadow: var(--shadow-3);">Raised: dialogs, menus, popovers</div></div>')),
        ("dark", "Elevation in the dark theme", p("Shadows barely show on ink, so the dark theme raises surfaces in lightness (ink-950 canvas, ink-900 surface, ink-850 raised) and uses stronger, pure-black shadows (50-70% opacity) at every level.")),
        ("z-order", "Z-order", table(["Layer", "Token", "Value", "Used by"], [[n, f"<code>--z-{n}</code>", f'<span data-token="--z-{n}"></span>', u] for n, u in [
            ("base", "Page content"), ("raised", "Pressed segment over neighbours"), ("sticky", "Top bar, buy bar, sticky form actions"), ("dropdown", "Menus"),
            ("overlay", "Modal backdrop"), ("modal", "Dialogs, drawers, menu sheet"), ("popover", "Popovers opened from a dialog"), ("toast", "Toasts, cookie consent"), ("tooltip", "Tooltips, skip link")]])
            + p("Components never set a raw <code>z-index</code>. Mock chrome sits above everything at <code>calc(var(--z-tooltip) + 10)</code>; it is not part of the product.")),
        ("usage", "Usage", ul("Don't add shadows to listing cards or list rows; they are flat by design.", "A floating element always gets a shadow and a raised surface, so it separates in both themes.", "Only one modal layer at a time; a dialog never opens another dialog.")),
        ("tokens", "Tokens", all_tokens("elevation")),
    ])

# ---------------------------------------------------------------------------
# Shape
# ---------------------------------------------------------------------------
_radii = "".join(f'<div class="ds-scale__row"><code>--radius-{r}</code><span data-token="--radius-{r}"></span><span class="ds-scale__box" style="--size: var(--radius-{r});"></span></div>' for r in ["xs", "sm", "md", "lg", "xl", "full"])
foundation("shape", "Shape",
    lead="Square like the logo. Corners are 0 to 4px, never soft, and one 45° chamfer — cut from the L — marks the size tag and the order confirmation.",
    covers="Radii (0, 2, 4, 6px and full), border widths, the 45° chamfer and which shape goes where.",
    sections=[
        ("overview", "Overview", p("The logo is built from square blocks and one diagonal cut. The UI follows: photos and size tags are square, controls have a 2px radius that reads as square but softens anti-aliasing, cards and dialogs 4px, and the only big radius is the top of a phone bottom sheet.")),
        ("radii", "Radii", f'<div class="ds-scale">{_radii}</div>' + table(["Token", "Where"], [
            ["<code>--radius-xs</code> (0)", "Checkboxes, photos, size tags, listing cards, panels"], ["<code>--radius-sm</code> (2px)", "Badges, chips, avatars, tooltips, switch track"],
            ["<code>--radius-md</code> (2px)", "Buttons, inputs, menus, alerts, toasts"], ["<code>--radius-lg</code> (4px)", "Cards, tables, dialogs on tablet and up"],
            ["<code>--radius-xl</code> (6px)", "Top corners of the bottom-sheet dialog on phones"], ["<code>--radius-full</code>", "Radio dots, progress tracks, spinner"]])
            + p("<code>--radius-sm</code> and <code>--radius-md</code> share a value today; they stay separate tokens so controls and small chips can diverge later without renaming. Five distinct values in total.")),
        ("chamfer", "The chamfer", p("<code>--chamfer</code> (10px) cuts the bottom-right corner at 45°, the same cut as the foot of the logo's L. It appears on the size tag and the confirmation mark only; anything more and it stops meaning 12L.")
            + ex(size_tag("US 12") + size_tag("L", "size-tag--lg") + f'<span class="confirm__mark">{ic("check")}</span>', "Size tags and the order confirmation mark.", show_code=True)),
        ("borders", "Border widths", table(["Token", "Value", "Where"], [[f"<code>{t}</code>", f'<span data-token="{t}"></span>', u] for t, u in [
            ("--border-width-hairline", "Every border and divider"), ("--border-width-thick", "Focus ring, step circles, kbd bottom edge"),
            ("--border-width-accent", "Current-page bar, tab indicator, flaws and quote rules, toast edge"), ("--border-width-heavy", "Alert leading edge, error summary")]])),
        ("usage", "Usage", ul("Never round a photo or a size tag.", "Don't use <code>--radius-full</code> for buttons or chips: pills are not part of 12L.", "Nested shapes keep the same or a smaller radius than their container.")),
        ("tokens", "Tokens", all_tokens("shape")),
    ])

# ---------------------------------------------------------------------------
# Motion
# ---------------------------------------------------------------------------
def _demo(d, e, label):
    return (f'<div class="ds-motion-demo" style="--demo-duration: var({d}); --demo-ease: var({e});"><button class="btn btn--sm" type="button" data-motion-run>Play {label}</button>'
            f'<span class="dot" aria-hidden="true"></span></div>')


foundation("motion", "Motion",
    lead="Quick and quiet. Colour changes in 120ms, things appear in 200-320ms, nothing bounces, and everything but status indicators stops when the member asks for reduced motion.",
    covers="Durations and easings with replayable demos, choreography, loops and reduced motion.",
    sections=[
        ("overview", "Overview", p("Motion explains where something came from: a dialog rises from the bottom on phones, a drawer slides from its edge, a toast slides up into the corner. It is never decorative, and it never delays an action.")),
        ("durations", "Durations", "".join(_demo(f"--duration-{d}", "--ease-standard", f"{d}") for d in ["fast", "base", "slow", "deliberate"])
            + table(["Token", "Value", "Use"], [[f"<code>--duration-{d}</code>", f'<span data-token="--duration-{d}"></span>', u] for d, u in [
                ("instant", "State flips with no transition"), ("fast", "Hover, colour, border, menus, tooltips"), ("base", "Toasts, switches, backdrops, accordion"),
                ("slow", "Dialogs, sheets, drawers, photo zoom on card hover"), ("deliberate", "Progress fills"), ("cycle-fast", "One spinner turn"), ("cycle", "Skeleton shimmer, indeterminate progress, pulse")]])),
        ("easings", "Easings", "".join(_demo("--duration-slow", f"--ease-{e}", e) for e in ["standard", "enter", "exit", "spring"])
            + ul("<code>--ease-standard</code> for things that move within the page.", "<code>--ease-enter</code> (decelerate) for things that arrive: dialogs, toasts, sheets.",
                 "<code>--ease-exit</code> (accelerate) for things that leave: dismissed toasts.", "<code>--ease-spring</code> is defined but unused in the mocks; keep it for a future celebratory moment, never for core UI.")),
        ("choreography", "Choreography", table(["Element", "Enter", "Exit"], [
            ["Dialog (phone)", "Slide up 16px + fade, slow, enter", "Instant"], ["Dialog (tablet+)", "Scale from 96% + fade, slow, enter", "Instant"],
            ["Drawer / filter sheet", "Slide from its edge, slow, enter", "Instant"], ["Menu", "Scale from 96% at its origin, fast, enter", "Instant"],
            ["Toast", "Slide up 16px + fade, base, enter", "Fade + 8px down, base, exit"], ["Backdrop", "Fade, base, enter", "Instant"],
            ["Listing card hover", "Photo scales to 104%, slow, standard", "Reverse"]])),
        ("accessibility", "Reduced motion", p("Under <code>prefers-reduced-motion: reduce</code> the tokens set every transition duration to 0.01ms, so components need no extra media queries. <code>components.css</code> also caps animation durations, removes the skeleton shimmer and freezes indeterminate progress at full width. Two loops keep running because they are status, not decoration: the spinner and the loading button's spinner. Smooth scrolling is turned off.")
            + p("Nothing flashes more than three times a second (2.3.1), and nothing moves for more than five seconds without a way to stop it (2.2.2): toasts pause their timer on hover and focus.")),
        ("tokens", "Tokens", all_tokens("motion")),
    ])

# ---------------------------------------------------------------------------
# Iconography
# ---------------------------------------------------------------------------
_sheet = "".join(f'<figure>{ic(n)}<figcaption>{n}</figcaption></figure>' for n in sorted(ICONS))
foundation("iconography", "Iconography",
    lead=f"{len(ICONS)} line icons on a 24-unit grid with a 2px square-ended stroke that inherits the text colour. Icons support a label; they rarely replace one.",
    covers="The icon set, style rules, sizes, colour, labelling and the full sheet of icons used in the mocks.",
    sections=[
        ("overview", "Overview", p("Icons are inline SVG (<code>&lt;svg class=\"icon\" viewBox=\"0 0 24 24\"&gt;</code>) with <code>fill: none</code>, <code>stroke: currentColor</code>, 2px stroke and round caps and joins. Rectangles in the set (lock, mail, card, calendar) are square-cornered, echoing the logo.")),
        ("set", "The set", p("Every icon the mocks use. The source of truth is <code>ICONS</code> in <code>docs/mocks/_build/mk.py</code>.") + f'<div class="ds-icon-sheet">{_sheet}</div>'),
        ("sizes", "Sizes", ex(ic("bag", "icon icon--sm") + ic("bag") + ic("bag", "icon icon--lg") + f'<span class="empty__icon">{ic("bag", "icon icon--lg")}</span>',
                              "<code>.icon--sm</code> 16px (chip remove, toast close) · <code>.icon</code> 20px default · <code>.icon--lg</code> 24px (empty states, dialog icons). Inside buttons icons are 1.25em.")),
        ("usage", "Usage and labelling", ul("Decorative icons next to text get <code>aria-hidden=\"true\"</code>; the text is the label.",
            "Icon-only controls (close, menu, search, more, remove photo) are buttons with an <code>aria-label</code>; the SVG stays hidden.",
            "Meaningful standalone icons get <code>role=\"img\"</code> and <code>aria-label</code>. The star rating is one image labelled \"Rated 4.8 out of 5 from 23 reviews\", not five icons.",
            "Status icons pair with colour and words: info, check-circle, alert and x-circle in alerts and toasts.",
            "Icons take the colour of their text. Don't colour an icon differently from its label except status icons in alerts and toasts.",
            "New icons: draw on the 24 grid, 2px stroke, round caps, square rectangles; add to <code>ICONS</code> and to this sheet.")),
        ("accessibility", "Accessibility", ul("Icon-only targets are at least 24×24px (2.5.8) and 40px in the top bar.", "Icons used as the only indicator of state (filled star) have a text equivalent in the accessible name.", "Icons keep 3:1 against their background because they use the text colours.")),
    ])

# ---------------------------------------------------------------------------
# Theming
# ---------------------------------------------------------------------------
foundation("theming", "Theming",
    lead="Light and dark from one token file. Themes override semantic tokens only; components and pages never know which theme they are in.",
    covers="How themes work, the token tiers, adding a theme, component re-skins and consuming tokens.json.",
    sections=[
        ("overview", "Overview", p("Light is <code>:root</code>. Dark applies with <code>data-theme=\"dark\"</code> on <code>&lt;html&gt;</code> or any container, and automatically when the OS prefers dark and the page hasn't forced <code>data-theme=\"light\"</code>. Each theme sets <code>color-scheme</code> so native controls and scrollbars follow.")
            + themes(f'<div class="stack stack--sm"><div class="cluster">{btn("Buy now", "primary")}{btn("Make an offer")}</div><label class="visually-hidden" for="th-q">Search 12L</label><input class="input" id="th-q" placeholder="Search brands and items"></div>')),
        ("tiers", "Token tiers", table(["Tier", "Prefix", "Example", "Who reads it"], [
            ["Primitive", "<code>--palette-*</code>, <code>--font-*</code>", "<code>--palette-ink-950: #0b0b0b</code>", "Only semantic tokens"],
            ["Semantic", "<code>--color-*</code>, <code>--text-*</code>, <code>--space-*</code>, …", "<code>--color-accent: var(--palette-ink-950)</code>", "Components and pages; themes override this tier"],
            ["Component", "<code>--btn-*</code>, <code>--field-*</code>, <code>--alert-*</code>, <code>--card-*</code>, <code>--chip-*</code>, <code>--toast-*</code>, <code>--dialog-*</code>", "<code>--btn-bg: var(--color-accent)</code>", "One component; declared in components.css"]])
            + p("Changing the brand hue touches primitives; changing what \"accent\" means touches semantic tokens; changing how buttons look touches component tokens.")),
        ("adding", "Adding a theme", pre("""
[data-theme="partner"] {
  --color-accent: var(--palette-blue-700);
  --color-accent-hover: var(--palette-blue-500);
  --color-fg-on-accent: var(--palette-white);
  --color-focus-ring: var(--palette-blue-700);
  color-scheme: light;
}""") + ul("Override semantic tokens only; never a component class.", "Add the theme's pairs (or run the existing list against it) with <code>scripts/check_contrast.py</code>; every pair must pass.",
           "Regenerate <code>tokens.json</code> with <code>scripts/tokens_to_json.py</code>.", "Keep the two dark blocks in <code>tokens.css</code> identical; the OS-preference block is a copy.")),
        ("reskin", "Re-skinning one surface", p("To change a component on one surface, override its component tokens there. The cookie consent does this to put buttons on an inverse surface:")
            + pre(".consent .btn { --btn-bg: transparent; --btn-fg: var(--color-fg-inverse); --btn-border: var(--color-border-inverse); }")),
        ("preferences", "User preferences", ul("<code>prefers-contrast: more</code> raises default borders to strong and muted text to default.",
            "<code>forced-colors: active</code> hands the focus ring and borders to system colours; buttons, inputs, cards, chips and badges draw a CanvasText border.",
            "<code>prefers-reduced-motion</code> zeroes durations; see " + found("motion") + ".")),
        ("json", "tokens.json", p("<a href=\"../tokens/tokens.json\"><code>tokens/tokens.json</code></a> is a W3C Design Tokens (DTCG) export: <code>--color-bg-canvas</code> becomes <code>color.bg.canvas</code>, single <code>var()</code> references become aliases (<code>{palette.paper.50}</code>), and the dark theme lives under <code>$extensions</code>. Use it to generate Angular SCSS maps, .NET constants for email templates, or native colour assets. Regenerate it whenever <code>tokens.css</code> changes:")
            + pre("python .claude/skills/extracting-design-systems/scripts/tokens_to_json.py docs/design-system/tokens/tokens.css")),
        ("usage", "Do and don't", dodont([
            ("do", '<code>color: var(--color-fg-muted);</code>', "Read semantic tokens in components."),
            ("dont", '<code>color: var(--palette-stone-700);</code>', "Read primitives in components; the dark theme can't remap them."),
            ("do", '<code>[data-theme="dark"] { --color-accent: … }</code>', "Change meaning in a theme block."),
            ("dont", '<code>[data-theme="dark"] .btn--primary { background: … }</code>', "Patch components per theme.")])),
    ])

# ---------------------------------------------------------------------------
# Responsive
# ---------------------------------------------------------------------------
foundation("responsive", "Responsive",
    lead="Designed at 360px first and checked at 320px. Every screen works on a phone with one thumb, then gains columns as the viewport grows.",
    covers="Mobile-first rules, what each component does at each breakpoint, touch rules and the testing matrix.",
    sections=[
        ("overview", "Overview", p("Most 12L traffic is a phone in one hand. The base layout is a single column with 16px margins, a sticky top bar and, on listing detail, a sticky buy bar. Breakpoints add columns; they never remove content. See " + found("layout") + " for the breakpoints and grid.")),
        ("components", "Component behaviour by breakpoint", table(["Component", "Below 640px", "640–1023px", "1024px and up"], [
            [comp("top-bar"), "Menu button, logo, search icon, avatar", "+ category nav and Sell from 768px", "+ search field"],
            [comp("listing-card") + " grid", "2-up, 32/16px gaps", "3-up from 768px, 40/24px gaps", "4-up; 3-up beside filters, 4-up again from 1280px"],
            ["Catalog filters", "Filters button opens the full-screen " + comp("drawer", "filter sheet"), "Filter sheet docks left (24rem) from 768px", "Sticky sidebar, 14rem"],
            [comp("gallery"), "Edge to edge with dots", "Inset, with thumbnails", "Thumbnails, no dots, beside the sticky info column"],
            [comp("buy-bar"), "Sticky at the bottom; large block buttons", "Same", "Static in the info column"],
            [comp("dialog"), "Bottom sheet, full width, 6px top corners", "Centred, max 32rem (sm 24rem, lg 48rem)", "Same"],
            [comp("toast"), "Full width at the bottom", "24rem, bottom-right", "Same"],
            [comp("form-layout") + " rows", "One column", "Two columns", "Two columns"],
            [comp("tabs", "Account tabs"), "Scroll horizontally", "Scroll if needed", "All visible"],
            [comp("stepper"), "Only the current step's label is visible", "All labels from 768px", "All labels"],
            [comp("table"), "Scrolls inside its frame", "Same", "Fits"]])),
        ("touch", "Touch", ul("Interactive targets are at least 24×24px (2.5.8). Nav links, tabs, segmented options, accordion rows and star inputs are 44px.",
            "Row actions in tables are always visible on devices without hover (<code>@media (hover: none)</code>).",
            "Nothing depends on hover: tooltips also show on focus, and every hover-only reveal has a visible alternative.",
            "Sticky bars stay under 20% of a 360×640 viewport.")),
        ("rules", "Rules", ul("Content reflows at 320px without horizontal scrolling (1.4.10); only tables and the gallery thumbnails scroll inside their own frame.",
            "Never hide content at small sizes; move it (into the menu sheet, the filter sheet, below the fold).",
            "Labels never truncate; listing titles and order meta may ellipsize because the full text is one tap away.",
            "Pinch zoom is never disabled.")),
        ("testing", "Testing matrix", table(["Viewport", "Why"], [["320×640", "Smallest supported; reflow check"], ["360×800", "Design width; most phones"], ["768×1024", "Tablet; nav and grid change"],
            ["1024×768", "Filters sidebar and two-column detail appear"], ["1280×800", "Design width for desktop"], ["1536×900", "Container max holds"]])
            + p("Check each in light and dark, with 200% zoom at 1280px, and with the keyboard only.")),
    ])

# ---------------------------------------------------------------------------
# Accessibility
# ---------------------------------------------------------------------------
foundation("accessibility", "Accessibility",
    lead="Every component and token in this system is designed to meet WCAG 2.2 AA in both themes. These are the commitments a 12L screen keeps, and how to check them.",
    covers="WCAG 2.2 AA commitments, focus, targets, testing procedure and the component contract.",
    sections=[
        ("overview", "Overview", p("Accessibility is part of each component's definition, not a review step. Every component page documents its role and pattern, keyboard map, focus behaviour, labelling, live contrast pairs, motion and touch targets.")),
        ("commitments", "Commitments", '<ul class="ds-checklist">' + "".join(f"<li><span>{x}</span></li>" for x in [
            "<b>1.1.1</b> Product photos have alt text naming brand and item; decorative icons are hidden.",
            "<b>1.3.1</b> Structure is in the markup: landmarks, one h1, headings in order, lists, tables with captions and scope, fieldsets with legends.",
            "<b>1.4.1</b> Colour is never the only signal: statuses have words, errors have icons and text, the current page has a bar and <code>aria-current</code>.",
            "<b>1.4.3</b> Text is at least 4.5:1; <b>1.4.11</b> control edges, focus rings and meaningful icons at least 3:1, in both themes (checked by <code>check_contrast.py</code>).",
            "<b>1.4.4 / 1.4.10 / 1.4.12</b> Text resizes to 200%, reflows at 320px and survives text-spacing overrides.",
            "<b>2.1.1</b> Everything works with a keyboard; there are no keyboard traps (dialogs trap focus but close with Esc).",
            "<b>2.4.1</b> A skip link is the first focusable element on every page.",
            "<b>2.4.3</b> Focus order follows reading order; dialogs move focus in and return it to the trigger.",
            "<b>2.4.7 / 2.4.11</b> A 2px focus ring with a 2px offset is always visible and never hidden by sticky bars.",
            "<b>2.5.8</b> Targets are at least 24×24px; primary touch targets are 44px.",
            "<b>3.3.1 / 3.3.3</b> Errors are described in text next to the field and summarised at the top of long forms with links to each field.",
            "<b>3.3.7 / 3.3.8</b> Checkout never asks for the same information twice; sign-in allows password managers and paste.",
            "<b>4.1.2</b> Custom controls expose name, role and state: <code>aria-pressed</code>, <code>aria-expanded</code>, <code>aria-selected</code>, <code>aria-current</code>, <code>aria-invalid</code>, <code>aria-busy</code>.",
            "<b>4.1.3</b> Status messages (toasts, form saves, timers) use polite live regions; errors use <code>role=\"alert\"</code>."]) + "</ul>"),
        ("focus", "Focus", p("One ring everywhere: <code>outline: var(--focus-ring-width) solid var(--color-focus-ring)</code> with <code>var(--focus-ring-offset)</code>, shown on <code>:focus-visible</code> only. Inputs draw it at 0 offset over their border. On inverse surfaces (toasts, consent) the ring switches to <code>--color-fg-inverse</code>.")
            + ex(btn("Buy now", "primary", attrs='data-state="focus"') + btn("Make an offer", attrs='data-state="focus"') + '<label class="visually-hidden" for="fa-in">Email</label><input class="input" id="fa-in" data-state="focus" style="max-width: 14rem;" value="marcus.bell@example.com">', show_code=False)
            + pairs([("Ring on canvas", "--color-focus-ring", "--color-bg-canvas", 3), ("Ring on surface", "--color-focus-ring", "--color-bg-surface", 3)])),
        ("testing", "Testing procedure", "<ol>" + "".join(f"<li>{x}</li>" for x in [
            "Run <code>check_contrast.py</code> and <code>check_design_system.py</code>; both exit 0.",
            "Tab through the page: every control is reachable, the order makes sense, the ring is always visible.",
            "Operate every component with the keys in its keyboard map.",
            "Zoom to 200% at 1280px and view at 320px: nothing overlaps or scrolls sideways.",
            "Turn on reduced motion and forced colours; check focus and borders remain visible.",
            "Listen with a screen reader (VoiceOver or NVDA): names, roles, states, live regions and dialog titles are announced.",
            "Switch to dark and repeat the contrast spot checks."]) + "</ol>"),
        ("contract", "The component contract", p("A component is ready when its page documents, and its CSS provides:") + ul(
            "Native element first; ARIA only where HTML has no equivalent, following the named WAI-ARIA APG pattern.",
            "Every state reachable by attribute (<code>disabled</code>, <code>aria-*</code>), not by class alone.",
            "Visible focus, 24px targets, labels that match the visible text (2.5.3).",
            "Every colour pairing listed in <code>contrast-pairs.json</code>.",
            "Motion through duration tokens, so reduced motion applies automatically.")),
        ("tokens", "Tokens", all_tokens("accessibility")),
    ])

# ---------------------------------------------------------------------------
# Content
# ---------------------------------------------------------------------------
foundation("content", "Content",
    lead="12L talks like a friend who also wears a 12: short, plain, specific. Sentence case, real numbers, verbs on buttons, and no filler.",
    covers="Voice and tone, sentence case, button verbs, numbers, money, dates and times, error and empty-state formulas, microcopy library.",
    sections=[
        ("overview", "Overview", p("Copy is part of the design. The mocks use short real copy and nothing that fills space; this page writes down the rules they follow. For the full pattern see " + patt("content-and-tone") + ".")),
        ("voice", "Voice and tone", table(["We are", "So we write", "Not"], [
            ["Plain", "Your order shipped.", "Your order has been successfully dispatched!"], ["Specific", "Ships by Fri 30 Oct.", "Ships soon."],
            ["Calm about problems", "Your bank declined the payment. Try another card.", "Oops! Something went wrong :("],
            ["On the member's side", "We'll refund you within 5 business days.", "Refunds are subject to processing."]])),
        ("mechanics", "Mechanics", ul("Sentence case everywhere, including buttons, titles and tabs. Proper nouns keep their capitals (Red Wing, Patagonia).",
            "Buttons are verbs: <i>Buy now</i>, <i>List item</i>, <i>Add tracking</i>, <i>Confirm receipt</i>.",
            "Sizes are written <i>US 12</i> for shoes and <i>L</i> for clothes; long form <i>Men's US 12</i>, <i>Men's L</i>.",
            "Money: <i>$85</i> in the catalog when there are no cents, <i>$94.00</i> in checkout and totals, always with the currency symbol.",
            "Dates: <i>Sun 25 Oct 2026</i>; drop the year in the current year when space is tight (<i>Fri 30 Oct</i>). Relative times only for recent things: <i>2 hours ago</i>, <i>Yesterday</i>.",
            "Times: 12-hour with lowercase am/pm, <i>3:40 pm</i>. Countdowns use tabular figures: <i>9:42</i>.",
            "References are monospace and uppercase: <i>12L-48213</i>, <i>L-20931</i>.",
            "Counts: numerals always (<i>3 reviews</i>, <i>1 review</i>), thousands separators from 1,000.")),
        ("errors", "Error message formula", p("<b>What happened + how to fix it</b>, in one or two short sentences, next to the thing that failed.")
            + table(["Situation", "Message"], [["Empty required field", "Enter a title."], ["Format", "Enter an email address like name@example.com."],
                ["Out of range", "Enter a price between $5 and $5,000."], ["Server failed", "We couldn't save your changes. Try again."], ["Card declined", "Your bank declined the payment. Try another card."]])
            + p("Never blame (\"invalid input\"), never use codes alone, never \"Oops\".")),
        ("empty", "Empty-state formula", p("<b>Title</b> (what's here, or not) + <b>one sentence</b> (why, or what will appear) + <b>one action</b>.")
            + ex(f'<div class="empty empty--compact"><div class="empty__icon">{ic("bag", "icon icon--lg")}</div><p class="empty__title">No purchases yet</p><p class="empty__text">Items you buy will show up here with tracking and receipts.</p><div class="empty__actions">{btn("Browse size 12", "primary", href="#")}</div></div>', show_code=False)),
        ("library", "Microcopy library", table(["Use", "Say"], [
            ["Primary purchase", "Buy now · Make an offer · Pay $94.00"], ["Selling", "List item · Save draft · Withdraw listing · Relist"],
            ["Orders", "Add tracking · Confirm receipt · Report a problem · Request cancellation"], ["Dismiss", "Close (dialogs) · Dismiss (toasts, banners)"],
            ["Safe option in confirmations", "Keep listing · Keep order"], ["Loading", "Loading listings (screen readers only)"],
            ["Optional fields", "(optional) after the label; required is the default"], ["No reviews", "No reviews yet"], ["New seller", "New seller"]])),
    ])
