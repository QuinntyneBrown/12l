Run on 25 Oct 2026 after the last rebuild:

| Check | Command | Result |
|---|---|---|
| Contrast, light and dark | `python .claude/skills/extracting-design-systems/scripts/check_contrast.py docs/design-system/tokens/tokens.css` | 156 pairs passed, 0 failed (78 pairs × 2 themes) |
| Structure, links, labels, raw colours | `python .claude/skills/extracting-design-systems/scripts/check_design_system.py docs/design-system` | 74 pages (53 components, 8 patterns, 12 foundations, index), 0 errors, 0 warnings |
| DTCG export | `python .claude/skills/extracting-design-systems/scripts/tokens_to_json.py docs/design-system/tokens/tokens.css` | 284 tokens written to `tokens/tokens.json` |
| Mocks on the system CSS | `python .claude/skills/writing-html-mocks/scripts/check_mocks.py docs/mocks` | 66 screens, 278 mocks, 0 errors, 0 warnings |
| Reflow at 360px | Playwright: `scrollWidth` of every page, both themes | No page scrolls sideways; no script errors |
| Screenshots | Index, button, dialog, listing card and color at 360 and 1280 px, light and dark; plus menu, file upload, text field, table, badge, toast, alert, error page, gallery, buy bar, top bar, layout primitives and the forms and dialogs patterns | Reviewed; fixed nav wrapping, anatomy overflow, unreadable ramp labels and the dark-theme size tag |
| Mocks before vs after | Pixel diff of catalog, listing detail and checkout at 360 and 1280 px against the mocks' own CSS | Identical; only the 992–1023 px range changes (breakpoint normalisation, see drift) |

Remaining differences, recorded rather than fixed in the mocks: components that no mock uses yet (sidebar navigation, numbered pagination, stepper, menu, button group, tooltip, progress bar, category tile) are documented from the kit and say so on their pages.
