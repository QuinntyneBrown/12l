"""Actions: button group, link, menu. (Button lives in comp_00_button.py.)"""
from ds import *

STATES = ["Default", "Hover", "Focus", "Active", "Disabled"]
DS = {"default": "", "hover": ' data-state="hover"', "focus": ' data-state="focus"', "active": ' data-state="active"', "disabled": " disabled"}

# ---------------------------------------------------------------------------
# Button group: segmented choice (.segmented) and pressed toolbar (.btn-group)
# ---------------------------------------------------------------------------
CONDS = ["New with tags", "New without tags", "Used - Excellent", "Used - Good", "Used - Fair"]


def segmented(name: str, opts, chosen: str = "", legend: str = "Condition", state: str = "", invalid: bool = False, disabled: bool = False) -> str:
    out = ""
    for o in opts:
        chk = " checked" if o == chosen else ""
        st = f' data-state="{state}"' if state and o == chosen else ""
        inv = ' aria-invalid="true"' if invalid else ""
        dis = " disabled" if disabled else ""
        out += f'<label><input type="radio" name="{name}"{chk}{inv}{dis}><span{st}>{esc(o)}</span></label>'
    return f'<fieldset><legend>{legend}</legend><div class="segmented">{out}</div></fieldset>'


def toolbar(sfx: str, state: str = "", pressed: int = 0) -> str:
    items = ["Shoes", "Tops", "Outerwear", "Bottoms"]
    out = ""
    for i, t in enumerate(items):
        pr = "true" if i == pressed else "false"
        st = DS.get(state, "") if i == 1 else ""
        out += f'<button class="btn btn--sm" type="button" aria-pressed="{pr}"{st}>{t}</button>'
    return f'<div class="btn-group" role="group" aria-label="Category {sfx}">{out}</div>'


def _seg_state(state: str) -> str:
    n = f"seg-{state}"
    if state == "default":
        return segmented(n, ["Good", "Fair"], "", legend="Condition")
    if state == "disabled":
        return segmented(n, ["Good", "Fair"], "Good", legend="Condition", disabled=True)
    if state == "focus":
        return f'<fieldset><legend>Condition</legend><div class="segmented"><label><input type="radio" name="{n}" checked><span style="outline: var(--focus-ring-width) solid var(--color-focus-ring); outline-offset: 2px;">Good</span></label><label><input type="radio" name="{n}"><span>Fair</span></label></div></fieldset>'
    if state == "hover":
        return f'<fieldset><legend>Condition</legend><div class="segmented"><label><input type="radio" name="{n}"><span data-state="hover">Good</span></label><label><input type="radio" name="{n}"><span>Fair</span></label></div></fieldset>'
    return segmented(n, ["Good", "Fair"], "Good", legend="Condition")


component(
    "button-group", "Button group", "Actions",
    lead="A set of mutually related choices shown side by side: the condition picker on the sell form and the problem type in Report a problem are segmented groups.",
    pills=["<code>fieldset</code> + radios", "<code>aria-pressed</code> toolbar"],
    summary_variants="segmented (single select, radio-based), toolbar (pressed toggles)",
    summary_states="default, hover, focus, checked/pressed, invalid, disabled",
    overview=p(f"Use a segmented group when the member picks exactly one of two to six short options and every option should be visible at once: the five conditions on the sell form, the three problem types in Report a problem. "
               f"With more than six options, or long labels, use a {comp('radio-group')} (a vertical list) or a {comp('select')}. To filter a list by status, use filter {comp('chip', 'chips')}, which can wrap and carry counts.")
    + ul("<b>Segmented</b> (<code>.segmented</code>) is built from real radio inputs inside a <code>&lt;fieldset&gt;</code>. It is a form control: it submits a value and shows errors like any field. This is the 12L default.",
         "<b>Toolbar</b> (<code>.btn-group</code>) joins buttons that toggle a view setting immediately with <code>aria-pressed</code>. It never submits a form."),
    anatomy=anatomy(
        '<div style="width: 100%; max-width: 30rem;">' + segmented("anat", CONDS[2:], "Used - Excellent") + "</div>",
        [("8%", "10%"), ("16%", "58%"), ("50%", "58%")],
        [("Legend", "The question, as a <code>&lt;legend&gt;</code> in <code>--text-label</code>. It names the group for assistive technology."),
         ("Selected segment", "Solid ink (<code>--color-accent</code>) with a paper label, the same treatment as a primary button."),
         ("Segment", "44px tall (<code>--target-comfortable</code>), 1px <code>--color-border-strong</code> edge, square corners, <code>--space-2</code> between segments so they wrap cleanly.")]),
    variants=p("Segmented groups wrap onto more lines on phones; toolbars stay on one line and are only used for short, single-word options.")
    + ex(segmented("v-cond", CONDS, "Used - Good"), "Segmented: the sell form's condition picker (five options, wraps on phones).")
    + ex(segmented("v-prob", ["Not as described", "Damaged", "Didn’t arrive"], "Damaged", legend="What’s wrong?"), "Segmented: Report a problem.")
    + ex(toolbar("v"), "Toolbar: joined buttons with <code>aria-pressed</code>; the pressed one carries the accent edge."),
    sizes=p("Segments have one size: 44px tall so they meet the comfortable touch target without a size switch. Toolbar buttons use the small button size (32px) because they sit in dense filter bars; use <code>.btn</code> without <code>--sm</code> when the toolbar is the main control on the screen.")
    + ex(toolbar("s-sm") + '<div class="btn-group" role="group" aria-label="Category medium"><button class="btn" type="button" aria-pressed="true">Shoes</button><button class="btn" type="button" aria-pressed="false">Tops</button></div>',
         "Toolbar small (32px) and medium (40px)."),
    states=p("Hover and focus are forced with <code>data-state</code> or an inline ring for review. Checked comes from the radio's <code>:checked</code>; invalid from <code>aria-invalid</code> on the inputs.")
    + state_matrix(STATES + ["Checked"], [("Segmented", lambda s: _seg_state(s if s != "checked" else "checked") if s != "active" else _seg_state("checked")),
                                         ("Toolbar", lambda s: toolbar(f"m-{s}", s if s in ("hover", "focus", "active") else "", 1 if s == "checked" else 0) if s != "disabled"
                                          else '<div class="btn-group" role="group" aria-label="Category disabled"><button class="btn btn--sm" type="button" aria-pressed="true" disabled>Shoes</button><button class="btn btn--sm" type="button" aria-pressed="false" disabled>Tops</button></div>')])
    + "<h3>Invalid</h3>"
    + ex(segmented("inv", CONDS, "", invalid=True) + '<span class="field__error" id="cond-error">Choose a condition</span>', "The sell form's invalid state: every segment gets the danger edge and the error sits under the group.")
    + "<h3>Both themes</h3>"
    + themes(segmented("th-d", CONDS[:3], "New without tags"), light=segmented("th-l", CONDS[:3], "New without tags")),
    responsive=ul("Segmented groups use <code>flex-wrap</code>: at 360px the five conditions wrap onto three lines, each segment keeping its full label. Never truncate or abbreviate a condition.",
                  "When a group would need more than three lines at 360px, switch to a " + comp("radio-group") + ".",
                  "Toolbars do not wrap; keep them to four short labels, and scroll the filter bar horizontally on phones rather than squeezing it."),
    theming=p("Segments read <code>--color-bg-surface</code>, <code>--color-border-strong</code> and, when checked, <code>--color-accent</code> with <code>--color-fg-on-accent</code>, so the dark theme inverts them to paper segments with ink labels. Toolbar buttons use the button tokens; the pressed one switches to <code>--color-accent-subtle</code> with an <code>--color-accent</code> edge.")
    + pre("""
/* A quieter segmented group for a filter sheet */
.filter-sheet .segmented input:checked + span { background: var(--color-accent-subtle); color: var(--color-fg-accent); }"""),
    accessibility=a11y(
        pattern="Segmented: native radio inputs in a <code>&lt;fieldset&gt;</code> with a <code>&lt;legend&gt;</code> (the APG Radio Group behaviour comes from the browser). Toolbar: <code>role=\"group\"</code> with an <code>aria-label</code>, each button a toggle with <code>aria-pressed</code>.",
        keyboard=[(kbd("Tab"), "Segmented: moves into the group onto the checked radio (or the first), then out. Toolbar: visits each button."),
                  (kbd("←") + " " + kbd("→") + " / " + kbd("↑") + " " + kbd("↓"), "Segmented: moves the selection to the previous or next option and checks it."),
                  (kbd("Space"), "Segmented: checks the focused option. Toolbar: toggles the focused button."),
                  (kbd("Enter"), "Toolbar: toggles. Segmented: submits the form, as radios do.")],
        focus="The input is visually hidden, so the ring is drawn on the segment (<code>input:focus-visible + span</code>) with the shared 2px ring and 2px offset.",
        labelling="The legend names the group (<i>Condition</i>); each segment's text names its option. Errors are linked with <code>aria-describedby</code> on the fieldset. Toolbar groups need an <code>aria-label</code> because they have no legend.",
        contrast=[("Selected label on accent", "--color-fg-on-accent", "--color-accent", 4.5), ("Segment edge on surface", "--color-border-strong", "--color-bg-surface", 3),
                  ("Segment edge on page", "--color-border-strong", "--color-bg-canvas", 3), ("Invalid edge", "--color-danger-solid", "--color-bg-surface", 3)],
        motion="Background changes over <code>--duration-fast</code>; nothing moves. Reduced motion zeroes the transition.",
        touch="Segments are 44px tall with 8px between them, so each is a comfortable target on its own."),
    content=ul("Labels are the answer, not a sentence: <i>Used - Good</i>, <i>Damaged</i>. Keep each to three words.",
               "Use the same casing and wording the rest of the product uses for the value (condition names match listing cards and filters exactly).",
               "The legend asks the question: <i>Condition</i>, <i>What’s wrong?</i>",
               "Do not preselect an option when the member must make a deliberate choice (condition, problem type); preselect only safe defaults."),
    do_dont=dodont([
        ("do", segmented("dd1", ["Not as described", "Damaged", "Didn’t arrive"], "", legend="What’s wrong?"), "Leave a consequential choice unselected and ask a clear question."),
        ("dont", segmented("dd2", ["Not as described", "Damaged", "Didn’t arrive"], "Not as described", legend="Type"), "Preselect the first problem type; members submit reports they did not mean."),
        ("do", segmented("dd3", ["Good", "Fair"], "Good"), "Two to six short options that fit the screen."),
        ("dont", '<div class="btn-group" role="group" aria-label="Condition toolbar"><button class="btn btn--sm" type="button" aria-pressed="true">New with tags</button><button class="btn btn--sm" type="button" aria-pressed="false">New without tags</button><button class="btn btn--sm" type="button" aria-pressed="false">Used - Excellent</button></div>',
         "Use a pressed toolbar for a form value; it does not submit and will overflow on phones. Use the segmented radios."),
    ]),
    tokens=token_table([("Segment background / edge", "--color-bg-surface / --color-border-strong"), ("Checked background / label", "--color-accent / --color-fg-on-accent"),
                        ("Pressed toolbar background / label / edge", "--color-accent-subtle / --color-fg-accent / --color-accent"),
                        ("Invalid edge", "--color-danger-solid"), ("Segment height", "--target-comfortable"), ("Gap between segments", "--space-2"),
                        ("Segment padding", "--space-4"), ("Label font", "--text-label"), ("Pressed layer", "--z-raised"), ("Transition", "--duration-fast / --ease-standard")]),
    code=pre("""
<fieldset aria-describedby="cond-error">
  <legend>Condition</legend>
  <div class="segmented">
    <label><input type="radio" name="cond" value="Used - Good" checked><span>Used - Good</span></label>
    <label><input type="radio" name="cond" value="Used - Fair"><span>Used - Fair</span></label>
  </div>
</fieldset>

<div class="btn-group" role="group" aria-label="Category">
  <button class="btn btn--sm" type="button" aria-pressed="true">Shoes</button>
  <button class="btn btn--sm" type="button" aria-pressed="false">Tops</button>
</div>""")
    + classes([("<code>.segmented</code>", "Wrapping row of radio segments; the input is transparent over its <code>span</code>."),
               ("<code>input:checked + span</code>", "Selected segment."), ("<code>input[aria-invalid=\"true\"] + span</code>", "Invalid edge."),
               ("<code>.btn-group</code>", "Joins buttons edge to edge; first and last keep the outer corners."),
               ("<code>.btn[aria-pressed=\"true\"]</code>", "Pressed toolbar button, raised above its neighbours.")]),
    sources=sources([("pages/sell/default", "condition segmented group"), ("pages/sell/invalid", "invalid segmented group"),
                     ("dialogs/report-problem/default", "problem type segmented group"), ("pages/my-listings/default", "status filter as pressed chips in a group")],
                    "none in the markup. <code>.btn-group</code> exists in the kit but no mock uses it yet; the status filter on My listings uses pressed chips in a <code>role=\"group\"</code>, which is the right choice there because the chips carry counts and wrap."),
)

# ---------------------------------------------------------------------------
# Link
# ---------------------------------------------------------------------------
EXT = ic("external", "icon icon--sm")


def _link(state: str, kind: str) -> str:
    st = {"default": "", "hover": ' data-state="hover"', "focus": ' data-state="focus"', "active": ' data-state="hover"', "disabled": ' aria-disabled="true"'}[state]
    if kind == "inline":
        return f'<p style="margin: 0;">I accept the <a href="#"{st}>terms</a>.</p>'
    if kind == "standalone":
        return f'<a class="link-standalone" href="#"{st}>{ic("arrow-left", "icon icon--sm")}Back to sales</a>'
    return f'<a class="link-standalone num" href="#"{st}>9400 1000 0000 0000 0482 13{EXT}<span class="visually-hidden">(opens USPS)</span></a>'


component(
    "link", "Link", "Actions",
    lead="Links take the member somewhere: to the terms, a seller's profile, a tracking page. They are ink and underlined, so they never rely on colour alone.",
    pills=["Native <code>&lt;a href&gt;</code>"],
    summary_variants="inline, standalone with icon, external",
    summary_states="default, hover, focus, active, disabled (aria-disabled)",
    overview=p(f"Use a link when activating it navigates: to another page, a section, a file or another site. If it changes something (saves, deletes, opens a dialog that acts), use a {comp('button')}. "
               "A link can look like a button when it is the primary way forward (<i>Sell an item</i>, <i>Sign in</i>); it stays an <code>&lt;a&gt;</code>.")
    + ul("<b>Inline</b> links sit in running text: <i>I accept the terms and marketplace rules</i>.",
         "<b>Standalone</b> links (<code>.link-standalone</code>) stand on their own line with an optional icon: <i>Back to sales</i>, the seller name on a listing.",
         "<b>External</b> links go off 12L (carrier tracking, the payment provider). They show the external icon and announce where they go."),
    anatomy=anatomy(
        f'<a class="link-standalone num" href="#">9400 1000 0000 0000 0482 13{EXT}</a>',
        [("40%", "30%"), ("88%", "30%"), ("40%", "70%")],
        [("Label", "Says where the link goes. Ink (<code>--color-fg-link</code>), <code>--text-label</code> when standalone."),
         ("External icon (optional)", "16px, after the label, only for links that leave 12L."),
         ("Underline", "1px, offset 0.15em; thickens to 2px on hover. It is how a link is recognised, so it is never removed in running text.")]),
    variants=ex(_link("default", "inline") + _link("default", "standalone") + _link("default", "external"),
                "Inline, standalone with a leading icon, external with a trailing icon and hidden destination text.")
    + "<h3>Links that look like buttons</h3>"
    + ex(btn("Sell an item", "primary", href="#") + btn("Sign in", href="#"), "Navigation that is the main way forward uses button styling but stays an anchor."),
    sizes=NA("Links inherit the size of the text they sit in; standalone links use --text-label."),
    states=p("12L does not style <code>:visited</code>: listings and orders are revisited constantly, and a second colour would add noise without helping.")
    + state_matrix(STATES, [("Inline", lambda s: _link(s, "inline")), ("Standalone", lambda s: _link(s, "standalone")), ("External", lambda s: _link(s, "external"))])
    + "<h3>Both themes</h3>" + themes(_link("default", "inline") + _link("default", "standalone") + _link("default", "external")),
    responsive=ul("Long links (tracking numbers, emails) break anywhere (<code>overflow-wrap: anywhere</code>) rather than overflowing at 320px.",
                  "Standalone links keep a 24px minimum height so they remain a target on touch screens.",
                  "Footer links wrap into rows with <code>--space-2</code> by <code>--space-6</code> gaps."),
    theming=p("Links read <code>--color-fg-link</code> and <code>--color-fg-link-hover</code>. In 12L both themes keep links the same colour as body text (ink in light, paper in dark) and rely on the underline, matching the brand's ink-on-paper restraint. Signal red is never a link colour.")
    + pre("""
/* Links inside an inverse surface inherit the surface text colour */
.consent a, .toast a { color: inherit; }"""),
    accessibility=a11y(
        pattern="Native <code>&lt;a href&gt;</code>; no role needed. A disabled link has no <code>href</code> or carries <code>aria-disabled=\"true\"</code> and is skipped by pointer events.",
        keyboard=[(kbd("Tab"), "Moves focus to the link."), (kbd("Enter"), "Follows the link. (Space scrolls the page; links do not respond to it.)")],
        focus="The shared 2px ink ring with 2px offset on <code>:focus-visible</code>; links inside inverse surfaces switch the ring to <code>--color-fg-inverse</code>.",
        labelling="The text says where it goes; never <i>click here</i> or <i>read more</i> on its own. External links add visually hidden text such as <i>(opens USPS)</i>. A link that opens a new tab says so.",
        contrast=[("Link on page", "--color-fg-link", "--color-bg-canvas", 4.5), ("Link on card", "--color-fg-link", "--color-bg-surface", 4.5), ("Hovered link", "--color-fg-link-hover", "--color-bg-surface", 4.5)],
        motion="No animation; the underline thickness changes instantly.",
        touch="Inline links rely on line height; standalone links are at least 24px tall (<code>--target-min</code>) and keep 8px from neighbouring targets."),
    content=ul("Name the destination: <i>marketplace rules</i>, <i>marcus_12</i>, <i>Back to sales</i>.",
               "Link the meaningful words in a sentence, not the whole sentence.",
               "Tracking numbers are links to the carrier, shown in tabular numerals.",
               "Do not link the same destination twice in one paragraph."),
    do_dont=dodont([
        ("do", '<p style="margin: 0;">I accept the <a href="#">terms</a> and <a href="#">marketplace rules</a></p>', "Link the names of the documents."),
        ("dont", '<p style="margin: 0;">To read the terms, <a href="#">click here</a>.</p>', "“Click here” says nothing out of context."),
        ("do", f'<a class="link-standalone num" href="#">9400 1000 0000 0000 0482 13{EXT}<span class="visually-hidden">(opens USPS)</span></a>', "Mark links that leave 12L and say where they go."),
        ("dont", '<a href="#" style="color: var(--color-brand); text-decoration: none;">View order</a>', "Red, un-underlined links: red is the brand mark, and colour alone does not identify a link."),
    ]),
    tokens=token_table([("Link", "--color-fg-link"), ("Link, hover", "--color-fg-link-hover"), ("Disabled", "--color-fg-disabled"), ("Focus ring", "--color-focus-ring"),
                        ("Standalone label", "--text-label"), ("Standalone minimum height", "--target-min"), ("Icon gap", "--space-1")]),
    code=pre("""
<p>I accept the <a href="/terms">terms</a>.</p>
<a class="link-standalone" href="/account/sales"><svg class="icon icon--sm" aria-hidden="true">…</svg>Back to sales</a>
<a class="link-standalone num" href="https://tools.usps.com/…">9400 1000 … 13<svg class="icon icon--sm" aria-hidden="true">…</svg><span class="visually-hidden">(opens USPS)</span></a>""")
    + classes([("<code>a</code>", "Ink, underlined, 2px underline on hover."), ("<code>.link-standalone</code>", "Label font, inline-flex with an icon, 24px minimum height."),
               ("<code>aria-disabled=\"true\"</code>", "Disabled look; pointer events off. Remove <code>href</code> as well."),
               ("<code>data-state=\"hover|focus\"</code>", "Documentation only.")]),
    sources=sources([("pages/register/default", "inline terms and rules links"), ("pages/order-detail/default", "external tracking link"),
                     ("pages/payouts/not-onboarded", "external payment-provider link styled as a button"), ("pages/listing-detail/default", "seller name link")],
                    "the tracking link had no hidden text naming its destination; the system adds <i>(opens USPS)</i>. Standalone links had no class; <code>.link-standalone</code> names them."),
)
drift("pages/order-detail/default", "External tracking link shows an icon but does not tell screen readers it leaves 12L.", "Link page documents visually hidden destination text, e.g. “(opens USPS)”.")

# ---------------------------------------------------------------------------
# Menu (dropdown)
# ---------------------------------------------------------------------------


def menu(mid: str, *, expanded: bool = True, hover: int = -1, focus: int = -1) -> str:
    items = [("edit", "Edit listing", "", ""), ("share", "Share", "", ""), ("download", "Download photos", "", ' aria-disabled="true"'),
             None, ("trash", "Withdraw listing", " menu__item--danger", "")]
    li = ""
    for i, it in enumerate(items):
        if it is None:
            li += '<li class="menu__divider" role="separator"></li>'
            continue
        icon, label, cls, extra = it
        st = ' data-state="hover"' if i == hover else (' data-state="focus"' if i == focus else "")
        li += f'<li role="none"><button class="menu__item{cls}" type="button" role="menuitem"{extra}{st} tabindex="-1">{ic(icon, "icon icon--sm")}{label}</button></li>'
    trig = (f'<button class="btn" type="button" aria-haspopup="menu" aria-expanded="{"true" if expanded else "false"}" aria-controls="{mid}">'
            f'Manage{ic("chevron-down", "icon icon--sm")}</button>')
    m = f'<ul class="menu" role="menu" id="{mid}" aria-label="Manage listing">{li}</ul>' if expanded else ""
    return f'<div class="menu-anchor">{trig}{m}</div>'


def checkable(mid: str) -> str:
    opts = ["Newest", "Price: low to high", "Price: high to low"]
    li = '<li role="none" class="menu__label">Sort by</li>' + "".join(
        f'<li role="none"><button class="menu__item" type="button" role="menuitemradio" aria-checked="{"true" if i == 0 else "false"}" tabindex="-1">{o}</button></li>' for i, o in enumerate(opts))
    return (f'<div class="menu-anchor"><button class="btn btn--sm" type="button" aria-haspopup="menu" aria-expanded="true" aria-controls="{mid}">Sort: Newest{ic("chevron-down", "icon icon--sm")}</button>'
            f'<ul class="menu" role="menu" id="{mid}" aria-label="Sort">{li}</ul></div>')


def icon_trigger(mid: str) -> str:
    return (f'<div class="menu-anchor"><button class="btn btn--ghost btn--icon" type="button" aria-label="More actions for Arizona sandals" aria-haspopup="menu" aria-expanded="true" aria-controls="{mid}">{ic("more")}</button>'
            f'<ul class="menu" role="menu" id="{mid}" aria-label="More actions"><li role="none"><button class="menu__item" type="button" role="menuitem" tabindex="-1">Copy link<kbd>Ctrl C</kbd></button></li>'
            f'<li role="none"><button class="menu__item" type="button" role="menuitem" tabindex="-1">Report listing</button></li></ul></div>')


component(
    "menu", "Menu", "Actions",
    lead="A menu button opens a short list of actions or choices: Manage on a listing you own, More actions on a row, Sort on the catalog toolbar.",
    pills=["APG Menu Button"],
    summary_variants="with icons, with shortcut, with section label, danger item, checkable (radio) items; text or icon-only trigger",
    summary_states="closed, open, item hover/focus, item disabled, item checked",
    overview=p(f"Use a menu when one trigger offers three to seven related actions and showing them all as {comp('button', 'buttons')} would crowd the screen, typically on phones or in list rows. "
               f"Do not use a menu for navigation between pages (use {comp('tabs')} or the {comp('top-bar')}), or for a form value that must submit (use a {comp('select')}).")
    + ul("<b>Action menu</b>: verbs that act on one object (<i>Edit listing</i>, <i>Share</i>, <i>Withdraw listing</i>). A destructive item is last, separated, in danger text, and opens a confirmation dialog.",
         "<b>Choice menu</b>: checkable items (<code>menuitemradio</code>) that change a view setting immediately, such as sort order."),
    anatomy=anatomy(
        '<div class="ds-float" style="min-height: 15rem; padding: 0;">' + menu("an-m") + "</div>",
        [("8%", "6%"), ("10%", "34%"), ("60%", "50%"), ("50%", "80%")],
        [("Trigger", "A button with a chevron, <code>aria-haspopup=\"menu\"</code> and <code>aria-expanded</code>."),
         ("Item", "32px tall (<code>--control-height-sm</code>), 16px icon, <code>--text-body-sm</code> label; whole row is the target."),
         ("Disabled item", "<code>aria-disabled=\"true\"</code>; stays focusable so it can be discovered, in <code>--color-fg-disabled</code>."),
         ("Divider and danger item", "A separator isolates the destructive item, which uses <code>--color-danger-fg</code>.")]),
    variants=p("Panels are <code>--color-bg-surface-raised</code> with <code>--shadow-3</code>, 2px corners and a 4px inner padding. They open below the trigger, aligned to its start edge, and flip above when there is no room.")
    + '<div class="ds-example"><div class="ds-float">' + menu("v-m1") + checkable("v-m2") + icon_trigger("v-m3") + '</div><div class="ds-example__caption"><span>Action menu with icons, divider and danger item · choice menu with a section label and checked item · icon-only trigger with a shortcut hint.</span></div></div>',
    sizes=NA("Menus have one size: 32px items with a 12rem minimum width that grows to the longest label."),
    states=matrix(["Closed", "Open", "Item hover", "Item focus"], [
        ("Action menu", [f'<div class="ds-float" style="min-height: 3rem; padding: 0;">{menu("s1", expanded=False)}</div>',
                         f'<div class="ds-float" style="padding: 0;">{menu("s2")}</div>',
                         f'<div class="ds-float" style="padding: 0;">{menu("s3", hover=0)}</div>',
                         f'<div class="ds-float" style="padding: 0;">{menu("s4", focus=1)}</div>'])], first="Menu")
    + ul("<b>Disabled item</b>: <i>Download photos</i> above, while the photos are still processing.", "<b>Checked item</b>: the current sort order, marked with a tick and <code>aria-checked=\"true\"</code>.",
         "<b>Trigger expanded</b>: <code>aria-expanded=\"true\"</code> while the menu is open; the trigger keeps its hover background.")
    + "<h3>Both themes</h3>" + themes(f'<div class="ds-float" style="padding: 0;">{menu("th-d")}</div>', light=f'<div class="ds-float" style="padding: 0;">{menu("th-l")}</div>'),
    responsive=ul("On phones (below 640px) an action menu with more than four items opens as a bottom sheet (" + comp("drawer") + ") instead of a floating panel, so items get 44px rows.",
                  "The panel never exceeds the viewport: <code>max-width: min(20rem, 100vw - 2 × --layout-margin)</code>; long labels wrap rather than truncate.",
                  "Row menus in lists stay visible on touch devices (no hover-only reveal)."),
    theming=p("The panel reads <code>--color-bg-surface-raised</code>, <code>--color-border-default</code> and <code>--shadow-3</code>; in the dark theme the raised surface is one step lighter than the page (ink-850 on ink-950) and the shadow darkens, so the panel still reads as floating. Item hover uses <code>--color-bg-subtle</code>.")
    + pre("""
.menu { --menu-min: 12rem; min-width: var(--menu-min); }"""),
    accessibility=a11y(
        pattern="WAI-ARIA APG Menu Button: trigger <code>button</code> with <code>aria-haspopup=\"menu\"</code>, <code>aria-expanded</code> and <code>aria-controls</code>; panel <code>role=\"menu\"</code> with an accessible name; items <code>role=\"menuitem\"</code> (or <code>menuitemradio</code>/<code>menuitemcheckbox</code>) with roving <code>tabindex</code>; dividers <code>role=\"separator\"</code>.",
        keyboard=[(kbd("Enter") + " / " + kbd("Space") + " / " + kbd("↓"), "On the trigger: opens the menu and focuses the first item."),
                  (kbd("↑"), "On the trigger: opens and focuses the last item. In the menu: previous item (wraps)."),
                  (kbd("↓"), "In the menu: next item (wraps)."), (kbd("Home") + " / " + kbd("End"), "First / last item."),
                  ("Printable character", "Moves to the next item starting with that letter (type-ahead)."),
                  (kbd("Enter") + " / " + kbd("Space"), "Activates the item and closes the menu; focus returns to the trigger."),
                  (kbd("Esc"), "Closes the menu and returns focus to the trigger."), (kbd("Tab"), "Closes the menu and moves focus on.")],
        focus="Focus moves into the menu on open and back to the trigger on close. The focused item shows <code>--color-bg-subtle</code> plus the ring when reached by keyboard.",
        labelling="The trigger names the object when it is icon-only (<i>More actions for Arizona sandals</i>). The panel is labelled by the trigger or an <code>aria-label</code>. Shortcuts are shown in a <code>&lt;kbd&gt;</code> and exposed with <code>aria-keyshortcuts</code>.",
        contrast=[("Item text on raised surface", "--color-fg-default", "--color-bg-surface-raised", 4.5), ("Item text on hover", "--color-fg-default", "--color-bg-subtle", 4.5),
                  ("Danger item", "--color-danger-fg", "--color-bg-surface-raised", 4.5), ("Section label", "--color-fg-subtle", "--color-bg-surface-raised", 4.5)],
        motion="The panel scales in from 96% and fades over <code>--duration-fast</code> with <code>--ease-enter</code>; it closes instantly. Reduced motion removes the scale.",
        touch="Items are 32px tall with the full row as target in floating menus; the bottom-sheet form on phones uses 44px rows."),
    content=ul("Items are verbs with the object when it is not obvious: <i>Edit listing</i>, <i>Withdraw listing</i>, <i>Copy link</i>.",
               "Order by frequency; destructive last, after a divider.", "An item that opens a dialog does not need an ellipsis; the dialog title confirms it.",
               "Choice menus show the current value in the trigger: <i>Sort: Newest</i>."),
    do_dont=dodont([
        ("do", f'<div class="ds-float" style="padding: 0; min-height: 15rem;">{menu("dd1")}</div>', "Put the destructive item last, after a divider, and confirm it in a dialog."),
        ("dont", '<div class="ds-float" style="padding: 0; min-height: 8rem;"><ul class="menu" role="menu" aria-label="Bad order"><li role="none"><button class="menu__item menu__item--danger" type="button" role="menuitem">Withdraw listing</button></li><li role="none"><button class="menu__item" type="button" role="menuitem">Edit listing</button></li></ul></div>', "Lead with the destructive item where a slip of the finger triggers it."),
        ("do", btn("Edit listing", "primary") + btn("Withdraw"), "With two actions, show both buttons (as listing detail does); a menu would hide them."),
        ("dont", f'<div class="ds-float" style="padding: 0; min-height: 3rem;">{icon_trigger("dd4").replace(" aria-label=\"More actions for Arizona sandals\"", " aria-label=\"More\"").split("<ul")[0]}</div></div>', "An icon-only trigger labelled just “More”: say more of what."),
    ]),
    tokens=token_table([("Panel background", "--color-bg-surface-raised"), ("Panel edge", "--color-border-default"), ("Panel shadow", "--shadow-3"),
                        ("Item hover / focus", "--color-bg-subtle"), ("Item text", "--color-fg-default"), ("Danger item", "--color-danger-fg"),
                        ("Disabled item", "--color-fg-disabled"), ("Item height", "--control-height-sm"), ("Panel padding", "--space-1"),
                        ("Panel radius / item radius", "--radius-md / --radius-sm"), ("Layer", "--z-dropdown"), ("Open animation", "--duration-fast / --ease-enter")]),
    code=pre("""
<div class="menu-anchor">
  <button class="btn" type="button" aria-haspopup="menu" aria-expanded="false" aria-controls="manage">Manage</button>
  <ul class="menu" role="menu" id="manage" aria-label="Manage listing" hidden>
    <li role="none"><button class="menu__item" type="button" role="menuitem" tabindex="-1">Edit listing</button></li>
    <li class="menu__divider" role="separator"></li>
    <li role="none"><button class="menu__item menu__item--danger" type="button" role="menuitem" tabindex="-1">Withdraw listing</button></li>
  </ul>
</div>""")
    + classes([("<code>.menu-anchor</code>", "Positioning context for the panel."), ("<code>.menu</code>", "The floating panel."),
               ("<code>.menu__item</code>", "An item; <code>--danger</code> for destructive."), ("<code>.menu__divider</code>", "Separator between groups."),
               ("<code>.menu__label</code>", "Non-interactive section label."), ("<code>aria-checked=\"true\"</code>", "Checked item (tick)."),
               ("<code>aria-disabled=\"true\"</code>", "Disabled item, still focusable."), ("<code>.menu--static</code>", "Documentation only: renders the panel in flow.")]),
    sources=sources([("pages/listing-detail/own", "owner actions Edit listing / Withdraw (a menu candidate on compact rows)"),
                     ("pages/catalog/default", "Sort select on the toolbar (choice-menu candidate)"), ("pages/sale-detail/default", "Add tracking / Cancel order actions")],
                    "no mock uses a dropdown menu yet; it is a core component documented from the kit's <code>.menu</code> styles so it is ready when list rows need row actions. The section label (<code>.menu__label</code>) was added during extraction."),
)
