"""Page kit for the 12L design-system documentation.

Every page in docs/design-system/ is rendered from the modules in this folder
so the shell, navigation and section order stay identical everywhere:

    comp_*.py        component pages   (component(...) calls)
    foundations.py   foundation pages  (foundation(...) calls)
    patterns.py      pattern pages     (pattern(...) calls)
    build.py         renders everything, splices css/*.css into
                     assets/components.css, writes index.html and README.md

Write section bodies as HTML strings using the helpers below. Every helper
returns a string. Pages sit one folder deep, so links to the mocks are
../../mocks/... and links between pages are ../<folder>/<page>.html.

    from ds import *
    component("button", "Button", "Actions", lead="...", overview=..., ...)
"""
from __future__ import annotations

import html as _html
import sys
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent                      # docs/design-system
MOCKS = ROOT.parent / "mocks"           # docs/mocks
sys.path.insert(0, str(MOCKS / "_build"))

from data import ITEMS, PEOPLE  # noqa: E402  (the mocks' cast and catalog)
from mk import ICONS, LOGO_SVG  # noqa: E402  (the mocks' icon set and logo)

esc = _html.escape
PRODUCT = "12L"
EXTRACTED = "25 Oct 2026"

# ---------------------------------------------------------------------------
# Registries
# ---------------------------------------------------------------------------
COMPONENT_GROUPS = ["Actions", "Inputs", "Navigation", "Containers and overlays", "Data display", "Feedback", "12L brand"]
COMPONENTS: dict[str, "Component"] = {}
FOUNDATIONS: dict[str, "Foundation"] = {}
PATTERNS: dict[str, "Pattern"] = {}
DRIFT: list[tuple[str, str, str]] = []   # (mock or file, issue, resolution) for README
SOURCES_USED: set[str] = set()

COMPONENT_SECTIONS = [("overview", "Overview"), ("anatomy", "Anatomy"), ("variants", "Variants"), ("sizes", "Sizes"),
                      ("states", "States"), ("responsive", "Responsive behaviour"), ("theming", "Theming"),
                      ("accessibility", "Accessibility"), ("content", "Content"), ("do-dont", "Do and don't"),
                      ("tokens", "Tokens"), ("code", "Code"), ("sources", "Sources")]
PATTERN_SECTIONS = [("overview", "Overview"), ("when", "When to use what"), ("structure", "Structure"), ("states", "States"),
                    ("responsive", "Responsive behaviour"), ("accessibility", "Accessibility"), ("content", "Content"),
                    ("do-dont", "Do and don't"), ("sources", "Sources")]


@dataclass
class NA:
    """A section that does not apply: NA("Tooltips have one size.")"""
    reason: str


@dataclass
class Component:
    slug: str
    title: str
    group: str
    lead: str
    sections: dict
    pills: list
    summary: dict          # README row: variants, states, sources


@dataclass
class Foundation:
    slug: str
    title: str
    lead: str
    covers: str
    sections: list          # [(id, title, html)]


@dataclass
class Pattern:
    slug: str
    title: str
    lead: str
    covers: str
    sections: dict


def component(slug, title, group, *, lead, overview, anatomy, variants, sizes, states, responsive, theming,
              accessibility, content, do_dont, tokens, code, sources, pills=(), summary_variants="", summary_states=""):
    """Register a component page. Every section is an HTML string or NA(reason)."""
    if group not in COMPONENT_GROUPS:
        raise ValueError(f"{slug}: unknown group {group}")
    if slug in COMPONENTS:
        raise ValueError(f"duplicate component {slug}")
    secs = dict(overview=overview, anatomy=anatomy, variants=variants, sizes=sizes, states=states, responsive=responsive,
                theming=theming, accessibility=accessibility, content=content, **{"do-dont": do_dont}, tokens=tokens,
                code=code, sources=sources)
    COMPONENTS[slug] = Component(slug, title, group, lead, secs, list(pills),
                                 {"variants": summary_variants, "states": summary_states})
    return COMPONENTS[slug]


def foundation(slug, title, *, lead, covers, sections):
    FOUNDATIONS[slug] = Foundation(slug, title, lead, covers, sections)


def pattern(slug, title, *, lead, covers, overview, when, structure, states, responsive, accessibility, content, do_dont, sources):
    PATTERNS[slug] = Pattern(slug, title, lead, covers, dict(overview=overview, when=when, structure=structure, states=states,
                                                             responsive=responsive, accessibility=accessibility, content=content,
                                                             **{"do-dont": do_dont}, sources=sources))


def drift(mock: str, issue: str, resolution: str) -> None:
    DRIFT.append((mock, issue, resolution))


# ---------------------------------------------------------------------------
# Small product helpers (mirror docs/mocks/_build/mk.py, with paths for pages
# one folder deep inside docs/design-system/)
# ---------------------------------------------------------------------------
MOCK_ASSETS = "../../mocks/assets/"


def ic(name: str, cls: str = "icon", label: str | None = None) -> str:
    aria = f'role="img" aria-label="{esc(label)}"' if label else 'aria-hidden="true"'
    return f'<svg class="{cls}" {aria} viewBox="0 0 24 24">{ICONS[name]}</svg>'


def logo(cls: str = "", href: str = "#") -> str:
    return f'<a class="logo {cls}" href="{href}" aria-label="12L home">{LOGO_SVG}</a>'


def size_of(key: str) -> str:
    return "US 12" if ITEMS[key]["cat"] == "Shoes" else "L"


def size_tag(s: str = "US 12", cls: str = "") -> str:
    num = s.split()[-1]
    pre = s[: -len(num)].strip()
    return f'<span class="size-tag {cls}" aria-label="Size {s}">{pre + " " if pre else ""}<b>{num}</b></span>'


def photo(key: str, cls: str = "", tag: bool = True, stamp: str | None = None, alt: str | None = None) -> str:
    it = ITEMS[key]
    alt = alt if alt is not None else f"{it['brand']} {it['title']}"
    st = f'<span class="photo__stamp{" photo__stamp--sold" if stamp == "Sold" else ""}">{stamp}</span>' if stamp else ""
    tg = size_tag(size_of(key)) if tag else ""
    return (f'<div class="photo photo--{it["tone"]} {cls}"><img src="{MOCK_ASSETS}items/{it["img"]}.svg" alt="{esc(alt)}" width="160" height="160" loading="lazy">'
            f'{st}{tg}</div>')


def price(v: float) -> str:
    return f"${v:,.0f}" if v == int(v) else f"${v:,.2f}"


def listing_card(key: str, stamp: str | None = None, attrs: str = "") -> str:
    it = ITEMS[key]
    stamp = stamp if stamp is not None else (it.get("status") if it.get("status") in ("Reserved", "Sold") else None)
    return (f'<a class="listing-card" href="#"{attrs}>{photo(key, stamp=stamp)}'
            f'<div class="listing-card__meta"><span class="listing-card__brand">{esc(it["brand"])}</span>'
            f'<span class="listing-card__title">{esc(it["title"])}</span>'
            f'<span class="listing-card__foot"><span class="listing-card__condition">{esc(it["cond"])}</span>'
            f'<span class="price">{price(it["price"])}</span></span></div></a>')


def stars(value: float) -> str:
    full = int(round(value))
    return "".join(ic("star", "icon" if i < full else "icon icon--off") for i in range(5))


def rating(value: float | None, count: int = 0) -> str:
    if not count:
        return '<span class="rating text-muted">No reviews yet</span>'
    word = "review" if count == 1 else "reviews"
    return (f'<span class="rating" role="img" aria-label="Rated {value:.1f} out of 5 from {count} {word}"><span class="rating__stars">{stars(value)}</span>'
            f'<span class="rating__value">{value:.1f}</span><span class="text-muted">({count:,} {word})</span></span>')


def btn(label: str, kind: str = "", icon: str | None = None, attrs: str = "", icon_after: str | None = None, href: str | None = None) -> str:
    cls = "btn" + "".join(f" btn--{k}" for k in kind.split()) if kind else "btn"
    inner = (ic(icon) if icon else "") + esc(label) + (ic(icon_after) if icon_after else "")
    if href is not None:
        return f'<a class="{cls}" href="{href}" {attrs}>{inner}</a>'.replace(" >", ">")
    t = "" if "type=" in attrs else 'type="button" '
    return f'<button class="{cls}" {t}{attrs}>{inner}</button>'.replace(" >", ">")


# ---------------------------------------------------------------------------
# Documentation helpers
# ---------------------------------------------------------------------------
def code(src: str) -> str:
    """Escape markup for a <pre><code> block, trimming shared indentation."""
    import textwrap
    return esc(textwrap.dedent(src).strip("\n"))


def pre(src: str) -> str:
    return f"<pre><code>{code(src)}</code></pre>"


def ex(canvas: str, caption: str = "", show_code: bool | str = True, cls: str = "", stack: bool = False) -> str:
    """A live example frame. The HTML shown under it defaults to the canvas itself."""
    klass = "ds-example__canvas" + (" ds-example__canvas--stack" if stack else "") + (f" {cls}" if cls else "")
    cap = f'<div class="ds-example__caption"><span>{caption}</span></div>' if caption else ""
    src = canvas if show_code is True else (show_code or "")
    det = f'<details class="ds-example__code"><summary>HTML</summary><pre><code>{code(pretty(src))}</code></pre></details>' if src else ""
    return f'<div class="ds-example"><div class="{klass}">{canvas}</div>{cap}{det}</div>'


def pretty(src: str) -> str:
    """Put adjacent sibling elements on their own lines in the code view."""
    import re
    return re.sub(r"(</(?:button|a|div|li|label|p|nav|ul|ol|table|figure|header|footer|section)>|<input[^>]*>|<hr[^>]*>)(?=<)", "\\1\n", src)


def stage(html: str, height: str = "28rem", caption: str = "", show_code: bool | str = True, canvas: bool = True) -> str:
    """Frame for overlays (dialogs, drawers, toasts, sheets): fixed children stay inside it."""
    cap = f'<div class="ds-example__caption"><span>{caption}</span></div>' if caption else ""
    src = html if show_code is True else (show_code or "")
    det = f'<details class="ds-example__code"><summary>HTML</summary><pre><code>{code(src)}</code></pre></details>' if src else ""
    return f'<div class="ds-example"><div class="ds-stage{" ds-stage--canvas" if canvas else ""}" style="--stage-height: {height};">{html}</div>{cap}{det}</div>'


def anatomy(figure: str, callouts: list[tuple[str, str]], parts: list[tuple[str, str]]) -> str:
    """callouts: [(left, top)] as CSS lengths; parts: [(name, description)] in the same order."""
    co = "".join(f'<span class="ds-callout" style="left: {l}; top: {t};" aria-hidden="true">{i}</span>' for i, (l, t) in enumerate(callouts, 1))
    li = "".join(f"<li><div><b>{n}</b><small>{d}</small></div></li>" for n, d in parts)
    return f'<div class="ds-anatomy"><figure class="ds-anatomy__figure">{figure}{co}</figure><ol class="ds-anatomy__list">{li}</ol></div>'


def matrix(cols: list[str], rows: list[tuple[str, list[str]]], first: str = "Variant") -> str:
    head = "".join(f'<th scope="col">{c}</th>' for c in [first, *cols])
    body = "".join(f'<tr><th scope="row">{label}</th>' + "".join(f"<td>{c}</td>" for c in cells) + "</tr>" for label, cells in rows)
    return f'<div class="ds-matrix"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def state_matrix(states: list[str], variants: list[tuple[str, object]], first: str = "Variant") -> str:
    """variants: [(label, fn(state) -> html)] where state is one of `states` lower-cased."""
    rows = [(label, [fn(s.lower()) for s in states]) for label, fn in variants]
    return matrix(states, rows, first)


def themes(html: str, light: str | None = None) -> str:
    """The same markup in the light and the dark theme, side by side."""
    return (f'<div class="ds-themes"><div data-theme="light">{light or html}</div>'
            f'<div data-theme="dark">{html}</div></div>')


def keys(rows: list[tuple[str, str]]) -> str:
    body = "".join(f"<tr><td>{k}</td><td>{a}</td></tr>" for k, a in rows)
    return f'<div class="ds-table-wrap"><table class="ds-table ds-keys"><thead><tr><th scope="col">Key</th><th scope="col">Action</th></tr></thead><tbody>{body}</tbody></table></div>'


def kbd(*names: str) -> str:
    return "+".join(f"<kbd>{n}</kbd>" for n in names)


def pairs(rows: list[tuple[str, str, str, float]]) -> str:
    """[(label, fg token, bg token, minimum)] -> live contrast pairs."""
    items = "".join(f'<div class="ds-pair"><span>{label}</span><span class="ds-pair__ratio" data-contrast="{fg}|{bg}" data-min="{mn}"></span></div>'
                    for label, fg, bg, mn in rows)
    return f'<div class="ds-pairs">{items}</div>'


def a11y(*, pattern: str, keyboard: list[tuple[str, str]] | str, focus: str, labelling: str, contrast: list, motion: str, touch: str) -> str:
    kb = keys(keyboard) if isinstance(keyboard, list) else f"<p>{keyboard}</p>"
    return (f"<h3>Role and pattern</h3><p>{pattern}</p><h3>Keyboard</h3>{kb}<h3>Focus</h3><p>{focus}</p>"
            f"<h3>Labelling</h3><p>{labelling}</p><h3>Contrast</h3>{pairs(contrast)}<h3>Motion</h3><p>{motion}</p><h3>Touch</h3><p>{touch}</p>")


def swatch(token: str, theme: str) -> str:
    return f'<span class="ds-swatch-cell" data-theme="{theme}"><i data-token="{token}" data-swatch></i><span data-token="{token}"></span></span>'


def tok(token: str, theme: str | None = None) -> str:
    t = f' data-theme="{theme}"' if theme else ""
    return f'<span data-token="{token}"{t}></span>'


def token_table(rows: list[tuple[str, str]]) -> str:
    """rows: [(part, token)]. Colour tokens get light and dark swatches; others one live value.
    token may list several names separated by ' / ' (values shown for each)."""
    out = []
    for part, token in rows:
        names = [t.strip() for t in token.split("/")]
        names = [n if n.startswith("--") else "--" + n for n in names]
        label = " / ".join(f"<code>{n}</code>" for n in names)
        if all(n.startswith(("--color-", "--palette-")) for n in names):
            lt = " ".join(swatch(n, "light") for n in names)
            dk = " ".join(swatch(n, "dark") for n in names)
            out.append(f"<tr><td>{part}</td><td>{label}</td><td>{lt}</td><td>{dk}</td></tr>")
        else:
            vals = " / ".join(tok(n) for n in names)
            out.append(f'<tr><td>{part}</td><td>{label}</td><td colspan="2">{vals}</td></tr>')
    return ('<div class="ds-table-wrap"><table class="ds-table"><thead><tr><th scope="col">Part</th><th scope="col">Token</th>'
            f'<th scope="col">Light</th><th scope="col">Dark</th></tr></thead><tbody>{"".join(out)}</tbody></table></div>')


def classes(rows: list[tuple[str, str]], head: tuple[str, str] = ("Class / attribute", "Effect")) -> str:
    body = "".join(f"<tr><td>{c}</td><td>{e}</td></tr>" for c, e in rows)
    return f'<div class="ds-table-wrap"><table class="ds-table"><thead><tr><th scope="col">{head[0]}</th><th scope="col">{head[1]}</th></tr></thead><tbody>{body}</tbody></table></div>'


def table(head: list[str], rows: list[list[str]]) -> str:
    h = "".join(f'<th scope="col">{c}</th>' for c in head)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="ds-table-wrap"><table class="ds-table"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'


def dodont(items: list[tuple[str, str, str]]) -> str:
    """[("do"|"dont", canvas html, caption)]"""
    out = "".join(f'<figure class="ds-{k}"><div class="ds-example__canvas">{c}</div><figcaption>{cap}</figcaption></figure>' for k, c, cap in items)
    return f'<div class="ds-dodont">{out}</div>'


def mock(path: str, note: str = "") -> str:
    """Link to a mock: 'pages/catalog/default'. Fails the build when the mock is missing."""
    if not (MOCKS / f"{path}.html").is_file():
        raise FileNotFoundError(f"mock not found: {path}")
    SOURCES_USED.add(path)
    n = f" ({note})" if note else ""
    return f'<li><a href="../../mocks/{path}.html">{path}</a>{n}</li>'


def sources(items: list[tuple[str, str]], drift_text: str = "none; every mock used the kit classes.") -> str:
    li = "".join(mock(p, n) for p, n in items)
    return f"<p>Extracted from these mocks:</p><ul>{li}</ul><p>Drift fixed during extraction: {drift_text}</p>"


def link(kind: str, slug: str, text: str | None = None) -> str:
    """Cross-link: link('components', 'button') -> ../components/button.html"""
    return f'<a href="../{kind}/{slug}.html">{text or slug.replace("-", " ")}</a>'


def comp(slug: str, text: str | None = None) -> str:
    return link("components", slug, text)


def found(slug: str, text: str | None = None) -> str:
    return link("foundations", slug, text)


def patt(slug: str, text: str | None = None) -> str:
    return link("patterns", slug, text)


def ul(*items: str) -> str:
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def p(*paras: str) -> str:
    return "".join(f"<p>{x}</p>" for x in paras)
