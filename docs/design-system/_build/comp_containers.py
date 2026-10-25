"""Containers and overlays: card, dialog, drawer, tooltip, divider, layout primitives."""
from ds import *


def _st(state: str) -> str:
    return {"default": "", "hover": ' data-state="hover"', "focus": ' data-state="focus"', "active": ' data-state="active"'}.get(state, "")


# ---------------------------------------------------------------------------
# Card
# ---------------------------------------------------------------------------
STAT = '<a class="panel stat" href="#" style="text-decoration: none; color: inherit;"{a}><span class="stat__value">3</span><span class="stat__label">Active listings</span></a>'
SUNKEN = ('<div class="panel panel--sunken stack"><h3 class="panel__title">How was jaybird?</h3><p class="text-muted text-sm">Your review stays hidden until jaybird reviews you too, or until Mon 16 Nov.</p>'
          f'<div>{btn("Leave a review", "primary", icon="star")}</div></div>')
CARD = ('<article class="card"><div class="card__header"><h3 class="card__title">Payout account</h3><span class="status status--active">Connected</span></div>'
        '<p class="text-muted">Payouts go to Chase checking ending 4417, two business days after an order completes.</p>'
        f'<div class="card__footer">{btn("Change account")}</div></article>')
TILE = f'<a class="category-tile" href="#"{{a}}><span class="category-tile__name">Shoes</span>{size_tag("US 12")}</a>'

component(
    "card", "Card", "Containers and overlays",
    lead="A bordered surface that groups related content: the order summary panel, the account stats, a payout account. 12L cards are square-cornered and mostly flat.",
    pills=["Panel, card, well, tile"],
    summary_variants="panel, panel sunken, card (with header/footer), interactive, selected, well, category tile",
    summary_states="default, hover, focus, selected",
    overview=p("12L leans on white space and hairlines rather than boxes, so most content sits straight on the canvas. Use a container only when content is a unit the member acts on as a whole:")
    + ul("<b>Panel</b> (<code>.panel</code>): the workhorse. Order and checkout summaries, account overview stats, the sell success summary. No shadow, no radius.",
         "<b>Sunken panel</b> (<code>.panel--sunken</code>): a quieter well for a prompt inside a page, such as <i>How was jaybird?</i> on a completed order.",
         "<b>Card</b> (<code>.card</code>): a raised unit with optional header and footer, for settings blocks and admin report cards. 4px radius and <code>--shadow-1</code>.",
         "<b>Interactive</b>: when the whole container is a link (account stats, category tiles), the container is the <code>&lt;a&gt;</code> and gets hover and focus states.",
         "<b>Well</b> (<code>.well</code>): rounded sunken area for code or fine print.")
    + p(f"Listings are not cards: they are {comp('listing-card')}s, photo first, no border."),
    anatomy=anatomy(CARD, [("6%", "12%"), ("80%", "12%"), ("6%", "48%"), ("6%", "80%")],
                    [("Header", "<code>.card__header</code>: title (h4) and an optional status or action."), ("Header aside", "Status, badge or ghost button, top-aligned."),
                     ("Body", "Any content; 24px padding all round."), ("Footer", "<code>.card__footer</code>: hairline top edge, actions right-aligned.")]),
    variants=ex('<div class="grid grid--auto" style="width: 100%;">' + STAT.format(a="") + SUNKEN + "</div>", "Panel as an account stat link, and a sunken prompt panel.", show_code=False)
    + ex(CARD, "Card with header, body and footer.")
    + ex(TILE.format(a="") + '<div class="well text-sm">Order reference 12L-48213 · placed Thu 22 Oct</div>', "Category tile and well."),
    sizes=p("Containers take the width of their grid cell. Padding is the only size: panels use 24px (<code>--space-6</code>) and 32px from 768px; cards use 24px; wells 16px.")
    + ex('<div class="panel" style="width: 100%;"><p class="text-sm">Panel padding: 24px, 32px from 768px.</p></div><div class="well" style="width: 100%;"><p class="text-sm">Well padding: 16px.</p></div>', "Padding by container.", show_code=False),
    states=state_matrix(["Default", "Hover", "Focus"],
                        [("Interactive card", lambda s: f'<a class="card card--interactive" href="#"{_st(s)} style="display: block; color: inherit; text-decoration: none;"><b>Sales</b><p class="text-sm text-muted">19 completed</p></a>'),
                         ("Stat panel", lambda s: STAT.format(a=_st(s))),
                         ("Category tile", lambda s: TILE.format(a=_st(s)))], first="Variant")
    + matrix(["Default", "Selected"], [("Card", ['<div class="card"><b>Ship to home</b></div>', '<div class="card card--selected" aria-selected="true"><b>Ship to home</b></div>'])])
    + p(f"Selection inside forms (shipping address, payout method) is the {comp('radio-group')} option card, which owns the real input; <code>.card--selected</code> is only for display.")
    + "<h3>Both themes</h3>" + themes('<div class="stack">' + CARD + SUNKEN + "</div>"),
    responsive=ul("Panels stack full width below 1024px; on order and checkout pages they become the right column (2fr of a 3fr/2fr split) from 1024px.",
                  "Panel padding grows from 24px to 32px at 768px.", "Category tiles are 2-up below 768px, 4-up above.",
                  "Never nest a card inside a card; use a divider or a sunken panel inside instead."),
    theming=p("Containers read <code>--color-bg-surface</code> and <code>--color-border-default</code>. In dark the surface is ink-900 on an ink-950 canvas, so a panel still reads as raised; sunken panels drop to ink-1000. "
              "Cards expose <code>--card-bg</code>, <code>--card-border</code>, <code>--card-shadow</code> and <code>--card-padding</code>.")
    + pre(".card--flat { --card-shadow: none; }  /* a card with no lift, e.g. inside a dialog */"),
    accessibility=a11y(
        pattern="A plain container: <code>&lt;div&gt;</code>, <code>&lt;section&gt;</code> with a heading, <code>&lt;article&gt;</code> for self-contained items, or <code>&lt;aside aria-label=\"Order summary\"&gt;</code> for complementary panels. A clickable container is a single <code>&lt;a&gt;</code> with all content inside; never a <code>div</code> with a click handler or a link nested in a link.",
        keyboard=[(kbd("Tab"), "Interactive containers are one tab stop; other containers are skipped, their own controls are reached in order."), (kbd("Enter"), "Follows an interactive container's link.")],
        focus="Interactive containers show the shared ring around the whole container.",
        labelling="Give section panels a heading or an <code>aria-label</code> (<i>Order summary</i>). A stat link's name is its content: <i>3 Active listings</i>.",
        contrast=[("Text on panel", "--color-fg-default", "--color-bg-surface", 4.5), ("Muted text in sunken panel", "--color-fg-muted", "--color-bg-surface-sunken", 4.5),
                  ("Selected edge", "--color-accent", "--color-bg-surface", 3)],
        motion="Interactive cards raise to <code>--shadow-2</code> and lift 1px over <code>--duration-fast</code>; removed under reduced motion.",
        touch="Interactive containers are far larger than 44px; keep only one target inside them."),
    content=ul("Panel titles are short labels in sentence case: <i>Order summary</i>, <i>Ship to</i>.", "Stat labels are plural nouns under the number: <i>Active listings</i>, <i>Completed sales</i>."),
    do_dont=dodont([("do", STAT.format(a=""), "Make the whole stat panel one link."),
                    ("dont", '<div class="panel stat"><span class="stat__value">3</span><span class="stat__label">Active listings</span><a href="#">View</a></div>', "Add a separate small link inside a panel that should itself be the link."),
                    ("do", '<div class="panel" style="width: 100%;"><b>Order summary</b><hr class="divider" style="margin: var(--space-3) 0;"><p class="text-sm">Subtotal $210.00</p></div>', "Separate parts inside a panel with a divider."),
                    ("dont", '<div class="card" style="width: 100%;"><div class="card"><div class="card">Nested</div></div></div>', "Nest cards in cards.")]),
    tokens=token_table([("Surface / border", "--color-bg-surface / --color-border-default"), ("Sunken surface", "--color-bg-surface-sunken"), ("Shadow / hover shadow", "--shadow-1 / --shadow-2"),
                        ("Selected edge", "--color-accent"), ("Padding panel / card / well", "--space-6 / --space-6 / --space-4"), ("Radius card / well", "--radius-lg / --radius-md"),
                        ("Header-to-body gap", "--space-4"), ("Transition", "--duration-fast")]),
    code=pre("""
<aside class="panel stack stack--lg" aria-label="Order summary">…</aside>
<div class="panel panel--sunken stack"><h2 class="panel__title">How was jaybird?</h2>…</div>
<article class="card">
  <div class="card__header"><h3 class="card__title">Payout account</h3>…</div>
  …
  <div class="card__footer"><button class="btn" type="button">Change account</button></div>
</article>""")
    + classes([("<code>.panel</code> / <code>.panel--sunken</code>", "Square panel / quiet sunken panel."), ("<code>.panel__title</code>", "Panel heading at body size."),
               ("<code>.card</code>", "Raised card, 4px radius."), ("<code>.card__header</code> <code>.card__title</code> <code>.card__footer</code>", "Card parts."),
               ("<code>.card--flush</code>", "No padding (media fills the card)."), ("<code>.card--interactive</code>", "Hover lift for a card that is a link."),
               ("<code>.card--selected</code> / <code>aria-selected</code>", "Selected edge."), ("<code>.well</code>", "Rounded sunken block."),
               ("<code>.category-tile</code>", "Category link tile with a size tag.")]),
    sources=sources([("pages/account/default", "stat panels as links"), ("pages/order-detail/completed", "sunken review prompt, card"), ("pages/checkout/default", "order summary panel"),
                     ("pages/report-detail/default", "admin card"), ("dialogs/leave-review/default", "sunken panel behind the dialog")],
                    "the account stat panels are links with no hover state; documented as interactive containers with hover and focus. Category tiles are defined in the kit but no mock renders them."),
)
drift("pages/account/default", "Stat panels are links but have no hover or focus affordance beyond the browser default.", "Documented as interactive containers; the system gives .panel links the hover border and the shared focus ring.")


# ---------------------------------------------------------------------------
# Dialog
# ---------------------------------------------------------------------------
X = btn("", "ghost icon", icon="close", attrs='aria-label="Close"')


def dialog(did: str, title: str, body: str, footer: str, desc: str = "", icon: str = "", size: str = "", top: str = "", backdrop: bool = True) -> str:
    ih = f'<div class="dialog__icon dialog__icon--{icon}" aria-hidden="true">{ic("trash" if icon == "danger" else "info")}</div>' if icon else ""
    d = f'<p id="{did}-desc" class="text-muted" style="margin-top: var(--space-2);">{desc}</p>' if desc else ""
    dd = f' aria-describedby="{did}-desc"' if desc else ""
    t = f'<div style="padding: var(--space-4) var(--space-6) 0;">{top}</div>' if top else ""
    sz = f" dialog__panel--{size}" if size else ""
    bd = '<div class="backdrop"></div>' if backdrop else ""
    return (f'{bd}<div class="dialog" role="dialog" aria-modal="true" aria-labelledby="{did}-title"{dd}><div class="dialog__panel{sz}">'
            f'<div class="dialog__header">{ih}<div style="flex: 1;"><h3 class="dialog__title" id="{did}-title">{title}</h3>{d}</div>{X}</div>{t}'
            f'<div class="dialog__body stack">{body}</div><div class="dialog__footer">{footer}</div></div></div>')


def panel(did: str, title: str, body: str, footer: str, desc: str = "", icon: str = "", size: str = "") -> str:
    """The dialog panel alone, static, for theme comparisons."""
    return dialog(did, title, body, footer, desc, icon, size, backdrop=False).replace('<div class="dialog" ', '<div class="ds-dialog-static" ')


def page_bg(text: str = "Order 12L-48302 · Paid · ship by Fri 30 Oct") -> str:
    return f'<div class="ds-stage__page" aria-hidden="true"><b>Sale detail</b><span class="text-muted text-sm">{text}</span></div>'


WITHDRAW = dict(title="Withdraw this listing?", desc="Iron Ranger 8111 boots leaves the catalog now. You can relist it from Your listings.",
                body='<p class="text-sm text-muted">Nobody has reserved it, so no buyer is affected.</p>',
                footer=btn("Keep listing", attrs="autofocus") + btn("Withdraw", "danger"), icon="danger")


def _reasons(did: str, invalid: bool) -> str:
    inv = ' aria-invalid="true"' if invalid else ""
    err = f'<span class="field__error" id="{did}-reason-error">Choose a reason</span>' if invalid else ""
    db = f' aria-describedby="{did}-reason-error"' if invalid else ""
    opts = "".join(f'<label class="choice"><input type="radio" name="{did}-reason"{inv}><span>{r}</span></label>' for r in ["Item damaged", "No longer have it", "Buyer asked me to cancel"])
    return f'<fieldset{db}><legend>Reason</legend>{opts}{err}</fieldset>'


def cancel(did: str, state: str = "default") -> str:
    busy = ' aria-busy="true"' if state == "busy" else ""
    top = alert("danger", "That didn’t go through", "Nothing changed. Check your connection and try again.") if state == "failed" else ""
    return dialog(did, "Cancel this sale?", _reasons(did, state == "invalid"),
                  btn("Keep sale") + btn("Try again" if state == "failed" else "Cancel sale", "danger", attrs=f'type="submit"{busy}'),
                  desc="tall_tom is refunded $48.15 in full. The listing stays off the catalog until you relist.", icon="danger", top=top)


def alert(kind: str, title: str, text: str) -> str:
    icon = {"danger": "x-circle", "info": "info"}[kind]
    role = ' role="alert"' if kind == "danger" else ""
    return f'<div class="alert alert--{kind}"{role}>{ic(icon)}<div class="alert__body"><div class="alert__title">{title}</div><div>{text}</div></div></div>'


TRACK_BODY = ('<div class="field"><label class="field__label" for="{d}-carrier">Carrier</label><select class="select" id="{d}-carrier"><option>USPS</option><option>UPS</option><option>FedEx</option></select></div>'
              '<div class="field"><label class="field__label" for="{d}-track">Tracking number</label><input class="input" id="{d}-track" type="text" value="9400 1118 9922 3456 1204 77" autocomplete="off"></div>')

component(
    "dialog", "Dialog", "Containers and overlays",
    lead="A modal window for one short task or one decision: add tracking, cancel a sale, withdraw a listing. On phones it rises from the bottom as a sheet.",
    pills=["APG Dialog (modal)", "Bottom sheet below 640px"],
    summary_variants="default, form, destructive (danger icon), small, large, bottom sheet",
    summary_states="default, invalid, busy, failed, success",
    overview=p("Use a dialog when the member must finish or dismiss something before going on, and the task fits on one screen: a confirmation, a form of one to four fields. "
               f"Anything longer is a page; filters and the mobile menu are {comp('drawer', 'sheets')}; a quiet result is a {comp('toast')}. See {patt('dialogs-and-overlays')}.")
    + ul("<b>Form</b>: add tracking, change password, report a problem. Primary action names the result (<i>Add tracking</i>).",
         "<b>Destructive</b>: a danger icon, a question title, a description of what will happen and a danger confirm button. The safe button is first and takes initial focus.",
         "<b>Small</b> (24rem) for one-line confirmations such as <i>Got it and all good?</i>; <b>large</b> (48rem) for the cookie and resolution dialogs with long content."),
    anatomy=anatomy(panel("an", **WITHDRAW),
                    [("4%", "8%"), ("20%", "8%"), ("92%", "8%"), ("6%", "50%"), ("60%", "84%")],
                    [("Icon (destructive only)", "40px square, danger tint; <code>aria-hidden</code>."), ("Title and description", "h3-size title is the accessible name; the description is linked with <code>aria-describedby</code>."),
                     ("Close button", "Ghost icon button, <i>Close</i>."), ("Body", "16px × 24px padding; stacks fields with 16px gaps."),
                     ("Footer", "Hairline top edge, sticky, actions right-aligned with the primary last.")]),
    variants=stage(page_bg() + dialog("dv1", "Add tracking", TRACK_BODY.format(d="dv1"), btn("Cancel") + btn("Add tracking", "primary", attrs='type="submit"'),
                                      desc="We’ll email tall_tom the tracking link."), "26rem", "Form dialog over its page; the page behind is inert.")
    + stage(page_bg("Your listings · 3 selling") + dialog("dv2", **WITHDRAW), "22rem", "Destructive dialog: danger icon, question title, the safe action first.")
    + stage(page_bg("Order 12L-48140 · Delivered") + dialog("dv3", "Got it and all good?", '<p class="text-sm">Better Sweater fleece · Patagonia · Men\'s L</p>',
                                                           btn("Not yet") + btn("Confirm receipt", "primary"), desc="This completes the order and pays vintage_lou. You can’t report a problem afterwards.", size="sm"),
            "24rem", "Small dialog."),
    sizes=p("Width is the only size; height follows content up to the viewport minus 48px, then the body scrolls and the footer stays pinned.")
    + table(["Size", "Max width", "Used for"], [["<code>.dialog__panel--sm</code>", "24rem (384px)", "Confirm receipt, cookie settings"], ["default", "32rem (512px)", "Forms, destructive confirmations"],
                                                ["<code>.dialog__panel--lg</code>", "48rem (768px)", "Resolve report, resolve problem (admin)"]]),
    states=p("Dialogs show the same states as forms. Each is a real mock:")
    + matrix(["What changes"], [("Default", ["Initial focus on the first field, or on the safe button in destructive dialogs."]),
                                ("Invalid", ["Errors under each field (<code>aria-invalid</code> + <code>aria-describedby</code>); focus moves to the first invalid field. The dialog stays open."]),
                                ("Busy", ["The primary button shows the spinner with <code>aria-busy=\"true\"</code>; other controls stay enabled; Esc and Close still work."]),
                                ("Failed", ["A danger alert under the header says nothing changed; the primary becomes <i>Try again</i>."]),
                                ("Success", ["The dialog closes and a toast confirms, or (when there is more to say) the body is replaced by a success message with one Done button."])], first="State")
    + stage(page_bg() + cancel("ds1", "invalid"), "32rem", "Invalid: the reason is required.", show_code=False)
    + stage(page_bg() + cancel("ds2", "busy"), "30rem", "Busy: the confirm button is loading.", show_code=False)
    + stage(page_bg() + cancel("ds3", "failed"), "34rem", "Failed: an alert explains, the primary retries.", show_code=False)
    + "<h3>Both themes</h3>" + themes(panel("dt-d", **WITHDRAW), light=panel("dt-l", **WITHDRAW))
    + p("The close button is a ghost button; its hover, focus and active states are the " + comp("button") + "'s."),
    responsive=ul("Below 640px the dialog is a bottom sheet: full width, 6px top corners (<code>--radius-xl</code>), rising from the bottom edge so the actions sit near the thumb.",
                  "From 640px it is centred with 24px of space around it, 4px corners, and scales in.",
                  "Footer buttons wrap; when they wrap the primary is on its own row at the bottom. Below 640px consider <code>.btn--block</code> for both.",
                  "The body scrolls; the header and footer stay visible.")
    + '<div class="ds-themes" style="grid-template-columns: minmax(0, 22rem);">' + stage(page_bg() + dialog("dr1", **WITHDRAW).replace('class="dialog"', 'class="dialog ds-dialog--sheet"'), "24rem", "Bottom sheet at 360px.", show_code=False) + "</div>",
    theming=p("The panel is <code>--color-bg-surface-raised</code> with <code>--shadow-4</code> over a <code>--color-bg-backdrop</code> scrim (55% ink in light, 70% black in dark). In dark the raised surface (ink-850) is lighter than the page behind it, so the panel still reads as on top. "
              "Component tokens: <code>--dialog-bg</code>, <code>--dialog-shadow</code>, <code>--dialog-max</code>."),
    accessibility=a11y(
        pattern="APG Dialog (modal): <code>role=\"dialog\"</code>, <code>aria-modal=\"true\"</code>, <code>aria-labelledby</code> the title and <code>aria-describedby</code> the description. The page behind gets <code>inert</code>. A native <code>&lt;dialog&gt;</code> opened with <code>showModal()</code> is an equivalent implementation.",
        keyboard=[(kbd("Tab") + " / " + kbd("Shift", "Tab"), "Cycles through the dialog's controls only; focus is trapped."), (kbd("Esc"), "Closes the dialog (also while busy; the request continues and its result arrives as a toast)."),
                  (kbd("Enter"), "In a form dialog, submits.")],
        focus="On open, focus goes to the first field, or to the safe button in destructive dialogs (<code>autofocus</code> on <i>Keep listing</i>). On close it returns to the control that opened the dialog. On an invalid submit it moves to the first invalid field.",
        labelling="Title is the name; the description says what will happen. The close button is <i>Close</i>. Destructive titles are questions that name the object: <i>Withdraw this listing?</i>",
        contrast=[("Text on panel", "--color-fg-default", "--color-bg-surface-raised", 4.5), ("Description", "--color-fg-muted", "--color-bg-surface-raised", 4.5),
                  ("Field error in dialog", "--color-danger-fg", "--color-bg-surface-raised", 4.5), ("Danger icon on tint", "--color-danger-icon", "--color-danger-bg", 3)],
        motion="Backdrop fades in over <code>--duration-base</code>; the panel scales in (or slides up as a sheet) over <code>--duration-slow</code> with <code>--ease-enter</code>. Under reduced motion both are instant.",
        touch="Footer buttons are 40px tall with 12px between them; the close button is 40px."),
    content=ul("Title: a question for decisions (<i>Cancel this sale?</i>), a verb phrase for tasks (<i>Add tracking</i>).",
               "Description: one or two sentences with the consequence and the numbers: <i>tall_tom is refunded $48.15 in full.</i>",
               "Buttons name outcomes: <i>Keep sale</i> / <i>Cancel sale</i>, never <i>No</i> / <i>Yes</i>.",
               "Failure copy: <i>That didn’t go through</i> + <i>Nothing changed. Check your connection and try again.</i>"),
    do_dont=dodont([("do", '<div class="cluster">' + btn("Keep listing") + btn("Withdraw", "danger") + "</div>", "Name both outcomes; put the destructive one last and focus the safe one."),
                    ("dont", '<div class="cluster">' + btn("No") + btn("Yes", "primary") + "</div>", "Ask a question and answer it with Yes / No."),
                    ("do", '<p class="text-sm">Iron Ranger 8111 boots leaves the catalog now. You can relist it from Your listings.</p>', "Say what happens and how to undo it."),
                    ("dont", '<p class="text-sm">Are you sure? This action cannot be undone.</p>', "Use generic warnings that do not name the object or the consequence.")]),
    tokens=token_table([("Panel / text", "--color-bg-surface-raised / --color-fg-default"), ("Scrim", "--color-bg-backdrop"), ("Shadow", "--shadow-4"), ("Footer edge", "--color-border-default"),
                        ("Danger icon", "--color-danger-bg / --color-danger-icon"), ("Info icon", "--color-info-bg / --color-info-icon"),
                        ("Radius centred / sheet", "--radius-lg / --radius-xl"), ("Padding", "--space-6 / --space-4"), ("Layers", "--z-overlay / --z-modal"),
                        ("Motion", "--duration-slow / --ease-enter")]),
    code=pre("""
<div class="backdrop"></div>
<div class="dialog" role="dialog" aria-modal="true" aria-labelledby="dlg-title" aria-describedby="dlg-desc">
  <div class="dialog__panel">
    <div class="dialog__header">
      <div class="dialog__icon dialog__icon--danger" aria-hidden="true">…</div>
      <div style="flex: 1;">
        <h2 class="dialog__title" id="dlg-title">Withdraw this listing?</h2>
        <p id="dlg-desc" class="text-muted">Iron Ranger 8111 boots leaves the catalog now.</p>
      </div>
      <button class="btn btn--ghost btn--icon" type="button" aria-label="Close">…</button>
    </div>
    <div class="dialog__body stack">…</div>
    <div class="dialog__footer">
      <button class="btn" type="button" autofocus>Keep listing</button>
      <button class="btn btn--danger" type="button">Withdraw</button>
    </div>
  </div>
</div>""")
    + classes([("<code>.backdrop</code>", "Scrim behind the dialog."), ("<code>.dialog</code>", "Fixed positioning layer; bottom sheet below 640px, centred above."),
               ("<code>.dialog__panel</code> <code>--sm</code> <code>--lg</code>", "The window and its width."), ("<code>.dialog__header</code> <code>.dialog__title</code>", "Header row and title."),
               ("<code>.dialog__icon--danger</code> / <code>--info</code>", "Leading icon tile."), ("<code>.dialog__body</code>", "Scrolling content."), ("<code>.dialog__footer</code>", "Sticky actions.")]),
    sources=sources([("dialogs/withdraw-listing/default", "destructive"), ("dialogs/cancel-order/invalid", "invalid"), ("dialogs/add-tracking/failed", "failed"),
                     ("dialogs/confirm-receipt/default", "small"), ("dialogs/resolve-report/default", "large"), ("dialogs/data-export/success", "success")],
                    "dialogs centred at the mocks' 36rem breakpoint; they now centre at the system's sm breakpoint (40rem)."),
)


# ---------------------------------------------------------------------------
# Drawer / sheet
# ---------------------------------------------------------------------------
def menu_sheet(sid: str) -> str:
    big = "".join(f'<li><a href="#">{n}{ic("chevron-right")}</a></li>' for n in ["Shoes", "Tops", "Outerwear", "Bottoms"])
    small = "".join(f'<li><a href="#">{n}</a></li>' for n in ["Sell an item", "Your listings", "Purchases", "Settings"])
    return (f'<div class="menu-sheet" role="dialog" aria-modal="true" aria-labelledby="{sid}-t"><div class="menu-sheet__head"><span class="logo">{LOGO_SVG}</span>'
            f'<h3 class="visually-hidden" id="{sid}-t">Menu</h3>{btn("", "ghost icon", icon="close", attrs="aria-label=\"Close menu\"")}</div>'
            f'<nav class="menu-sheet__body" aria-label="Menu {sid}"><ul class="menu-sheet__links" role="list">{big}</ul><ul class="menu-sheet__links menu-sheet__links--small" role="list">{small}</ul></nav>'
            f'<div class="menu-sheet__foot">{btn("Sign out", icon="log-out")}</div></div>')


def filter_sheet(sid: str) -> str:
    cats = "".join(f'<label class="choice"><input type="checkbox" name="{sid}-c"{" checked" if c == "Sneakers" else ""}><span>{c}</span></label>' for c in ["Sneakers", "Boots", "Dress shoes"])
    return (f'<div class="menu-sheet filter-sheet" role="dialog" aria-modal="true" aria-labelledby="{sid}-t"><div class="menu-sheet__head"><h3 id="{sid}-t" style="font: var(--text-h4);">Filters</h3>'
            f'{btn("", "ghost icon", icon="close", attrs="aria-label=\"Close filters\"")}</div><div class="menu-sheet__body"><fieldset class="filters__group"><legend>Category</legend>{cats}</fieldset>'
            f'<div class="filters__group"><span class="eyebrow">Price</span><div class="filters__range"><label class="visually-hidden" for="{sid}-min">Minimum price</label><input class="input input--sm" id="{sid}-min" inputmode="numeric" placeholder="Min">'
            f'<span class="text-muted">to</span><label class="visually-hidden" for="{sid}-max">Maximum price</label><input class="input input--sm" id="{sid}-max" inputmode="numeric" placeholder="Max"></div></div></div>'
            f'<div class="menu-sheet__foot">{btn("Clear all")}{btn("Show 41 results", "primary")}</div></div>')


def drawer(sid: str) -> str:
    return (f'<div class="backdrop"></div><div class="drawer" role="dialog" aria-modal="true" aria-labelledby="{sid}-t"><div class="drawer__header"><h3 class="drawer__title" id="{sid}-t">Order 12L-48213</h3>'
            f'{btn("", "ghost icon", icon="close", attrs="aria-label=\"Close\"")}</div><div class="drawer__body stack"><p class="text-sm text-muted">Red Wing Iron Ranger 8111 boots · $225.00 · Shipped Fri 23 Oct</p></div>'
            f'<div class="drawer__footer">{btn("Close")}{btn("Open order", "primary")}</div></div>')


component(
    "drawer", "Drawer and sheet", "Containers and overlays",
    lead="Panels that slide in from an edge: the full-screen menu sheet on phones, the filters sheet, and a side drawer for previews.",
    pills=["APG Dialog (modal)"],
    summary_variants="menu sheet (full screen), filter sheet (left, full screen on phones), right drawer, left drawer",
    summary_states="default, busy",
    overview=p("Sheets and drawers are dialogs that keep the page's context at the edge. 12L uses two:")
    + ul("<b>Menu sheet</b> (<code>.menu-sheet</code>): opened by the top bar's menu button below 768px. Full screen, categories in large type, account links in body type, Sign out at the bottom.",
         "<b>Filter sheet</b> (<code>.menu-sheet.filter-sheet</code>): catalog filters below 1024px. Full screen on phones, a 24rem panel from the left from 768px, with <i>Clear all</i> and <i>Show 41 results</i> pinned at the bottom.",
         "<b>Drawer</b> (<code>.drawer</code>): a 28rem side panel from the right (or left) for previews and secondary tasks. Core; no mock uses it yet.")
    + p(f"Use a {comp('dialog')} for a decision; use a sheet when the content is navigation or a set of controls the member adjusts and applies."),
    anatomy=anatomy(stage(filter_sheet("fa"), "26rem", show_code=False), [("6%", "8%"), ("88%", "8%"), ("6%", "30%"), ("40%", "90%")],
                    [("Head", "Title (or the logo) and the close button, 64px tall like the top bar."), ("Close", "Ghost icon button."),
                     ("Body", "Scrolls; 32px vertical padding, groups 32px apart."), ("Foot", "Pinned actions; 48px buttons that share the width.")]),
    variants=stage(menu_sheet("mv"), "34rem", "Menu sheet (phones).") + stage(filter_sheet("fv"), "28rem", "Filter sheet.")
    + stage('<div class="ds-stage__page" aria-hidden="true"><b>Purchases</b></div>' + drawer("dv"), "20rem", "Right drawer (core)."),
    sizes=table(["Variant", "Below 768px", "768px and up"], [["Menu sheet", "Full screen", "Not used (top-bar links visible)"], ["Filter sheet", "Full screen", "24rem from the left, <code>--shadow-4</code>"],
                                                         ["Drawer", "Full width", "<code>min(100%, 28rem)</code>"]]),
    states=matrix(["What changes"], [("Default", ["Opens with focus on the close button (menu) or the first control (filters)."]),
                                     ("Busy", ["Filters: <i>Show 41 results</i> shows the button spinner while the count updates; the sheet stays open."]),
                                     ("Invalid", ["Filters: a price range with min above max shows a field error and disables nothing; <i>Show results</i> moves focus to the error."])], first="State")
    + "<h3>Both themes</h3>" + themes(stage(menu_sheet("mt-d"), "22rem", show_code=False), light=stage(menu_sheet("mt-l"), "22rem", show_code=False)),
    responsive=ul("The menu sheet only exists below 768px; at 768px the top bar shows the links and the sheet closes if open.",
                  "The filter sheet becomes the sticky filters column at 1024px.", "Sheet heads match <code>--layout-topbar-height</code> so the close button sits where the menu button was."),
    theming=p("Sheets use <code>--color-bg-canvas</code> (they replace the page); drawers use <code>--color-bg-surface-raised</code> with <code>--shadow-4</code>. Dividers are <code>--color-border-default</code>."),
    accessibility=a11y(
        pattern="APG Dialog (modal) with <code>role=\"dialog\"</code>, <code>aria-modal=\"true\"</code> and a label (a visually hidden <i>Menu</i> heading for the menu sheet). The opener has <code>aria-expanded</code> and <code>aria-controls</code>.",
        keyboard=[(kbd("Tab"), "Cycles inside the sheet."), (kbd("Esc"), "Closes and returns focus to the opener."), (kbd("Enter"), "Follows a link or applies filters.")],
        focus="Menu sheet: initial focus on <i>Close menu</i>. Filter sheet: on the first filter. Focus returns to the menu or <i>Filters</i> button on close.",
        labelling="Close buttons say what they close: <i>Close menu</i>, <i>Close filters</i>. The apply button includes the result count.",
        contrast=[("Sheet link", "--color-fg-default", "--color-bg-canvas", 4.5), ("Drawer text", "--color-fg-muted", "--color-bg-surface-raised", 4.5)],
        motion="Menu sheet fades in over <code>--duration-base</code>; filter sheet and drawer slide from their edge over <code>--duration-slow</code>. Instant under reduced motion.",
        touch="Menu links are 56px tall rows; small links 44px; foot buttons 48px."),
    content=ul("Apply buttons state the outcome with the count: <i>Show 41 results</i>.", "Reset is <i>Clear all</i>.", "Menu categories match the top bar exactly."),
    do_dont=dodont([("do", f'<div class="cluster">{btn("Clear all")}{btn("Show 41 results", "primary")}</div>', "Tell the member how many results they will get."),
                    ("dont", f'<div class="cluster">{btn("Reset")}{btn("Apply", "primary")}</div>', "Use vague Apply / Reset labels."),
                    ("do", f'{btn("", "ghost icon", icon="close", attrs="aria-label=\"Close menu\"")}', "Name what the close button closes."),
                    ("dont", '<p class="text-sm">A drawer holding a multi-step checkout.</p>', "Put a long task in a drawer; give it a page.")]),
    tokens=token_table([("Sheet background", "--color-bg-canvas"), ("Drawer background", "--color-bg-surface-raised"), ("Dividers", "--color-border-default"), ("Shadow", "--shadow-4"),
                        ("Head height", "--layout-topbar-height"), ("Layer", "--z-modal"), ("Motion", "--duration-slow / --ease-enter")]),
    code=pre("""
<div class="menu-sheet" id="menu" role="dialog" aria-modal="true" aria-labelledby="menu-title">
  <div class="menu-sheet__head">… <h2 class="visually-hidden" id="menu-title">Menu</h2>
    <button class="btn btn--ghost btn--icon" type="button" aria-label="Close menu">…</button></div>
  <nav class="menu-sheet__body" aria-label="Menu">
    <ul class="menu-sheet__links" role="list"><li><a href="/shoes">Shoes …</a></li></ul>
  </nav>
  <div class="menu-sheet__foot"><button class="btn" type="button">Sign out</button></div>
</div>""")
    + classes([("<code>.menu-sheet</code>", "Full-screen sheet; head, body, foot."), ("<code>.filter-sheet</code>", "Filters variant; left panel from 768px."),
               ("<code>.menu-sheet__links</code> / <code>--small</code>", "Large or body-size link list."), ("<code>.drawer</code> / <code>.drawer--left</code>", "Side drawer from the right / left."),
               ("<code>.drawer__header</code> <code>__body</code> <code>__footer</code>", "Drawer parts.")]),
    sources=sources([("dialogs/nav-menu/default", "member menu sheet"), ("dialogs/nav-menu/guest", "guest menu sheet"), ("dialogs/filters/default", "filter sheet"),
                     ("dialogs/filters/invalid", "price range error"), ("dialogs/filters/busy", "updating count")]),
)


# ---------------------------------------------------------------------------
# Tooltip
# ---------------------------------------------------------------------------
def tip(label: str, text: str, state: str = "", tid: str = "tt") -> str:
    s = f' data-state="{state}"' if state else ""
    return (f'<span class="has-tooltip"{s}><button class="btn btn--ghost btn--icon" type="button" aria-label="{label}" aria-describedby="{tid}">{ic("share")}</button>'
            f'<span class="tooltip" role="tooltip" id="{tid}">{text}</span></span>')


component(
    "tooltip", "Tooltip", "Containers and overlays",
    lead="A short label that appears on hover and focus to name an icon-only button. Core; the mocks rely on aria-label alone today.",
    pills=["role=\"tooltip\"", "Core (not in mocks)"],
    summary_variants="text, with shortcut",
    summary_states="hidden, hover, focus",
    overview=p("Icon-only buttons (Share, Save, Close, More actions) need a visible name for sighted pointer and keyboard users; a tooltip shows the same words as the button's <code>aria-label</code>. "
               "Tooltips never hold anything interactive or anything the member must read to finish a task; that is a popover or inline help.")
    + ul("<b>Text</b>: one to three words.", "<b>With shortcut</b>: the label plus a <code>&lt;kbd&gt;</code> hint, for admin tools."),
    anatomy=anatomy('<div class="ds-float" style="min-height: 7rem;">' + tip("Share listing", "Share listing", "hover", "tt-a") + "</div>",
                    [("50%", "18%"), ("52%", "70%")], [("Bubble", "Inverse surface, caption text, 4px × 8px padding, 2px radius, 5px arrow."), ("Trigger", "The icon button it names.")]),
    variants=ex('<div class="ds-float" style="min-height: 7rem;">' + tip("Share listing", "Share listing", "hover", "tt-v1")
                + f'<span class="has-tooltip" data-state="hover"><button class="btn btn--ghost btn--icon" type="button" aria-label="Approve report" aria-describedby="tt-v2">{ic("check")}</button><span class="tooltip" role="tooltip" id="tt-v2">Approve <kbd>A</kbd></span></span></div>',
                "Text, and with a keyboard shortcut.", show_code=False),
    sizes=NA("Tooltips have one size."),
    states=matrix(["Hidden", "Hover", "Focus"], [("Tooltip", ['<div class="ds-float" style="min-height: 6rem;">' + tip("Save", "Save", st, f"tt-s{i}") + "</div>"
                                                              for i, st in enumerate(["", "hover", "focus"])])], first="Element")
    + "<h3>Both themes</h3>" + themes('<div class="ds-float" style="min-height: 6rem;">' + tip("Share listing", "Share listing", "hover", "tt-td") + "</div>",
                                      light='<div class="ds-float" style="min-height: 6rem;">' + tip("Share listing", "Share listing", "hover", "tt-tl") + "</div>"),
    responsive=ul("Touch devices have no hover: the tooltip appears on long press only, and never replaces a visible label where space allows.", "Tooltips flip below the trigger when there is no room above."),
    theming=p("<code>--color-bg-inverse</code> with <code>--color-fg-inverse</code>: ink on paper in light, paper on ink in dark, always the opposite of the page."),
    accessibility=a11y(
        pattern="APG Tooltip: the bubble has <code>role=\"tooltip\"</code> and the trigger references it with <code>aria-describedby</code>. The trigger keeps its own <code>aria-label</code>, so the name never depends on the tooltip.",
        keyboard=[(kbd("Tab"), "Focusing the trigger shows the tooltip."), (kbd("Esc"), "Hides the tooltip without moving focus (1.4.13).")],
        focus="Focus stays on the trigger; the tooltip is not focusable.",
        labelling="Tooltip text matches the <code>aria-label</code>; when they are identical, <code>aria-describedby</code> may be omitted to avoid double announcement.",
        contrast=[("Tooltip text", "--color-fg-inverse", "--color-bg-inverse", 4.5)],
        motion="Fades in over <code>--duration-fast</code> after a 300ms hover delay; hides immediately. Stays visible while the pointer is over it (1.4.13 hoverable).",
        touch="Not relied on; triggers are 40px buttons."),
    content=ul("Same words as the button's label, sentence case, no full stop: <i>Share listing</i>.", "Never instructions or policy text."),
    do_dont=dodont([("do", '<div class="ds-float" style="min-height: 6rem;">' + tip("Share listing", "Share listing", "hover", "tt-d1") + "</div>", "Name an icon-only control."),
                    ("dont", '<div class="ds-float" style="min-height: 6rem;"><span class="has-tooltip" data-state="hover"><span class="text-sm">Platform fee</span><span class="tooltip" role="tooltip">12L keeps 10% of the item price, $3.70 on this order. <a href="#">Learn more</a></span></span></div>', "Put essential fee information or a link in a tooltip; show it inline.")]),
    tokens=token_table([("Background / text", "--color-bg-inverse / --color-fg-inverse"), ("Font", "--text-caption"), ("Padding", "--space-1 / --space-2"), ("Radius", "--radius-sm"),
                        ("Shadow", "--shadow-2"), ("Layer", "--z-tooltip"), ("Fade", "--duration-fast")]),
    code=pre("""
<span class="has-tooltip">
  <button class="btn btn--ghost btn--icon" type="button" aria-label="Share listing" aria-describedby="tip-share">…</button>
  <span class="tooltip" role="tooltip" id="tip-share">Share listing</span>
</span>""")
    + classes([("<code>.has-tooltip</code>", "Positioning wrapper; shows the tooltip on hover and focus-within."), ("<code>.tooltip</code>", "The bubble, above the trigger."),
               ("<code>data-state=\"hover|focus\"</code>", "Documentation only: shows the tooltip statically.")]),
    sources=sources([("pages/listing-detail/default", "icon-only Share and Save"), ("pages/sell/default", "icon-only Remove photo"), ("pages/moderation-queue/default", "admin icon actions")],
                    "icon-only buttons in the mocks have aria-label but no visible tooltip; the system adds the tooltip for pointer and keyboard users."),
)
drift("pages/listing-detail/default", "Icon-only buttons (Share, Save, Remove photo, Close) carry aria-label but show no visible name on hover or focus.", "Tooltip component specified; product builds add it to every icon-only button.")


# ---------------------------------------------------------------------------
# Divider
# ---------------------------------------------------------------------------
component(
    "divider", "Divider", "Containers and overlays",
    lead="A hairline that separates groups of content where white space alone is not enough: reviews in a dialog, order rows, form sections.",
    pills=["<code>&lt;hr&gt;</code>"],
    summary_variants="horizontal, vertical, with label",
    summary_states="none (static)",
    overview=p("12L prefers space to lines. Use a divider when two adjacent blocks would otherwise read as one: a buyer's and a seller's statement in the resolve-problem dialog, the total row of an order summary. "
               "Lists (orders, settings, reviews) draw their own row borders; do not add dividers between their items."),
    anatomy=anatomy('<div style="width: 100%;"><p class="text-sm">Buyer’s statement</p><hr class="divider"><p class="text-sm">Seller’s statement</p></div>', [("50%", "48%")],
                    [("Rule", "1px <code>--color-border-default</code>, 24px space above and below.")]),
    variants=ex('<div style="width: 100%;"><hr class="divider"></div>', "Horizontal.") + ex('<div class="cluster"><span class="text-sm">Size US 12</span><span class="divider--vertical" role="separator" aria-orientation="vertical"></span><span class="text-sm">Used - Good</span></div>', "Vertical, between inline facts.")
    + ex('<div style="width: 100%;"><div class="divider--label" role="separator" aria-label="or">or</div></div>', "With a label, between alternative sign-in methods."),
    sizes=NA("One weight: --border-width-hairline. Spacing comes from the surrounding stack."),
    states=NA("Dividers are static and have no interactive states."),
    responsive=ul("Full width of their container at every breakpoint.", "Vertical dividers become horizontal (or disappear) when the row wraps below 640px."),
    theming=p("<code>--color-border-default</code>: paper-300 in light, ink-700 in dark. Decorative, so not held to a contrast minimum.") + themes('<p class="text-sm">Above</p><hr class="divider"><p class="text-sm">Below</p>'),
    accessibility=a11y(
        pattern="<code>&lt;hr&gt;</code> (implicit <code>role=\"separator\"</code>) when it marks a thematic break. Purely decorative lines are borders on the containers instead. Vertical and labelled dividers use <code>role=\"separator\"</code> explicitly.",
        keyboard="Not focusable.", focus="None.", labelling="Labelled dividers carry the label as text; plain ones need none.",
        contrast=[("Divider (decorative)", "--color-border-default", "--color-bg-surface", 1), ("Label", "--color-fg-subtle", "--color-bg-surface", 4.5)],
        motion="None.", touch="Not interactive."),
    content=ul("Labels are one lowercase word: <i>or</i>."),
    do_dont=dodont([("do", '<div style="width: 100%;"><p class="text-sm"><b>tall_tom</b> · buyer</p><hr class="divider"><p class="text-sm"><b>marcus_12</b> · seller</p></div>', "Separate two statements that sit in one dialog."),
                    ("dont", '<div style="width: 100%;"><p class="text-sm">Subtotal</p><hr class="divider"><p class="text-sm">Shipping</p><hr class="divider"><p class="text-sm">Tax</p></div>', "Put a rule between every line; use spacing and one rule above the total.")]),
    tokens=token_table([("Line", "--color-border-default"), ("Weight", "--border-width-hairline"), ("Space around", "--space-6"), ("Label", "--color-fg-subtle")]),
    code=pre('<hr class="divider">\n<div class="divider--label" role="separator" aria-label="or">or</div>\n<span class="divider--vertical" role="separator" aria-orientation="vertical"></span>')
    + classes([("<code>hr</code>, <code>.divider</code>", "Horizontal rule."), ("<code>.divider--vertical</code>", "Vertical rule in a row."), ("<code>.divider--label</code>", "Rule with centred label."),
               ("<code>.rule</code>", "Page-level rule with 48px space (legal pages).")]),
    sources=sources([("dialogs/resolve-problem/default", "between statements"), ("pages/terms/default", "page rule")]),
)


# ---------------------------------------------------------------------------
# Layout primitives
# ---------------------------------------------------------------------------
BOX = '<span class="ds-box">{t}</span>'

component(
    "layout-primitives", "Layout primitives", "Containers and overlays",
    lead="Container, page, stack, cluster, grid and split: the six classes every 12L screen is laid out with, driven by the layout tokens.",
    pills=["Gutters, margins, breakpoints"],
    summary_variants="container, page (narrow, form), stack (sm, lg), cluster (between, end), grid (auto), split",
    summary_states="none (static)",
    overview=p(f"Pages compose these primitives instead of writing layout CSS. Their spacing comes from <code>--layout-margin</code>, <code>--layout-gutter</code>, <code>--layout-columns</code> and the spacing scale, so every screen changes together at the breakpoints in {found('layout')}.")
    + ul("<b>Container</b> centres content at <code>--layout-container-max</code> (1216px) with <code>--layout-margin</code> on each side.",
         "<b>Page</b> adds the 64px bottom space; <code>.page--narrow</code> (40rem) for confirmations and <code>.page--form</code> (44rem) for the sell and profile forms.",
         "<b>Stack</b> is a vertical flow with one gap (16px; 8px <code>--sm</code>; 32px <code>--lg</code>).",
         "<b>Cluster</b> is a wrapping row (12px gap) for buttons, chips and inline facts.",
         "<b>Grid</b> is the column grid (4 / 8 / 12 columns); <code>.grid--auto</code> fits 18rem cards.",
         "<b>Split</b> is the detail layout: one column, then 3fr / 2fr from 1024px (order, sale and checkout pages)."),
    anatomy=anatomy('<div class="ds-grid-demo" style="width: 100%;">' + "".join(f"<span>{i}</span>" for i in range(1, 13)) + "</div>",
                    [("1%", "10%"), ("8%", "50%"), ("15%", "50%")],
                    [("Margin", "<code>--layout-margin</code>: 16 / 32 / 48px."), ("Column", "<code>--layout-columns</code>: 4 / 8 / 12."), ("Gutter", "<code>--layout-gutter</code>: 16 / 24 / 32px.")]),
    variants="<h3>Live grid</h3>" + p("Resize the window: the grid shows the current column count, gutter and margin from the tokens.")
    + ex('<div class="ds-grid-demo" style="width: 100%;">' + "".join(f"<span>{i}</span>" for i in range(1, 13)) + "</div>", "4 columns below 768px, 8 to 1023px, 12 from 1024px.", show_code=False)
    + "<h3>Stack and cluster</h3>" + ex('<div class="stack" style="width: 100%;">' + "".join(BOX.format(t=t) for t in ["Title", "Meta", "Body"]) + "</div>", "Stack: 16px between children.")
    + ex('<div class="cluster">' + btn("Make an offer") + btn("Buy now", "primary") + size_tag("US 12") + "</div>", "Cluster: wraps, 12px gaps.")
    + "<h3>Split</h3>" + ex('<div class="split" style="width: 100%;">' + BOX.format(t="Order details (3fr)") + BOX.format(t="Order summary (2fr)") + "</div>", "One column below 1024px; 3fr / 2fr with a 64px gap above.")
    + "<h3>Auto grid</h3>" + ex('<div class="grid grid--auto" style="width: 100%;">' + "".join(BOX.format(t=f"Card {i}") for i in range(1, 5)) + "</div>", "As many 18rem columns as fit."),
    sizes=table(["Class", "Max width", "Used for"], [["<code>.container</code>", "<code>--layout-container-max</code> (76rem)", "Every app page"], ["<code>.page--narrow</code>", "40rem", "Order confirmation, error pages"],
                                                  ["<code>.page--form</code>", "44rem", "Sell, edit listing, edit profile"], ["<code>.auth-card</code>", "24rem", "Sign in, register, password reset"]]),
    states=NA("Layout primitives are static; they have no interactive states."),
    responsive=table(["Breakpoint", "Columns", "Gutter", "Margin"], [["&lt; 768px", "4", "16px", "16px"], ["768–1023px", "8", "24px", "32px"], ["≥ 1024px", "12", "32px", "48px"]])
    + ul("Split, catalog layout and listing detail switch to two columns at 1024px (the system's lg breakpoint).", "The listing grid is 2-up, 3-up from 768px, 4-up from 1024px; with the filters column it is 3-up at 1024px and 4-up from 1280px.",
         "Below 640px the listing-detail gallery bleeds to the screen edge (negative <code>--layout-margin</code>)."),
    theming=p("Layout primitives carry no colour; they theme by inheritance.") + themes('<div class="cluster">' + BOX.format(t="Same layout") + BOX.format(t="both themes") + "</div>"),
    accessibility=a11y(
        pattern="Presentational: plain <code>&lt;div&gt;</code>s that never change reading order. Visual order always matches DOM order (no <code>order</code> or reversed flex), so focus moves the way the page reads (1.3.2, 2.4.3).",
        keyboard="Not interactive.", focus="Not applicable.", labelling="Not applicable; use landmarks (<code>main</code>, <code>aside aria-label</code>) inside the layout for structure.",
        contrast=[("Text on canvas", "--color-fg-default", "--color-bg-canvas", 4.5)], motion="None.",
        touch="Reflows to one column at 320px without horizontal scrolling (1.4.10)."),
    content=NA("Layout primitives hold no copy."),
    do_dont=dodont([("do", '<div class="stack stack--sm" style="width: 100%;">' + BOX.format(t="Label") + BOX.format(t="Field") + "</div>", "Use the stack gap instead of margins on children."),
                    ("dont", f'<div style="width: 100%;"><span class="ds-box" style="margin-bottom: 13px; display: block;">Label</span><span class="ds-box" style="display: block;">Field</span></div>', "Hand-set off-scale margins (13px) on children."),
                    ("do", '<div class="split" style="width: 100%;">' + BOX.format(t="Details") + BOX.format(t="Summary") + "</div>", "Use split for detail + summary."),
                    ("dont", '<div style="display: grid; grid-template-columns: 1fr 380px; width: 100%;">' + BOX.format(t="Details") + BOX.format(t="Fixed 380px") + "</div>", "Hard-code pixel columns that overflow at 360px.")]),
    tokens=token_table([("Container max", "--layout-container-max"), ("Columns", "--layout-columns"), ("Gutter", "--layout-gutter"), ("Margin", "--layout-margin"),
                        ("Measure", "--layout-measure"), ("Stack gaps", "--space-2 / --space-4 / --space-8"), ("Cluster gap", "--space-3"), ("Split gap", "--space-10 / --space-16"), ("Page bottom", "--space-16")]),
    code=pre("""
<main id="main" class="container page">
  <div class="split">
    <div class="stack stack--lg">…</div>
    <aside class="panel" aria-label="Order summary">…</aside>
  </div>
</main>""")
    + classes([("<code>.container</code>", "Centred, max width, side margins."), ("<code>.page</code> <code>--narrow</code> <code>--form</code>", "Page bottom space and max widths."),
               ("<code>.stack</code> <code>--sm</code> <code>--lg</code>", "Vertical flow."), ("<code>.cluster</code> <code>--between</code> <code>--end</code>", "Wrapping row."),
               ("<code>.grid</code> <code>.grid--auto</code> <code>.span-full</code>", "Column grid."), ("<code>.split</code>", "Detail + summary columns.")]),
    sources=sources([("pages/order-detail/default", "split"), ("pages/account/default", "grid--auto stats"), ("pages/sell/default", "page--form"), ("pages/order-confirmation/default", "narrow page"),
                     ("pages/catalog/default", "catalog layout and listing grid")],
                    "breakpoints at 36rem, 62rem and 75rem in the mocks' ui.css were normalised to the system's 40rem, 64rem and 80rem."),
)
drift("docs/mocks/assets/ui.css", "Media queries used 36rem, 62rem and 75rem (plus 35.99rem), none of which were layout tokens (40/48/64/80/96rem).",
      "Normalised to 40rem (sm), 64rem (lg) and 80rem (xl) in components.css; dialogs centre, form rows split and two-column layouts start 32–64px later.")
