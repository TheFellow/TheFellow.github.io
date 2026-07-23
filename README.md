# TheFellow.github.io

Source for Ryan Harris's project notes, tutorials, and resume site at <https://thefellow.github.io>.

## Editing content

- Project commentary is in `_projects/`.
- Long-form series are in `_guides/`.
- Dated notes go in `_posts/` using `YYYY-MM-DD-title.md` filenames.
- Top navigation is in `_data/navigation.yml`.
- The future resume lives at `resume.md`.

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
