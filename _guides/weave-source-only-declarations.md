---
title: "Index Declarations Without Executing the Repository"
date: 2026-08-09 10:35:00 -0700
last_modified_at: 2026-08-10
excerpt: "Markdown, schemas, and build files contribute navigation facts through source-only parsing."
permalink: /articles/weave-source-only-declarations/
series: weave
series_order: 6
order: 6
status: "Weave, part 6"
featured: true
icon: "braces"
accent: "#20c997"
topics: ["Schema indexing", "Build manifests", "Source evidence"]
image: /assets/images/articles/weave/source-only-schema-build.svg
---

{% include series-notice.html %}

Not every important declaration lives in compiler source. Weave also indexes structured Markdown and common schema and build families through source-only providers.

![Documents and schemas entering the navigation profile](/assets/images/articles/weave/source-only-schema-build.svg)

These providers parse files without running renderers, builds, package managers, databases, plugins, or network loaders. They emit document and declaration anchors plus retained relationships such as dependencies, generation, documentation, and embeds.

Linked schema categories publish atomically. If one changed file makes a category invalid, the previous complete facts remain available instead of exposing a partial model.

The result is still the same format-5 navigation profile. A schema operation, Markdown heading, Go declaration, and build target can all lead a query back to exact source.

[Continue to semantic changes](/articles/weave-semantic-diffs-and-impact/){: .btn .btn--primary }
