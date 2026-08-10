---
title: "Federate Fresh Worktrees"
date: 2026-08-09 10:37:00 -0700
last_modified_at: 2026-08-10
excerpt: "Cross-repository queries refresh selected worktrees before using a disposable aggregate."
permalink: /articles/weave-federated-queries/
series: weave
series_order: 8
order: 8
status: "Weave, part 8"
featured: true
icon: "modules"
accent: "#f06595"
topics: ["Federated queries", "Fresh worktrees", "Machine aggregates"]
image: /assets/images/articles/weave/machine-aggregate.svg
---

{% include series-notice.html %}

Weave can query a bounded set of cataloged repositories without making a hosted graph authoritative. Each selected worktree passes its normal freshness gate first.

![Fresh worktree generations forming a machine aggregate](/assets/images/articles/weave/machine-aggregate.svg)

The generation identities form a deterministic aggregate key. A matching immutable aggregate can answer the query quickly; otherwise Weave builds one or falls back to authoritative federation over the refreshed member databases.

Aggregates live outside Git and are safe to delete. Missing or unhealthy members are reported as partial results rather than hidden.

Source context remains repository-local. Federation helps choose the repository and target, then `weave context` reopens source under that repository's own bounds and freshness rules.

[Continue to local acceleration](/articles/weave-local-acceleration/){: .btn .btn--primary }
