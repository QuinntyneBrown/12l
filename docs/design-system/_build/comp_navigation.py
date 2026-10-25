"""Navigation components: top bar, sidebar navigation, tabs, breadcrumb, pagination, stepper, footer, skip link."""
from ds import *

NAV = ["Shoes", "Tops", "Outerwear", "Bottoms"]
ACCOUNT_TABS = ["Overview", "Listings", "Purchases", "Sales", "Payouts", "Profile", "Emails", "Settings"]


def _st(state: str) -> str:
    """Attribute string for a documentation state."""
    return {"default": "", "hover": ' data-state="hover"', "focus": ' data-state="focus"', "active": ' data-state="active"',
            "current": ' aria-current="page"', "selected": ' aria-selected="true"', "disabled": ' aria-disabled="true"'}.get(state, "")


def topbar(sid: str, current: str = "Shoes", guest: bool = False) -> str:
    links = "".join(f'<a class="nav-link" href="#"{" aria-current=\"page\"" if n == current else ""}>{n}</a>' for n in NAV)
    search = (f'<form class="search" role="search" action="#"><label class="visually-hidden" for="{sid}">Search 12L</label>'
              f'{ic("search")}<input class="input" id="{sid}" name="q" type="search" placeholder="Search brands and items"></form>')
    if guest:
        right = (f'<a class="btn btn--ghost btn--icon topbar__search-btn" href="#" aria-label="Search">{ic("search")}</a>'
                 f'<a class="btn btn--ghost topbar__sell" href="#">Sell</a><a class="btn" href="#">Sign in</a>')
    else:
        right = (f'<a class="btn btn--ghost btn--icon topbar__search-btn" href="#" aria-label="Search">{ic("search")}</a>'
                 f'<a class="nav-link topbar__sell" href="#">{ic("plus")}Sell</a>'
                 f'<a class="avatar avatar--sm" href="#" aria-label="Your account, Marcus Bell" style="text-decoration: none;">MB</a>')
    return (f'<header class="topbar"><button class="btn btn--ghost btn--icon topbar__menu" type="button" aria-label="Open menu" aria-expanded="false">{ic("menu")}</button>'
            f'{logo()}<nav class="topbar__nav" aria-label="Primary">{links}</nav><span class="topbar__spacer"></span>{search}'
            f'<div class="topbar__actions">{right}</div></header>')


def admin_topbar(current: str = "Queue") -> str:
    links = "".join(f'<a class="nav-link" href="#"{" aria-current=\"page\"" if n == current else ""}>{n}</a>' for n in ["Queue", "Audit log"])
    return (f'<header class="topbar">{logo()}<span class="topbar__admin">Admin</span>'
            f'<nav class="topbar__nav" aria-label="Primary" style="display: flex;">{links}</nav><span class="topbar__spacer"></span>'
            f'<span class="avatar avatar--sm" aria-label="Signed in as Ana Ruiz" role="img">AR</span></header>')


def subnav(current: str = "Overview") -> str:
    return '<nav class="subnav" aria-label="Account" style="margin-top: 0;">' + "".join(
        f'<a class="tab" href="#"{" aria-current=\"page\"" if t == current else ""}>{t}</a>' for t in ACCOUNT_TABS) + "</nav>"


def footer_html() -> str:
    return (f'<footer class="footer" style="margin-top: 0;">{logo("logo--sm")}<nav aria-label="Footer"><a href="#">Marketplace rules</a>'
            '<a href="#">Privacy</a><a href="#">Terms</a><a href="#">Cookie settings</a></nav><span>© 2026 12L</span></footer>')


# ---------------------------------------------------------------------------
# Top bar
# ---------------------------------------------------------------------------
def _navlink(label: str, extra: str = ""):
    return lambda s: f'<a class="nav-link {extra}" href="#"{_st(s)}>{label}</a>'.replace('nav-link "', 'nav-link"')


component(
    "top-bar", "Top bar", "Navigation",
    lead="The sticky header on every member screen: menu button, the 12L logo, the four category links, search, Sell and the member's avatar.",
    pills=["<code>&lt;header&gt;</code> + <code>&lt;nav aria-label=\"Primary\"&gt;</code>"],
    summary_variants="member, guest, admin, compact (mobile)",
    summary_states="link default, hover, focus, current; menu expanded",
    overview=p("The top bar is the only global navigation. It stays on screen while the member scrolls (sticky, <code>--z-sticky</code>) so search and Sell are always one tap away. "
               f"The page itself provides the rest: account screens add {comp('tabs')}, listing detail adds a {comp('breadcrumb')}. Auth screens (sign in, register) drop the top bar for a centred logo.")
    + ul("<b>Member</b>: categories, search, <i>Sell</i> as a nav link with a plus icon, the avatar linking to the account.",
         "<b>Guest</b>: the same, with <i>Sell</i> as a ghost button and <i>Sign in</i> as a secondary button.",
         "<b>Admin</b>: logo, a red <i>Admin</i> tag, <i>Queue</i> and <i>Audit log</i>, and the administrator's initials. No search, no Sell.",
         f"<b>Compact</b> (below 768px): a menu button opens the full-screen menu sheet ({comp('drawer')}); search collapses to an icon button."),
    anatomy=anatomy(
        '<div style="width: 100%;">' + topbar("q-anat") + "</div>",
        [("2%", "8%"), ("9%", "8%"), ("25%", "8%"), ("55%", "8%"), ("88%", "8%")],
        [("Menu button", "Ghost icon button, <code>aria-expanded</code>, visible below 768px only."),
         ("Logo", "Links to the catalog; <code>aria-label=\"12L home\"</code>; 26px tall."),
         ("Primary nav", "Nav links, 64px tall, the current one marked by a 3px signal-red bar."),
         ("Search", "Search field from 1024px; an icon button below."),
         ("Actions", "Sell link and avatar (member) or Sell + Sign in (guest).")]),
    variants=ex(topbar("q-v1"), "Member, current category Shoes.", show_code=False)
    + ex(topbar("q-v2", current="", guest=True), "Guest: Sell and Sign in replace the avatar.", show_code=False)
    + ex(admin_topbar(), "Admin: the signal-red tag tells an administrator which side they are on.", show_code=False),
    sizes=NA("The top bar has one height, --layout-topbar-height (64px), at every breakpoint."),
    states=p("Nav links share the states below. The current page is marked with <code>aria-current=\"page\"</code>, which draws the brand bar; hover tints the background.")
    + state_matrix(["Default", "Hover", "Focus", "Current"],
                   [("Category link", _navlink("Shoes")), ("Sell link", lambda s: f'<a class="nav-link" href="#"{_st(s)}>{ic("plus")}Sell</a>'),
                    ("Menu button", lambda s: f'<button class="btn btn--ghost btn--icon" type="button" aria-label="Open menu" aria-expanded="{"true" if s == "current" else "false"}"{_st(s) if s != "current" else ""}>{ic("menu")}</button>')],
                   first="Element")
    + p("For the menu button, “Current” means expanded: <code>aria-expanded=\"true\"</code> while the menu sheet is open.")
    + "<h3>Both themes</h3>" + themes(topbar("q-th-dark"), light=topbar("q-th-light")),
    responsive=ul("Below 768px: menu button, logo, spacer, search icon button and avatar. The category links and Sell move into the menu sheet.",
                  "768px–1023px: category links and Sell appear; search is still an icon button that opens the catalog search state.",
                  "1024px and up: the search field appears (max 22rem) and the search icon button hides.",
                  "Height stays 64px; horizontal padding follows <code>--layout-margin</code> (16 / 32 / 48px)."),
    theming=p("The bar is <code>--color-bg-surface</code> with a hairline <code>--color-border-default</code> bottom edge, so in dark it reads as a raised ink-900 strip over the ink-950 canvas. "
              "Nav links use <code>--color-fg-muted</code> and turn <code>--color-fg-default</code> on hover and when current; the current bar is <code>--color-brand</code> in both themes. "
              "The admin tag is <code>--color-brand</code> with <code>--color-fg-on-brand</code>."),
    accessibility=a11y(
        pattern="A <code>&lt;header&gt;</code> landmark containing a <code>&lt;nav aria-label=\"Primary\"&gt;</code> of plain links (not an APG menubar), a <code>role=\"search\"</code> form, and a disclosure button for the mobile menu (<code>aria-expanded</code>, <code>aria-controls=\"menu\"</code>).",
        keyboard=[(kbd("Tab"), "Moves through menu button, logo, category links, search, Sell, avatar in that order."),
                  (kbd("Enter"), "Follows a link; on the menu button opens the menu sheet and moves focus to its close button."),
                  (kbd("Esc"), "Closes the menu sheet and returns focus to the menu button.")],
        focus="The shared focus ring; nav links are 44px+ tall so the ring never clips. The skip link precedes the bar so keyboard users can jump straight to <code>#main</code>.",
        labelling="Icon-only controls carry labels: <i>Open menu</i>, <i>Search</i>, <i>Your account, Marcus Bell</i>. The search input has a visually hidden <i>Search 12L</i> label. The current category is announced through <code>aria-current=\"page\"</code>, not colour alone.",
        contrast=[("Muted link on bar", "--color-fg-muted", "--color-bg-surface", 4.5), ("Current link", "--color-fg-default", "--color-bg-surface", 4.5),
                  ("Current-page bar", "--color-brand", "--color-bg-surface", 3), ("Admin tag", "--color-fg-on-brand", "--color-brand", 4.5)],
        motion="Link colour and background change over <code>--duration-fast</code>. The bar itself never animates or hides on scroll.",
        touch="Nav links are <code>--layout-topbar-height</code> (64px) tall; icon buttons 40px; the avatar 32px with 8px around it."),
    content=ul("Category names are single nouns in title case as they appear in the catalog: Shoes, Tops, Outerwear, Bottoms.",
               "<i>Sell</i>, never <i>Create listing</i> or <i>Post</i>.",
               "Guest call to action is <i>Sign in</i>; registration is offered from the sign-in page.",
               "The account link's label names the member: <i>Your account, Marcus Bell</i>."),
    do_dont=dodont([
        ("do", f'<nav class="cluster" aria-label="Example"><a class="nav-link" href="#" aria-current="page">Shoes</a><a class="nav-link" href="#">Tops</a></nav>', "Mark the current category with <code>aria-current</code>; the red bar follows."),
        ("dont", '<nav class="cluster" aria-label="Example 2"><a class="nav-link" href="#" style="color: var(--color-brand);">Shoes</a><a class="nav-link" href="#">Tops</a></nav>', "Colour the current link red. Signal red is never text, and colour alone does not announce the current page."),
        ("do", f'<button class="btn btn--ghost btn--icon" type="button" aria-label="Open menu" aria-expanded="false">{ic("menu")}</button>', "Label the menu button and expose its expanded state."),
        ("dont", f'<button class="btn btn--primary" type="button">Sell</button><button class="btn btn--primary" type="button">Sign in</button>', "Put primary buttons in the top bar. The bar stays quiet; the page owns its one primary action."),
    ]),
    tokens=token_table([("Background / bottom edge", "--color-bg-surface / --color-border-default"), ("Link / current link", "--color-fg-muted / --color-fg-default"),
                        ("Link hover background", "--color-bg-subtle"), ("Current bar", "--color-brand"), ("Admin tag", "--color-brand / --color-fg-on-brand"),
                        ("Height", "--layout-topbar-height"), ("Side padding", "--layout-margin"), ("Gap mobile / tablet+", "--space-3 / --space-6"),
                        ("Current bar width", "--border-width-accent"), ("Layer", "--z-sticky")]),
    code=pre("""
<header class="topbar">
  <button class="btn btn--ghost btn--icon topbar__menu" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="menu">…</button>
  <a class="logo" href="/" aria-label="12L home">…</a>
  <nav class="topbar__nav" aria-label="Primary">
    <a class="nav-link" href="/shoes" aria-current="page">Shoes</a> …
  </nav>
  <span class="topbar__spacer"></span>
  <form class="search" role="search"><label class="visually-hidden" for="q">Search 12L</label>…<input class="input" id="q" type="search"></form>
  <div class="topbar__actions">
    <a class="btn btn--ghost btn--icon topbar__search-btn" href="/search" aria-label="Search">…</a>
    <a class="nav-link topbar__sell" href="/sell">…Sell</a>
    <a class="avatar avatar--sm" href="/account" aria-label="Your account, Marcus Bell">MB</a>
  </div>
</header>""")
    + classes([("<code>.topbar</code>", "Sticky bar, surface background, hairline bottom edge."), ("<code>.topbar__menu</code>", "Menu button; hidden from 768px."),
               ("<code>.topbar__nav</code>", "Primary links; shown from 768px."), ("<code>.topbar__spacer</code>", "Pushes search and actions right."),
               ("<code>.topbar__search-btn</code>", "Search icon button; hidden from 1024px."), ("<code>.topbar__sell</code>", "Sell link; shown from 768px."),
               ("<code>.topbar__admin</code>", "Red Admin tag."), ("<code>.nav-link</code> + <code>aria-current=\"page\"</code>", "Link; current page gets the brand bar.")]),
    sources=sources([("pages/catalog/default", "member top bar"), ("pages/catalog/guest", "guest top bar"), ("pages/catalog/category", "Shoes current"),
                     ("pages/moderation-queue/default", "admin top bar"), ("dialogs/nav-menu/default", "menu button expanded")],
                    "the search field appeared at the mocks' 62rem breakpoint; it now appears at the system's lg breakpoint (64rem)."),
)


# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------
def sidebar(current: str = "Listings", sid: str = "") -> str:
    groups = [("Buying", ["Purchases", "Saved"]), ("Selling", ["Listings", "Sales", "Payouts"]), ("Account", ["Profile", "Settings"])]
    icons = {"Purchases": "bag", "Saved": "heart", "Listings": "tag", "Sales": "box", "Payouts": "bank", "Profile": "user", "Settings": "settings"}
    out = ""
    for g, items in groups:
        out += f'<p class="sidebar__group">{g}</p>' + "".join(
            f'<a class="nav-link" href="#"{" aria-current=\"page\"" if i == current else ""}>{ic(icons[i])}{i}</a>' for i in items)
    return f'<nav class="sidebar ds-sidebar-demo" aria-label="Account sections{sid}">{out}</nav>'


component(
    "sidebar-navigation", "Sidebar navigation", "Navigation",
    lead="A vertical list of grouped links for sections a member moves between often. Part of the core kit; no 12L mock uses it yet.",
    pills=["Core (not in mocks)"],
    summary_variants="grouped, with icons",
    summary_states="default, hover, focus, current",
    overview=p(f"The mocks put account sections in horizontal {comp('tabs')} (the account sub-nav) because there are only eight of them and the content needs the width. "
               "The sidebar is documented from <code>.sidebar</code> in components.css for when a section outgrows tabs, for example a future seller dashboard or admin console with more than eight destinations. "
               "Until then, prefer tabs for account screens and the top bar for everything global.")
    + ul("Use it for 6–20 destinations in named groups.", "Do not use it for actions; actions are buttons in the page header.",
         "Do not combine it with sub-nav tabs for the same level of hierarchy."),
    anatomy=anatomy(sidebar("Listings", " anatomy"), [("10%", "4%"), ("8%", "45%"), ("70%", "45%")],
                    [("Group label", "Overline, <code>--color-fg-subtle</code>, not focusable."), ("Icon", "20px, <code>aria-hidden</code>."),
                     ("Link", "Full-width nav link, 44px tall; current gets the brand bar.")]),
    variants=ex(sidebar("Listings", " variants"), "Grouped, with icons. Without icons, drop the svg; groups stay.", show_code=False),
    sizes=NA("One width: --layout-sidebar-width (256px)."),
    states=state_matrix(["Default", "Hover", "Focus", "Current"],
                        [("Link", lambda s: f'<a class="nav-link" href="#"{_st(s)} style="width: 12rem;">{ic("tag")}Listings</a>')], first="Element")
    + "<h3>Both themes</h3>" + themes(sidebar("Sales", " dark"), light=sidebar("Sales", " light")),
    responsive=ul("Hidden below 1024px; the page shows a menu button that sets <code>data-open=\"true\"</code> to reveal it as an overlay.",
                  "From 1024px it sits in a <code>.sidebar-layout</code> grid column, sticky and full height, scrolling on its own."),
    theming=p("Surface background with a hairline right edge. Links reuse <code>.nav-link</code>, so they theme exactly like the top bar: muted text, subtle hover, brand bar for the current page."),
    accessibility=a11y(
        pattern="A <code>&lt;nav aria-label&gt;</code> landmark of links; group labels are paragraphs (or headings when the groups are long). Not an APG tree or menu.",
        keyboard=[(kbd("Tab"), "Moves through links top to bottom."), (kbd("Enter"), "Follows the link.")],
        focus="Shared focus ring inside the 44px link.",
        labelling="Give each sidebar a distinct <code>aria-label</code> (<i>Account sections</i>). The current link has <code>aria-current=\"page\"</code>.",
        contrast=[("Link", "--color-fg-muted", "--color-bg-surface", 4.5), ("Group label", "--color-fg-subtle", "--color-bg-surface", 4.5),
                  ("Current bar", "--color-brand", "--color-bg-surface", 3)],
        motion="Colour changes over <code>--duration-fast</code>.",
        touch="Links meet the 44px comfortable target."),
    content=ul("Links are nouns naming the destination: <i>Listings</i>, <i>Payouts</i>.", "Group labels are one word: <i>Buying</i>, <i>Selling</i>, <i>Account</i>."),
    do_dont=dodont([("do", sidebar("Listings", " do"), "Group destinations under short labels."),
                    ("dont", f'<nav class="sidebar ds-sidebar-demo" aria-label="Bad example"><a class="nav-link" href="#">{ic("plus")}Sell an item</a><a class="nav-link" href="#">{ic("log-out")}Sign out</a></nav>', "Mix actions (Sell, Sign out) into navigation."),
                    ("do", subnav("Listings"), "With eight or fewer account sections, use the tabs the mocks use."),
                    ("dont", sidebar("Listings", " dont2") + subnav("Listings"), "Show a sidebar and tabs for the same destinations.")]),
    tokens=token_table([("Background / edge", "--color-bg-surface / --color-border-default"), ("Group label", "--color-fg-subtle"), ("Link / current", "--color-fg-muted / --color-fg-default"),
                        ("Current bar", "--color-brand"), ("Width", "--layout-sidebar-width"), ("Padding", "--space-4"), ("Link height", "--target-comfortable")]),
    code=pre("""
<div class="sidebar-layout">
  <nav class="sidebar" aria-label="Account sections">
    <p class="sidebar__group">Selling</p>
    <a class="nav-link" href="/account/listings" aria-current="page">…Listings</a>
  </nav>
  <main id="main">…</main>
</div>""")
    + classes([("<code>.sidebar-layout</code>", "Grid: one column, sidebar + content from 1024px."), ("<code>.sidebar</code>", "The panel; hidden below 1024px."),
               ("<code>.sidebar[data-open=\"true\"]</code>", "Shown below 1024px when opened."), ("<code>.sidebar__group</code>", "Group label."),
               ("<code>.nav-link</code>", "Each destination.")]),
    sources=sources([("pages/account/default", "the account sub-nav the sidebar would replace"), ("pages/my-listings/default", "account section destinations")],
                    "none; the component is not used by any mock. Its breakpoint moved from 62rem to 64rem with the rest of the kit."),
)


# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------
def _tablist(sel: int = 0, pid: str = "t") -> str:
    labels = [("Selling", 3), ("Sold", 19), ("Drafts", 1)]
    tabs = "".join(f'<button class="tab" role="tab" type="button" id="{pid}-{i}" aria-selected="{"true" if i == sel else "false"}" aria-controls="{pid}-panel"{"" if i == sel else " tabindex=\"-1\""}>{l}<span class="badge">{n}</span></button>'
                   for i, (l, n) in enumerate(labels))
    return f'<div class="tabs" role="tablist" aria-label="Listing status">{tabs}</div><div id="{pid}-panel" role="tabpanel" aria-labelledby="{pid}-{sel}" style="padding-top: var(--space-4);" class="text-muted text-sm">3 listings selling.</div>'


component(
    "tabs", "Tabs", "Navigation",
    lead="Tabs switch between views of the same thing (listing statuses) or between sibling pages (the account sub-nav). The selected tab carries the red bar.",
    pills=["APG Tabs", "Link tabs for sub-pages"],
    summary_variants="tab panel (role=tablist), link tabs (sub-nav), with counts, scrollable",
    summary_states="default, hover, focus, selected/current, disabled",
    overview=p("Two variants share one look:")
    + ul("<b>Tab panel</b>: buttons with <code>role=\"tab\"</code> that swap content on the same page without a URL change. Use for filtered views of one collection.",
         "<b>Link tabs</b> (<code>.subnav</code>): real links with <code>aria-current=\"page\"</code> that go to sibling pages. The account area uses these: Overview, Listings, Purchases, Sales, Payouts, Profile, Emails, Settings.")
    + p(f"Use link tabs whenever each view deserves its own URL. Use a {comp('button-group')} for a setting, not a view."),
    anatomy=anatomy(_tablist(0, "ta"), [("6%", "18%"), ("22%", "18%"), ("8%", "44%")],
                    [("Tab label", "<code>--text-label</code>, muted until selected."), ("Count (optional)", "A neutral badge."),
                     ("Selected bar", "3px <code>--color-brand</code> over the hairline baseline.")]),
    variants=ex(_tablist(0, "tv"), "Tab panel with counts.") + ex(subnav("Overview"), "Link tabs: the account sub-nav. Scrolls horizontally when it does not fit."),
    sizes=NA("One size: tabs are 44px tall (--target-comfortable) everywhere."),
    states=state_matrix(["Default", "Hover", "Focus", "Selected", "Disabled"],
                        [("Tab", lambda s: f'<button class="tab" role="tab" type="button" aria-selected="{"true" if s == "selected" else "false"}"{_st(s) if s not in ("selected",) else ""}{" disabled" if s == "disabled" else ""}>Selling</button>'),
                         ("Link tab", lambda s: f'<a class="tab" href="#"{_st("current" if s == "selected" else s)}>Purchases</a>')])
    + p("Disabled tabs are rare; prefer hiding a view the member cannot reach. Link tabs are never disabled.")
    + "<h3>Both themes</h3>" + themes(subnav("Sales")),
    responsive=ul("Tabs never wrap; the list scrolls horizontally (scrollbar hidden) and the selected tab is scrolled into view on load.",
                  "At 360px the account sub-nav shows about four tabs; the cut-off fifth tab signals that it scrolls.",
                  "Labels never truncate."),
    theming=p("Labels use <code>--color-fg-muted</code>, turning <code>--color-fg-default</code> on hover and selection. The baseline is <code>--color-border-default</code>; the selected bar is <code>--color-brand</code> in both themes."),
    accessibility=a11y(
        pattern="Tab panel: APG Tabs with <code>role=\"tablist\"</code>, <code>role=\"tab\"</code>, <code>role=\"tabpanel\"</code>, roving <code>tabindex</code> and <b>automatic activation</b> (arrow keys select). Link tabs: a <code>&lt;nav aria-label=\"Account\"&gt;</code> of links with <code>aria-current=\"page\"</code>; no tab roles.",
        keyboard=[(kbd("Tab"), "Tab panel: focus enters the selected tab, the next Tab goes into the panel. Link tabs: each link is a stop."),
                  (kbd("←") + " / " + kbd("→"), "Tab panel: select the previous / next tab (wraps)."),
                  (kbd("Home") + " / " + kbd("End"), "Tab panel: first / last tab."), (kbd("Enter"), "Link tabs: follow the link.")],
        focus="Shared ring around the tab; the selected bar stays visible under it.",
        labelling="The tablist has an <code>aria-label</code> (<i>Listing status</i>); each panel is labelled by its tab. Counts are part of the tab's name (<i>Sold 19</i>).",
        contrast=[("Unselected label", "--color-fg-muted", "--color-bg-canvas", 4.5), ("Selected label", "--color-fg-default", "--color-bg-canvas", 4.5),
                  ("Selected bar", "--color-brand", "--color-bg-canvas", 3)],
        motion="The bar's colour fades in over <code>--duration-fast</code>; nothing slides.",
        touch="Each tab is 44px tall with 12px side padding."),
    content=ul("One or two words, nouns: <i>Purchases</i>, <i>Payouts</i>. The account email-preferences tab is <i>Emails</i>, not <i>Notification settings</i>.",
               "Counts go in a badge, not in brackets."),
    do_dont=dodont([("do", subnav("Purchases"), "Sibling pages are link tabs with <code>aria-current</code>."),
                    ("dont", '<div class="tabs" role="tablist" aria-label="Bad"><button class="tab" role="tab" type="button" aria-selected="true">Overview</button><button class="tab" role="tab" type="button" aria-selected="false">Purchases</button></div>', "Use <code>role=\"tab\"</code> for links to other pages: screen readers then expect a panel on this page."),
                    ("do", _tablist(1, "td"), "Show counts in neutral badges."),
                    ("dont", '<div class="tabs" role="tablist" aria-label="Bad 2"><button class="tab" role="tab" type="button" aria-selected="true">Listings that are currently selling</button></div>', "Write sentences in tabs; they scroll off at 360px.")]),
    tokens=token_table([("Label / selected label", "--color-fg-muted / --color-fg-default"), ("Baseline", "--color-border-default"), ("Selected bar", "--color-brand"),
                        ("Height", "--target-comfortable"), ("Padding / gap", "--space-3 / --space-1"), ("Bar thickness", "--border-width-accent"), ("Transition", "--duration-fast")]),
    code=pre("""
<div class="tabs" role="tablist" aria-label="Listing status">
  <button class="tab" role="tab" id="t-0" aria-selected="true" aria-controls="p-0">Selling <span class="badge">3</span></button>
  <button class="tab" role="tab" id="t-1" aria-selected="false" aria-controls="p-1" tabindex="-1">Sold</button>
</div>
<div role="tabpanel" id="p-0" aria-labelledby="t-0">…</div>

<nav class="subnav" aria-label="Account">
  <a class="tab" href="/account" aria-current="page">Overview</a>
  <a class="tab" href="/account/listings">Listings</a>
</nav>""")
    + classes([("<code>.tabs</code>", "Tablist row with baseline; scrolls horizontally."), ("<code>.subnav</code>", "Link-tab row for sibling pages."),
               ("<code>.tab</code>", "A tab (button or link)."), ("<code>aria-selected=\"true\"</code> / <code>aria-current=\"page\"</code>", "Selected; draws the brand bar."),
               ("<code>disabled</code>", "Disabled tab (button only).")]),
    sources=sources([("pages/account/default", "account sub-nav, Overview current"), ("pages/purchases/default", "Purchases current"),
                     ("pages/my-listings/default", "Listings current"), ("pages/settings/default", "last tab scrolled into view")]),
)


# ---------------------------------------------------------------------------
# Breadcrumb
# ---------------------------------------------------------------------------
def crumbs(items=("Shop", "Shoes", "Sneakers"), label: str = "Breadcrumb") -> str:
    li = "".join(f'<li><a href="#">{x}</a></li>' for x in items[:-1]) + f'<li aria-current="page">{items[-1]}</li>'
    return f'<nav aria-label="{label}"><ol class="breadcrumb">{li}</ol></nav>'


component(
    "breadcrumb", "Breadcrumb", "Navigation",
    lead="Shows where a listing or order sits and lets the member step back up: Shop / Shoes / Sneakers.",
    pills=["<code>&lt;nav aria-label=\"Breadcrumb\"&gt;</code>"],
    summary_variants="category path, back to list",
    summary_states="link default, hover, focus; current",
    overview=p("Use a breadcrumb on detail pages that sit under a hierarchy: listing detail (category path), order and sale detail (<i>Purchases / Order 12L-48213</i>), admin report and problem detail. "
               "Do not use it on top-level pages or as the only way back from a dialog.")
    + ul("<b>Category path</b>: Shop / Shoes / Sneakers on listing detail.", "<b>Back to list</b>: two levels, the list and the item: Sales / Order 12L-48302."),
    anatomy=anatomy(crumbs(label="Breadcrumb anatomy"), [("6%", "10%"), ("22%", "10%"), ("45%", "10%")],
                    [("Ancestor link", "Muted, no underline until hover."), ("Separator", "A slash drawn by CSS; not read out."), ("Current page", "Default colour, medium weight, not a link.")]),
    variants=ex(crumbs(label="Category path")) + ex(crumbs(("Sales", "Order 12L-48302"), "Back to list"), "Order and sale detail use two levels."),
    sizes=NA("One size: --text-body-sm."),
    states=state_matrix(["Default", "Hover", "Focus", "Current"],
                        [("Crumb", lambda s: f'<ol class="breadcrumb"><li><a href="#"{_st(s)}>Shoes</a></li></ol>' if s != "current" else '<ol class="breadcrumb"><li aria-current="page">Sneakers</li></ol>')], first="Element")
    + "<h3>Both themes</h3>" + themes(crumbs(label="Breadcrumb dark"), light=crumbs(label="Breadcrumb light")),
    responsive=ul("The list wraps onto a second line rather than truncating.", "Below 640px, paths deeper than three levels collapse to the parent only, shown with a back arrow: <i>← Shoes</i>."),
    theming=p("Ancestors <code>--color-fg-muted</code>, separators <code>--color-fg-subtle</code>, current <code>--color-fg-default</code>. No component tokens."),
    accessibility=a11y(
        pattern="APG Breadcrumb: <code>&lt;nav aria-label=\"Breadcrumb\"&gt;</code> around an ordered list; the last item has <code>aria-current=\"page\"</code>. Separators are CSS generated content so they are not announced.",
        keyboard=[(kbd("Tab"), "Each ancestor link is a stop; the current item is not focusable."), (kbd("Enter"), "Follows the link.")],
        focus="Shared focus ring.", labelling="One breadcrumb per page, labelled <i>Breadcrumb</i>.",
        contrast=[("Ancestor link", "--color-fg-muted", "--color-bg-canvas", 4.5), ("Current", "--color-fg-default", "--color-bg-canvas", 4.5)],
        motion="None.", touch="Links are inline text; the row has 8px gaps. On phones the collapsed back link is 44px tall."),
    content=ul("Use the same names as the destination pages' headings.", "The current item is the page's own name, short: the order number, not the item title."),
    do_dont=dodont([("do", crumbs(label="Do"), "End with the current page, not a link."),
                    ("dont", '<nav aria-label="Dont"><ol class="breadcrumb"><li><a href="#">Home</a></li><li><a href="#">Shop</a></li><li><a href="#">Shoes</a></li><li><a href="#">Sneakers</a></li><li><a href="#">Nike</a></li><li aria-current="page">Air Max 90, white</li></ol></nav>', "Repeat the whole title and every level; the logo already goes home."),
                    ("do", crumbs(("Purchases", "Order 12L-48213"), "Do 2"), "Name the list the member came from."),
                    ("dont", '<p class="text-sm"><a href="#">← Back</a></p>', "A bare Back link that depends on browser history.")]),
    tokens=token_table([("Ancestor / hover", "--color-fg-muted / --color-fg-default"), ("Separator", "--color-fg-subtle"), ("Current", "--color-fg-default"),
                        ("Font", "--text-body-sm"), ("Gap", "--space-2")]),
    code=pre("""
<nav aria-label="Breadcrumb">
  <ol class="breadcrumb">
    <li><a href="/">Shop</a></li>
    <li><a href="/shoes">Shoes</a></li>
    <li aria-current="page">Sneakers</li>
  </ol>
</nav>""") + classes([("<code>.breadcrumb</code>", "The ordered list; draws separators."), ("<code>aria-current=\"page\"</code>", "Current item styling.")]),
    sources=sources([("pages/listing-detail/default", "Shop / Shoes / Sneakers"), ("pages/order-detail/default", "order breadcrumb"), ("pages/report-detail/default", "admin breadcrumb")]),
)


# ---------------------------------------------------------------------------
# Pagination
# ---------------------------------------------------------------------------
def pager(cur: int = 2, label: str = "Pagination") -> str:
    prev = '<li><a href="#" aria-label="Previous page">' + ic("chevron-left", "icon icon--sm") + "</a></li>" if cur > 1 else '<li><a aria-disabled="true" aria-label="Previous page">' + ic("chevron-left", "icon icon--sm") + "</a></li>"
    pages = "".join(f'<li><a href="#"{" aria-current=\"page\"" if n == cur else ""} aria-label="Page {n}">{n}</a></li>' for n in (1, 2, 3))
    return f'<nav aria-label="{label}"><ul class="pagination">{prev}{pages}<li><span class="text-subtle" aria-hidden="true">…</span></li><li><a href="#" aria-label="Page 12">12</a></li><li><a href="#" aria-label="Next page">{ic("chevron-right", "icon icon--sm")}</a></li></ul></nav>'


LOAD_MORE = '<div class="load-more" style="margin-top: 0;"><span class="text-sm text-muted">Showing 14 of 1,284</span><button class="btn" type="button" aria-describedby="lm-note">Load more</button><span id="lm-note" class="visually-hidden">Loads the next 24 items</span></div>'

component(
    "pagination", "Pagination", "Navigation",
    lead="Moves through long result sets. The catalog uses Load more; numbered pagination is the core alternative for tables and the audit log.",
    pills=["<code>&lt;nav aria-label=\"Pagination\"&gt;</code>"],
    summary_variants="load more (catalog), numbered, simple prev/next",
    summary_states="default, hover, focus, current, disabled; load more busy",
    overview=p("Browsing listings is exploratory, so the catalog appends results with a <b>Load more</b> button and a count (<i>Showing 14 of 1,284</i>), keeping earlier items and the scroll position. "
               "Numbered pagination is for lists people search by position or come back to: admin queues, the audit log, long order histories. Never use infinite scroll: the footer must stay reachable.")
    + p(f"See {patt('data-tables-and-lists')} for which to choose."),
    anatomy=anatomy(pager(2, "Pagination anatomy"), [("3%", "12%"), ("30%", "12%"), ("60%", "12%")],
                    [("Previous / next", "Icon links with <code>aria-label</code>; disabled at the ends."), ("Current page", "Accent-subtle fill and accent edge, <code>aria-current=\"page\"</code>."),
                     ("Gap", "An ellipsis hidden from assistive tech.")]),
    variants=ex(LOAD_MORE, "Load more: count, then a secondary button. The count updates after loading.") + ex(pager(2, "Numbered"), "Numbered.")
    + ex(f'<nav aria-label="Simple"><ul class="pagination"><li><a href="#">{ic("chevron-left", "icon icon--sm")}Newer</a></li><li><a href="#">Older{ic("chevron-right", "icon icon--sm")}</a></li></ul></nav>', "Simple previous / next for the audit log."),
    sizes=NA("One size: 32px square items (--control-height-sm)."),
    states=state_matrix(["Default", "Hover", "Focus", "Current", "Disabled"],
                        [("Page link", lambda s: f'<ul class="pagination"><li><a href="#"{_st(s)} aria-label="Page 3">3</a></li></ul>'),
                         ("Load more", lambda s: btn("Load more", attrs={"default": "", "hover": 'data-state="hover"', "focus": 'data-state="focus"', "current": 'aria-busy="true"', "disabled": "disabled"}[s]))], first="Element")
    + p("For Load more the “Current” column shows the busy state while the next 24 items load; skeleton cards are appended at the same time.")
    + "<h3>Both themes</h3>" + themes(pager(2, "Pagination dark"), light=pager(2, "Pagination light")),
    responsive=ul("Below 640px numbered pagination shows previous, current of total and next (<i>2 of 12</i>) instead of every number.", "Load more is centred and full width below 640px."),
    theming=p("Items are transparent with <code>--color-fg-muted</code> labels; hover uses <code>--color-bg-subtle</code>; the current page reuses the selected treatment (<code>--color-accent-subtle</code> fill, <code>--color-accent</code> edge)."),
    accessibility=a11y(
        pattern="A <code>&lt;nav aria-label=\"Pagination\"&gt;</code> with a list of links. Load more is a <code>&lt;button&gt;</code> described by <i>Loads the next 24 items</i>; after loading, focus moves to the first new item.",
        keyboard=[(kbd("Tab"), "Each page link is a stop; disabled ends are skipped."), (kbd("Enter"), "Goes to the page / loads more.")],
        focus="Shared focus ring on the 32px item.",
        labelling="Numbers get <code>aria-label=\"Page 3\"</code>; arrows <i>Previous page</i> / <i>Next page</i>. The result count is plain text next to Load more and is updated through the catalog's polite live region.",
        contrast=[("Page number", "--color-fg-muted", "--color-bg-canvas", 4.5), ("Current page", "--color-fg-accent", "--color-accent-subtle", 4.5), ("Current edge", "--color-accent", "--color-bg-canvas", 3)],
        motion="None; new results appear without animation.", touch="32px items with 4px gaps meet the 24px minimum; Load more is a 40px button."),
    content=ul("Count format: <i>Showing 14 of 1,284</i>, with thousands separators.", "Button label: <i>Load more</i>, never <i>See more results…</i>.", "Simple pager labels for time-ordered lists: <i>Newer</i> / <i>Older</i>."),
    do_dont=dodont([("do", LOAD_MORE, "Say how many are shown out of how many."),
                    ("dont", '<div class="load-more" style="margin-top: 0;"><button class="btn btn--primary" type="button">Load more</button></div>', "Make Load more primary; the primary action on the catalog is opening a listing."),
                    ("do", pager(1, "Do numbered"), "Disable Previous on the first page."),
                    ("dont", '<nav aria-label="Dont numbered"><ul class="pagination"><li><a href="#">1</a></li><li><a href="#">2</a></li></ul></nav>', "Use numbers without labels or a current page.")]),
    tokens=token_table([("Label / hover", "--color-fg-muted / --color-fg-default"), ("Hover background", "--color-bg-subtle"), ("Current fill / edge / label", "--color-accent-subtle / --color-accent / --color-fg-accent"),
                        ("Item size", "--control-height-sm"), ("Radius", "--radius-md"), ("Load more gap", "--space-3")]),
    code=pre("""
<div class="load-more">
  <span class="text-sm text-muted">Showing 14 of 1,284</span>
  <button class="btn" type="button" aria-describedby="lm-note">Load more</button>
  <span id="lm-note" class="visually-hidden">Loads the next 24 items</span>
</div>

<nav aria-label="Pagination"><ul class="pagination">
  <li><a href="?page=1" aria-label="Page 1">1</a></li>
  <li><a href="?page=2" aria-label="Page 2" aria-current="page">2</a></li>
</ul></nav>""")
    + classes([("<code>.load-more</code>", "Count + button, centred."), ("<code>.pagination</code>", "Row of page links."),
               ("<code>aria-current=\"page\"</code>", "Current page."), ("<code>aria-disabled=\"true\"</code>", "Unavailable end (no <code>href</code>).")]),
    sources=sources([("pages/catalog/default", "Load more with count"), ("pages/catalog/loading", "results loading"), ("pages/audit-log/default", "long list")]),
)


# ---------------------------------------------------------------------------
# Stepper
# ---------------------------------------------------------------------------
def timeline(cur: str = "Shipped") -> str:
    steps = [("Paid", "Thu 22 Oct"), ("Shipped", "Fri 23 Oct"), ("Delivered", ""), ("Completed", "")]
    idx = [s for s, _ in steps].index(cur)
    li = ""
    for i, (s, d) in enumerate(steps):
        attr = " data-done" if i < idx else (' aria-current="step"' if i == idx else "")
        li += f"<li{attr}><b>{s}</b><span>{d if i <= idx else ''}</span></li>"
    return f'<ol class="timeline" aria-label="Order progress">{li}</ol>'


def stepper(cur: int = 1, label: str = "Listing steps") -> str:
    steps = ["Photos", "Details", "Price", "Review"]
    li = "".join(f'<li{" data-complete" if i < cur else (" aria-current=\"step\"" if i == cur else "")}><span>{s}</span></li>' for i, s in enumerate(steps))
    return f'<ol class="stepper" aria-label="{label}">{li}</ol>'


component(
    "stepper", "Stepper", "Navigation",
    lead="Shows progress through fixed stages. Orders use the timeline (Paid, Shipped, Delivered, Completed); the numbered stepper is the core form variant.",
    pills=["<code>&lt;ol&gt;</code> + <code>aria-current=\"step\"</code>"],
    summary_variants="order timeline, numbered stepper",
    summary_states="complete, current, upcoming",
    overview=p("The <b>order timeline</b> sits at the top of order and sale detail. It is status, not navigation: the steps are not links, and the dates say when each happened. "
               "The current step is drawn in signal red, completed steps in ink, upcoming in the hairline colour.")
    + p("The <b>numbered stepper</b> (<code>.stepper</code>) is for multi-step forms. 12L's sell and checkout flows are single pages with sections, so no mock uses it yet; keep it for a flow that genuinely cannot fit on one page."),
    anatomy=anatomy(timeline(), [("4%", "14%"), ("30%", "14%"), ("30%", "62%")],
                    [("Completed segment", "3px ink bar; label default colour."), ("Current segment", "3px <code>--color-brand</code> bar; <code>aria-current=\"step\"</code>."),
                     ("Label and date", "Bold step name over a tabular date; upcoming steps have no date.")]),
    variants=ex(timeline("Shipped"), "Order timeline, Shipped.") + ex(stepper(1), "Numbered stepper (core). Completed steps show a check."),
    sizes=NA("One size; the timeline fills its container in four equal columns."),
    states=matrix(["Complete", "Current", "Upcoming"],
                  [("Timeline step", ['<ol class="timeline" style="grid-template-columns: 1fr;" aria-label="Complete"><li data-done><b>Paid</b><span>Thu 22 Oct</span></li></ol>',
                                      '<ol class="timeline" style="grid-template-columns: 1fr;" aria-label="Current"><li aria-current="step"><b>Shipped</b><span>Fri 23 Oct</span></li></ol>',
                                      '<ol class="timeline" style="grid-template-columns: 1fr;" aria-label="Upcoming"><li><b>Delivered</b><span></span></li></ol>']),
                   ("Stepper step", ['<ol class="stepper" aria-label="Complete step"><li data-complete><span>Photos</span></li></ol>',
                                     '<ol class="stepper" aria-label="Current step"><li aria-current="step"><span>Details</span></li></ol>',
                                     '<ol class="stepper" aria-label="Upcoming step"><li><span>Price</span></li></ol>'])], first="Variant")
    + p("Cancelled and refunded orders do not use an error step: the timeline is replaced by an " + comp("alert") + " that says what happened and when.")
    + "<h3>Both themes</h3>" + themes(timeline("Delivered")),
    responsive=ul("The timeline keeps four columns down to 320px; labels are short enough to fit.", "Below 768px the numbered stepper hides every label except the current step's, keeping the numbers."),
    theming=p("Upcoming bars <code>--color-border-default</code>, completed <code>--color-fg-default</code>, current <code>--color-brand</code>. Labels move from <code>--color-fg-muted</code> to default once reached."),
    accessibility=a11y(
        pattern="An ordered list with <code>aria-label=\"Order progress\"</code>; the current step has <code>aria-current=\"step\"</code>. Steps are not interactive.",
        keyboard="Not focusable; nothing to operate. Actions for the current step (Add tracking, Confirm receipt) are buttons below the timeline.",
        focus="None.", labelling="Step names are text; completed state is conveyed by the date and by list position, and <code>aria-current</code> marks the current step so colour is not the only cue.",
        contrast=[("Completed bar", "--color-fg-default", "--color-bg-surface", 3), ("Current bar", "--color-brand", "--color-bg-surface", 3), ("Upcoming label", "--color-fg-muted", "--color-bg-surface", 4.5)],
        motion="None.", touch="Not interactive."),
    content=ul("Step names are the order statuses members see elsewhere: Paid, Shipped, Delivered, Completed.", "Dates as <i>Fri 23 Oct</i>; no times."),
    do_dont=dodont([("do", timeline("Shipped"), "Date each step that has happened."),
                    ("dont", '<ol class="timeline" aria-label="Bad"><li data-done><a href="#"><b>Paid</b></a></li><li aria-current="step"><a href="#"><b>Shipped</b></a></li><li><b>Delivered</b></li><li><b>Completed</b></li></ol>', "Make steps links; the timeline reports status, it does not navigate."),
                    ("do", stepper(2, "Do stepper"), "Use the numbered stepper only for a genuinely multi-page form."),
                    ("dont", stepper(0, "Dont stepper"), "Add a stepper to the one-page sell form; its sections already show progress.")]),
    tokens=token_table([("Upcoming / completed / current bar", "--color-border-default / --color-fg-default / --color-brand"), ("Labels", "--color-fg-muted / --color-fg-default"),
                        ("Bar thickness", "--border-width-accent"), ("Gap", "--space-2"), ("Stepper current", "--color-accent / --color-fg-on-accent"), ("Stepper complete", "--color-success-fg")]),
    code=pre("""
<ol class="timeline" aria-label="Order progress">
  <li data-done><b>Paid</b><span>Thu 22 Oct</span></li>
  <li aria-current="step"><b>Shipped</b><span>Fri 23 Oct</span></li>
  <li><b>Delivered</b><span></span></li>
  <li><b>Completed</b><span></span></li>
</ol>""")
    + classes([("<code>.timeline</code>", "Four-column order progress."), ("<code>data-done</code>", "Completed step."), ("<code>aria-current=\"step\"</code>", "Current step."),
               ("<code>.stepper</code>", "Numbered form stepper."), ("<code>data-complete</code>", "Completed stepper step (check mark).")]),
    sources=sources([("pages/order-detail/default", "Shipped"), ("pages/order-detail/paid", "Paid"), ("pages/order-detail/completed", "all done"), ("pages/sale-detail/default", "seller's view")]),
)


# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
component(
    "footer", "Footer", "Navigation",
    lead="The quiet end of every member page: the small logo, the policy links and the copyright.",
    pills=["<code>&lt;footer&gt;</code> landmark"],
    summary_variants="simple",
    summary_states="link default, hover, focus",
    overview=p("The footer holds what members look for rarely but must always find: <i>Marketplace rules</i>, <i>Privacy</i>, <i>Terms</i> and <i>Cookie settings</i> (which opens the cookie dialog). "
               "It sits 96px below the content. Admin screens and auth screens have no footer; dialogs never do."),
    anatomy=anatomy(footer_html(), [("4%", "30%"), ("40%", "30%"), ("88%", "30%")],
                    [("Logo", "Small (18px) logo linking home."), ("Footer nav", "<code>&lt;nav aria-label=\"Footer\"&gt;</code>, links underline on hover."), ("Copyright", "<i>© 2026 12L</i>.")]),
    variants=ex(footer_html(), "The only variant. Multi-column footers are not part of 12L."),
    sizes=NA("One size."),
    states=state_matrix(["Default", "Hover", "Focus"], [("Footer link", lambda s: f'<footer class="footer" style="margin: 0; padding: 0; border: 0;"><a href="#"{_st(s)}>Privacy</a></footer>')], first="Element")
    + "<h3>Both themes</h3>" + themes(footer_html()),
    responsive=ul("The three parts wrap onto separate lines below about 600px; links wrap with 8px row and 24px column gaps.", "Padding follows <code>--layout-margin</code>."),
    theming=p("Text <code>--color-fg-muted</code> on the canvas, a hairline <code>--color-border-default</code> top edge. Links inherit the muted colour."),
    accessibility=a11y(
        pattern="A <code>&lt;footer&gt;</code> (contentinfo) landmark containing a <code>&lt;nav aria-label=\"Footer\"&gt;</code>.",
        keyboard=[(kbd("Tab"), "Logo, then each link."), (kbd("Enter"), "Follows the link; Cookie settings opens the dialog.")],
        focus="Shared focus ring.", labelling="The footer nav is labelled <i>Footer</i> so it is distinct from <i>Primary</i>.",
        contrast=[("Footer text", "--color-fg-muted", "--color-bg-canvas", 4.5)], motion="None.",
        touch="Links are text with 8px / 24px gaps; on phones each wraps onto its own row for a larger target."),
    content=ul("Policy page names exactly as their headings.", "Copyright as <i>© 2026 12L</i>; no “All rights reserved”."),
    do_dont=dodont([("do", footer_html(), "Keep it to policy links."),
                    ("dont", '<footer class="footer" style="margin: 0;"><nav aria-label="Bad footer"><a href="#">Shoes</a><a href="#">Tops</a><a href="#">Sell</a><a href="#">Sign out</a></nav></footer>', "Repeat the primary navigation or put actions in the footer.")]),
    tokens=token_table([("Text / links", "--color-fg-muted"), ("Top edge", "--color-border-default"), ("Space above", "--space-24"), ("Padding", "--space-10 / --layout-margin"), ("Font", "--text-body-sm")]),
    code=pre("""
<footer class="footer">
  <a class="logo logo--sm" href="/" aria-label="12L home">…</a>
  <nav aria-label="Footer"><a href="/rules">Marketplace rules</a><a href="/privacy">Privacy</a><a href="/terms">Terms</a><a href="#cookies">Cookie settings</a></nav>
  <span>© 2026 12L</span>
</footer>""") + classes([("<code>.footer</code>", "Footer row, muted, wraps."), ("<code>.logo--sm</code>", "Small logo.")]),
    sources=sources([("pages/catalog/default", "member footer"), ("pages/privacy/default", "policy page"), ("dialogs/cookie-settings/default", "opened from Cookie settings")]),
)


# ---------------------------------------------------------------------------
# Skip link
# ---------------------------------------------------------------------------
def skip(state: str = "") -> str:
    return f'<div class="ds-skip-frame"><a class="skip-link" href="#main"{_st(state) if state else ""}>Skip to content</a><span class="text-sm text-muted">Page content</span></div>'


component(
    "skip-link", "Skip link", "Navigation",
    lead="The first thing a keyboard user reaches on every page: one link that jumps past the top bar to the main content.",
    pills=["WCAG 2.4.1 Bypass blocks"],
    summary_variants="one",
    summary_states="hidden, focused",
    overview=p("Every 12L page, including auth and admin screens, starts with <code>&lt;a class=\"skip-link\" href=\"#main\"&gt;Skip to content&lt;/a&gt;</code>. It is off screen until it receives keyboard focus, then slides into the top-left corner above everything (<code>--z-tooltip</code>)."),
    anatomy=anatomy(skip("focus"), [("8%", "20%")], [("Link", "Raised surface, <code>--shadow-3</code>, 8px × 16px padding, appears at 16px from the top-left.")]),
    variants=NA("There is one skip link per page, always to #main."),
    sizes=NA("One size."),
    states=matrix(["Hidden", "Focused"], [("Skip link", [skip(), skip("focus")])], first="Element")
    + p("Hidden means positioned above the viewport (not <code>display: none</code>), so it stays in the tab order.")
    + "<h3>Both themes</h3>" + themes(skip("focus")),
    responsive=ul("Same on every breakpoint; it overlays the top bar rather than pushing it down."),
    theming=p("<code>--color-bg-surface-raised</code> with <code>--color-fg-default</code> and <code>--shadow-3</code>, so it stands off the top bar in both themes."),
    accessibility=a11y(
        pattern="A same-page link to <code>&lt;main id=\"main\"&gt;</code>. The target needs no <code>tabindex</code> in modern browsers; focus and the reading position move to main.",
        keyboard=[(kbd("Tab"), "First press on page load focuses and reveals it."), (kbd("Enter"), "Moves to the main content; the next Tab continues from there.")],
        focus="The shared ring plus the slide-in; the link is fully visible while focused (2.4.11 Focus not obscured).",
        labelling="Visible text <i>Skip to content</i>.",
        contrast=[("Link text on raised surface", "--color-fg-link", "--color-bg-surface-raised", 4.5)],
        motion="Slides in over <code>--duration-fast</code>; instant under reduced motion.", touch="Not used by touch; 40px tall when visible."),
    content=ul("Always <i>Skip to content</i>."),
    do_dont=dodont([("do", skip("focus"), "Make it the first focusable element, visible on focus."),
                    ("dont", '<a class="visually-hidden" href="#main">Skip to content</a>', "Hide it permanently with <code>.visually-hidden</code>; sighted keyboard users then cannot see where focus went.")]),
    tokens=token_table([("Background / text", "--color-bg-surface-raised / --color-fg-default"), ("Shadow", "--shadow-3"), ("Offset", "--space-4"), ("Layer", "--z-tooltip"), ("Transition", "--duration-fast")]),
    code=pre("""
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="topbar">…</header>
  <main id="main">…</main>
</body>""") + classes([("<code>.skip-link</code>", "Off-screen until <code>:focus-visible</code>."), ("<code>data-state=\"focus\"</code>", "Documentation only: shows it revealed.")]),
    sources=sources([("pages/catalog/default", "first element"), ("pages/sign-in/default", "auth shell"), ("pages/audit-log/default", "admin shell")]),
)
