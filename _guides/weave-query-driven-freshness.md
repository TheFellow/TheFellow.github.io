---
title: "Freshness Belongs on Every Weave Read"
date: 2026-08-09 10:31:00 -0700
last_modified_at: 2026-08-10
excerpt: "Every query proves that its navigation facts match the current worktree and providers."
permalink: /articles/weave-query-driven-freshness/
series: weave
series_order: 2
order: 2
status: "Weave, part 2"
featured: true
icon: "branch"
accent: "#4dabf7"
topics: ["Git freshness", "Provider state", "Current evidence"]
image: /assets/images/articles/weave/fresh-query.svg
---

{% include series-notice.html %}

Weave checks freshness when a read begins. Users do not need to remember a separate indexing step, and a background process is never the authority.

![A query passing through a freshness gate](/assets/images/articles/weave/fresh-query.svg)

The gate compares current Git state, provider capabilities, configuration, and source observations with the published manifest. Changed provider units rebuild atomically before the query opens the database.

Publication matters as much as detection. A new unit and its manifest become visible together, so readers see either the previous complete generation or the next complete generation.

Caches and warm processes may reduce the cost of this check. They cannot skip it. The simple promise is that every answer describes the worktree the caller is actually using.

[Continue to language adapters](/articles/weave-language-adapters/){: .btn .btn--primary }
