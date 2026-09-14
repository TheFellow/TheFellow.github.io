# Mixology deck screenshots

These are real application renders for `_site_pages/building-mixology-deck.md`.
The capture scripts use the deck's pinned source revision,
`0d5e64b0455f7a5c96d4afada64654a5fdbb9a2c`, from `go-modular-monolith`.

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

The complete capture set was rerendered from PR #64 on September 13, 2026, including the dashboard, ingredient editors, menu and order details, and typed-error adapters. The harness asserts real domain results and typed errors before capturing each surface. Seed menu prices are unset, so menu and
order values display `N/A`. IDs, timestamps, recent activity order, and catalog
row ordering can vary across runs; these are review images, not pixel goldens.
The scripts fail if expected seed records are missing or a TUI frame exceeds its
viewport. Inspect new PNGs before committing, and update HTML image dimensions
if the renderer or viewport changes. The deck links each image at full size and
includes alt text, captions, and capture context in speaker notes.

## Typed error captures (chapter 1.3)

The same script also captures six error screens and `cli-errors.txt` using the
fixtures and harnesses in `errors/`:

| Kind | Scenario | CLI | TUI root | GUI |
| --- | --- | --- | --- | --- |
| Invalid | Create an ingredient with no name. | stderr, exit 10 | error styling | inline form validation |
| Conflict | Create the existing London Dry Gin again. | stderr, exit 40 | warning styling | warning dialog, input retained |
| Internal | Inject a readiness failure through the real action evaluator. | safe stderr, exit 50 | safe error styling | safe error dialog |

The first two CLI examples run the actual built CLI. `deck-error-probe` is a
small capture-only executable that feeds the chapter's injected, wrapped
Internal failure into the same `ToCLIExit` / `HandleExitCoder` boundary.
`MIXOLOGY_LOG_FILE` separates diagnostic logging from the captured stderr.
The capture asserts actual process exit codes, empty stdout, and safe output.

The TUI harness obtains Invalid and Conflict from real application commands,
then delivers each error through `routes.ErrorMsg`. These are specifically
**root status-bar adapter captures**, not recordings of a form's submit path.
The root uses `ToTUIError`; individual domain forms also have local error
rendering. Error frames use 120 × 34 cells. The harness checks the typed kind,
CLI code, TUI severity, displayed text, and absence of injected diagnostic detail.

The GUI captures call the real ingredient presenter's submit method. Invalid
is rejected by presenter preflight validation; Conflict reaches the domain/store
and returns through the mutation callback. Both preserve entered form values.
Internal is injected directly at `ShowPresentation` with the composed window's
real dialogs. GUI assertions check typed classification through presentation
wrappers, severity, safe message parity, and retained input on conflict.
The Internal captures do not induce a database outage or claim to exercise an
actual failed menu load.

The chapter also places the same duplicate-ingredient `Conflict` side by side
as three images. `cli-error-conflict.png` rasterizes the built CLI's captured
stderr and exit status; only its displayed invocation is reflowed with shell
continuations. `tui-error-conflict-detail.png` and
`gui-error-conflict-detail.png` crop the status bar and dialog from their full
captures without changing their pixels. The comparison links to the full images
and explains how the typed kind selects exit code 40 and warning severity
without parsing the message. The crop coordinates and expected capture sizes
are checked in `render_terminal.py`; inspect the comparison slide after changing
the capture viewport or application layout.
