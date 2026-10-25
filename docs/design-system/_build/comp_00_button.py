"""Button: the reference component page. Other comp_*.py modules follow this shape."""
from ds import *

STATES = ["Default", "Hover", "Focus", "Active", "Disabled", "Loading"]


def _b(kind: str, label: str):
    def make(state: str) -> str:
        attrs = {"default": "", "hover": 'data-state="hover"', "focus": 'data-state="focus"', "active": 'data-state="active"',
                 "disabled": "disabled", "loading": 'aria-busy="true"'}[state]
        return btn(label, kind, attrs=attrs)
    return make


_row = btn("Buy now", "primary") + btn("Make an offer") + btn("Save", "ghost", icon="heart") + btn("Remove photo", "danger")

component(
    "button", "Button", "Actions",
    lead="Buttons start an action: buy, list an item, ship, save. One ink primary button per screen tells the member what matters most.",
    pills=["Native <code>&lt;button&gt;</code>"],
    summary_variants="primary, secondary, ghost, link, danger; icon, icon-only, block",
    summary_states="default, hover, focus, active, disabled, loading",
    overview=p(f"Use a button when activating it changes something: it submits a form, opens a dialog, reserves an item or saves a draft. "
               f"Use a {comp('link')} when it only takes the member somewhere (a listing, a seller's profile). Several related actions behind one trigger are a {comp('menu')}.")
    + ul("<b>Primary</b> (solid ink, bold label) is the one action the screen exists for: <i>Buy now</i>, <i>List item</i>, <i>Pay $94.00</i>. Never two per view.",
         "<b>Secondary</b> (the default look, outlined) is for every other action: <i>Make an offer</i>, <i>Cancel</i>, <i>Save draft</i>.",
         "<b>Ghost</b> sits in dense places: the top bar, dialog close buttons, card and row actions.",
         "<b>Link</b> looks like a link but is a button: <i>Show more reviews</i> inside text.",
         "<b>Danger</b> confirms a destructive action (<i>Withdraw listing</i>, <i>Close account</i>) and appears only inside a confirmation dialog."),
    anatomy=anatomy(
        btn("List item", "primary lg", icon="plus"),
        [("30%", "18%"), ("55%", "18%"), ("74%", "74%")],
        [("Leading icon (optional)", "1.25em square, 2px stroke, inherits the label colour, <code>aria-hidden</code>."),
         ("Label", "A verb phrase in sentence case. It is the accessible name. Primary labels are bold."),
         ("Container", "Height from <code>--control-height-*</code>, <code>--radius-md</code> (2px) corners, 1px border, padding from the spacing scale.")]),
    variants=p("Variants change emphasis, not meaning. Pick by how much attention the action deserves on this screen.")
    + ex(btn("Buy now", "primary") + btn("Make an offer") + btn("Close", "ghost") + btn("Show more reviews", "link") + btn("Withdraw listing", "danger"),
         "Emphasis from highest to lowest; danger only appears inside confirmation dialogs.")
    + "<h3>With icons, icon-only and block</h3>"
    + ex(btn("Sell", "primary", icon="plus") + btn("Share", icon="share") + btn("Download data", icon_after="download")
         + btn("", "icon", icon="edit", attrs='aria-label="Edit listing"') + btn("", "ghost icon", icon="more", attrs='aria-label="More actions"')
         + '<div style="width: 100%; max-width: 20rem;">' + btn("Continue to payment", "primary block") + "</div>",
         "Icon-only buttons carry <code>aria-label</code>; the icon is <code>aria-hidden</code>. Block buttons fill their container (buy bar, auth forms, dialog footers on phones)."),
    sizes=p("Medium (40px) is the default. Small (32px) lives in toolbars, uploader tiles and row actions. Large (48px) is for the buy bar, auth screens and the hero, where the button is the point of the screen.")
    + ex(btn("Small", "primary sm") + btn("Medium", "primary") + btn("Large", "primary lg"),
         "Heights <code>--control-height-sm/md/lg</code>; padding <code>--space-3/4/6</code>; label <code>--font-size-sm/md/lg</code>."),
    states=p("Every variant has the same six states. Hover, focus and active are forced here with <code>data-state</code> so they can be reviewed without a pointer; real pages get them from <code>:hover</code>, <code>:focus-visible</code>, <code>:active</code>, <code>disabled</code> and <code>aria-busy</code>.")
    + state_matrix(STATES, [("Primary", _b("primary", "Buy now")), ("Secondary", _b("", "Make an offer")), ("Ghost", _b("ghost", "Edit")),
                            ("Link", _b("link", "Show more")), ("Danger", _b("danger", "Withdraw"))])
    + "<h3>Both themes</h3>"
    + themes(f'<div class="cluster">{_row}</div>')
    + ul("<b>Loading</b> keeps the width, hides the label behind a spinner, sets <code>aria-busy=\"true\"</code> and ignores clicks. In the mocks: <i>Pay $94.00</i> while the card is charged, <i>Publishing…</i> on the sell form, dialog confirm buttons while they save.",
         "<b>Disabled</b> uses the native attribute: not focusable, 50% opacity. Prefer leaving the button enabled and explaining the problem on submit (the sell form shows an error summary instead of a dead <i>List item</i> button).",
         f"<b>Pressed</b> toggles use <code>aria-pressed</code>; see {comp('button-group')}. <b>Expanded</b> menu triggers use <code>aria-expanded</code>; see {comp('menu')}."),
    responsive=ul("Below 640px the primary action of a form or dialog becomes full width (<code>.btn--block</code>) and sits last, under the secondary action.",
                  "On listing detail below 1024px, <i>Buy now</i> and <i>Make an offer</i> move into the sticky " + comp("buy-bar") + " as large block buttons; from 1024px they sit in the info column.",
                  "In dialog footers buttons stay on one row and wrap when the row is too narrow; the primary stays last (rightmost, or bottom when wrapped).",
                  "The top bar's <i>Sell</i> action is a nav link from 768px and moves into the menu sheet below it.",
                  "Labels never truncate. A label that wraps at 360px is too long; shorten the verb phrase."),
    theming=p("The button reads semantic tokens through five component tokens that each variant overrides: <code>--btn-bg</code>, <code>--btn-fg</code>, <code>--btn-border</code>, <code>--btn-bg-hover</code> and <code>--btn-bg-active</code>. A theme changes the semantic tokens; a surface re-skin overrides the component tokens; neither edits <code>.btn</code>.")
    + pre("""
/* Buttons on an inverse surface (cookie consent) flip to paper on ink: */
.consent .btn         { --btn-bg: transparent; --btn-fg: var(--color-fg-inverse); --btn-border: var(--color-border-inverse); }
.consent .btn--primary { --btn-bg: var(--color-fg-inverse); --btn-fg: var(--color-bg-inverse); --btn-border: var(--color-fg-inverse); }""")
    + p("In the dark theme the accent becomes paper, so the primary button is paper with an ink label (the logo inverted), and the danger button lightens to <code>--palette-red-300</code> with a deep-red label. Both pairs stay above 7:1."),
    accessibility=a11y(
        pattern="Native <code>&lt;button type=\"button\"&gt;</code>, or <code>type=\"submit\"</code> inside a form. A link styled as a button (<i>Sign in</i> in the top bar) stays an <code>&lt;a href&gt;</code>. Never a <code>&lt;div&gt;</code> with a click handler. No ARIA role is needed.",
        keyboard=[(kbd("Tab") + " / " + kbd("Shift", "Tab"), "Moves focus to and from the button in DOM order."),
                  (kbd("Enter") + ", " + kbd("Space"), "Activates the button. Space fires on key up, so a mis-press can be cancelled by moving away."),
                  (kbd("Esc"), "No effect on the button. A loading button cannot be cancelled with Esc; long actions offer a separate Cancel.")],
        focus="The shared ring (2px <code>--color-focus-ring</code>, 2px offset) appears on <code>:focus-visible</code> only. Ink on paper in light and paper on ink in dark, so it reaches 3:1 against the page and the button in both themes.",
        labelling="The visible label is the accessible name. Icon-only buttons set <code>aria-label</code> with a verb and object (<i>Remove photo 2</i>, <i>Close</i>). Loading buttons keep their name and add <code>aria-busy=\"true\"</code>; progress text is announced by the form's live region, not the button.",
        contrast=[("Label on primary", "--color-fg-on-accent", "--color-accent", 4.5), ("Label on primary, hover", "--color-fg-on-accent", "--color-accent-hover", 4.5),
                  ("Label on danger", "--color-fg-on-danger", "--color-danger-solid", 4.5), ("Secondary border on surface", "--color-border-strong", "--color-bg-surface", 3),
                  ("Focus ring on canvas", "--color-focus-ring", "--color-bg-canvas", 3)],
        motion="Background, border and shadow transition over <code>--duration-fast</code> (120ms); active nudges down 1px. Both disappear under <code>prefers-reduced-motion</code> because the tokens zero the durations. The loading spinner keeps turning: it is a status, not decoration.",
        touch="Medium (40px) and large (48px) clear the 24px minimum; large meets the 44px comfortable target and is used for the buy bar and auth forms. Small (32px) only appears with 8px between neighbours."),
    content=ul("Verb phrases in sentence case: <i>Buy now</i>, <i>List item</i>, <i>Add tracking</i>, <i>Confirm receipt</i>. Never <i>OK</i>, <i>Yes</i>, <i>Submit</i> or <i>Click here</i>.",
               "Put the amount in payment buttons: <i>Pay $94.00</i>. The member sees exactly what they agree to.",
               "Destructive labels name the loss: <i>Withdraw listing</i>, <i>Close account</i>, not <i>Confirm</i>.",
               "The safe option says what it keeps: <i>Keep listing</i>, <i>Keep order</i>, rather than a bare <i>Cancel</i> when Cancel is ambiguous (as in <i>Cancel order</i> dialogs).",
               "Keep labels to three words where possible; loading never changes the label."),
    do_dont=dodont([
        ("do", btn("Keep listing") + btn("Withdraw listing", "danger"), "One destructive action, placed last, with a safe action that says what it keeps."),
        ("dont", btn("Cancel", "danger") + btn("Cancel order", "primary"), "Two buttons that both say Cancel and both look loud. Name each outcome and keep one emphasised."),
        ("do", btn("Pay $94.00", "primary"), "Put the amount in the payment button."),
        ("dont", btn("Buy now", "primary") + btn("Make an offer", "primary"), "Two primary buttons compete. Make the second one secondary."),
        ("do", btn("", "ghost icon", icon="close", attrs='aria-label="Close"'), "Icon-only buttons have an <code>aria-label</code>."),
        ("dont", btn("Delete account", "danger"), "A danger button on a settings page with no confirmation. Open a confirmation dialog first."),
    ]),
    tokens=token_table([("Primary background / hover / active", "--color-accent / --color-accent-hover / --color-accent-active"),
                        ("Primary label", "--color-fg-on-accent"), ("Secondary background / border", "--color-bg-surface / --color-border-strong"),
                        ("Secondary and ghost hover", "--color-bg-subtle"), ("Secondary active", "--color-bg-subtle-hover"),
                        ("Danger background / hover", "--color-danger-solid / --color-danger-solid-hover"), ("Danger label", "--color-fg-on-danger"),
                        ("Link label", "--color-fg-link"), ("Focus ring", "--color-focus-ring"),
                        ("Height sm / md / lg", "--control-height-sm / --control-height-md / --control-height-lg"),
                        ("Padding sm / md / lg", "--space-3 / --space-4 / --space-6"), ("Radius", "--radius-md"),
                        ("Label font", "--text-label"), ("Primary weight", "--font-weight-bold"), ("Transition", "--duration-fast / --ease-standard")]),
    code=pre("""
<button class="btn btn--primary" type="submit">Buy now</button>
<button class="btn" type="button">Make an offer</button>
<button class="btn btn--primary btn--lg btn--block" type="submit" aria-busy="true">Pay $94.00</button>
<button class="btn btn--ghost btn--icon" type="button" aria-label="Close">
  <svg class="icon" aria-hidden="true" viewBox="0 0 24 24">…</svg>
</button>
<a class="btn" href="/sign-in">Sign in</a>""")
    + classes([("<code>.btn</code>", "Base: secondary look, medium size."),
               ("<code>.btn--primary</code> <code>.btn--ghost</code> <code>.btn--link</code> <code>.btn--danger</code>", "Variant."),
               ("<code>.btn--sm</code> <code>.btn--lg</code>", "Size; omit for medium."),
               ("<code>.btn--icon</code>", "Square icon-only button; requires <code>aria-label</code>."),
               ("<code>.btn--block</code>", "Full width."),
               ("<code>disabled</code> / <code>aria-disabled=\"true\"</code>", "Disabled. Use <code>aria-disabled</code> on links."),
               ("<code>aria-busy=\"true\"</code>", "Loading: spinner, label hidden, clicks ignored, width kept."),
               ("<code>aria-pressed</code>, <code>aria-expanded</code>", "Toggle and menu-trigger states."),
               ("<code>data-state=\"hover|focus|active|loading\"</code>", "Documentation only: forces a state in static pages.")]),
    sources=sources([("pages/listing-detail/default", "Buy now, Make an offer, share and save"),
                     ("pages/sell/default", "List item, Save draft, uploader actions"),
                     ("pages/checkout/submitting", "Pay $94.00 loading"),
                     ("dialogs/withdraw-listing/default", "danger confirmation with Keep listing"),
                     ("notifications/cookie-consent/info", "buttons on an inverse surface")],
                    "the mocks' radius comments said 8px while the value was 2px; the system documents the real 2px."),
)
