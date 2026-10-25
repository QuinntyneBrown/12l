"""Pattern pages: compositions of components for a job, with the rules that span them."""
from ds import *

ICON_FOR = {"info": "info", "success": "check-circle", "warning": "alert", "danger": "x-circle"}


# ---------------------------------------------------------------------------
# Local markup helpers (mirror docs/mocks/_build/mk.py)
# ---------------------------------------------------------------------------
def fld(fid: str, label: str, value: str = "", *, help: str | None = None, error: str | None = None, optional: bool = False,
        type: str = "text", attrs: str = "", control: str = "") -> str:
    db = " ".join(x for x in [f"{fid}-help" if help else "", f"{fid}-error" if error else ""] if x)
    dba = f' aria-describedby="{db}"' if db else ""
    inv = ' aria-invalid="true"' if error else ""
    if not control:
        v = f' value="{esc(value)}"' if value else ""
        control = f'<input class="input" id="{fid}" type="{type}"{v}{dba}{inv}{(" " + attrs) if attrs else ""}>'
    opt = ' <span class="optional">(optional)</span>' if optional else ""
    h = f'<span class="field__help" id="{fid}-help">{help}</span>' if help else ""
    e = f'<span class="field__error" id="{fid}-error">{esc(error)}</span>' if error else ""
    return f'<div class="field"><label class="field__label" for="{fid}">{label}{opt}</label>{control}{h}{e}</div>'


def summary(errors: list[tuple[str, str]], title: str = "Fix these to continue", sid: str = "error-summary") -> str:
    items = "".join(f'<li><a href="#{f}">{esc(m)}</a></li>' for f, m in errors)
    return (f'<div class="alert alert--danger form-summary" role="alert" tabindex="-1" id="{sid}">{ic("x-circle")}'
            f'<div class="alert__body"><div class="alert__title">{title}</div><ul class="ds-plain-list">{items}</ul></div></div>')


def alrt(kind: str, title: str, text: str = "", actions: str = "", icon: str | None = None, role: str | None = None) -> str:
    r = f' role="{role}"' if role else (' role="alert"' if kind == "danger" else "")
    body = f'<div class="alert__title">{title}</div>' + (f"<div>{text}</div>" if text else "") + (f'<div class="alert__actions">{actions}</div>' if actions else "")
    return f'<div class="alert alert--{kind}"{r}>{ic(icon or ICON_FOR[kind])}<div class="alert__body">{body}</div></div>'


def bnr(kind: str, text: str, actions: str = "", dismiss: bool = True, icon: str | None = None) -> str:
    role = ' role="alert"' if kind == "danger" else ' role="status"'
    d = f'<button class="close" type="button" aria-label="Dismiss">{ic("close", "icon icon--sm")}</button>' if dismiss else ""
    a = f'<span class="alert__actions">{actions}</span>' if actions else ""
    return f'<div class="alert alert--{kind} banner"{role}>{ic(icon or ICON_FOR[kind])}<div class="alert__body"><span>{text}</span>{a}</div>{d}</div>'


def tst(kind: str, title: str, text: str = "", action: str | None = None, progress: bool = True) -> str:
    role = ' role="alert"' if kind == "danger" else ""
    a = f'<button class="toast__action" type="button">{action}</button>' if action else ""
    t = f'<div class="toast__text">{text}</div>' if text else ""
    pr = '<span class="toast__progress" aria-hidden="true"></span>' if progress and kind != "danger" else ""
    return (f'<div class="toast toast--{kind}"{role}>{ic(ICON_FOR[kind])}<div class="toast__body"><div class="toast__title">{title}</div>{t}{a}</div>'
            f'<button class="close" type="button" aria-label="Dismiss">{ic("close", "icon icon--sm")}</button>{pr}</div>')


def empt(icon: str, title: str, text: str = "", actions: str = "", cls: str = "", heading: str = "h3") -> str:
    t = f'<p class="empty__text">{text}</p>' if text else ""
    a = f'<div class="empty__actions">{actions}</div>' if actions else ""
    return f'<div class="empty {cls}"><div class="empty__icon">{ic(icon, "icon icon--lg")}</div><{heading} class="empty__title">{title}</{heading}>{t}{a}</div>'


def dlg(title: str, body: str, footer: str, *, did: str, desc: str | None = None, icon: str | None = None, icon_kind: str = "info", size: str = "", top: str = "") -> str:
    ih = f'<div class="dialog__icon dialog__icon--{icon_kind}" aria-hidden="true">{ic(icon)}</div>' if icon else ""
    d = f'<p id="{did}-desc" class="text-muted ds-dialog-desc">{desc}</p>' if desc else ""
    dd = f' aria-describedby="{did}-desc"' if desc else ""
    sz = f" dialog__panel--{size}" if size else ""
    t = f'<div class="ds-dialog-top">{top}</div>' if top else ""
    return (f'<div class="backdrop"></div><div class="dialog" role="dialog" aria-modal="true" aria-labelledby="{did}-title"{dd}>'
            f'<div class="dialog__panel{sz}"><div class="dialog__header">{ih}<div class="ds-grow"><h2 class="dialog__title" id="{did}-title">{title}</h2>{d}</div>'
            f'<button class="btn btn--ghost btn--icon" type="button" aria-label="Close">{ic("close")}</button></div>{t}'
            f'<div class="dialog__body stack">{body}</div><div class="dialog__footer">{footer}</div></div></div>')


def timer(text: str = "9:41", kind: str = "") -> str:
    k = f" timer--{kind}" if kind else ""
    return f'<p class="timer{k}" role="timer" aria-live="off">{ic("clock")}<span>Reserved for you · <span class="num">{text}</span> left</span></p>'


def fake_page(inner: str) -> str:
    """Background content under an overlay; inert so it cannot take focus."""
    return f'<div class="ds-stage__page" inert aria-hidden="true">{inner}</div>'


def item_row(key: str, meta: str = "") -> str:
    it = ITEMS[key]
    meta = meta or f'{esc(it["brand"])} · {"Men’s US 12" if it["cat"] == "Shoes" else "Men’s L"}'
    return (f'<div class="item-row"><div class="thumb">{photo(key, tag=False, alt="")}</div>'
            f'<div class="item-row__body"><span class="item-row__title">{esc(it["title"])}</span><span class="item-row__meta">{meta}</span></div></div>')


def status(label: str, mod: str) -> str:
    return f'<span class="status status--{mod}">{label}</span>'


def topbar_mini(cur: str = "") -> str:
    nav = "".join(f'<a class="nav-link" href="#"{" aria-current=\"page\"" if k == cur else ""}>{k}</a>' for k in ["Shoes", "Tops", "Outerwear", "Bottoms"])
    return (f'<header class="topbar"><button class="btn btn--ghost btn--icon topbar__menu" type="button" aria-label="Open menu" aria-expanded="false">{ic("menu")}</button>'
            f'{logo()}<nav class="topbar__nav" aria-label="Primary (example)">{nav}</nav><span class="topbar__spacer"></span>'
            f'<div class="topbar__actions"><a class="btn btn--ghost btn--icon topbar__search-btn" href="#" aria-label="Search">{ic("search")}</a>'
            f'<a class="nav-link topbar__sell" href="#">{ic("plus")}Sell</a><a class="avatar avatar--sm ds-no-underline" href="#" aria-label="Your account, Marcus Bell">MB</a></div></header>')


# ---------------------------------------------------------------------------
# Forms
# ---------------------------------------------------------------------------
_sell_invalid = (
    '<form class="stack stack--lg" novalidate aria-labelledby="pf-h">'
    '<h2 class="ds-h4" id="pf-h">List an item</h2>'
    + summary([("pf-title", "Title must be 5 to 80 characters"), ("pf-price", "Enter a price from $1.00 to $5,000.00")], sid="pf-summary")
    + '<section class="form-section" aria-labelledby="pf-s1"><h2 id="pf-s1">The item</h2>'
    + fld("pf-title", "Title", "AF1", help="Brand, model and colour. 5–80 characters.", error="Title must be 5 to 80 characters")
    + '<div class="form-row">'
    + fld("pf-cond", "Condition", control='<select class="select" id="pf-cond"><option>Used - Good</option><option>Used - Excellent</option></select>')
    + fld("pf-price", "Price", control='<div class="input-group"><span class="addon">$</span><input class="input" id="pf-price" inputmode="decimal" value="0.99" aria-invalid="true" aria-describedby="pf-price-error"></div>',
          error="Enter a price from $1.00 to $5,000.00")
    + '</div></section>'
    + f'<div class="form-actions form-actions--split">{btn("Save draft")}{btn("List item", "primary", attrs="type=\"submit\"")}</div></form>')

_signin_busy = (
    '<form class="stack" novalidate aria-labelledby="si-h"><h2 class="ds-h4" id="si-h">Sign in</h2>'
    + fld("si-email", "Email", "marcus.bell@example.com", type="email", attrs="readonly autocomplete=\"email\"")
    + fld("si-pw", "Password", "xxxxxxxxxxxx", type="password", attrs="readonly autocomplete=\"current-password\"")
    + btn("Sign in", "primary lg block", attrs='type="submit" aria-busy="true"') + "</form>")

pattern(
    "forms", "Forms",
    lead="How 12L asks for information: one column, labels above, errors after the first submit, a summary that links to every problem, and a busy button that keeps the layout still.",
    covers="Layout, labels, validation timing, error summary, submit and success states, drafts, destructive confirmations.",
    overview=p("Every 12L form follows one shape so a member who has signed up, listed an item and checked out never has to relearn it. "
               f"It is built from {comp('form-field')}, {comp('text-field')}, {comp('select')}, {comp('checkbox')}, {comp('radio-group')}, {comp('file-upload')} and {comp('form-layout')}, "
               f"with {comp('alert')} for the error summary and {comp('button')} for the actions.")
    + ul("<b>One column</b>, labels above fields. Pairs that belong together (City + State, ZIP + Country, Condition + Price) share a <code>.form-row</code> from 640px.",
         "<b>Ask only what is needed.</b> The sell form has no size input at all: picking a category shows the fixed size (men’s US 12 or L).",
         "<b>Validate on submit first</b>, then re-validate each field as it changes, so members are not scolded while typing.",
         "<b>Never lose input.</b> Server errors keep every value and add a reference (<i>Ref 0c4e-7b21</i>).",
         "<b>One primary action</b>, last in the actions row: <i>List item</i>, <i>Join 12L</i>, <i>Pay $94.00</i>."),
    when=table(["Situation", "Use", "Example in the mocks"], [
        ["Two to five fields, one goal", "Auth card layout (<code>.auth-card</code>), block primary button", "Sign in, Join 12L, Reset your password"],
        ["Long form in sections", f"<code>.form-section</code> with h2 per section, sticky {comp('form-layout', 'form actions')}", "Sell an item, Edit listing"],
        ["Two-step purchase", "Steps as sections in one page, order summary beside", "Checkout: Ship to, Pay"],
        ["A decision with one to three fields", f"{comp('dialog')} with the fields in its body", "Change password, Report problem, Add tracking"],
        ["A setting that applies at once", f"{comp('switch')} plus a Save button for the group", "Email settings"],
        ["A destructive action", "Confirmation dialog naming the loss, danger button", "Withdraw listing, Close account"],
    ]),
    structure=p("A long form, as the sell form shows it after a refused publish: error summary first, then sections, then the actions row. Focus moves to the summary; each link jumps to its field.")
    + ex(f'<div class="ds-form-demo">{_sell_invalid}</div>', "Summary links use the field id; each field keeps its own message, linked with aria-describedby.", stack=True)
    + "<h3>Short form, submitting</h3>"
    + ex(f'<div class="ds-form-demo ds-form-demo--narrow">{_signin_busy}</div>', "Submitting: fields read-only (not disabled, so values stay readable and announced), button busy, nothing shifts.", stack=True),
    states=table(["State", "What changes", "Mock"], [
        ["Default", "Empty or prefilled fields; help text only where a rule is not obvious.", f'<a href="../../mocks/pages/register/default.html">register/default</a>'],
        ["Invalid", "Summary at the top (<code>role=\"alert\"</code>, <code>tabindex=\"-1\"</code>, focused), every error inline with <code>aria-invalid</code>.", f'<a href="../../mocks/pages/sell/invalid.html">sell/invalid</a>'],
        ["Submitting", "Primary button <code>aria-busy</code>; fields <code>readonly</code>; secondary actions disabled.", f'<a href="../../mocks/pages/sell/submitting.html">sell/submitting</a>'],
        ["Success", "Short form: replace the form with the next step (<i>Check your email</i>). Long form: success alert above, form stays.", f'<a href="../../mocks/pages/register/success.html">register/success</a>'],
        ["Server error", "Danger alert above the form with a reference; input kept; same button retries.", f'<a href="../../mocks/pages/register/error.html">register/error</a>'],
        ["Draft saved", "Success alert with a link to where the draft lives; the form stays editable.", f'<a href="../../mocks/pages/sell/draft-saved.html">sell/draft-saved</a>'],
        ["Locked / limited", "Warning alert with the wait time; the form stays visible.", f'<a href="../../mocks/pages/sign-in/locked.html">sign-in/locked</a>'],
    ])
    + "<h3>Validation timing</h3>"
    + ul("On first submit: validate everything, render the summary and every inline error at once, move focus to the summary.",
         "After that: re-validate a field on <code>input</code> (clear the error as soon as it is fixed) and on <code>blur</code> (add it back if it breaks again).",
         "Never validate on the first <code>blur</code> of an untouched field, and never disable the submit button to signal invalid input.",
         "Server-only checks (<i>That display name is taken</i>) return in the same summary and inline format."),
    responsive=ul("Forms are one column at every width; <code>.form-row</code> pairs split into two columns from 640px.",
                  "Long forms cap at 44rem (<code>.page--form</code>) and auth forms at 24rem so lines stay readable on desktop.",
                  "On phones the primary button is full width and large; on the sell form the actions row sticks to the bottom (<code>.form-actions--sticky</code>).",
                  "Numeric fields set <code>inputmode</code> (<code>numeric</code> for ZIP, <code>decimal</code> for price) and <code>autocomplete</code> so phones show the right keyboard and autofill."),
    accessibility=ul("Every control has a visible <code>&lt;label for&gt;</code>; help and errors are joined with <code>aria-describedby</code>. Groups of checkboxes or radios sit in a <code>&lt;fieldset&gt;</code> with a <code>&lt;legend&gt;</code>.",
                     "Forms use <code>novalidate</code> so 12L’s messages replace the browser’s; errors are text plus an icon, never colour alone.",
                     "The error summary is announced (<code>role=\"alert\"</code>) and focused; links move focus to the field (WCAG 3.3.1, 3.3.3).",
                     "Required fields are the default; optional ones say <i>(optional)</i>. Nothing relies on an asterisk.",
                     "Busy buttons keep their name and set <code>aria-busy</code>; read-only fields stay in the tab order.",
                     "Re-entering information is avoided (WCAG 3.3.7): the saved address is preselected at checkout, the email is prefilled after a failed sign-in.",
                     "Authentication allows paste and password managers (WCAG 3.3.8): no copy blocking, <code>autocomplete</code> on every credential field."),
    content=ul("Labels are nouns (<i>Display name</i>, <i>Street address</i>); help text states the rule (<i>3–30 letters, numbers, _ or -. Shown publicly.</i>).",
               "Errors say what to do, not what went wrong: <i>Enter a 5-digit ZIP code</i>, <i>Choose a rating</i>, <i>Title must be 5 to 80 characters</i>.",
               "The summary title is <i>Fix these to continue</i>, or names the problem when there is one (<i>Check the price range</i>).",
               "Server errors: what failed, what to do, a reference: <i>Couldn’t create your account. Try again in a moment. Ref 0c4e-7b21</i>.",
               f"See {patt('content-and-tone')} for verbs and numbers."),
    do_dont=dodont([
        ("do", fld("dd-zip", "ZIP code", "1120", error="Enter a 5-digit ZIP code", attrs='inputmode="numeric"'), "Say what to enter, next to the field, linked to it."),
        ("dont", fld("dd-zip2", "ZIP code", "1120", error="Invalid input"), "A message that names no fix."),
        ("do", btn("Save draft") + btn("List item", "primary", attrs='type="submit"'), "Keep the submit button enabled; explain problems on submit."),
        ("dont", btn("Save draft") + btn("List item", "primary", attrs="disabled"), "A disabled submit button with no reason leaves members guessing."),
    ]),
    sources=sources([("pages/sell/invalid", "error summary and inline errors"), ("pages/sell/submitting", "busy publish"),
                     ("pages/register/invalid", "every error at once"), ("pages/register/success", "form replaced by next step"),
                     ("pages/sign-in/submitting", "read-only fields"), ("pages/checkout/invalid", "address errors"),
                     ("pages/edit-profile/success", "success alert above the form"), ("dialogs/change-password/invalid", "form in a dialog")]),
)

# ---------------------------------------------------------------------------
# Feedback and loading
# ---------------------------------------------------------------------------
_skel_rows = "".join('<li class="ds-skel-row"><span class="skeleton skeleton--rect ds-skel-thumb"></span><div class="stack stack--sm ds-grow">'
                     '<span class="skeleton skeleton--text"></span><span class="skeleton skeleton--text"></span></div></li>' for _ in range(3))

pattern(
    "feedback-and-loading", "Feedback and loading",
    lead="Every action gets an answer in the place the member is looking: inline for a field, on the button for a submit, a toast for something done elsewhere, a banner for something that lasts.",
    covers="Which feedback for which action; skeleton vs spinner vs progress; optimistic updates and undo.",
    overview=p("Feedback in 12L is quiet and close to the action. A member who taps <i>Pay $94.00</i> sees that button work; a member whose price change saved sees a toast with <i>Undo</i>; "
               "a member who is offline sees a banner that stays until the connection comes back.")
    + ul("<b>Inline</b> (field errors, the reservation timer) for feedback about one thing on screen.",
         "<b>Button busy</b> for the action just pressed; never a full-page spinner for a form submit.",
         f"<b>{comp('alert')}</b> inside the page for results of that page’s form: <i>Draft saved</i>, <i>Profile saved</i>, <i>Your bank declined the card</i>.",
         f"<b>{comp('toast')}</b> for something that finished and does not need the member now: <i>Listing published · View listing</i>.",
         f"<b>Banner</b> for a condition that persists across pages: offline, unverified email, payout returned.",
         f"<b>{comp('dialog')}</b> only when the member must decide before going on."),
    when=table(["Waiting for", "Use", "Why"], [
        [f"A page or list to load", f"{comp('skeleton')} in the shape of the content", "The layout does not jump when data arrives; members see what is coming."],
        ["A button’s action", f"Busy button (spinner inside, <code>aria-busy</code>)", "Feedback where the member clicked; width kept."],
        ["Something under a second inside a small area", f"{comp('spinner')}", "A skeleton would flash."],
        ["A known amount (photo upload)", f"{comp('progress')} with a value", "Members can judge how long is left."],
        ["A countdown with a deadline", "Timer (<code>role=\"timer\"</code>) plus a banner at thresholds", "The reservation must be visible without being noisy."],
    ]),
    structure=p("Loading a list: the skeleton keeps the final shape, the container says it is busy, and the real rows replace it in place.")
    + ex(f'<ul class="ds-skel-list" aria-busy="true" aria-label="Loading purchases">{_skel_rows}</ul>', "Skeleton rows are aria-hidden by shape; the list carries aria-busy and a label.", stack=True)
    + "<h3>Result of a page action</h3>"
    + ex(alrt("success", "Draft saved", 'Finish it any time from <a href="#">your listings</a>.', role="status")
         + alrt("danger", "Your bank declined the card", "Insufficient funds. Try another card — the item is still reserved for you."), stack=True)
    + "<h3>Optimistic update with undo</h3>"
    + stage(fake_page(f'<div class="ds-h4">Your listings</div>{item_row("arizona", "Arizona sandals · $40")}')
            + f'<div class="toast-region" role="status" aria-live="polite">{tst("success", "Price updated to $40", "Arizona sandals", "Undo")}</div>',
            "16rem", "The list shows $40 immediately; the toast offers Undo for its lifetime and pauses on hover and focus."),
    states=table(["State", "Feedback", "Mock"], [
        ["Loading a page", "Skeleton of the page’s own content; header and nav render at once.", '<a href="../../mocks/pages/catalog/loading.html">catalog/loading</a>'],
        ["Saving a form", "Busy primary button; fields read-only.", '<a href="../../mocks/pages/edit-listing/submitting.html">edit-listing/submitting</a>'],
        ["Saved", "Success alert above the form (<code>role=\"status\"</code>).", '<a href="../../mocks/pages/edit-listing/success.html">edit-listing/success</a>'],
        ["Done elsewhere", "Toast with an action.", '<a href="../../mocks/notifications/toast/with-action.html">toast/with-action</a>'],
        ["Failed to save", "Danger toast that stays, with <i>Try again</i>.", '<a href="../../mocks/notifications/toast/danger.html">toast/danger</a>'],
        ["Offline", "Warning banner that cannot be dismissed while offline; cached content stays.", '<a href="../../mocks/pages/catalog/offline.html">catalog/offline</a>'],
    ]),
    responsive=ul("Toasts stack at the bottom, full width with 16px margins on phones; from 640px they are 24rem wide at the bottom right.",
                  "Banners are full width under the top bar at every size; their actions wrap below the text on phones.",
                  "Skeletons use the same grid as the content (2-up listing cards on phones, 4-up on desktop)."),
    accessibility=ul("Success and info messages use <code>role=\"status\"</code> (polite); danger messages use <code>role=\"alert\"</code>. The toast region exists on page load so announcements are not lost.",
                     "Busy containers set <code>aria-busy=\"true\"</code> and an <code>aria-label</code> (<i>Loading listings</i>); skeleton shapes are not announced.",
                     "Toasts pause their timer on hover and focus and are reachable by keyboard; error toasts never auto-dismiss (WCAG 2.2.1).",
                     "The reservation timer is <code>aria-live=\"off\"</code> so it does not announce every second; threshold banners announce instead.",
                     "Reduced motion stops the skeleton shimmer and slide-ins; spinners keep turning because they carry meaning."),
    content=ul("Past tense for done things: <i>Draft saved</i>, <i>Payment confirmed</i>, <i>Price updated to $40</i>.",
               "Name the object: <i>Listing published · Air Force 1 ’07 is live.</i>",
               "Errors say what is safe: <i>Couldn’t withdraw. Your listing is still live.</i>",
               "No <i>Loading…</i> text in skeletons; spinners carry a visually hidden label of what is loading."),
    do_dont=dodont([
        ("do", btn("Pay $94.00", "primary", attrs='aria-busy="true"'), "Show progress on the button that was pressed."),
        ("dont", f'<span class="spinner spinner--lg" role="status"><span class="visually-hidden">Loading</span></span>', "A full-page spinner for a form submit hides the member’s input and loses their place."),
        ("do", tst("danger", "Couldn’t save your draft", "Check your connection.", "Try again"), "Errors persist and offer a retry."),
        ("dont", tst("success", "Error!", "Something happened."), "A success-styled toast for an error, with no detail."),
    ]),
    sources=sources([("pages/catalog/loading", "skeleton grid"), ("pages/purchases/loading", "skeleton rows"), ("pages/checkout/declined", "page-level danger alert"),
                     ("notifications/toast/with-action", "Undo"), ("notifications/toast/danger", "persistent error"), ("pages/catalog/offline", "offline banner"),
                     ("pages/sell/draft-saved", "success alert")]),
)

# ---------------------------------------------------------------------------
# Empty and error states
# ---------------------------------------------------------------------------
pattern(
    "empty-and-error-states", "Empty and error states",
    lead="When there is nothing to show, say why in one line and offer the one action that fixes it. When something broke, say what is safe and give a reference.",
    covers="First-run, no-results, error-as-empty and full error pages; copy formulas and when to use which.",
    overview=p(f"All four empty states and every error state use the {comp('empty-state')} component (icon, title, one sentence, one action) or, for whole pages, the {comp('error-page')} layout. "
               "They keep the page shell (top bar, account tabs, filters) so the member can still go somewhere else."),
    when=table(["Situation", "Variant", "Example"], [
        ["Nothing exists yet", "First-run: neutral icon, encouraging line, primary action that creates", "<i>Nothing bought yet. Everything in the catalog already fits.</i> · Browse the catalog"],
        ["Filters or search hide everything", "No results (<code>.empty--compact</code>): suggest loosening, action clears", "<i>No items match. Try fewer filters or a different word.</i> · Clear search and filters"],
        ["The list failed to load", "Error as empty (<code>.empty--error</code>): danger icon, reference, Try again", "<i>Couldn’t load purchases. Ref 51ce-0a92</i> · Try again"],
        ["Work is done", "Positive empty: check icon", "<i>Queue clear. New reports and order problems land here.</i>"],
        ["The whole page is gone", f"{comp('error-page')}: 404, 403, 500, offline, maintenance", "<i>Page not found</i>, <i>You can’t view this page</i>"],
    ]),
    structure=ex(empt("bag", "Nothing bought yet", "Everything in the catalog already fits.", btn("Browse the catalog", "primary")), "First-run, inside the Purchases tab.")
    + ex(empt("search", "No items match", "Try fewer filters or a different word.", btn("Clear search and filters", "primary"), cls="empty--compact"), "No results, inside the catalog grid area; the filters stay visible beside it.")
    + ex(empt("refresh", "Couldn’t load purchases", 'Something went wrong on our side. <span class="ref">Ref 51ce-0a92</span>', btn("Try again", "primary", icon="refresh"), cls="empty--error"), "Error as empty: the shell and tabs still work."),
    states=table(["Page", "Empty", "No results", "Error"], [
        ["Catalog", '<a href="../../mocks/pages/catalog/empty.html">Nothing listed yet</a>', '<a href="../../mocks/pages/catalog/no-results.html">No items match</a>', '<a href="../../mocks/pages/catalog/error.html">Couldn’t load items</a>'],
        ["Purchases", '<a href="../../mocks/pages/purchases/empty.html">Nothing bought yet</a>', "—", '<a href="../../mocks/pages/purchases/error.html">Couldn’t load purchases</a>'],
        ["My listings", '<a href="../../mocks/pages/my-listings/empty.html">Nothing listed yet</a>', '<a href="../../mocks/pages/my-listings/filtered.html">filtered</a>', '<a href="../../mocks/pages/my-listings/error.html">Couldn’t load your listings</a>'],
        ["Payouts", '<a href="../../mocks/pages/payouts/empty.html">No payouts yet</a>', "—", '<a href="../../mocks/pages/payouts/error.html">Couldn’t load payouts</a>'],
        ["Moderation queue", '<a href="../../mocks/pages/moderation-queue/empty.html">Queue clear</a>', "—", '<a href="../../mocks/pages/moderation-queue/error.html">error</a>'],
        ["Audit log", '<a href="../../mocks/pages/audit-log/empty.html">No actions yet</a>', '<a href="../../mocks/pages/audit-log/no-results.html">no-results</a>', '<a href="../../mocks/pages/audit-log/error.html">error</a>'],
    ]),
    responsive=ul("Empty states centre in the space the content would have used; on phones they keep 48px of vertical padding, compact ones 32px.",
                  "Actions wrap and centre; the primary comes first.",
                  "Full error pages align left with a large code (404 with the red L treatment) and stack their actions on phones."),
    accessibility=ul("The empty-state title is a real heading at the right level for its place (h2 for a page body, h3 inside a section).",
                     "The icon is decorative (<code>aria-hidden</code>); the title carries the meaning.",
                     "When an error replaces a list after a retry, focus stays on the Try again button and the new state is announced through the page’s status region.",
                     "Reference codes are text, selectable and copyable, in the mono face."),
    content=ul("<b>Empty formula</b>: title states the fact (<i>No sales yet</i>), one line says what happens next or why it is fine (<i>Sold items show up here with what to do next.</i>), one action.",
               "<b>No-results formula</b>: <i>No items match</i> + how to widen + <i>Clear search and filters</i>.",
               "<b>Error formula</b>: <i>Couldn’t load {thing}</i> + <i>Something went wrong on our side.</i> + <i>Ref xxxx-xxxx</i> + <i>Try again</i>. Never blame the member for a server failure.",
               "Titles are short and sentence case; no exclamation marks, no jokes in errors."),
    do_dont=dodont([
        ("do", empt("tag", "No sales yet", "Sold items show up here with what to do next.", btn("Sell an item", "primary"), cls="empty--compact"), "One line, one action that fixes it."),
        ("dont", empt("x-circle", "Oops! No data found", "There are no records to display at this time.", btn("OK") + btn("Go back") + btn("Refresh"), cls="empty--compact empty--error"), "Danger styling for a normal empty list, vague copy and three actions."),
    ]),
    sources=sources([("pages/purchases/empty", ""), ("pages/catalog/no-results", ""), ("pages/purchases/error", ""), ("pages/moderation-queue/empty", "positive empty"),
                     ("pages/not-found/default", "full error page"), ("pages/offline/default", ""), ("pages/server-error/default", "")]),
)

# ---------------------------------------------------------------------------
# Navigation and page structure
# ---------------------------------------------------------------------------
_subnav = ('<nav class="subnav" aria-label="Account (example)">' + "".join(
    f'<a class="tab" href="#"{" aria-current=\"page\"" if t == "Purchases" else ""}>{t}</a>' for t in ["Overview", "Listings", "Purchases", "Sales", "Payouts", "Profile", "Emails", "Settings"]) + "</nav>")

pattern(
    "navigation-and-page-structure", "Navigation and page structure",
    lead="One top bar, one page header, one main column. Categories live in the top bar, account areas in tabs, and depth is shown with breadcrumbs only where pages nest.",
    covers="App shell, page header, account tabs, breadcrumbs, mobile menu sheet, admin shell, back behaviour.",
    overview=p(f"Every member page has the same skeleton: {comp('skip-link')}, {comp('top-bar')}, an optional banner, the page header (h1, subtitle, actions), the content, and the {comp('footer')}. "
               "Admin pages swap the top bar for the admin variant (red <i>Admin</i> tag, Queue and Audit log) and drop the footer. Auth pages centre a narrow card under the large logo.")
    + table(["Shell", "Used by", "Parts"], [
        ["App", "Catalog, listing, account, orders, selling", "Top bar (categories, search, Sell, avatar), page, footer"],
        ["Account", "Account overview and its seven tabs", "App shell plus account tabs under the top bar"],
        ["Auth", "Sign in, Join, reset and verify", "Large logo, 24rem card, no top bar"],
        ["Admin", "Moderation queue, report and problem detail, audit log", "Admin top bar, no footer"],
        ["Bare", "Checkout", "Top bar with the logo only; no footer, so nothing pulls the buyer away while the item is reserved"],
    ]),
    when=table(["Need", "Use", "Not"], [
        ["Move between catalog categories", "Top-bar nav links with the red current bar", "Tabs"],
        ["Move between sibling areas of one hub (account)", f"{comp('tabs')} as links (<code>aria-current=\"page\"</code>)", "A sidebar: 12L has eight short areas, tabs fit"],
        ["Show where a nested page sits", f"{comp('breadcrumb')}: Purchases / Order 12L-48213", "Breadcrumbs on top-level pages"],
        ["Navigation on phones", "Menu button opens the full-screen menu sheet", "A hamburger on desktop"],
        ["Progress through an order", f"{comp('stepper')} (order timeline)", "Breadcrumbs"],
    ]),
    structure=ex(f'<div class="ds-shell-demo">{topbar_mini("Shoes")}<div class="ds-shell-demo__body">{_subnav}'
                 '<div class="page-header"><div><h2 class="ds-h1">Purchases</h2><p class="subtitle">5 orders</p></div></div></div></div>',
                 "Top bar with the current category bar, account tabs and page header. Resize the window: the nav moves into the menu below 768px.", show_code=False)
    + "<h3>Mobile menu sheet</h3>"
    + stage('<div class="menu-sheet" role="dialog" aria-modal="true" aria-label="Menu (example)"><div class="menu-sheet__head">' + logo()
            + f'<button class="btn btn--ghost btn--icon" type="button" aria-label="Close menu">{ic("close")}</button></div>'
            + '<div class="menu-sheet__body"><ul class="menu-sheet__links">' + "".join(f'<li><a href="#">{t}{ic("chevron-right")}</a></li>' for t in ["Shoes", "Tops", "Outerwear", "Bottoms"])
            + '</ul><ul class="menu-sheet__links menu-sheet__links--small">' + "".join(f'<li><a href="#">{t}</a></li>' for t in ["Your account", "Purchases", "Sales"])
            + f'</ul></div><div class="menu-sheet__foot">{btn("Sell an item", "primary", icon="plus")}</div></div>', "30rem",
            "The sheet is a modal dialog: focus moves in, Esc and Close return focus to the menu button."),
    states=ul("<b>Current page</b>: top-bar links and tabs use <code>aria-current=\"page\"</code> and the 3px red bar; nothing else is red.",
              "<b>Guest</b>: avatar becomes <i>Sign in</i>; Sell still shows and leads to sign-in.",
              "<b>Unverified or suspended</b>: a banner sits above the top bar on every page until resolved.",
              "<b>Admin</b>: the shell changes so administrators always know they are acting as staff.",
              "<b>Back</b>: browser back always works; dialogs and sheets do not add history entries; filters and search update the URL so back restores them."),
    responsive=table(["Width", "Top bar", "Account tabs"], [
        ["&lt; 768px", "Menu button, logo, search icon, avatar", "Scroll horizontally; the current tab stays in view"],
        ["768–1023px", "Category links and Sell appear", "Fit on one row"],
        ["≥ 1024px", "Search field replaces the search icon", "One row"],
    ]),
    accessibility=ul("Landmarks: <code>header</code>, <code>nav</code> with distinct <code>aria-label</code>s (<i>Primary</i>, <i>Account</i>, <i>Footer</i>), one <code>main</code>, <code>footer</code>.",
                     "The skip link is the first focusable element and jumps to <code>#main</code>.",
                     "One h1 per page, in the page header; sections use h2.",
                     "The menu button has <code>aria-expanded</code> and <code>aria-controls</code>; the sheet traps focus and returns it on close.",
                     "Page titles follow <i>Page · 12L</i> so tabs and history are distinguishable (WCAG 2.4.2)."),
    content=ul("Nav labels are single nouns: <i>Shoes</i>, <i>Purchases</i>, <i>Payouts</i>. The email settings tab is <i>Emails</i> to stay short.",
               "Page h1 matches the nav label that led there.",
               "Subtitles give a count or a state, not a description: <i>5 orders</i>, <i>Read-only · kept for 2 years</i>."),
    do_dont=dodont([
        ("do", _subnav.replace("Account (example)", "Account (do example)"), "Tabs as links for sibling areas, current marked with aria-current."),
        ("dont", '<nav aria-label="Breadcrumb (dont example)"><ol class="breadcrumb"><li><a href="#">Home</a></li><li><span aria-current="page">Catalog</span></li></ol></nav>', "Breadcrumbs on a top-level page repeat the top bar."),
    ]),
    sources=sources([("pages/catalog/category", "current category"), ("pages/purchases/default", "account tabs"), ("dialogs/nav-menu/default", "menu sheet"),
                     ("pages/sign-in/default", "auth shell"), ("pages/moderation-queue/default", "admin shell"), ("pages/order-detail/default", "breadcrumb"), ("pages/checkout/default", "bare shell")]),
)

# ---------------------------------------------------------------------------
# Dialogs and overlays
# ---------------------------------------------------------------------------
_withdraw = dlg("Withdraw this listing?", '<p>Air Max 90, white comes off the catalog. You can relist it later from your listings.</p>',
                btn("Keep listing") + btn("Withdraw listing", "danger"), did="wd", icon="trash", icon_kind="danger", size="sm")
_failed = dlg("Add tracking", fld("tr-no", "Tracking number", "1Z 999 AA1 01 2345 6784", attrs="autocomplete=\"off\""),
              btn("Cancel") + btn("Try again", "primary"), did="tr",
              top=alrt("danger", "That didn’t go through", "Your tracking number wasn’t saved. Try again."))

pattern(
    "dialogs-and-overlays", "Dialogs and overlays",
    lead="Overlays interrupt, so 12L uses them only for a decision that must happen before going on. Everything else is a page, a sheet or inline.",
    covers="Dialog vs sheet vs page vs inline; confirmations; busy, invalid and failed dialogs; stacking; mobile sheets.",
    overview=p(f"12L has three overlays: the modal {comp('dialog')} (a bottom sheet on phones), the full-screen menu and filter sheets ({comp('drawer')}), and the {comp('cookie-consent')} panel. "
               f"Tooltips and menus float but do not block. Every overlay sits on the z-order scale in {found('elevation')}."),
    when=table(["Job", "Use", "Example"], [
        ["Confirm something irreversible", "Small dialog, danger icon, danger confirm", "Withdraw listing, Close account, Cancel order"],
        ["Collect one to three fields tied to the current page", "Dialog with a form", "Add tracking, Change password, Leave a review"],
        ["Navigate on a phone", "Full-screen menu sheet", "Menu"],
        ["Refine a list on a phone", "Filter sheet (left drawer from 768px)", "Filters"],
        ["Anything long, shareable or with its own URL", "A page", "Checkout, Sell an item, Report detail"],
        ["Explain a control", f"{comp('tooltip')}", "Icon-only buttons"],
    ]),
    structure=stage(fake_page(f'<div class="ds-h4">Your listings</div>{item_row("air-max-90")}') + _withdraw, "26rem",
                    "Destructive confirmation: the question is the title, the body says what happens, the safe action says what it keeps.")
    + "<h3>Failed</h3>"
    + stage(fake_page(f'<div class="ds-h4">Sale 12L-48302</div>{item_row("reverse-weave")}') + _failed, "30rem",
            "Failed: the input is kept, a danger alert under the header says what was not saved, the primary becomes Try again."),
    states=table(["State", "Behaviour", "Mock"], [
        ["Default", "Focus on the first field, or on the safe action for confirmations.", '<a href="../../mocks/dialogs/cancel-order/default.html">cancel-order/default</a>'],
        ["Invalid", "Inline errors; with two or more, a summary above the body.", '<a href="../../mocks/dialogs/report-problem/invalid.html">report-problem/invalid</a>'],
        ["Busy", "Confirm button busy; Close and Esc still work only if the action can be abandoned safely.", '<a href="../../mocks/dialogs/withdraw-listing/busy.html">withdraw-listing/busy</a>'],
        ["Failed", "Danger alert at the top, input kept, Try again.", '<a href="../../mocks/dialogs/add-tracking/failed.html">add-tracking/failed</a>'],
        ["Success", "Close and confirm with a toast, or show the result in the dialog when the member needs to read it.", '<a href="../../mocks/dialogs/report-listing/success.html">report-listing/success</a>'],
        ["Blocked", "Warning alert explains why the action is not possible yet; only Close.", '<a href="../../mocks/dialogs/close-account/blocked.html">close-account/blocked</a>'],
    ]),
    responsive=ul("Below 640px dialogs are bottom sheets: full width, rounded top corners (<code>--radius-xl</code>), footer sticky at the bottom, buttons full width.",
                  "From 640px dialogs centre with 24px around them; sizes sm 24rem, md 32rem, lg 48rem; height caps at the viewport minus 48px and the body scrolls.",
                  "The filter sheet is full screen on phones and a 24rem left drawer from 768px; on 1024px+ filters are a sidebar and the sheet is not used."),
    accessibility=ul("<code>role=\"dialog\"</code>, <code>aria-modal=\"true\"</code>, <code>aria-labelledby</code> to the title, <code>aria-describedby</code> to the description when there is one.",
                     "Focus moves into the dialog, is trapped, and returns to the trigger on close. The page behind is <code>inert</code>.",
                     "Esc closes (except while an irreversible action is busy). The close button is labelled <i>Close</i>.",
                     "One dialog at a time. A dialog never opens another dialog; it replaces its content or hands over to a page.",
                     "Opening and closing use <code>--duration-slow</code> with the enter easing; reduced motion removes the slide."),
    content=ul("Titles are questions for confirmations (<i>Withdraw this listing?</i>) and verb phrases for tasks (<i>Add tracking</i>).",
               "The confirm button repeats the verb of the title: <i>Withdraw listing</i>, never <i>OK</i> or <i>Yes</i>.",
               "The safe button says what it keeps: <i>Keep listing</i>, <i>Keep order</i>.",
               "Bodies state the consequence and what can be undone, in one or two sentences."),
    do_dont=dodont([
        ("do", btn("Keep order") + btn("Cancel order", "danger"), "Name both outcomes."),
        ("dont", btn("No") + btn("Yes", "primary"), "Yes and No force the member to reread the question."),
        ("do", '<span class="text-sm">Checkout is a page with its own URL.</span>', "Long, multi-step tasks are pages."),
        ("dont", '<span class="text-sm">A dialog that opens a second dialog on top.</span>', "Stacked dialogs lose focus and context."),
    ]),
    sources=sources([("dialogs/withdraw-listing/default", ""), ("dialogs/add-tracking/failed", ""), ("dialogs/report-problem/invalid", ""), ("dialogs/withdraw-listing/busy", ""),
                     ("dialogs/close-account/blocked", ""), ("dialogs/filters/default", "filter sheet"), ("dialogs/nav-menu/default", "menu sheet")]),
)

# ---------------------------------------------------------------------------
# Data tables and lists
# ---------------------------------------------------------------------------
_orders = ('<ul class="order-list">' + "".join(
    f'<li><a href="#">{item_row(k)}<span class="order-list__end"><span class="price">{pr}</span>{st}</span></a></li>'
    for k, pr, st in [("iron-ranger", "$244.97", status("Shipped", "info")), ("better-sweater", "$58.03", status("Delivered", "info")), ("samba-og", "$83.10", status("Completed", "active"))]) + "</ul>")
_audit = ('<div class="table-wrap"><table class="table"><caption class="visually-hidden">Administrator actions, newest first (example)</caption>'
          '<thead><tr><th scope="col">When</th><th scope="col">Administrator</th><th scope="col">Action</th><th scope="col">Target</th></tr></thead><tbody>'
          + "".join(f'<tr><td class="num">{w}</td><td>Ana Ruiz</td><td>{a}</td><td><code>{t}</code></td></tr>' for w, a, t in
                    [("Today 11:05", "Refunded order", "12L-48140"), ("Today 10:42", "Removed listing", "L-20802"), ("Fri 10:15", "Suspended member", "jaybird")])
          + "</tbody></table></div>")

pattern(
    "data-tables-and-lists", "Data tables and lists",
    lead="Members see lists of things they recognise by photo, so 12L uses rows with thumbnails; administrators compare records, so they get tables.",
    covers="Order and listing lists, settings rows, the admin queue and audit table, filtering, sorting, load more, responsive strategy.",
    overview=p(f"Most collections in 12L are {comp('list', 'lists')} of item rows (thumbnail, title, meta, price, {comp('badge', 'status')}): purchases, sales, my listings, the moderation queue. "
               f"Only the audit log and the size rules are true {comp('table', 'tables')}, because their rows are compared column by column. The catalog itself is a grid of {comp('listing-card', 'listing cards')}."),
    when=table(["Data", "Use", "Example"], [
        ["Items a member recognises visually", "Order list / item rows with thumbnails", "Purchases, Sales, My listings"],
        ["Things to browse and compare by eye", "Listing grid", "Catalog"],
        ["Settings and preferences", "Settings list (title, meta, control)", "Settings, Emails"],
        ["Records compared across columns", "Table with caption and scoped headers", "Audit log"],
        ["Work to triage", "Queue list with type, age and status", "Moderation queue"],
    ]),
    structure=ex(_orders, "Order list: the whole row is one link; status is text plus a square marker; price uses tabular numbers.", stack=True)
    + "<h3>Table</h3>" + ex(_audit, "Audit table: visually hidden caption, scoped headers, mono IDs. It scrolls horizontally inside its wrapper on phones.", stack=True),
    states=ul('<b>Loading</b>: skeleton rows in the list’s shape, container <code>aria-busy</code> (<a href="../../mocks/pages/sales/loading.html">sales/loading</a>).',
              '<b>Empty</b> and <b>error</b>: see ' + patt("empty-and-error-states") + '.',
              '<b>Filtered</b>: chips above the list show active filters, each removable; the count updates (<a href="../../mocks/pages/my-listings/filtered.html">my-listings/filtered</a>).',
              '<b>No results</b>: compact empty state with <i>Clear filters</i> (<a href="../../mocks/pages/audit-log/no-results.html">audit-log/no-results</a>).',
              "<b>Hover</b>: the row title underlines; tables tint the row with <code>--color-bg-subtle</code>.",
              "<b>More</b>: the catalog uses <i>Load more</i> with a count (<i>Showing 24 of 61</i>) rather than numbered pages; numbered " + comp("pagination") + " is reserved for admin tables."),
    responsive=ul("Item rows never become tables: on phones the end column (price and status) stacks under the price.",
                  "Tables keep their columns and scroll inside <code>.table-wrap</code>; the first column carries the row’s identity.",
                  "The listing grid is 2 columns on phones, 3 from 768px, 4 from 1024px (3 beside the filters, 4 again from 1280px).",
                  "Toolbars (search, sort, filter button) wrap; the filter button only shows below 1024px."),
    accessibility=ul("Lists are <code>&lt;ul&gt;</code>; a clickable row contains exactly one link, and its accessible name is the row text.",
                     "Tables have a <code>&lt;caption&gt;</code> (visually hidden when the page heading already says it) and <code>scope</code> on headers; sortable headers use <code>aria-sort</code> on a button.",
                     "Status never relies on colour: the label is always text.",
                     "Thumbnails in rows have empty <code>alt</code> because the title next to them names the item.",
                     "Load more keeps focus on the button and announces the new count through the status region."),
    content=ul("Row titles are the item title; meta is <i>Brand · Men’s US 12</i> or <i>Order 12L-48213 · Shipped Thu 22 Oct</i>.",
               "Dates are short and absolute in lists (<i>Fri 30 Oct</i>), relative only for very recent events (<i>2 hours ago</i>).",
               "Column headers are nouns in sentence case: <i>When</i>, <i>Administrator</i>, <i>Action</i>, <i>Target</i>."),
    do_dont=dodont([
        ("do", status("Shipped", "info"), "Status as text with a marker."),
        ("dont", '<span class="ds-dot-only" aria-hidden="true"></span>', "A coloured dot with no label."),
    ]),
    sources=sources([("pages/purchases/default", "order list"), ("pages/sales/loading", "skeleton rows"), ("pages/my-listings/filtered", "filter chips"),
                     ("pages/audit-log/default", "table"), ("pages/moderation-queue/default", "queue"), ("pages/catalog/default", "listing grid and load more"), ("pages/settings/default", "settings list")]),
)

# ---------------------------------------------------------------------------
# Notifications
# ---------------------------------------------------------------------------
pattern(
    "notifications", "Notifications",
    lead="Toasts for things that just happened, banners for conditions that last, and the reservation timer for the one deadline 12L enforces.",
    covers="Toast vs banner vs inline alert; priority and persistence; stacking; the reservation timer; cookie consent.",
    overview=p(f"12L has no notification centre; email carries anything a member must see later. On screen there are three channels: {comp('toast', 'toasts')} on an ink surface with a coloured edge, "
               f"full-width banners (the {comp('alert')} banner variant) under the top bar, and the {comp('cookie-consent')} panel on first visit."),
    when=table(["Message", "Channel", "Dismiss", "Example"], [
        ["An action finished", "Toast (success/info)", "Auto after ~6s, pauses on hover/focus", "<i>Listing published · View listing</i>"],
        ["An action can be undone", "Toast with action", "Auto, longer (~10s)", "<i>Price updated to $40 · Undo</i>"],
        ["An action failed in the background", "Toast (danger)", "Never auto", "<i>Couldn’t save your draft · Try again</i>"],
        ["A deadline approaching", "Toast (warning) or banner", "Toast auto; banner while true", "<i>Ship by Fri 30 Oct · Add tracking</i>"],
        ["A condition across pages", "Banner", "Only when it is no longer true, or by the member if informational", "Unverified email, account suspended, payout returned, offline"],
        ["A system-wide notice", "Banner above everything", "Dismissible unless it blocks", "Scheduled maintenance"],
    ]),
    structure=stage(fake_page('<div class="ds-h4">Your listings</div>')
                    + '<div class="toast-region" role="status" aria-live="polite">'
                    + tst("info", "Draft saved") + tst("success", "Listing published", "Air Force 1 ’07 is live.", "View listing")
                    + tst("warning", "Ship by Fri 30 Oct", "Reverse Weave hoodie", "Add tracking") + "</div>", "26rem",
                    "Stacked toasts: newest at the bottom, at most three visible, older ones leave first.")
    + "<h3>Banners</h3>"
    + ex(bnr("warning", "Verify your email to buy and sell.", btn("Resend link", "sm"), dismiss=False, icon="mail")
         + bnr("danger", "Your last payout was returned by the bank.", '<a href="#">Update bank details</a>', dismiss=False)
         + bnr("info", "$33.30 is on its way to Chase •••• 6021.", '<a href="#">Payouts</a>'), stack=True, cls="ds-flush")
    + "<h3>Reservation timer</h3>"
    + ex(timer("9:41") + timer("0:48", "warning") + timer("0:00", "danger"), "Checkout holds the item for 10 minutes. The timer sits under the h1; under a minute it turns warning and a banner appears; at zero the Pay button disables and a danger banner offers Start again.", stack=True),
    states=table(["Kind", "Toast edge / banner tone", "Icon", "Role"], [
        ["Info", "Blue", "info", "status"], ["Success", "Green", "check-circle", "status"],
        ["Warning", "Amber", "alert or a topical icon (clock, mail)", "status"], ["Danger", "Red", "x-circle", "alert"],
    ]),
    responsive=ul("Toasts: full width at the bottom with 16px margins on phones; 24rem at the bottom right from 640px.",
                  "Banners span the viewport; text and actions centre and wrap.",
                  "The consent panel is a bottom sheet on phones and a 26rem card at the bottom right from 768px."),
    accessibility=ul("The polite toast region is in the page from the start; danger toasts and banners use <code>role=\"alert\"</code>.",
                     "Toast actions and dismiss buttons are real buttons in the tab order; the focus ring flips to paper on the ink surface.",
                     "Auto-dismiss pauses on hover and focus and never applies to errors (WCAG 2.2.1). Toasts never hold the only path to an action: <i>Add tracking</i> also lives on the sale page.",
                     "The timer is <code>role=\"timer\"</code> with <code>aria-live=\"off\"</code>; threshold banners do the announcing.",
                     "Colour is never alone: each kind has its own icon and words."),
    content=ul("Toast title: the fact, past tense, under six words. Text: the object. Action: one verb.",
               "Banner: one sentence with the consequence and the fix: <i>Finish payout setup to receive $34.20.</i> · <i>Set up payouts</i>.",
               "Timer: <i>Reserved for you · 9:41 left</i>; at zero: <i>Your reservation ended. You weren’t charged.</i>"),
    do_dont=dodont([
        ("do", tst("success", "Price updated to $40", "Arizona sandals", "Undo"), "Offer undo instead of asking for confirmation for reversible changes."),
        ("dont", tst("danger", "Your account is suspended", "", progress=True), "Account conditions in a toast that disappears. Use a persistent banner."),
    ]),
    sources=sources([("notifications/toast/stacked", ""), ("notifications/toast/with-action", ""), ("notifications/account-banner/warning", ""),
                     ("notifications/payout-banner/danger", ""), ("notifications/reservation-timer/warning", ""), ("notifications/reservation-timer/danger", ""),
                     ("notifications/system-banner/info", ""), ("notifications/cookie-consent/info", "")]),
)

# ---------------------------------------------------------------------------
# Content and tone
# ---------------------------------------------------------------------------
pattern(
    "content-and-tone", "Content and tone",
    lead="12L talks like a friend who also wears a 12: short, plain, specific. It names the item, the amount and the date, and never makes the member work out what happens next.",
    covers="Voice, sentence case, button verbs, numbers, money, dates, error and empty formulas, microcopy library.",
    overview=p(f"This page applies the rules in {found('content')} to whole screens. The mocks use one cast and one catalog (Marcus Bell, Dre Okafor, the Air Max 90, order 12L-48213) so every example reads as real.")
    + ul("<b>Short</b>: one idea per sentence; most UI strings are under ten words.",
         "<b>Specific</b>: <i>Pay $94.00</i>, <i>Ship by Fri 30 Oct</i>, <i>Reserved for you · 9:41 left</i>.",
         "<b>Calm</b>: no exclamation marks, no blame, no jokes in errors.",
         "<b>Fit first</b>: sizes are always written out (<i>Men’s US 12</i>, <i>Men’s L</i>) because that is why members are here."),
    when=table(["Situation", "Tone", "Example"], [
        ["Selling and buying", "Encouraging, practical", "<i>List something you no longer wear, or find something that fits.</i>"],
        ["Money", "Exact, neutral", "<i>$33.30 after the 10% fee of $3.70</i>"],
        ["Errors", "Calm, what is safe, what to do", "<i>Couldn’t withdraw. Your listing is still live.</i>"],
        ["Moderation and suspension", "Plain, factual, no judgement", "<i>Your account is suspended. You can still ship and track open orders. We emailed you the reason.</i>"],
        ["Legal", "Plain English, numbered", "Marketplace rules, Terms, Privacy"],
    ]),
    structure=ex('<div class="stack">' + alrt("warning", "Set up payouts to get paid", "$34.20 is waiting for you.", btn("Set up payouts", "sm"))
                 + f'<div class="cluster">{btn("Keep listing")}{btn("Withdraw listing", "danger")}</div>'
                 + fld("ct-title", "Title", "Air Max 90, white", help="Brand, model and colour. 5–80 characters.") + "</div>",
                 "Title says the outcome, text gives the amount, the button names the action; field help states the rule.", stack=True)
    + "<h3>Microcopy library</h3>"
    + table(["Use", "Say", "Not"], [
        ["Primary buy action", "Buy now", "Purchase, Checkout"], ["Second buy action", "Make an offer", "Offer"],
        ["Create a listing", "Sell (nav), List item (submit)", "Post, Create"], ["Save without publishing", "Save draft", "Save for later"],
        ["Pay", "Pay $94.00", "Submit payment, Place order"], ["Close a dialog", "Close (icon label)", "X, Dismiss dialog"],
        ["Retry", "Try again", "Retry, Reload"], ["Undo a change", "Undo", "Revert"],
        ["Sign in / out", "Sign in, Sign out", "Log in, Login, Logout"], ["Join", "Join 12L", "Sign up, Register"],
        ["Optional field", "(optional)", "*, Required"], ["Server error", "Something went wrong on our side. Ref xxxx-xxxx", "Error 500, Unknown error"],
    ]),
    states=table(["State", "Formula", "Example"], [
        ["Empty", "Fact + what happens next + one action", "<i>No sales yet. Sold items show up here with what to do next.</i> · Sell an item"],
        ["No results", "No items match + how to widen + clear", "<i>No items match. Try fewer filters or a different word.</i>"],
        ["Field error", "What to enter", "<i>Enter a price from $1.00 to $5,000.00</i>"],
        ["Server error", "Couldn’t + verb + what is safe + Ref", "<i>Couldn’t save your password. Try again in a moment. Ref 6b7d-2a40</i>"],
        ["Success", "Past tense + object + next link", "<i>Changes saved · View listing</i>"],
        ["Confirmation", "Question + consequence + named outcomes", "<i>Withdraw this listing?</i> · Keep listing / Withdraw listing"],
    ]),
    responsive=ul("Write for 360px first: button labels must not wrap there, titles may wrap to two lines.",
                  "Never shorten copy per breakpoint; if it does not fit on a phone it is too long everywhere.",
                  "Numbers and prices never break across lines (<code>white-space: nowrap</code> on <code>.price</code>)."),
    accessibility=ul("Link text makes sense alone: <i>View listing</i>, <i>Update bank details</i>; never <i>Click here</i> or <i>Learn more</i> without an object.",
                     "Icon-only buttons have verb labels, with the object when several are on screen (<i>Remove photo 2</i>).",
                     "Abbreviations are expanded on first use or avoided; dates include the weekday.",
                     "Plain language (aim for grade 7) helps everyone, including members reading in a second language."),
    content=ul("Sentence case everywhere, including buttons, titles and nav. Brand and model names keep their own casing (<i>990v6</i>, <i>Arc’teryx</i>).",
               "Money: <code>$85</code> in the catalog when there are no cents; <code>$94.00</code> in checkout, orders and payouts.",
               "Dates: <i>Sun 25 Oct 2026</i>, <i>Fri 30 Oct</i> within the year; times <i>10:42 ET</i>.",
               "Order and listing IDs in mono: <code>12L-48213</code>, <code>L-20931</code>.",
               "Use curly apostrophes and the en dash for ranges (<i>3–30 letters</i>)."),
    do_dont=dodont([
        ("do", btn("Withdraw listing", "danger"), "Name the action and its object."),
        ("dont", btn("Confirm", "danger"), "A generic verb hides the consequence."),
        ("do", '<span>Ship by <b>Fri 30 Oct</b></span>', "Absolute dates with weekdays for deadlines."),
        ("dont", '<span>Ship within 5 business days!!</span>', "Make the member count days; exclamation marks."),
    ]),
    sources=sources([("pages/payouts/not-onboarded", ""), ("dialogs/withdraw-listing/default", ""), ("pages/sell/default", "help text"),
                     ("pages/account/suspended", "moderation tone"), ("pages/rules/default", "legal tone"), ("pages/order-confirmation/default", "money and dates")]),
)
