# TheFellow.github.io

Source for Ryan Harris's project notes, tutorials, and resume site at <https://thefellow.github.io>.

## Editing content

- Project commentary is in `_projects/`.
- Long-form series are in `_guides/`.
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

Every content file begins with YAML front matter. Copy a nearby file when adding a project, guide, or note so the theme applies the right layout automatically.

## Changing the theme appearance

The site uses the free [Minimal Mistakes](https://jekyllthemes.io/theme/minimal-mistakes) theme, pinned as a remote theme so its source does not have to be copied into this repository.

For a new color scheme, change this single line in `_config.yml`:

```yaml
minimal_mistakes_skin: "neon"
```

Available built-in values are `default`, `air`, `aqua`, `contrast`, `dark`, `dirt`, `neon`, `mint`, `plum`, and `sunrise`. To upgrade the theme itself, change the version on the adjacent `remote_theme` line and test the site.

## Previewing locally

Use a current Ruby installation with Bundler:

```sh
bundle install
bundle exec jekyll serve --livereload
```

Then open <http://localhost:4000>. GitHub Pages builds and publishes `main` automatically.
