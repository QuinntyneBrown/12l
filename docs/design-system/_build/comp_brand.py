"""12L brand components: the marketplace-specific layer built on the generic kit.

logo, size-tag, photo, listing-card, price, rating, gallery, order-summary, review, buy-bar
"""
from ds import *

G = "12L brand"


# ---------------------------------------------------------------------------
# Local helpers (mirror docs/mocks/_build/mk.py and the screen modules)
# ---------------------------------------------------------------------------
def money(v: float) -> str:
    return f"${v:,.2f}"


def item_row(key: str, meta: str | None = None, thumb: str = "thumb") -> str:
    it = ITEMS[key]
    meta = meta or f'{esc(it["brand"])} · {"Men\'s US 12" if it["cat"] == "Shoes" else "Men\'s L"} · {esc(it["cond"])}'
    return (f'<div class="item-row"><div class="{thumb}">{photo(key, tag=False, alt="")}</div>'
            f'<div class="item-row__body"><span class="item-row__title">{esc(it["title"])}</span><span class="item-row__meta">{meta}</span></div></div>')


def totals(rows: list[tuple[str, str]], total: tuple[str, str]) -> str:
    r = "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in rows)
    return f'<dl class="totals">{r}<div class="totals__total"><dt>{total[0]}</dt><dd>{total[1]}</dd></div></dl>'


def avatar(initials: str) -> str:
    return f'<span class="avatar avatar--sm" aria-hidden="true">{initials}</span>'


def review(author: str, initials: str, n: int, date: str, text: str, reply: str | None = None, reply_link: bool = False) -> str:
    rp = f'<div class="review__reply"><strong>Reply:</strong> {esc(reply)}</div>' if reply else ""
    rb = '<a class="text-sm" href="#" style="align-self: flex-start;">Reply</a>' if reply_link and not reply else ""
    stars_html = (f'<span class="rating" role="img" aria-label="Rated {n} out of 5"><span class="rating__stars">{stars(n)}</span>'
                  f'<span class="rating__value">{n:.1f}</span></span>')
    return (f'<article class="review"><div class="review__head">{avatar(initials)}<a href="#">{author}</a>{stars_html}'
            f'<span class="text-caption"><time datetime="2026-10-25">{date}</time></span></div><p>{esc(text)}</p>{rp}{rb}</article>')


WORDS = ["Poor", "Fair", "Good", "Great", "Excellent"]


def star_input(name: str, value: int = 0, err: bool = False, focus: int = 0, legend: str = "Rating") -> str:
    lab = ""
    for i in range(1, 6):
        on = "is-on" if i <= value else ""
        chk = " checked" if i == value else ""
        inv = ' aria-invalid="true"' if err else ""
        icon = ic("star").replace('class="icon"', 'class="icon" data-state="focus"') if i == focus else ic("star")
        lab += (f'<label class="{on}"><input type="radio" name="{name}" value="{i}"{chk}{inv}>{icon}'
                f'<span class="visually-hidden">{i} star{"s" if i > 1 else ""}, {WORDS[i - 1]}</span></label>')
    e = f'<span class="field__error" id="{name}-error">Choose a rating from 1 to 5 stars</span>' if err else ""
    cap = f'<span class="text-sm text-muted">{WORDS[value - 1]}</span>' if value else ""
    db = f' aria-describedby="{name}-error"' if err else ""
    return (f'<fieldset{db}><legend>{legend}</legend><div class="cluster" style="gap: var(--space-3);"><div class="star-input">{lab}</div>{cap}</div>{e}</fieldset>')


def gallery(key: str, current: int = 1, n: int | None = None, thumb_state: dict | None = None) -> str:
    it = ITEMS[key]
    n = n or min(it["photos"], 6)
    thumb_state = thumb_state or {}
    thumbs = ""
    for i in range(1, n + 1):
        tone = ((it["tone"] + i - 2) % 6) + 1
        cur = ' aria-current="true"' if i == current else ""
        st = f' data-state="{thumb_state[i]}"' if i in thumb_state else ""
        thumbs += (f'<li><button type="button" aria-label="Show photo {i} of {n}"{cur}{st}>'
                   f'<div class="photo photo--{tone}"><img src="{MOCK_ASSETS}items/{it["img"]}.svg" alt="" width="160" height="160" loading="lazy"></div></button></li>')
    dots = "".join(f'<span{" aria-current=\"true\"" if i == current else ""}></span>' for i in range(1, n + 1))
    return (f'<section class="gallery" aria-label="Photos"><div class="gallery__main">{photo(key, tag=False, alt=f"Photo {current} of {n}, {it["brand"]} {it["title"]}")}</div>'
            f'<div class="gallery__dots" aria-hidden="true">{dots}</div><ul class="gallery__thumbs" role="list">{thumbs}</ul></section>')


def buy_bar(total: float, actions: str, phone: bool = False) -> str:
    """phone=True pins the bar to the bottom of a demo frame with inline styles (the real
    bar is sticky below 1024px through a viewport media query the docs cannot trigger)."""
    style = ""
    price_style = ""
    if phone:
        style = (' style="position: absolute; left: 0; right: 0; bottom: 0; margin: 0; padding: var(--space-3) var(--space-4);'
                 ' background: var(--color-bg-surface); border-top: var(--border-width-hairline) solid var(--color-border-default);"')
        price_style = ' style="display: flex;"'
    return (f'<div class="buy-bar"{style}><div class="buy-bar__price"{price_style}><span class="price">{money(total)}</span>'
            f'<span class="text-caption">incl. shipping</span></div>{actions}</div>')


def logo_img(theme: str = "light", h: str = "2.75rem") -> str:
    f = "logo.svg" if theme == "light" else "logo-dark.svg"
    return f'<img src="../assets/{f}" alt="12L" style="height: {h}; width: auto;">'


# ---------------------------------------------------------------------------
# Logo
# ---------------------------------------------------------------------------
component(
    "logo", "Logo", G,
    lead="The 12L wordmark: two heavy ink numerals and a signal-red L with one 45° cut. It links home and is the only place the red appears at full size.",
    pills=["Inline SVG", "<code>.logo</code>"],
    summary_variants="sm (footer), md (top bar), lg (auth); inline SVG and static files for light and dark",
    summary_states="default, hover, focus",
    overview=p("The logo identifies 12L and takes the member home. In the product it is always inline SVG inside <code>&lt;a class=\"logo\"&gt;</code>, so the ink numerals follow <code>currentColor</code> (ink in light, paper in dark) while the L stays <code>--color-brand</code>. Static files in "
               "<code>docs/design-system/assets/</code> (<code>logo.svg</code>, <code>logo-dark.svg</code>, PNG and favicon) are for email, social and app icons where CSS cannot reach.")
    + ul("<b>Top bar</b> (medium, 26px tall) on every member and admin page.",
         "<b>Auth</b> (large, 44px) centred above sign-in, register and password screens.",
         "<b>Footer</b> (small, 18px) beside the legal links.",
         f"The red L is never used as a general accent colour; for <i>indicators</i> (current page, current order step) use {found('color', '--color-brand')} as a 3px bar, not as text."),
    anatomy=anatomy(
        logo("logo--lg"),
        [("26%", "16%"), ("48%", "16%"), ("72%", "16%"), ("82%", "76%")],
        [("1", "Ink numeral; <code>.logo__ink</code>, fills with <code>currentColor</code>."),
         ("2", "Ink numeral with the diagonal; same fill."),
         ("L", "Signal red <code>--color-brand</code>; <code>.logo__l</code>. Never recoloured."),
         ("The cut", "One 45° chamfer at the bottom right of the L. It is the source of the size tag's and confirmation mark's chamfer.")]),
    variants=p("One mark, rendered two ways. Inline SVG in the product (it themes itself); static files outside it.")
    + ex(logo() + logo("logo--sm"), "Inline SVG: the numerals follow the text colour, the L stays red.")
    + "<h3>Static files</h3>"
    + themes(logo_img("dark"), logo_img("light"))
    + p("<code>logo.svg</code> (ink numerals) on light backgrounds; <code>logo-dark.svg</code> (paper numerals) on ink. <code>app-icon.svg</code> and <code>favicon.ico</code> use the L alone on ink."),
    sizes=p("Height is the only dimension set; width follows the 192:108 viewBox.")
    + ex(logo("logo--sm") + logo() + logo("logo--lg"), "Small 18px (<code>.logo--sm</code>, footer) · medium 26px (default, top bar) · large 44px (<code>.logo--lg</code>, auth).")
    + p("Below 18px the numerals' counters close up; use the app icon instead. Clear space on every side is at least the width of the L's stem (about a quarter of the height): nothing, not even the admin tag, sits closer."),
    states=p("The logo is a link. It has no hover colour change (the brand mark does not flicker); the focus ring is the shared ring.")
    + matrix(["Default", "Hover", "Focus"], [
        ("Top bar", [logo(), logo(href="#").replace('class="logo "', 'class="logo " data-state="hover"'), logo().replace('class="logo "', 'class="logo " data-state="focus"')]),
        ("Footer", [logo("logo--sm"), logo("logo--sm").replace('class="logo logo--sm"', 'class="logo logo--sm" data-state="hover"'), logo("logo--sm").replace('class="logo logo--sm"', 'class="logo logo--sm" data-state="focus"')]),
    ], "Placement")
    + "<h3>Both themes</h3>" + themes(f'<div class="cluster">{logo()}{logo("logo--sm")}</div>'),
    responsive=ul("The top-bar logo stays medium at every width; on phones it sits after the menu button, on tablet and up before the category links.",
                  "Auth screens keep the large logo at every width and centre it above the card.",
                  "The admin shell shows the red <i>Admin</i> tag after the logo with <code>--space-3</code> between them, never touching the L."),
    theming=p("Two colours, two mechanisms: the numerals use <code>currentColor</code> (so <code>--color-fg-default</code> in both themes), and the L uses <code>--color-brand</code>, which is <code>--palette-signal-500</code> in light <i>and</i> dark. On ink the red keeps 3.3:1 against the canvas.")
    + pre("""
.logo svg .logo__ink { fill: currentColor; }
.logo svg .logo__l   { fill: var(--color-brand); }"""),
    accessibility=a11y(
        pattern="A link (<code>&lt;a class=\"logo\" href=\"/\"&gt;</code>) with <code>aria-label=\"12L home\"</code>; the SVG inside is <code>aria-hidden</code> and <code>focusable=\"false\"</code>. A static <code>&lt;img&gt;</code> logo has <code>alt=\"12L\"</code>.",
        keyboard=[(kbd("Tab"), "Reaches the logo after the skip link and menu button."), (kbd("Enter"), "Goes to the catalog (members) or the moderation queue (admin).")],
        focus="Shared 2px ring with 2px offset around the whole mark.",
        labelling="<i>12L home</i> in the top bar; the footer logo has the same name. Never <i>logo</i> or <i>image</i>.",
        contrast=[("Numerals on canvas", "--color-fg-default", "--color-bg-canvas", 4.5), ("Red L on canvas", "--color-brand", "--color-bg-canvas", 3),
                  ("Red L on top bar", "--color-brand", "--color-bg-surface", 3)],
        motion="None. The mark never animates.",
        touch="The medium logo link is 26px tall inside a 64px top bar; its hit area is padded to the bar height so it clears the 44px target."),
    content=ul("Write the name as <b>12L</b>: digits then a capital L, no space, never <i>12l</i>, <i>Twelve L</i> or <i>12-L</i>.",
               "In sentences the name is plain text, not the logo.",
               "Alt text and labels say <i>12L</i> or <i>12L home</i>; nothing about colours or shapes."),
    do_dont=dodont([
        ("do", logo(), "Keep the L signal red and the numerals in the text colour."),
        ("dont", f'<span style="color: var(--color-fg-default);">{logo().replace("logo__l", "logo__ink")}</span>', "Recolour the L to match the numerals, or the numerals to match the L."),
        ("do", f'<div class="cluster" style="gap: var(--space-3);">{logo()}<span class="topbar__admin">Admin</span></div>', "Give the admin tag clear space after the mark."),
        ("dont", f'<div class="cluster" style="gap: 0;">{logo()}<span class="topbar__admin">Admin</span></div>', "Butt a label against the L; it reads as part of the mark."),
    ]),
    tokens=token_table([("Numerals", "--color-fg-default"), ("L", "--color-brand"), ("Admin tag", "--color-brand / --color-fg-on-brand"),
                        ("Clear space beside a tag", "--space-3"), ("Height sm / md / lg", "--font-size-lg / --font-size-2xl / --space-10")])
    + p("Logo heights are set in <code>components.css</code> (1.125rem, 1.625rem, 2.75rem) because they are optical sizes of the mark, not spacing; the row above lists the nearest scale values for reference."),
    code=pre("""
<a class="logo" href="/" aria-label="12L home">
  <svg viewBox="-4 -4 192 108" aria-hidden="true" focusable="false">
    <polygon class="logo__ink" points="0,14 20,0 40,0 40,100 20,100 20,24 0,38"/>
    <polygon class="logo__ink" points="52,0 112,0 112,50 78,80 112,80 112,100 52,100 52,76 92,41 92,20 52,20"/>
    <polygon class="logo__l" points="124,0 144,0 144,80 170,80 184,66 184,88 172,100 124,100"/>
  </svg>
</a>""")
    + classes([("<code>.logo</code>", "Medium mark (26px), link reset."), ("<code>.logo--sm</code> <code>.logo--lg</code>", "Footer (18px) and auth (44px) sizes."),
               ("<code>.logo__ink</code>", "Numeral polygons; fill <code>currentColor</code>."), ("<code>.logo__l</code>", "The L; fill <code>--color-brand</code>."),
               ("<code>.topbar__admin</code>", "Red <i>Admin</i> tag shown after the logo in the admin shell.")]),
    sources=sources([("pages/catalog/default", "top-bar logo and footer logo"), ("pages/sign-in/default", "large auth logo"),
                     ("pages/moderation-queue/default", "logo with the Admin tag")]),
)


# ---------------------------------------------------------------------------
# Size tag
# ---------------------------------------------------------------------------
drift("assets/ui.css (.size-tag, .photo__stamp, .topbar__admin)",
      "The size tag, photo stamps and admin tag read --palette-ink-950, --palette-paper-100 and --palette-white directly, skipping the semantic tier.",
      "Added semantic --color-size-tag-bg/-fg, --color-stamp-bg/-fg and --color-fg-on-brand; components.css reads only those. Values unchanged.")

component(
    "size-tag", "Size tag", G,
    lead="The ink block that says US 12 or L. Every 12L listing is men's US 12 (shoes) or men's L (everything else); the tag carries that promise with the logo's 45° cut.",
    pills=["<code>.size-tag</code>", "Chamfer from the logo"],
    summary_variants="default (cards, photos), large (listing detail, category tiles)",
    summary_states="static; on photo, on canvas, in tile",
    overview=p("The size tag is a label, not a control. It appears on every listing photo (bottom left), next to the condition on listing detail, and on category tiles. It is the same ink-on-paper block in both themes because it usually sits on a light studio photo.")
    + ul("Shoes read <b>US 12</b>; tops, outerwear and bottoms read <b>L</b>.",
         "The number or letter is black-weight; the prefix (US) is the overline style.",
         "There is no other size: the tag never shows 11.5, XL or a range. A listing in another size cannot exist on 12L."),
    anatomy=anatomy(
        size_tag("US 12", "size-tag--lg"),
        [("8%", "20%"), ("52%", "20%"), ("90%", "78%")],
        [("Prefix", "<code>--text-overline</code>, uppercase, wide tracking. Shoes only."),
         ("Size", "<code>&lt;b&gt;</code>, black weight, one step larger than the prefix."),
         ("Chamfer", "45° cut at the bottom right, <code>--chamfer</code> × 0.7 (default) by <code>clip-path</code>; padding on the right makes room for it.")]),
    variants=ex(size_tag("US 12") + size_tag("L"), "Default: on listing-card photos and thumbnails.")
    + ex(size_tag("US 12", "size-tag--lg") + size_tag("L", "size-tag--lg"), "Large: listing detail beside the condition, and category tiles."),
    sizes=p("Two sizes. Default is 12px overline with a 14px size; large is 14px with an 18px size and more padding.")
    + ex(size_tag("US 12") + size_tag("US 12", "size-tag--lg"), "Default · large (<code>.size-tag--lg</code>)."),
    states=p("Not interactive, so no hover, focus or disabled. What changes is the context it sits on; the tag itself never changes colour.")
    + matrix(["On photo", "On canvas", "In category tile"], [
        ("Shoes", [f'<div style="width: 8rem;">{photo("air-max-90")}</div>', f'<div class="cluster">{size_tag("US 12", "size-tag--lg")}<span class="text-muted">Used - Excellent</span></div>',
                   '<a class="category-tile" href="#" style="width: 10rem;"><span class="category-tile__name">Shoes</span>' + size_tag("US 12") + "</a>"]),
        ("Clothing", [f'<div style="width: 8rem;">{photo("better-sweater")}</div>', f'<div class="cluster">{size_tag("L", "size-tag--lg")}<span class="text-muted">Used - Good</span></div>',
                      '<a class="category-tile" href="#" style="width: 10rem;"><span class="category-tile__name">Outerwear</span>' + size_tag("L") + "</a>"]),
    ], "Category")
    + "<h3>Both themes</h3>" + themes(f'<div class="cluster">{size_tag("US 12")}{size_tag("L", "size-tag--lg")}<div style="width: 6rem;">{photo("nb-990")}</div></div>'),
    responsive=ul("The tag never scales with the viewport; on a 2-up phone grid it is the same 12px tag as on desktop.",
                  "On photos it stays pinned to the bottom-left corner, flush with the edges, so it survives any crop.",
                  "On thumbnails smaller than 4rem (order rows, uploader tiles) the tag is omitted: the row text already says <i>Men's US 12</i>."),
    theming=p("The tag reads <code>--color-size-tag-bg</code> and <code>--color-size-tag-fg</code>, fixed to ink and paper in both themes. Product photos keep a light backdrop in dark mode, so an ink tag stays readable on them; inverting it would put a paper block on a paper photo."),
    accessibility=a11y(
        pattern="A <code>&lt;span&gt;</code> with <code>aria-label=\"Size US 12\"</code> (or <i>Size L</i>) so screen readers hear a word, not a fragment. Inside a listing card link, the label becomes part of the link text.",
        keyboard="Not focusable; it is read as part of its card or row.",
        focus="Not applicable to the tag; the card around it shows the ring.",
        labelling="<code>aria-label=\"Size US 12\"</code>. Never rely on the shape or colour to say it is a size.",
        contrast=[("Label on tag", "--color-size-tag-fg", "--color-size-tag-bg", 4.5), ("Tag edge on sand photo", "--color-size-tag-bg", "--color-photo-bg-1", 3),
                  ("Tag edge on cool photo", "--color-size-tag-bg", "--color-photo-bg-4", 3)],
        motion="None.",
        touch="Not a target."),
    content=ul("Shoes: <b>US 12</b> (prefix, space, number). Everything else: <b>L</b>.", "In running text write <i>Men's US 12</i> and <i>Men's L</i>; the tag is the short form.",
               "Never pluralise, never add <i>size</i> inside the tag."),
    do_dont=dodont([
        ("do", f'<div style="width: 8rem;">{photo("samba-og")}</div>', "Pin the tag to the photo's bottom-left corner."),
        ("dont", f'<div style="width: 8rem;"><div class="photo photo--2"><img src="{MOCK_ASSETS}items/sneaker-samba.svg" alt="Adidas Samba OG" width="160" height="160"><span class="size-tag" aria-label="Size US 12" style="position: absolute; right: var(--space-3); top: var(--space-3);">US <b>12</b></span></div></div>',
         "Float the tag over the product; the chamfer points at nothing and it covers the item."),
        ("do", size_tag("L", "size-tag--lg"), "Keep ink on paper in both themes."),
        ("dont", '<span class="size-tag size-tag--lg" aria-label="Size L" style="background: var(--color-brand); color: var(--color-fg-on-brand);"><b>L</b></span>', "Paint the tag red; red is reserved for the logo and indicators."),
    ]),
    tokens=token_table([("Background", "--color-size-tag-bg"), ("Label", "--color-size-tag-fg"), ("Chamfer", "--chamfer"), ("Prefix font", "--text-overline"),
                        ("Tracking", "--letter-spacing-wide"), ("Size weight", "--font-weight-black"), ("Padding", "--space-0-5 / --space-2 / --space-3")]),
    code=pre("""
<span class="size-tag" aria-label="Size US 12">US <b>12</b></span>
<span class="size-tag size-tag--lg" aria-label="Size L"><b>L</b></span>""")
    + classes([("<code>.size-tag</code>", "Ink block with the chamfer; default size."), ("<code>.size-tag--lg</code>", "Large: detail page and category tiles."),
               ("<code>&lt;b&gt;</code>", "The size itself, black weight."), ("<code>aria-label</code>", "Required: <i>Size US 12</i> or <i>Size L</i>.")]),
    sources=sources([("pages/catalog/default", "tags on every card photo"), ("pages/listing-detail/default", "large tag beside the condition"),
                     ("pages/catalog/guest", "category tiles")],
                    "the tag read palette primitives directly; it now reads <code>--color-size-tag-*</code> (see README drift log)."),
)


# ---------------------------------------------------------------------------
# Photo
# ---------------------------------------------------------------------------
drift("assets/tokens.css (--photo-bg-1..6)",
      "Photo backdrops were declared as unprefixed --photo-bg-* custom properties, outside both the primitive and the semantic tier.",
      "Renamed to primitives --palette-photo-1..6 with semantic --color-photo-bg-1..6; .photo--1..6 read the semantic tokens.")

PHOTO_KEYS = ["iron-ranger", "samba-og", "park-avenue", "nb-990", "detroit-jacket", "air-max-90"]

component(
    "photo", "Photo", G,
    lead="The product photo frame: a 4:5 studio backdrop in one of six warm tones, the item centred, the size tag in the corner and a stamp when it is reserved or sold.",
    pills=["<code>.photo</code>", "4:5 and 1:1"],
    summary_variants="tones 1-6; portrait 4:5, square; stamps Reserved and Sold; thumb, large thumb; no photo",
    summary_states="default, hover zoom (in cards), reserved, sold, loading, missing",
    overview=p("Every listing image sits in <code>.photo</code>: square corners, a light studio backdrop that stays light in dark mode (real photos would), and an aspect ratio that never shifts while the image loads. "
               f"Cards use the 4:5 portrait frame; thumbnails in order rows, the uploader and the gallery strip use the square frame. Missing photos (a draft without images) show {comp('empty-state', 'an icon on subtle')} instead of a broken image.")
    + ul("<b>Tone</b> (<code>.photo--1</code> to <code>--6</code>) is assigned per listing so a grid reads as a set of different products, not one flat block.",
         "<b>Stamp</b> (<i>Reserved</i>, <i>Sold</i>) sits top left; the size tag sits bottom left.",
         "<b>Thumb</b> wraps a square photo at 56px (<code>.thumb</code>) or 80px (<code>.thumb--lg</code>)."),
    anatomy=anatomy(
        f'<div style="width: 12rem;">{photo("bedale", stamp="Reserved")}</div>',
        [("20%", "14%"), ("50%", "48%"), ("16%", "86%"), ("88%", "50%")],
        [("Stamp (optional)", "<i>Reserved</i> on paper, <i>Sold</i> on ink; <code>--text-overline</code>, <code>--shadow-1</code>."),
         ("Image", "Centred at 78% width; <code>alt</code> names brand and item."),
         ("Size tag", f"{comp('size-tag')}, pinned bottom left."),
         ("Frame", "<code>aspect-ratio: 4 / 5</code>, backdrop <code>--color-photo-bg-N</code>, square corners, overflow hidden.")]),
    variants="<h3>Tones</h3>"
    + ex("".join(f'<div style="width: 7rem;">{photo(k)}</div>' for k in PHOTO_KEYS), "Six backdrops: sand, sage, blush, cool grey, cream, neutral. Order follows the listing, not the position.")
    + "<h3>Stamps and missing photo</h3>"
    + ex(f'<div style="width: 9rem;">{photo("bedale", stamp="Reserved")}</div><div style="width: 9rem;">{photo("detroit-jacket", stamp="Sold")}</div>'
         f'<div style="width: 9rem;"><div class="photo photo--none" role="img" aria-label="No photos yet">{ic("image", "icon icon--lg")}</div></div>',
         "Reserved (paper stamp) · Sold (ink stamp) · <code>.photo--none</code> for drafts without images."),
    sizes=p("The frame fills its container; the container decides the size.")
    + ex(f'<div class="thumb">{photo("arizona", tag=False, alt="")}</div><div class="thumb thumb--lg">{photo("arizona", tag=False, alt="")}</div>'
         f'<div style="width: 9rem;">{photo("arizona", "photo--square")}</div><div style="width: 9rem;">{photo("arizona")}</div>',
         "<code>.thumb</code> 56px · <code>.thumb--lg</code> 80px · <code>.photo--square</code> · default 4:5. Thumbs drop the size tag."),
    states=state_matrix(["Default", "Hover (in a card)", "Reserved", "Sold", "Loading", "No photo"], [
        ("Portrait", lambda s: {
            "default": f'<div style="width: 7rem;">{photo("organic-tee")}</div>',
            "hover (in a card)": f'<div style="width: 7rem;"><a class="listing-card" href="#" data-state="hover">{photo("organic-tee")}<span class="visually-hidden">Everlane organic cotton tee</span></a></div>',
            "reserved": f'<div style="width: 7rem;">{photo("bedale", stamp="Reserved")}</div>',
            "sold": f'<div style="width: 7rem;">{photo("detroit-jacket", stamp="Sold")}</div>',
            "loading": '<span class="skeleton skeleton--photo" style="width: 7rem;" aria-hidden="true"></span>',
            "no photo": f'<div style="width: 7rem;"><div class="photo photo--none" role="img" aria-label="No photos yet">{ic("image", "icon icon--lg")}</div></div>'}[s]),
    ], "Frame")
    + "<h3>Both themes</h3>" + themes(f'<div class="cluster"><div style="width: 7rem;">{photo("gamma-pants")}</div><div style="width: 7rem;">{photo("detroit-jacket", stamp="Sold")}</div></div>')
    + p("Backdrops do not darken in dark mode: the photo is content, not chrome."),
    responsive=ul("The frame is fluid; the aspect ratio holds at every width, so grids never jump while images load (<code>width</code>/<code>height</code> attributes are still set).",
                  "On listing detail below 640px the main photo bleeds to the screen edges; from 640px it sits inside the margins.",
                  "Images load lazily (<code>loading=\"lazy\"</code>) except the first row of the catalog and the gallery's main photo."),
    theming=p("Backdrops read <code>--color-photo-bg-1..6</code>, which alias <code>--palette-photo-1..6</code> in both themes. Stamps read <code>--color-stamp-bg</code>/<code>-fg</code> (paper/ink); <i>Sold</i> swaps them. To add a tone, add a primitive and a semantic token, then a <code>.photo--7</code> modifier."),
    accessibility=a11y(
        pattern="A <code>&lt;div class=\"photo\"&gt;</code> around a real <code>&lt;img&gt;</code>. The stamp and tag are text, so they are read in order after the image.",
        keyboard="Not focusable on its own; it is reached through its card, row or gallery button.",
        focus="The containing card or gallery button shows the ring around the frame.",
        labelling="<code>alt</code> names the item: <i>Nike Air Max 90, white</i>; gallery photos add the position: <i>Photo 2 of 5, Nike Air Max 90, white</i>. Thumbnails next to the item title use <code>alt=\"\"</code> so the name is not read twice. The no-photo frame is <code>role=\"img\"</code> with <i>No photos yet</i>.",
        contrast=[("Reserved stamp", "--color-stamp-fg", "--color-stamp-bg", 4.5), ("Sold stamp", "--color-stamp-bg", "--color-size-tag-bg", 4.5),
                  ("Size tag on backdrop", "--color-size-tag-bg", "--color-photo-bg-1", 3)],
        motion="In listing cards the image scales to 104% over <code>--duration-slow</code> on hover; reduced motion removes the transition.",
        touch="Not a target on its own."),
    content=ul("Alt text: brand, then the listing title as the seller wrote it. No <i>photo of</i>, no colours the title does not mention.",
               "Stamps are one word: <i>Reserved</i>, <i>Sold</i>. No other stamps (no <i>New</i>, no <i>Sale</i>).",
               "Never overlay prices or text on the photo; they go below in the card."),
    do_dont=dodont([
        ("do", f'<div style="width: 8rem;">{photo("bedale", stamp="Reserved")}</div>', "Stamp a reserved listing so buyers know it is not available yet."),
        ("dont", f'<div style="width: 8rem;">{photo("bedale")}</div><p class="text-sm" style="max-width: 10rem;">Reserved — check back later</p>', "Hide the reservation in text far from the image."),
        ("do", f'<div class="item-row"><div class="thumb">{photo("tech-shorts", tag=False, alt="")}</div><div class="item-row__body"><span class="item-row__title">Tech Fleece shorts</span><span class="item-row__meta">Nike · Men\'s L</span></div></div>', "Use an empty alt on a thumb beside its title."),
        ("dont", f'<div class="item-row"><div class="thumb">{photo("tech-shorts", tag=False, alt="Photo of Nike Tech Fleece shorts")}</div><div class="item-row__body"><span class="item-row__title">Tech Fleece shorts</span></div></div>', "Repeat the title in the thumb's alt; screen readers hear it twice."),
    ]),
    tokens=token_table([("Backdrop 1-6", "--color-photo-bg-1 / --color-photo-bg-2 / --color-photo-bg-3 / --color-photo-bg-4 / --color-photo-bg-5 / --color-photo-bg-6"),
                        ("Reserved stamp", "--color-stamp-bg / --color-stamp-fg"), ("Stamp shadow", "--shadow-1"), ("Stamp inset", "--space-3"),
                        ("No-photo background / icon", "--color-bg-subtle / --color-fg-subtle"), ("Hover zoom", "--duration-slow / --ease-standard")]),
    code=pre(f"""
<div class="photo photo--5">
  <img src="items/coat.svg" alt="Barbour Bedale waxed jacket" width="160" height="160" loading="lazy">
  <span class="photo__stamp">Reserved</span>
  <span class="size-tag" aria-label="Size L"><b>L</b></span>
</div>
<div class="thumb"><div class="photo photo--6"><img src="items/shorts.svg" alt=""></div></div>""")
    + classes([("<code>.photo</code>", "4:5 frame, backdrop tone 1 by default."), ("<code>.photo--1</code> … <code>.photo--6</code>", "Backdrop tone."),
               ("<code>.photo--square</code>", "1:1 frame."), ("<code>.photo--none</code>", "Missing photo: subtle background, centred icon."),
               ("<code>.photo__stamp</code>, <code>.photo__stamp--sold</code>", "Status stamp; Sold inverts it."), ("<code>.thumb</code>, <code>.thumb--lg</code>", "56px / 80px square wrapper."),
               ("<code>.skeleton--photo</code>", "Loading placeholder with the same 4:5 ratio.")]),
    sources=sources([("pages/catalog/default", "4:5 card photos in six tones"), ("pages/listing-detail/reserved", "Reserved stamp"),
                     ("pages/listing-detail/sold", "Sold stamp"), ("pages/my-listings/default", "thumbs and the no-photo draft"),
                     ("pages/catalog/loading", "photo skeletons")],
                    "<code>--photo-bg-*</code> renamed into the token tiers (see README drift log)."),
)


# ---------------------------------------------------------------------------
# Listing card
# ---------------------------------------------------------------------------
def _card(state: str) -> str:
    if state == "loading":
        return ('<div class="listing-card" aria-hidden="true" style="width: 9rem;"><span class="skeleton skeleton--photo"></span><div class="listing-card__meta">'
                '<span class="skeleton skeleton--text" style="width: 40%;"></span><span class="skeleton skeleton--text" style="width: 85%;"></span>'
                '<span class="skeleton skeleton--text" style="width: 55%;"></span></div></div>')
    key, stamp, attrs = {"default": ("air-max-90", None, ""), "hover": ("air-max-90", None, ' data-state="hover"'), "focus": ("air-max-90", None, ' data-state="focus"'),
                         "reserved": ("bedale", None, ""), "sold": ("detroit-jacket", "Sold", "")}[state]
    return f'<div style="width: 9rem;">{listing_card(key, stamp=stamp, attrs=attrs)}</div>'


component(
    "listing-card", "Listing card", G,
    lead="One item for sale in the catalog grid: photo with size tag, brand, title, condition and price. The whole card is one link to the listing.",
    pills=["<code>&lt;a class=\"listing-card\"&gt;</code>", "Grid 2/3/4 columns"],
    summary_variants="default, reserved, sold; in .listing-grid (2/3/4 columns) and in the catalog with filters (2/3/4)",
    summary_states="default, hover (photo zoom), focus, reserved, sold, loading skeleton",
    overview=p("The listing card is the catalog's unit: profile pages, <i>More in size 12</i> and search results all reuse it. It deliberately has no border, shadow or buttons: the photo carries the card, and the text below it answers the four questions a buyer scans for (brand, what it is, condition, price).")
    + ul("The whole card is a single <code>&lt;a&gt;</code>; nothing inside is separately clickable (no save heart, no seller link), so there is one tab stop per item.",
         f"Status is shown by the photo stamp ({comp('photo')}); price stays visible on reserved and sold items.",
         f"For lists of a member's own items (my listings, orders) use an {comp('list', 'item row')} instead; cards are for browsing."),
    anatomy=anatomy(
        '<div style="position: relative; width: 13rem;">' + listing_card("iron-ranger")
        + "".join(f'<span class="ds-callout" style="left: {l}; top: {t};" aria-hidden="true">{i}</span>' for i, (l, t) in enumerate(
            [("60%", "36%"), ("-16%", "77%"), ("-16%", "85%"), ("-16%", "93%"), ("104%", "93%")], 1)) + "</div>",
        [],
        [("Photo", f"{comp('photo')} 4:5 with the {comp('size-tag')}; zooms to 104% on hover."),
         ("Brand", "<code>.listing-card__brand</code>, overline, muted."),
         ("Title", "<code>.listing-card__title</code>, body, one line with ellipsis."),
         ("Condition", "<code>.listing-card__condition</code>, small, muted, truncates first."),
         ("Price", f"{comp('price')}, bold tabular, never truncates.")]),
    variants=ex(_card("default") + f'<div style="width: 9rem;">{listing_card("bedale")}</div>' + _card("sold"),
                "Available · reserved (stamp from the listing status) · sold.")
    + "<h3>In the grid</h3>"
    + ex('<ul class="listing-grid" role="list" style="width: 100%;">' + "".join(f"<li>{listing_card(k)}</li>" for k in ["air-max-90", "nb-990", "samba-og", "iron-ranger"]) + "</ul>",
         "<code>.listing-grid</code>: 2 columns on phones, 3 from 768px, 4 from 1024px; row gap larger than column gap so each card reads as a unit.", show_code=False),
    sizes=NA("The card has one size; the grid column sets its width."),
    states=state_matrix(["Default", "Hover", "Focus", "Reserved", "Sold", "Loading"], [("Card", _card)])
    + p("Active (pressed) is the browser's default for a link; the card does not shift. Disabled does not exist: an unavailable listing is removed from the grid, and a direct link shows the <i>unavailable</i> page.")
    + "<h3>Both themes</h3>" + themes(f'<div class="cluster" style="align-items: flex-start;">{_card("default")}{_card("sold")}</div>'),
    responsive=table(["Viewport", "Home and profile grid", "Catalog with filters", "Gaps (row / column)"], [
        ["&lt; 768px", "2 columns", "2 columns (filters in a sheet)", "<code>--space-8</code> / <code>--space-4</code>"],
        ["768–1023px", "3 columns", "3 columns", "<code>--space-10</code> / <code>--space-6</code>"],
        ["1024–1279px", "4 columns", "3 columns beside the 224px filters column", "same"],
        ["≥ 1280px", "4 columns", "4 columns", "same"]])
    + ul("Title and condition truncate with an ellipsis; brand and price never do. Long titles are still the link's full accessible name.",
         "On touch devices there is no hover zoom; nothing is hidden behind hover."),
    theming=p("The card has no surface of its own: text uses <code>--color-fg-default</code> and <code>--color-fg-muted</code> on the canvas, the photo keeps its light backdrop in both themes. Change the grid density with <code>.listing-grid</code> gap tokens, not by adding borders to cards."),
    accessibility=a11y(
        pattern="One <code>&lt;a href&gt;</code> wrapping the photo and text, inside <code>&lt;li&gt;</code> in a <code>&lt;ul class=\"listing-grid\" role=\"list\"&gt;</code> (the role restores list semantics that <code>list-style: none</code> removes in Safari).",
        keyboard=[(kbd("Tab"), "Moves card to card in reading order (left to right, row by row)."), (kbd("Enter"), "Opens the listing.")],
        focus="The ring is offset by <code>--space-1</code> so it clears the photo edge and wraps photo and text together.",
        labelling="The link's name is its text in order: <i>Size US 12, Nike, Air Max 90, white, Used - Excellent, $85</i>. The photo's alt adds brand and title; keep it, because the card may be the only place the image is described. Stamps are read as text (<i>Reserved</i>).",
        contrast=[("Title on canvas", "--color-fg-default", "--color-bg-canvas", 4.5), ("Brand and condition on canvas", "--color-fg-muted", "--color-bg-canvas", 4.5),
                  ("Focus ring on canvas", "--color-focus-ring", "--color-bg-canvas", 3)],
        motion="Photo zoom over <code>--duration-slow</code>; removed under reduced motion. Skeleton shimmer stops under reduced motion.",
        touch="Each card is far larger than 44px; the 16px column gap on phones prevents mis-taps."),
    content=ul("Brand as the seller entered it (<i>New Balance</i>, <i>Arc'teryx</i>).", "Title without the brand or the size: <i>990v6, grey</i>, not <i>New Balance 990v6 size 12</i>.",
               "Condition from the fixed list: <i>New with tags</i>, <i>New without tags</i>, <i>Used - Excellent</i>, <i>Used - Good</i>, <i>Used - Fair</i>.",
               "Price in whole dollars when there are no cents (<i>$85</i>); shipping is shown on the listing, not the card."),
    do_dont=dodont([
        ("do", f'<div style="width: 10rem;">{listing_card("bedale")}</div>', "Keep the price on a reserved listing; the stamp says why it cannot be bought."),
        ("dont", '<div style="width: 10rem;"><a class="listing-card" href="#">' + photo("bedale") + '<div class="listing-card__meta"><span class="listing-card__title">Bedale waxed jacket</span>'
                 '<span class="btn btn--primary btn--sm">Buy now</span></div></a></div>', "Put a button inside the card link; it nests interactive elements and adds a second tab stop."),
        ("do", f'<div style="width: 10rem;">{listing_card("nb-990")}</div>', "Title without the brand or size."),
        ("dont", '<div style="width: 10rem;"><a class="listing-card" href="#">' + photo("nb-990") + '<div class="listing-card__meta"><span class="listing-card__brand">New Balance</span>'
                 '<span class="listing-card__title">New Balance 990v6 grey size 12 mens</span></div></a></div>', "Repeat the brand and size in the title; it truncates before the useful part."),
    ]),
    tokens=token_table([("Title", "--color-fg-default"), ("Brand / condition", "--color-fg-muted"), ("Brand font", "--text-overline"),
                        ("Meta gap / photo to meta", "--space-0-5 / --space-3"), ("Grid gaps (phone)", "--space-8 / --space-4"),
                        ("Grid gaps (tablet+)", "--space-10 / --space-6"), ("Focus offset", "--space-1"), ("Zoom", "--duration-slow / --ease-standard")]),
    code=pre("""
<ul class="listing-grid" role="list">
  <li>
    <a class="listing-card" href="/items/L-20931">
      <div class="photo photo--6">
        <img src="items/sneaker-white.svg" alt="Nike Air Max 90, white" width="160" height="160" loading="lazy">
        <span class="size-tag" aria-label="Size US 12">US <b>12</b></span>
      </div>
      <div class="listing-card__meta">
        <span class="listing-card__brand">Nike</span>
        <span class="listing-card__title">Air Max 90, white</span>
        <span class="listing-card__foot">
          <span class="listing-card__condition">Used - Excellent</span>
          <span class="price">$85</span>
        </span>
      </div>
    </a>
  </li>
</ul>""")
    + classes([("<code>.listing-grid</code>", "Responsive grid, 2/3/4 columns; inside <code>.catalog-layout</code> 2/3/3/4."),
               ("<code>.listing-card</code>", "The link; column flex with photo and meta."),
               ("<code>__meta</code> <code>__brand</code> <code>__title</code> <code>__foot</code> <code>__condition</code>", "Text parts."),
               ("<code>.skeleton--photo</code> + <code>.skeleton--text</code>", "Loading card; the grid gets <code>aria-busy=\"true\"</code>.")]),
    sources=sources([("pages/catalog/default", "grid of 24 cards"), ("pages/catalog/filtered", "grid beside filters"), ("pages/catalog/loading", "skeleton cards"),
                     ("pages/profile/default", "seller's listings"), ("pages/listing-detail/default", "More in size 12")],
                    "the catalog grid's 62rem and 75rem breakpoints snapped to the system's 64rem (lg) and 80rem (xl)."),
)


# ---------------------------------------------------------------------------
# Price
# ---------------------------------------------------------------------------
component(
    "price", "Price", G,
    lead="Money, set in bold tabular figures. Whole dollars in the catalog, cents everywhere a member pays or gets paid.",
    pills=["<code>.price</code>", "Tabular numbers"],
    summary_variants="default (cards, rows), large (listing detail), muted (secondary amounts)",
    summary_states="static; with shipping line, free shipping, loading",
    overview=p("<code>.price</code> styles an amount; the formatting rules below decide the string. Prices are always US dollars (12L ships within the US only).")
    + ul("<b>Catalog</b> (cards, search): whole dollars when there are no cents, <i>$85</i>.",
         "<b>Listing detail</b>: <i>$85.00</i> large, then a muted line <i>$9.00 shipping · $94.00 total before tax</i>.",
         f"<b>Checkout, orders, payouts</b>: always cents, in an {comp('order-summary')}. Fees are shown as negative amounts with a true minus: <i>−$3.70</i>."),
    anatomy=anatomy(
        '<div class="detail__price"><span class="price price--lg">$85.00</span><span class="text-muted text-sm">$9.00 shipping · <span class="num">$94.00</span> total before tax</span></div>',
        [("6%", "18%"), ("40%", "72%")],
        [("Amount", "<code>.price--lg</code>: <code>--text-h2</code>, tight tracking, tabular figures."),
         ("Shipping line", "Small muted text; the total uses <code>.num</code> so digits align.")]),
    variants=ex('<span class="price">$85</span><span class="price price--lg">$85.00</span><span class="price price--muted">$9.00 shipping</span>',
                "Default · large · muted."),
    sizes=p("Default inherits the surrounding size (body in cards, label in rows); large is <code>--text-h2</code> on the listing page and the buy bar's total stays default.")
    + ex('<span class="price">$210</span><span class="price" style="font-size: var(--font-size-lg);">$210.00</span><span class="price price--lg">$210.00</span>', "In a card · in a row · on detail."),
    states=matrix(["Default", "Free shipping", "Loading"], [
        ("Card", ['<span class="price">$150</span>', '<span class="price">$150</span>', '<span class="skeleton skeleton--text" style="width: 3rem;" aria-hidden="true"></span>']),
        ("Detail", ['<div class="detail__price"><span class="price price--lg">$150.00</span><span class="text-muted text-sm">$9.00 shipping · <span class="num">$159.00</span> total before tax</span></div>',
                    '<div class="detail__price"><span class="price price--lg">$150.00</span><span class="text-muted text-sm">Free shipping · <span class="num">$150.00</span> total before tax</span></div>',
                    '<span class="skeleton skeleton--title" style="width: 8rem;" aria-hidden="true"></span>']),
    ], "Context")
    + p("Prices are not interactive, so hover, focus and disabled do not apply. There is no strikethrough or sale state: 12L has no discounts, only offers.")
    + "<h3>Both themes</h3>" + themes('<div class="cluster"><span class="price">$85</span><span class="price price--lg">$85.00</span><span class="price price--muted">Free</span></div>'),
    responsive=ul("The large price does not shrink on phones; it is the second thing a buyer reads after the title.",
                  "Below 1024px the total (item + shipping) repeats in the sticky " + comp("buy-bar") + "; it hides when the bar holds two buttons.",
                  "Prices never wrap: <code>white-space: nowrap</code>. A row that cannot fit truncates the title first."),
    theming=p("Weight and figures, not colour, make a price: <code>--font-weight-bold</code>, <code>font-variant-numeric: tabular-nums</code>, <code>--color-fg-default</code>. Muted amounts use <code>--color-fg-muted</code> and regular weight. Never colour a price green or red; payouts and refunds say what they are in words."),
    accessibility=a11y(
        pattern="Plain text in a <code>&lt;span&gt;</code>. Screen readers read <i>$85.00</i> correctly; do not split the amount across elements.",
        keyboard="Not focusable.",
        focus="Not applicable.",
        labelling="The words around the price carry its meaning: <i>shipping</i>, <i>total before tax</i>, <i>Your payout</i>. A minus fee uses the Unicode minus (−), which screen readers read as <i>minus</i>.",
        contrast=[("Price on canvas", "--color-fg-default", "--color-bg-canvas", 4.5), ("Muted amount on canvas", "--color-fg-muted", "--color-bg-canvas", 4.5),
                  ("Muted amount in a sunken panel", "--color-fg-muted", "--color-bg-surface-sunken", 4.5)],
        motion="None.",
        touch="Not a target."),
    content=ul("<i>$1,240</i> with a thousands separator; <i>$85</i> not <i>$85.00</i> in the catalog; <i>$85.00</i> on detail and everywhere money moves.",
               "<i>Free shipping</i> in words, never <i>$0.00 shipping</i>; in a totals row write <i>Free</i>.",
               "<i>total before tax</i> on detail; tax appears only at checkout once the address is known.",
               "Fees: <i>12L fee (10%)</i> then <i>−$3.70</i>; payouts: <i>Your payout</i> <i>$33.30</i>."),
    do_dont=dodont([
        ("do", '<span class="text-muted text-sm">Free shipping · <span class="num">$150.00</span> total before tax</span>', "Say <i>Free shipping</i> in words."),
        ("dont", '<span class="text-muted text-sm">$0.00 shipping · $150.00 total</span>', "Show a zero amount; it reads like an error."),
        ("do", '<span class="price">$48</span>', "Ink, bold, tabular."),
        ("dont", '<span class="price" style="color: var(--color-success-fg);">$48</span>', "Colour prices to signal a deal."),
    ]),
    tokens=token_table([("Amount", "--color-fg-default"), ("Muted amount", "--color-fg-muted"), ("Weight", "--font-weight-bold"),
                        ("Large", "--text-h2 / --letter-spacing-tight"), ("Amount to shipping line", "--space-1")]),
    code=pre("""
<span class="price">$85</span>
<div class="detail__price">
  <span class="price price--lg">$85.00</span>
  <span class="text-muted text-sm">$9.00 shipping · <span class="num">$94.00</span> total before tax</span>
</div>""")
    + classes([("<code>.price</code>", "Bold, tabular, no wrap."), ("<code>.price--lg</code>", "Detail-page size."), ("<code>.price--muted</code>", "Secondary amount, regular weight."),
               ("<code>.num</code>", "Tabular figures for amounts inside running text.")]),
    sources=sources([("pages/catalog/default", "whole-dollar card prices"), ("pages/listing-detail/default", "large price and shipping line"),
                     ("pages/listing-detail/new-seller", "free shipping"), ("pages/sale-detail/completed", "fee and payout")]),
)


# ---------------------------------------------------------------------------
# Rating
# ---------------------------------------------------------------------------
component(
    "rating", "Rating", G,
    lead="Seller reputation as five stars, the average and the review count; and the star input buyers use to leave a review.",
    pills=["<code>.rating</code>", "<code>.star-input</code>"],
    summary_variants="summary (stars, value, count), compact (count only), no reviews yet, new seller; star input",
    summary_states="display: rated, none; input: empty, hover, focus, selected, invalid",
    overview=p("Two parts that share the star. <b>Rating</b> summarises a member's reviews wherever they are named as a seller (listing detail, profile, reviews). <b>Star input</b> collects one rating from 1 to 5 in the <i>Leave a review</i> dialog.")
    + ul("Stars are ink, not gold: the system's only accent is the red L, and ink stars match the type.",
         "Zero reviews is a real state: <i>No reviews yet</i> in muted text, never five empty stars.",
         f"A seller with no completed sales shows a <i>New seller</i> {comp('badge')} instead of a rating."),
    anatomy=anatomy(
        rating(4.9, 128),
        [("16%", "14%"), ("58%", "14%"), ("82%", "14%")],
        [("Stars", "Five 14px stars, filled to the rounded average; off stars use <code>--color-border-strong</code>."),
         ("Average", "One decimal, bold."),
         ("Count", "Muted, in brackets, with the noun: <i>(128 reviews)</i>.")]),
    variants=ex(rating(4.9, 128) + rating(4.3, 3) + rating(5.0, 1) + rating(None, 0) + '<span class="badge">New seller</span>',
                "Rated · few reviews · one review · no reviews yet · new seller (no sales).")
    + "<h3>Star input</h3>"
    + ex(star_input("stars-variant", 4), "Five radio buttons in a fieldset; the selected value is echoed as a word (<i>Great</i>).", show_code=False),
    sizes=p("The summary inherits <code>--text-body-sm</code>; stars are 0.9rem. The star input uses 28px stars inside 44px targets.")
    + ex(rating(4.8, 23) + '<span style="font-size: var(--font-size-md);">' + rating(4.8, 23) + "</span>", "Small (default) · inside body text."),
    states=matrix(["Empty", "Hover", "Focus", "Selected", "Invalid"], [
        ("Star input", [star_input("st-empty"), star_input("st-hover", 3).replace('class="star-input"', 'class="star-input" data-state="hover"'),
                        star_input("st-focus", 0, focus=1), star_input("st-sel", 5), star_input("st-inv", 0, err=True)]),
    ], "Part")
    + matrix(["Rated", "No reviews", "New seller"], [("Summary", [rating(4.7, 41), rating(None, 0), '<span class="badge">New seller</span>'])], "Part")
    + p("Hover previews by filling stars up to the pointer (implemented in script; shown here as the selected fill). The display rating is not interactive.")
    + "<h3>Both themes</h3>" + themes(f'<div class="stack stack--sm">{rating(4.9, 128)}{rating(None, 0)}</div>'),
    responsive=ul("The summary never wraps (<code>white-space: nowrap</code>); in a narrow seller block it moves to its own line under the city.",
                  "Star-input targets stay 44px at every width; on a 320px screen five stars plus the word fit in one row."),
    theming=p("Filled stars use <code>--color-fg-default</code> (ink, or paper in dark); off stars use <code>--color-border-strong</code>. The star input's selected fill reads <code>--color-fg-default</code> too, so it inverts with the theme."),
    accessibility=a11y(
        pattern="Display: <code>role=\"img\"</code> with <code>aria-label=\"Rated 4.9 out of 5 from 128 reviews\"</code>; the stars inside are <code>aria-hidden</code>. Input: native radio group in a <code>&lt;fieldset&gt;</code> with <code>&lt;legend&gt;Rating&lt;/legend&gt;</code>; each visually hidden label says <i>4 stars, Great</i>.",
        keyboard=[(kbd("Tab"), "Enters the star group (the checked star, or the first)."), (kbd("←") + " " + kbd("→"), "Moves the selection one star."), (kbd("Space"), "Selects the focused star.")],
        focus="The focused star's icon gets the shared ring (the input itself is visually hidden).",
        labelling="Each star's label names its number and word. The error <i>Choose a rating from 1 to 5 stars</i> is linked with <code>aria-describedby</code> on the fieldset.",
        contrast=[("Filled star on canvas", "--color-fg-default", "--color-bg-canvas", 3), ("Off star on canvas", "--color-border-strong", "--color-bg-canvas", 3),
                  ("Off star in a dialog", "--color-border-strong", "--color-bg-surface", 3), ("Count text", "--color-fg-muted", "--color-bg-canvas", 4.5)],
        motion="None.",
        touch="Star-input labels are 44 × 44px with no gap overlap."),
    content=ul("<i>4.9 (128 reviews)</i>; <i>5.0 (1 review)</i>; <i>No reviews yet</i>. One decimal always.",
               "Star words, low to high: <i>Poor</i>, <i>Fair</i>, <i>Good</i>, <i>Great</i>, <i>Excellent</i>.",
               "Never round a 4.96 to 5.0 stars of fill and 4.9 in text; both use the same rounding."),
    do_dont=dodont([
        ("do", rating(None, 0), "Say <i>No reviews yet</i>."),
        ("dont", '<span class="rating" role="img" aria-label="Rated 0 out of 5"><span class="rating__stars">' + stars(0) + '</span><span class="rating__value">0.0</span></span>', "Show 0.0 and five empty stars; it reads as a terrible seller."),
        ("do", star_input("dd-ok", 4), "Echo the chosen value as a word."),
        ("dont", '<fieldset><legend>Rating</legend><div class="star-input">' + "".join(f'<label><input type="radio" name="dd-bad">{ic("star")}</label>' for _ in range(5)) + "</div></fieldset>", "Stars with no text labels; a screen reader hears <i>radio button</i> five times."),
    ]),
    tokens=token_table([("Filled star", "--color-fg-default"), ("Off star", "--color-border-strong"), ("Count", "--color-fg-muted"), ("Value weight", "--font-weight-bold"),
                        ("Input target", "--target-comfortable"), ("Focus ring", "--color-focus-ring")]),
    code=pre("""
<span class="rating" role="img" aria-label="Rated 4.9 out of 5 from 128 reviews">
  <span class="rating__stars"><svg class="icon">…</svg>…<svg class="icon icon--off">…</svg></span>
  <span class="rating__value">4.9</span><span class="text-muted">(128 reviews)</span>
</span>

<fieldset><legend>Rating</legend>
  <div class="star-input">
    <label class="is-on"><input type="radio" name="stars" value="1"><svg class="icon">…</svg>
      <span class="visually-hidden">1 star, Poor</span></label>
    …
  </div>
</fieldset>""")
    + classes([("<code>.rating</code>", "Summary row."), ("<code>.rating__stars</code>, <code>.icon--off</code>", "Star strip; off stars."), ("<code>.rating__value</code>", "Bold average."),
               ("<code>.star-input</code>", "Radio-based star picker."), ("<code>.is-on</code>", "Filled star (set by script up to the selection or hover)."),
               ("<code>aria-invalid</code> on the radios", "Invalid state; pair with <code>.field__error</code>.")]),
    sources=sources([("pages/listing-detail/default", "seller rating"), ("pages/listing-detail/new-seller", "New seller badge"),
                     ("pages/profile/default", "rating in the profile header and reviews"), ("dialogs/leave-review/default", "star input"),
                     ("dialogs/leave-review/invalid", "star input error")]),
)


# ---------------------------------------------------------------------------
# Gallery
# ---------------------------------------------------------------------------
component(
    "gallery", "Gallery", G,
    lead="The listing's photos: one large 4:5 image, a strip of square thumbnails to switch it, and position dots on phones.",
    pills=["<code>.gallery</code>", "Up to 6 photos shown"],
    summary_variants="with thumbnails (all widths), with dots (below 1024px), single photo",
    summary_states="thumb default, hover, focus, current; loading",
    overview=p("The gallery leads the listing detail page. Sellers upload up to 8 photos (the uploader, see " + comp("file-upload") + "); the strip shows the first six. Photos are the buyer's main evidence of condition, so the main image is as large as the column allows and never cropped.")
    + ul("Selecting a thumbnail swaps the main image; it does not open a lightbox.", "On phones the main image swipes horizontally; dots show the position.",
         "A listing with one photo shows the main image only, no strip and no dots."),
    anatomy=anatomy(
        '<div style="position: relative; width: 16rem;">' + gallery("iron-ranger", n=4)
        + "".join(f'<span class="ds-callout" style="left: {l}; top: {t};" aria-hidden="true">{i}</span>' for i, (l, t) in enumerate(
            [("62%", "34%"), ("104%", "78%"), ("-14%", "90%")], 1)) + "</div>",
        [],
        [("Main photo", "<code>.gallery__main</code>: 4:5 <code>.photo</code>, image at 72% width, alt names the position."),
         ("Dots", "<code>.gallery__dots</code>: position indicator, phones only, <code>aria-hidden</code>."),
         ("Thumbnails", "<code>.gallery__thumbs</code>: 64px square buttons; the current one has a 2px ink outline.")]),
    variants=ex(f'<div style="width: 18rem;">{gallery("park-avenue", n=6)}</div><div style="width: 12rem;"><section class="gallery" aria-label="Photos"><div class="gallery__main">{photo("oxford-shirt", tag=False)}</div></section></div>',
                "Six photos with thumbnails · one photo (no strip).", show_code=False),
    sizes=NA("The gallery fills its column; there is one size."),
    states=matrix(["Default", "Hover", "Focus", "Current"], [
        ("Thumbnail", [
            f'<div style="width: 4rem;"><ul class="gallery__thumbs" role="list"><li><button type="button" aria-label="Show photo 2 of 5"><div class="photo photo--2"><img src="{MOCK_ASSETS}items/boot.svg" alt="" width="160" height="160"></div></button></li></ul></div>',
            f'<div style="width: 4rem;"><ul class="gallery__thumbs" role="list"><li><button type="button" aria-label="Show photo 2 of 5" data-state="hover" style="opacity: 0.85;"><div class="photo photo--2"><img src="{MOCK_ASSETS}items/boot.svg" alt="" width="160" height="160"></div></button></li></ul></div>',
            f'<div style="width: 4rem;"><ul class="gallery__thumbs" role="list"><li><button type="button" aria-label="Show photo 2 of 5" data-state="focus"><div class="photo photo--2"><img src="{MOCK_ASSETS}items/boot.svg" alt="" width="160" height="160"></div></button></li></ul></div>',
            f'<div style="width: 4rem;"><ul class="gallery__thumbs" role="list"><li><button type="button" aria-label="Show photo 2 of 5" aria-current="true"><div class="photo photo--2"><img src="{MOCK_ASSETS}items/boot.svg" alt="" width="160" height="160"></div></button></li></ul></div>']),
    ], "Part")
    + "<h3>Loading</h3>" + ex('<div style="width: 12rem;"><section class="gallery" aria-busy="true" aria-label="Loading photos"><span class="skeleton skeleton--photo"></span></section></div>', "One photo-shaped skeleton until the first image is ready.")
    + "<h3>Both themes</h3>" + themes(f'<div style="max-width: 14rem;">{gallery("samba-og", n=4, current=2)}</div>'),
    responsive=table(["Viewport", "Layout"], [
        ["&lt; 640px", "Main photo bleeds to the screen edges; thumbnails scroll horizontally inside the margins; dots under the photo."],
        ["640–1023px", "Main photo inside the margins; thumbnails and dots."],
        ["≥ 1024px", "Left column of the two-column detail (7 of 12 columns); dots hidden; thumbnails stay."]]),
    theming=p("Backdrops stay light in both themes (see " + comp("photo") + "). Dots use <code>--color-border-strong</code> and the current dot <code>--color-fg-default</code>, widened to 20px so position is shown by shape as well as colour. The current thumbnail outline is <code>--color-fg-default</code>."),
    accessibility=a11y(
        pattern="A <code>&lt;section aria-label=\"Photos\"&gt;</code>. Thumbnails are buttons in a list; the current one has <code>aria-current=\"true\"</code>. Dots are decorative (<code>aria-hidden</code>) because the thumbnails already expose the position.",
        keyboard=[(kbd("Tab"), "Moves through the thumbnail buttons."), (kbd("Enter") + " / " + kbd("Space"), "Shows that photo in the main frame; focus stays on the thumbnail.")],
        focus="Shared ring with 2px offset around the thumbnail; distinct from the 2px current outline because the ring sits outside it.",
        labelling="Thumbnail buttons: <i>Show photo 2 of 5</i>. Main photo alt: <i>Photo 2 of 5, Red Wing Iron Ranger 8111 boots</i>. Thumbnail images have empty alt (the button names them).",
        contrast=[("Current thumbnail outline", "--color-fg-default", "--color-bg-canvas", 3), ("Dot on canvas", "--color-border-strong", "--color-bg-canvas", 3),
                  ("Focus ring", "--color-focus-ring", "--color-bg-canvas", 3)],
        motion="Swipe follows the finger; the main image swaps without a cross-fade so nothing animates under reduced motion.",
        touch="Thumbnails are 64px square with 8px gaps."),
    content=ul("Photo alt text counts from 1 and includes the total.", "Sellers order photos; the first is the cover and also the card photo.",
               "No captions: condition notes belong in the description and the flaws note."),
    do_dont=dodont([
        ("do", f'<div style="width: 14rem;">{gallery("arizona", n=3)}</div>', "Mark the current thumbnail with <code>aria-current</code> and an outline."),
        ("dont", f'<div style="width: 14rem;"><section class="gallery" aria-label="Photos"><div class="gallery__main">{photo("arizona", tag=False)}</div><div class="gallery__dots" aria-hidden="true" style="display: flex;"><span aria-current="true"></span><span></span><span></span></div></section></div>',
         "Dots alone on desktop; they are too small to click and invisible to screen readers."),
    ]),
    tokens=token_table([("Current thumbnail outline", "--color-fg-default"), ("Dot / current dot", "--color-border-strong / --color-fg-default"), ("Gaps", "--space-2 / --space-3"),
                        ("Phone bleed", "--layout-margin"), ("Focus ring", "--color-focus-ring")]),
    code=pre("""
<section class="gallery" aria-label="Photos">
  <div class="gallery__main"><div class="photo photo--1"><img src="items/boot.svg" alt="Photo 1 of 6, Red Wing Iron Ranger 8111 boots"></div></div>
  <div class="gallery__dots" aria-hidden="true"><span aria-current="true"></span><span></span>…</div>
  <ul class="gallery__thumbs" role="list">
    <li><button type="button" aria-label="Show photo 1 of 6" aria-current="true"><div class="photo photo--1"><img src="items/boot.svg" alt=""></div></button></li>
    …
  </ul>
</section>""")
    + classes([("<code>.gallery</code>", "Column with main, dots and thumbs; bleeds on phones."), ("<code>.gallery__main</code>", "Main 4:5 photo."),
               ("<code>.gallery__thumbs</code>", "Horizontal strip of 64px buttons."), ("<code>.gallery__dots</code>", "Phone position dots (hidden from 1024px)."),
               ("<code>aria-current=\"true\"</code>", "Current thumbnail and dot.")]),
    sources=sources([("pages/listing-detail/default", "gallery with thumbs"), ("pages/listing-detail/loading", "photo skeleton"), ("pages/listing-detail/sold", "gallery on a sold listing")],
                    "the gallery's 36rem bleed and 62rem dots breakpoints snapped to 40rem (sm) and 64rem (lg)."),
)


# ---------------------------------------------------------------------------
# Order summary
# ---------------------------------------------------------------------------
CHECKOUT = totals([("Item", "$85.00"), ("Shipping", "$9.00"), ("Sales tax", "$8.34")], ("Total", "$102.34"))
PAYOUT = totals([("Item and shipping", "$37.00"), ("12L fee (10%)", "−$3.70")], ("Your payout", "$33.30"))


def _summary(body: str, title: str = "Summary", sid: str = "sum") -> str:
    return (f'<aside class="panel stack stack--lg" aria-labelledby="{sid}" style="width: 100%; max-width: 24rem;"><h2 id="{sid}" class="panel__title">{title}</h2>'
            f'{item_row("air-max-90")}{body}</aside>')


component(
    "order-summary", "Order summary", G,
    lead="What is being bought or paid out, and the arithmetic: an item row, then label–amount rows ending in a ruled total.",
    pills=["<code>&lt;dl class=\"totals\"&gt;</code>", "<code>.item-row</code>"],
    summary_variants="checkout summary, order detail summary, seller payout (with 10% fee)",
    summary_states="default, free shipping, loading, payout held",
    overview=p("The order summary appears in the checkout's right column, on order and sale detail, and as the payout panel. It is built from two parts: an <b>item row</b> (thumb, title, brand and size) and a <b>totals</b> description list.")
    + ul("Buyers see <i>Item</i>, <i>Shipping</i>, <i>Sales tax</i>, <i>Total</i>.",
         "Sellers see <i>Item and shipping</i>, <i>12L fee (10%)</i> as a negative amount, <i>Your payout</i>.",
         "Every amount has cents; the total row is bold with a rule above it."),
    anatomy=anatomy(
        _summary(CHECKOUT, sid="sum-anatomy"),
        [("8%", "10%"), ("8%", "30%"), ("8%", "58%"), ("8%", "86%")],
        [("Title", "<code>.panel__title</code>: <i>Summary</i> or <i>Payout</i>; labels the <code>&lt;aside&gt;</code>."),
         ("Item row", f"{comp('photo')} thumb + title (one line, ellipsis) + brand, size and condition."),
         ("Lines", "<code>&lt;div&gt;&lt;dt&gt;&lt;dd&gt;</code> pairs; labels muted, amounts tabular."),
         ("Total", "<code>.totals__total</code>: rule above, bold, label in the default colour.")]),
    variants=ex(_summary(CHECKOUT, sid="sum-v1") + f'<div class="panel panel--sunken stack" style="width: 100%; max-width: 24rem;"><h2 class="panel__title">Payout</h2>{PAYOUT}<p class="text-caption">Sent Wed 7 Oct to Chase ending 6610.</p></div>',
                "Checkout summary (panel) · seller payout (sunken panel).", show_code=False),
    sizes=NA("One size; the panel takes the width of its column."),
    states=matrix(["Default", "Free shipping", "Loading", "Payout held"], [
        ("Summary", [
            f'<div style="width: 15rem;">{CHECKOUT}</div>',
            '<div style="width: 15rem;">' + totals([("Item", "$150.00"), ("Shipping", "Free"), ("Sales tax", "$13.31")], ("Total", "$163.31")) + "</div>",
            '<div class="stack stack--sm" style="width: 15rem;" aria-hidden="true"><span class="skeleton skeleton--text"></span><span class="skeleton skeleton--text"></span><span class="skeleton skeleton--text" style="width: 60%;"></span></div>',
            '<div class="stack stack--sm" style="width: 15rem;">' + totals([("Item and shipping", "$45.00"), ("12L fee (10%)", "−$4.50")], ("Your payout", "$40.50")) + '<span class="status status--reserved">Held: problem open</span></div>']),
    ], "Part")
    + "<h3>Both themes</h3>" + themes(f'<div style="max-width: 18rem;">{PAYOUT}</div>'),
    responsive=ul("On checkout below 1024px the summary stacks <i>above</i> the payment step so the total is seen before the card form; from 1024px it is the right column (2 of 5).",
                  "Labels and amounts stay on one line; long item titles truncate in the item row, never the amounts.",
                  "Panel padding grows from <code>--space-6</code> to <code>--space-8</code> at 768px."),
    theming=p("Panels use <code>--color-bg-surface</code> (summary) or <code>--color-bg-surface-sunken</code> (payout); labels <code>--color-fg-muted</code>; the total and amounts <code>--color-fg-default</code>; the rule <code>--color-border-default</code>."),
    accessibility=a11y(
        pattern="<code>&lt;aside aria-labelledby&gt;</code> containing a <code>&lt;dl&gt;</code>. Each row wraps one <code>&lt;dt&gt;</code>/<code>&lt;dd&gt;</code> pair in a <code>&lt;div&gt;</code> (valid HTML) so label and amount are read together.",
        keyboard="Not interactive. The item title may be a link to the listing.",
        focus="Not applicable.",
        labelling="Row labels say what the amount is (<i>Sales tax</i>, <i>12L fee (10%)</i>). The negative fee uses the Unicode minus so it is read as <i>minus 3 dollars 70</i>.",
        contrast=[("Label in panel", "--color-fg-muted", "--color-bg-surface", 4.5), ("Label in sunken panel", "--color-fg-muted", "--color-bg-surface-sunken", 4.5),
                  ("Amounts", "--color-fg-default", "--color-bg-surface", 4.5)],
        motion="None.",
        touch="Not a target."),
    content=ul("Buyer rows: <i>Item</i>, <i>Shipping</i>, <i>Sales tax</i>, <i>Total</i>. Seller rows: <i>Item and shipping</i>, <i>12L fee (10%)</i>, <i>Your payout</i>.",
               "The fee always states the rate in brackets and is 10% of item plus shipping, rounded to the cent.",
               "Item meta: <i>Nike · Men's US 12 · Used - Excellent</i>.",
               "Under a payout, say where and when it went: <i>Sent Wed 7 Oct to Chase ending 6610.</i>"),
    do_dont=dodont([
        ("do", f'<div style="width: 15rem;">{PAYOUT}</div>', "Show the fee as its own negative line with the rate."),
        ("dont", '<div style="width: 15rem;">' + totals([("Item and shipping", "$37.00")], ("Payout", "$33.30")) + "</div>", "Net the fee silently; the seller cannot see where $3.70 went."),
        ("do", f'<div style="width: 15rem;">{CHECKOUT}</div>', "End with one ruled total."),
        ("dont", '<div style="width: 15rem;">' + totals([("Item", "$85"), ("Shipping", "$9"), ("Tax", "8.34")], ("Total", "$102.34")) + "</div>", "Mix whole dollars, cents and missing currency signs."),
    ]),
    tokens=token_table([("Panel / sunken panel", "--color-bg-surface / --color-bg-surface-sunken"), ("Labels", "--color-fg-muted"), ("Amounts and total", "--color-fg-default"),
                        ("Total rule", "--color-border-default"), ("Row gap", "--space-3"), ("Total padding", "--space-4"), ("Panel padding", "--space-6 / --space-8")]),
    code=pre("""
<aside class="panel stack stack--lg" aria-labelledby="sum-title">
  <h2 id="sum-title" class="panel__title">Summary</h2>
  <div class="item-row">
    <div class="thumb"><div class="photo photo--6"><img src="items/sneaker-white.svg" alt=""></div></div>
    <div class="item-row__body"><span class="item-row__title">Air Max 90, white</span>
      <span class="item-row__meta">Nike · Men's US 12 · Used - Excellent</span></div>
  </div>
  <dl class="totals">
    <div><dt>Item</dt><dd>$85.00</dd></div>
    <div><dt>Shipping</dt><dd>$9.00</dd></div>
    <div><dt>Sales tax</dt><dd>$8.34</dd></div>
    <div class="totals__total"><dt>Total</dt><dd>$102.34</dd></div>
  </dl>
</aside>""")
    + classes([("<code>.totals</code>", "Description list of amount rows."), ("<code>.totals__total</code>", "Ruled, bold final row."),
               ("<code>.item-row</code>, <code>__body</code>, <code>__title</code>, <code>__meta</code>", "Thumb + title + meta row."),
               ("<code>.panel</code>, <code>.panel--sunken</code>, <code>.panel__title</code>", "Container and its heading.")]),
    sources=sources([("pages/checkout/default", "checkout summary, $102.34 total"), ("pages/order-detail/default", "order summary"),
                     ("pages/sale-detail/completed", "payout with the 10% fee"), ("pages/checkout/loading", "summary skeleton")]),
)


# ---------------------------------------------------------------------------
# Review
# ---------------------------------------------------------------------------
component(
    "review", "Review", G,
    lead="A buyer's rating and words about a seller, with at most one public reply. The same quote and thread parts carry problem reports and cancellation requests.",
    pills=["<code>&lt;article class=\"review\"&gt;</code>", "<code>.quote</code>", "<code>.thread</code>"],
    summary_variants="review, review with reply, own review with Reply link; quote; thread",
    summary_states="default, with reply, reply available, loading, empty (no reviews yet)",
    overview=p("Reviews build trust in a peer marketplace, so they are plain and attributable: who, how many stars, when, what they said. Sellers can reply once, publicly. Two smaller parts share the look:")
    + ul("<b>Quote</b> (<code>.quote</code>): one member's words shown inside a dialog or order page, with <code>&lt;cite&gt;</code> naming them (a cancellation reason, a problem description).",
         "<b>Thread</b> (<code>.thread</code>): a short exchange between buyer and seller on a problem, oldest first, in sunken blocks."),
    anatomy=anatomy(
        f'<div style="width: 22rem;">{review("tall_tom", "TR", 5, "Mon 5 Oct", "Shorts were spotless. Fast shipping.", "Thanks Tom, enjoy them.")}</div>',
        [("6%", "16%"), ("40%", "16%"), ("6%", "48%"), ("6%", "80%")],
        [("Head", f"{comp('avatar')} (sm), author link, stars and value, date."),
         ("Rating", f"{comp('rating')} for this one review, no count."),
         ("Text", "Body text, the buyer's words unedited."),
         ("Reply", "<code>.review__reply</code>: 2px rule on the left, muted small text, prefixed <b>Reply:</b>.")]),
    variants=ex(f'<div class="stack" style="width: 100%; max-width: 32rem;">'
                f'{review("vintage_lou", "LF", 4, "Tue 15 Sep", "Great pair, took a week to arrive.")}'
                f'{review("jaybird", "JP", 4, "Thu 17 Sep", "Good seller, a little slow to reply.", reply_link=True)}</div>',
                "Review · own profile with a <i>Reply</i> link (no reply yet).", show_code=False)
    + "<h3>Quote and thread</h3>"
    + ex('<blockquote class="quote"><p>“Ordered the wrong colour, sorry. Can we cancel?”</p><cite>tall_tom</cite></blockquote>'
         '<div class="thread" style="width: 100%; max-width: 28rem;"><div class="thread__item"><span class="text-caption">You · Sat 24 Oct</span><p>Label inside says 11.5, not 12.</p></div>'
         '<div class="thread__item"><span class="text-caption">vintage_lou · Sun 25 Oct</span><p>My mistake, the box said 12. Happy to take them back.</p></div></div>',
         "Quote in the respond-to-cancellation dialog · thread on an open problem.", stack=True),
    sizes=NA("One size."),
    states=matrix(["Default", "With reply", "Reply available", "Loading"], [
        ("Review", [f'<div style="width: 14rem;">{review("tall_tom", "TR", 5, "Mon 28 Sep", "Boxed well. Would buy again.")}</div>',
                    f'<div style="width: 14rem;">{review("tall_tom", "TR", 5, "Mon 5 Oct", "Shorts were spotless.", "Thanks Tom, enjoy them.")}</div>',
                    f'<div style="width: 14rem;">{review("jaybird", "JP", 4, "Thu 17 Sep", "A little slow to reply.", reply_link=True)}</div>',
                    '<div class="stack stack--sm" style="width: 14rem;" aria-hidden="true"><span class="skeleton skeleton--text" style="width: 50%;"></span><span class="skeleton skeleton--text"></span><span class="skeleton skeleton--text"></span></div>']),
    ], "Part")
    + p("The author link and Reply link have the standard link hover and focus. With no reviews, the reviews section shows a compact " + comp("empty-state") + ": <i>No reviews yet</i>.")
    + "<h3>Both themes</h3>" + themes(f'<div style="max-width: 22rem;">{review("tall_tom", "TR", 5, "Mon 5 Oct", "Shorts were spotless. Fast shipping.", "Thanks Tom, enjoy them.")}</div>'),
    responsive=ul("The head wraps: stars and date drop under the name on narrow screens (flex-wrap with <code>--space-3</code> gaps).",
                  "Reviews are a single column at every width, capped at the reading measure on profile pages."),
    theming=p("No surface: reviews sit on the canvas separated by <code>--color-border-default</code> rules. Replies and quotes use a left rule (<code>--color-border-default</code> 2px for replies, <code>--color-border-strong</code> 3px for quotes); thread items use <code>--color-bg-surface-sunken</code>."),
    accessibility=a11y(
        pattern="Each review is an <code>&lt;article&gt;</code> in a list; the date is a <code>&lt;time&gt;</code>. Quotes are <code>&lt;blockquote&gt;</code> with <code>&lt;cite&gt;</code>.",
        keyboard=[(kbd("Tab"), "Reaches the author link, then the Reply link when present.")],
        focus="Shared ring on the links.",
        labelling="The stars are <code>role=\"img\"</code>: <i>Rated 5 out of 5</i>. The reply starts with a bold <i>Reply:</i> so it is distinguishable without the rule.",
        contrast=[("Review text", "--color-fg-default", "--color-bg-canvas", 4.5), ("Reply text", "--color-fg-muted", "--color-bg-canvas", 4.5),
                  ("Thread text", "--color-fg-default", "--color-bg-surface-sunken", 4.5), ("Caption in thread", "--color-fg-muted", "--color-bg-surface-sunken", 4.5)],
        motion="None.",
        touch="Author and Reply links are text links with at least 24px line boxes."),
    content=ul("Show the buyer's words as written; 12L moderates abuse through reports, not edits.",
               "Dates as <i>Mon 5 Oct</i>; add the year only when it is not the current one.",
               "Quotes use typographic quotes (“ ”) and cite the member handle, not the real name.",
               "Thread captions: <i>You · Sat 24 Oct</i> for the viewer, the handle for the other member."),
    do_dont=dodont([
        ("do", f'<div style="width: 16rem;">{review("tall_tom", "TR", 5, "Mon 5 Oct", "Shorts were spotless.", "Thanks Tom, enjoy them.")}</div>', "One short public reply, under the review."),
        ("dont", '<div style="width: 16rem;"><article class="review"><p>Shorts were spotless.</p><div class="review__reply">Thanks!</div><div class="review__reply">Also, check my other listings</div></article></div>', "Several replies, or a review with no author, stars or date."),
        ("do", '<blockquote class="quote"><p>“Can we cancel?”</p><cite>tall_tom</cite></blockquote>', "Cite who said it."),
        ("dont", '<p class="text-muted"><i>Can we cancel?</i></p>', "Paraphrase the member in italics with no attribution."),
    ]),
    tokens=token_table([("Separator", "--color-border-default"), ("Reply rule", "--border-width-thick"), ("Quote rule", "--color-border-strong / --border-width-accent"),
                        ("Thread item", "--color-bg-surface-sunken"), ("Reply text", "--color-fg-muted"), ("Spacing", "--space-6 / --space-2 / --space-4")]),
    code=pre("""
<article class="review">
  <div class="review__head">
    <span class="avatar avatar--sm" aria-hidden="true">TR</span><a href="/u/tall_tom">tall_tom</a>
    <span class="rating" role="img" aria-label="Rated 5 out of 5">…</span>
    <span class="text-caption"><time datetime="2026-10-05">Mon 5 Oct</time></span>
  </div>
  <p>Shorts were spotless. Fast shipping.</p>
  <div class="review__reply"><strong>Reply:</strong> Thanks Tom, enjoy them.</div>
</article>

<blockquote class="quote"><p>“Ordered the wrong colour, sorry. Can we cancel?”</p><cite>tall_tom</cite></blockquote>""")
    + classes([("<code>.review</code>, <code>.review__head</code>", "Review block and its wrapping head row."), ("<code>.review__reply</code>", "Seller's one reply."),
               ("<code>.quote</code>", "Attributed quote with a 3px rule."), ("<code>.thread</code>, <code>.thread__item</code>", "Short buyer–seller exchange.")]),
    sources=sources([("pages/profile/default", "reviews on a seller's profile"), ("pages/profile/own", "Reply link on own reviews"),
                     ("dialogs/reply-review/default", "the review being replied to"), ("dialogs/respond-cancellation/default", "quote"),
                     ("pages/order-detail/problem", "thread")]),
)


# ---------------------------------------------------------------------------
# Buy bar
# ---------------------------------------------------------------------------
_phone_page = (f'<div class="ds-stage__page" style="max-width: 22rem; margin-inline: auto; height: 100%; position: relative; padding-bottom: 6rem;">'
               f'<span class="eyebrow">Nike</span><h2 class="detail__title" style="font-size: var(--font-size-2xl);">Air Max 90, white</h2>'
               f'<div class="cluster">{size_tag("US 12", "size-tag--lg")}<span class="text-muted">Used - Excellent</span></div>'
               f'<span class="price price--lg">$85.00</span><p class="text-muted">Worn a handful of times. Original box.</p>')

component(
    "buy-bar", "Buy bar", G,
    lead="The listing's purchase actions. On phones it sticks to the bottom of the screen with the total; from 1024px it sits in the info column.",
    pills=["<code>.buy-bar</code>", "Sticky below 1024px"],
    summary_variants="one action with total, two actions (total hidden), own listing (Edit / Withdraw), reserved/sold (no bar)",
    summary_states="default, loading (Buy now busy), guest (Sign in to buy)",
    overview=p("The buy bar keeps the one primary action of the listing page in reach while a buyer scrolls photos, description and seller details. It holds the total including shipping and at most two buttons.")
    + ul("<b>Buyer</b>: <i>Buy now</i> (primary, large) with <i>$94.00 incl. shipping</i>.",
         "<b>Guest</b>: <i>Sign in to buy</i>.",
         "<b>Own listing</b>: <i>Edit listing</i> and <i>Withdraw</i>; with two buttons the total is hidden to give them room.",
         "<b>Reserved or sold</b>: no bar; the stamp and a status line replace it."),
    anatomy=anatomy(
        f'<div style="width: 22rem; position: relative; height: 5rem;">{buy_bar(94, btn("Buy now", "primary lg"), phone=True)}</div>',
        [("10%", "30%"), ("10%", "70%"), ("70%", "50%")],
        [("Total", "<code>.buy-bar__price</code>: item plus shipping, bold tabular."),
         ("Caption", "<i>incl. shipping</i>, caption style."),
         ("Actions", f"Large {comp('button')}s that share the remaining width (<code>flex: 1</code>).")]),
    variants=stage(_phone_page + buy_bar(94, btn("Buy now", "primary lg"), phone=True) + "</div>", "22rem",
                   "Phone: pinned to the bottom with the total (shown in a frame; the real bar is <code>position: sticky</code> below 1024px).", show_code=False)
    + stage(_phone_page.replace("Air Max 90, white", "Reverse Weave hoodie, grey").replace("Nike", "Champion").replace("US 12", "L").replace("$85.00", "$38.00")
            + buy_bar(45, btn("Edit listing") + btn("Withdraw", "danger"), phone=True).replace('<div class="buy-bar__price" style="display: flex;">', '<div class="buy-bar__price" style="display: none;">') + "</div>", "22rem",
            "Own listing: two actions, total hidden.", show_code=False)
    + ex(f'<div style="width: 100%; max-width: 24rem;">{buy_bar(94, btn("Buy now", "primary lg"))}</div>', "Desktop (≥ 1024px): static in the info column, total hidden (the large price is just above)."),
    sizes=NA("Buttons in the bar are always large (48px); the bar has no size variants."),
    states=matrix(["Default", "Hover", "Focus", "Loading", "Guest"], [
        ("Phone bar", [f'<div style="width: 12rem; position: relative; height: 4.5rem;">{buy_bar(94, btn("Buy now", "primary lg"), phone=True)}</div>',
                       f'<div style="width: 12rem; position: relative; height: 4.5rem;">{buy_bar(94, btn("Buy now", "primary lg", attrs=chr(32) + "data-state=" + chr(34) + "hover" + chr(34)), phone=True)}</div>',
                       f'<div style="width: 12rem; position: relative; height: 4.5rem;">{buy_bar(94, btn("Buy now", "primary lg", attrs="data-state=" + chr(34) + "focus" + chr(34)), phone=True)}</div>',
                       f'<div style="width: 12rem; position: relative; height: 4.5rem;">{buy_bar(94, btn("Buy now", "primary lg", attrs="aria-busy=" + chr(34) + "true" + chr(34)), phone=True)}</div>',
                       f'<div style="width: 12rem; position: relative; height: 4.5rem;">{buy_bar(94, btn("Sign in to buy", "primary lg", href="#"), phone=True)}</div>']),
    ], "Part")
    + "<h3>Both themes</h3>" + themes(f'<div style="position: relative; height: 4.5rem;">{buy_bar(94, btn("Buy now", "primary lg"), phone=True)}</div>'),
    responsive=table(["Viewport", "Behaviour"], [
        ["&lt; 1024px", "<code>position: sticky; bottom: 0</code>, full bleed (negative <code>--layout-margin</code>), surface background with a top rule, total shown when there is one button."],
        ["≥ 1024px", "Static inside the info column after the price; no background, rule or total."]])
    + ul("The page reserves no extra bottom padding: sticky (not fixed) positioning releases the bar at the end of the info column.",
         "Buttons share the width equally and never wrap; labels are short enough to fit at 320px (<i>Buy now</i>, <i>Edit listing</i>, <i>Withdraw</i>)."),
    theming=p("Background <code>--color-bg-surface</code>, top rule <code>--color-border-default</code>, layer <code>--z-sticky</code>. In dark mode the bar is ink-900 over the ink-950 canvas, so it reads as raised without a shadow."),
    accessibility=a11y(
        pattern="A <code>&lt;div&gt;</code> in the info column's DOM order, after the price, so keyboard and screen-reader order match the desktop layout even when it is visually pinned on phones. No landmark role.",
        keyboard=[(kbd("Tab"), "Reaches the bar's buttons after the price, before the description."), (kbd("Enter") + " / " + kbd("Space"), "Activates the button.")],
        focus="Shared ring on the buttons. When focus moves to an element under the pinned bar, the page scrolls it into view above the bar (<code>scroll-padding-bottom</code> equal to the bar height).",
        labelling="Button labels stand alone (<i>Buy now</i>); the total's caption <i>incl. shipping</i> is plain text next to it.",
        contrast=[("Total on bar", "--color-fg-default", "--color-bg-surface", 4.5), ("Caption on bar", "--color-fg-muted", "--color-bg-surface", 4.5),
                  ("Primary label", "--color-fg-on-accent", "--color-accent", 4.5)],
        motion="None; the bar does not slide in or hide on scroll.",
        touch="48px buttons; the bar adds <code>--space-3</code> padding so its full height is 72px."),
    content=ul("One primary verb: <i>Buy now</i>. Not <i>Purchase</i>, not <i>Add to bag</i> (12L has no cart).", "Total caption is always <i>incl. shipping</i>; tax is added at checkout.",
               "Own listing actions: <i>Edit listing</i>, <i>Withdraw</i> (danger, opens a confirmation)."),
    do_dont=dodont([
        ("do", f'<div style="width: 16rem; position: relative; height: 4.5rem;">{buy_bar(94, btn("Buy now", "primary lg"), phone=True)}</div>', "One primary action with the total including shipping."),
        ("dont", f'<div style="width: 16rem; position: relative; height: 4.5rem;">{buy_bar(94, btn("Buy now", "primary lg") + btn("Offer", "primary lg") + btn("", "icon", icon="heart", attrs="aria-label=" + chr(34) + "Save" + chr(34)), phone=True)}</div>', "Crowd the bar with several emphasised actions."),
        ("do", '<div class="cluster"><span class="photo__stamp" style="position: static;">Sold</span><span class="text-muted">Sold Thu 22 Oct</span></div>', "Remove the bar on sold listings and say why."),
        ("dont", f'<div style="width: 16rem; position: relative; height: 4.5rem;">{buy_bar(85, btn("Buy now", "primary lg", attrs="disabled"), phone=True)}</div>', "Leave a disabled Buy now pinned to the screen."),
    ]),
    tokens=token_table([("Background", "--color-bg-surface"), ("Top rule", "--color-border-default"), ("Layer", "--z-sticky"), ("Padding", "--space-3 / --layout-margin"),
                        ("Gap", "--space-4"), ("Button height", "--control-height-lg")]),
    code=pre("""
<div class="buy-bar">
  <div class="buy-bar__price"><span class="price">$94.00</span><span class="text-caption">incl. shipping</span></div>
  <a class="btn btn--primary btn--lg" href="/checkout/L-20931">Buy now</a>
</div>""")
    + classes([("<code>.buy-bar</code>", "Sticky bottom bar below 1024px; static from 1024px."), ("<code>.buy-bar__price</code>", "Total; hidden from 1024px and whenever the bar holds two buttons."),
               ("<code>.buy-bar .btn</code>", "Large, equal-width buttons.")]),
    sources=sources([("pages/listing-detail/default", "Buy now with total"), ("pages/listing-detail/guest", "Sign in to buy"), ("pages/listing-detail/own", "Edit listing and Withdraw"),
                     ("pages/listing-detail/sold", "no bar on a sold listing")],
                    "the mock note said the bar pins below 992px (62rem); the system uses the lg breakpoint, 1024px (64rem)."),
)
