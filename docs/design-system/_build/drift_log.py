"""Drift found while extracting tokens and the shared kit (component pages log their own)."""
from ds import drift

drift("assets/tokens.css", "Radius comments said 2/4/8/12/16px while the values were 0/2/2/4/6px.", "Documented the real values; comments fixed; five distinct radii kept.")
drift("assets/tokens.css", "--layout-topbar-height comment said 56px, value 4rem (64px); --layout-container-max comment said 1280px, value 76rem (1216px).", "Kept the values the mocks render with; comments fixed.")
drift("assets/tokens.css", "The prefers-color-scheme dark block repeated the four --color-inverse-* lines and differed from the [data-theme=dark] block.", "Both dark blocks are now generated identical.")
drift("assets/tokens.css", "Dark --color-bg-surface-sunken was a raw #080808 inside the theme block.", "Added primitive --palette-ink-1000 and aliased it.")
drift("assets/tokens.css", "Dark --color-focus-ring-offset and --shadow-focus resolved against the light surface inside nested [data-theme=dark] containers.", "Redeclared both in the dark theme.")
drift("assets/ui.css", "Spinner, shimmer and pulse used raw 0.8s, 1.4s and 1.6s durations; borders used raw 1-4px widths.", "Added --duration-cycle-fast (800ms) and --duration-cycle (1400ms; pulse snapped from 1.6s) and --border-width-accent/heavy; components.css uses tokens only.")
drift("assets/ui.css", "The global reduced-motion rule also stopped the spinner and the loading button, hiding a status indicator.", "Spinners keep turning under reduced motion; decorative motion still stops.")
drift("pages/catalog/default (category tiles)", "Size tags were fixed ink on paper in both themes, so outside a photo they vanished into dark-theme surfaces (1.1:1).", "Size tags use --color-accent / --color-fg-on-accent by default and switch to the fixed --color-size-tag-* only on photos.")
