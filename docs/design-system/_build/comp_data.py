"""Data display: table, list, description list, avatar, badge, chip, stat."""
from ds import *

ST6 = ["Default", "Hover", "Focus", "Active", "Disabled"]


def _ds(state: str) -> str:
    """data-state attribute for a forced pointer/focus state."""
    return f' data-state="{state}"' if state in ("hover", "focus", "active") else ""


def _thumb(key: str, lg: bool = False) -> str:
    return f'<div class="thumb{" thumb--lg" if lg else ""}">{photo(key, tag=False, alt="")}</div>'


def _item_row(key: str, meta: str, lg: bool = False) -> str:
    it = ITEMS[key]
    return (f'<div class="item-row">{_thumb(key, lg)}<div class="item-row__body"><span class="item-row__title">{esc(it["title"])}</span>'
            f'<span class="item-row__meta">{meta}</span></div></div>')


def _status(label: str) -> str:
    mod = {"Draft": "draft", "Active": "active", "Reserved": "reserved", "Sold": "sold", "Removed": "removed", "Paid": "info",
           "Shipped": "info", "Delivered": "info", "Completed": "active", "Cancelled": "removed", "Refunded": "removed",
           "Open": "reserved", "Suspended": "removed", "Pending": "reserved"}[label]
    return f'<span class="status status--{mod}">{label}</span>'


# ===========================================================================
# Table
# ===========================================================================
AUDIT = [("Today 11:20", "Ana Ruiz", "Member suspended", "vintage_lou", "Repeated wrong-size listings"),
         ("Today 11:05", "Ana Ruiz", "Problem resolved: refund", "P-0912", "Hole by the left cuff, not disclosed"),
         ("Today 10:42", "Ana Ruiz", "Listing removed", "L-20802", "Label shows men's M"),
         ("Sat 24 Oct 16:18", "Ana Ruiz", "Report dismissed", "R-3290", "Photos match the listing")]
AUDIT_HEAD = '<thead><tr><th scope="col">Time (ET)</th><th scope="col">Administrator</th><th scope="col">Action</th><th scope="col">Target</th><th scope="col">Reason</th></tr></thead>'


def _audit_rows(rows=AUDIT, attrs=("",) * 4) -> str:
    return "".join(f'<tr{a}><td class="nowrap">{t}</td><td>{w}</td><td>{act}</td><td><code>{tg}</code></td><td>{r}</td></tr>'
                   for (t, w, act, tg, r), a in zip(rows, attrs))


def _audit(caption="Administrator actions, newest first", rows=AUDIT, attrs=("",) * 4, cls="table", hidden_caption=True) -> str:
    cap = f'<caption{" class=\"visually-hidden\"" if hidden_caption else ""}>{caption}</caption>'
    return f'<div class="table-wrap"><table class="{cls}">{cap}{AUDIT_HEAD}<tbody>{_audit_rows(rows, attrs)}</tbody></table></div>'


RULES_TABLE = ('<div class="table-wrap"><table class="table"><caption class="visually-hidden">Accepted categories and sizes</caption>'
               '<thead><tr><th scope="col">Category</th><th scope="col">Includes</th><th scope="col">Size</th></tr></thead><tbody>'
               f'<tr><th scope="row">Shoes</th><td>Sneakers, Boots, Dress shoes, Sandals</td><td>{size_tag("US 12")}</td></tr>'
               f'<tr><th scope="row">Tops</th><td>Shirts, T-shirts, Sweaters, Hoodies</td><td>{size_tag("L")}</td></tr>'
               f'<tr><th scope="row">Outerwear</th><td>Jackets, Coats</td><td>{size_tag("L")}</td></tr></tbody></table></div>')

PAYOUTS = [("12L-48302", "Reverse Weave hoodie, grey", "$45.00", "$4.50", "$40.50", "Pending"),
           ("12L-47511", "Tech Fleece shorts", "$37.00", "$3.70", "$33.30", "Paid")]


def _payouts(sort="descending", selected=None, actions=True, hover_row=None) -> str:
    th_sort = f'<th scope="col" aria-sort="{sort}"><button type="button">Order</button></th>'
    head = (f'<thead><tr><th scope="col"><span class="visually-hidden">Select</span></th>{th_sort}<th scope="col">Item</th>'
            '<th scope="col" class="num">Sale</th><th scope="col" class="num">Fee</th><th scope="col" class="num">You earn</th><th scope="col">Status</th>'
            + ('<th scope="col"><span class="visually-hidden">Actions</span></th>' if actions else "") + "</tr></thead>")
    body = ""
    for i, (o, item, sale, fee, net, stt) in enumerate(PAYOUTS):
        sel = ' aria-selected="true"' if selected == i else ""
        hv = ' data-state="hover"' if hover_row == i else ""
        chk = f'<input type="checkbox" id="pay-sel-{sort}-{i}"{" checked" if selected == i else ""} aria-label="Select order {o}">'
        act = (f'<td><span class="row-actions">{btn("", "ghost icon sm", icon="more", attrs=f"aria-label=\"More actions for order {o}\"")}</span></td>' if actions else "")
        body += (f'<tr{sel}{hv}><td><label class="choice">{chk}</label></td><td><code>{o}</code></td><td>{item}</td><td class="num">{sale}</td>'
                 f'<td class="num">{fee}</td><td class="num">{net}</td><td>{_status(stt)}</td>{act}</tr>')
    return (f'<div class="table-wrap"><table class="table"><caption>Payout history, newest first</caption>{head}<tbody>{body}</tbody></table></div>')


SKELETON_ROWS = "".join('<tr>' + "".join('<td><span class="skeleton skeleton--text"></span></td>' for _ in range(5)) + '</tr>' for _ in range(3))
LOADING_TABLE = (f'<div class="table-wrap" aria-busy="true"><table class="table"><caption class="visually-hidden">Loading audit log</caption>{AUDIT_HEAD}'
                 f'<tbody>{SKELETON_ROWS}</tbody></table></div>')
EMPTY_TABLE = ('<div class="table-wrap"><div class="empty empty--compact"><div class="empty__icon">' + ic("list", "icon icon--lg") +
               '</div><h3 class="empty__title">No actions match L-99999</h3><p class="empty__text">Check the ID or clear the search to see the full log.</p>'
               '<div class="empty__actions">' + btn("Clear search") + '</div></div></div>')
ERROR_TABLE = ('<div class="table-wrap"><div class="empty empty--compact empty--error"><div class="empty__icon">' + ic("alert", "icon icon--lg") +
               '</div><h3 class="empty__title">The audit log did not load</h3><p class="empty__text">Nothing was changed. Try again in a moment.</p>'
               '<div class="empty__actions">' + btn("Try again", icon="refresh") + '</div></div></div>')


def _row_state(state: str) -> str:
    one = [AUDIT[0]]
    if state == "selected":
        return f'<table class="table"><caption class="visually-hidden">Row {state}</caption><tbody><tr aria-selected="true"><td>{one[0][0]}</td><td>{one[0][2]}</td></tr></tbody></table>'
    attr = _ds(state)
    return f'<table class="table"><caption class="visually-hidden">Row {state}</caption><tbody><tr{attr}><td>{one[0][0]}</td><td>{one[0][2]}</td></tr></tbody></table>'


component(
    "table", "Table", "Data display",
    lead="Tables compare records across the same columns: the admin audit log, payout history, the accepted sizes in the marketplace rules.",
    pills=["Native <code>&lt;table&gt;</code>"],
    summary_variants="default, dense, sortable, selectable with row actions, row headers",
    summary_states="row hover, focus, selected; loading (skeleton rows), empty, error",
    overview=p("Use a table when people read across columns to compare values: when an action happened, who did it, to what and why. "
               f"Use a {comp('list')} when each record is read on its own (orders, listings, reports), and a {comp('description-list')} for one record's facts.")
    + ul("<b>Default</b> is the admin audit log: five text columns, newest first, sticky sunken header.",
         "<b>Row headers</b> (<code>&lt;th scope=\"row\"&gt;</code>) name each row when the first column is the key, as in the rules page's category table.",
         "<b>Sortable</b> columns put a button in the header and set <code>aria-sort</code>.",
         "<b>Selectable</b> rows add a checkbox column and <code>aria-selected</code>; row actions sit in a last, unlabelled column.",
         "12L is mostly read on phones, so tables are reserved for admin and reference content. Member-facing collections are lists."),
    anatomy=anatomy(
        '<div style="width: 100%;">' + _audit(rows=AUDIT[:2]) + "</div>",
        [("4%", "14%"), ("4%", "48%"), ("40%", "48%"), ("2%", "84%")],
        [("Container", "<code>.table-wrap</code>: 1px <code>--color-border-default</code>, <code>--radius-lg</code>, surface background, horizontal scroll."),
         ("Header cell", "Sunken background, <code>--text-label</code> in muted ink, sticky to the top of the scroll area, never wraps."),
         ("Body cell", "<code>--text-body-sm</code>, 12px × 16px padding, 1px divider between rows; numbers right-aligned with tabular figures."),
         ("Caption", "Names the table for screen readers; visually hidden when the page heading already says it.")]),
    variants=p("Choose the smallest variant that does the job. Every variant keeps a real <code>&lt;caption&gt;</code> and scoped headers.")
    + "<h3>Default (audit log)</h3>" + ex(_audit(), "Five columns, newest first. The target ID is code so it can be copied exactly.")
    + "<h3>Row headers (rules)</h3>" + ex(RULES_TABLE, "The first column is a <code>&lt;th scope=\"row\"&gt;</code>; it reads as a label, not as a second header.")
    + "<h3>Sortable, selectable, with row actions</h3>"
    + ex(_payouts(), "Sorted by order, newest first. Money columns are right-aligned. Row actions appear on hover and focus, and always on touch screens."),
    sizes=p("Default cells are 12px × 16px (<code>--space-3</code> × <code>--space-4</code>). Dense (<code>.table--dense</code>, 8px × 12px) is for admin screens that need more rows on one screen; it is never used for member-facing data.")
    + ex(_audit(rows=AUDIT[:2], cls="table table--dense", caption="Dense audit log"), "<code>.table--dense</code>"),
    states=p("Row states apply to the whole row. Hover and focus are forced here with <code>data-state</code>; selection uses <code>aria-selected=\"true\"</code>.")
    + state_matrix(["Default", "Hover", "Focus", "Selected"], [("Row", _row_state)], first="Part")
    + "<h3>Table states</h3>"
    + table(["State", "What shows"], [
        ["Loading", "The header renders immediately with three skeleton rows; the wrapper sets <code>aria-busy=\"true\"</code>."],
        ["Empty / no results", "A compact " + comp("empty-state") + " inside the wrapper that says what was searched and how to clear it."],
        ["Error", "A compact error empty state with <i>Try again</i>; nothing about the data is implied."],
        ["Sorted", "<code>aria-sort=\"ascending|descending\"</code> on the sorted header; the arrow follows."]])
    + ex(LOADING_TABLE, "Loading: header plus skeleton rows (pages/audit-log/loading).", show_code=False)
    + ex(EMPTY_TABLE, "No results for a search (pages/audit-log/no-results).", show_code=False)
    + ex(ERROR_TABLE, "Error (pages/audit-log/error).", show_code=False)
    + "<h3>Both themes</h3>" + themes(_audit(rows=AUDIT[:2], attrs=(' aria-selected="true"', ""))),
    responsive=ul("The wrapper scrolls horizontally below the table's natural width; the page never scrolls sideways. Header cells never wrap, body cells do.",
                  "Below 640px keep at most four columns visible; move secondary columns (Administrator, Fee) into the row's detail page rather than squeezing them.",
                  "Member-facing records (orders, listings, payouts on phones) use a " + comp("list") + " instead of a table; the payout table is the desktop view.",
                  "Row actions are always visible on touch devices (<code>@media (hover: none)</code>), because hover never happens there."),
    theming=p("The table reads <code>--color-bg-surface</code> for cells, <code>--color-bg-surface-sunken</code> for headers, <code>--color-border-default</code> for rules, "
              "<code>--color-bg-subtle</code> for row hover and <code>--color-accent-subtle</code> for selected rows. In dark the surface is <code>--palette-ink-900</code> and the header drops to the sunken ink, so the header still reads as a separate band.")
    + pre("""
/* An embedded table on a sunken panel keeps its own surface: */
.panel--sunken .table-wrap { background: var(--color-bg-surface); }"""),
    accessibility=a11y(
        pattern="A native <code>&lt;table&gt;</code> with <code>&lt;caption&gt;</code>, <code>&lt;thead&gt;</code> and <code>scope</code> on every header cell. No grid role: the table is read, not navigated cell by cell. Sortable headers contain a real <code>&lt;button&gt;</code> and the <code>&lt;th&gt;</code> carries <code>aria-sort</code>.",
        keyboard=[(kbd("Tab"), "Moves through the interactive things in the table only: sort buttons, row checkboxes, links and row actions, in reading order."),
                  (kbd("Enter") + " / " + kbd("Space"), "On a sort button, toggles ascending and descending; on a checkbox, selects the row."),
                  ("Screen-reader table keys", "Move by cell and announce the column and row headers, because every header has a scope.")],
        focus="Each control inside a row shows the standard ring. Row actions that are hidden until hover become visible on <code>:focus-within</code>, so keyboard users never tab to an invisible button.",
        labelling="The caption names the table (<i>Administrator actions, newest first</i>). The checkbox and actions columns have visually hidden header text. Each row checkbox and action button names its record: <i>Select order 12L-48302</i>, <i>More actions for order 12L-48302</i>.",
        contrast=[("Header text on sunken", "--color-fg-muted", "--color-bg-surface-sunken", 4.5), ("Cell text on surface", "--color-fg-default", "--color-bg-surface", 4.5),
                  ("Cell text on hovered row", "--color-fg-default", "--color-bg-subtle", 4.5), ("Cell text on selected row", "--color-fg-default", "--color-accent-subtle", 4.5)],
        motion="Row actions fade in over <code>--duration-fast</code>; nothing else moves. Reduced motion removes the fade.",
        touch="Sort buttons and row checkboxes keep a 24px minimum target; row action buttons are 32px (<code>.btn--sm</code>) with 8px around them."),
    content=ul("Column headers are nouns in sentence case: <i>Time (ET)</i>, <i>Action</i>, <i>You earn</i>. Put the unit or time zone in the header, not in every cell.",
               "Dates follow the 12L format: <i>Today 11:20</i>, <i>Sat 24 Oct 16:18</i>. Money always has cents in tables: <i>$40.50</i>.",
               "IDs (<i>L-20802</i>, <i>12L-48302</i>, <i>R-3290</i>) are shown exactly, in code style, never shortened.",
               "Reasons are one sentence fragment without a full stop: <i>Photos match the listing</i>.",
               "Empty cells show an em dash (—), never blank and never <i>N/A</i>."),
    do_dont=dodont([
        ("do", RULES_TABLE, "Mark the key column as row headers so every cell is announced with its category."),
        ("dont", '<div class="table-wrap"><table class="table"><caption class="visually-hidden">Categories</caption><tbody><tr><td><b>Shoes</b></td><td>' + size_tag("US 12") + '</td></tr><tr><td><b>Tops</b></td><td>' + size_tag("L") + '</td></tr></tbody></table></div>',
         "Bold body cells instead of headers. Screen readers lose the relationship between row and value."),
        ("do", '<ul class="order-list" role="list"><li><a href="#">' + _item_row("iron-ranger", "from vintage_lou · Thu 22 Oct") + '<span class="order-list__end"><span class="price">$244.97</span>' + _status("Shipped") + '</span></a></li></ul>',
         "Show a member's purchases as a list: one record per row, readable at 360px."),
        ("dont", '<div class="table-wrap"><table class="table"><caption class="visually-hidden">Purchases</caption><thead><tr><th scope="col">Item</th><th scope="col">Seller</th><th scope="col">Date</th><th scope="col" class="num">Total</th><th scope="col">Status</th></tr></thead><tbody><tr><td>Iron Ranger 8111 boots</td><td>vintage_lou</td><td>Thu 22 Oct</td><td class="num">$244.97</td><td>Shipped</td></tr></tbody></table></div>',
         "A five-column table for member purchases. On a phone it scrolls sideways and hides the status."),
    ]),
    tokens=token_table([("Cell background", "--color-bg-surface"), ("Header background", "--color-bg-surface-sunken"), ("Header text", "--color-fg-muted"),
                        ("Row divider and frame", "--color-border-default"), ("Row hover", "--color-bg-subtle"), ("Selected row", "--color-accent-subtle"),
                        ("Cell padding", "--space-3 / --space-4"), ("Dense padding", "--space-2 / --space-3"), ("Frame radius", "--radius-lg"),
                        ("Body font", "--text-body-sm"), ("Header font", "--text-label"), ("Header stacking", "--z-base"), ("Row actions fade", "--duration-fast")]),
    code=pre("""
<div class="table-wrap">
  <table class="table">
    <caption class="visually-hidden">Administrator actions, newest first</caption>
    <thead><tr><th scope="col">Time (ET)</th><th scope="col">Action</th><th scope="col">Target</th></tr></thead>
    <tbody>
      <tr><td class="nowrap">Today 11:20</td><td>Member suspended</td><td><code>vintage_lou</code></td></tr>
    </tbody>
  </table>
</div>""")
    + classes([("<code>.table-wrap</code>", "Frame, radius and horizontal scroll."), ("<code>.table</code>", "Base table."),
               ("<code>.table--dense</code>", "Admin-only compact cells."), ("<code>td.num</code>, <code>th.num</code>", "Right-aligned tabular numbers (money, counts)."),
               ("<code>td.nowrap</code>", "Keeps dates and IDs on one line."), ("<code>th[aria-sort] &gt; button</code>", "Sortable header; arrow follows <code>aria-sort</code>."),
               ("<code>tr[aria-selected=\"true\"]</code>", "Selected row."), ("<code>.row-actions</code>", "Wrapper that reveals row actions on hover and focus."),
               ("<code>.table-wrap[aria-busy=\"true\"]</code>", "Loading with skeleton rows."), ("<code>data-state=\"hover|focus\"</code> on <code>tr</code>", "Documentation only.")]),
    sources=sources([("pages/audit-log/default", "admin audit log"), ("pages/audit-log/loading", "skeleton rows"), ("pages/audit-log/no-results", "search with no matches"),
                     ("pages/audit-log/error", "error state"), ("pages/rules/default", "category table with row headers"), ("pages/payouts/default", "payout history the sortable variant is drawn from")],
                    "row headers inherited the sunken column-header style; the audit log put <code>.num</code> (right-aligned figures) on text columns and inline <code>white-space</code> on dates. The system adds a body row-header style and <code>.nowrap</code>."),
)
drift("pages/rules/default", "Row headers (th scope=row) in the category table picked up the column-header style: sunken background, muted label, sticky.",
      "Added .table tbody th as a plain label cell in components.css.")
drift("pages/audit-log/default", "Time and Target cells used .num (tabular, right-aligned intent) on text, plus inline style white-space: nowrap.",
      "Added .nowrap; .num is reserved for numbers. Target IDs are shown as code.")


# ===========================================================================
# List
# ===========================================================================
def _order_li(key, meta, total, stt, attr=""):
    return (f'<li><a href="#"{attr}>{_item_row(key, meta)}<span class="order-list__end"><span class="price">{total}</span>{_status(stt)}</span></a></li>')


ORDERS = ('<ul class="order-list" role="list">'
          + _order_li("iron-ranger", "from vintage_lou · Thu 22 Oct", "$244.97", "Shipped")
          + _order_li("better-sweater", "from vintage_lou · Mon 19 Oct", "$55.00", "Delivered")
          + _order_li("samba-og", "from jaybird · Tue 6 Oct", "$78.00", "Completed") + "</ul>")

SETTINGS = ('<ul class="settings-list"><li><div class="settings-list__body"><span class="settings-list__title">Email</span><span class="settings-list__meta">marcus.bell@example.com</span></div></li>'
            '<li><div class="settings-list__body"><span class="settings-list__title">Password</span><span class="settings-list__meta">Changed Tue 2 Jun</span></div>' + btn("Change", href="#") + '</li>'
            '<li><div class="settings-list__body"><span class="settings-list__title">Sessions</span><span class="settings-list__meta">Signed in on 2 devices</span></div>' + btn("Sign out everywhere", href="#") + '</li></ul>')

QUEUE = ('<ul class="queue" role="list"><li><a href="#"><div style="flex: 1 1 16rem; min-width: 0;">' + _item_row("bedale", "Listing · Wrong size") + '</div>'
         '<div class="cluster"><span class="badge badge--warning">Hidden</span><span class="pill-count" aria-label="3 reporters">3</span><span class="text-sm text-muted">2 days</span></div></a></li>'
         '<li><a href="#"><div style="flex: 1 1 16rem; min-width: 0;">' + _item_row("better-sweater", "Order problem · Not as described · Order 12L-48140") + '</div>'
         '<div class="cluster"><span class="badge badge--info">Payout held</span><span class="text-sm text-muted">1 day</span></div></a></li></ul>')

SIMPLE = ('<ul class="list" role="list"><li class="list__item"><div class="list__body"><div class="list__title">Report R-3318 · wrong size</div><div class="list__meta">Bedale waxed jacket · 2 days ago</div></div>' + _status("Open") + '</li>'
          '<li class="list__item"><div class="list__body"><div class="list__title">Problem P-0912 · not as described</div><div class="list__meta">Order 12L-48140 · yesterday</div></div>' + _status("Open") + '</li></ul>')

RULES = ('<ol class="rules-list" role="list"><li><span class="settings-list__title">Only two sizes</span><span class="settings-list__meta">Men’s US 12 shoes and men’s L clothing. The label must say so.</span></li>'
         '<li><span class="settings-list__title">18 and over</span><span class="settings-list__meta">One account to buy and sell. No approval step.</span></li></ol>')


def _list_state(state):
    if state == "disabled":
        return '<ul class="list" role="list"><li><a class="list__item list__item--interactive" href="#" aria-disabled="true"><div class="list__body"><div class="list__title">Report R-3318</div><div class="list__meta">Closed</div></div></a></li></ul>'
    if state == "selected":
        return '<ul class="list" role="list"><li><a class="list__item list__item--interactive" href="#" aria-current="page"><div class="list__body"><div class="list__title">Report R-3318</div><div class="list__meta">Bedale waxed jacket</div></div></a></li></ul>'
    return f'<ul class="list" role="list"><li><a class="list__item list__item--interactive" href="#"{_ds(state)}><div class="list__body"><div class="list__title">Report R-3318</div><div class="list__meta">Bedale waxed jacket</div></div></a></li></ul>'


def _order_state(state):
    if state in ("disabled", "selected"):
        return '<span class="text-muted text-sm">—</span>'
    return '<ul class="order-list" role="list" style="min-width: 16rem;">' + _order_li("iron-ranger", "Thu 22 Oct", "$244.97", "Shipped", _ds(state)) + "</ul>"


component(
    "list", "List", "Data display",
    lead="Lists show one record per row: purchases and sales, listings, account settings, the moderation queue, the marketplace rules.",
    pills=["<code>&lt;ul role=\"list\"&gt;</code>"],
    summary_variants="simple, order list (item rows), settings list, queue, rules (numbered); item row",
    summary_states="default, hover, focus, active, selected (current), disabled",
    overview=p(f"Lists are 12L's main way to show collections outside the catalog grid. Each row is read on its own, so they work at 360px where a {comp('table')} would not. "
               f"The {comp('listing-card')} grid is for browsing items; lists are for managing them.")
    + ul("<b>Order list</b> (<code>.order-list</code>): a whole-row link with an <b>item row</b> (thumbnail, title, meta) and an end column with price and status. Purchases, sales, my listings, payouts.",
         "<b>Settings list</b> (<code>.settings-list</code>): a title, a current value and one action per row. Account settings, email preferences.",
         "<b>Queue</b> (<code>.queue</code>): the admin moderation queue; an order-list row that wraps and carries a badge, a reporter count and the age.",
         "<b>Simple list</b> (<code>.list</code>): title and meta with an optional trailing status; open reports on a member's admin page.",
         "<b>Rules</b> (<code>.rules-list</code>): a numbered <code>&lt;ol&gt;</code> of title and explanation."),
    anatomy=anatomy('<div style="width: 100%;">' + '<ul class="order-list" role="list">' + _order_li("iron-ranger", "from vintage_lou · Thu 22 Oct", "$244.97", "Shipped") + "</ul></div>",
                    [("4%", "40%"), ("22%", "28%"), ("22%", "62%"), ("88%", "28%"), ("84%", "64%")],
                    [("Thumbnail", "<code>.thumb</code>: 56px square photo (80px with <code>.thumb--lg</code>), decorative <code>alt=\"\"</code> because the title names the item."),
                     ("Title", "<code>.item-row__title</code>: <code>--text-label</code> at 16px, truncates with an ellipsis."),
                     ("Meta", "<code>.item-row__meta</code>: who and when, <code>--text-body-sm</code> muted, joined with a middle dot."),
                     ("Amount", f"A {comp('price')} with cents, tabular figures."),
                     ("Status", f"A {comp('badge')} status: square dot plus word.")]),
    variants="<h3>Order list</h3>" + ex(ORDERS, "Purchases: the whole row links to the order.")
    + "<h3>Settings list</h3>" + ex(SETTINGS, "One action per row, at the end; the action wraps under the text on narrow screens.")
    + "<h3>Queue</h3>" + ex(QUEUE, "Admin queue: badge, reporter count, age. The row wraps below 640px.")
    + "<h3>Simple list</h3>" + ex(SIMPLE, "Open reports on a member's admin page.")
    + "<h3>Rules</h3>" + ex(RULES, "Numbered rules: an ordered list, title plus one sentence."),
    sizes=p("Rows have one height per variant, set by their padding: order list and queue 20px (<code>--space-5</code>) top and bottom, settings 24px (<code>--space-6</code>), simple list 12px. "
            "Thumbnails come in two sizes: 56px (<code>.thumb</code>) in order and queue rows, 80px (<code>.thumb--lg</code>) in my listings where the photo identifies a draft.")
    + ex('<ul class="order-list" role="list" style="width: 100%;"><li><a href="#">' + _item_row("detroit-jacket", "Active · listed 2 days ago") + '<span class="order-list__end"><span class="price">$95</span></span></a></li>'
         '<li><a href="#">' + _item_row("detroit-jacket", "Active · listed 2 days ago", lg=True) + '<span class="order-list__end"><span class="price">$95</span></span></a></li></ul>',
         "<code>.thumb</code> (56px) and <code>.thumb--lg</code> (80px)."),
    states=p("Interactive rows are links, so they get link states. Hover underlines the title; focus draws the ring around the whole row; the current record in a master list uses <code>aria-current=\"page\"</code>.")
    + state_matrix(ST6 + ["Selected"], [("Simple list", _list_state), ("Order list", _order_state)])
    + "<h3>Both themes</h3>" + themes(ORDERS),
    responsive=ul("Item rows never wrap the title; it truncates. The end column (price, status) stays on the right at every width.",
                  "Queue rows wrap at 640px: the item row takes the first line, badge, count and age the second.",
                  "Settings rows wrap their action under the text when the row is narrower than 16rem of text plus the button.",
                  "Lists are full width inside <code>.page--form</code> (44rem max) so long lines stay readable on desktop."),
    theming=p("Lists read <code>--color-border-default</code> for dividers, <code>--color-fg-muted</code> for meta and <code>--color-bg-subtle</code> for hover on simple lists. They have no surface of their own: they sit on the canvas or inside a " + comp("card") + ". Photos keep their light studio backdrop in dark."),
    accessibility=a11y(
        pattern="<code>&lt;ul role=\"list\"&gt;</code> (the role restores list semantics that Safari drops when <code>list-style: none</code>), or <code>&lt;ol&gt;</code> for ordered rules. Interactive rows are one <code>&lt;a&gt;</code> each; a row with its own action (settings) is not itself a link.",
        keyboard=[(kbd("Tab"), "Moves from row link to row link, or to each row's action in a settings list."),
                  (kbd("Enter"), "Opens the record."),
                  ("Screen-reader list keys", "Announce the item count (<i>list, 3 items</i>) and move item by item.")],
        focus="The whole row link gets the standard focus ring with a 2px offset, so the thumbnail and status are inside it.",
        labelling="The row link's name is its text: title, meta, price and status read in order. Thumbnails are <code>alt=\"\"</code>. Counts that are only numbers carry an <code>aria-label</code> (<i>3 reporters</i>).",
        contrast=[("Title on canvas", "--color-fg-default", "--color-bg-canvas", 4.5), ("Meta on canvas", "--color-fg-muted", "--color-bg-canvas", 4.5),
                  ("Meta on hovered row", "--color-fg-muted", "--color-bg-subtle", 4.5), ("Shipped status on canvas", "--color-info-fg", "--color-bg-canvas", 4.5)],
        motion="None. Hover changes the underline or background instantly.",
        touch="Order and queue rows are at least 80px tall; settings actions are 40px buttons."),
    content=ul("Titles are the item's title as listed, never rewritten: <i>Iron Ranger 8111 boots</i>.",
               "Meta answers who and when, joined with a middle dot: <i>from vintage_lou · Thu 22 Oct</i>.",
               "Settings meta shows the current value, not a description: <i>Changed Tue 2 Jun</i>, <i>Signed in on 2 devices</i>.",
               "Drafts without a title say so: <i>Untitled draft · Tops</i>; a missing price is an em dash."),
    do_dont=dodont([
        ("do", ORDERS.replace(_order_li("better-sweater", "from vintage_lou · Mon 19 Oct", "$55.00", "Delivered"), "").replace(_order_li("samba-og", "from jaybird · Tue 6 Oct", "$78.00", "Completed"), ""),
         "One link per row; price and status at the end where the eye checks them."),
        ("dont", '<ul class="list" role="list"><li class="list__item"><div class="list__body"><div class="list__title">Iron Ranger 8111 boots</div></div>' + btn("View", "sm") + btn("Track", "sm") + btn("Report", "sm") + '</li></ul>',
         "Three buttons on every row. Open the order; actions live on the order page."),
        ("do", RULES, "Rules in an ordered list styled by the list class."),
        ("dont", '<ol class="rules-list" role="list"><li class="settings-list__body" style="padding-block: var(--space-5); border-bottom: 1px solid var(--color-border-default);"><span class="settings-list__title">Only two sizes</span></li></ol>',
         "Inline padding and borders on each item (as the rules mock did). Use <code>.rules-list</code>; it carries the rhythm."),
    ]),
    tokens=token_table([("Divider", "--color-border-default"), ("Title", "--color-fg-default"), ("Meta", "--color-fg-muted"), ("Hover (simple list)", "--color-bg-subtle"),
                        ("Current row", "--color-accent-subtle"), ("Row padding: order / settings / simple", "--space-5 / --space-6 / --space-3"),
                        ("Thumb to text gap", "--space-4"), ("Title font", "--text-label"), ("Meta font", "--text-body-sm")]),
    code=pre("""
<ul class="order-list" role="list">
  <li><a href="/orders/12L-48213">
    <div class="item-row">
      <div class="thumb"><div class="photo photo--1"><img src="boot.svg" alt=""></div></div>
      <div class="item-row__body"><span class="item-row__title">Iron Ranger 8111 boots</span>
        <span class="item-row__meta">from vintage_lou · Thu 22 Oct</span></div>
    </div>
    <span class="order-list__end"><span class="price">$244.97</span><span class="status status--info">Shipped</span></span>
  </a></li>
</ul>""")
    + classes([("<code>.order-list</code> + <code>.order-list__end</code>", "Linked rows with an end column."), ("<code>.item-row</code>, <code>__body</code>, <code>__title</code>, <code>__meta</code>", "Thumbnail plus text block used inside rows, summaries and dialogs."),
               ("<code>.thumb</code>, <code>.thumb--lg</code>", "56px / 80px square photo."), ("<code>.settings-list</code>, <code>__body</code>, <code>__title</code>, <code>__meta</code>", "Setting rows with one action."),
               ("<code>.queue</code>", "Admin queue rows that wrap."), ("<code>.list</code>, <code>.list__item</code>, <code>--interactive</code>", "Simple list; interactive items are links."),
               ("<code>.rules-list</code>", "Numbered rules (added during extraction)."), ("<code>aria-current=\"page\"</code>", "Current record in a master list.")]),
    sources=sources([("pages/purchases/default", "order list"), ("pages/my-listings/default", "item rows with large thumbs and drafts"), ("pages/settings/default", "settings list"),
                     ("pages/moderation-queue/default", "queue"), ("pages/member-admin/default", "simple list of open reports"), ("pages/rules/default", "numbered rules")],
                    "the rules list styled each item inline and reused <code>.settings-list__body</code>; the system adds <code>.rules-list &gt; li</code>."),
)
drift("pages/rules/default", "Each rules-list item carried inline padding-block and border-bottom (with a raw 1px) and borrowed .settings-list__body.",
      "Added .rules-list > li with the same rhythm; the inline styles can be dropped.")


# ===========================================================================
# Description list
# ===========================================================================
FACTS = ('<dl class="facts"><dt>Size</dt><dd>Men\'s US 12</dd><dt>Category</dt><dd>Shoes · Sneakers</dd><dt>Condition</dt><dd>Used - Excellent</dd>'
         '<dt>Listed</dt><dd><time datetime="2026-10-25">2 hours ago</time></dd></dl>')
DL = ('<dl class="dl"><dt>Member</dt><dd>vintage_lou</dd><dt>Email</dt><dd>lou.ferreira@example.com</dd><dt>Joined</dt><dd>Jun 2025</dd><dt>Status</dt><dd>' + _status("Active") + '</dd></dl>')
FACTS_ROW = ('<div class="facts-row" style="width: 100%;"><span class="text-muted text-sm">USPS tracking</span><a href="#" class="num">9400 1118 9922 3456 7890 12'
             + ic("external", "icon icon--sm") + '<span class="visually-hidden"> (opens USPS tracking)</span></a></div>')

component(
    "description-list", "Description list", "Data display",
    lead="Key–value pairs for one record: a listing's facts, a member's account details, an order's tracking number.",
    pills=["Native <code>&lt;dl&gt;</code>"],
    summary_variants="facts (listing detail), dl (admin), facts row (one pair, split)",
    summary_states="static",
    overview=p(f"Use a description list when a record has a handful of named attributes that are read one by one. For many records with the same attributes use a {comp('table')}; for money that adds up use the {comp('order-summary')}.")
    + ul("<b>Facts</b> (<code>.facts</code>): the listing detail block. Muted term column sized to its longest term, 12px × 32px gaps.",
         "<b>Dl</b> (<code>.dl</code>): the generic two-column list for admin and account detail. Label-style terms.",
         "<b>Facts row</b> (<code>.facts-row</code>): a single pair spread across the row between rules, for a value that must stand out, such as a tracking number."),
    anatomy=anatomy('<div style="width: 100%; max-width: 22rem;">' + FACTS + "</div>", [("2%", "14%"), ("44%", "14%")],
                    [("Term", "<code>&lt;dt&gt;</code>: <code>--text-body-sm</code> in <code>--color-fg-muted</code>, column as wide as the longest term."),
                     ("Description", "<code>&lt;dd&gt;</code>: body text in the default colour; may hold a link, a time or a status.")]),
    variants="<h3>Facts</h3>" + ex(FACTS, "Listing detail facts. Dates use <code>&lt;time&gt;</code>.")
    + "<h3>Dl</h3>" + ex(DL, "Generic list with label-style terms.")
    + "<h3>Facts row</h3>" + ex(FACTS_ROW, "A single important pair; the external link says where it goes."),
    sizes=NA("Description lists take the type size of their context; spacing is fixed per variant."),
    states=p("Description lists are static. The only interactive content is a link inside a <code>&lt;dd&gt;</code>, which takes the " + comp("link") + " states.")
    + "<h3>Both themes</h3>" + themes(FACTS + "<br>" + FACTS_ROW),
    responsive=ul("The two columns stay side by side down to 320px because terms are short (<i>Size</i>, <i>Listed</i>). A term longer than three words means the list is the wrong component.",
                  "Facts rows wrap the value under the term when they do not fit; long tracking numbers break anywhere (<code>overflow-wrap: anywhere</code>).",
                  "On listing detail the facts sit in the sticky info column from 1024px."),
    theming=p("Terms read <code>--color-fg-muted</code>, values <code>--color-fg-default</code>, facts-row rules <code>--color-border-default</code>. No surface of its own."),
    accessibility=a11y(
        pattern="A native <code>&lt;dl&gt;</code> with <code>&lt;dt&gt;</code>/<code>&lt;dd&gt;</code> pairs. Screen readers announce <i>description list, 4 items</i> and pair each term with its value. A facts row is a plain two-span row because it holds one pair.",
        keyboard="No keyboard interaction of its own; links inside values are in the normal tab order.",
        focus="Links inside values show the standard ring.",
        labelling="Terms label their values. External links add visually hidden text (<i>opens USPS tracking</i>) next to the external icon.",
        contrast=[("Term on canvas", "--color-fg-muted", "--color-bg-canvas", 4.5), ("Term on surface", "--color-fg-muted", "--color-bg-surface", 4.5), ("Value on canvas", "--color-fg-default", "--color-bg-canvas", 4.5)],
        motion="None.",
        touch="Links inside values are inline text; tracking links get the full line height as their target."),
    content=ul("Terms are one or two words, sentence case, no colon: <i>Size</i>, <i>Member since</i>.",
               "Sizes are written in full in facts: <i>Men's US 12</i>; conditions use the listing scale: <i>Used - Excellent</i>.",
               "Relative times (<i>2 hours ago</i>) carry an absolute <code>datetime</code>."),
    do_dont=dodont([
        ("do", FACTS, "Short terms, muted; values in full."),
        ("dont", '<p>Size: Men\'s US 12<br>Category: Shoes · Sneakers<br>Condition: Used - Excellent</p>', "Pairs written as a paragraph with colons. Screen readers cannot pair them and the values do not line up."),
        ("do", FACTS_ROW, "One important value gets its own row."),
        ("dont", '<dl class="facts"><dt>The tracking number for this shipment from USPS</dt><dd>9400 1118 9922 3456 7890 12</dd></dl>', "A sentence as a term squeezes the value column."),
    ]),
    tokens=token_table([("Term", "--color-fg-muted"), ("Value", "--color-fg-default"), ("Facts gaps", "--space-3 / --space-8"), ("Dl gaps", "--space-2 / --space-6"),
                        ("Facts row rules", "--color-border-default"), ("Facts row padding", "--space-4"), ("Term font (facts / dl)", "--text-body-sm / --text-label")]),
    code=pre("""
<dl class="facts">
  <dt>Size</dt><dd>Men's US 12</dd>
  <dt>Listed</dt><dd><time datetime="2026-10-25">2 hours ago</time></dd>
</dl>""")
    + classes([("<code>.facts</code>", "Listing facts: muted body-sm terms."), ("<code>.dl</code>", "Generic list: label-style terms."), ("<code>.facts-row</code>", "One pair spread between top and bottom rules.")]),
    sources=sources([("pages/listing-detail/default", "facts"), ("pages/order-detail/default", "tracking facts row"), ("pages/sale-detail/shipped", "facts row on the seller side")],
                    "none. <code>.dl</code> exists in the kit but no mock used it yet; it is kept for admin detail."),
)


# ===========================================================================
# Avatar
# ===========================================================================
def _av(handle, cls=""):
    return f'<span class="avatar {cls}" aria-hidden="true">{PEOPLE[handle]["initials"]}</span>'


def _av_state(state):
    if state == "disabled":
        return '<span class="text-muted text-sm">—</span>'
    return f'<a class="avatar avatar--sm" href="#" aria-label="Your account, Marcus Bell"{_ds(state)}>MB</a>'


GROUP = ('<div class="avatar-group" role="img" aria-label="Seen by kicks_12, vintage_lou, jaybird and 2 others">' + _av("kicks_12", "avatar--sm") + _av("vintage_lou", "avatar--sm")
         + _av("jaybird", "avatar--sm") + '<span class="avatar avatar--sm avatar--more" aria-hidden="true">+2</span></div>')

component(
    "avatar", "Avatar", "Data display",
    lead="A member's initials in a small square block: next to a seller's name, in the top bar as the account link, large on profiles.",
    pills=["Initials only"],
    summary_variants="initials, account link, group with overflow, with status dot",
    summary_states="default, hover, focus, active (as link)",
    overview=p("12L has no profile photos: members are identified by handle, and the avatar is their initials on <code>--color-accent-subtle</code>. Square with 2px corners, like every other 12L block.")
    + ul("<b>Decorative</b> next to a name (seller block, reviews, admin pages): <code>aria-hidden=\"true\"</code>, because the name is right there.",
         "<b>Account link</b> in the top bar: an <code>&lt;a&gt;</code> with <code>aria-label=\"Your account, Marcus Bell\"</code>.",
         "<b>Group</b>: overlapping avatars with a <i>+2</i> overflow block and one label for the group.",
         "<b>Status dot</b>: a green dot for <i>online now</i>, always repeated in text nearby."),
    anatomy=anatomy('<span class="avatar avatar--lg" aria-hidden="true">DO</span>', [("52%", "20%"), ("40%", "72%")],
                    [("Initials", "Two letters from the real name, <code>--text-label</code> scaled with the size."), ("Block", "Square, <code>--radius-sm</code>, <code>--color-accent-subtle</code> background.")]),
    variants=ex(_av("kicks_12") + '<a class="avatar avatar--sm" href="#" aria-label="Your account, Marcus Bell">MB</a>' + GROUP
                + '<span class="avatar-wrap">' + _av("jaybird") + '<span class="dot dot--success" aria-hidden="true"></span></span><span class="text-sm text-muted">jaybird · online now</span>',
                "Decorative, account link, group, with status dot (and its text)."),
    sizes=ex(_av("marcus_12", "avatar--sm") + _av("marcus_12") + _av("marcus_12", "avatar--lg") + _av("marcus_12", "avatar--xl"),
             "32px top bar and reviews · 40px seller block · 56px · 96px profile header (initials in <code>--text-h2</code>)."),
    states=p("Only the account-link avatar is interactive.")
    + state_matrix(ST6, [("Account link", _av_state)])
    + "<h3>Both themes</h3>" + themes('<div class="cluster">' + _av("kicks_12") + _av("vintage_lou", "avatar--lg") + GROUP + "</div>"),
    responsive=ul("The profile header avatar stays 96px; the header wraps the name and stats under it below 640px.",
                  "The top-bar account avatar is 32px at every width and sits last in the actions."),
    theming=p("Background <code>--color-accent-subtle</code>, initials <code>--color-fg-accent</code>. In dark both flip to ink-800 with paper initials. Groups ring each avatar with <code>--color-bg-surface</code> so overlaps stay readable.")
    + pre(".seller .avatar { --color-accent-subtle: var(--color-bg-subtle); } /* quieter block on a busy surface */"),
    accessibility=a11y(
        pattern="A <code>&lt;span&gt;</code> with <code>aria-hidden=\"true\"</code> when a name is adjacent; an <code>&lt;a&gt;</code> with an <code>aria-label</code> when it is the only link to the account; <code>role=\"img\"</code> with a label on a group.",
        keyboard=[(kbd("Tab"), "Reaches the account avatar link; decorative avatars are skipped."), (kbd("Enter"), "Opens the account.")],
        focus="The standard focus ring around the 32px block.",
        labelling="Account link: <i>Your account, Marcus Bell</i>. Groups: one label listing the names and the overflow count. Status dots are never the only signal.",
        contrast=[("Initials on avatar block", "--color-fg-accent", "--color-accent-subtle", 4.5), ("Initials on hovered block", "--color-fg-accent", "--color-accent-subtle-hover", 4.5)],
        motion="None.",
        touch="The 32px account link has 8px around it in the top bar; it is above the 24px minimum."),
    content=ul("Initials come from the member's real name (<i>MB</i> for Marcus Bell), never from the handle; show the handle beside it.",
               "Overflow says the exact count: <i>+2</i>."),
    do_dont=dodont([
        ("do", '<div class="seller">' + _av("kicks_12") + '<div><a href="#" class="seller__name">kicks_12</a><div class="seller__meta">141 sales · Atlanta, GA</div></div></div>', "Decorative avatar next to the linked handle."),
        ("dont", '<a class="avatar" href="#" aria-label="kicks_12">DO</a><a href="#">kicks_12</a>', "Two links to the same profile side by side; the avatar link adds a tab stop with nothing new."),
        ("do", '<span class="avatar-wrap">' + _av("jaybird") + '<span class="dot dot--success" aria-hidden="true"></span></span><span class="text-sm">online now</span>', "Status dot plus text."),
        ("dont", '<span class="avatar-wrap">' + _av("jaybird") + '<span class="dot dot--success" aria-hidden="true"></span></span>', "A dot alone; colour is the only signal."),
    ]),
    tokens=token_table([("Block", "--color-accent-subtle"), ("Initials", "--color-fg-accent"), ("Hover (link)", "--color-accent-subtle-hover"), ("Group ring", "--color-bg-surface"),
                        ("Radius", "--radius-sm"), ("Initials font", "--text-label"), ("XL initials font", "--text-h2"), ("Group overlap", "--space-2")]),
    code=pre("""
<span class="avatar" aria-hidden="true">DO</span>
<a class="avatar avatar--sm" href="/account" aria-label="Your account, Marcus Bell">MB</a>""")
    + classes([("<code>.avatar</code>", "40px block."), ("<code>.avatar--sm</code> <code>--lg</code> <code>--xl</code>", "32 / 56 / 96px."), ("<code>.avatar-group</code>", "Overlapping group."),
               ("<code>.avatar--more</code>", "Overflow block (added during extraction)."), ("<code>.avatar-wrap</code> + <code>.dot</code>", "Status dot (added during extraction).")]),
    sources=sources([("pages/listing-detail/default", "seller block"), ("pages/catalog/default", "top-bar account link"), ("pages/profile/default", "XL profile avatar"),
                     ("pages/member-admin/default", "admin member header")],
                    "the top-bar account link set <code>text-decoration: none</code> inline; the system styles <code>a.avatar</code>."),
)


# ===========================================================================
# Badge (and status)
# ===========================================================================
BADGES = ('<span class="badge">New seller</span><span class="badge badge--info">Payout held</span><span class="badge badge--success">Verified</span>'
          '<span class="badge badge--warning">Hidden</span><span class="badge badge--danger">Suspended</span>')
STATUSES = "".join(_status(s) for s in ["Draft", "Active", "Reserved", "Sold", "Paid", "Shipped", "Completed", "Refunded", "Removed"])
COUNTS = ('<span class="badge badge--solid">Admin view</span><span class="badge badge--count" aria-label="4 new reports">4</span>'
          '<span class="pill-count" aria-label="3 reporters">3</span>')

component(
    "badge", "Badge", "Data display",
    lead="Badges and statuses label a record's state in a word: New seller, Hidden, Shipped, Sold. They are never buttons.",
    pills=["Text, not colour alone"],
    summary_variants="badge neutral/info/success/warning/danger, solid, count; status (order and listing); pill count",
    summary_states="static",
    overview=p("12L uses two forms. Pick by where the label sits:")
    + ul("<b>Status</b> (<code>.status</code>): a square dot and a word in the status colour, no background. Order and listing lifecycle in lists and headers: <i>Active</i>, <i>Reserved</i>, <i>Sold</i>, <i>Shipped</i>, <i>Refunded</i>.",
         "<b>Badge</b> (<code>.badge</code>): an uppercase tag on a tinted block, for attributes and moderation flags: <i>New seller</i>, <i>Hidden</i>, <i>Payout held</i>.",
         "<b>Solid</b> and <b>count</b> badges carry a filled background for counts and admin markers; <b>pill count</b> is the neutral square count in the moderation queue.")
    + p(f"Neither is interactive. A filter you can toggle is a {comp('chip')}; a message is an {comp('alert')}."),
    anatomy=anatomy('<span class="badge badge--warning">Hidden</span>&nbsp;&nbsp;' + _status("Shipped"), [("10%", "34%"), ("30%", "34%"), ("68%", "34%")],
                    [("Dot", "6px round on badges, 8px square on statuses; <code>currentColor</code>."), ("Badge label", "<code>--text-overline</code>, uppercase, wide tracking, on the tone's <code>-bg</code>."),
                     ("Status label", "<code>--text-body-sm</code> in the tone's <code>-fg</code>, sentence case.")]),
    variants="<h3>Badge tones</h3>" + ex(BADGES, "Neutral, info, success, warning, danger.")
    + "<h3>Statuses</h3>" + ex(STATUSES, "Every order and listing status in the mocks. Paid, Shipped and Delivered share info; Completed shares success with Active.")
    + "<h3>Solid, count and pill count</h3>" + ex(COUNTS, "Counts carry an <code>aria-label</code> that says what is counted.")
    + table(["Status", "Tone", "Used for"], [["Draft", "muted", "Unpublished listings"], ["Active, Completed", "success", "Live listings; orders closed normally"],
                                             ["Reserved, Open", "warning", "Checkout in progress; open reports and problems"], ["Sold", "default ink", "Sold listings"],
                                             ["Paid, Shipped, Delivered", "info", "Orders in progress"], ["Removed, Cancelled, Refunded, Suspended", "danger", "Ended by a person or a rule"]]),
    sizes=NA("Badges and statuses have one size each; they take the caption and body-sm sizes of the rows they sit in."),
    states=p("Badges are static: no hover, focus or disabled state. Their tone is their state. Both forms in both themes:")
    + themes(f'<div class="stack stack--sm"><div class="cluster">{BADGES}</div><div class="cluster">{STATUSES}</div><div class="cluster">{COUNTS}</div></div>'),
    responsive=ul("Badges never wrap (<code>white-space: nowrap</code>); keep labels to two words.",
                  "In order lists the status sits under the price in the end column at every width; in the queue it wraps to the second line with the count."),
    theming=p("Each tone reads its status set: <code>--color-{tone}-bg</code> and <code>--color-{tone}-fg</code> for badges, <code>--color-{tone}-fg</code> for statuses. "
              "In dark the backgrounds become deep tints (<code>--palette-green-950</code>) and the text lightens (<code>--palette-green-300</code>), so the pairs stay above 7:1."),
    accessibility=a11y(
        pattern="Plain text in a <code>&lt;span&gt;</code>. No role: the word is the information, and the dot is decoration. A count badge gets an <code>aria-label</code>.",
        keyboard="Not focusable.",
        focus="Not focusable; a badge inside a link is part of that link's name.",
        labelling="The label text is read as part of its row (<i>Iron Ranger 8111 boots … $244.97 Shipped</i>). Count-only badges say what they count: <i>3 reporters</i>.",
        contrast=[("Info badge", "--color-info-fg", "--color-info-bg", 4.5), ("Success badge", "--color-success-fg", "--color-success-bg", 4.5),
                  ("Warning badge", "--color-warning-fg", "--color-warning-bg", 4.5), ("Danger badge", "--color-danger-fg", "--color-danger-bg", 4.5),
                  ("Reserved status on canvas", "--color-warning-fg", "--color-bg-canvas", 4.5), ("Active status on canvas", "--color-success-fg", "--color-bg-canvas", 4.5),
                  ("Count badge", "--color-fg-on-danger", "--color-danger-solid", 4.5), ("Solid badge", "--color-fg-on-accent", "--color-info-solid", 4.5)],
        motion="None.",
        touch="Not a target."),
    content=ul("One or two words. Statuses are past participles or adjectives in sentence case: <i>Shipped</i>, <i>Reserved</i>. Badges are nouns or adjectives: <i>New seller</i>, <i>Hidden</i>.",
               "Use the same word for the same state everywhere: an order is <i>Completed</i> in purchases, sales and admin.",
               "Never put an action in a badge (<i>Click to verify</i>)."),
    do_dont=dodont([
        ("do", _status("Reserved") + _status("Sold"), "A status word with its dot."),
        ("dont", '<span class="dot" style="color: var(--color-warning-fg);" aria-hidden="true"></span>', "A coloured dot with no word; colour is the only signal."),
        ("do", '<span class="pill-count" aria-label="3 reporters">3</span>', "A count with an aria-label saying what it counts."),
        ("dont", '<span class="badge badge--danger">Report this listing</span>', "An action dressed as a badge. Use a link or a button."),
    ]),
    tokens=token_table([("Neutral badge", "--color-bg-subtle / --color-fg-muted"), ("Info", "--color-info-bg / --color-info-fg"), ("Success", "--color-success-bg / --color-success-fg"),
                        ("Warning", "--color-warning-bg / --color-warning-fg"), ("Danger", "--color-danger-bg / --color-danger-fg"),
                        ("Count", "--color-danger-solid / --color-fg-on-danger"), ("Solid", "--color-info-solid / --color-fg-on-accent"),
                        ("Badge font", "--text-overline"), ("Status font", "--text-body-sm"), ("Badge radius", "--radius-sm"), ("Tracking", "--letter-spacing-wide")]),
    code=pre("""
<span class="badge badge--warning">Hidden</span>
<span class="status status--info">Shipped</span>
<span class="pill-count" aria-label="3 reporters">3</span>""")
    + classes([("<code>.badge</code> + <code>--info|--success|--warning|--danger</code>", "Tinted uppercase tag."), ("<code>.badge--solid</code>, <code>.badge--count</code>", "Filled marker; count without dot."),
               ("<code>.status</code> + <code>--draft|--active|--reserved|--sold|--info|--removed</code>", "Lifecycle word with square dot."), ("<code>.pill-count</code>", "Neutral square count.")]),
    sources=sources([("pages/my-listings/default", "listing statuses"), ("pages/purchases/default", "order statuses"), ("pages/moderation-queue/default", "badges and reporter count"),
                     ("pages/listing-detail/new-seller", "New seller badge")]),
)


# ===========================================================================
# Chip
# ===========================================================================
def _chip(label, state="", selected=False, remove=False, cls=""):
    attrs = ' aria-pressed="true"' if selected else ' aria-pressed="false"'
    st = {"hover": ' data-state="hover"', "focus": ' data-state="focus"', "active": ' data-state="active"', "disabled": " disabled"}.get(state, "")
    if remove:
        return (f'<span class="chip {cls}">{esc(label)}<button class="remove" type="button" aria-label="Remove filter {esc(label)}">{ic("close", "icon icon--sm")}</button></span>')
    return f'<button class="chip {cls}" type="button"{attrs}{st}>{esc(label)}</button>'


FILTERS = _chip("Shoes", remove=True) + _chip("New with tags", remove=True) + _chip("$20–$200", remove=True) + btn("Clear all", "link sm")

component(
    "chip", "Chip", "Data display",
    lead="Chips show the filters applied to the catalog and let the member remove one at a time, or toggle a quick filter on and off.",
    pills=["<code>aria-pressed</code>"],
    summary_variants="filter (toggle), applied filter (removable), small",
    summary_states="default, hover, focus, active, disabled, selected (pressed)",
    overview=p(f"Use chips for filter values a member can see and undo at a glance. Choosing one option from a set inside a form is a {comp('radio-group')} or a {comp('button-group')}; a read-only label is a {comp('badge')}.")
    + ul("<b>Applied filter</b>: ink chip with a labelled remove button; the row ends with <i>Clear all</i>. Catalog toolbar after filtering.",
         "<b>Filter toggle</b>: a <code>&lt;button aria-pressed&gt;</code> that turns a quick filter on and off (<i>Free shipping</i>)."),
    anatomy=anatomy(_chip("New with tags", remove=True), [("30%", "20%"), ("78%", "20%")],
                    [("Label", "The filter value as the member chose it, <code>--text-label</code>."), ("Remove button", "20px round hit area inside the chip, labelled <i>Remove filter New with tags</i>.")]),
    variants="<h3>Applied filters</h3>" + ex(FILTERS, "Each chip removes one filter; Clear all removes every one.")
    + "<h3>Filter toggles</h3>" + ex(_chip("Free shipping", selected=True) + _chip("Under $50") + _chip("New with tags"), "Pressed chips are ink; unpressed are outlined."),
    sizes=ex(_chip("Under $50") + _chip("Under $50", cls="chip--sm"), "Default 32px (<code>--control-height-sm</code>); small 24px (<code>.chip--sm</code>) for dense admin filters only."),
    states=state_matrix(ST6 + ["Selected"], [
        ("Toggle", lambda s: _chip("Free shipping", state=s, selected=(s == "selected"))),
        ("Toggle, pressed", lambda s: _chip("Free shipping", state=s, selected=True) if s != "selected" else '<span class="text-muted text-sm">—</span>')])
    + "<h3>Both themes</h3>" + themes('<div class="cluster">' + FILTERS + _chip("Under $50", selected=True) + _chip("Free shipping") + "</div>"),
    responsive=ul("The chip row wraps; it never scrolls sideways, so every applied filter stays visible.",
                  "Below 1024px the filters live in the filter sheet, and the applied chips stay on the catalog toolbar above the grid.",
                  "<i>Clear all</i> appears once two or more filters are applied."),
    theming=p("Component tokens <code>--chip-bg</code>, <code>--chip-fg</code> and <code>--chip-border</code> alias surface, default text and strong border; pressed chips switch to <code>--color-accent</code> with <code>--color-fg-on-accent</code>. In dark a pressed chip is paper with ink text, like the primary button."),
    accessibility=a11y(
        pattern="Toggle chips are <code>&lt;button type=\"button\" aria-pressed&gt;</code>. Applied-filter chips are a <code>&lt;span&gt;</code> holding a real remove <code>&lt;button&gt;</code>; the chip itself is not focusable.",
        keyboard=[(kbd("Tab"), "Moves to each toggle chip, or to each chip's remove button."), (kbd("Space") + " / " + kbd("Enter"), "Toggles the chip, or removes the filter."),
                  ("After removal", "Focus moves to the next chip's remove button, or to <i>Clear all</i>, or to the toolbar heading when none remain; the result count is announced politely.")],
        focus="Standard focus ring on the chip (toggle) or on the remove button.",
        labelling="Remove buttons say what they remove: <i>Remove filter Shoes</i>. Toggles are named by their label; the pressed state is announced by <code>aria-pressed</code>.",
        contrast=[("Label on chip", "--color-fg-default", "--color-bg-surface", 4.5), ("Chip edge", "--color-border-strong", "--color-bg-surface", 3),
                  ("Label on pressed chip", "--color-fg-on-accent", "--color-accent", 4.5), ("Label on hovered chip", "--color-fg-default", "--color-bg-subtle", 4.5)],
        motion="Background changes over <code>--duration-fast</code>.",
        touch="Default chips are 32px tall; small chips (24px) meet the minimum and are admin-only. The remove button's 20px icon area sits inside the 32px chip."),
    content=ul("Labels repeat the filter value exactly: <i>New with tags</i>, <i>$20–$200</i> (en dash for ranges).",
               "No category prefix unless two filters could share a value (<i>Shoes</i>, not <i>Category: Shoes</i>)."),
    do_dont=dodont([
        ("do", FILTERS, "Each applied filter removable, plus Clear all."),
        ("dont", '<span class="chip" aria-pressed="true">Shoes<button class="remove" type="button" aria-label="Remove">' + ic("close", "icon icon--sm") + '</button></span>', "A remove button labelled just <i>Remove</i>: with three chips, which one?"),
        ("do", _chip("Free shipping", selected=True), "A toggle chip uses <code>aria-pressed</code>."),
        ("dont", '<span class="chip" aria-pressed="true">Free shipping</span>', "A span with aria-pressed (the catalog mock's applied chips): not focusable, so the state cannot be changed. Make it a button, or give it a remove button."),
    ]),
    tokens=token_table([("Background", "--color-bg-surface"), ("Label", "--color-fg-default"), ("Border", "--color-border-strong"), ("Hover", "--color-bg-subtle"),
                        ("Pressed background / label", "--color-accent / --color-fg-on-accent"), ("Height", "--control-height-sm"), ("Padding", "--space-3"),
                        ("Radius", "--radius-sm"), ("Font", "--text-label"), ("Transition", "--duration-fast")]),
    code=pre("""
<span class="chip">Shoes
  <button class="remove" type="button" aria-label="Remove filter Shoes"><svg class="icon icon--sm" aria-hidden="true">…</svg></button>
</span>
<button class="chip" type="button" aria-pressed="true">Free shipping</button>""")
    + classes([("<code>.chip</code>", "Base chip."), ("<code>.chip .remove</code>", "Remove button inside an applied-filter chip."), ("<code>aria-pressed=\"true\"</code>", "Pressed toggle (ink)."),
               ("<code>.chip--sm</code>", "24px admin chip (added during extraction)."), ("<code>data-state</code>", "Documentation only.")]),
    sources=sources([("pages/catalog/filtered", "applied filters"), ("pages/catalog/category", "category chip"), ("pages/catalog/no-results", "filters that returned nothing")],
                    "applied-filter chips were spans carrying <code>aria-pressed=\"true\"</code>, which announces a toggle that cannot be focused."),
)
drift("pages/catalog/filtered", "Applied-filter chips were <span aria-pressed=\"true\">: a toggle state on an element that cannot take focus.",
      "Applied filters are plain chips with a labelled remove button; aria-pressed is only for <button> toggles.")


# ===========================================================================
# Stat
# ===========================================================================
def _stat(label, value, delta=""):
    return f'<div class="stat"><span class="stat__label">{label}</span><span class="stat__value">{value}</span>{delta}</div>'


ADMIN_STATS = '<div class="stats">' + _stat("Rating", "4.7") + _stat("Sales", "46") + _stat("Active listings", "4") + _stat("Open reports", "1") + "</div>"
PAYOUT_STATS = '<div class="stats">' + _stat("Paid out", "$33.30") + _stat("Pending", "$40.50") + "</div>"
EARN = '<p class="earnings"><span>You earn after the 10% fee</span><strong>$61.20</strong></p>'
LOADING_STATS = ('<div class="stats" aria-busy="true"><div class="stat"><span class="stat__label">Paid out</span><span class="skeleton skeleton--title" style="width: 6rem;"></span></div>'
                 '<div class="stat"><span class="stat__label">Pending</span><span class="skeleton skeleton--title" style="width: 6rem;"></span></div></div>')

component(
    "stat", "Stat", "Data display",
    lead="A labelled number that summarises something: payouts paid and pending, a seller's sales and rating, what the seller earns after the fee.",
    pills=["Tabular figures"],
    summary_variants="stat, stats row, with delta, earnings line",
    summary_states="default, loading",
    overview=p("Use a stat when one number answers a question the member came with (<i>How much is pending?</i>). Keep it to two to four per row; more is a " + comp("table") + ".")
    + ul("<b>Stats row</b> (<code>.stats</code>): wrapping row of stats; values in <code>--text-h3</code>. Profile, member admin, payouts.",
         "<b>Stat</b> on its own: value in <code>--text-h2</code>, optional delta (<code>.stat__delta--up|--down</code>) with arrow and sign.",
         "<b>Earnings</b> (<code>.earnings</code>): one line under the price field on the sell form: <i>You earn after the 10% fee — $61.20</i>."),
    anatomy=anatomy(_stat("Pending", "$40.50", '<span class="stat__delta stat__delta--up">↑ +$40.50 this week</span>'), [("10%", "8%"), ("10%", "42%"), ("10%", "80%")],
                    [("Label", "<code>--text-label</code>, muted, above the value."), ("Value", "<code>--text-h2</code> (or <code>--text-h3</code> in a row), tabular figures."),
                     ("Delta (optional)", "Arrow, sign and amount in success or danger text; never colour alone.")]),
    variants="<h3>Stats row</h3>" + ex(ADMIN_STATS, "Member admin: four stats.") + ex(PAYOUT_STATS, "Payouts.")
    + "<h3>With delta</h3>" + ex(_stat("Sales this month", "7", '<span class="stat__delta stat__delta--up">↑ +3 vs September</span>') + _stat("Open reports", "1", '<span class="stat__delta stat__delta--down">↑ +1 since Friday</span>'),
                                  "Up is not always good: an increase in reports is shown in danger.")
    + "<h3>Earnings</h3>" + ex(EARN, "Sell form: updates as the price changes.", stack=True),
    sizes=ex(_stat("Paid out", "$33.30") + '<div class="stats">' + _stat("Paid out", "$33.30") + "</div>", "Standalone value <code>--text-h2</code> (30px); in a stats row <code>--text-h3</code> (24px)."),
    states=table(["State", "Behaviour"], [["Default", "Label and value."], ["Loading", "The label renders; the value is a title skeleton; the row sets <code>aria-busy=\"true\"</code>."],
                                         ["Empty", "A value that does not exist yet reads <i>$0.00</i> or an em dash, never blank; payouts without history show an " + comp("empty-state") + " below."]])
    + ex(LOADING_STATS, "Loading (pages/payouts/loading).", show_code=False)
    + "<h3>Both themes</h3>" + themes(ADMIN_STATS + "<br>" + EARN),
    responsive=ul("Stats rows wrap with a 32px gap; at 360px a four-stat row becomes two rows of two.", "Values never truncate; shorten the label instead."),
    theming=p("Values read <code>--color-fg-default</code>, labels <code>--color-fg-muted</code>, deltas <code>--color-success-fg</code> and <code>--color-danger-fg</code>. Values use the display family through <code>--text-h2/h3</code>, the heavy numerals of the logo."),
    accessibility=a11y(
        pattern="Plain text: a label span and a value span inside a <code>&lt;div&gt;</code>. The label comes first in the DOM so it is read first. When a stats row is the main summary of a page, wrap it in a <code>&lt;dl&gt;</code>-like order (label then value) rather than value then label.",
        keyboard="Not interactive.",
        focus="Not focusable.",
        labelling="The label is adjacent and read first. Deltas include the sign and a unit in words or symbols (<i>+3 vs September</i>), and the arrow is text, not an icon only.",
        contrast=[("Label on canvas", "--color-fg-muted", "--color-bg-canvas", 4.5), ("Value on canvas", "--color-fg-default", "--color-bg-canvas", 4.5),
                  ("Up delta on canvas", "--color-success-fg", "--color-bg-canvas", 4.5), ("Down delta on canvas", "--color-danger-fg", "--color-bg-canvas", 4.5)],
        motion="Values change without animation; no counting-up effects.",
        touch="Not a target."),
    content=ul("Labels are short nouns in sentence case: <i>Paid out</i>, <i>Pending</i>, <i>Member since</i>.",
               "Money with cents and a dollar sign: <i>$40.50</i>. Counts as digits: <i>46</i>.",
               "Say what a derived number is derived from: <i>You earn after the 10% fee</i>."),
    do_dont=dodont([
        ("do", ADMIN_STATS, "Label above value, in the same order on every page."),
        ("dont", '<div class="stats"><div class="stat"><span class="stat__value">141</span><span class="stat__label">Sales</span></div><div class="stat"><span class="stat__label">Rating</span><span class="stat__value">4.7</span></div></div>',
         "Value-first on one page and label-first on another (profile versus member admin). Pick one order."),
        ("do", _stat("Open reports", "1", '<span class="stat__delta stat__delta--down">↑ +1 since Friday</span>'), "Delta with arrow, sign and context."),
        ("dont", _stat("Open reports", "1", '<span class="stat__delta stat__delta--down"></span>') , "A coloured value change with no text."),
    ]),
    tokens=token_table([("Label", "--color-fg-muted"), ("Value", "--color-fg-default"), ("Delta up / down", "--color-success-fg / --color-danger-fg"),
                        ("Value font (stat / stats row)", "--text-h2 / --text-h3"), ("Label font", "--text-label"), ("Label to value", "--space-1"), ("Row gap", "--space-8")]),
    code=pre("""
<div class="stats">
  <div class="stat"><span class="stat__label">Paid out</span><span class="stat__value">$33.30</span></div>
  <div class="stat"><span class="stat__label">Pending</span><span class="stat__value">$40.50</span></div>
</div>
<p class="earnings"><span>You earn after the 10% fee</span><strong>$61.20</strong></p>""")
    + classes([("<code>.stat</code>, <code>__label</code>, <code>__value</code>", "One stat."), ("<code>.stat__delta--up|--down</code>", "Change with arrow and sign."),
               ("<code>.stats</code>", "Wrapping row; values step down to h3."), ("<code>.earnings</code>", "Label and amount on one line.")]),
    sources=sources([("pages/member-admin/default", "stats row, label first"), ("pages/profile/default", "stats row, value first"), ("pages/payouts/default", "paid out and pending"),
                     ("pages/payouts/loading", "loading"), ("pages/sell/filled", "earnings line")],
                    "the profile put the value before the label while member admin put the label first; the system standard is label first."),
)
drift("pages/profile/default", "Stats put stat__value before stat__label; member-admin and payouts put the label first.",
      "Label first is the standard (read order and visual order agree); the profile markup should be reordered.")
