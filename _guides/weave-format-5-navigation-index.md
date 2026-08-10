---
title: "Weave Format 5 Is a Navigation Index"
date: 2026-08-09 10:30:00 -0700
last_modified_at: 2026-08-10
excerpt: "Format 5 keeps the few semantic facts needed to reach current source quickly."
permalink: /articles/weave-format-5-navigation-index/
series: weave
series_order: 1
order: 1
status: "Weave, part 1"
featured: true
icon: "storage"
accent: "#22b8cf"
topics: ["Navigation index", "Source discovery", "Compact storage"]
image: /assets/images/articles/weave/compact-storage.svg
---

{% include series-notice.html %}

Weave format 5 is deliberately small. It stores documents, declaration anchors, and relationships that help a person or coding agent choose where to look next.

![A compact index pointing back to source](/assets/images/articles/weave/compact-storage.svg)

Providers emit one `navigation-v1` profile. The profile retains dependencies, imports, implementations, tests, generation, documentation, authored links, and embeds. It does not retain occurrences, calls, references, locals, fields, containment, or body terms.

That boundary keeps indexing and queries practical. A result identifies a useful package, declaration, document, or relationship. Detailed investigation then returns to current source through `weave explore` and `weave context`.

The database is disposable and stays outside Git. Its job is navigation, not a second copy of the repository.

[Explore the Weave project](/projects/weave/){: .btn .btn--primary }
[Continue to freshness](/articles/weave-query-driven-freshness/){: .btn }
