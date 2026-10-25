#!/usr/bin/env python3
"""Render the 12L design-system documentation.

    python docs/design-system/_build/build.py

Imports every comp_*.py, foundations.py and patterns.py module, renders one
HTML page per registered component, foundation and pattern, splices the
component CSS kept in _build/css/*.css into assets/components.css (between
the @@extensions markers), and writes index.html and README.md. Then run:

    python .claude/skills/extracting-design-systems/scripts/check_design_system.py docs/design-system
    python .claude/skills/extracting-design-systems/scripts/check_contrast.py docs/design-system/tokens/tokens.css
"""
from __future__ import annotations

import importlib
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import ds  # noqa: E402
from ds import esc  # noqa: E402

ROOT = ds.ROOT


def load_modules() -> None:
    for name in ["foundations", *sorted(p.stem for p in HERE.glob("comp_*.py")), "patterns", "drift_log"]:
        if (HERE / f"{name}.py").exists():
            try:
                importlib.import_module(name)
            except Exception as exc:  # another author may be mid-edit; report and carry on
                print(f"WARN  skipped {name}.py: {type(exc).__name__}: {exc}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Shell
# ---------------------------------------------------------------------------
FOUNDATION_ORDER = ["color", "typography", "spacing", "layout", "elevation", "shape", "motion", "iconography",
                    "theming", "responsive", "accessibility", "content"]
PATTERN_ORDER = ["forms", "feedback-and-loading", "empty-and-error-states", "navigation-and-page-structure",
                 "dialogs-and-overlays", "data-tables-and-lists", "notifications", "content-and-tone"]


def ordered_foundations():
    return [ds.FOUNDATIONS[s] for s in FOUNDATION_ORDER if s in ds.FOUNDATIONS] + \
           [f for s, f in ds.FOUNDATIONS.items() if s not in FOUNDATION_ORDER]


def ordered_patterns():
    return [ds.PATTERNS[s] for s in PATTERN_ORDER if s in ds.PATTERNS] + \
           [p for s, p in ds.PATTERNS.items() if s not in PATTERN_ORDER]


def components_by_group():
    out = []
    for g in ds.COMPONENT_GROUPS:
        items = sorted((c for c in ds.COMPONENTS.values() if c.group == g), key=lambda c: c.title.lower())
        if items:
            out.append((g, items))
    return out


def nav(prefix: str) -> str:
    def group(title, links):
        li = "".join(f'<li><a href="{prefix}{h}">{esc(t)}</a></li>' for h, t in links)
        return f"<details open><summary>{title}</summary><ul>{li}</ul></details>"
    parts = [group("Foundations", [(f"foundations/{f.slug}.html", f.title) for f in ordered_foundations()])]
    for g, items in components_by_group():
        parts.append(group(g, [(f"components/{c.slug}.html", c.title) for c in items]))
    parts.append(group("Patterns", [(f"patterns/{p.slug}.html", p.title) for p in ordered_patterns()]))
    home = f"{prefix}index.html"
    return (f'<nav class="ds-nav" aria-label="Design system"><div class="ds-nav__brand">'
            f'<a class="ds-nav__home" href="{home}" aria-label="12L design system home"><span class="logo logo--sm">{ds.LOGO_SVG}</span><span>Design system</span></a>'
            f'<button class="ds-theme-toggle" type="button" aria-pressed="false">☾ Dark</button></div>{"".join(parts)}</nav>')


def shell(*, title: str, description: str, prefix: str, kicker: str, h1: str, lead: str, pills: list[str], toc: list[tuple[str, str]], body: str) -> str:
    pill_html = "".join(pills)
    toc_html = "".join(f'<li><a href="#{i}">{esc(t)}</a></li>' for i, t in toc)
    toc_block = f'<ul class="ds-toc">{toc_html}</ul>' if toc else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="icon" href="{prefix}assets/favicon.ico">
<link rel="stylesheet" href="{prefix}tokens/tokens.css">
<link rel="stylesheet" href="{prefix}assets/components.css">
<link rel="stylesheet" href="{prefix}assets/ds.css">
</head>
<body id="top">
<a class="skip-link" href="#main">Skip to content</a>
<div class="ds-shell">
{nav(prefix)}
<main id="main" class="ds-main">
<header class="ds-header">
<p class="ds-kicker">{kicker}</p>
<h1>{h1}</h1>
<p class="ds-lead">{lead}</p>
<div class="ds-meta">{pill_html}</div>
{toc_block}
</header>
{body}
<footer class="ds-footer"><span>12L design system · extracted from <a href="{prefix}../mocks/index.html">docs/mocks</a> on {ds.EXTRACTED}</span><a href="#top">Back to top</a></footer>
</main>
</div>
<script src="{prefix}assets/ds.js"></script>
</body>
</html>
"""


def section(sid: str, title: str, content) -> str:
    if isinstance(content, ds.NA):
        return (f'<section class="ds-section" id="{sid}" data-na="{esc(content.reason)}"><h2><a href="#{sid}">{title}</a></h2>'
                f'<p class="ds-na">{content.reason}</p></section>\n')
    return f'<section class="ds-section" id="{sid}"><h2><a href="#{sid}">{title}</a></h2>\n{content}\n</section>\n'


def pill(text: str, ok: bool = False) -> str:
    return f'<span class="ds-pill{" ds-pill--ok" if ok else ""}">{text}</span>'


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def render_component(c: ds.Component) -> str:
    body = "".join(section(sid, t, c.sections[sid]) for sid, t in ds.COMPONENT_SECTIONS)
    pills = [pill("WCAG 2.2 AA", True), pill("Status: stable"), *[pill(x) for x in c.pills]]
    return shell(title=f"{c.title} — 12L design system", description=strip(c.lead), prefix="../",
                 kicker=f"Component · {c.group}", h1=c.title, lead=c.lead, pills=pills, toc=ds.COMPONENT_SECTIONS, body=body)


def render_foundation(f: ds.Foundation) -> str:
    body = "".join(section(sid, t, h) for sid, t, h in f.sections)
    return shell(title=f"{f.title} — 12L design system", description=strip(f.lead), prefix="../",
                 kicker="Foundation", h1=f.title, lead=f.lead, pills=[pill("Tokens: tokens/tokens.css")],
                 toc=[(sid, t) for sid, t, _ in f.sections], body=body)


def render_pattern(pt: ds.Pattern) -> str:
    body = "".join(section(sid, t, pt.sections[sid]) for sid, t in ds.PATTERN_SECTIONS)
    return shell(title=f"{pt.title} — 12L design system", description=strip(pt.lead), prefix="../",
                 kicker="Pattern", h1=pt.title, lead=pt.lead, pills=[pill("WCAG 2.2 AA", True)], toc=ds.PATTERN_SECTIONS, body=body)


def strip(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def card(href: str, title: str, text: str, preview: str = "") -> str:
    pv = f'<div class="ds-card__preview" aria-hidden="true">{preview}</div>' if preview else ""
    return f'<a class="ds-card" href="{href}">{pv}<b>{esc(title)}</b><span>{text}</span></a>'


def render_index() -> str:
    C = ds.COMPONENTS
    start = [
        card("foundations/color.html", "Color", "Ink, paper and signal red; roles, themes and every checked contrast pair.",
             '<span class="ds-index-swatches"><i style="--swatch: var(--palette-ink-950);"></i><i style="--swatch: var(--palette-paper-100);"></i><i style="--swatch: var(--palette-signal-500);"></i></span>'),
        card("foundations/typography.html", "Typography", "Archivo black headings, Inter body, a nine-step scale.",
             '<span class="display" style="font-size: var(--font-size-3xl);">Aa 12</span>'),
        card("foundations/layout.html", "Layout", "Breakpoints, 4/8/12 columns, gutters, margins, page templates.",
             '<span class="ds-index-grid"><i></i><i></i><i></i><i></i></span>'),
        card("components/button.html", "Button", "Ink primary, outlined secondary, ghost, link, danger; every state.",
             '<span class="btn btn--primary btn--sm">Buy now</span>'),
        card("components/form-field.html", "Form field", "Label, control, help, error and counter in one wrapper.",
             '<span class="input input--sm" style="width: 9rem; display: inline-flex; align-items: center; color: var(--color-fg-subtle);">you@example.com</span>'),
        card("components/dialog.html", "Dialog", "Modal dialogs and mobile bottom sheets with focus management.",
             '<span class="ds-index-dialog"></span>'),
    ]

    found_cards = "".join(card(f"foundations/{f.slug}.html", f.title, f.covers) for f in ordered_foundations())
    groups = ""
    for g, items in components_by_group():
        groups += f'<h3>{g}</h3><div class="ds-cards">' + "".join(card(f"components/{c.slug}.html", c.title, strip(c.lead)) for c in items) + "</div>"
    patt_cards = "".join(card(f"patterns/{pt.slug}.html", pt.title, pt.covers) for pt in ordered_patterns())
    body = f"""
<section class="ds-section" id="start"><h2><a href="#start">Start here</a></h2>
<p>The 12L design system is the marketplace's visual and interaction language written down once: the tokens, components and patterns every 12L screen is built from. It was extracted from the {len(ds.SOURCES_USED)} mocks it cites (of the full set in <a href="../mocks/index.html">docs/mocks</a>), normalised into tokens, and verified for WCAG 2.2 AA in the light and dark themes.</p>
<div class="ds-cards">{"".join(start)}</div>
</section>
<section class="ds-section" id="foundations"><h2><a href="#foundations">Foundations</a></h2><div class="ds-cards">{found_cards}</div></section>
<section class="ds-section" id="components"><h2><a href="#components">Components</a></h2><p>{len(C)} components in {len(components_by_group())} groups. Every page shows anatomy, variants, sizes, the full state matrix in both themes, responsive rules, accessibility, content rules, do and don't, live tokens, code and the mocks it came from.</p>{groups}</section>
<section class="ds-section" id="patterns"><h2><a href="#patterns">Patterns</a></h2><div class="ds-cards">{patt_cards}</div></section>
<section class="ds-section" id="how-to-use"><h2><a href="#how-to-use">How to use</a></h2>
<ol>
<li>Link the two stylesheets in this order; nothing else is needed for the components to render:
<pre><code>{esc('<link rel="stylesheet" href="docs/design-system/tokens/tokens.css">')}
{esc('<link rel="stylesheet" href="docs/design-system/assets/components.css">')}</code></pre></li>
<li>Build markup with the documented classes and native elements (<code>&lt;button class="btn btn--primary"&gt;</code>, <code>&lt;div class="field"&gt;</code>). States come from real attributes: <code>disabled</code>, <code>aria-invalid</code>, <code>aria-busy</code>, <code>aria-pressed</code>, <code>aria-selected</code>, <code>aria-current</code>, <code>aria-expanded</code>. <code>data-state</code> exists only so these pages can show hover and focus statically.</li>
<li>Theme with <code>data-theme="light|dark"</code> on <code>&lt;html&gt;</code>; without it the OS preference applies. Never set colours in a component: override a component token (<code>--btn-bg</code>) or a semantic token instead. See {''}<a href="foundations/theming.html">Theming</a>.</li>
<li>Generate platform constants (Angular, .NET, email templates) from <a href="tokens/tokens.json"><code>tokens/tokens.json</code></a>, a W3C DTCG export with the dark theme under <code>$extensions</code>.</li>
<li>Before shipping a new colour pairing, add it to <a href="tokens/contrast-pairs.json"><code>tokens/contrast-pairs.json</code></a> and run the contrast check.</li>
</ol>
</section>
<section class="ds-section" id="provenance"><h2><a href="#provenance">Provenance</a></h2>
<p>Extracted on {ds.EXTRACTED} from <a href="../mocks/index.html">docs/mocks</a> (66 screens, 278 mocks) and their draft kit (<code>docs/mocks/assets/tokens.css</code>, <code>ui.css</code>). The mocks now load this system's <code>tokens.css</code> and <code>components.css</code> directly, so a change here shows up in every mock. Every value traces to a mock or to a correction logged in the <a href="README.md">README drift log</a>.</p>
<p>The pages are generated by <code>docs/design-system/_build/build.py</code>; edit the modules there, not the HTML.</p>
</section>
"""
    toc = [("start", "Start here"), ("foundations", "Foundations"), ("components", "Components"), ("patterns", "Patterns"), ("how-to-use", "How to use"), ("provenance", "Provenance")]
    pills = [pill("WCAG 2.2 AA", True), pill(f"{len(ds.FOUNDATIONS)} foundations"), pill(f"{len(C)} components"), pill(f"{len(ds.PATTERNS)} patterns"), pill("Light + dark")]
    return shell(title="12L design system", description="Tokens, components and patterns for the 12L marketplace, extracted from the HTML mocks.",
                 prefix="", kicker="12L · Design system", h1="12L design system",
                 lead="Ink, paper and one red L. Square corners, heavy numerals, lots of white space, one primary action per screen. Everything a 12L screen is made of, in one place.",
                 pills=pills, toc=toc, body=body)


def md_escape(s: str) -> str:
    return strip(s).replace("|", "\\|").replace("\n", " ").strip()


def render_readme(verification: str) -> str:
    lines = [f"# 12L design system", "",
             f"Extracted from [docs/mocks](../mocks/README.md) on {ds.EXTRACTED}. Open [index.html](index.html) locally (no server needed); "
             "press `t` or use the toggle to switch themes.", "",
             "Ink `#0B0B0B`, paper `#F4F1EA` and signal red `#E1251B` from the logo; square corners and one 45° chamfer; "
             "Archivo black-weight headings over Inter body text. Every page shows its tokens live in both themes and every colour pair is "
             "checked against WCAG 2.2 AA.", "",
             "## Foundations", "", "| Page | Covers |", "|---|---|"]
    for f in ordered_foundations():
        lines.append(f"| [{f.title}](foundations/{f.slug}.html) | {md_escape(f.covers)} |")
    lines += ["", "## Components", ""]
    for g, items in components_by_group():
        lines += [f"### {g}", "", "| Component | Variants | States | Source mocks |", "|---|---|---|---|"]
        for c in items:
            srcs = re.findall(r'href="\.\./\.\./mocks/([^"]+)\.html"', c.sections["sources"]) if isinstance(c.sections["sources"], str) else []
            src = ", ".join(f"[{s}](../mocks/{s}.html)" for s in srcs[:3]) + (f" +{len(srcs) - 3}" if len(srcs) > 3 else "")
            lines.append(f"| [{c.title}](components/{c.slug}.html) | {md_escape(c.summary['variants'])} | {md_escape(c.summary['states'])} | {src} |")
        lines.append("")
    lines += ["## Patterns", "", "| Pattern | Covers |", "|---|---|"]
    for pt in ordered_patterns():
        lines.append(f"| [{pt.title}](patterns/{pt.slug}.html) | {md_escape(pt.covers)} |")
    lines += ["", "## Tokens", "",
              "- [`tokens/tokens.css`](tokens/tokens.css) — source of truth: primitives, semantic tokens, light and dark themes, reduced-motion, more-contrast and forced-colours overrides.",
              "- [`tokens/tokens.json`](tokens/tokens.json) — W3C DTCG export generated from `tokens.css` (dark theme under `$extensions`).",
              "- [`tokens/contrast-pairs.json`](tokens/contrast-pairs.json) — every foreground/background pair the components rely on, checked in both themes.",
              "- [`assets/components.css`](assets/components.css) — the product stylesheet: every component class, token-driven, with `data-state` hooks.",
              "- [`assets/ds.css`](assets/ds.css), [`assets/ds.js`](assets/ds.js) — documentation chrome only (theme toggle, live token values and contrast ratios).",
              "", "## How the pages are built", "",
              "The HTML is generated so that every page shares one shell, one navigation and the same section order:", "",
              "```sh", "python docs/design-system/_build/build.py", "```", "",
              "Component pages live in `_build/comp_*.py`, foundations in `_build/foundations.py`, patterns in `_build/patterns.py`, "
              "and component CSS added during extraction in `_build/css/*.css` (spliced into `assets/components.css`). Edit those, then rebuild.", "",
              "## Changelog", "",
              f"- {ds.EXTRACTED} — first extraction from the mocks (v1.0).", "",
              "## Drift found in the mocks", "",
              "Values and markup in the mocks that disagreed with the system, and what was done. The mocks now load this system's CSS, so each fix applies there too.", "",
              "| Mock | Issue | Resolution |", "|---|---|---|"]
    for m, issue, res in ds.DRIFT:
        lines.append(f"| {md_escape(m)} | {md_escape(issue)} | {md_escape(res)} |")
    lines += ["", "## Verification", "", verification, ""]
    return "\n".join(lines)


def splice_css() -> None:
    path = ROOT / "assets" / "components.css"
    css = path.read_text(encoding="utf-8")
    start, end = "/* @@extensions:start", "/* @@extensions:end */"
    parts = []
    for f in sorted((HERE / "css").glob("*.css")):
        parts.append(f"/* ---- from _build/css/{f.name} ---- */\n" + f.read_text(encoding="utf-8").strip() + "\n")
    block = (f"{start} — generated by _build/build.py from _build/css/*.css; edit those files */\n" + "".join(parts) + end)
    if start in css:
        css = re.sub(re.escape(start) + r".*?" + re.escape(end), lambda m: block, css, flags=re.S)
    else:
        css = css.rstrip() + "\n\n" + block + "\n"
    path.write_text(css, encoding="utf-8")


def main() -> int:
    load_modules()
    splice_css()
    written = []
    for kind, reg, fn in [("components", ds.COMPONENTS, render_component), ("foundations", ds.FOUNDATIONS, render_foundation), ("patterns", ds.PATTERNS, render_pattern)]:
        out = ROOT / kind
        out.mkdir(exist_ok=True)
        for slug, obj in reg.items():
            (out / f"{slug}.html").write_text(fn(obj), encoding="utf-8")
            written.append(f"{kind}/{slug}.html")
        for stale in out.glob("*.html"):
            if stale.stem not in reg:
                stale.unlink()
    (ROOT / "index.html").write_text(render_index(), encoding="utf-8")
    verification_file = HERE / "verification.md"
    verification = verification_file.read_text(encoding="utf-8").strip() if verification_file.exists() else "Not yet verified."
    (ROOT / "README.md").write_text(render_readme(verification), encoding="utf-8")
    print(f"wrote {len(written)} pages + index.html + README.md ({len(ds.COMPONENTS)} components, {len(ds.FOUNDATIONS)} foundations, {len(ds.PATTERNS)} patterns, {len(ds.DRIFT)} drift entries)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
