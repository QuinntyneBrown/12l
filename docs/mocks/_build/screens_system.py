"""Moderation, administration, error pages, legal pages, cookies and system notices
(L1-012, L1-014, L1-018, L2-044 to L2-047, L2-056, L2-068)."""
from mk import *

# ---------------------------------------------------------------------------
# Shared pieces
# ---------------------------------------------------------------------------
STATIC_NA = {"loading": "Static content ships with the app; nothing is fetched.",
             "empty": "The page always has content.",
             "error": "Static content cannot fail to load once the app is served."}


def admin_page(main: str, tab: str = "", notes: str = "") -> Page:
    return Page(main=main, shell="admin", admin_tab=tab, footer=False, notes=notes)


def head(title: str, sub: str = "", actions: str = "", crumb: tuple[str, str] | None = None) -> str:
    c = (f'<nav aria-label="Breadcrumb"><ol class="breadcrumb"><li><a href="{crumb[1]}">{crumb[0]}</a></li>'
         f'<li aria-current="page">{title}</li></ol></nav>') if crumb else ""
    s = f'<p class="subtitle">{sub}</p>' if sub else ""
    return f'<div class="page-header"><div class="stack stack--sm">{c}<h1>{title}</h1>{s}</div>{actions}</div>'


def center(code: str, title: str, text: str, actions: str, ref: str = "", icon: str | None = None) -> str:
    big = f'<span class="code" aria-hidden="true">{code}</span>' if code else ""
    i = f'<div class="empty__icon">{ic(icon, "icon icon--lg")}</div>' if icon else ""
    r = f'<span class="ref">{ref}</span>' if ref else ""
    return f'<div class="center-state">{big}{i}<h1>{title}</h1><p class="text-muted">{text}</p>{r}<div class="actions">{actions}</div></div>'


def skel_rows(n: int = 4) -> str:
    row = ('<li><div class="item-row" style="padding-block: var(--space-5);" aria-hidden="true"><span class="skeleton skeleton--rect" style="width: 3.5rem; height: 3.5rem;"></span>'
           '<div class="item-row__body"><span class="skeleton skeleton--text" style="width: 45%;"></span><span class="skeleton skeleton--text" style="width: 25%;"></span></div></div></li>')
    return f'<ul class="queue" role="list" aria-busy="true" aria-label="Loading">{row * n}</ul>'


def skel_detail() -> str:
    return ('<div class="split" aria-busy="true" aria-label="Loading"><div class="stack stack--lg"><span class="skeleton skeleton--title" style="width: 60%;"></span>'
            '<span class="skeleton skeleton--rect" style="height: 10rem;"></span><div><span class="skeleton skeleton--text"></span><span class="skeleton skeleton--text"></span></div></div>'
            '<div class="panel panel--sunken stack"><span class="skeleton skeleton--text" style="width: 40%;"></span><span class="skeleton skeleton--rect" style="height: 3rem;"></span></div></div>')


def load_error(what: str, ref: str) -> str:
    return empty("refresh", f"Couldn’t load {what}", f'Something went wrong on our side. <span class="ref">Ref {ref}</span>',
                 btn("Try again", "primary", icon="refresh"), cls="empty--error")


# ---------------------------------------------------------------------------
# Moderation queue
# ---------------------------------------------------------------------------
QUEUE = [
    # kind, key/handle, title line, reason, count, age, hidden
    ("report", "bedale", "Wrong size", 3, "2 days", True),
    ("problem", "better-sweater", "Not as described · Order 12L-48140", 1, "Yesterday", False),
    ("report", "nb-990", "Counterfeit", 1, "Yesterday", False),
    ("member", "jaybird", "Misleading descriptions", 1, "5 hours", False),
]


def queue_item(kind, key, reason, count, age, hidden) -> str:
    href = P("problem-detail") if kind == "problem" else P("member-admin") if kind == "member" else P("report-detail", "hidden" if hidden else "default")
    if kind == "member":
        row = (f'<div class="item-row">{avatar(key)}<div class="item-row__body"><span class="item-row__title">{key}</span>'
               f'<span class="item-row__meta">Member · {reason}</span></div></div>')
    else:
        label = "Order problem" if kind == "problem" else "Listing"
        row = item_row(key, f"{label} · {reason}")
    tag = '<span class="badge badge--warning">Hidden</span>' if hidden else ""
    cnt = f'<span class="pill-count" aria-label="{count} reporter{"s" if count > 1 else ""}">{count}</span>' if kind != "problem" else '<span class="badge badge--info">Payout held</span>'
    return (f'<li><a href="{href}"><div style="flex: 1 1 16rem; min-width: 0;">{row}</div>'
            f'<div class="cluster" style="gap: var(--space-3);">{tag}{cnt}<span class="text-sm text-muted" style="min-width: 4.5rem; text-align: right;">{age}</span></div></a></li>')


q = screen("moderation-queue", "page", "Moderation queue", route="/admin/queue", reqs=["L2-045", "L2-036", "L2-044", "L2-010"])


@q.state("default", "Open reports and order problems, oldest first, with reason and reporter count.")
def _():
    items = "".join(queue_item(*x) for x in QUEUE)
    main = head("Queue", "4 open · oldest first") + f'<ul class="queue" role="list">{items}</ul>'
    return admin_page(main, "queue", note("A listing reported by 3 different members is hidden from the catalog until reviewed.", "top: 6rem; right: 1rem;"))


@q.state("loading", "Queue rows as skeletons while the first request is in flight.")
def _():
    return admin_page(head("Queue", '<span class="skeleton skeleton--text" style="width: 8rem; display: inline-block;"></span>') + skel_rows(), "queue")


@q.state("empty", "Nothing waiting for review.")
def _():
    return admin_page(head("Queue") + empty("check-circle", "Queue clear", "New reports and order problems land here.",
                                            btn("View audit log", href=P("audit-log"))), "queue")


@q.state("error", "The queue failed to load: retry with a reference code.")
def _():
    return admin_page(head("Queue") + load_error("the queue", "c41d-0e7a"), "queue")


@q.state("forbidden", "A member without the Administrator role opens the queue (HTTP 403).")
def _():
    return Page(main=center("4<em>0</em>3", "Admins only", "This area is for the 12L moderation team.", btn("Back to shop", "primary", P("catalog"))))


# ---------------------------------------------------------------------------
# Report detail
# ---------------------------------------------------------------------------
REPORTERS = [("tall_tom", "Wrong size", "Label inside says M, not L."),
             ("marcus_12", "Wrong size", "Collar tag reads Medium."),
             ("jaybird", "Wrong size", "")]


def report_main(state: str) -> str:
    it = ITEMS["bedale"]
    reps = "".join(
        f'<li class="review"><div class="review__head">{avatar(h, "avatar--sm")}<span class="text-sm"><b>{h}</b> · {r}</span></div>'
        + (f'<p class="text-sm">{esc(t)}</p>' if t else '<p class="text-sm text-muted">No note</p>') + "</li>" for h, r, t in REPORTERS)
    if state == "resolved":
        top = alert("success", "Listing removed", "By Ana Ruiz, today 10:42 ET. vintage_lou was emailed the reason.")
        action = ""
    else:
        top = alert("warning", "Hidden from the catalog", "3 members reported it. It stays hidden until you decide.", icon="eye-off") if state == "hidden" else ""
        action = btn("Resolve report", "primary", D("resolve-report"))
    side = (f'<aside class="panel panel--sunken stack"><span class="eyebrow">Listing</span>{item_row("bedale", f"{esc(it["brand"])} · {money(it["price"])}")}'
            f'<dl class="facts"><dt>Status</dt><dd>{status("Removed" if state == "resolved" else "Reserved")}</dd><dt>ID</dt><dd class="num">{it["id"]}</dd>'
            f'<dt>Seller</dt><dd><a href="{P("member-admin")}">vintage_lou</a></dd></dl>{action}</aside>')
    body = f'<div class="stack stack--lg">{top}<section><div class="section-head"><h2>3 reports</h2></div><ul class="list" role="list">{reps}</ul></section></div>'
    return head("Report R-3318", "Wrong size · opened 2 days ago", crumb=("Queue", P("moderation-queue"))) + f'<div class="split">{body}{side}</div>'


r = screen("report-detail", "page", "Report detail", route="/admin/reports/{id}", reqs=["L2-044", "L2-045", "L2-047"],
           na={"empty": "A report always has a reported listing or member and at least one reporter."})


@r.state("default", "A listing report: who reported it and why, with one action to resolve.")
def _():
    return admin_page(report_main("default"), "queue")


@r.state("hidden", "Third report hid the listing from the catalog pending review.")
def _():
    return admin_page(report_main("hidden"), "queue")


@r.state("resolved", "Closed report: the decision, who made it and when.")
def _():
    return admin_page(report_main("resolved"), "queue")


@r.state("loading", "Report detail skeleton.")
def _():
    return admin_page('<h1 class="visually-hidden">Loading report</h1><div style="margin-top: var(--space-10);">' + skel_detail() + "</div>", "queue")


@r.state("error", "The report failed to load.")
def _():
    return admin_page(head("Report R-3318", crumb=("Queue", P("moderation-queue"))) + load_error("this report", "a9f2-77b1"), "queue")


# ---------------------------------------------------------------------------
# Problem detail
# ---------------------------------------------------------------------------
def problem_main(resolved: bool) -> str:
    o = ORDERS["12L-48140"]
    photos = '<ul class="uploader" role="list">' + "".join(
        f'<li>{photo("better-sweater", tag=False, alt=f"Buyer photo {i} of the fleece", tone=t)}</li>' for i, t in [(1, 1), (2, 3)]) + "</ul>"
    claim = (f'<section class="stack"><div class="review__head">{avatar("marcus_12", "avatar--sm")}<span class="text-sm"><b>marcus_12</b> · buyer · Sun 25 Oct</span></div>'
             '<p>Pilling all over the front and a small hole by the left cuff. Listing said excellent.</p>' + photos + "</section>")
    reply = (f'<section class="stack"><div class="review__head">{avatar("vintage_lou", "avatar--sm")}<span class="text-sm"><b>vintage_lou</b> · seller · Sun 25 Oct</span></div>'
             '<p>It left here without the hole. Happy to take it back.</p></section>')
    if resolved:
        top = alert("success", "Refunded in full", f"{money(o['total'])} back to the buyer. No payout. Today 11:05 ET.")
        action = ""
    else:
        top = ""
        action = btn("Resolve", "primary", D("resolve-problem"))
    side = (f'<aside class="panel panel--sunken stack"><span class="eyebrow">Order 12L-48140</span>{item_row("better-sweater")}'
            f'<dl class="facts"><dt>Status</dt><dd>{status("Refunded" if resolved else "Delivered")}</dd><dt>Total</dt><dd class="num">{money(o["total"])}</dd>'
            f'<dt>Delivered</dt><dd>{o["delivered"]}</dd><dt>Payout</dt><dd>{"Not paid" if resolved else "Held"}</dd></dl>{action}</aside>')
    body = f'<div class="stack stack--lg">{top}{claim}<hr class="divider">{reply}</div>'
    return head("Not as described", "Order problem P-0912 · opened yesterday", crumb=("Queue", P("moderation-queue"))) + f'<div class="split">{body}{side}</div>'


pr = screen("problem-detail", "page", "Problem detail", route="/admin/problems/{id}", reqs=["L2-036", "L2-045", "L2-047"],
            na={"empty": "A problem always has a buyer claim and an order."})


@pr.state("default", "Buyer claim with photos, seller response, payout held; one action to resolve.")
def _():
    return admin_page(problem_main(False), "queue")


@pr.state("resolved", "Resolved in the buyer's favour: order refunded, no payout.")
def _():
    return admin_page(problem_main(True), "queue")


@pr.state("loading", "Problem detail skeleton.")
def _():
    return admin_page('<h1 class="visually-hidden">Loading problem</h1><div style="margin-top: var(--space-10);">' + skel_detail() + "</div>", "queue")


@pr.state("error", "The problem failed to load.")
def _():
    return admin_page(head("Order problem", crumb=("Queue", P("moderation-queue"))) + load_error("this problem", "5d10-be3c"), "queue")


# ---------------------------------------------------------------------------
# Member admin
# ---------------------------------------------------------------------------
def member_main(suspended: bool) -> str:
    p = PEOPLE["vintage_lou"]
    top = alert("danger", "Suspended", "Since today 11:20 ET by Ana Ruiz. Reason: repeated wrong-size listings.", role="status") if suspended else ""
    act = btn("Reinstate", "primary", D("suspend-member", "reinstate")) if suspended else btn("Suspend member", "danger", D("suspend-member"))
    stats = (f'<div class="stats"><div class="stat"><span class="stat__label">Rating</span><span class="stat__value">{p["rating"]}</span></div>'
             f'<div class="stat"><span class="stat__label">Sales</span><span class="stat__value">{p["sales"]}</span></div>'
             f'<div class="stat"><span class="stat__label">Active listings</span><span class="stat__value">{0 if suspended else 4}</span></div>'
             f'<div class="stat"><span class="stat__label">Open reports</span><span class="stat__value">1</span></div></div>')
    head_html = (f'<div class="profile-head">{avatar("vintage_lou", "avatar--xl")}<div class="profile-head__body"><h1>vintage_lou</h1>'
                 f'<span class="text-muted">{p["city"]} · member since {p["since"]}</span></div>{act}</div>')
    hist = ('<section class="section"><div class="section-head"><h2>History</h2></div><ul class="list" role="list">'
            '<li class="list__item"><div class="list__body"><div class="list__title">Report R-3318 · wrong size</div><div class="list__meta">Bedale waxed jacket · 2 days ago</div></div>'
            f'{status("Open")}</li><li class="list__item"><div class="list__body"><div class="list__title">Problem P-0912 · not as described</div>'
            f'<div class="list__meta">Order 12L-48140 · yesterday</div></div>{status("Open")}</li></ul></section>')
    hidden = '<p class="text-sm text-muted">Active listings are hidden while suspended. Open orders continue.</p>' if suspended else ""
    return (f'<nav aria-label="Breadcrumb" style="margin-top: var(--space-6);"><ol class="breadcrumb"><li><a href="{P("moderation-queue")}">Queue</a></li>'
            f'<li aria-current="page">vintage_lou</li></ol></nav>{head_html}<div class="stack stack--lg">{top}{stats}{hidden}</div>{hist}')


ma = screen("member-admin", "page", "Member admin", route="/admin/members/{name}", reqs=["L2-046", "L2-047"],
            na={"empty": "Every member record has a profile and history."})


@ma.state("default", "Member summary for moderation with one action: suspend.")
def _():
    return admin_page(member_main(False), "queue")


@ma.state("suspended", "Suspended member: reason, listings hidden, reinstate.")
def _():
    return admin_page(member_main(True), "queue")


@ma.state("loading", "Member summary skeleton.")
def _():
    sk = ('<div class="profile-head" aria-busy="true" aria-label="Loading member"><span class="skeleton skeleton--rect" style="width: 6rem; height: 6rem;"></span>'
          '<div class="profile-head__body"><span class="skeleton skeleton--title"></span><span class="skeleton skeleton--text" style="width: 30%;"></span></div></div>')
    return admin_page('<h1 class="visually-hidden">Loading member</h1>' + sk + skel_rows(2), "queue")


@ma.state("error", "The member failed to load.")
def _():
    return admin_page(head("vintage_lou", crumb=("Queue", P("moderation-queue"))) + load_error("this member", "e2c7-1f08"), "queue")


# ---------------------------------------------------------------------------
# Audit log
# ---------------------------------------------------------------------------
AUDIT = [
    ("Today 11:20", "Ana Ruiz", "Member suspended", "vintage_lou", "Repeated wrong-size listings"),
    ("Today 11:05", "Ana Ruiz", "Problem resolved: refund", "P-0912", "Hole by the left cuff, not disclosed"),
    ("Today 10:42", "Ana Ruiz", "Listing removed", "L-20802", "Label shows men's M"),
    ("Sat 24 Oct 16:18", "Ana Ruiz", "Report dismissed", "R-3290", "Photos match the listing"),
    ("Fri 23 Oct 09:51", "Ana Ruiz", "Member reinstated", "kicks_12", "Appeal accepted"),
]


def audit_table(rows) -> str:
    body = "".join(f'<tr><td class="num" style="white-space: nowrap;">{t}</td><td>{a}</td><td>{act}</td><td class="num">{tgt}</td><td>{esc(why)}</td></tr>'
                   for t, a, act, tgt, why in rows)
    return ('<div class="table-wrap"><table class="table"><caption class="visually-hidden">Administrator actions, newest first</caption>'
            '<thead><tr><th scope="col">Time (ET)</th><th scope="col">Administrator</th><th scope="col">Action</th><th scope="col">Target</th><th scope="col">Reason</th></tr></thead>'
            f'<tbody>{body}</tbody></table></div>')


def audit_tools(q: str = "", act: str = "All actions") -> str:
    opts = "".join(f"<option{' selected' if o == act else ''}>{o}</option>" for o in ["All actions", "Listing removed", "Member suspended", "Member reinstated", "Report dismissed", "Problem resolved"])
    return (f'<div class="toolbar"><form class="search" role="search" style="flex: 1 1 16rem; max-width: 22rem;"><label class="visually-hidden" for="audit-q">Search by target ID</label>'
            f'{ic("search")}<input class="input" id="audit-q" type="search" placeholder="Target ID" value="{q}"></form>'
            f'<label class="sort"><span class="text-sm text-muted">Action</span><select class="select input--sm">{opts}</select></label></div>')


al = screen("audit-log", "page", "Audit log", route="/admin/audit", reqs=["L2-047"])


@al.state("default", "Append-only log of administrator actions, newest first.")
def _():
    pg = admin_page(head("Audit log", "Read-only · kept for 2 years") + audit_tools() + audit_table(AUDIT), "audit")
    pg.notes = note("No edit or delete controls exist; entries are append-only.", "top: 6rem; right: 1rem;")
    return pg


@al.state("loading", "Table skeleton while the log loads.")
def _():
    rows = "".join('<tr>' + "".join('<td><span class="skeleton skeleton--text"></span></td>' for _ in range(5)) + "</tr>" for _ in range(5))
    t = ('<div class="table-wrap" aria-busy="true"><table class="table"><caption class="visually-hidden">Loading audit log</caption>'
         '<thead><tr><th scope="col">Time (ET)</th><th scope="col">Administrator</th><th scope="col">Action</th><th scope="col">Target</th><th scope="col">Reason</th></tr></thead>'
         f"<tbody>{rows}</tbody></table></div>")
    return admin_page(head("Audit log", "Read-only · kept for 2 years") + audit_tools() + t, "audit")


@al.state("empty", "No administrator actions recorded yet.")
def _():
    return admin_page(head("Audit log") + empty("list", "No actions yet", "Every moderation decision is recorded here."), "audit")


@al.state("error", "The log failed to load.")
def _():
    return admin_page(head("Audit log") + load_error("the audit log", "91ab-34d0"), "audit")


@al.state("no-results", "A target search matched nothing; the filter stays visible and clearable.")
def _():
    res = empty("search", "No entries for L-19999", "Check the ID or clear the search.", btn("Clear search", "primary"), cls="empty--compact")
    return admin_page(head("Audit log") + audit_tools("L-19999") + res, "audit")


# ---------------------------------------------------------------------------
# Admin second factor
# ---------------------------------------------------------------------------
def verify_form(error: str | None = None, busy: bool = False, value: str = "") -> str:
    ctrl = (f'<input class="input input--lg otp" id="totp" name="totp" inputmode="numeric" autocomplete="one-time-code" maxlength="6" value="{value}"'
            f'{{db}}{" readonly" if busy else ""} autofocus>')
    f = field("totp", "6-digit code", ctrl, help="From your authenticator app.", error=error)
    b = btn("Verifying", "primary block lg", attrs='type="submit" aria-busy="true"') if busy else btn("Verify", "primary block lg", attrs='type="submit"')
    return f'<form class="stack stack--lg">{f}{b}</form>'


av = screen("admin-verify", "page", "Admin verification", route="/admin/verify", reqs=["L2-047", "L2-006"],
            na={"loading": "The form renders without fetching data.", "empty": "A single-field form has no collection."})


def verify_head() -> str:
    return '<div class="stack stack--sm"><span class="topbar__admin" style="align-self: flex-start;">Admin</span><h1>Enter your code</h1></div>'


@av.state("default", "TOTP second factor required for administrators after password sign-in.")
def _():
    return Page(main=verify_head() + verify_form(), shell="auth")


@av.state("invalid", "Wrong or expired code: inline error, field keeps focus.")
def _():
    return Page(main=verify_head() + verify_form("That code didn’t work. Codes change every 30 seconds.", value="482913"), shell="auth")


@av.state("submitting", "Code sent: button busy, field read-only.")
def _():
    return Page(main=verify_head() + verify_form(busy=True, value="604218"), shell="auth")


@av.state("error", "Verification service failed: say so and offer retry.")
def _():
    top = alert("danger", "Couldn’t verify right now", 'Try again in a moment. <span class="ref">Ref 0d4f-6a21</span>')
    return Page(main=verify_head() + top + verify_form(value="604218"), shell="auth")


# ---------------------------------------------------------------------------
# Error and status pages
# ---------------------------------------------------------------------------
def simple(sid, title, route, reqs, desc, page_fn, na=None):
    sc = screen(sid, "page", title, route=route, reqs=reqs, na=na or STATIC_NA)
    sc.state("default", desc)(page_fn)
    return sc


simple("not-found", "Not found", "/*", ["L2-068"], "Unknown URL: say so plainly, offer the shop.",
       lambda: Page(main=center("4<em>0</em>4", "Page not found", "The link may be old or mistyped.", btn("Back to shop", "primary", P("catalog")))),
       na={"loading": "Shown after routing; nothing to load.", "empty": "Not a collection.", "error": "This page is itself the error."})

simple("forbidden", "Forbidden", "/403", ["L2-010", "L2-068"], "Signed in but not allowed: who can see this and a way back.",
       lambda: Page(main=center("4<em>0</em>3", "You can’t open this", "It belongs to another member’s account.", btn("Go to your account", "primary", P("account")))),
       na={"loading": "Shown after the API refuses; nothing to load.", "empty": "Not a collection.", "error": "This page is itself the error."})

simple("server-error", "Server error", "/error", ["L2-068"], "Unhandled 500: “Something went wrong”, Try again and the correlation ID.",
       lambda: Page(main=center("5<em>0</em>0", "Something went wrong", "It’s on our side. Your data is safe.",
                                btn("Try again", "primary", icon="refresh") + btn("Back to shop", href=P("catalog")), ref="Ref 3c8e-1d42-a7f0")),
       na={"loading": "Rendered from the error response; nothing to load.", "empty": "Not a collection.", "error": "This page is itself the error."})

simple("offline", "Offline", "(any)", ["L2-068"], "The device lost its connection: “You’re offline”, retry when back.",
       lambda: Page(main=center("", "You’re offline", "Check your connection. We’ll pick up where you left off.", btn("Try again", "primary", icon="refresh"), icon="wifi-off")),
       na={"loading": "Shown from the cached shell without a request.", "empty": "Not a collection.", "error": "This page is itself the error state."})

simple("maintenance", "Maintenance", "(any)", ["L2-066"], "Announced maintenance window with the time we’re back.",
       lambda: Page(main=center("", "Back at 3:00 AM ET", "12L is down for planned maintenance. Orders and payments are safe.",
                                btn("Check status", "primary", icon="refresh"), icon="wrench"), user="guest"),
       na={"loading": "Served as a static page during maintenance.", "empty": "Not a collection.", "error": "This page is itself the outage notice."})


# ---------------------------------------------------------------------------
# Legal and rules
# ---------------------------------------------------------------------------
def doc_page(title: str, sub: str, body: str) -> Page:
    return Page(main=f'<div class="page--narrow">{head(title, sub)}{body}</div>', user="guest")


def rules_body() -> str:
    rows = "".join(f'<tr><th scope="row">{c}</th><td>{", ".join(s)}</td><td>{size_tag(z)}</td></tr>' for c, s, z in CATEGORIES)
    sizes = ('<div class="table-wrap"><table class="table"><caption class="visually-hidden">Accepted categories and sizes</caption>'
             f'<thead><tr><th scope="col">Category</th><th scope="col">Includes</th><th scope="col">Size</th></tr></thead><tbody>{rows}</tbody></table></div>')
    rules = [("Only two sizes", "Men’s US 12 shoes and men’s L clothing. The label must say so."),
             ("18 and over", "One account to buy and sell. No approval step."),
             ("Honest condition", ", ".join(CONDITIONS) + ". Used - Fair needs its flaws described."),
             ("Ship in 5 business days", "Add tracking or the order is cancelled and refunded."),
             ("10% fee", "Taken from item plus shipping when the order completes."),
             ("US only", "Prices in US dollars, shipping within the United States."),
             ("No counterfeits", "Fakes are removed and the seller may be suspended.")]
    lst = "".join(f'<li class="settings-list__body" style="padding-block: var(--space-5); border-bottom: 1px solid var(--color-border-default);">'
                  f'<span class="settings-list__title">{t}</span><span class="settings-list__meta">{d}</span></li>' for t, d in rules)
    return f'<div class="stack stack--lg">{sizes}<ol class="rules-list" role="list">{lst}</ol></div>'


simple("rules", "Marketplace rules", "/rules", ["L2-011", "L2-014", "L2-016", "L2-031", "L2-033", "L2-044"],
       "The rules on one short page: sizes, age, condition, shipping, fee, US only, counterfeits.",
       lambda: doc_page("Marketplace rules", "Short, because it only has to cover two sizes.", rules_body()))


def privacy_body() -> str:
    items = [("What we collect", "Email, password hash, display name, shipping addresses, and orders."),
             ("Never public", "Your email, phone and street address never appear on 12L pages."),
             ("Encrypted", "Shipping addresses are encrypted at rest. Card numbers never reach us."),
             ("Your copy", "Download everything we hold from Settings as a JSON file."),
             ("Erasure", "Close your account and we erase your data within 30 days."),
             ("Cookies", "Only necessary cookies until you accept analytics.")]
    lst = "".join(f'<li class="settings-list__body" style="padding-block: var(--space-5); border-bottom: 1px solid var(--color-border-default);">'
                  f'<span class="settings-list__title">{t}</span><span class="settings-list__meta">{d}</span></li>' for t, d in items)
    return f'<ul class="rules-list" role="list">{lst}</ul><p class="text-sm" style="margin-top: var(--space-8);"><a href="{D("cookie-settings")}">Cookie settings</a></p>'


simple("privacy", "Privacy", "/privacy", ["L2-054", "L2-055", "L2-056", "L2-005"], "What 12L keeps, what stays private, export and erasure.",
       lambda: doc_page("Privacy", "Updated 1 Oct 2026", privacy_body()))


def terms_body() -> str:
    terms = ["You must be 18 or older to hold an account.",
             "List only items you own, in men’s US 12 or men’s L.",
             "Describe condition and flaws honestly; photos must be of the actual item.",
             "Payment goes through our payment provider. Sellers are paid when the order completes.",
             "Buyers can report a problem until 3 days after delivery.",
             "We may remove listings or suspend accounts that break the marketplace rules.",
             "12L operates in the United States only."]
    lst = "".join(f"<li>{t}</li>" for t in terms)
    return (f'<ol class="terms-list">{lst}</ol><p class="text-sm text-muted" style="margin-top: var(--space-8);">See also the '
            f'<a href="{P("rules")}">marketplace rules</a> and <a href="{P("privacy")}">privacy</a>.</p>')


simple("terms", "Terms", "/terms", ["L2-001", "L2-036", "L2-031"], "Terms of service as a short numbered list.",
       lambda: doc_page("Terms of service", "Effective 1 Oct 2026", terms_body()))


# ---------------------------------------------------------------------------
# Dialogs
# ---------------------------------------------------------------------------
def reason_field(error: str | None = None, value: str = "", busy: bool = False) -> str:
    ro = " readonly" if busy else ""
    ctrl = f'<textarea class="textarea" id="reason" name="reason" rows="3"{{db}}{ro}>{esc(value)}</textarea>'
    return field("reason", "Reason", ctrl, help="Sent to the member and kept in the audit log.", error=error)


def report_choices(checked: str = "remove", invalid: bool = False) -> str:
    opts = [("dismiss", "Dismiss report", "The listing returns to the catalog"),
            ("remove", "Remove listing", "The seller is emailed your reason"),
            ("suspend", "Suspend member", "Hides all of vintage_lou’s listings")]
    return '<fieldset><legend>Decision</legend>' + "".join(
        f'<label class="choice"><input type="radio" name="decision"{" checked" if k == checked else ""}><span class="choice__text">{t}<small>{d}</small></span></label>'
        for k, t, d in opts) + "</fieldset>"


def rr_dialog(*, error=None, value="", busy=False, top="", primary=None, title="Resolve report R-3318") -> str:
    prim = primary or (btn("Removing", "primary", attrs='aria-busy="true"') if busy else btn("Remove listing", "primary"))
    cancel = btn("Cancel", attrs="disabled" if busy else "")
    return dialog(title, report_choices() + reason_field(error, value, busy), cancel + prim, top=top)


rr = screen("resolve-report", "dialog", "Resolve report", opens_from="report-detail", reqs=["L2-045", "L2-046", "L2-047"])
REASON = "The label shows men's M. 12L only accepts men's L clothing."


@rr.state("default", "Choose dismiss, remove or suspend and give the reason sent to the member.")
def _():
    return Dialog(bg=("report-detail", "hidden"), html=rr_dialog())


@rr.state("invalid", "No reason given: inline error on the reason field.")
def _():
    return Dialog(bg=("report-detail", "hidden"), html=rr_dialog(error="Add a reason. The member sees it."))


@rr.state("busy", "Decision submitting: confirm busy, inputs read-only, cancel disabled.")
def _():
    return Dialog(bg=("report-detail", "hidden"), html=rr_dialog(value=REASON, busy=True))


@rr.state("order-warning", "The listing is Reserved: removing it cancels the checkout and refunds; confirm explicitly.")
def _():
    top = alert("warning", "This item is in someone’s checkout", "Removing it cancels that order and refunds the buyer in full.")
    return Dialog(bg=("report-detail", "hidden"), html=rr_dialog(value=REASON, top=top, primary=btn("Remove and refund", "danger")))


@rr.state("failed", "The decision failed to save: error at the top, inputs kept, retry.")
def _():
    top = alert("danger", "Couldn’t save the decision", 'Nothing changed. <span class="ref">Ref 6b0c-22e9</span>')
    return Dialog(bg=("report-detail", "hidden"), html=rr_dialog(value=REASON, top=top, primary=btn("Try again", "primary")))


def rp_dialog(error=None, value="", busy=False) -> str:
    o = ORDERS["12L-48140"]
    ch = ('<fieldset><legend>Decision</legend>'
          f'<label class="choice"><input type="radio" name="outcome" checked><span class="choice__text">Refund buyer in full<small>{money(o["total"])} to marcus_12 · no payout</small></span></label>'
          f'<label class="choice"><input type="radio" name="outcome"><span class="choice__text">Release payout to seller<small>Order completes · vintage_lou is paid</small></span></label></fieldset>')
    prim = btn("Refunding", "primary", attrs='aria-busy="true"') if busy else btn("Refund buyer", "primary")
    return dialog("Resolve problem P-0912", ch + reason_field(error, value, busy), btn("Cancel", attrs="disabled" if busy else "") + prim)


rp = screen("resolve-problem", "dialog", "Resolve problem", opens_from="problem-detail", reqs=["L2-036", "L2-045", "L2-047"])


@rp.state("default", "Refund the buyer or release the payout, with a reason.")
def _():
    return Dialog(bg=("problem-detail", "default"), html=rp_dialog())


@rp.state("invalid", "Reason missing.")
def _():
    return Dialog(bg=("problem-detail", "default"), html=rp_dialog(error="Add a reason. Both members see it."))


@rp.state("busy", "Refund in progress: confirm busy.")
def _():
    return Dialog(bg=("problem-detail", "default"), html=rp_dialog(value="Hole by the left cuff wasn't disclosed.", busy=True))


def sm_dialog(error=None, value="", busy=False, reinstate=False) -> str:
    if reinstate:
        body = '<p>Their 4 listings return to the catalog and they can buy and sell again.</p>' + reason_field(value="Appeal accepted.")
        return dialog("Reinstate vintage_lou?", body, btn("Cancel") + btn("Reinstate", "primary"))
    body = ('<p>Their 4 active listings are hidden. They can still sign in, see orders and ship open sales.</p>' + reason_field(error, value, busy))
    prim = btn("Suspending", "danger", attrs='aria-busy="true"') if busy else btn("Suspend", "danger")
    return dialog("Suspend vintage_lou?", body, btn("Cancel", attrs="disabled" if busy else "autofocus") + prim, icon="shield", icon_kind="danger")


sm = screen("suspend-member", "dialog", "Suspend member", opens_from="member-admin", reqs=["L2-046", "L2-047"])


@sm.state("default", "Destructive confirmation naming the member and what changes; Cancel is the default focus.")
def _():
    return Dialog(bg=("member-admin", "default"), html=sm_dialog())


@sm.state("invalid", "Reason missing.")
def _():
    return Dialog(bg=("member-admin", "default"), html=sm_dialog(error="Add a reason. The member is emailed it."))


@sm.state("busy", "Suspension saving.")
def _():
    return Dialog(bg=("member-admin", "default"), html=sm_dialog(value="Repeated wrong-size listings.", busy=True))


@sm.state("reinstate", "Reinstating a suspended member brings their listings back.")
def _():
    return Dialog(bg=("member-admin", "suspended"), html=sm_dialog(reinstate=True))


def cookie_dialog(analytics: bool) -> str:
    body = (f'<label class="switch" style="justify-content: space-between; width: 100%;"><span class="choice__text">Strictly necessary<small>Sign-in and checkout. Always on.</small></span>'
            f'<input type="checkbox" role="switch" checked disabled></label>'
            f'<label class="switch" style="justify-content: space-between; width: 100%;"><span class="choice__text">Analytics<small>Helps us see which pages are slow.</small></span>'
            f'<input type="checkbox" role="switch"{" checked" if analytics else ""} autofocus></label>')
    return dialog("Cookie settings", body, btn("Cancel") + btn("Save", "primary"), size="sm")


cs = screen("cookie-settings", "dialog", "Cookie settings", opens_from="catalog", reqs=["L2-056"],
            na={"busy": "The choice is stored in the browser instantly; no request.", "invalid": "Only switches; nothing can be invalid."})


@cs.state("default", "Strictly necessary always on; analytics off until the visitor opts in.")
def _():
    return Dialog(bg=("catalog", "guest"), html=cookie_dialog(False))


@cs.state("analytics-on", "Analytics accepted; turning it off removes the cookies.")
def _():
    return Dialog(bg=("catalog", "guest"), html=cookie_dialog(True))


# ---------------------------------------------------------------------------
# Notifications
# ---------------------------------------------------------------------------
cc = screen("cookie-consent", "notification", "Cookie consent", opens_from="catalog", reqs=["L2-056"],
            na={"warning": "Consent has nothing to warn about.", "danger": "Choices are stored locally and cannot fail."})


@cc.state("info", "First visit: only necessary cookies are set until the visitor chooses.")
def _():
    html = (f'<section class="consent" aria-labelledby="consent-title"><h2 id="consent-title" style="font: var(--text-h4);">Cookies</h2>'
            f'<p class="text-sm">We use necessary cookies to run 12L. Analytics only if you say yes.</p>'
            f'<div class="consent__actions">{btn("Accept analytics", "primary")}{btn("Necessary only")}</div>'
            f'<a class="text-sm" href="{D("cookie-settings")}">Cookie settings</a></section>')
    return Note(bg=("catalog", "guest"), after=html)


@cc.state("success", "Choice saved: short toast with a way to change it.")
def _():
    return Note(bg=("catalog", "guest"), toasts=toast_region(toast("success", "Cookie choice saved", "Necessary only. Change it any time in the footer.")))


sb = screen("system-banner", "notification", "System notices", opens_from="catalog", reqs=["L2-066", "L2-068"])


@sb.state("info", "Announced maintenance: persistent banner with the window in ET.")
def _():
    return Note(bg=("catalog", "default"), top=banner("info", "Planned maintenance Tue 27 Oct, 2:00–3:00 AM ET.", icon="wrench"))


@sb.state("success", "Connection restored: brief toast.")
def _():
    return Note(bg=("catalog", "default"), toasts=toast_region(toast("success", "Back online")))


@sb.state("warning", "Offline: persistent banner instead of a generic error.")
def _():
    return Note(bg=("catalog", "default"), top=banner("warning", "You’re offline. We’ll retry when you’re back.", dismiss=False, icon="wifi-off"))


@sb.state("danger", "A request failed with 500: error toast with Try again and the correlation ID; never auto-dismisses.")
def _():
    pg = Note(bg=("catalog", "default"), toasts=toast_region(toast("danger", "Something went wrong", "Ref 3c8e-1d42-a7f0", action="Try again")))
    pg.notes = note("Error toasts stay until dismissed.", "bottom: 9rem; right: 1rem;")
    return pg
