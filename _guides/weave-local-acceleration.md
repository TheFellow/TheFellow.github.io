---
title: "Keep Acceleration Optional"
date: 2026-08-09 10:38:00 -0700
last_modified_at: 2026-08-10
excerpt: "Watch, sessions, and the transient broker reuse state without weakening freshness."
permalink: /articles/weave-local-acceleration/
series: weave
series_order: 9
order: 9
status: "Weave, part 9"
featured: true
icon: "watch"
accent: "#fab005"
topics: ["Watch mode", "Query sessions", "Local acceleration"]
image: /assets/images/articles/weave/resident-query-session.svg
---

{% include series-notice.html %}

Weave's fast paths reuse authoritative local state. They do not create a second consistency model.

![Several queries sharing one bounded local session](/assets/images/articles/weave/resident-query-session.svg)

`weave watch` is an optional foreground warmer. `weave session` gives a host an explicit framed query process. On Unix, a transient per-worktree broker can amortize startup for ordinary bounded reads and reaps itself when idle.

Every path still applies the freshness contract before answering. Maintenance and mutation commands drain resident readers before taking ownership, and callers can disable the broker when one process per command is preferable.

This is the final shape of format 5: a small disposable index, authoritative source, and optional acceleration that can always be removed without changing meaning.

[Return to the Weave project](/projects/weave/){: .btn .btn--primary }
