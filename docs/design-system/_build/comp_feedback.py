"""Feedback: toast, alert, inline message, progress, spinner, skeleton, empty state, error page, cookie consent."""
from ds import *

TONE_ICON = {"info": "info", "success": "check-circle", "warning": "alert", "danger": "x-circle"}
TONES = ["info", "success", "warning", "danger"]


def _toast(kind: str, title: str, text: str = "", action: str | None = None, progress: bool = True, attrs: str = "") -> str:
    role = ' role="alert"' if kind == "danger" else ""
    a = f'<button class="toast__action" type="button">{action}</button>' if action else ""
    t = f'<div class="toast__text">{text}</div>' if text else ""
    pr = '<span class="toast__progress" aria-hidden="true"></span>' if progress and kind != "danger" else ""
    return (f'<div class="toast toast--{kind}"{role}{attrs}>{ic(TONE_ICON[kind])}<div class="toast__body"><div class="toast__title">{title}</div>{t}{a}</div>'
            f'<button class="close" type="button" aria-label="Dismiss">{ic("close", "icon icon--sm")}</button>{pr}</div>')


def _region(*toasts: str) -> str:
    return f'<div class="toast-region" role="status" aria-live="polite">{"".join(toasts)}</div>'


def _page(text: str = "Catalog · 148 items") -> str:
    return (f'<div class="ds-stage__page"><span class="eyebrow">Behind the overlay</span><p class="text-muted">{text}</p>'
            '<span class="skeleton skeleton--text" style="width: 60%;"></span><span class="skeleton skeleton--text" style="width: 40%;"></span></div>')


def _alert(kind: str, title: str, text: str = "", actions: str = "", icon: str | None = None, role: str | None = None, close: bool = False, cls: str = "") -> str:
    icon = icon or TONE_ICON[kind]
    r = f' role="{role}"' if role else (' role="alert"' if kind == "danger" else "")
    body = f'<div class="alert__title">{title}</div>' + (f"<div>{text}</div>" if text else "") + (f'<div class="alert__actions">{actions}</div>' if actions else "")
    x = f'<button class="close" type="button" aria-label="Dismiss">{ic("close", "icon icon--sm")}</button>' if close else ""
    return f'<div class="alert alert--{kind}{(" " + cls) if cls else ""}"{r}>{ic(icon)}<div class="alert__body">{body}</div>{x}</div>'


def _banner(kind: str, text: str, actions: str = "", dismiss: bool = True, icon: str | None = None) -> str:
    icon = icon or TONE_ICON[kind]
    role = ' role="alert"' if kind == "danger" else ' role="status"'
    d = f'<button class="close" type="button" aria-label="Dismiss">{ic("close", "icon icon--sm")}</button>' if dismiss else ""
    a = f'<span class="alert__actions" style="margin: 0;">{actions}</span>' if actions else ""
    return f'<div class="alert alert--{kind} banner"{role}>{ic(icon)}<div class="alert__body"><span>{text}</span>{a}</div>{d}</div>'


def _empty(icon: str, title: str, text: str = "", actions: str = "", cls: str = "", heading: str = "h3") -> str:
    t = f'<p class="empty__text">{text}</p>' if text else ""
    a = f'<div class="empty__actions">{actions}</div>' if actions else ""
    c = f" {cls}" if cls else ""
    return f'<div class="empty{c}"><div class="empty__icon">{ic(icon, "icon icon--lg")}</div><{heading} class="empty__title">{title}</{heading}>{t}{a}</div>'


def _center(code_: str, title: str, text: str, actions: str, ref: str = "", icon: str | None = None, heading: str = "h2") -> str:
    big = f'<span class="code" aria-hidden="true">{code_}</span>' if code_ else ""
    i = f'<div class="empty__icon">{ic(icon, "icon icon--lg")}</div>' if icon else ""
    r = f'<span class="ref">{ref}</span>' if ref else ""
    return f'<div class="center-state">{big}{i}<{heading}>{title}</{heading}><p class="text-muted">{text}</p>{r}<div class="actions">{actions}</div></div>'


def _timer(text: str, kind: str = "") -> str:
    k = f" timer--{kind}" if kind else ""
    return f'<p class="timer{k}" role="timer" aria-live="off">{ic("clock")}<span>Reserved for you · <span class="num">{text}</span> left</span></p>'


def _progress(value: int | None, label: str, kind: str = "", lid: str = "") -> str:
    cls = "progress" + (f" progress--{kind}" if kind else "") + (" progress--indeterminate" if value is None else "")
    aria = (f'aria-valuenow="{value}" aria-valuemin="0" aria-valuemax="100"' if value is not None else 'aria-busy="true"')
    style = f' style="--value: {value}%;"' if value is not None else ""
    return f'<div class="{cls}" role="progressbar" aria-label="{label}" {aria}><div class="progress__bar"{style}></div></div>'


def _skel_card() -> str:
    return ('<div class="listing-card" aria-hidden="true" style="width: 10rem;"><span class="skeleton skeleton--photo"></span>'
            '<div class="listing-card__meta"><span class="skeleton skeleton--text" style="width: 40%;"></span>'
            '<span class="skeleton skeleton--text" style="width: 85%;"></span><span class="skeleton skeleton--text" style="width: 55%;"></span></div></div>')


def _skel_row() -> str:
    return ('<div class="item-row" aria-hidden="true" style="width: 100%;"><span class="skeleton skeleton--rect" style="width: 3.5rem; height: 3.5rem;"></span>'
            '<div class="item-row__body"><span class="skeleton skeleton--text" style="width: 45%;"></span><span class="skeleton skeleton--text" style="width: 25%;"></span></div></div>')


# ===========================================================================
# Toast
# ===========================================================================
def _t_state(kind: str):
    titles = {"info": ("Draft saved", ""), "success": ("Listing published", "Air Force 1 '07 is live."),
              "warning": ("Ship by Fri 30 Oct", "Reverse Weave hoodie for tall_tom."), "danger": ("Couldn’t save your draft", "Check your connection.")}

    def make(state: str) -> str:
        title, text = titles[kind]
        if state == "default":
            return _toast(kind, title, text)
        if state == "with action":
            act = {"info": "View", "success": "View listing", "warning": "Add tracking", "danger": "Try again"}[kind]
            return _toast(kind, title, text, act)
        if state == "hover (paused)":
            return _toast(kind, title, text, attrs=' data-state="hover"')
        if state == "focus":
            return _toast(kind, title, text).replace('class="close" type="button"', 'class="close" type="button" data-state="focus"')
        return _toast(kind, title, text, attrs=' data-state="leaving" style="animation: none; opacity: 0.5; translate: 0 var(--space-2);"')
    return lambda state: '<div style="width: 17rem;">' + make(state) + "</div>"


component(
    "toast", "Toast", "Feedback",
    lead="Toasts confirm that something just happened (Listing published, Payment confirmed) or that a background request failed, without taking the member off the page.",
    pills=["<code>role=\"status\"</code> region"],
    summary_variants="info, success, warning, danger; with action (Undo, View, Try again); stacked",
    summary_states="entering, visible, paused on hover/focus, leaving; errors persist",
    overview=p(f"A toast is a short, temporary message on the inverse (ink) surface, bottom right on desktop and full width at the bottom on phones. "
               f"Use it for the result of an action the member just took, when the page itself does not show the change. "
               f"Use an {comp('alert')} when the message belongs to a part of the page and must stay (a declined card, a suspended account); "
               f"use a page banner (see {comp('alert')}) for conditions that last (offline, maintenance); use a {comp('dialog')} when the member must decide.")
    + ul("<b>Info</b>: neutral news (<i>Draft saved</i>, <i>Drafts older than 90 days are deleted</i>).",
         "<b>Success</b>: the action worked (<i>Listing published</i>, <i>Payment confirmed</i>, <i>Back online</i>).",
         "<b>Warning</b>: something needs doing soon (<i>Ship by Fri 30 Oct</i>, with <i>Add tracking</i>).",
         "<b>Danger</b>: a request failed (<i>Something went wrong</i>, Ref 3c8e-1d42-a7f0, <i>Try again</i>). Error toasts never auto-dismiss.")
    + p(f"Rules for which feedback to use live in {patt('notifications')} and {patt('feedback-and-loading')}."),
    anatomy=anatomy(
        '<div style="width: min(100%, 24rem);">' + _toast("success", "Listing published", "Air Force 1 '07 is live.", "View listing") + "</div>",
        [("14%", "45%"), ("20%", "6%"), ("34%", "6%"), ("30%", "85%"), ("78%", "6%"), ("56%", "85%")],
        [("Status edge", "3px leading rule in the tone colour on ink (<code>--toast-edge</code>); the brand red when untoned."),
         ("Icon", "20px tone icon: info, check-circle, alert, x-circle. Paired with text, never alone."),
         ("Title", "<code>--text-label</code>, one line: what happened."),
         ("Text and action (optional)", "<code>--text-body-sm</code> detail; one underlined text button (<i>Undo</i>, <i>View listing</i>, <i>Try again</i>)."),
         ("Dismiss", "24px <code>.close</code> button labelled <i>Dismiss</i>; always present."),
         ("Timer bar", "2px <code>.toast__progress</code> showing time left before auto-dismiss; absent on danger toasts.")]),
    variants=p("The tone changes the icon and the leading edge; the surface stays ink in light and paper in dark so toasts read as one family above any page.")
    + ex('<div class="stack" style="width: min(100%, 24rem);">' + _toast("info", "Draft saved") + _toast("success", "Payment confirmed", "$94.00 charged to Visa ending 4242.")
         + _toast("warning", "Ship by Fri 30 Oct", "Reverse Weave hoodie for tall_tom.", "Add tracking") + _toast("danger", "Something went wrong", "Ref 3c8e-1d42-a7f0", "Try again") + "</div>",
         "Info, success, warning and danger. Danger has no timer bar and uses <code>role=\"alert\"</code>.", stack=True)
    + "<h3>Stacked in the region</h3>"
    + stage(_page() + _region(_toast("info", "Draft saved"), _toast("success", "Listing published", "Air Force 1 '07 is live.", "View listing"),
                              _toast("warning", "Ship by Fri 30 Oct", "Reverse Weave hoodie", "Add tracking")), "30rem",
            "Up to three toasts stack bottom-up in <code>.toast-region</code>, newest at the bottom; a fourth replaces the oldest non-error toast."),
    sizes=NA("Toasts have one size: 24rem wide from 640px, full width minus the page margin below it."),
    states=p("Toasts enter with <code>slide-up</code> over <code>--duration-base</code>, stay 5 seconds (8 with an action), pause while hovered or focused, and leave with <code>fade-out</code> (<code>data-state=\"leaving\"</code>). Hover and focus are forced with <code>data-state</code>.")
    + state_matrix(["Default", "With action", "Hover (paused)", "Focus", "Leaving"],
                   [(k.capitalize(), _t_state(k)) for k in TONES], "Tone")
    + "<h3>Both themes</h3>"
    + themes('<div class="stack">' + _toast("success", "Price updated to $40", "Arizona sandals", "Undo") + _toast("danger", "Couldn’t save your draft", "Check your connection.", "Try again") + "</div>")
    + ul("<b>Paused</b>: the timer bar stops while the pointer is over the toast or focus is inside it, so an <i>Undo</i> is never pulled away mid-reach.",
         "<b>Persistent</b>: danger toasts have no timer and stay until dismissed or the request succeeds on <i>Try again</i>.",
         "<b>Leaving</b>: fades and drops 8px; the region closes the gap without animation."),
    responsive=ul("Below 640px the region spans the viewport with a 16px margin and sits above the sticky " + comp("buy-bar") + " and form action bars, never over them.",
                  "From 640px the region is 24rem wide, 24px from the bottom-right corner.",
                  "Text wraps; titles do not truncate. On phones keep the detail to one line by naming the item, not describing it.",
                  "With the on-screen keyboard open, toasts wait until it closes rather than covering the field."),
    theming=p("Component tokens: <code>--toast-bg</code> (<code>--color-bg-inverse</code>), <code>--toast-fg</code> (<code>--color-fg-inverse</code>) and <code>--toast-edge</code>, which each tone points at <code>--color-inverse-info|success|warning|danger</code>. Those inverse tokens exist because the regular status icons are tuned for light surfaces: on ink the tone uses the 300 step, on paper (dark theme) the 700 step.")
    + pre("""
.toast--success { --toast-edge: var(--color-inverse-success); }
.toast--success .icon { color: var(--color-inverse-success); }"""),
    accessibility=a11y(
        pattern="One <code>.toast-region</code> per page with <code>role=\"status\" aria-live=\"polite\"</code>, present in the DOM from page load (empty) so screen readers register it. Toasts are inserted into it and announced politely. Danger toasts carry <code>role=\"alert\"</code> so the failure interrupts. Toasts never take focus.",
        keyboard=[(kbd("Tab"), "Reaches the toast's action and Dismiss button in DOM order (the region sits at the end of <code>&lt;body&gt;</code>)."),
                  (kbd("Enter") + ", " + kbd("Space"), "Runs the action or dismisses."),
                  (kbd("Esc"), "Dismisses the toast that holds focus."),
                  (kbd("F6"), "(Recommended in the app) jumps focus into the region when a toast with an action is showing.")],
        focus="Focus inside a toast pauses its timer. The ring uses <code>--color-fg-inverse</code> on the ink surface so it stays visible (3:1+) against the toast itself.",
        labelling="The title and text are the announcement; keep the important words first. Dismiss is <code>aria-label=\"Dismiss\"</code>. The timer bar is <code>aria-hidden</code>. Actions repeat the object when it is not in the title (<i>View listing</i>, not <i>View</i>).",
        contrast=[("Text on toast", "--color-fg-inverse", "--color-bg-inverse", 4.5), ("Success icon and edge", "--color-inverse-success", "--color-bg-inverse", 3),
                  ("Warning icon and edge", "--color-inverse-warning", "--color-bg-inverse", 3), ("Danger icon and edge", "--color-inverse-danger", "--color-bg-inverse", 3),
                  ("Info icon and edge", "--color-inverse-info", "--color-bg-inverse", 3)],
        motion="Enter <code>slide-up</code> 16px over <code>--duration-base</code> with <code>--ease-enter</code>; leave over <code>--duration-base</code> with <code>--ease-exit</code>. Under reduced motion toasts appear and disappear without movement. Auto-dismiss times are long enough to read (WCAG 2.2.1): 5s, 8s with an action, never for errors.",
        touch="The Dismiss button is 24px (the minimum) with 12px clear around it; the action is a full-height text button. Swiping a toast away is an enhancement, never the only way."),
    content=ul("Title says what happened in past tense or a short fact: <i>Listing published</i>, <i>Draft saved</i>, <i>Back online</i>. No exclamation marks.",
               "Detail names the item or amount: <i>$94.00 charged to Visa ending 4242.</i>, <i>Arizona sandals</i>.",
               "One action at most, a verb: <i>Undo</i>, <i>View listing</i>, <i>Add tracking</i>, <i>Try again</i>.",
               "Errors say it failed and give the reference: <i>Something went wrong</i> · <i>Ref 3c8e-1d42-a7f0</i>.",
               f"Never put information only in a toast that the member needs later; it disappears. See {patt('content-and-tone')}."),
    do_dont=dodont([
        ("do", '<div style="width: 100%;">' + _toast("success", "Price updated to $40", "Arizona sandals", "Undo") + "</div>", "Offer <i>Undo</i> for a quick, reversible change instead of a confirmation dialog."),
        ("dont", '<div style="width: 100%;">' + _toast("danger", "Your bank declined the card", "Insufficient funds.") + "</div>", "A declined card in a toast. It belongs in an inline alert above the payment form, where it stays while the member fixes it (as in checkout/declined)."),
        ("do", '<div style="width: 100%;">' + _toast("danger", "Something went wrong", "Ref 3c8e-1d42-a7f0", "Try again") + "</div>", "Error toasts persist, offer <i>Try again</i> and show the reference."),
        ("dont", '<div style="width: 100%;">' + _toast("success", "Success!") + "</div>", "A vague title with an exclamation mark. Say what succeeded."),
    ]),
    tokens=token_table([("Surface", "--color-bg-inverse"), ("Text", "--color-fg-inverse"),
                        ("Tone edge and icon", "--color-inverse-info / --color-inverse-success / --color-inverse-warning / --color-inverse-danger"),
                        ("Untoned edge", "--color-brand"), ("Edge width", "--border-width-accent"), ("Radius", "--radius-sm"), ("Shadow", "--shadow-3"),
                        ("Padding / gap", "--space-4 / --space-3"), ("Title / text", "--text-label / --text-body-sm"), ("Layer", "--z-toast"),
                        ("Enter / leave", "--duration-base / --ease-enter / --ease-exit")]),
    code=pre("""
<div class="toast-region" role="status" aria-live="polite">
  <div class="toast toast--success">
    <svg class="icon" aria-hidden="true" viewBox="0 0 24 24">…</svg>
    <div class="toast__body">
      <div class="toast__title">Listing published</div>
      <div class="toast__text">Air Force 1 '07 is live.</div>
      <button class="toast__action" type="button">View listing</button>
    </div>
    <button class="close" type="button" aria-label="Dismiss">…</button>
    <span class="toast__progress" aria-hidden="true"></span>
  </div>
</div>""")
    + classes([("<code>.toast-region</code>", "Fixed live region; <code>--top</code> modifier places it under the top bar."),
               ("<code>.toast</code>", "Ink surface with the brand edge."),
               ("<code>.toast--info|success|warning|danger</code>", "Tone: edge and icon colour."),
               ("<code>.toast__title</code>, <code>.toast__text</code>, <code>.toast__action</code>", "Content parts."),
               ("<code>.toast__progress</code>", "Auto-dismiss timer bar (omit on danger)."),
               ("<code>role=\"alert\"</code>", "On danger toasts only."),
               ("<code>data-state=\"leaving\"</code>", "Exit animation; also used in documentation.")]),
    sources=sources([("notifications/toast/info", "Draft saved"), ("notifications/toast/success", "Listing published"),
                     ("notifications/toast/warning", "Ship by Fri 30 Oct"), ("notifications/toast/danger", "Couldn’t save your draft"),
                     ("notifications/toast/with-action", "Price updated, Undo"), ("notifications/toast/stacked", "three toasts"),
                     ("notifications/system-banner/danger", "500 error toast with reference")],
                    "the mocks declared the toast's tone colours twice (status icon tokens, then inverse tokens); the system keeps only the inverse tokens behind <code>--toast-edge</code>."),
)
drift("assets/ui.css (toast)", "Toast icon colour was set twice: first to --color-*-icon (tuned for light surfaces, 2–3:1 on ink), then overridden with --color-inverse-*.",
      "Kept only the inverse tokens, routed through the new --toast-edge component token.")


# ===========================================================================
# Alert and banner
# ===========================================================================
def _a_state(kind: str):
    copy = {"info": ("Refunded in full", "$244.97 back to Visa ending 4242. Allow 5–10 days."),
            "success": ("Profile saved", ""), "warning": ("Verify your email to buy and sell", "We sent a link to marcus.bell@example.com."),
            "danger": ("Your bank declined the card", "Insufficient funds. Try another card — the item is still reserved for you.")}

    def make(state: str) -> str:
        t, x = copy[kind]
        if state == "default":
            return _alert(kind, t, x)
        if state == "with actions":
            return _alert(kind, t, x, btn("Resend link", "sm") if kind == "warning" else '<a href="#">View details</a>')
        if state == "dismissible":
            return _alert(kind, t, x, close=True)
        if state == "focus":
            return _alert(kind, t, x, close=True).replace('class="close" type="button"', 'class="close" type="button" data-state="focus"')
        return _banner(kind, t)
    return lambda state: '<div style="width: 20rem;">' + make(state) + "</div>"


component(
    "alert", "Alert", "Feedback",
    lead="Alerts put a lasting message where it applies: above a form after it failed, at the top of an order, or across the page as a banner when the whole site is affected.",
    pills=["Inline alert + page banner"],
    summary_variants="info, success, warning, danger; with actions; dismissible; page banner; flaws note",
    summary_states="default, dismissible, with actions, focus; role alert vs status",
    overview=p(f"Alerts stay on screen until the condition changes. Use an inline <code>.alert</code> for a message about one form, order or section; "
               f"use <code>.alert.banner</code> above the top bar for something that affects the whole account or site (offline, maintenance, unverified email, payout problems). "
               f"For a passing confirmation use a {comp('toast')}; for one field use an {comp('inline-message')}; for a choice use a {comp('dialog')}.")
    + ul("<b>Info</b>: a fact about the state of things (<i>Refunded in full</i>, <i>You’ve already reported this listing</i>).",
         "<b>Success</b>: the thing the member did is done and the page stays (<i>Profile saved</i>, <i>Draft saved</i>, <i>Link sent</i>).",
         "<b>Warning</b>: something limits what they can do, with a way out (<i>Verify your email to buy and sell</i>, <i>In someone’s checkout</i>, <i>Too many attempts</i>).",
         "<b>Danger</b>: something failed or is blocked (<i>Your bank declined the card</i>, <i>Your account is suspended</i>, <i>Couldn’t withdraw</i>).",
         "<b>Flaws note</b> (<code>.flaws</code>): the warning-toned rule on a Used - Fair listing that states its flaws. It is content, not a status, so it has no icon or role."),
    anatomy=anatomy(
        '<div style="width: min(100%, 30rem);">' + _alert("warning", "Verify your email to buy and sell", "We sent a link to marcus.bell@example.com.", btn("Resend link", "sm"), icon="mail", close=True) + "</div>",
        [("3%", "45%"), ("11%", "4%"), ("28%", "4%"), ("60%", "84%"), ("26%", "84%"), ("93%", "20%")],
        [("Leading edge", "4px rule (<code>--border-width-heavy</code>) in the tone border colour; 1px on the other sides."),
         ("Icon", "20px, <code>--alert-icon</code>; can be swapped for a more specific one (mail, clock, lock, flag, wifi-off)."),
         ("Title", "<code>--text-label</code>; the whole message when it fits in one line."),
         ("Text", "Detail and the way forward; may include a reference (<code>.ref</code>)."),
         ("Actions (optional)", "Small secondary button or underlined links in the tone colour."),
         ("Dismiss (optional)", "Only for messages the member can safely forget.")]),
    variants=ex('<div class="stack" style="width: 100%;">' + _alert("info", "Refunded in full", "$244.97 back to Visa ending 4242. Allow 5–10 days.")
                + _alert("success", "Draft saved", 'Finish it any time from <a href="#">your listings</a>.', role="status")
                + _alert("warning", "In someone’s checkout", "If they don’t finish within 10 minutes, it’s back on sale.", icon="clock")
                + _alert("danger", "Email or password is incorrect", "Check both and try again.") + "</div>",
                "Inline alerts in the four tones with icons swapped where the mocks use a more specific one.", stack=True)
    + "<h3>Page banners</h3>"
    + ex('<div class="stack" style="width: 100%;">' + _banner("info", "Planned maintenance Tue 27 Oct, 2:00–3:00 AM ET.", icon="wrench")
         + _banner("success", "Email verified. Buying and selling are open.")
         + _banner("warning", "You’re offline. Showing items from your last visit.", dismiss=False, icon="wifi-off")
         + _banner("danger", "Your last payout was returned by the bank.", '<a href="#">Update bank details</a>', dismiss=False) + "</div>",
         "<code>.banner</code> is full-bleed, square, centred, with a bottom rule instead of a leading edge. It sits above the top bar.", stack=True)
    + "<h3>Flaws note</h3>"
    + ex('<div class="flaws" style="width: 100%;"><strong>Flaws:</strong> Footbed worn at the heel. Small scuff on the left strap.</div>',
         "On listing detail for Used - Fair items (Birkenstock Arizona). Not an alert: no role, no icon."),
    sizes=NA("Alerts have one size; they take the width of their container. Banners always span the viewport."),
    states=p("Alerts are static; their states are about structure and interaction. The dismiss button's hover and focus are forced with <code>data-state</code>.")
    + state_matrix(["Default", "With actions", "Dismissible", "Focus", "Banner"], [(k.capitalize(), _a_state(k)) for k in TONES], "Tone")
    + "<h3>Both themes</h3>"
    + themes('<div class="stack">' + "".join(_alert(k, t) for k, t in [("info", "Refunded in full"), ("success", "Changes saved"), ("warning", "Problem open · Wrong size"), ("danger", "Couldn’t withdraw")]) + "</div>")
    + ul("<b>Appearing</b>: an alert that results from a submit is inserted above the form and focused (<code>tabindex=\"-1\"</code>) when it is an error summary; otherwise it is announced by its role.",
         "<b>Dismissed</b>: removed from the DOM; focus moves to the next logical element (the form's first field or the page heading).",
         "<b>Non-dismissible</b>: anything that blocks buying, selling or getting paid (unverified, suspended, payout setup, offline) stays until resolved."),
    responsive=ul("Inline alerts take their container's width; actions wrap under the text below 480px.",
                  "Banner text and actions wrap and stay centred; the dismiss button stays top-right.",
                  "Banners stack above the top bar in the order danger, warning, info; never more than two at once (show the most severe and queue the rest).",
                  "The reservation banner and the checkout timer are the same message at two zoom levels: the banner for the page, the " + comp("inline-message", "timer") + " next to the pay button."),
    theming=p("Four component tokens drive every tone: <code>--alert-bg</code>, <code>--alert-fg</code>, <code>--alert-border</code> and <code>--alert-icon</code>, defaulting to info and re-pointed by each tone modifier to <code>--color-{tone}-bg|fg|border|icon</code>. In the dark theme those status tokens become deep tints with light text, so the same markup works unchanged.")
    + pre("""
.alert--warning { --alert-bg: var(--color-warning-bg); --alert-fg: var(--color-warning-fg);
                  --alert-border: var(--color-warning-border); --alert-icon: var(--color-warning-icon); }"""),
    accessibility=a11y(
        pattern="A plain <code>&lt;div&gt;</code>. Add <code>role=\"alert\"</code> only to danger alerts inserted after page load (a failed submit, a declined card) so they interrupt; success and info alerts inserted after load use <code>role=\"status\"</code>. Alerts rendered with the page (suspended account, refunded order) need no role: they are read in order. The error summary variant is focused and links to each field (see " + comp("form-layout") + ").",
        keyboard=[(kbd("Tab"), "Reaches actions and the dismiss button in order."), (kbd("Enter") + ", " + kbd("Space"), "Activates the action or dismisses."),
                  (kbd("Esc"), "No effect; alerts are part of the page, not overlays.")],
        focus="The shared focus ring on actions and dismiss. A focused error summary shows the ring around the whole alert.",
        labelling="Tone is never colour alone: each tone has its icon and the title says the problem. The icon is decorative (<code>aria-hidden</code>). Dismiss buttons are <i>Dismiss</i>. Links name their destination (<i>Update bank details</i>).",
        contrast=[("Info text", "--color-info-fg", "--color-info-bg", 4.5), ("Success text", "--color-success-fg", "--color-success-bg", 4.5),
                  ("Warning text", "--color-warning-fg", "--color-warning-bg", 4.5), ("Danger text", "--color-danger-fg", "--color-danger-bg", 4.5),
                  ("Warning icon", "--color-warning-icon", "--color-warning-bg", 3), ("Danger icon", "--color-danger-icon", "--color-danger-bg", 3),
                  ("Flaws rule", "--color-warning-solid", "--color-warning-bg", 3)],
        motion="Alerts do not animate in; they appear where the content is. Dismissal removes them without a transition so layout does not jump twice.",
        touch="Dismiss is a 24px target inset into the corner; small action buttons are 32px with 12px between them."),
    content=ul("Title states the situation in plain words: <i>Your bank declined the card</i>, not <i>Payment error</i>.",
               "Text gives the reason and the next step, and what is safe: <i>Try another card — the item is still reserved for you.</i>, <i>Your listing is still live.</i>",
               "Errors from our side include the reference: <i>Try again in a moment.</i> <code>Ref 5d1c-0a77</code>.",
               "Times are Eastern and specific: <i>Planned maintenance Tue 27 Oct, 2:00–3:00 AM ET.</i>",
               "Never blame the member; never say <i>Oops</i>. See " + patt("content-and-tone") + "."),
    do_dont=dodont([
        ("do", _alert("danger", "Your bank declined the card", "Insufficient funds. Try another card — the item is still reserved for you."), "Say what failed, why, and what is still safe."),
        ("dont", _alert("danger", "Error", "Something happened."), "A generic error with no cause or next step."),
        ("do", _banner("warning", "Verify your email to buy and sell.", '<a href="#">Resend link</a>', dismiss=False, icon="mail"), "Blocking conditions stay as non-dismissible banners with the fix as a link."),
        ("dont", '<p class="text-sm" style="color: var(--color-danger-fg);">Your account is suspended.</p>', "Status by colour alone, with no icon, title or way forward."),
    ]),
    tokens=token_table([("Background", "--color-info-bg / --color-success-bg / --color-warning-bg / --color-danger-bg"),
                        ("Text", "--color-info-fg / --color-success-fg / --color-warning-fg / --color-danger-fg"),
                        ("Border", "--color-info-border / --color-success-border / --color-warning-border / --color-danger-border"),
                        ("Icon", "--color-info-icon / --color-success-icon / --color-warning-icon / --color-danger-icon"),
                        ("Leading edge", "--border-width-heavy"), ("Flaws rule", "--color-warning-solid / --border-width-accent"),
                        ("Padding / gap", "--space-4 / --space-3"), ("Radius", "--radius-md"), ("Title", "--text-label")]),
    code=pre("""
<div class="alert alert--danger" role="alert">
  <svg class="icon" aria-hidden="true" viewBox="0 0 24 24">…</svg>
  <div class="alert__body">
    <div class="alert__title">Your bank declined the card</div>
    <div>Insufficient funds. Try another card — the item is still reserved for you.</div>
  </div>
</div>

<div class="alert alert--warning banner" role="status">
  <svg class="icon" aria-hidden="true" viewBox="0 0 24 24">…</svg>
  <div class="alert__body"><span>Verify your email to buy and sell.</span>
    <span class="alert__actions"><button type="button">Resend link</button></span></div>
</div>""")
    + classes([("<code>.alert</code>", "Inline alert, info tone by default."), ("<code>.alert--success|warning|danger</code>", "Tone."),
               ("<code>.banner</code>", "Full-bleed page banner (with <code>.alert</code>)."), ("<code>.alert__title</code>, <code>.alert__actions</code>", "Parts."),
               ("<code>.close</code>", "Dismiss button inside an alert."), ("<code>.form-summary</code>", "Error summary: heavy danger edge, focusable."),
               ("<code>.flaws</code>", "Warning-toned flaws note on a listing."),
               ("<code>role=\"alert\"</code> / <code>role=\"status\"</code>", "Only on alerts inserted after load.")]),
    sources=sources([("pages/checkout/declined", "declined card"), ("pages/sign-in/invalid", "danger inline"), ("pages/account/unverified", "warning with action"),
                     ("pages/order-detail/refunded", "info"), ("notifications/account-banner/warning", "non-dismissible banner"),
                     ("notifications/payout-banner/danger", "banner with link"), ("notifications/system-banner/info", "maintenance banner"),
                     ("pages/listing-detail/own", "flaws note")],
                    "banners in the mocks set <code>border-left-width</code> twice (1px, then 0); the system keeps the final rule only. Inline alerts in the mocks added spacing with an empty <code>&lt;div style=\"height\"&gt;</code>; the system uses the parent stack gap."),
)
drift("pages/edit-profile/success, pages/notification-settings/success", "Spacing under a success alert came from an empty <div style=\"height: var(--space-8)\">.",
      "Documented: alerts sit in a .stack and take the stack gap; no spacer elements.")


# ===========================================================================
# Inline message
# ===========================================================================
def _field(fid: str, label: str, value: str, state: str) -> str:
    help_ = '<span class="field__help" id="{0}-help">Shown on the listing. At least 10 characters.</span>'.format(fid)
    err = f'<span class="field__error" id="{fid}-error">Describe the item\'s flaws</span>'
    ok = f'<span class="inline-status inline-status--success" id="{fid}-ok">{ic("check", "icon icon--sm")}Saved</span>'
    db, extra, inv = f"{fid}-help", "", ""
    if state == "error":
        db += f" {fid}-error"; extra = err; inv = ' aria-invalid="true"'
    elif state == "success":
        db += f" {fid}-ok"; extra = ok
    return (f'<div class="field" style="width: 100%;"><label class="field__label" for="{fid}">{label}</label>'
            f'<input class="input" id="{fid}" type="text" value="{value}" aria-describedby="{db}"{inv}>{help_}{extra}</div>')


component(
    "inline-message", "Inline message", "Feedback",
    lead="Small text next to the thing it is about: a field hint or error, a saved status, the reservation countdown, the secure-payment note.",
    pills=["Linked with <code>aria-describedby</code>"],
    summary_variants="field hint, field error, inline status (muted, success, danger), reservation timer (neutral, warning, danger), secure note",
    summary_states="hint, invalid, success, timer warning, timer danger",
    overview=p(f"Inline messages are the quietest feedback: one line beside a control or in a panel. They never interrupt and never float. "
               f"Use them when the message belongs to exactly one element. For a message about a whole form use an {comp('alert')} (error summary); for a passing confirmation a {comp('toast')}.")
    + ul("<b>Field hint</b> (<code>.field__help</code>): what to enter, before the member types (<i>At least 10 characters.</i>).",
         "<b>Field error</b> (<code>.field__error</code>): what to fix, with a ⚠ marker so it is not colour alone (<i>Enter a price from $1.00 to $5,000.00</i>).",
         "<b>Inline status</b> (<code>.inline-status</code>): the result of a small action in place (<i>Saved</i>, <i>Checking your link…</i>).",
         "<b>Reservation timer</b> (<code>.timer</code>): the checkout countdown, neutral then warning under a minute, danger at zero.",
         "<b>Secure note</b> (<code>.secure-note</code>): reassurance under the card field (<i>Card details go straight to our payment provider. 12L never sees them.</i>)."),
    anatomy=anatomy(
        '<div style="width: min(100%, 22rem);">' + _field("anat-flaws", "Describe the flaws", "", "error") + "</div>",
        [("1%", "18%"), ("1%", "38%"), ("1%", "54%"), ("1%", "68%")],
        [("Label", "The field's name; see " + comp("form-field") + "."), ("Control", "Marked <code>aria-invalid</code> when the error shows."),
         ("Hint", "<code>--text-body-sm</code>, muted, always visible."), ("Error", "<code>--text-body-sm</code> in <code>--color-danger-fg</code> with a ⚠ marker; below the hint.")]),
    variants=ex('<div class="stack" style="width: min(100%, 24rem);">' + _field("v-hint", "Price", "45.00", "hint") + _field("v-err", "Describe the flaws", "", "error") + "</div>",
                "Hint and error on fields, as on the sell form.", stack=True)
    + ex('<span class="inline-status">' + '<span class="spinner" aria-hidden="true"></span>Checking your link…</span>'
         + f'<span class="inline-status inline-status--success">{ic("check", "icon icon--sm")}Saved</span>'
         + f'<span class="inline-status inline-status--danger">{ic("x-circle", "icon icon--sm")}Not saved</span>'
         + '<span class="inline-status"><span class="dot dot--pulse" aria-hidden="true"></span>Live</span>',
         "Inline status: busy, success, danger and a live dot.")
    + ex(_timer("9:41") + _timer("0:48", "warning") + _timer("0:00", "danger")
         + f'<p class="secure-note">{ic("lock", "icon icon--sm")}Card details go straight to our payment provider. 12L never sees them.</p>',
         "Reservation timer in three tones, and the secure note from checkout."),
    sizes=NA("Inline messages take the size of their text role (body-sm, label or caption); there are no size variants."),
    states=state_matrix(["Hint", "Invalid", "Success"], [("Field", lambda s: '<div style="width: 16rem;">' + _field(f"st-{s}", "Display name", "marcus_12" if s != "invalid" else "", {"hint": "hint", "invalid": "error", "success": "success"}[s]) + "</div>")], "Context")
    + state_matrix(["Neutral", "Warning", "Danger"], [("Timer", lambda s: _timer({"neutral": "9:41", "warning": "0:48", "danger": "0:00"}[s], "" if s == "neutral" else s))], "Context")
    + "<h3>Both themes</h3>"
    + themes('<div class="stack">' + _field("th-field", "Price", "5200", "error").replace('id="th-field', 'id="th-field') + _timer("0:48", "warning") + "</div>",
             '<div class="stack">' + _field("th-field-l", "Price", "5200", "error") + _timer("0:48", "warning") + "</div>")
    + ul("Errors appear on submit and on blur after the first edit, and clear as soon as the value is valid (see " + patt("forms") + ").",
         "The timer turns warning at 1:00 and danger at 0:00, when the pay button is disabled and a banner explains what happened."),
    responsive=ul("Messages wrap under their control at every width; they never sit beside a field on phones.",
                  "The timer sits above the pay button in the order panel; on phones it stays visible next to the sticky pay action.",
                  "Long errors wrap with a hanging indent so the ⚠ marker stays on the first line."),
    theming=p("Inline messages use semantic text tokens directly: <code>--color-fg-muted</code> for hints and neutral status, <code>--color-danger-fg</code> for errors, <code>--color-success-fg</code> and <code>--color-warning-fg</code> for status. No component tokens are needed; the dark theme lightens each status foreground to its 300 step."),
    accessibility=a11y(
        pattern="Hints and errors are linked to their control with <code>aria-describedby</code> (hint id first, then error id), and the control gets <code>aria-invalid=\"true\"</code>. The checkout timer uses <code>role=\"timer\"</code> with <code>aria-live=\"off\"</code> so it is not read every second; the warning and danger banners announce the important moments instead. An inline status inserted after an action sits in a <code>role=\"status\"</code> container.",
        keyboard="Inline messages are not interactive. Links inside them (rare) are reached with <kbd>Tab</kbd>.",
        focus="No focus of their own. On a failed submit focus goes to the error summary, which links to each field; the field's own error is then read with it.",
        labelling="Errors name the fix, not the rule that failed. The ⚠ marker is CSS content; the error text carries the meaning. Icons in statuses are decorative.",
        contrast=[("Hint on surface", "--color-fg-muted", "--color-bg-surface", 4.5), ("Error on surface", "--color-danger-fg", "--color-bg-surface", 4.5),
                  ("Error in dialogs", "--color-danger-fg", "--color-bg-surface-raised", 4.5), ("Warning timer on page", "--color-warning-fg", "--color-bg-canvas", 4.5),
                  ("Success status on surface", "--color-success-fg", "--color-bg-surface", 4.5)],
        motion="Nothing moves except the live dot's pulse (<code>--duration-cycle</code>), which stops under reduced motion.",
        touch="Not interactive; no target size applies."),
    content=ul("Hints say what is expected before it goes wrong: <i>Shown on the listing. At least 10 characters.</i>",
               "Errors are imperative and specific: <i>Enter a price from $1.00 to $5,000.00</i>, <i>Describe the item's flaws</i>, <i>Confirm the label shows men's US 12</i>.",
               "Status is one or two words: <i>Saved</i>, <i>Checking your link…</i> (with an ellipsis while busy).",
               "Timer: <i>Reserved for you · 9:41 left</i>, minutes and seconds in tabular numerals."),
    do_dont=dodont([
        ("do", '<div style="width: 100%;">' + _field("dd-ok", "Price", "5200", "error").replace("Describe the item's flaws", "Enter a price from $1.00 to $5,000.00") + "</div>", "Say the valid range in the error."),
        ("dont", '<div class="field" style="width: 100%;"><label class="field__label" for="dd-bad">Price</label><input class="input" id="dd-bad" type="text" value="5200" aria-invalid="true" aria-describedby="dd-bad-e"><span class="field__error" id="dd-bad-e">Invalid value</span></div>', "<i>Invalid value</i> tells the member nothing about the fix."),
        ("do", _timer("0:48", "warning"), "Turn the timer warning under a minute, with the banner explaining what happens next."),
        ("dont", '<p class="timer" style="color: var(--color-danger-fg);" role="timer" aria-live="assertive">Reserved · 9:41 left</p>', "A red, assertive timer from the start: alarming and announced every second."),
    ]),
    tokens=token_table([("Hint and neutral status", "--color-fg-muted"), ("Error", "--color-danger-fg"), ("Success", "--color-success-fg"), ("Warning timer", "--color-warning-fg"),
                        ("Counter", "--color-fg-subtle"), ("Hint / error font", "--text-body-sm"), ("Timer font", "--text-label"), ("Secure note font", "--text-caption"),
                        ("Gap to control", "--space-1")]),
    code=pre("""
<div class="field">
  <label class="field__label" for="flaws">Describe the flaws</label>
  <textarea class="textarea" id="flaws" aria-describedby="flaws-help flaws-error" aria-invalid="true"></textarea>
  <span class="field__help" id="flaws-help">Shown on the listing. At least 10 characters.</span>
  <span class="field__error" id="flaws-error">Describe the item's flaws</span>
</div>
<p class="timer timer--warning" role="timer" aria-live="off">…<span>Reserved for you · <span class="num">0:48</span> left</span></p>""")
    + classes([("<code>.field__help</code>", "Hint."), ("<code>.field__error</code>", "Error with ⚠ marker."), ("<code>.field__counter</code>", "Character counter."),
               ("<code>.inline-status</code> + <code>--success|--danger</code>", "In-place status."), ("<code>.dot</code>, <code>.dot--pulse</code>", "Status dot."),
               ("<code>.timer</code> + <code>--warning|--danger</code>", "Reservation countdown."), ("<code>.secure-note</code>", "Caption with a lock icon.")]),
    sources=sources([("pages/sell/invalid", "field errors"), ("pages/edit-listing/invalid", "flaws error"), ("pages/checkout/default", "timer and secure note"),
                     ("notifications/reservation-timer/warning", "timer warning"), ("notifications/reservation-timer/danger", "timer at zero"),
                     ("pages/verify-email/loading", "Checking your link…")]),
)


# ===========================================================================
# Progress
# ===========================================================================
component(
    "progress", "Progress bar", "Feedback",
    lead="A thin bar that shows how far a measurable task has got: a photo upload, a data export.",
    pills=["<code>role=\"progressbar\"</code>"],
    summary_variants="determinate, indeterminate, with label and value, success, danger",
    summary_states="0–100%, indeterminate, complete, failed",
    overview=p(f"Use a progress bar when the task has a known size and takes longer than about a second: uploading listing photos, preparing a data export. "
               f"When the duration is unknown and short use a {comp('spinner')}; when content is loading into a known layout use a {comp('skeleton')}. "
               f"Order progress (Paid → Shipped → Delivered → Completed) is a {comp('stepper')}, not a progress bar.")
    + p("The mocks show no progress bar yet; it is in the system because photo uploads on the sell form (<code>.uploader__progress</code>) and the data export need one."),
    anatomy=anatomy(
        '<div class="stack stack--sm" style="width: min(100%, 22rem);"><div class="cluster cluster--between"><span class="text-sm" id="anat-up">Uploading photo 2 of 4</span><span class="text-sm num">60%</span></div>'
        + _progress(60, "Uploading photo 2 of 4") + "</div>",
        [("2%", "18%"), ("92%", "18%"), ("2%", "72%"), ("40%", "72%")],
        [("Label", "What is happening, above the bar; also the bar's <code>aria-label</code>."), ("Value (optional)", "Percentage in tabular numerals."),
         ("Track", "8px, <code>--color-bg-subtle-hover</code>, fully rounded."), ("Fill", "<code>--color-accent</code>; width from <code>--value</code>.")]),
    variants=ex('<div class="stack" style="width: min(100%, 24rem);">' + _progress(35, "Uploading photos") + _progress(None, "Preparing your data export")
                + _progress(100, "Upload complete", "success") + _progress(70, "Upload failed", "danger") + "</div>",
                "Determinate, indeterminate, success and danger.", stack=True),
    sizes=NA("One height (8px). Inside uploader tiles the bar is inset 8px from the tile edges."),
    states=state_matrix(["0%", "50%", "Complete", "Failed", "Indeterminate"],
                        [("Bar", lambda s: {"0%": _progress(0, "Upload"), "50%": _progress(50, "Upload"), "complete": _progress(100, "Upload", "success"),
                                            "failed": _progress(60, "Upload", "danger"), "indeterminate": _progress(None, "Upload")}[s])], "Variant")
    + "<h3>Both themes</h3>" + themes('<div class="stack">' + _progress(45, "Uploading") + _progress(100, "Done", "success") + _progress(60, "Failed", "danger") + "</div>")
    + ul("On failure the bar keeps its position in danger and an " + comp("inline-message", "inline error") + " names the file and offers <i>Try again</i>.",
         "On success the bar disappears after a short pause; the thing it was making (the photo tile) is the confirmation."),
    responsive=ul("The bar is fluid: it fills its container at every breakpoint.", "In the uploader grid (3 tiles across on phones, 4 from 640px) each tile has its own bar."),
    theming=p("The track reads <code>--color-bg-subtle-hover</code>; the fill <code>--color-accent</code>, or <code>--color-success-solid</code> / <code>--color-danger-solid</code>. In dark the accent is paper on an ink track."),
    accessibility=a11y(
        pattern="<code>role=\"progressbar\"</code> with <code>aria-valuenow</code>, <code>aria-valuemin=\"0\"</code>, <code>aria-valuemax=\"100\"</code> and an <code>aria-label</code> (or <code>aria-labelledby</code> pointing at the visible label). Indeterminate bars omit <code>aria-valuenow</code> and set <code>aria-busy=\"true\"</code> on the region being updated.",
        keyboard="Not focusable. A Cancel button, when offered, sits next to the bar.",
        focus="None.",
        labelling="The label says what is in progress and is announced on completion through a separate <code>role=\"status\"</code> message (<i>4 photos uploaded</i>); the bar itself is not polled by screen readers.",
        contrast=[("Fill on track", "--color-accent", "--color-bg-subtle-hover", 3), ("Value text", "--color-fg-default", "--color-bg-surface", 4.5)],
        motion="Width changes ease over <code>--duration-slow</code>. The indeterminate sweep runs on <code>--duration-cycle</code> and becomes a static 60%-opacity full bar under reduced motion.",
        touch="Not interactive."),
    content=ul("Label with a count: <i>Uploading photo 2 of 4</i>, <i>Preparing your data export</i>.", "Show a percentage only when it is meaningful; never fake progress."),
    do_dont=dodont([("do", '<div style="width: 100%;">' + _progress(50, "Uploading photo 2 of 4") + '<p class="text-sm">Uploading photo 2 of 4</p></div>', "Label the bar with what and how many."),
                    ("dont", '<div style="width: 100%;">' + _progress(None, "Loading") + "</div>", "An indeterminate bar for a page load; use skeletons in the final layout."),
                    ("do", '<div style="width: 100%;">' + _progress(70, "Upload failed", "danger") + '<p class="field__error">sandal-3.jpg is over 10 MB</p></div>', "On failure say which file and why."),
                    ("dont", '<div style="width: 100%;">' + _progress(70, "Uploading", "danger") + "</div>", "A red bar with no message.")]),
    tokens=token_table([("Track", "--color-bg-subtle-hover"), ("Fill", "--color-accent"), ("Success / danger fill", "--color-success-solid / --color-danger-solid"),
                        ("Radius", "--radius-full"), ("Fill transition", "--duration-slow"), ("Indeterminate cycle", "--duration-cycle")]),
    code=pre("""
<div class="progress" role="progressbar" aria-label="Uploading photo 2 of 4"
     aria-valuenow="50" aria-valuemin="0" aria-valuemax="100">
  <div class="progress__bar" style="--value: 50%;"></div>
</div>""")
    + classes([("<code>.progress</code>", "Track."), ("<code>.progress__bar</code>", "Fill; set <code>--value</code>."),
               ("<code>.progress--indeterminate</code>", "Looping sweep."), ("<code>.progress--success|danger</code>", "Outcome colour."),
               ("<code>.uploader__progress</code>", "Positions a bar inside an uploader tile.")]),
    sources=sources([("pages/sell/default", "uploader tiles the bar sits in"), ("dialogs/data-export/busy", "export in progress")],
                    "no mock shows a determinate bar; the component is documented from the kit and the two places that need it."),
)


# ===========================================================================
# Spinner
# ===========================================================================
component(
    "spinner", "Spinner", "Feedback",
    lead="A small turning ring for short waits of unknown length: checking an email link, loading an order confirmation, a button that is saving.",
    pills=["Status, not decoration"],
    summary_variants="sm (inline, 20px), lg (page, 40px), inside a button",
    summary_states="spinning; reduced motion keeps it turning",
    overview=p(f"Use a spinner when nothing about the result's shape is known and the wait is short. When the layout is known (a listing grid, an order) use a {comp('skeleton')}; when the amount of work is known use a {comp('progress')} bar. "
               f"Buttons show their own spinner through <code>aria-busy</code>; see {comp('button')}."),
    anatomy=anatomy('<div class="cluster"><span class="spinner spinner--lg" aria-hidden="true"></span><span class="text-muted">Loading your order…</span></div>',
                    [("6%", "28%"), ("44%", "28%")],
                    [("Ring", "2px (3px large) <code>--color-border-default</code> ring with an accent arc; turns once per <code>--duration-cycle-fast</code>."),
                     ("Status text", "Says what is loading. The text, not the ring, is announced.")]),
    variants=ex('<span class="cluster"><span class="spinner" aria-hidden="true"></span><span class="text-muted" role="status">Checking your link…</span></span>'
                + '<span class="spinner spinner--lg" aria-hidden="true"></span>' + btn("Pay $94.00", "primary", attrs='aria-busy="true"'),
                "Inline with text, page-level large, and the button loading state."),
    sizes=ex('<span class="spinner" aria-hidden="true"></span><span class="spinner spinner--lg" aria-hidden="true"></span>',
             "Small 20px (inline with text) and large 40px (centred in an empty page area)."),
    states=matrix(["Light", "Dark"], [("Small", [f'<div data-theme="light" class="ds-example__canvas"><span class="spinner" aria-hidden="true"></span></div>', f'<div data-theme="dark" class="ds-example__canvas" style="background: var(--color-bg-surface);"><span class="spinner" aria-hidden="true"></span></div>']),
                                      ("Large", [f'<div data-theme="light" class="ds-example__canvas"><span class="spinner spinner--lg" aria-hidden="true"></span></div>', f'<div data-theme="dark" class="ds-example__canvas" style="background: var(--color-bg-surface);"><span class="spinner spinner--lg" aria-hidden="true"></span></div>'])], "Size")
    + "<h3>Both themes</h3>" + themes('<div class="cluster"><span class="spinner" aria-hidden="true"></span><span class="text-muted">Checking your link…</span></div>')
    + p("A spinner has one state: turning. If the wait passes 10 seconds, replace it with a message and a way out (<i>This is taking longer than usual.</i> <i>Try again</i>)."),
    responsive=p("Spinners do not change with the viewport. Page-level spinners are centred in the content area, never over the top bar."),
    theming=p("The ring is <code>--color-border-default</code>; the arc <code>--color-accent</code> (ink in light, paper in dark). Inside buttons the arc uses <code>--btn-fg</code>."),
    accessibility=a11y(
        pattern="The ring is <code>aria-hidden=\"true\"</code>. The adjacent text sits in <code>role=\"status\"</code> so it is announced once; the busy region gets <code>aria-busy=\"true\"</code>.",
        keyboard="Not focusable.", focus="None. Focus stays where it was (on the button that started the wait).",
        labelling="Always pair with visible text, or a visually hidden <code>role=\"status\"</code> message (<i>Loading your order</i>).",
        contrast=[("Arc on surface", "--color-accent", "--color-bg-surface", 3), ("Arc on canvas", "--color-accent", "--color-bg-canvas", 3)],
        motion="One rotation per 800ms (<code>--duration-cycle-fast</code>). It keeps turning under reduced motion because it communicates status; the components stylesheet exempts it from the global reduced-motion rule.",
        touch="Not interactive."),
    content=ul("Status text uses a present participle and an ellipsis: <i>Checking your link…</i>, <i>Loading your order…</i>", "Never <i>Please wait</i> on its own."),
    do_dont=dodont([("do", '<span class="cluster"><span class="spinner" aria-hidden="true"></span><span class="text-muted">Checking your link…</span></span>', "Say what is loading."),
                    ("dont", '<span class="spinner spinner--lg" aria-hidden="true"></span>', "A bare spinner with no text."),
                    ("do", _skel_card(), "Use skeletons for a grid of listings."),
                    ("dont", '<span class="cluster"><span class="spinner" aria-hidden="true"></span><span class="spinner" aria-hidden="true"></span><span class="spinner" aria-hidden="true"></span></span>', "A spinner per card.")]),
    tokens=token_table([("Ring", "--color-border-default"), ("Arc", "--color-accent"), ("Rotation", "--duration-cycle-fast"), ("Ring width", "--border-width-thick")]),
    code=pre("""
<div class="center-state" aria-busy="true">
  <span class="spinner spinner--lg" aria-hidden="true"></span>
  <p class="text-muted" role="status">Loading your order…</p>
</div>""") + classes([("<code>.spinner</code>", "20px ring."), ("<code>.spinner--lg</code>", "40px ring, 3px stroke."), ("<code>aria-busy</code>", "On the region that is loading.")]),
    sources=sources([("pages/verify-email/loading", "Checking your link…"), ("pages/order-confirmation/loading", "large spinner"), ("pages/checkout/submitting", "button spinner")],
                    "spinner durations were raw 0.8s values in the mocks; now <code>--duration-cycle-fast</code>, and the spinner keeps turning under reduced motion."),
)
drift("assets/ui.css (spinner, skeleton, progress, pulse)", "Loop durations were raw (0.8s, 1.4s, 1.6s) and the global reduced-motion rule stopped spinners too.",
      "Added --duration-cycle-fast (800ms) and --duration-cycle (1400ms; pulse snapped from 1.6s); spinners and busy buttons keep turning under reduced motion.")


# ===========================================================================
# Skeleton
# ===========================================================================
component(
    "skeleton", "Skeleton", "Feedback",
    lead="Grey placeholders in the exact shape of the content that is loading, so the page does not jump when the data arrives.",
    pills=["<code>aria-hidden</code> shapes"],
    summary_variants="text, title, circle, rect, photo; composed listing card, list row, detail",
    summary_states="shimmering; static under reduced motion",
    overview=p(f"Every page that fetches data shows skeletons on first load, in the final layout: the catalog shows eight skeleton listing cards in the real grid with the filters already usable; account lists show skeleton rows. "
               f"Use a {comp('spinner')} only when the shape of the result is unknown. Never show skeletons for more than a few seconds; after that switch to an error ({comp('empty-state')})."),
    anatomy=anatomy(_skel_card(), [("8%", "8%"), ("8%", "76%"), ("8%", "84%"), ("8%", "92%")],
                    [("Photo", "<code>.skeleton--photo</code>: 4:5, square corners like real photos."), ("Brand", "Text line at 40% width."),
                     ("Title", "Text line at 85%."), ("Condition and price", "Text line at 55%.")]),
    variants=ex('<div class="stack" style="width: min(100%, 20rem);"><span class="skeleton skeleton--title"></span><span class="skeleton skeleton--text"></span><span class="skeleton skeleton--text"></span>'
                '<div class="cluster"><span class="skeleton skeleton--circle" style="width: 2.5rem; height: 2.5rem;"></span><span class="skeleton skeleton--rect" style="width: 6rem; height: 2.5rem;"></span></div></div>',
                "Primitives: title, text (last line 60%), circle, rect.", stack=True, show_code=False)
    + "<h3>Composed</h3>"
    + ex('<div class="cluster" style="align-items: flex-start;">' + _skel_card() + _skel_card() + "</div>" + '<div class="stack" style="width: 100%;">' + _skel_row() + _skel_row() + "</div>",
         "Listing cards (catalog/loading) and list rows (purchases, sales, queue).", stack=True, show_code=False),
    sizes=NA("Skeletons take the size of the content they stand in for; text lines follow the font size of their parent."),
    states=matrix(["Shimmer", "Reduced motion"], [("Text", ['<span class="skeleton skeleton--text" style="width: 10rem;"></span>', '<span class="skeleton skeleton--text" style="width: 10rem; animation: none;"></span>']),
                                                   ("Photo", ['<span class="skeleton skeleton--photo" style="width: 6rem;"></span>', '<span class="skeleton skeleton--photo" style="width: 6rem; animation: none;"></span>'])], "Shape")
    + "<h3>Both themes</h3>" + themes('<div class="cluster" style="align-items: flex-start;">' + _skel_card() + "</div>")
    + p("When data arrives the skeletons are replaced in one swap, not card by card, and <code>aria-busy</code> is removed so the new content is read."),
    responsive=ul("Skeleton grids use the real grid classes (<code>.listing-grid</code>), so they get 2, 3 and 4 columns at the real breakpoints.",
                  "Show as many skeleton items as fit the first screen: 8 cards on the catalog, 4 rows in lists."),
    theming=p("The shimmer is a gradient between <code>--color-bg-subtle</code> and <code>--color-bg-subtle-hover</code>; in dark those are ink-800 and ink-700, so skeletons sit just above the surface."),
    accessibility=a11y(
        pattern="Every skeleton shape is <code>aria-hidden=\"true\"</code> (or inside an <code>aria-hidden</code> card). The container that is loading gets <code>aria-busy=\"true\"</code> and an <code>aria-label</code> (<i>Loading listings</i>).",
        keyboard="Nothing focusable inside a skeleton. Controls that work without data (filters, search) stay usable.",
        focus="Unchanged.", labelling="The container's <code>aria-label</code> is the only announcement.",
        contrast=[("Skeleton on surface (decorative)", "--color-bg-subtle", "--color-bg-surface", 1)],
        motion="Shimmer sweeps over <code>--duration-cycle</code>; under reduced motion it is static.", touch="Not interactive."),
    content=p("Skeletons have no text. Do not write <i>Loading…</i> over them."),
    do_dont=dodont([("do", '<div class="cluster" style="align-items: flex-start;">' + _skel_card() + _skel_card() + "</div>", "Skeletons in the real grid, in the real card shape."),
                    ("dont", '<div class="stack" style="width: 100%;"><span class="skeleton skeleton--rect" style="height: 8rem;"></span></div>', "One big grey block that looks nothing like the content."),
                    ("do", _skel_row(), "Rows that match the thumbnail and two text lines of the real list."),
                    ("dont", '<div class="cluster"><span class="spinner" aria-hidden="true"></span>' + _skel_row() + "</div>", "Spinner and skeleton together; pick one.")]),
    tokens=token_table([("Base", "--color-bg-subtle"), ("Highlight", "--color-bg-subtle-hover"), ("Radius text / rect", "--radius-sm / --radius-md"), ("Shimmer cycle", "--duration-cycle")]),
    code=pre("""
<ul class="listing-grid" role="list" aria-busy="true" aria-label="Loading listings">
  <li><div class="listing-card" aria-hidden="true">
    <span class="skeleton skeleton--photo"></span>
    <div class="listing-card__meta">
      <span class="skeleton skeleton--text" style="width: 40%;"></span>
      <span class="skeleton skeleton--text" style="width: 85%;"></span>
    </div>
  </div></li>
</ul>""") + classes([("<code>.skeleton</code>", "Base shimmer block."), ("<code>--text</code>, <code>--title</code>", "Line shapes."), ("<code>--circle</code>, <code>--rect</code>", "Avatar and media shapes."),
                     ("<code>--photo</code>", "4:5 listing photo."), ("<code>aria-busy</code> + <code>aria-label</code>", "On the loading container.")]),
    sources=sources([("pages/catalog/loading", "skeleton listing grid"), ("pages/purchases/loading", "skeleton rows"), ("pages/listing-detail/loading", "detail skeleton"),
                     ("pages/moderation-queue/loading", "queue rows")],
                    "widths of skeleton lines were inline styles in every mock; the system keeps them inline (they describe content) but documents the 40/85/55% card recipe."),
)


# ===========================================================================
# Empty state
# ===========================================================================
component(
    "empty-state", "Empty state", "Feedback",
    lead="What a list or area shows when it has nothing in it, nothing matches, or it could not load: an icon, a title, one sentence and one way forward.",
    pills=["Compact and full"],
    summary_variants="first-run, no results, error (as empty), success (queue clear); compact",
    summary_states="empty, no results, failed to load",
    overview=p(f"Use an empty state in place of a list, grid or table. It explains why the area is empty and offers the one action that fills it. "
               f"Use an {comp('error-page')} when the whole page failed, and an {comp('alert')} when content exists but something about it is wrong. Formulas for the copy are in {patt('empty-and-error-states')}.")
    + ul("<b>First run</b>: <i>Nothing bought yet</i> · <i>Everything in the catalog already fits.</i> · <i>Browse the catalog</i>.",
         "<b>No results</b> (compact): <i>No items match</i> · <i>Try fewer filters or a different word.</i> · <i>Clear search and filters</i>.",
         "<b>Error</b> (<code>.empty--error</code>): <i>Couldn’t load purchases</i> · <i>Ref 51ce-0a92</i> · <i>Try again</i>.",
         "<b>Done</b>: <i>Queue clear</i> · <i>New reports and order problems land here.</i>"),
    anatomy=anatomy(_empty("bag", "Nothing bought yet", "Everything in the catalog already fits.", btn("Browse the catalog", "primary")),
                    [("44%", "12%"), ("30%", "42%"), ("22%", "58%"), ("36%", "80%")],
                    [("Icon tile", "64px square, <code>--color-accent-subtle</code> with an accent icon; danger-tinted for errors."),
                     ("Title", "<code>--text-h3</code>, a heading at the right level for the page."),
                     ("Text", "One sentence, max 36ch, muted."), ("Actions", "One primary action; an optional secondary link.")]),
    variants=ex(_empty("tag", "Nothing listed yet", "Be the first to list a pair of 12s or something in L.", btn("Sell an item", "primary"))
                + _empty("search", "No items match", "Try fewer filters or a different word.", btn("Clear search and filters", "primary"), cls="empty--compact")
                + _empty("refresh", "Couldn’t load items", 'Something went wrong on our side. <span class="ref">Ref 7f3a-91c2</span>', btn("Try again", "primary", icon="refresh"), cls="empty--error")
                + _empty("check-circle", "Queue clear", "New reports and order problems land here."),
                "First run, no results (compact), error and done."),
    sizes=ex(_empty("dollar", "No payouts yet", "Your earnings show up here after your first sale.", btn("Sell an item", "primary"))
             + _empty("tag", "No items for sale", "jaybird hasn’t listed anything yet.", cls="empty--compact"),
             "Full (48px vertical padding) for a page's main list; compact (32px) inside a section or beside filters."),
    states=state_matrix(["Empty", "No results", "Failed"], [("Purchases", lambda s: {
        "empty": _empty("bag", "Nothing bought yet", "Everything in the catalog already fits.", btn("Browse the catalog", "primary")),
        "no results": _empty("search", "No purchases match", "Try a different order number.", btn("Clear search", "primary"), cls="empty--compact"),
        "failed": _empty("refresh", "Couldn’t load purchases", '<span class="ref">Ref 51ce-0a92</span>', btn("Try again", "primary", icon="refresh"), cls="empty--error")}[s])], "List")
    + "<h3>Both themes</h3>" + themes(_empty("refresh", "Couldn’t load sales", '<span class="ref">Ref 6d10-77fe</span>', btn("Try again", "primary", icon="refresh"), cls="empty--error")),
    responsive=ul("Centred at every width; text wraps at 36ch.", "Actions wrap and centre; on phones the primary action stays inline-size (not block) because the empty state is not a form.",
                  "Beside the catalog filters (from 1024px) use the compact size so the filters stay the visual anchor."),
    theming=p("Reads <code>--color-accent-subtle</code> / <code>--color-fg-accent</code> for the icon tile and <code>--color-danger-bg</code> / <code>--color-danger-icon</code> for the error tile. No component tokens."),
    accessibility=a11y(
        pattern="Plain content in place of the list. The title is a real heading (<code>h2</code> on a page whose list is the main content, <code>h3</code> inside a section). When a filter change produces no results, announce the result count through the page's <code>role=\"status\"</code> region (<i>0 items</i>).",
        keyboard=[(kbd("Tab"), "Reaches the action."), (kbd("Enter"), "Activates it.")],
        focus="Focus is not moved to the empty state; after <i>Clear search and filters</i> focus returns to the search field.",
        labelling="The icon is decorative. The reference (<code>.ref</code>) is real text so it can be copied and read.",
        contrast=[("Icon on tile", "--color-fg-accent", "--color-bg-subtle", 4.5), ("Text on canvas", "--color-fg-muted", "--color-bg-canvas", 4.5), ("Error icon on tile", "--color-danger-icon", "--color-danger-bg", 3)],
        motion="None.", touch="The action is a 40px button."),
    content=ul("Title says what is missing in member words: <i>Nothing bought yet</i>, <i>No sales yet</i>, <i>No items match</i>.",
               "Text is one sentence that explains or encourages, with a little 12L voice: <i>Everything in the catalog already fits.</i>",
               "Action is the verb that fixes it: <i>Sell an item</i>, <i>Clear search and filters</i>, <i>Try again</i>.",
               "Errors: <i>Couldn’t load {thing}</i> + reference. Never <i>No data</i>."),
    do_dont=dodont([("do", _empty("search", "No items match", "Try fewer filters or a different word.", btn("Clear search and filters", "primary"), cls="empty--compact"), "Offer the action that gets results back."),
                    ("dont", '<p class="text-muted">No data.</p>', "<i>No data.</i> with no reason or action."),
                    ("do", _empty("refresh", "Couldn’t load payouts", '<span class="ref">Ref 61fa-c3d9</span>', btn("Try again", "primary", icon="refresh"), cls="empty--error"), "Say it failed, show the reference, offer Try again."),
                    ("dont", _empty("bag", "Nothing bought yet", "Everything in the catalog already fits.", btn("Browse the catalog", "primary") + btn("Sell an item", "primary")), "Two primary actions.")]),
    tokens=token_table([("Icon tile", "--color-accent-subtle / --color-fg-accent"), ("Error tile", "--color-danger-bg / --color-danger-icon"), ("Text", "--color-fg-muted"),
                        ("Title", "--text-h3"), ("Padding full / compact", "--space-12 / --space-8"), ("Gap", "--space-3")]),
    code=pre("""
<div class="empty">
  <div class="empty__icon"><svg class="icon icon--lg" aria-hidden="true" viewBox="0 0 24 24">…</svg></div>
  <h2 class="empty__title">Nothing bought yet</h2>
  <p class="empty__text">Everything in the catalog already fits.</p>
  <div class="empty__actions"><a class="btn btn--primary" href="/">Browse the catalog</a></div>
</div>""") + classes([("<code>.empty</code>", "Full empty state."), ("<code>.empty--compact</code>", "Less padding."), ("<code>.empty--error</code>", "Danger icon tile."),
                     ("<code>.empty__icon|title|text|actions</code>", "Parts."), ("<code>.ref</code>", "Reference ID in mono.")]),
    sources=sources([("pages/purchases/empty", "first run"), ("pages/catalog/no-results", "compact no results"), ("pages/purchases/error", "error as empty"),
                     ("pages/moderation-queue/empty", "queue clear"), ("pages/payouts/empty", "no payouts")]),
)


# ===========================================================================
# Error page
# ===========================================================================
ERRS = {
    "404": ("4<em>0</em>4", "Page not found", "The link may be old or mistyped.", btn("Back to shop", "primary"), "", None),
    "403": ("4<em>0</em>3", "You can’t open this", "It belongs to another member’s account.", btn("Go to your account", "primary"), "", None),
    "500": ("5<em>0</em>0", "Something went wrong", "It’s on our side. Your data is safe.", btn("Try again", "primary", icon="refresh") + btn("Back to shop"), "Ref 3c8e-1d42-a7f0", None),
    "offline": ("", "You’re offline", "Check your connection. We’ll pick up where you left off.", btn("Try again", "primary", icon="refresh"), "", "wifi-off"),
    "maintenance": ("", "Back at 3:00 AM ET", "12L is down for planned maintenance. Orders and payments are safe.", "", "", "wrench"),
}


def _err(k: str) -> str:
    c, t, x, a, r, i = ERRS[k]
    return _center(c, t, x, a, r, i)


component(
    "error-page", "Error page", "Feedback",
    lead="When a whole page cannot be shown: a big 12L-style code, a plain title, what is safe, and one way back. The shell stays so the member is never stranded.",
    pills=["Keeps the shell"],
    summary_variants="404, 403, 500, offline, maintenance; inline page errors (item unavailable, couldn’t load)",
    summary_states="static; 500 shows a reference",
    overview=p(f"Error pages replace the main content, not the whole document: the top bar, footer and search stay so the member can carry on. "
               f"The status code is set in the display face with the middle digit in signal red, echoing the red L. "
               f"For a failed list use an {comp('empty-state')}; for a failed action an {comp('alert')} or {comp('toast')}.")
    + ul("<b>404</b> <i>Page not found</i>, and the listing-specific <i>This item isn’t available</i>.", "<b>403</b> <i>You can’t open this</i> / <i>Admins only</i>.",
         "<b>500</b> <i>Something went wrong</i> with <i>Try again</i> and the reference.", "<b>Offline</b> <i>You’re offline</i>, with an icon instead of a code.",
         "<b>Maintenance</b> <i>Back at 3:00 AM ET</i>, served statically."),
    anatomy=anatomy(_err("500"), [("1%", "29%"), ("1%", "45%"), ("1%", "54%"), ("1%", "61%"), ("1%", "73%")],
                    [("Code", "<code>--text-display</code> at 96px, black weight, middle digit in <code>--color-brand</code>; <code>aria-hidden</code>."),
                     ("Title", "The page heading (<code>h1</code> in the product)."), ("Text", "What happened and what is safe."),
                     ("Reference (500)", "<code>.ref</code>, mono caption, for support."), ("Actions", "One primary recovery action, optional secondary.")]),
    variants=ex('<div class="stack" style="width: 100%;">' + _err("404") + _err("403") + _err("500") + "</div>", "Status-code pages. In the product the title is the page's <code>h1</code>; here they are <code>h2</code>.", stack=True, show_code=False)
    + ex('<div class="stack" style="width: 100%;">' + _err("offline") + _err("maintenance") + "</div>", "Icon pages for offline and maintenance.", stack=True, show_code=False),
    sizes=NA("One size. The 96px code (three digits) fits a 320px screen inside the 16px page margins, so it does not scale down."),
    states=state_matrix(["404", "403", "500", "Offline", "Maintenance"], [("Page", lambda s: _err(s))], "Variant")
    + "<h3>Both themes</h3>" + themes(_err("404")),
    responsive=ul("Left-aligned in the content column at every width (not centred), max 32rem, matching the page header.",
                  "Below 640px the title wraps under the 96px code; keep titles to four words so the first action stays above the fold at 360×640.", "Actions wrap; the primary stays first."),
    theming=p("The code is <code>--color-fg-default</code> with the red accent from <code>--color-brand</code>, which stays signal red in both themes (3.3:1 on the dark canvas, used at display size only)."),
    accessibility=a11y(
        pattern="The page keeps its landmarks; the error replaces <code>&lt;main&gt;</code> content. The title is the page's only <code>h1</code> and the document <code>&lt;title&gt;</code> starts with it (<i>Page not found — 12L</i>). The big code is <code>aria-hidden</code> because the title says the same thing.",
        keyboard=[(kbd("Tab"), "Skip link, top bar, then the recovery actions."), (kbd("Enter"), "Activates an action.")],
        focus="After a client-side navigation to an error, focus moves to the <code>h1</code> (<code>tabindex=\"-1\"</code>).",
        labelling="Titles name the situation; the reference is copyable text.",
        contrast=[("Code accent on canvas (large)", "--color-brand", "--color-bg-canvas", 3), ("Text on canvas", "--color-fg-muted", "--color-bg-canvas", 4.5)],
        motion="None.", touch="Actions are 40px buttons."),
    content=ul("Titles in plain words: <i>Page not found</i>, <i>You can’t open this</i>, <i>Something went wrong</i>, <i>You’re offline</i>.",
               "Say what is safe: <i>Your data is safe.</i>, <i>Orders and payments are safe.</i>", "Maintenance gives the time back in ET: <i>Back at 3:00 AM ET</i>.",
               "Never blame the member, never show a stack trace."),
    do_dont=dodont([("do", _err("500"), "Reference, reassurance and Try again."), ("dont", '<div class="center-state"><span class="code" aria-hidden="true">5<em>0</em>0</span><h3>Internal Server Error</h3></div>', "Technical title, no way out."),
                    ("do", _err("offline"), "An icon page for offline: it is not a server status."),
                    ("dont", '<div class="center-state"><span class="code" aria-hidden="true">4<em>0</em>4</span><h3>Oops! You broke it</h3><p class="text-muted">This page doesn’t exist.</p></div>', "Blame and no action.")]),
    tokens=token_table([("Code", "--text-display / --letter-spacing-display"), ("Code accent", "--color-brand"), ("Text", "--color-fg-muted"), ("Reference", "--text-code"),
                        ("Padding", "--space-20 / --space-16"), ("Gap", "--space-4")]),
    code=pre("""
<main id="main" class="container page">
  <div class="center-state">
    <span class="code" aria-hidden="true">5<em>0</em>0</span>
    <h1>Something went wrong</h1>
    <p class="text-muted">It’s on our side. Your data is safe.</p>
    <span class="ref">Ref 3c8e-1d42-a7f0</span>
    <div class="actions"><button class="btn btn--primary" type="button">Try again</button></div>
  </div>
</main>""") + classes([("<code>.center-state</code>", "Left-aligned recovery block."), ("<code>.code</code> + <code>&lt;em&gt;</code>", "Big code with red middle digit."),
                     ("<code>.ref</code>", "Reference ID."), ("<code>.actions</code>", "Action row."), ("<code>.empty__icon</code>", "Icon tile for offline/maintenance.")]),
    sources=sources([("pages/not-found/default", "404"), ("pages/forbidden/default", "403"), ("pages/server-error/default", "500"), ("pages/offline/default", "offline"),
                     ("pages/maintenance/default", "maintenance"), ("pages/listing-detail/unavailable", "item 404")]),
)


# ===========================================================================
# Cookie consent
# ===========================================================================
def _consent(cid: str, focus: str = "") -> str:
    p_btn = btn("Accept analytics", "primary", attrs=f'data-state="{focus}"' if focus == "hover" else ("data-state=\"focus\"" if focus == "focus" else ""))
    return (f'<section class="consent" aria-labelledby="{cid}"><h2 id="{cid}" style="font: var(--text-h4);">Cookies</h2>'
            f'<p class="text-sm">We use necessary cookies to run 12L. Analytics only if you say yes.</p>'
            f'<div class="consent__actions">{p_btn}{btn("Necessary only")}</div>'
            f'<a class="text-sm" href="#">Cookie settings</a></section>')


component(
    "cookie-consent", "Cookie consent", "Feedback",
    lead="A small ink panel on a visitor's first visit: necessary cookies only until they choose, two equal choices and a link to the details.",
    pills=["Non-modal", "Inverse surface"],
    summary_variants="first visit panel; saved toast",
    summary_states="default, hover, focus; saved",
    overview=p(f"Consent is a non-modal region, bottom right (full width on phones), on the inverse surface so it is clearly separate from the page. The page stays usable; nothing waits for an answer. "
               f"<i>Accept analytics</i> and <i>Necessary only</i> are equally easy. After a choice the panel closes and a {comp('toast')} confirms (<i>Cookie choice saved</i>). Details live in the cookie settings {comp('dialog')}, also linked from the {comp('footer')}."),
    anatomy=anatomy('<div class="ds-stage" style="--stage-height: 16rem; width: 100%;">' + _consent("an-c") + "</div>", [("16%", "21%"), ("16%", "36%"), ("16%", "53%"), ("16%", "67%")],
                    [("Title", "<i>Cookies</i>, <code>h2</code> styled as h4, labels the region."), ("Text", "One sentence in <code>--text-body-sm</code>."),
                     ("Choices", "Primary <i>Accept analytics</i> and secondary <i>Necessary only</i>, re-skinned for the inverse surface."), ("Settings link", "Opens the cookie settings dialog.")]),
    variants=stage(_page("Catalog · guest") + _consent("v-c"), "22rem", "First visit: the panel over the guest catalog.")
    + stage(_page("Catalog · guest") + _region(_toast("success", "Cookie choice saved", "Necessary only. Change it any time in the footer.")), "16rem", "After choosing: a success toast."),
    sizes=NA("One size: 26rem wide from 768px, full width minus 16px margins below it."),
    states=state_matrix(["Default", "Hover", "Focus"], [("Panel", lambda s: '<div class="ds-stage" style="--stage-height: 15rem;">' + _consent(f"st-c-{s}", "" if s == "default" else s) + "</div>")], "Variant")
    + "<h3>Both themes</h3>" + themes('<div class="ds-stage" style="--stage-height: 15rem;">' + _consent("th-c-d") + "</div>", '<div class="ds-stage" style="--stage-height: 15rem;">' + _consent("th-c-l") + "</div>"),
    responsive=ul("Below 768px the panel spans the viewport with 16px margins at the bottom; from 768px it is 26rem, 24px from the bottom-right corner.",
                  "Buttons wrap to two rows on narrow phones; both stay full height."),
    theming=p("The panel reads <code>--color-bg-inverse</code> / <code>--color-fg-inverse</code> and re-points the button tokens: secondary buttons get a transparent fill and <code>--color-border-inverse</code> edge; the primary becomes paper on ink (ink on paper in dark). Focus rings use <code>--color-fg-inverse</code>.")
    + pre(""".consent .btn          { --btn-bg: transparent; --btn-fg: var(--color-fg-inverse); --btn-border: var(--color-border-inverse); }
.consent .btn--primary { --btn-bg: var(--color-fg-inverse); --btn-fg: var(--color-bg-inverse); --btn-border: var(--color-fg-inverse); }"""),
    accessibility=a11y(
        pattern="A <code>&lt;section aria-labelledby&gt;</code> landmark, not a dialog: it does not trap focus or block the page. It is placed at the end of <code>&lt;body&gt;</code>, after the skip link targets, so keyboard users reach the page first and the region via landmarks.",
        keyboard=[(kbd("Tab"), "Reaches Accept analytics, Necessary only and Cookie settings."), (kbd("Enter") + ", " + kbd("Space"), "Makes the choice; the panel closes and focus returns to where it was before (or the page heading).")],
        focus="Focus rings switch to <code>--color-fg-inverse</code> on the ink panel so they remain 3:1+.",
        labelling="Region named by its <i>Cookies</i> heading. Both choices name the outcome.",
        contrast=[("Text on panel", "--color-fg-inverse", "--color-bg-inverse", 4.5), ("Secondary button edge", "--color-border-inverse", "--color-bg-inverse", 3)],
        motion="Slides up over <code>--duration-slow</code>; appears without movement under reduced motion.",
        touch="Buttons are 40px tall with 12px between them."),
    content=ul("Title: <i>Cookies</i>. Text: <i>We use necessary cookies to run 12L. Analytics only if you say yes.</i>", "Choices are equal and plain: <i>Accept analytics</i>, <i>Necessary only</i>. No <i>Accept all</i> dark pattern."),
    do_dont=dodont([("do", '<div class="ds-stage" style="--stage-height: 15rem; width: 100%;">' + _consent("dd-c") + "</div>", "Two equally reachable choices, page still usable."),
                    ("dont", '<div class="ds-example__canvas--inverse ds-example__canvas" style="width: 100%;"><span>We use cookies.</span>' + btn("Accept all", "primary") + "</div>", "<i>Accept all</i> with no way to refuse and no detail."),
                    ("do", _toast("success", "Cookie choice saved", "Necessary only. Change it any time in the footer."), "Confirm the choice and say where to change it."),
                    ("dont", '<div class="ds-example__canvas ds-example__canvas--inverse" style="width: 100%;"><button class="btn" type="button" style="border-color: var(--color-border-default);">Necessary only</button></div>', "A secondary button whose edge disappears on ink (the mocks' original 1.7:1 edge).")]),
    tokens=token_table([("Panel", "--color-bg-inverse"), ("Text", "--color-fg-inverse"), ("Secondary edge", "--color-border-inverse"), ("Shadow", "--shadow-4"), ("Layer", "--z-toast"),
                        ("Padding / gap", "--space-6 / --space-4"), ("Enter", "--duration-slow / --ease-enter")]),
    code=pre("""
<section class="consent" aria-labelledby="consent-title">
  <h2 id="consent-title">Cookies</h2>
  <p class="text-sm">We use necessary cookies to run 12L. Analytics only if you say yes.</p>
  <div class="consent__actions">
    <button class="btn btn--primary" type="button">Accept analytics</button>
    <button class="btn" type="button">Necessary only</button>
  </div>
  <a class="text-sm" href="/cookies">Cookie settings</a>
</section>""") + classes([("<code>.consent</code>", "Fixed inverse panel; re-skins buttons inside it."), ("<code>.consent__actions</code>", "Button row.")]),
    sources=sources([("notifications/cookie-consent/info", "first visit"), ("notifications/cookie-consent/success", "saved toast"), ("dialogs/cookie-settings/default", "settings dialog")],
                    "the secondary button edge (<code>--color-border-inverse</code>) was 1.73:1 on ink in light and 1.35:1 on paper in dark; tokens now use stone-500 / stone-600 (above 3:1)."),
)
drift("notifications/cookie-consent/info", "Secondary button edge (--color-border-inverse) on the inverse panel was 1.73:1 in light and 1.35:1 in dark, below the 3:1 for UI components (1.4.11).",
      "--color-border-inverse now aliases --palette-stone-500 (light) and --palette-stone-600 (dark); both pass 3:1. Pair added to contrast-pairs.json.")
