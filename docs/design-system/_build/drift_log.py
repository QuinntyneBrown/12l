"""Drift found while extracting tokens and the shared kit (component pages log their own)."""
from ds import drift

drift("assets/tokens.css", "Radius comments said 2/4/8/12/16px while the values were 0/2/2/4/6px.", "Documented the real values; comments fixed; five distinct radii kept.")
drift("assets/tokens.css", "--layout-topbar-height comment said 56px, value 4rem (64px); --layout-container-max comment said 1280px, value 76rem (1216px).", "Kept the values the mocks render with; comments fixed.")
drift("assets/tokens.css", "The prefers-color-scheme dark block repeated the four --color-inverse-* lines and differed from the [data-theme=dark] block.", "Both dark blocks are now generated identical.")
drift("assets/tokens.css", "Dark --color-bg-surface-sunken was a raw #080808 inside the theme block.", "Added primitive --palette-ink-1000 and aliased it.")
drift("assets/tokens.css", "Dark --color-focus-ring-offset and --shadow-focus resolved against the light surface inside nested [data-theme=dark] containers.", "Redeclared both in the dark theme.")
drift("assets/ui.css", "Borders used raw 1px, 2px, 3px and 4px widths.", "Added --border-width-accent (3px) and --border-width-heavy (4px) beside hairline and thick; components.css uses tokens only.")
drift("pages/listing-detail/default, pages/sell/default", "Size tags were fixed ink on paper in both themes, so outside a photo (next to the listing title, in the sell form) they vanished into the dark-theme canvas (1.1:1).", "Size tags use --color-accent / --color-fg-on-accent by default and switch to the fixed --color-size-tag-* only on photos.")
