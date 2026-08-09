<!-- Generated from https://thefellow.github.io/articles/shrinking-a-semantic-graph-without-changing-its-meaning/ by scripts/generate_llm_content.py; do not edit. -->

# Shrinking a Semantic Graph into a Navigation Index

Source: [https://thefellow.github.io/articles/shrinking-a-semantic-graph-without-changing-its-meaning/](https://thefellow.github.io/articles/shrinking-a-semantic-graph-without-changing-its-meaning/)

## Pyramid summary

- **~2 words:** Format-5 navigation
- **~8 words:** A small navigation profile keeps detail in current source.
- **Expanded:** How Weave format 5 keeps only the anchors and relationships needed to navigate back to current source.

## Full content

**Part 6 of [Building Weave](/series/weave.md).**

[Weave](https://github.com/TheFellow/weave) format 5 is a navigation index, not a compiler-event archive. Its job is to identify useful declarations, documents, and relationships, then point back to current source.

<figure class="article-figure">
  <img src="/assets/images/articles/weave/compact-storage.svg" alt="Language and content providers emit format-5 navigation facts. The index keeps documents, package and declaration anchors, and high-value dependency, implementation, test, generation, documentation, link, and embed edges. Occurrences, calls, references, containment, fields, constants, locals, and search terms stay outside the contract. Current source supplies detail after discovery.">
  <figcaption>Format 5 keeps navigation in the index and statement detail in source.</figcaption>
</figure>

## Keep one small profile

The `navigation-v1` profile retains:

- documents and declaration anchors;
- package, namespace, type, callable, test, and content identities;
- dependencies, imports, extension and implementation edges;
- tests, generation, documentation, exposure, links, and embeds; and
- compact declaration-name lookup indexes.

It omits occurrences, calls, references, definition and containment edges, fields, constants, locals, parameters, body terms, and copied source text.

## Apply the boundary everywhere

Built-in providers create navigation facts directly. External adapters receive `profile: navigation-v1` and stream the same shape. The adapter parser and storage layer project again defensively, so an older or third-party producer cannot expand the managed index.

## Recover detail from source

`weave explore` returns a few semantic anchors plus bounded ripgrep hits. `weave context` opens the selected declaration from current Git-visible source. `definition`, `graph`, `path`, `impact`, and architecture queries operate only on facts the format actually retains.

This is the complete product boundary: keep enough exact structure to navigate, keep every response bounded, and leave statement-level truth in source.
