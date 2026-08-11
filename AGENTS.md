# Website contributor instructions

These instructions apply to the entire repository. Preserve the site as two
parallel, explicitly linked representations of the same content: the
human-facing Jekyll site and the generated Markdown site for LLM consumption.

## Sources and generated files

- Edit project commentary in `_projects/`, long-form articles in `_guides/`,
  ordered reading paths in `_reading_series/`, dated notes in `_posts/`, and standalone
  pages in `_site_pages/`.
- Edit top-level human navigation in `_data/navigation.yml`.
- Treat `index.md`, `projects.md`, `articles.md`, `notes.md`, `resume.md`,
  `404.html.md`, the `projects/`, `articles/`, and `notes/` Markdown trees,
  `llms.txt`, and `llms-full.txt` as generated output. Do not edit them by hand.
- After changing authored content or the generator, run
  `uv run scripts/generate_llm_content.py` and commit every resulting change.
- Add a `SUMMARIES` entry in `scripts/generate_llm_content.py` for every new
  public page. Preserve the context pyramid: a roughly two-word summary, a
  roughly eight-word summary, the front-matter excerpt, and the full content.
- Begin authored content files with YAML front matter. Copy the structure of a
  nearby file in the same collection so layouts and collection behavior remain
  consistent.
- Give every public authored page a `date` and `last_modified_at` in its YAML
  front matter. Update `last_modified_at` only for substantive page changes so
  SEO metadata and the sitemap never fall back to the site build time.

## Parallel-site routing contract

- Human pages use trailing-slash routes, such as `/notes/` and
  `/notes/example/`. Human-facing navigation, breadcrumbs, and internal content
  links must include the trailing slash. Do not use an extensionless basename
  such as `/notes` because it is ambiguous beside `/notes.md`.
- LLM pages use explicit `.md` routes, such as `/notes.md` and
  `/notes/example.md`; the LLM home page is `/index.md`.
- Links within generated LLM pages and LLM indexes must stay in the Markdown
  site and point directly to `.md` routes. Do not make an LLM traverse the HTML
  site or choose between duplicate HTML and Markdown links.
- `llms.txt` must index the explicit `.md` URLs. `llms-full.txt` must preserve
  the same Markdown-to-Markdown internal navigation in its rendered content.
- A generated page's canonical `Source` link may point to the human-facing HTML
  page. This attribution link is the deliberate boundary between the parallel
  sites, not internal LLM navigation.
- Maintain these rules in `scripts/generate_llm_content.py`; do not rely on
  manual repairs to generated files. Keep its validation that rejects links
  from generated LLM pages back to known HTML routes.

## Content voice and shape

- Use commas, periods, parentheses, or semicolons instead of em dashes.
- Describe demonstrations in terms of what they explore and show. Do not add
  defensive disclaimers about what they are not or compare their scope with a
  production system unless that distinction is essential to understanding the
  work.
- Match the direct, first-person engineering voice of the surrounding content.
  Prefer concrete descriptions over promotional or generic explanatory
  language.
- State observable software behavior plainly. Say that invalid code “does not
  compile” or “fails to compile” when that is the behavior; avoid indirect
  phrasing such as “the program does not type-check.”
- Preserve the established page shape: useful front matter and excerpt, a
  concrete opening, descriptive sections that build the idea, executable or
  mathematical detail where it helps, and a concise synthesis grounded in the
  demonstrated result.

## Required checks

- Run `python3 scripts/check_feature_icons.py` after adding or changing an `icon` field or the shared feature icon include.
- Run `uv run scripts/generate_llm_content.py` after content or generator
  changes. A second run should leave the worktree unchanged.
- Run `git diff --check`.
- Confirm human-facing internal routes use trailing slashes and generated
  LLM-facing internal routes use `.md` suffixes.
- When Ruby and the pinned Bundler version are available, run
  `bundle exec jekyll build` for changes that can affect rendering, layouts,
  includes, navigation, or configuration. Report clearly when the local Ruby
  environment prevents this check.
- Do not weaken `.github/workflows/llm-content.yml`; it must regenerate the LLM
  site and fail when committed generated files are stale.
