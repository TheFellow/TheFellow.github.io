<!-- Generated from https://thefellow.github.io/articles/weave-source-only-declarations/ by scripts/generate_llm_content.py; do not edit. -->

# Index Declarations Without Executing the Repository

Source: [https://thefellow.github.io/articles/weave-source-only-declarations/](https://thefellow.github.io/articles/weave-source-only-declarations/)

## Pyramid summary

- **~2 words:** Source-only declarations
- **~8 words:** Documents and schemas add facts without executing tools.
- **Expanded:** Markdown, schemas, and build files contribute navigation facts through source-only parsing.

## Full content

**Part 6 of [Building Weave](/series/weave.md).**

Not every important declaration lives in compiler source. Weave also indexes structured Markdown and common schema and build families through source-only providers.

![Documents and schemas entering the navigation profile](/assets/images/articles/weave/source-only-schema-build.svg)

These providers parse files without running renderers, builds, package managers, databases, plugins, or network loaders. They emit document and declaration anchors plus retained relationships such as dependencies, generation, documentation, and embeds.

Linked schema categories publish atomically. If one changed file makes a category invalid, the previous complete facts remain available instead of exposing a partial model.

The result is still the same format-5 navigation profile. A schema operation, Markdown heading, Go declaration, and build target can all lead a query back to exact source.

[Continue to semantic changes](/articles/weave-semantic-diffs-and-impact.md)
