#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "pyyaml>=6.0.3,<7",
# ]
# ///

from __future__ import annotations

import html
import re
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parent.parent
SITE_URL = "https://thefellow.github.io"
GENERATOR_NAME = "scripts/generate_llm_content.py"

# Deliberately authored rather than mechanically truncated. These are the two
# smallest levels of each page's pyramid; the front-matter excerpt is the next.
SUMMARIES = {
    "/": ("Engineering notes", "Public notes connecting software architecture to working projects."),
    "/projects/": ("Project catalog", "Open-source projects with design context beyond their repository READMEs."),
    "/articles/": ("Practical articles", "Long-form articles turning architecture principles into testable working designs."),
    "/notes/": ("Technical notes", "Focused observations drawn from active projects, experiments, and research."),
    "/series/": ("Reading series", "Ordered paths through related articles, notes, and projects."),
    "/resume/": ("Engineering experience", "Staff-level experience in authorization, architecture, delivery, and technical leadership."),
    "/404.html": ("Missing page", "Navigation help when a requested page cannot be found."),
    "/projects/expr-dotnet/": ("Typed expressions", "A safe .NET expression language with inspectable compilation and bounded execution."),
    "/projects/go-modular-monolith/": ("Executable architecture", "A Go reference app enforcing modular boundaries and cross-cutting concerns."),
    "/projects/modular-monolith/": ("Semantic architecture port", "An idiomatic .NET port preserving Mixology's observable application behavior."),
    "/projects/cedar-dotnet/": ("Cedar for .NET", "A semantic Cedar implementation with idiomatic C# APIs and conformance tests."),
    "/projects/go-riblt/": ("Set reconciliation", "A generic Go RIBLT library reconciling sets with difference-sized communication."),
    "/projects/arch-lint/": ("Enforced boundaries", "A Go analyzer that makes architectural dependency rules build-time checks."),
    "/projects/fkyeah/": ("Agent pipelines", "An F# engine executing inspectable, resumable AI workflows from DOT graphs."),
    "/projects/enumstruct/": ("Exhaustive unions", "A Go analyzer that detects missing pointer-union cases as models evolve."),
    "/projects/fluid/": ("Fluid simulation", "An interactive Go playground for exploring two-dimensional Eulerian fluid dynamics."),
    "/projects/value-types/": ("Structural equality", "A compact C# library for modeling value-object equality and composition."),
    "/series/mixology/": ("Mixology series", "An ordered path through Mixology's executable application architecture."),
    "/articles/building-high-quality-software/": ("Architecture lessons", "Eleven lessons that turn architectural intent into executable software constraints."),
    "/articles/turning-cross-domain-calls-into-enforced-boundaries/": ("Domain boundaries", "Transactional events replace cross-domain calls with enforced ownership."),
    "/articles/preserving-truth-through-operational-degradation/": ("Honest degradation", "Preserve history while blocking knowingly degraded state promotion."),
    "/articles/growing-a-reciprocal-domain-workflow/": ("Reciprocal workflow", "Procurement and Inventory expose the boundary between reactions and workflows."),
    "/articles/building-an-application-tui-toolkit/": ("Testable TUI", "How Mixology adapts MVVM and Elm ideas into an application toolkit."),
    "/articles/growing-mixology-with-fyne/": ("GUI expansion", "Tracking Mixology's testable growth from two surfaces to three."),
    "/articles/authorization-is-part-of-navigation/": ("Authorized navigation", "How Cedar shapes routes, aggregates, rows, and available actions."),
    "/articles/bespoke-views-over-a-shared-application-boundary/": ("Bespoke surfaces", "Why native views share application behavior, not universal view models."),
    "/articles/typed-filtering-over-bstore/": ("Typed filters", "How typed expressions become safe, exact bstore query plans."),
    "/articles/using-a-third-surface-as-an-architecture-test/": ("Architecture audit", "A third presentation runtime tests whether application boundaries are real."),
    "/articles/testing-native-go-desktop-applications-headlessly/": ("Headless desktop", "Layered evidence for native GUI behavior without opening windows."),
    "/articles/making-illegal-states-unrepresentable-in-go/": ("Modeled states", "F# techniques make Go domain constraints explicit and enforceable."),
    "/articles/building-a-file-backed-columnar-event-pipeline/": ("Columnar events", "Immutable Parquet snapshots support direct analytical queries and typed results."),
    "/notes/elliptic-curve-cryptography-from-first-principles/": ("ECDSA foundations", "A ground-up route through groups, finite fields, curves, and signatures."),
    "/notes/porting-cedar-semantics-from-go-to-dotnet/": ("Semantic porting", "How conformance tests preserve Cedar behavior while C# APIs remain idiomatic."),
    "/notes/type-safe-linear-algebra-in-fsharp/": ("Typed dimensions", "Phantom dimensions make invalid matrix arithmetic fail at compile time."),
    "/notes/octonions-and-the-standard-model-in-fsharp/": ("Executable octonions", "Non-associative multiplication produces a Furey-inspired eight-state particle pattern."),
    "/notes/riblt-in-go/": ("Rateless reconciliation", "A generic Go RIBLT reveals streaming set reconciliation step by step."),
    "/notes/linux-for-windows-brains/": ("Linux models", "Translate Windows concepts into practical Linux mental models."),
    "/notes/projecting-actions-across-user-interfaces/": ("Action projection", "Share action meaning across native interfaces without sharing views."),
    "/notes/retiring-weave/": ("Retired experiment", "A local code-index experiment yielded a useful benchmark."),
}

Document = dict[str, Any]


def parse_document(path: Path) -> Document:
    text = path.read_text()
    match = re.fullmatch(r"---\s*\n(.*?)\n---\s*\n(.*)", text, re.DOTALL)
    if not match:
        raise ValueError(f"Missing front matter: {path}")

    data = yaml.safe_load(match.group(1)) or {}
    data["source"] = str(path.relative_to(ROOT))
    data["body"] = match.group(2).strip()
    return data


def documents() -> list[Document]:
    patterns = ("_site_pages/*.md", "_projects/*.md", "_guides/*.md", "_posts/*.md", "_reading_series/*.md")
    paths = sorted(path for pattern in patterns for path in ROOT.glob(pattern))
    return [parse_document(path) for path in paths]


def validate_page_dates(docs: list[Document]) -> None:
    def is_date(value: object) -> bool:
        return isinstance(value, (date, datetime)) or (
            isinstance(value, str)
            and re.fullmatch(
                r"\d{4}-\d{2}-\d{2}(?:[ T]\d{2}:\d{2}:\d{2}(?: [+-]\d{4})?)?",
                value,
            )
            is not None
        )

    invalid = []
    for doc in docs:
        published = doc.get("date")
        modified = doc.get("last_modified_at")
        if not is_date(published):
            invalid.append(f"{doc['source']}: missing date")
        if not is_date(modified):
            invalid.append(f"{doc['source']}: missing last_modified_at")
    if invalid:
        raise ValueError(
            "Public pages need explicit dates to prevent build-time SEO metadata: "
            + ", ".join(invalid)
        )


def route_for(doc: Document) -> str:
    if permalink := doc.get("permalink"):
        return str(permalink)

    source = str(doc["source"])
    stem = Path(source).stem
    if source.startswith("_projects/"):
        return f"/projects/{stem}/"
    if source.startswith("_guides/"):
        return f"/articles/{stem}/"
    if source.startswith("_reading_series/"):
        return f"/series/{stem}/"
    raise ValueError(f"No public route for {source}")


def markdown_path(route: str) -> Path:
    if route == "/":
        return Path("index.md")
    return Path(f"{route.removeprefix('/').removesuffix('/')}.md")


def markdown_url(route: str) -> str:
    return f"/{markdown_path(route)}"


def link_markdown_alternates(body: str, all_docs: list[Document]) -> str:
    alternate_by_route = {
        route_for(doc): markdown_url(route_for(doc)) for doc in all_docs
    }

    def replace_link(match: re.Match[str]) -> str:
        target = match.group("target")
        path, separator, fragment = target.partition("#")
        alternate = alternate_by_route.get(path)
        if alternate is None:
            return match.group(0)
        suffix = f"{separator}{fragment}" if separator else ""
        return f"]({alternate}{suffix})"

    return re.sub(r"\]\((?P<target>/[^)\s]+)\)", replace_link, body)


def validate_markdown_navigation(
    rendered: dict[str, str], routes: dict[str, Document]
) -> None:
    html_links = []
    for alternate_route, content in rendered.items():
        for match in re.finditer(r"\]\((?P<target>/[^)\s]+)\)", content):
            target = match.group("target").partition("#")[0]
            if target in routes:
                html_links.append(f"{markdown_url(alternate_route)} -> {target}")
    if html_links:
        raise ValueError(
            "LLM alternates must link to explicit .md routes: "
            + ", ".join(html_links)
        )


def clean_body(body: str) -> str:
    strip_layout_indentation = 'class="resume-hero"' in body
    replacements = (
        (r"\{\{\s*['\"]([^'\"]+)['\"]\s*\|\s*relative_url\s*\}\}", r"\1", 0),
        (r"\{:\s*[^}]+\}", "", 0),
        (r'<div class="project-meta">.*?</div>', "", re.DOTALL),
        (r"<svg\b.*?</svg>", "", re.DOTALL),
        (r"</?(?:section|article|div)(?:\s[^>]*)?>", "", re.IGNORECASE),
        (r"<h2[^>]*>(.*?)</h2>", r"## \1", re.IGNORECASE | re.DOTALL),
        (r"<h3[^>]*>(.*?)</h3>", r"### \1", re.IGNORECASE | re.DOTALL),
        (r"<h4[^>]*>(.*?)</h4>", r"#### \1", re.IGNORECASE | re.DOTALL),
        (r"<p[^>]*>(.*?)</p>", r"\1\n", re.IGNORECASE | re.DOTALL),
        (r'<a\s+[^>]*href="([^"]+)"[^>]*>(.*?)</a>', r"[\2](\1)", re.IGNORECASE | re.DOTALL),
        (r"<strong[^>]*>(.*?)</strong>", r"**\1**", re.IGNORECASE | re.DOTALL),
        (r"<span[^>]*>(.*?)</span>", r"\1", re.IGNORECASE | re.DOTALL),
        (r"<li[^>]*>(.*?)</li>", r"- \1", re.IGNORECASE | re.DOTALL),
        (r"</?(?:ul|ol)(?:\s[^>]*)?>", "", re.IGNORECASE),
        (r"\[\s*\]\([^)]*\)", "", re.DOTALL),
        (r"\{%.+?%\}", "", re.DOTALL),
    )
    for pattern, replacement, flags in replacements:
        body = re.sub(pattern, replacement, body, flags=flags)
    if strip_layout_indentation:
        body = "\n".join(line.strip() for line in body.splitlines())
    return html.unescape(re.sub(r"\n{3,}", "\n\n", body).strip())


def sort_value(doc: Document) -> tuple[int, float | int]:
    if "order" in doc:
        return 0, int(doc["order"])
    value = doc.get("date")
    if isinstance(value, datetime):
        return 1, value.timestamp()
    if isinstance(value, date):
        return 1, datetime.combine(value, datetime.min.time()).timestamp()
    return 2, 0


def collection_index(doc: Document, all_docs: list[Document]) -> str | None:
    route = route_for(doc)
    prefixes = {
        "/projects/": "_projects/",
        "/articles/": "_guides/",
        "/notes/": "_posts/",
        "/series/": "_reading_series/",
    }
    prefix = prefixes.get(route)
    if prefix is None:
        return None

    intro = clean_body(doc["body"].split('<div class="feature-tiles', 1)[0])
    selected = sorted(
        (item for item in all_docs if str(item["source"]).startswith(prefix)),
        key=sort_value,
    )
    links = []
    for item in selected:
        item_route = route_for(item)
        links.append(
            f"- [{item['title']}]({markdown_url(item_route)}): {item['excerpt']}"
        )
    return f"{intro}\n\n{'\n'.join(links)}"


def series_body(doc: Document, all_docs: list[Document]) -> str | None:
    source = str(doc["source"])
    if not source.startswith("_reading_series/"):
        return None

    slug = Path(source).stem
    intro = clean_body(doc["body"].split("{% assign series_entries", 1)[0])
    entries = sorted(
        (item for item in all_docs if item.get("series") == slug),
        key=lambda item: int(item["series_order"]),
    )
    links = []
    for item in entries:
        kind = "Note" if str(item["source"]).startswith("_posts/") else "Article"
        links.append(
            f"{item['series_order']}. **{kind}:** "
            f"[{item['title']}]({markdown_url(route_for(item))}): {item['excerpt']}"
        )
    return f"{intro}\n\n{'\n'.join(links)}"


def home_body(all_docs: list[Document]) -> str:
    lines = []
    for route in ("/projects/", "/articles/", "/notes/", "/series/", "/resume/"):
        doc = next(item for item in all_docs if route_for(item) == route)
        lines.append(
            f"- [{doc['title']}]({markdown_url(route)}): "
            f"{SUMMARIES[route][1]}"
        )
    return "\n".join(lines)


def render_page(doc: Document, all_docs: list[Document]) -> str:
    route = route_for(doc)
    try:
        short, medium = SUMMARIES[route]
    except KeyError as error:
        raise ValueError(f"Missing pyramid summary for {route}") from error

    body = (
        home_body(all_docs)
        if route == "/"
        else collection_index(doc, all_docs)
        or series_body(doc, all_docs)
        or clean_body(doc["body"])
    )
    if series_slug := doc.get("series"):
        series_doc = next(
            item
            for item in all_docs
            if str(item["source"]) == f"_reading_series/{series_slug}.md"
        )
        body = (
            f"**Part {doc['series_order']} of [{series_doc['title']}]"
            f"({markdown_url(route_for(series_doc))}).**\n\n{body}"
        )
    body = link_markdown_alternates(body, all_docs)
    excerpt = doc.get("excerpt", medium)
    return f"""<!-- Generated from {SITE_URL}{route} by {GENERATOR_NAME}; do not edit. -->

# {doc["title"]}

Source: [{SITE_URL}{route}]({SITE_URL}{route})

## Pyramid summary

- **~2 words:** {short}
- **~8 words:** {medium}
- **Expanded:** {excerpt}

## Full content

{body}
"""


def write_if_changed(relative_path: str | Path, content: str) -> None:
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text() == content:
        return
    path.write_text(content)


def write_legacy_article_alternates(routes: dict[str, Document]) -> None:
    aliases = {"/guides/": "/articles/"}
    aliases.update(
        {
            route.replace("/articles/", "/guides/", 1): route
            for route in routes
            if re.fullmatch(r"/articles/.+/$", route)
        }
    )
    for legacy_route, article_route in aliases.items():
        title = routes[article_route]["title"]
        write_if_changed(
            markdown_path(legacy_route),
            f"<!-- Generated from {SITE_URL}{article_route} by {GENERATOR_NAME}; do not edit. -->\n\n"
            f"# {title}\n\nThis content moved to "
            f"[{markdown_url(article_route)}]({markdown_url(article_route)}).\n",
        )


def remove_obsolete_alternates() -> None:
    for path in ROOT.glob("**/*.md"):
        try:
            first_line = path.open().readline()
        except OSError:
            continue
        if f"Generated from {SITE_URL}" in first_line and "generate_llm_content." in first_line:
            path.unlink()


def main() -> None:
    remove_obsolete_alternates()
    docs = documents()
    validate_page_dates(docs)
    routes = {route_for(doc): doc for doc in docs}
    missing = routes.keys() - SUMMARIES.keys()
    stale = SUMMARIES.keys() - routes.keys()
    if missing:
        raise ValueError(f"Missing summaries: {', '.join(sorted(missing))}")
    if stale:
        raise ValueError(f"Stale summaries: {', '.join(sorted(stale))}")

    rendered = {route: render_page(doc, docs) for route, doc in routes.items()}
    validate_markdown_navigation(rendered, routes)
    for route, content in rendered.items():
        write_if_changed(markdown_path(route), content)
    write_legacy_article_alternates(routes)

    core_routes = ("/", "/projects/", "/articles/", "/notes/", "/series/", "/resume/")
    sections = {
        "Start Here": core_routes,
        "Projects": [route for route in routes if re.fullmatch(r"/projects/.+/$", route)],
        "Articles": [route for route in routes if re.fullmatch(r"/articles/.+/$", route)],
        "Notes": [route for route in routes if re.fullmatch(r"/notes/.+/$", route)],
        "Series": [route for route in routes if re.fullmatch(r"/series/.+/$", route)],
    }
    llms = [
        "# Ryan Harris — Engineering in Public",
        "",
        "> Software architecture, developer tools, authorization, and AI workflow notes connected to working open-source projects.",
        "",
        f"This is the compact level of a three-level context pyramid: follow a Markdown link for a page summary and full article, or use [llms-full.txt]({SITE_URL}/llms-full.txt) for the complete site corpus. Source repositories are linked from their project pages.",
    ]
    for heading, section_routes in sections.items():
        llms.append(f"\n## {heading}\n")
        for route in sorted(section_routes):
            doc = routes[route]
            llms.append(
                f"- [{doc['title']}]({SITE_URL}/{markdown_path(route)}): {SUMMARIES[route][1]}"
            )
    write_if_changed("llms.txt", "\n".join(llms) + "\n")

    full = [
        "# Ryan Harris — Full Site Context",
        "",
        f"> Generated full-text companion to [llms.txt]({SITE_URL}/llms.txt). Prefer the compact index when context is limited.",
        "",
    ]
    for route in sorted(route for route in routes if route != "/404.html"):
        full.extend((rendered[route], "\n---\n"))
    write_if_changed("llms-full.txt", "\n".join(full) + "\n")

    print(f"Generated {len(rendered)} page alternates, llms.txt, and llms-full.txt")


if __name__ == "__main__":
    main()
