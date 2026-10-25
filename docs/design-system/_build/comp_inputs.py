"""Inputs: text field, textarea, select, checkbox, radio group, switch, file upload, form field, form layout."""
from ds import *


# ---------------------------------------------------------------------------
# Local helpers (mirror mk.field / mk.error_summary, with ids unique per page)
# ---------------------------------------------------------------------------
def field(fid: str, label: str, control: str = "", *, help: str | None = None, error: str | None = None, optional: bool = False,
          value: str = "", type: str = "text", attrs: str = "", counter: str | None = None) -> str:
    db = " ".join(x for x in [f"{fid}-help" if help else "", f"{fid}-error" if error else ""] if x)
    dba = f' aria-describedby="{db}"' if db else ""
    inv = ' aria-invalid="true"' if error else ""
    if not control:
        v = f' value="{esc(value)}"' if value else ""
        control = f'<input class="input" id="{fid}" name="{fid}" type="{type}"{v}{dba}{inv}{(" " + attrs) if attrs else ""}>'
    else:
        control = control.replace("{db}", dba + inv)
    opt = ' <span class="optional">(optional)</span>' if optional else ""
    h = f'<span class="field__help" id="{fid}-help">{help}</span>' if help else ""
    e = f'<span class="field__error" id="{fid}-error">{esc(error)}</span>' if error else ""
    c = f'<span class="field__counter">{counter}</span>' if counter else ""
    return f'<div class="field"><label class="field__label" for="{fid}">{label}{opt}</label>{control}{h}{e}{c}</div>'


def summary(errors: list[tuple[str, str]], title: str = "Fix these to continue", sid: str = "error-summary") -> str:
    items = "".join(f'<li><a href="#{fid}">{esc(msg)}</a></li>' for fid, msg in errors)
    return (f'<div class="alert alert--danger form-summary" role="alert" tabindex="-1" id="{sid}">{ic("x-circle")}'
            f'<div class="alert__body"><div class="alert__title">{title}</div><ul>{items}</ul></div></div>')


ST_INPUT = {"default": "", "hover": ' data-state="hover"', "focus": ' data-state="focus"', "invalid": ' aria-invalid="true"',
            "disabled": " disabled", "read-only": " readonly"}
INPUT_STATES = ["Default", "Hover", "Focus", "Invalid", "Disabled", "Read-only"]


def w(html: str, width: str = "14rem") -> str:
    return f'<div style="width: {width};">{html}</div>'


def both(fn) -> str:
    """themes() with unique ids per side: fn(suffix) -> html."""
    return themes(fn("d"), light=fn("l"))


# ===========================================================================
# Text field
# ===========================================================================
def tf(sfx: str, state: str, value: str = "marcus_12", label: str = "Display name") -> str:
    v = f' value="{esc(value)}"' if value else ""
    return f'<input class="input" id="tf-{sfx}" type="text" aria-label="{label}, {state}"{v}{ST_INPUT[state]}>'


EYE = ic("eye-off")

component(
    "text-field", "Text field", "Inputs",
    lead="A single-line input for short answers: email, display name, title, price, tracking number. Always inside a form field with a visible label.",
    pills=["Native <code>&lt;input&gt;</code>"],
    summary_variants="text, email, password with show toggle, number/decimal, search, prefix/suffix addon, with icon, with counter",
    summary_states="default, hover, focus, invalid, disabled, read-only, required",
    overview=p(f"Use a text field for one line of free text. Use a {comp('textarea')} for more than a sentence, a {comp('select')} when the answer comes from a short fixed list, and a {comp('radio-group')} when the member should see every option. "
               f"The field is the bare control; the label, help, error and counter around it come from {comp('form-field')}.")
    + ul("<b>Text</b>, <b>email</b>, <b>password</b>: set the right <code>type</code>, <code>autocomplete</code> and <code>inputmode</code> so phones show the right keyboard and password managers work.",
         "<b>Money</b> (<code>.input-group</code> with a <code>$</code> addon and <code>inputmode=\"decimal\"</code>): price on the sell form, the price range in filters.",
         "<b>Search</b> (<code>.search</code>): the top-bar search with a leading icon and a visually hidden label."),
    anatomy=anatomy(
        w('<div class="input-group"><span class="addon">$</span><input class="input" id="an-price" inputmode="decimal" value="45.00" aria-label="Price"></div>', "16rem"),
        [("14%", "34%"), ("50%", "34%"), ("88%", "72%")],
        [("Addon (optional)", "Unit or prefix on <code>--color-bg-subtle</code>, <code>--text-body-sm</code>, muted. Not focusable."),
         ("Value", "<code>--text-body</code> (16px, so iOS does not zoom); placeholder in <code>--color-fg-subtle</code> only as an example, never as the label."),
         ("Container", "40px (<code>--control-height-md</code>), 1px <code>--color-border-strong</code> edge, 2px corners, <code>--space-3</code> side padding.")]),
    variants=ex(w(field("v-email", "Email", type="email", attrs='autocomplete="email"', value="marcus.bell@example.com"), "18rem")
                + w('<div class="field"><label class="field__label" for="v-pw">Password</label><div class="input-group"><input class="input" id="v-pw" type="password" autocomplete="current-password" value="••••••••••••"><button class="btn btn--icon" type="button" aria-label="Show password" aria-pressed="false">' + EYE + '</button></div></div>', "18rem")
                + w(field("v-price", "Price", '<div class="input-group"><span class="addon">$</span><input class="input" id="v-price" inputmode="decimal" value="45.00"{db}></div>'), "12rem")
                + w('<form class="search" role="search"><label class="visually-hidden" for="v-q">Search 12L</label>' + ic("search") + '<input class="input" id="v-q" type="search" placeholder="Search brands and items"></form>', "18rem")
                + w(field("v-track", "Tracking number", attrs='inputmode="numeric" autocomplete="off"', value="9400 1000 0000 0000 0482 13"), "18rem"),
                "Email · password with show toggle · money with addon · search · tracking number."),
    sizes=p("Medium (40px) everywhere in forms. Small (32px, <code>.input--sm</code>) only in toolbars (sort, audit-log filter). Large (48px, <code>.input--lg</code>) for the one-time code on verify screens.")
    + ex(w(tf("sz-sm", "default").replace('class="input"', 'class="input input--sm"'), "12rem") + w(tf("sz-md", "default"), "12rem") + w(tf("sz-lg", "default").replace('class="input"', 'class="input input--lg"'), "12rem"),
         "<code>.input--sm</code> 32px · default 40px · <code>.input--lg</code> 48px."),
    states=state_matrix(INPUT_STATES, [("Text", lambda s: w(tf(f"m-{s}", s), "11rem")),
                                       ("Money", lambda s: w(f'<div class="input-group"><span class="addon">$</span><input class="input" id="mm-{s}" inputmode="decimal" aria-label="Price, {s}" value="45.00"{ST_INPUT[s]}></div>', "9rem"))], first="Type")
    + ul("<b>Invalid</b> (<code>aria-invalid=\"true\"</code>) doubles the edge in danger red; the message under the field says what to do.",
         "<b>Read-only</b> is used while a form submits (the register and profile forms) so values stay readable and selectable; it switches to the sunken background.",
         "<b>Disabled</b> is rare: a field that cannot apply yet (Type until a Category is chosen on the sell form).",
         "<b>Required</b> is the default; only optional fields are marked, with <i>(optional)</i> in the label.")
    + "<h3>Both themes</h3>" + both(lambda x: '<div class="stack">' + tf(f"th{x}a", "default") + tf(f"th{x}b", "invalid") + tf(f"th{x}c", "disabled") + "</div>"),
    responsive=ul("Fields are full width of their column at every breakpoint; the form column caps line length (<code>.page--form</code>, 44rem).",
                  "Two short fields share a row from 640px (<code>.form-row</code>); below that they stack.",
                  "Input text stays 16px on phones so iOS Safari does not zoom on focus.",
                  "The top-bar search is a field from 1024px and an icon button that opens search below it."),
    theming=p("Component tokens <code>--field-bg</code>, <code>--field-fg</code>, <code>--field-border</code>, <code>--field-border-hover</code> and <code>--field-border-invalid</code> alias the semantic tokens; override them on a container to re-skin fields (the toolbar sort uses a quieter edge).")
    + pre("""
.sort .select { --field-border: var(--color-border-default); }"""),
    accessibility=a11y(
        pattern="Native <code>&lt;input&gt;</code> with a visible <code>&lt;label for&gt;</code>. Help and error text are linked with <code>aria-describedby</code>; invalid fields set <code>aria-invalid=\"true\"</code>. The password toggle is a button with <code>aria-pressed</code> and the label <i>Show password</i>.",
        keyboard=[(kbd("Tab"), "Moves into the field; the addon is skipped."), ("Typing", "Edits the value. Arrow keys, Home and End move the caret."),
                  (kbd("Enter"), "Submits the enclosing form (forms validate and focus the error summary).")],
        focus="Focus replaces the edge with the 2px ring at 0 offset so the box does not grow. It is visible on paper and on ink.",
        labelling="Every field has a visible label; search is the only exception and carries a visually hidden one. Placeholders are examples, never labels. Use <code>autocomplete</code> tokens (<code>email</code>, <code>username</code>, <code>new-password</code>, <code>street-address</code>).",
        contrast=[("Value on field", "--color-fg-default", "--color-bg-surface", 4.5), ("Placeholder", "--color-fg-subtle", "--color-bg-surface", 4.5),
                  ("Edge on page", "--color-border-strong", "--color-bg-canvas", 3), ("Edge on card", "--color-border-strong", "--color-bg-surface", 3),
                  ("Invalid edge", "--color-danger-solid", "--color-bg-surface", 3), ("Addon text", "--color-fg-muted", "--color-bg-subtle", 4.5)],
        motion="Edge colour transitions over <code>--duration-fast</code>; zeroed under reduced motion.",
        touch="40px tall and full width, well over the 24px minimum; the password toggle is a 40px square."),
    content=ul("Labels are nouns in sentence case: <i>Display name</i>, <i>Tracking number</i>.",
               "Put format rules in help text before the member types: <i>3–30 letters, numbers, _ or -. Shown publicly.</i>",
               "Units go in an addon (<i>$</i>), not in the label.", "Never use placeholder text for instructions."),
    do_dont=dodont([
        ("do", w(field("dd-name", "Display name", help="3–30 letters, numbers, _ or -. Shown publicly.", value="marcus_12"), "18rem"), "State the rule in help text before the member types."),
        ("dont", w('<input class="input" id="dd-ph" type="text" placeholder="Display name (3–30 characters)" aria-label="Display name">', "18rem"), "A placeholder as the label disappears on typing and fails contrast for instructions."),
        ("do", w(field("dd-price", "Price", '<div class="input-group"><span class="addon">$</span><input class="input" id="dd-price" inputmode="decimal" value="45.00"{db}></div>'), "12rem"), "Money with a $ addon and a decimal keyboard."),
        ("dont", w(field("dd-price2", "Price ($)", value="$45"), "12rem"), "Unit in the label and typed into the value; parsing breaks and phones show the full keyboard."),
    ]),
    tokens=token_table([("Background / text", "--color-bg-surface / --color-fg-default"), ("Edge / hover edge", "--color-border-strong / --color-fg-muted"),
                        ("Placeholder", "--color-fg-subtle"), ("Invalid edge", "--color-danger-solid"), ("Disabled background / text", "--color-bg-subtle / --color-fg-disabled"),
                        ("Read-only background", "--color-bg-surface-sunken"), ("Addon background", "--color-bg-subtle"), ("Focus ring", "--color-focus-ring"),
                        ("Height sm / md / lg", "--control-height-sm / --control-height-md / --control-height-lg"), ("Padding", "--space-2 / --space-3"),
                        ("Radius", "--radius-md"), ("Text", "--text-body")]),
    code=pre("""
<div class="field">
  <label class="field__label" for="email">Email</label>
  <input class="input" id="email" name="email" type="email" autocomplete="email">
</div>

<div class="input-group">
  <span class="addon">$</span>
  <input class="input" id="price" name="price" inputmode="decimal" aria-describedby="price-error" aria-invalid="true">
</div>""")
    + classes([("<code>.input</code>", "The control."), ("<code>.input--sm</code> <code>.input--lg</code>", "Size."),
               ("<code>.input-group</code> + <code>.addon</code>", "Joined prefix/suffix or trailing button."), ("<code>.search</code>", "Leading search icon."),
               ("<code>aria-invalid=\"true\"</code>", "Invalid."), ("<code>readonly</code> / <code>disabled</code>", "Read-only / disabled."),
               ("<code>data-state=\"hover|focus\"</code>", "Documentation only.")]),
    sources=sources([("pages/sign-in/default", "email and password"), ("pages/register/invalid", "invalid fields with messages"), ("pages/register/submitting", "read-only while submitting"),
                     ("pages/sell/filled", "title with counter, $ price"), ("dialogs/add-tracking/default", "tracking number"), ("dialogs/filters/invalid", "price range addons")],
                    "the catalog calls for a password show toggle, but no mock had one; the system adds it as an <code>.input-group</code> button."),
)
drift("pages/sign-in/default", "Password fields have no show/hide toggle.", "Text field page documents an input-group toggle button with aria-pressed and the label “Show password”.")

# ===========================================================================
# Textarea
# ===========================================================================
REPLY = "Thanks Tom! Glad the hoodie fits. Shipped it the same day."


def ta(sfx: str, state: str, text: str = REPLY) -> str:
    return f'<textarea class="textarea" id="ta-{sfx}" rows="3" aria-label="Your reply, {state}"{ST_INPUT[state]}>{esc(text)}</textarea>'


component(
    "textarea", "Textarea", "Inputs",
    lead="A multi-line input for descriptions, review replies, report details and notes. Grows with its content and shows a counter when there is a limit.",
    pills=["Native <code>&lt;textarea&gt;</code>"],
    summary_variants="default, auto-grow, with counter",
    summary_states="default, hover, focus, invalid, disabled, read-only",
    overview=p(f"Use a textarea when the answer can run past one sentence: the listing description (2,000 characters), a review comment (500), a reply to a review, details for a report or a cancellation note. For one line, use a {comp('text-field')}.")
    + ul("Minimum two rows; three for comments and replies, four for the listing description.", "Resizable vertically only, and auto-growing where supported (<code>field-sizing: content</code>).",
         "When there is a limit, a counter sits under the field (<i>58 / 500</i>) and turns into an error past the limit."),
    anatomy=anatomy(w(field("an-ta", "Your reply", ta("an", "default").replace('id="ta-an"', 'id="an-ta"').replace(' aria-label="Your reply, default"', "{db}"), help="One reply per review. It can’t be edited later.", counter="58 / 500"), "22rem"),
                    [("6%", "6%"), ("50%", "35%"), ("50%", "74%"), ("92%", "90%")],
                    [("Label", "Visible, <code>--text-label</code>."), ("Control", "At least 2 rows (100px at <code>--control-height-md</code> × 2.5), <code>--text-body</code>, vertical resize."),
                     ("Help", "Rules that apply before typing."), ("Counter", "<code>--text-caption</code>, right-aligned, <code>--color-fg-subtle</code>.")]),
    variants=ex(w(field("v-desc", "Description", '<textarea class="textarea" id="v-desc" rows="4"{db}>Worn twice. No marks on the leather; laces replaced with originals included.</textarea>', counter="76 / 2,000"), "24rem")
                + w(field("v-note", "Note to buyer", '<textarea class="textarea" id="v-note" rows="2"{db}></textarea>', optional=True), "20rem"),
                "Listing description with counter · optional two-row note."),
    sizes=NA("Textareas have one width (their column) and set height in rows: 2 for notes, 3 for comments, 4 for descriptions."),
    states=state_matrix(INPUT_STATES, [("Textarea", lambda s: w(ta(f"m-{s}", s), "12rem"))])
    + "<h3>Over the limit</h3>" + ex(w(field("ov", "Your reply", '<textarea class="textarea" id="ov" rows="3"{db}>' + "Thanks Tom! " * 44 + "</textarea>", error="Keep the reply to 500 characters", counter="528 / 500"), "24rem"),
                                   "The counter stays; the error names the limit. The text is kept so the member can trim it.")
    + "<h3>Both themes</h3>" + both(lambda x: ta(f"th{x}", "default") + ta(f"th{x}i", "invalid")),
    responsive=ul("Full width of its column at every size.", "On phones keep the visible rows small (2–3) so the keyboard does not hide the submit button; auto-grow takes over as the member types."),
    theming=p("Same component tokens as the " + comp("text-field") + " (<code>--field-*</code>); the counter reads <code>--color-fg-subtle</code>."),
    accessibility=a11y(
        pattern="Native <code>&lt;textarea&gt;</code> with <code>&lt;label for&gt;</code>; help, error and counter are linked via <code>aria-describedby</code>. The counter is not a live region on every keystroke; it is announced when the limit is crossed through the error.",
        keyboard=[(kbd("Tab"), "Moves into and out of the textarea."), (kbd("Enter"), "New line (it never submits)."), (kbd("Ctrl", "Enter"), "Not bound; forms submit with their button.")],
        focus="Same 2px ring at 0 offset as text fields.",
        labelling="Visible label; limits stated in help or counter before the member types.",
        contrast=[("Text on field", "--color-fg-default", "--color-bg-surface", 4.5), ("Counter on page", "--color-fg-subtle", "--color-bg-canvas", 4.5), ("Edge on page", "--color-border-strong", "--color-bg-canvas", 3)],
        motion="None beyond the edge colour transition.", touch="Minimum 80px tall; the resize handle is optional, not the only way to see content (it scrolls)."),
    content=ul("Say who will read it: <i>Visible to the buyer and to 12L.</i>", "State the limit as numbers with a thousands separator: <i>76 / 2,000</i>.", "Prompt with a label, not a question in the placeholder."),
    do_dont=dodont([("do", w(field("dd-r", "Your reply", ta("dd1", "default").replace('id="ta-dd1"', 'id="dd-r"').replace(' aria-label="Your reply, default"', "{db}"), help="One reply per review. It can’t be edited later.", counter="58 / 500"), "18rem"), "Explain consequences and show the limit."),
                    ("dont", w('<textarea class="textarea" id="dd-r2" rows="1" aria-label="Reply" placeholder="Write a reply (max 500, can’t edit later)…"></textarea>', "18rem"), "One row with the rules in the placeholder."),
                    ("do", w(field("dd-f", "Describe the flaws", '<textarea class="textarea" id="dd-f" rows="2"{db}>Footbed worn at the heel.</textarea>'), "18rem"), "Ask for specifics in the label."),
                    ("dont", w('<input class="input" id="dd-f2" type="text" aria-label="Description" value="Comfortable and broken in. Regular width. Footbed worn at the…">', "18rem"), "A single-line input for a description clips the text.")]),
    tokens=token_table([("Background / text", "--color-bg-surface / --color-fg-default"), ("Edge", "--color-border-strong"), ("Invalid edge", "--color-danger-solid"),
                        ("Counter", "--color-fg-subtle"), ("Minimum height", "--control-height-md"), ("Padding", "--space-2 / --space-3"), ("Radius", "--radius-md")]),
    code=pre("""
<div class="field">
  <label class="field__label" for="reply">Your reply</label>
  <textarea class="textarea" id="reply" rows="3" aria-describedby="reply-help"></textarea>
  <span class="field__help" id="reply-help">One reply per review. It can’t be edited later.</span>
  <span class="field__counter">0 / 500</span>
</div>""")
    + classes([("<code>.textarea</code>", "The control; vertical resize, auto-grow where supported."), ("<code>rows</code>", "Initial height; minimum 2."),
               ("<code>.field__counter</code>", "Character count under the field.")]),
    sources=sources([("dialogs/reply-review/default", "reply with help and counter"), ("dialogs/reply-review/invalid", "over the limit"),
                     ("pages/sell/filled", "description with 2,000 counter"), ("dialogs/cancel-order/default", "optional note"), ("dialogs/leave-review/invalid", "review comment error")]),
)

# ===========================================================================
# Select
# ===========================================================================
CATS = ["Shoes", "Tops", "Outerwear", "Bottoms"]


def sel(sfx: str, state: str, chosen: str = "Shoes", cls: str = "select", label: str = "Category") -> str:
    opts = '<option value="">Choose a category</option>' + "".join(f'<option{" selected" if c == chosen else ""}>{c}</option>' for c in CATS)
    st = ST_INPUT[state] if state != "read-only" else ' aria-readonly="true"'
    return f'<select class="{cls}" id="sel-{sfx}" aria-label="{label}, {state}"{st}>{opts}</select>'


component(
    "select", "Select", "Inputs",
    lead="A native drop-down for one answer from a fixed list: category, type, state, country, carrier, sort order.",
    pills=["Native <code>&lt;select&gt;</code>"],
    summary_variants="native, with placeholder option, dependent (disabled until parent chosen), toolbar sort",
    summary_states="default, hover, focus, invalid, disabled",
    overview=p(f"Use a select for 5–15 known options where the member knows the answer (their state, the carrier). Under five options that deserve comparison, use a {comp('radio-group')} or segmented {comp('button-group')}. "
               "12L uses the native element everywhere: it gets the platform picker on phones, type-ahead and full accessibility for free. A custom listbox is only justified when options need rich content.")
    + ul("<b>Placeholder option</b> (<i>Choose a category</i>, <code>value=\"\"</code>) when there is no safe default; validation treats it as empty.",
         "<b>Dependent</b>: <i>Type</i> is disabled until <i>Category</i> is chosen on the sell form.",
         "<b>Toolbar sort</b>: small, with a quieter edge, labelled by a visible <i>Sort</i> prefix."),
    anatomy=anatomy(w(sel("an", "default"), "16rem"), [("30%", "34%"), ("90%", "34%")],
                    [("Selected value", "<code>--text-body</code>; the placeholder option reads as a value, so the field label must carry the question."),
                     ("Chevron", "Drawn with two gradients in <code>currentColor</code>, 40px reserved on the right (<code>--space-10</code>).")]),
    variants=ex(w(field("v-cat", "Category", '<select class="select" id="v-cat"{db}><option value="">Choose a category</option>' + "".join(f"<option>{c}</option>" for c in CATS) + "</select>"), "16rem")
                + w(field("v-sub", "Type", '<select class="select" id="v-sub" disabled{db}><option value="">Choose a type</option></select>', help="Choose a category first."), "16rem")
                + '<label class="sort"><span class="text-sm text-muted">Sort</span><select class="select input--sm"><option>Newest</option><option>Price: low to high</option><option>Price: high to low</option></select></label>',
                "Placeholder option · dependent and disabled · toolbar sort."),
    sizes=ex(w(sel("sm", "default", cls="select input--sm"), "12rem") + w(sel("md", "default"), "12rem") + w(sel("lg", "default", cls="select input--lg"), "12rem"), "32px toolbar · 40px form default · 48px."),
    states=state_matrix(["Default", "Hover", "Focus", "Invalid", "Disabled"], [("Select", lambda s: w(sel(f"m-{s}", s, "" if s == "invalid" else "Shoes"), "12rem"))])
    + "<h3>Both themes</h3>" + both(lambda x: '<div class="stack">' + sel(f"th{x}", "default") + sel(f"th{x}i", "invalid", "") + "</div>"),
    responsive=ul("Full width in forms; auto width in toolbars.", "On phones the OS picker replaces the drop-down list; nothing to design there.", "State and ZIP share a row from 640px on the address form."),
    theming=p("Shares <code>--field-*</code> tokens with text fields. The chevron uses <code>currentColor</code>, so it follows <code>--field-fg</code> in both themes. Toolbars override <code>--field-border</code> with <code>--color-border-default</code>."),
    accessibility=a11y(
        pattern="Native <code>&lt;select&gt;</code> with <code>&lt;label for&gt;</code>; errors via <code>aria-describedby</code> and <code>aria-invalid</code>. If a custom listbox is ever needed, it follows the APG Select-Only Combobox.",
        keyboard=[(kbd("Tab"), "Focuses the select."), (kbd("↑") + " " + kbd("↓"), "Changes the option (Windows) or opens the list (macOS)."),
                  (kbd("Space") + " / " + kbd("Alt", "↓"), "Opens the list."), ("Typing", "Jumps to the matching option."), (kbd("Esc"), "Closes the list without changing.")],
        focus="2px ring at 0 offset, as text fields.", labelling="Visible label; the toolbar sort is wrapped in a <code>&lt;label&gt;</code> with visible text <i>Sort</i>.",
        contrast=[("Value on field", "--color-fg-default", "--color-bg-surface", 4.5), ("Edge on page", "--color-border-strong", "--color-bg-canvas", 3), ("Invalid edge", "--color-danger-solid", "--color-bg-surface", 3)],
        motion="None.", touch="40px tall (32px in toolbars, with a 44px row around it)."),
    content=ul("Placeholder options start with a verb: <i>Choose a category</i>, <i>Select a state</i>.", "Order options logically (alphabetical states; categories in catalog order), not by internal id.", "Show the current sort in the selected option text; no separate label needed beyond <i>Sort</i>."),
    do_dont=dodont([("do", w(field("dd-st", "State", '<select class="select" id="dd-st"{db}><option>Select a state</option><option>Colorado</option><option>New York</option></select>'), "14rem"), "A native select for a long, known list."),
                    ("dont", w('<select class="select" id="dd-yn" aria-label="Accept terms"><option>Yes</option><option>No</option></select>', "14rem"), "A select for a yes/no choice; use a checkbox."),
                    ("do", w(field("dd-sub", "Type", '<select class="select" id="dd-sub" disabled{db}><option>Choose a type</option></select>', help="Choose a category first."), "14rem"), "Explain why a dependent select is disabled."),
                    ("dont", w(sel("dd-nolabel", "default").replace(' aria-label="Category, default"', ' aria-label="Choose"'), "14rem"), "Rely on the placeholder option instead of a visible label.")]),
    tokens=token_table([("Background / text", "--color-bg-surface / --color-fg-default"), ("Edge", "--color-border-strong"), ("Invalid edge", "--color-danger-solid"),
                        ("Disabled", "--color-bg-subtle / --color-fg-disabled"), ("Chevron space", "--space-10"), ("Height", "--control-height-md")]),
    code=pre("""
<div class="field">
  <label class="field__label" for="cat">Category</label>
  <select class="select" id="cat" name="cat">
    <option value="">Choose a category</option>
    <option>Shoes</option><option>Tops</option>
  </select>
</div>""")
    + classes([("<code>.select</code>", "Native select with the 12L chevron."), ("<code>.input--sm</code> <code>.input--lg</code>", "Sizes."), ("<code>.sort</code>", "Inline label + small select for toolbars.")]),
    sources=sources([("pages/sell/default", "Category and dependent Type"), ("pages/checkout/new-address", "State and Country"), ("dialogs/add-tracking/default", "Carrier"),
                     ("pages/catalog/default", "toolbar Sort"), ("pages/audit-log/default", "toolbar Action filter")]),
)

# ===========================================================================
# Checkbox
# ===========================================================================


def cb(sfx: str, state: str, label: str = "I’m 18 or older") -> str:
    attrs = {"default": "", "hover": ' data-state="hover"', "focus": ' data-state="focus"', "checked": " checked",
             "indeterminate": ' data-state="indeterminate" aria-checked="mixed"', "invalid": ' aria-invalid="true"', "disabled": " disabled"}[state]
    return f'<label class="choice"><input type="checkbox" id="cb-{sfx}"{attrs}><span>{label}</span></label>'


component(
    "checkbox", "Checkbox", "Inputs",
    lead="A square box for an independent yes/no: accepting terms, confirming the label shows US 12, picking any number of filters.",
    pills=["Native checkbox"],
    summary_variants="single, group in fieldset, with description",
    summary_states="default, hover, focus, checked, indeterminate, invalid, disabled",
    overview=p(f"Use a checkbox for a choice that stands alone (<i>I accept the terms</i>) or for picking any number from a list (filters: <i>Sneakers</i>, <i>Boots</i>). For exactly one of several, use a {comp('radio-group')}. "
               f"For a setting that applies immediately, use a {comp('switch')}.")
    + ul("Square (<code>--radius-xs</code> is 0) like the logo; ink fill with a paper tick when checked.", "Groups live in a <code>&lt;fieldset&gt;</code> with a <code>&lt;legend&gt;</code>; the whole label is the target."),
    anatomy=anatomy(cb("an", "checked", "Confirm the label shows men’s US 12"), [("6%", "30%"), ("40%", "30%")],
                    [("Box", "20px square, 1px <code>--color-border-strong</code> edge; checked fills with <code>--color-accent</code> and a <code>--color-fg-on-accent</code> tick."),
                     ("Label", "<code>--text-body</code>, wraps beside the box; clicking it toggles.")]),
    variants=ex(cb("v1", "default", 'I accept the <a href="#">terms</a> and <a href="#">marketplace rules</a>'), "Single, with links in the label.")
    + ex('<fieldset><legend>Type</legend><div class="stack stack--sm">' + cb("v2a", "checked", "Sneakers") + cb("v2b", "default", "Boots") + cb("v2c", "default", "Dress shoes") + "</div></fieldset>", "Group in a fieldset (catalog filters).")
    + ex('<label class="choice"><input type="checkbox" id="v3" checked><span class="choice__text">Show my city on my profile<small>Brooklyn, NY appears under your name.</small></span></label>', "With a description (<code>.choice__text</code>)."),
    sizes=NA("One size: a 20px box with a row at least 24px tall (--target-min)."),
    states=state_matrix(["Default", "Hover", "Focus", "Checked", "Indeterminate", "Invalid", "Disabled"], [("Checkbox", lambda s: cb(f"m-{s}", s, "Boots"))], first="Control")
    + p("Indeterminate is set from script (<code>input.indeterminate = true</code>) for a parent that summarises a partly checked group; it is shown here with <code>data-state</code>.")
    + "<h3>Invalid with message</h3>" + ex('<div class="field">' + cb("inv", "invalid", "Confirm the label shows men’s US 12").replace("aria-invalid=\"true\"", 'aria-invalid="true" aria-describedby="inv-error"') + '<span class="field__error" id="inv-error">Confirm the label shows men’s US 12</span></div>')
    + "<h3>Both themes</h3>" + both(lambda x: '<div class="stack stack--sm">' + cb(f"t{x}1", "default", "Sneakers") + cb(f"t{x}2", "checked", "Boots") + cb(f"t{x}3", "disabled", "Sandals") + "</div>"),
    responsive=ul("Labels wrap beside the box; the box stays top-aligned with the first line.", "Filter groups sit in the sidebar from 1024px and in the filter sheet below it; same markup."),
    theming=p("Reads <code>--color-border-strong</code>, <code>--color-bg-surface</code>, and when checked <code>--color-accent</code> with <code>--color-fg-on-accent</code>; in the dark theme the box fills paper with an ink tick."),
    accessibility=a11y(
        pattern="Native <code>&lt;input type=\"checkbox\"&gt;</code> inside its <code>&lt;label&gt;</code>; groups in <code>&lt;fieldset&gt;</code>/<code>&lt;legend&gt;</code>. Mixed state uses the <code>indeterminate</code> property (exposed as mixed).",
        keyboard=[(kbd("Tab"), "Moves to each checkbox."), (kbd("Space"), "Toggles.")],
        focus="The ring is drawn around the box (2px, 2px offset).",
        labelling="The label text is the name; errors are linked with <code>aria-describedby</code> and the group legend gives context.",
        contrast=[("Box edge on page", "--color-border-strong", "--color-bg-canvas", 3), ("Tick on fill", "--color-fg-on-accent", "--color-accent", 3), ("Checked fill on page", "--color-accent", "--color-bg-canvas", 3), ("Invalid edge", "--color-danger-solid", "--color-bg-surface", 3)],
        motion="Fill transitions over <code>--duration-fast</code>.", touch="The whole label is the target; rows are at least 24px tall with 8px between them."),
    content=ul("Write the label as the statement being agreed to: <i>I’m 18 or older</i>.", "Errors repeat what to tick: <i>Accept the terms to continue</i>.", "Never pre-tick consent or marketing boxes."),
    do_dont=dodont([("do", cb("dd1", "default", "Email me new arrivals in my size"), "Leave optional consent unticked."),
                    ("dont", cb("dd2", "checked", "Email me new arrivals in my size"), "Pre-tick marketing consent."),
                    ("do", '<fieldset><legend>Type</legend>' + cb("dd3a", "checked", "Sneakers") + cb("dd3b", "checked", "Boots") + "</fieldset>", "Checkboxes when several can apply."),
                    ("dont", '<fieldset><legend>Condition</legend>' + cb("dd4a", "checked", "Used - Good") + cb("dd4b", "checked", "Used - Fair") + "</fieldset>", "Checkboxes for a value that can have only one answer.")]),
    tokens=token_table([("Box edge", "--color-border-strong"), ("Box background", "--color-bg-surface"), ("Checked fill", "--color-accent"), ("Tick", "--color-fg-on-accent"),
                        ("Invalid edge", "--color-danger-solid"), ("Disabled", "--color-bg-subtle / --color-fg-disabled"), ("Radius", "--radius-xs"), ("Row height", "--target-min"), ("Gap", "--space-3")]),
    code=pre("""
<label class="choice"><input type="checkbox" id="age" name="age"><span>I’m 18 or older</span></label>""")
    + classes([("<code>.choice</code>", "Label row for a checkbox or radio."), ("<code>.choice__text</code>", "Label + description stack."),
               ("<code>aria-invalid=\"true\"</code>", "Invalid edge."), ("<code>data-state=\"indeterminate\"</code>", "Documentation only; use the property in product.")]),
    sources=sources([("pages/register/default", "age and terms"), ("pages/register/invalid", "invalid ticks"), ("pages/sell/invalid", "size confirmation"), ("pages/catalog/default", "filter groups")]),
)

# ===========================================================================
# Radio group
# ===========================================================================


def rd(sfx: str, state: str, label: str, name: str) -> str:
    attrs = {"default": "", "hover": ' data-state="hover"', "focus": ' data-state="focus"', "checked": " checked", "invalid": ' aria-invalid="true"', "disabled": " disabled"}[state]
    return f'<label class="choice"><input type="radio" name="{name}" id="rd-{sfx}"{attrs}><span>{label}</span></label>'


def opt(sfx: str, state: str, body: str, name: str) -> str:
    attrs = {"default": "", "hover": "", "focus": ' data-state="focus"', "checked": " checked", "invalid": ' aria-invalid="true"', "disabled": " disabled"}[state]
    hv = ' data-state="hover"' if state == "hover" else ""
    return f'<label class="option"{hv}><input type="radio" name="{name}" id="op-{sfx}"{attrs}><span class="option__body">{body}</span></label>'


ADDR = '<address class="address">Marcus Bell<br>214 Kent Ave, Apt 3R<br>Brooklyn, NY 11249</address>'
REASONS = ["Buyer asked to cancel", "Item is damaged", "Item is no longer available"]

component(
    "radio-group", "Radio group", "Inputs",
    lead="One answer from a short list where every option should be read: a cancellation reason, a report decision, the shipping address at checkout.",
    pills=["<code>fieldset</code> + native radios"],
    summary_variants="vertical list, with descriptions, option cards; segmented (see button group)",
    summary_states="default, hover, focus, checked, invalid, disabled",
    overview=p(f"Use radios for two to seven options with exactly one answer. With short labels that fit side by side use the segmented {comp('button-group')}; for long known lists use a {comp('select')}.")
    + ul("<b>List</b> (<code>.choice</code>): reasons and decisions in dialogs.", "<b>With description</b> (<code>.choice__text</code>): admin decisions that need a consequence line.",
         "<b>Option cards</b> (<code>.option</code>): the whole card is the target; used for addresses at checkout where the option contains rich content."),
    anatomy=anatomy(w('<fieldset class="stack"><legend>Ship to</legend>' + opt("an", "checked", ADDR, "an") + "</fieldset>", "18rem"), [("6%", "10%"), ("12%", "40%"), ("60%", "55%")],
                    [("Legend", "The question."), ("Radio", "20px circle; checked fills ink with a paper dot."), ("Option card", "Surface, 1px edge; checked edge doubles in <code>--color-fg-default</code>.")]),
    variants=ex('<fieldset><legend>Reason</legend><div class="stack stack--sm">' + "".join(rd(f"v1{i}", "checked" if i == 0 else "default", r, "v1") for i, r in enumerate(REASONS)) + "</div></fieldset>", "Vertical list (cancel order).")
    + ex('<fieldset><legend>Decision</legend><div class="stack stack--sm"><label class="choice"><input type="radio" name="v2" id="v2a" checked><span class="choice__text">Remove listing<small>Hidden for good; the seller is told why.</small></span></label>'
         '<label class="choice"><input type="radio" name="v2" id="v2b"><span class="choice__text">Dismiss reports<small>The listing returns to the catalog.</small></span></label></div></fieldset>', "With descriptions (resolve report).")
    + ex(w('<fieldset class="stack"><legend>Ship to</legend>' + opt("v3a", "checked", ADDR, "v3") + opt("v3b", "default", "New address", "v3") + "</fieldset>", "22rem"), "Option cards (checkout)."),
    sizes=NA("One size: 20px controls, rows at least 24px; option cards pad with --space-4."),
    states=state_matrix(["Default", "Hover", "Focus", "Checked", "Invalid", "Disabled"],
                        [("List", lambda s: rd(f"m-{s}", s, "Item is damaged", f"m-{s}")), ("Option card", lambda s: w(opt(f"o-{s}", s, "New address", f"o-{s}"), "11rem"))], first="Variant")
    + "<h3>Both themes</h3>" + both(lambda x: '<div class="stack">' + opt(f"t{x}a", "checked", ADDR, f"t{x}") + rd(f"t{x}b", "default", "Item is damaged", f"t{x}r") + "</div>"),
    responsive=ul("Lists stay vertical at every width.", "Option cards fill the column; they stack, never sit side by side, so long addresses wrap cleanly."),
    theming=p("Radios share checkbox tokens. Option cards read <code>--color-bg-surface</code> and <code>--color-border-default</code>, hover <code>--color-border-strong</code>, and the checked card draws an inset 1px ring in <code>--color-fg-default</code> on top of its edge."),
    accessibility=a11y(
        pattern="Native radios sharing a <code>name</code> inside <code>&lt;fieldset&gt;</code>/<code>&lt;legend&gt;</code> (APG Radio Group behaviour from the browser). Option cards are <code>&lt;label&gt;</code> elements wrapping the radio, so the whole card toggles it.",
        keyboard=[(kbd("Tab"), "Into the group (the checked radio, or the first), then out."), (kbd("↑") + " " + kbd("↓") + " / " + kbd("←") + " " + kbd("→"), "Moves and checks."), (kbd("Space"), "Checks the focused radio.")],
        focus="Ring around the radio circle; option cards also show it on the radio, which sits at the card's start.",
        labelling="Legend names the group; error linked from the fieldset with <code>aria-describedby</code>.",
        contrast=[("Radio edge on page", "--color-border-strong", "--color-bg-canvas", 3), ("Checked fill", "--color-accent", "--color-bg-surface", 3), ("Card text", "--color-fg-default", "--color-bg-surface", 4.5)],
        motion="Edge and fill transition over <code>--duration-fast</code>.", touch="Option cards are large targets; list rows are at least 24px with 8px gaps."),
    content=ul("Options are parallel phrases of similar length.", "Order by likelihood, or logically; never preselect a consequential choice such as a cancellation reason.", "Describe consequences in the description line, not the label."),
    do_dont=dodont([("do", '<fieldset><legend>Reason</legend>' + "".join(rd(f"dd1{i}", "default", r, "dd1") for i, r in enumerate(REASONS)) + "</fieldset>", "No preselection for a reason the seller must choose."),
                    ("dont", '<fieldset><legend>Reason</legend>' + rd("dd2a", "checked", "Other", "dd2") + rd("dd2b", "default", "Buyer asked to cancel", "dd2") + "</fieldset>", "Preselect “Other” and hide the real reasons below it."),
                    ("do", w(opt("dd3", "checked", ADDR, "dd3"), "16rem"), "Option cards for options with rich content."),
                    ("dont", w('<fieldset><legend>Ship to</legend>' + rd("dd4", "checked", "Marcus Bell, 214 Kent Ave, Apt 3R, Brooklyn, NY 11249, United States", "dd4") + "</fieldset>", "16rem"), "Cram an address into one radio label.")]),
    tokens=token_table([("Radio edge / fill", "--color-border-strong / --color-accent"), ("Dot", "--color-fg-on-accent"), ("Card background / edge", "--color-bg-surface / --color-border-default"),
                        ("Card hover edge", "--color-border-strong"), ("Card checked ring", "--color-fg-default"), ("Card padding", "--space-4"), ("Radius", "--radius-full")]),
    code=pre("""
<fieldset>
  <legend>Reason</legend>
  <label class="choice"><input type="radio" name="reason" value="buyer"><span>Buyer asked to cancel</span></label>
  <label class="choice"><input type="radio" name="reason" value="damaged"><span>Item is damaged</span></label>
</fieldset>

<label class="option"><input type="radio" name="addr" checked><span class="option__body"><address class="address">…</address></span></label>""")
    + classes([("<code>.choice</code>", "Radio row."), ("<code>.option</code>", "Card that wraps a radio and its rich body."), ("<code>.option__body</code>", "Card content."),
               ("<code>.segmented</code>", "Side-by-side variant; see " + comp("button-group") + ".")]),
    sources=sources([("dialogs/cancel-order/default", "reason list"), ("dialogs/cancel-order/invalid", "invalid reason"), ("dialogs/resolve-report/default", "decision with descriptions"),
                     ("pages/checkout/default", "address option cards")]),
)

# ===========================================================================
# Switch
# ===========================================================================


def sw(sfx: str, state: str, label: str = "Reviews") -> str:
    attrs = {"off": "", "on": " checked", "hover": ' data-state="hover"', "focus": ' data-state="focus"', "disabled off": " disabled", "disabled on": " checked disabled"}[state]
    return f'<label class="switch"><input type="checkbox" role="switch" id="sw-{sfx}"{attrs}><span>{label}</span></label>'


def sw_row(sfx: str, title: str, meta: str, on: bool, disabled: bool = False) -> str:
    return (f'<label class="switch switch--between"><span class="choice__text">{title}<small>{meta}</small></span>'
            f'<input type="checkbox" role="switch" id="swr-{sfx}"{" checked" if on else ""}{" disabled" if disabled else ""}></label>')


component(
    "switch", "Switch", "Inputs",
    lead="An on/off control for a setting: which emails 12L sends, whether analytics cookies are allowed. The label names the setting, not the action.",
    pills=["<code>role=\"switch\"</code> on a checkbox"],
    summary_variants="label right, label left (row, .switch--between), with description",
    summary_states="off, on, hover, focus, disabled off, disabled on",
    overview=p(f"Use a switch for a setting that is either on or off. In 12L switches sit in settings lists saved by a button (<i>Save</i> on Emails) or apply at once (cookie settings). For agreeing to something, use a {comp('checkbox')}.")
    + ul("Square track and thumb, echoing the logo; the checked track is ink (paper in dark).", "Mandatory settings are shown on and disabled with the reason in the description (<i>Always on</i>)."),
    anatomy=anatomy(w(sw_row("an", "Analytics", "Helps us see which pages are slow.", True), "20rem"), [("20%", "30%"), ("88%", "40%")],
                    [("Label and description", "<code>.choice__text</code>: setting name and what it controls."), ("Track and thumb", "44 × 24px track, 20px thumb; thumb slides 20px when on.")]),
    variants=ex(sw("v1", "on", "Reviews") + sw("v2", "off", "News from 12L"), "Label right (compact).")
    + ex(w('<div class="stack">' + sw_row("v3", "Strictly necessary", "Sign-in and checkout. Always on.", True, True) + sw_row("v4", "Analytics", "Helps us see which pages are slow.", False) + "</div>", "24rem"), "Row with label left and description (cookie settings)."),
    sizes=NA("One size: a 44 × 24px track in a row at least 24px tall."),
    states=state_matrix(["Off", "On", "Hover", "Focus", "Disabled off", "Disabled on"], [("Switch", lambda s: sw(f"m-{s.replace(' ', '-')}", s, "Reviews"))], first="Control")
    + "<h3>Both themes</h3>" + both(lambda x: sw(f"t{x}1", "on", "Reviews") + sw(f"t{x}2", "off", "News from 12L")),
    responsive=ul("Rows keep label left, switch right at every width; the label wraps, the switch never moves below it.", "In settings lists the switch aligns to the row's end."),
    theming=p("Off track <code>--color-border-strong</code>, on track <code>--color-accent</code>, thumb <code>--color-bg-surface</code> with <code>--shadow-1</code>. Dark theme: paper track when on, ink thumb."),
    accessibility=a11y(
        pattern="Native checkbox with <code>role=\"switch\"</code>, so it announces on/off; inside a <code>&lt;label&gt;</code>. In the Emails list the visible row title names the switch through visually hidden text in the label.",
        keyboard=[(kbd("Tab"), "Moves to the switch."), (kbd("Space"), "Toggles.")],
        focus="Ring around the track (2px, 2px offset).", labelling="Name the setting (<i>Analytics</i>), never <i>Turn on analytics</i>; state is announced by the role.",
        contrast=[("Off track on surface", "--color-border-strong", "--color-bg-surface", 3), ("On track on surface", "--color-accent", "--color-bg-surface", 3), ("Thumb on on-track", "--color-bg-surface", "--color-accent", 3)],
        motion="Thumb slides and track colour changes over <code>--duration-base</code> (200ms); reduced motion makes it instant.", touch="The whole label row is the target."),
    content=ul("Labels are nouns for the setting: <i>Reviews</i>, <i>News from 12L</i>.", "Descriptions say what is sent or tracked: <i>When someone reviews you</i>.", "Explain disabled switches: <i>Always on</i>."),
    do_dont=dodont([("do", sw("dd1", "on", "Reviews"), "Name the setting."), ("dont", sw("dd2", "off", "Click to turn on review emails"), "Describe the action; the state already says it."),
                    ("do", w(sw_row("dd3", "Orders", "Sales, shipping, delivery, refunds. Always on.", True, True), "18rem"), "Show mandatory settings as on and disabled, with the reason."),
                    ("dont", cb("dd4", "checked", "Analytics cookies"), "A checkbox for a setting that applies immediately reads like consent to a form.")]),
    tokens=token_table([("Track off / on", "--color-border-strong / --color-accent"), ("Thumb", "--color-bg-surface"), ("Thumb shadow", "--shadow-1"), ("Track / thumb radius", "--radius-sm / --radius-xs"), ("Row height", "--target-min"), ("Motion", "--duration-base / --ease-standard")]),
    code=pre("""
<label class="switch switch--between">
  <span class="choice__text">Analytics<small>Helps us see which pages are slow.</small></span>
  <input type="checkbox" role="switch" name="analytics">
</label>""")
    + classes([("<code>.switch</code>", "Inline switch with label."), ("<code>.switch--between</code>", "Full-width row, label start, switch end."), ("<code>role=\"switch\"</code>", "Required on the input.")]),
    sources=sources([("pages/notification-settings/default", "email switches"), ("pages/notification-settings/submitting", "disabled while saving"), ("dialogs/cookie-settings/default", "rows with descriptions"), ("dialogs/cookie-settings/analytics-on", "on state")],
                    "cookie-settings rows set <code>justify-content</code> and <code>width</code> inline; the system adds <code>.switch--between</code>."),
)
drift("dialogs/cookie-settings/default", "Switch rows use inline style (justify-content: space-between; width: 100%).", "Added .switch--between.")

# ===========================================================================
# File upload
# ===========================================================================
PH = [("sneaker-white", 6), ("sneaker-white", 1), ("sneaker-white", 4)]


def tile(i: int) -> str:
    cover = '<span class="badge uploader__cover">Cover</span>' if i == 1 else ""
    return (f'<li>{photo("air-max-90", tag=False, alt=f"Photo {i}")}{cover}'
            f'<button class="btn btn--icon btn--sm uploader__remove" type="button" aria-label="Remove photo {i}">{ic("close", "icon icon--sm")}</button></li>')


def add(sfx: str, n: int, state: str = "") -> str:
    inv = ' aria-invalid="true"' if state == "invalid" else ""
    st = f' data-state="{state}"' if state in ("hover", "dragging", "focus") else ""
    return (f'<li><label class="uploader__add"{inv}{st}>{ic("camera", "icon icon--lg")}<span>Add photos</span><span class="text-caption">{n} of 8</span>'
            f'<input class="visually-hidden" id="up-{sfx}" type="file" accept="image/jpeg,image/png,image/webp" multiple></label></li>')


def uploading(sfx: str) -> str:
    return (f'<li>{photo("air-max-90", tag=False, alt="Photo 4, uploading")}<div class="uploader__progress"><div class="progress" role="progressbar" aria-label="Uploading photo 4" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100" style="--value: 60%;"><div class="progress__bar"></div></div></div></li>')


def rejected() -> str:
    return (f'<li><div class="uploader__rejected">{ic("x-circle")}<span>IMG_4471.jpg</span><span>11.4 MB</span></div>'
            f'<button class="btn btn--icon btn--sm uploader__remove" type="button" aria-label="Remove IMG_4471.jpg">{ic("close", "icon icon--sm")}</button></li>')


def up(inner: str, width: str = "30rem", cols: int = 4) -> str:
    return w(f'<ul class="uploader" role="list" style="grid-template-columns: repeat({cols}, minmax(0, 1fr));">{inner}</ul>', width)


component(
    "file-upload", "File upload", "Inputs",
    lead="The photo uploader on the sell form and problem reports: a grid of square tiles, the first is the cover, with an Add photos tile that opens the file picker or takes a drop.",
    pills=["<code>&lt;input type=\"file\"&gt;</code>"],
    summary_variants="photo grid with cover, add tile, upload progress, rejected file",
    summary_states="empty, hover, focus, dragging, uploading, rejected, invalid",
    overview=p("Use the uploader for photos of an item: 1–8 on a listing, up to 4 on a problem report. The real control is a visually hidden <code>&lt;input type=\"file\" multiple&gt;</code> inside the Add photos label; drag-and-drop and reordering are enhancements on top.")
    + ul("The first tile is the cover and carries a <i>Cover</i> badge.", "Each tile has a labelled remove button (<i>Remove photo 2</i>).", "Rejected files stay as a red tile naming the file and why, until removed."),
    anatomy=anatomy(up(tile(1) + add("an", 1), "16rem", 2), [("30%", "26%"), ("47%", "22%"), ("76%", "55%")],
                    [("Cover badge", "<code>.badge</code> on the first photo."), ("Remove", "Small icon button, surface background, top-right."), ("Add tile", "Dashed 1px <code>--color-border-strong</code>, camera icon, count <i>1 of 8</i>.")]),
    variants=ex(up(tile(1) + tile(2) + uploading("v") + rejected() + add("v", 3), "38rem", 5), "Photos with cover, one uploading, one rejected, and the add tile.")
    + '<span class="field__help">JPEG, PNG or WebP up to 10 MB. Drag to reorder; the first is the cover.</span>',
    sizes=NA("Tiles size to the grid: 3 columns below 640px, 4 from 640px."),
    states=matrix(["Empty", "Hover", "Focus", "Dragging", "Uploading", "Rejected", "Invalid"], [("Uploader", [
        up(add("s-e", 0), "7rem", 1), up(add("s-h", 0, "hover"), "7rem", 1), up(add("s-f", 0, "focus"), "7rem", 1), up(add("s-d", 0, "dragging"), "7rem", 1),
        up(uploading("s-u"), "7rem", 1), up(rejected(), "7rem", 1), up(add("s-i", 0, "invalid"), "7rem", 1)])], first="Component")
    + "<h3>Both themes</h3>" + both(lambda x: up(tile(1) + rejected() + add(f"t{x}", 1), "20rem", 3)),
    responsive=ul("3 columns with 8px gaps below 640px; 4 columns with 12px gaps from 640px.", "On phones the file picker offers the camera directly (<code>accept=\"image/*\"</code> types).", "Reordering by drag has a keyboard alternative: Move earlier / Move later buttons in each tile's menu."),
    theming=p("Add tile: <code>--color-border-strong</code> dashed edge, <code>--color-fg-muted</code> text; hover and dragging switch to <code>--color-fg-default</code>. Rejected tile: <code>--color-danger-bg</code> with <code>--color-danger-fg</code>. Photos keep their light studio backdrops in dark theme."),
    accessibility=a11y(
        pattern="The native file input is the control (inside the Add photos <code>&lt;label&gt;</code>); the list is <code>role=\"list\"</code>; progress uses <code>role=\"progressbar\"</code>. Drop is an enhancement only.",
        keyboard=[(kbd("Tab"), "Reaches the Add photos tile (the hidden input) and each remove button."), (kbd("Enter") + " / " + kbd("Space"), "Opens the file picker or removes a photo.")],
        focus="The ring is drawn on the add tile via <code>:focus-within</code>.",
        labelling="Remove buttons name the photo. Errors (<i>Add at least one photo. Photos must be 10 MB or smaller.</i>) are linked to the input with <code>aria-describedby</code>; upload completion is announced in the form's live region.",
        contrast=[("Add tile edge", "--color-border-strong", "--color-bg-canvas", 3), ("Add tile text", "--color-fg-muted", "--color-bg-canvas", 4.5), ("Rejected text", "--color-danger-fg", "--color-danger-bg", 4.5)],
        motion="Progress fill animates over <code>--duration-slow</code>; zeroed under reduced motion.", touch="Tiles are at least 96px square; remove buttons are 32px."),
    content=ul("State the formats and limit once, in help: <i>JPEG, PNG or WebP up to 10 MB.</i>", "Rejected tiles show the file name and size, so the member knows which photo failed.", "Show the count against the limit: <i>3 of 8</i>."),
    do_dont=dodont([("do", up(rejected() + add("dd1", 0), "14rem", 2), "Keep a rejected file visible with its name and size."),
                    ("dont", up(add("dd2", 0), "7rem", 1), "Silently drop a file that was too large."),
                    ("do", up(tile(1) + add("dd3", 1), "14rem", 2), "Mark the cover photo."),
                    ("dont", w('<div class="uploader__add" role="button" tabindex="0" aria-label="Drop zone">Drop files here</div>', "10rem"), "A drop-only zone with no file input; keyboard and phone users cannot add photos.")]),
    tokens=token_table([("Add tile edge / text", "--color-border-strong / --color-fg-muted"), ("Rejected", "--color-danger-bg / --color-danger-fg"), ("Rejected edge", "--color-danger-solid"),
                        ("Remove button background", "--color-bg-surface"), ("Grid gap phone / tablet", "--space-2 / --space-3"), ("Progress fill", "--color-accent")]),
    code=pre("""
<ul class="uploader" role="list">
  <li><div class="photo">…</div><span class="badge uploader__cover">Cover</span>
      <button class="btn btn--icon btn--sm uploader__remove" type="button" aria-label="Remove photo 1">…</button></li>
  <li><label class="uploader__add">… Add photos <span class="text-caption">1 of 8</span>
      <input class="visually-hidden" id="photos" type="file" accept="image/jpeg,image/png,image/webp" multiple aria-describedby="photos-help"></label></li>
</ul>""")
    + classes([("<code>.uploader</code>", "Grid of tiles."), ("<code>.uploader__add</code>", "Add tile; <code>aria-invalid</code> for errors."), ("<code>.uploader__cover</code>", "Cover badge."),
               ("<code>.uploader__remove</code>", "Remove button."), ("<code>.uploader__rejected</code>", "Rejected file tile."), ("<code>.uploader__progress</code>", "Progress bar over an uploading tile."),
               ("<code>data-state=\"dragging\"</code>", "Set while a file is dragged over (also used here for documentation).")]),
    sources=sources([("pages/sell/filled", "photos with cover"), ("pages/sell/invalid", "rejected file and invalid add tile"), ("dialogs/report-problem/default", "up to 4 photos")],
                    "the mocks had no dragging or uploading tile state; the system adds both."),
)

# ===========================================================================
# Form field
# ===========================================================================
component(
    "form-field", "Form field", "Inputs",
    lead="The wrapper every input sits in: label, optional marker, control, help, error and counter, always in that order and spacing.",
    pills=["<code>.field</code> wrapper"],
    summary_variants="label + control, with help, with error, optional, with counter, choice field",
    summary_states="default, invalid, read-only (submitting), disabled",
    overview=p(f"Every {comp('text-field')}, {comp('textarea')}, {comp('select')} and single {comp('checkbox')} is wrapped in a <code>.field</code>. It fixes the vertical rhythm (<code>--space-1</code> between parts) and wires the accessibility: <code>for</code>/<code>id</code>, <code>aria-describedby</code> and <code>aria-invalid</code>.")
    + ul("Help text appears before the error; both can show at once.", "Only optional fields are marked, with <i>(optional)</i> in subtle text.", "The counter is last and right-aligned."),
    anatomy=anatomy(w(field("an-t", "Title", help="Brand, model and colour.", error="Title must be 5 to 80 characters", counter="3 / 80", value="AM9"), "20rem"),
                    [("4%", "4%"), ("50%", "26%"), ("4%", "48%"), ("4%", "64%"), ("92%", "84%")],
                    [("Label", "<code>--text-label</code>, <code>--color-fg-default</code>."), ("Control", "Any input; carries <code>aria-describedby</code> and <code>aria-invalid</code>."),
                     ("Help", "<code>--text-body-sm</code>, muted."), ("Error", "<code>--text-body-sm</code>, <code>--color-danger-fg</code>, with a warning glyph."), ("Counter", "Caption, subtle, right-aligned.")]),
    variants=ex(w(field("v1", "Email", type="email", value="marcus.bell@example.com"), "16rem") + w(field("v2", "Display name", help="3–30 letters, numbers, _ or -. Shown publicly.", value="marcus_12"), "16rem")
                + w(field("v3", "Apartment, suite", optional=True), "16rem") + w(field("v4", "Title", counter="17 / 80", value="Air Max 90, white"), "16rem"),
                "Plain · with help · optional · with counter."),
    sizes=NA("The wrapper follows its control's size; spacing between parts is fixed at --space-1."),
    states=matrix(["Default", "Invalid", "Read-only", "Disabled"], [("Field", [
        w(field("s1", "Email", value="marcus.bell@example.com"), "13rem"), w(field("s2", "Email", value="marcus.bell@", error="Enter an email like name@example.com"), "13rem"),
        w(field("s3", "Email", value="marcus.bell@example.com", attrs="readonly"), "13rem"), w(field("s4", "Email", value="marcus.bell@example.com", attrs="disabled"), "13rem")])], first="Wrapper")
    + "<h3>Both themes</h3>" + both(lambda x: field(f"t{x}", "Display name", help="Shown publicly.", error="That display name is taken", value="marcus_12")),
    responsive=ul("Fields fill their column; in <code>.form-row</code> two fields sit side by side from 640px.", "Error and help text wrap; never truncate them."),
    theming=p("Help reads <code>--color-fg-muted</code>, errors <code>--color-danger-fg</code>, the optional marker and counter <code>--color-fg-subtle</code>. All pass 4.5:1 on canvas, surface and raised surfaces in both themes."),
    accessibility=a11y(
        pattern="<code>&lt;label for&gt;</code> plus <code>aria-describedby</code> listing help then error ids; <code>aria-invalid=\"true\"</code> on the control when the error shows. Choice fields use <code>&lt;fieldset&gt;</code>/<code>&lt;legend&gt;</code> instead of a label.",
        keyboard="The wrapper adds no keyboard behaviour; see the control's page.",
        focus="On submit with errors, focus goes to the error summary, whose links move focus to each field.",
        labelling="Errors say what to do, are shown under the field and in the summary, and are announced via the summary's <code>role=\"alert\"</code>.",
        contrast=[("Help on page", "--color-fg-muted", "--color-bg-canvas", 4.5), ("Error on page", "--color-danger-fg", "--color-bg-canvas", 4.5), ("Error in dialog", "--color-danger-fg", "--color-bg-surface-raised", 4.5), ("Optional marker", "--color-fg-subtle", "--color-bg-canvas", 4.5)],
        motion="None.", touch="Labels are clickable and focus their control."),
    content=ul("Error formula: what to do, not what went wrong: <i>Enter a price from $1.00 to $5,000.00</i>.", "Mark optional fields, not required ones.", "Help text is one sentence; rules belong there, not in the error alone."),
    do_dont=dodont([("do", w(field("dd1", "Price", error="Enter a price from $1.00 to $5,000.00", value="0"), "16rem"), "Say how to fix it, with the limits."),
                    ("dont", w(field("dd2", "Price", error="Invalid input", value="0"), "16rem"), "A generic error."),
                    ("do", w(field("dd3", "Apartment, suite", optional=True), "16rem"), "Mark the optional field."),
                    ("dont", w(field("dd4", "Email *", value=""), "16rem"), "Asterisks on every required field.")]),
    tokens=token_table([("Label", "--text-label / --color-fg-default"), ("Help", "--color-fg-muted"), ("Error", "--color-danger-fg"), ("Optional / counter", "--color-fg-subtle"), ("Gap between parts", "--space-1")]),
    code=pre("""
<div class="field">
  <label class="field__label" for="title">Title</label>
  <input class="input" id="title" aria-describedby="title-help title-error" aria-invalid="true">
  <span class="field__help" id="title-help">Brand, model and colour.</span>
  <span class="field__error" id="title-error">Title must be 5 to 80 characters</span>
  <span class="field__counter">3 / 80</span>
</div>""")
    + classes([("<code>.field</code>", "Vertical stack with <code>--space-1</code> gaps."), ("<code>.field__label</code>", "Label; holds <code>.optional</code>."), ("<code>.field__help</code>", "Help text."),
               ("<code>.field__error</code>", "Error with leading glyph."), ("<code>.field__counter</code>", "Counter.")]),
    sources=sources([("pages/register/default", "help text"), ("pages/register/invalid", "errors"), ("pages/edit-profile/default", "optional fields and counter"), ("pages/checkout/invalid", "address errors")]),
)

# ===========================================================================
# Form layout
# ===========================================================================


def mini_form(sfx: str, *, errors: bool = False, busy: bool = False) -> str:
    ro = " readonly" if busy else ""
    top = summary([(f"{sfx}-title", "Title must be 5 to 80 characters"), (f"{sfx}-price", "Enter a price from $1.00 to $5,000.00")], sid=f"{sfx}-summary") if errors else ""
    title = field(f"{sfx}-title", "Title", value="AM9" if errors else "Air Max 90, white", error="Title must be 5 to 80 characters" if errors else None, counter=("3" if errors else "17") + " / 80", attrs=ro.strip())
    pr = field(f"{sfx}-price", "Price", f'<div class="input-group"><span class="addon">$</span><input class="input" id="{sfx}-price" inputmode="decimal" value="{"0" if errors else "85.00"}"{{db}}{ro}></div>',
               error="Enter a price from $1.00 to $5,000.00" if errors else None)
    ship = field(f"{sfx}-ship", "Shipping", f'<div class="input-group"><span class="addon">$</span><input class="input" id="{sfx}-ship" inputmode="decimal" value="9.00"{{db}}{ro}></div>')
    busy_a = ' aria-busy="true"' if busy else ""
    return (f'<form class="stack" novalidate>{top}<section class="form-section" aria-labelledby="{sfx}-h"><h2 id="{sfx}-h">Item</h2>{title}<div class="form-row">{pr}{ship}</div></section>'
            f'<div class="form-actions form-actions--split">{btn("Save draft")}{btn("List item", "primary", attrs="type=\"submit\"" + busy_a)}</div></form>')


component(
    "form-layout", "Form layout", "Inputs",
    lead="How fields are arranged into a form: titled sections, two-up rows, the error summary at the top and an actions bar at the end that can stick to the bottom.",
    pills=["<code>.form-section</code> · <code>.form-row</code> · <code>.form-actions</code>"],
    summary_variants="single column, sections, two-column row, actions end / start / split / sticky, error summary",
    summary_states="default, invalid (summary), submitting, success",
    overview=p(f"Forms are one column, capped at 44rem (<code>.page--form</code>) or 24rem on auth screens. Group long forms into <code>.form-section</code>s with an h2; pair short related fields in a <code>.form-row</code>. See the {patt('forms')} pattern for validation timing and submit behaviour.")
    + ul("<b>Error summary</b> (<code>.form-summary</code>): an alert at the top listing every error as a link to its field; receives focus on a failed submit.",
         "<b>Actions</b> (<code>.form-actions</code>): end-aligned by default; <code>--split</code> puts a secondary action at the start (<i>Save draft</i> · <i>List item</i>); <code>--start</code> for settings pages; <code>--sticky</code> keeps them on screen in long forms."),
    anatomy=anatomy(w(mini_form("an"), "26rem"), [("4%", "6%"), ("4%", "40%"), ("4%", "60%"), ("70%", "90%")],
                    [("Section heading", "<code>--text-h4</code>; sections separated by a 1px rule and <code>--space-10</code>."), ("Field", "Full width; <code>--space-6</code> between fields."),
                     ("Form row", "Two fields side by side from 640px."), ("Actions", "Primary last; split, sticky or start-aligned variants.")]),
    variants=ex(w(mini_form("v1"), "30rem"), "Sections, a two-up row and split sticky-ready actions (sell form).")
    + ex(w(summary([("v1-title", "Title must be 5 to 80 characters"), ("v1-price", "Enter a price from $1.00 to $5,000.00")], sid="v2-summary"), "30rem"), "Error summary.")
    + ex(w('<div class="form-actions form-actions--start">' + btn("Save", "primary") + "</div>", "30rem"), "Start-aligned actions (settings)."),
    sizes=p("Width, not height, varies: <code>.auth-card</code> 24rem for sign-in and register, <code>.page--narrow</code> 40rem, <code>.page--form</code> 44rem for the sell form and profile.")
    + table(["Container", "Max width", "Used by"], [["<code>.auth-card</code>", "24rem", "Sign in, Join, password reset"], ["<code>.page--narrow</code>", "40rem", "Legal and confirmation pages"], ["<code>.page--form</code>", "44rem", "Sell, edit listing, edit profile, emails"]]),
    states=matrix(["Default", "Invalid", "Submitting"], [("Form", [w(mini_form("s1"), "18rem"), w(mini_form("s2", errors=True), "18rem"), w(mini_form("s3", busy=True), "18rem")])], first="Layout")
    + ul("<b>Invalid</b>: summary first, focus moves to it; each field shows its own error.", "<b>Submitting</b>: the pressed button is busy, fields become read-only, nothing else moves.",
         "<b>Success</b>: navigate to the result (the new listing) or show a success " + comp("alert") + " above the form for in-place saves (<i>Profile saved</i>).")
    + "<h3>Both themes</h3>" + both(lambda x: mini_form(f"t{x}", errors=True)),
    responsive=ul("One column below 640px; <code>.form-row</code> splits into two columns from 640px.", "Sticky actions (<code>--sticky</code>) sit at the bottom of the viewport on long forms, with a top rule and canvas background.",
                  "Below 640px, split actions keep their order; primary buttons may become block in auth forms (<code>.btn--block</code>)."),
    theming=p("Section rules and the sticky bar edge use <code>--color-border-default</code>; the sticky bar background is <code>--color-bg-canvas</code> so content scrolls under it. The summary uses alert danger tokens with a <code>--border-width-heavy</code> leading edge."),
    accessibility=a11y(
        pattern="A <code>&lt;form novalidate&gt;</code> with custom messages; sections are <code>&lt;section aria-labelledby&gt;</code>; the summary is <code>role=\"alert\"</code> with <code>tabindex=\"-1\"</code> and receives focus after a failed submit; its links target field ids.",
        keyboard=[(kbd("Tab"), "Fields in visual order, then actions."), (kbd("Enter"), "In a text field, submits."), ("Summary link + " + kbd("Enter"), "Moves focus to the field with the error.")],
        focus="Never move focus while the member types; only on submit (to the summary) or on success (to the result heading).",
        labelling="The summary title says what to do: <i>Fix these to continue</i>; errors read the same in the summary and under the field.",
        contrast=[("Summary text", "--color-danger-fg", "--color-danger-bg", 4.5), ("Summary edge on page", "--color-danger-solid", "--color-bg-canvas", 3), ("Section heading", "--color-fg-default", "--color-bg-canvas", 4.5)],
        motion="None; submit states rely on the button's spinner.", touch="Actions are 40–48px tall with 12px between."),
    content=ul("Section titles are nouns: <i>Photos</i>, <i>Item</i>, <i>Price and shipping</i>.", "Primary action names the outcome: <i>List item</i>, <i>Save profile</i>, <i>Join 12L</i>.", "The summary lists errors in field order."),
    do_dont=dodont([("do", w(summary([("v1-title", "Title must be 5 to 80 characters")], sid="dd-s1"), "18rem"), "List errors as links at the top and focus the summary."),
                    ("dont", w('<div class="alert alert--danger" role="alert">' + ic("x-circle") + '<div class="alert__body"><div class="alert__title">There were errors</div></div></div>', "18rem"), "A summary that does not say which fields."),
                    ("do", '<div class="form-actions form-actions--split" style="width: 100%;">' + btn("Save draft") + btn("List item", "primary") + "</div>", "Secondary at the start, primary at the end."),
                    ("dont", '<div class="form-actions" style="width: 100%;">' + btn("List item", "primary") + btn("Save draft") + "</div>", "Primary first, secondary last; the order flips between forms.")]),
    tokens=token_table([("Section rule", "--color-border-default"), ("Section padding", "--space-10"), ("Field gap", "--space-6"), ("Row gap", "--space-6"), ("Actions gap", "--space-3"),
                        ("Sticky bar background", "--color-bg-canvas"), ("Sticky layer", "--z-sticky"), ("Summary edge", "--border-width-heavy / --color-danger-solid")]),
    code=pre("""
<form novalidate>
  <div class="alert alert--danger form-summary" role="alert" tabindex="-1" id="error-summary">…<ul><li><a href="#title">Title must be 5 to 80 characters</a></li></ul></div>
  <section class="form-section" aria-labelledby="s-item"><h2 id="s-item">Item</h2>
    <div class="field">…</div>
    <div class="form-row"><div class="field">…</div><div class="field">…</div></div>
  </section>
  <div class="form-actions form-actions--sticky form-actions--split">
    <button class="btn" type="button">Save draft</button>
    <button class="btn btn--primary" type="submit">List item</button>
  </div>
</form>""")
    + classes([("<code>.form-section</code>", "Titled group with top rule."), ("<code>.form-row</code>", "Two columns from 640px."), ("<code>.form-actions</code>", "End-aligned actions."),
               ("<code>--split</code> <code>--start</code> <code>--sticky</code>", "Action variants."), ("<code>.form-summary</code>", "Error summary alert."), ("<code>.page--form</code> <code>.auth-card</code>", "Width containers.")]),
    sources=sources([("pages/sell/default", "sections, rows, sticky split actions"), ("pages/sell/invalid", "error summary"), ("pages/sell/submitting", "submitting"), ("pages/notification-settings/default", "start-aligned save"), ("pages/edit-profile/success", "in-place success")],
                    "the summary list and start-aligned actions were styled inline in the mocks; the system adds <code>.form-summary ul</code> and <code>.form-actions--start</code>."),
)
drift("pages/sell/invalid", "Error summary list styled inline (margin: 0; padding-left: var(--space-5)).", "Added .form-summary ul rule.")
drift("pages/notification-settings/default", "Start-aligned form actions use inline justify-content.", "Added .form-actions--start.")
