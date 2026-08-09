<!-- Generated from https://thefellow.github.io/articles/weave-format-5-navigation-index/ by scripts/generate_llm_content.py; do not edit. -->

# Weave Format 5 Is a Navigation Index

Source: [https://thefellow.github.io/articles/weave-format-5-navigation-index/](https://thefellow.github.io/articles/weave-format-5-navigation-index/)

## Pyramid summary

- **~2 words:** Format-5 navigation
- **~8 words:** A small navigation profile points back to source.
- **Expanded:** Format 5 keeps the few semantic facts needed to reach current source quickly.

## Full content

**Part 1 of [Building Weave](/series/weave.md).**

Weave format 5 is deliberately small. It stores documents, declaration anchors, and relationships that help a person or coding agent choose where to look next.

![A compact index pointing back to source](/assets/images/articles/weave/compact-storage.svg)

Providers emit one `navigation-v1` profile. The profile retains dependencies, imports, implementations, tests, generation, documentation, authored links, and embeds. It does not retain occurrences, calls, references, locals, fields, containment, or body terms.

That boundary keeps indexing and queries practical. A result identifies a useful package, declaration, document, or relationship. Detailed investigation then returns to current source through `weave explore` and `weave context`.

The database is disposable and stays outside Git. Its job is navigation, not a second copy of the repository.

[Explore the Weave project](/projects/weave.md)
[Continue to freshness](/articles/weave-query-driven-freshness.md)
