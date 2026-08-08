<!-- Generated from https://thefellow.github.io/articles/serving-persistent-agent-queries-without-a-daemon/ by scripts/generate_llm_content.py; do not edit. -->

# Serving Persistent Agent Queries Without a Daemon

Source: [https://thefellow.github.io/articles/serving-persistent-agent-queries-without-a-daemon/](https://thefellow.github.io/articles/serving-persistent-agent-queries-without-a-daemon/)

## Pyramid summary

- **~2 words:** Resident agent queries
- **~8 words:** One foreground owner keeps bounded graph queries warm and fresh.
- **Expanded:** How Weave keeps one local graph handle hot behind a bounded NDJSON session, moves exact Git observation off the request path, and preserves its authoritative refresh and source checks without installing a daemon.

## Full content

**Part 14 of [Building Weave](/series/weave.md).**

A correct one-shot CLI can still be the wrong shape for a long agent session. Every invocation starts a process, observes Git, opens bstore, validates its schema, and hydrates hot dictionaries before answering one bounded query. An IDE keeps its project services alive because navigation is a conversation, not a sequence of unrelated cold starts.

Weave cannot improve that path by pretending its embedded database supports concurrent owners. bstore opens the worktree index read/write and permits one owning process. [Weave](https://github.com/TheFellow/weave) makes that constraint the center of `weave session`: one foreground child owns one database, serializes bounded read requests, observes source state in the background, and releases everything when its client closes the stream.

<figure class="article-figure">
  <img src="/assets/images/articles/weave/resident-query-session.svg" alt="An agent host starts a foreground weave session and exchanges versioned NDJSON requests and responses over standard input and output. The first valid request runs authoritative freshness and opens one bstore handle. Warm requests reuse the handle and dictionaries. A background exact Git observer marks a pending change; the next request closes the database, uses the ordinary provider refresh pipeline, reopens the published generation, and answers. EOF or cancellation closes the owner, while maintenance, mutation, and catalog operations stay outside the session.">
  <figcaption>One client-owned process is the explicit database owner. Warm queries reuse it; a detected source change crosses the same close, authoritative refresh, and reopen boundary as ordinary commands.</figcaption>
</figure>

## Make the long-lived owner explicit

`weave session` is a foreground subprocess, not an installed daemon. The client starts it in the repository it wants to query, writes one UTF-8 JSON object per line to stdin, reads one response per line from stdout, and closes stdin when finished. There is no socket discovery, PID file, hook, durable session record, or second index authority.

```console
printf '%s\n' \
  '{"protocol":"weave.query-session/v1","id":"research","command":"explore","arguments":["where is publish authorization enforced"],"limit":6}' \
  '{"protocol":"weave.query-session/v1","id":"callers","command":"callers","arguments":["Module.Publish"],"limit":25}' \
  | weave session
```

Stdout is protocol-only. The request ID correlates each frame, and the protocol name makes incompatible semantics visible. A successful frame contains the ordinary `weave.query/v1` application response. An invalid request or failed query returns a typed error frame without ending the stream, allowing the client to correct one call while retaining the warm process.

## Bound the wire before executing a query

The session accepts the local read operations agents use for research: symbols, context, explore, definitions, references, callers, callees, dependencies, paths, impact, graphs, and workspace navigation. Every request maps to the existing application invocation and its limits for results, traversal depth, edges, relationship sections, source lines, and source bytes.

One line is limited to 1 MiB, an ID to 128 bytes, source output to at most 4 MiB, and graph traversal to explicit ceilings. Unknown fields, unsupported protocols and commands, unknown edge kinds, incorrect argument counts, and invalid bounds fail before application execution. An oversized frame terminates the process because its next record boundary cannot be recovered safely. Error messages are converted to valid UTF-8 and capped at 8 KiB before they enter a frame.

Maintenance, mutation, indexing, verification, compaction, full export, authored-link changes, adapter management, and catalog queries are deliberately absent. Those operations may open storage independently, replace derived state, or require a different ownership model. The client closes the session and uses the one-shot command instead.

## Pay the cold path once

The process does not open bstore merely because it started. Its first valid database-backed request performs the ordinary authoritative freshness check, opens the current worktree database, and records the resulting observation and freshness status. Later local requests reuse that handle, its storage pages, and its in-memory intern dictionary.

Requests are serialized under one owner. This is not a claim that bstore became a multi-reader server. Another Weave process targeting the same worktree cannot open the file while the session owns it; it waits for the existing bounded timeout and then fails. The correct client behavior is to route its supported research queries through the resident stream and close it before launching maintenance or another owner.

EOF, cancellation, or process termination closes the database. Closing is idempotent, stops the observer, waits for it to finish, and releases the file before returning. Tests prove that a second bstore open fails during ownership and succeeds after the resident closes.

## Move observation off the warm request path

[Query-driven freshness](/articles/keeping-a-semantic-index-fresh-without-a-daemon.md) remains authoritative, but running a complete exact Git observation synchronously before every warm query would preserve much of the cold overhead. After the first request, the resident starts a background observer at the same bounded interval used by optional watch warming.

An unchanged observation leaves the open handle alone. A changed or non-current observation becomes pending state. Before answering the next request, the resident closes the database, invokes the ordinary freshness manager, observes the published state, and opens the new generation. There is no resident-only provider pipeline and no refresh against an open file.

Detection is asynchronous, so a graph-only request can briefly see the preceding generation before the observer notices an edit. Source-rich responses retain a stronger immediate guard: they reopen the current Git-visible file and compare its identity and hash on every request. A changed file is reported as changed rather than paired with stale graph coordinates.

Observation failures also remain visible. The resident records the failure and returns it through the next valid query instead of silently continuing forever on a generation it can no longer prove current.

## Measure the resident shape directly

One local macOS run against a rebuilt Mixology storage-v3 index compared `symbols Readiness --limit 5` as an ordinary CLI command with 20 identical requests sent through one foreground session:

| Path | Latency |
| --- | ---: |
| One-shot CLI | 751.974 ms |
| Session first request | 1,453.892 ms |
| Session warm median | 0.379 ms |
| Session warm range | 0.275–2.193 ms |

This is one latency sample, not a throughput distribution. It demonstrates the intended lifecycle rather than a universal speed ratio: the first session request pays freshness and open costs, while serialized warm requests reuse one handle and its dictionaries.

The same run tested the less glamorous half of the contract. An ordinary CLI process failed with the bounded `inspect database schema: timeout` error while the resident owned bstore. After EOF closed the session, the identical command succeeded. The single-owner constraint is therefore observable at the process boundary and the file is released at the client-owned lifetime boundary.

## Keep the application boundary shared

The resident service did not duplicate every query. The ordinary local application path was split so one-shot commands can open and close a database around `executeDatabase`, while the resident supplies its already-owned handle to the same function. Human text, CLI JSON, NDJSON session frames, and a future adapter therefore consume the same application semantics.

The wire is language-neutral for the same reason. A query can return facts produced by Go, Roslyn, FSharp.Compiler.Service, rust-analyzer, SCIP, structured content, or an authored declaration without encoding those producers into the session lifecycle. Provider and evidence metadata remain in the normal response.

MCP remains a possible thin facade over this boundary, not a second implementation. A future local broker could multiplex clients through one owner, and a resident catalog service could hold an aggregate with a different lifecycle. Neither is implied by this foreground contract. The useful increment is smaller and more honest: one client can keep its existing local graph hot across a research conversation without installing a daemon or weakening freshness.
