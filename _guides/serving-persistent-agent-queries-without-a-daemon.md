---
title: "Reusing Local Query State Without Installing a Daemon"
date: 2026-08-08 01:46:00 -0700
last_modified_at: 2026-08-08 14:20:00 -0700
excerpt: "How Weave serves bounded reads through an explicit NDJSON session or an idle-reaping per-worktree broker while preserving one-shot freshness and maintenance paths."
permalink: /articles/serving-persistent-agent-queries-without-a-daemon/
series: weave
series_order: 14
order: 18
featured: true
status: "Weave, part 14"
icon: "terminal"
accent: "#20c997"
topics: ["Coding agents", "Developer tools", "Protocols"]
---

{% include series-notice.html %}

A correct one-shot CLI still repeats process startup, freshness inspection, schema validation, database open, and dictionary work during a research conversation. The first Weave optimization made that ownership explicit with `weave session`, a foreground NDJSON subprocess controlled by one agent host.

The current implementation keeps that protocol and adds a smaller default optimization on supported Unix platforms: ordinary bounded local reads can reuse an ephemeral per-worktree broker. The broker is started on demand, is never installed or supervised, and exits after one minute without an accepted client or active request.

<figure class="article-figure">
  <img src="{{ '/assets/images/articles/weave/resident-query-session.svg' | relative_url }}" alt="Bounded local read commands either enter an explicit foreground NDJSON session or connect to an on-demand per-worktree Unix-socket broker. Both reuse the same resident application service and query normalization. The broker accepts only matching worktree identity and protocol frames, drains before maintenance or mutation, and exits after one idle minute. The ordinary freshness manager and one-shot fallback remain authoritative.">
  <figcaption>Persistence is a local latency optimization around the existing application boundary, not another indexing authority.</figcaption>
</figure>

## Keep the explicit session

`weave session` remains useful for an agent host that already owns a child process. It accepts newline-delimited `weave.query-session/v1` requests on stdin and writes one response frame per request on stdout.

```sh
printf '%s\n' \
  '{"protocol":"weave.query-session/v1","id":"discover","command":"explore","arguments":["menu publication persistence"]}' \
  '{"protocol":"weave.query-session/v1","id":"context","command":"context","arguments":["example.com/project/menu.Service.Publish"]}' \
  | weave session
```

Requests map to the same application invocations as the CLI. The session accepts bounded local research operations such as symbols, compact explore, context, definition anchors, dependencies, paths, impact, and graphs. It rejects maintenance, mutation, catalog, adapter, index, full-export, and the removed posting-dependent workspace operations.

Every frame has a fixed maximum size, one request ID, validated command arity, bounded limits, traversal depth, edge counts, source lines, and source bytes. Removed statement-level commands such as `references`, `callers`, and `callees` are not part of the session surface because the navigation profile does not contain their facts.

## Add an ephemeral broker for ordinary commands

An explicit session requires its caller to manage a stream. The local broker lets normal commands reuse the resident path without changing their text or JSON interface. A client discovers a user-private per-worktree endpoint and sends one `weave.local-broker/v1` request containing the exact repository identity and a normalized bounded invocation.

The first client starts the current Weave executable. A cross-process startup lock prevents duplicate brokers. The broker accepts only bounded local read queries, validates protocol and worktree identity before execution, limits frames to 16 MiB, and serves each request through the same resident application service. Catalog queries stay outside it.

`WEAVE_NO_BROKER=1` disables the optimization and asks an existing broker to shut down. Windows currently keeps the one-shot path. If a safe broker endpoint cannot be established, the client falls back to ordinary local execution instead of making the optimization a prerequisite.

## Preserve maintenance boundaries

Index refresh, initialization, status, garbage collection, architecture mutation, link edits, adapter work, `watch`, and an explicit `session` require a different ownership boundary. Before those operations begin, the application asks an existing broker to stop accepting work, drains active requests, closes its database, and removes its endpoint. It does not start a broker merely to shut one down.

This keeps ambiguous retries away from mutation. Once a request reached a broker, a transport failure is not replayed as a possibly mutating one-shot action. Remote application errors remain authoritative. Only failure to reach or safely start the read broker falls back before the request is accepted.

## Keep freshness authoritative

Neither persistent shape decides what is current. The resident service uses the same query-driven freshness manager as one-shot execution. A background exact Git observation can mark a generation stale; the next request crosses the ordinary close, refresh, publish, and reopen boundary before answering. Current-source reads keep their own path, encoding, hash, range, race, and byte checks.

Per-worktree and aggregate queries now use bstore's shared read-only mode after freshness is established, while writers remain exclusive. The broker amortizes process, schema, and dictionary startup; it does not make the database writable by many clients or create a second publication path.

## Separate latency work from payload work

The original session experiment measured a 0.379 ms warm median after a 1,453.892 ms first request in one 20-request local sample, compared with 751.974 ms for one one-shot call. That sample justified reusing startup state, not treating a resident process as the product.

It also exposed a different problem: the old eight-focus exploration response still occupied tens of kilobytes because it repeated graph dossiers. The later progressive-discovery work solved that at the query boundary. Its measured format-4 fixture returned a representative 3,157-byte first-stage response and fetched exact context only for a selected anchor.

These optimizations compose cleanly because they solve different costs. The broker makes repeated commands cheaper to start. The navigation projection makes the database smaller. Progressive discovery makes agent responses smaller. Freshness and current source remain shared correctness boundaries underneath all three.
