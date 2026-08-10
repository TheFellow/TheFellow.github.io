---
title: "Inspect the Graph and Author Missing Links"
date: 2026-08-09 10:34:00 -0700
last_modified_at: 2026-08-10
excerpt: "Bounded graph views and checked-in links make navigation facts visible and reviewable."
permalink: /articles/weave-graph-inspection-and-links/
series: weave
series_order: 5
order: 5
status: "Weave, part 5"
featured: true
icon: "sitemap"
accent: "#51cf66"
topics: ["Graph inspection", "Contextual links", "Source evidence"]
image: /assets/images/articles/weave/inspectable-graph.svg
---

{% include series-notice.html %}

Navigation facts must be easy to inspect. `weave graph` resolves a target and renders a bounded neighborhood as DOT, JSON, or an interactive local explorer.

![A bounded graph with visible evidence](/assets/images/articles/weave/inspectable-graph.svg)

Each edge carries its kind and evidence. Filters, direction, depth, and result limits keep the answer focused instead of turning the command into an unbounded graph dump.

Some useful relationships cannot be derived from source alone. `weave links` edits reviewed relationships in `.weave/bridges.json`, such as a design section documenting a handler or a schema generating a client. Writes are validated, canonical, atomic, and guarded against stale interactive editors.

Derived and authored edges then flow through the same path, graph, impact, export, and architecture queries.

[Continue to source-only declarations](/articles/weave-source-only-declarations/){: .btn .btn--primary }
