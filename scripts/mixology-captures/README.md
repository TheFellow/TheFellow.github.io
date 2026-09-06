# Mixology deck screenshots

These are real application renders for `_site_pages/building-mixology-deck.md`.
The capture scripts use the deck's pinned source revision,
`635c59b4101bdc614beb973cef83e8c2073a9787`, from `go-modular-monolith`.

Run from the website checkout with Go 1.27.1+, `uv`, Google Chrome, Git, and
the C toolchain needed to compile Fyne's headless tests:

```sh
scripts/mixology-captures/capture.sh ../go-modular-monolith
# Optional: render elsewhere for comparison before replacing committed images.
scripts/mixology-captures/capture.sh ../go-modular-monolith /tmp/mixology-review
```

The script exports the pinned revision into a disposable directory, copies the
capture harnesses into its GUI and TUI test packages, and runs the normal seed
executable against a fresh temporary SQLite file. It removes that directory on
exit. It does not modify the application checkout or an existing demo database.

Both surfaces run as `owner`. The TUI uses the repository's `tuitest.Driver` to
advance the actual root model and drain commands. It captures 140 × 36 cell
frames in true color with a dark background, then converts ANSI spans to HTML
and rasterizes them at 2× resolution in headless Chrome. The terminal font stack is DejaVu Sans Mono, Menlo, then monospace;
these committed captures were made on macOS.
The Python dependencies are pinned in `render_terminal.py`.

The GUI uses Fyne's in-memory test application, a dark theme, a 1100 × 720
canvas, and the repository's deterministic desktop dependencies. PNGs come from
`Canvas().Capture()` through the existing `captureReview` helper. The menu and
order views receive real scroll events to bring the relevant content into view.
These images capture application content without OS window chrome.

| Asset | State and use in the deck |
| --- | --- |
| `tui-dashboard.png` | Fresh seed, seven workspaces and recent activity; orientation. |
| `tui-ingredients.png` | Browse Ingredients and select London Dry Gin; TUI walkthrough. |
| `tui-ingredient-edit.png` | Press `e` on that ingredient; keyboard input ownership. |
| `gui-ingredients.png` | Seeded ingredient table and filters; GUI walkthrough. |
| `gui-ingredient-edit.png` | Select London Dry Gin as owner; retained fields and tags. |
| `gui-menu.png` | Published Classic Cocktails, scrolled to readiness and six drinks. |
| `gui-order.png` | Place two Margaritas for “Bar seat four” through `Orders.Place`, then inspect the saved preparation. |

The ingredient forms remain unchanged. Seed menu prices are unset, so menu and
order values display `N/A`. IDs, timestamps, recent activity order, and catalog
row ordering can vary across runs; these are review images, not pixel goldens.
The scripts fail if expected seed records are missing or a TUI frame exceeds its
viewport. Inspect new PNGs before committing, and update HTML image dimensions
if the renderer or viewport changes. The deck links each image at full size and
includes alt text, captions, and capture context in speaker notes.
