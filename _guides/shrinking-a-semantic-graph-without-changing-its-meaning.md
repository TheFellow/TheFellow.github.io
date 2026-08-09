---
title: "Shrinking a Semantic Graph into a Navigation Index"
date: 2026-08-07 12:45:59 -0700
last_modified_at: 2026-08-09 10:00:00 -0700
excerpt: "How Weave format 5 keeps only the anchors and relationships needed to navigate back to current source."
permalink: /articles/shrinking-a-semantic-graph-without-changing-its-meaning/
series: weave
series_order: 6
order: 10
featured: true
status: "Weave, part 6"
icon: "layers"
accent: "#22b8cf"
topics: ["Storage design", "Code navigation", "Performance"]
---

{% include series-notice.html %}

[Weave](https://github.com/TheFellow/weave) format 5 is a navigation index, not a compiler-event archive. Its job is to identify useful declarations, documents, and relationships, then point back to current source.

<figure class="article-figure">
  <img src="{{ '/assets/images/articles/weave/compact-storage.svg' | relative_url }}" alt="Language and content providers emit format-5 navigation facts. The index keeps documents, package and declaration anchors, and high-value dependency, implementation, test, generation, documentation, link, and embed edges. Occurrences, calls, references, containment, fields, constants, locals, and search terms stay outside the contract. Current source supplies detail after discovery.">
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
