# TheFellow.github.io

Source for Ryan Harris's projects, articles, notes, and resume site at
<https://thefellow.github.io>.

Repository-wide content, routing, and validation rules for automated contributors
are codified in [`AGENTS.md`](AGENTS.md).

## Editing content

- Project commentary is in `_projects/`.
- Long-form articles are authored in `_guides/` and published under `/articles/`;
  the source directory retains its name for Jekyll collection compatibility.
- Ordered reading paths are in `_reading_series/`.
- Dated notes go in `_posts/` using `YYYY-MM-DD-title.md` filenames.
- Top navigation is in `_data/navigation.yml`.
- Standalone pages live in `_site_pages/`.

## LLM-readable site

Every public page has a generated Markdown alternate: remove a trailing slash and
append `.md` (the home page is `/index.md`). The site also publishes a concise
[`llms.txt`](https://thefellow.github.io/llms.txt) index and an expanded
[`llms-full.txt`](https://thefellow.github.io/llms-full.txt) corpus.

After editing or adding content, regenerate these files and commit the result:

```sh
uv run scripts/generate_llm_content.py
```

The script uses [PEP 723](https://peps.python.org/pep-0723/) inline metadata,
so `uv` creates an isolated environment and installs its declared dependency
without requiring a project-wide Python environment.

The generator fails if a public source page lacks a pyramid summary, so the
compact index, page-level context, and full text remain synchronized.

Every content file begins with YAML front matter. Copy a nearby file when adding a project, article, or note so the theme applies the right layout automatically.

## Writing style

- Use commas, periods, parentheses, or semicolons instead of em dashes.
- Describe demonstrations in terms of what they explore and show. Do not add defensive disclaimers about what they are not or compare their scope with a production system unless that distinction is essential to understanding the work.
- Match the direct, first-person engineering voice of the surrounding content. Prefer concrete descriptions over promotional or generic explanatory language.

## Changing the theme appearance

The site uses the free [Minimal Mistakes](https://jekyllthemes.io/theme/minimal-mistakes) theme, pinned as a remote theme so its source does not have to be copied into this repository.

For a new color scheme, change this single line in `_config.yml`:

```yaml
minimal_mistakes_skin: "neon"
```

Available built-in values are `default`, `air`, `aqua`, `contrast`, `dark`, `dirt`, `neon`, `mint`, `plum`, and `sunrise`. To upgrade the theme itself, change the version on the adjacent `remote_theme` line and test the site.

## Previewing locally

The repository pins Ruby and provides setup, build, and serve tasks through
[mise](https://mise.jdx.dev/):

```sh
mise install
mise run setup
mise run serve
```

Then open <http://localhost:4000>. Run `mise run build` for the same rendering
check used on pull requests. GitHub Pages builds and publishes `main`
automatically.
