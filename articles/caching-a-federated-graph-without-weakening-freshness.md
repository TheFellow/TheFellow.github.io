<!-- Generated from https://thefellow.github.io/articles/caching-a-federated-graph-without-weakening-freshness/ by scripts/generate_llm_content.py; do not edit. -->

# Caching a Federated Graph Without Weakening Freshness

Source: [https://thefellow.github.io/articles/caching-a-federated-graph-without-weakening-freshness/](https://thefellow.github.io/articles/caching-a-federated-graph-without-weakening-freshness/)

## Pyramid summary

- **~2 words:** Exact graph cache
- **~8 words:** Authoritative worktree generations select one immutable hot federation projection.
- **Expanded:** How Weave accelerates machine-wide symbol and graph queries with an immutable hot projection keyed by exact worktree generations while keeping every repository authoritative.

## Full content

**Part 5 of [Building Weave](/series/weave.md).**

A repository catalog makes cross-worktree questions possible without a hosted index. It also makes a common query expensive in a new way. Every invocation can refresh the selected worktrees, open each independent graph database, fan the same search across them, merge equivalent facts, and close them again. That is correct, but repeated symbol and relationship queries keep paying the federation cost after the underlying graphs have stopped changing.

The obvious cache is dangerous. If a machine-wide database can answer before the worktrees prove what generation they are on, it quietly becomes a second freshness authority. [Weave](https://github.com/TheFellow/weave) instead builds a disposable aggregate whose identity is derived from the exact authoritative generations it represents. The cache can make a read faster; it cannot make an old read current.

<figure class="article-figure">
  <img src="/assets/images/articles/weave/machine-aggregate.svg" alt="Each selected worktree refreshes through its authoritative local index and produces a deterministic freshness generation. Weave sorts the complete source set and hashes its identities and generations. An exact immutable aggregate hit serves hot symbol and edge queries; a miss opens the authoritative databases, rebuilds the projection under a lock, and atomically publishes it. Any cache failure falls back to federation.">
  <figcaption>Freshness flows from each worktree into the cache key. The aggregate is selected by authoritative state, never used to determine it.</figcaption>
</figure>

## Keep authority in every worktree

Catalog query execution still starts by selecting a bounded set of explicitly registered worktrees. Each selected root must exist, and each repository runs its ordinary query-driven freshness check before an aggregate is considered. A worktree that cannot refresh is excluded and marks the response partial just as it would under direct federation.

That ordering closes the most tempting shortcut. An aggregate from yesterday may contain a symbol that still looks plausible, but Weave never consults it while deciding whether today's repository is current. Git state, provider identity, configuration, dirty overlay, and per-unit fingerprints remain inputs to the local freshness manifest.

The manifest now exposes a deterministic generation digest. Publication time and diagnostics are omitted because they do not change graph facts. Repository and worktree identity, provider, commit, tree, branch state, dirty-overlay digest, complete unit set, and schema remain. Two checks of unchanged authoritative state produce the same generation; any semantic source or provider change produces a different one.

That digest is also stored inside the worktree graph. Before a supposedly current manifest can supply an aggregate generation, the freshness check opens the local database and requires its marker to match. A refresh invalidates the marker before its bounded multi-transaction writes, then installs the new generation only after the complete fact set succeeds. A crash cannot leave an old complete manifest pointing at partial new graph facts and still produce a trusted cache key.

## Name the cache from the complete source set

A single worktree generation is not enough for a federated result. The aggregate key includes every selected catalog key, repository identity, worktree identity, root, local database path, and freshness generation. Weave sorts that source set, includes both aggregate and graph schema versions, serializes the canonical projection, and hashes it.

The digest becomes an immutable generation filename. Opening a candidate validates its embedded schema, generation, source count, and complete source records against the requested set. A different selector, moved catalog, changed worktree, refreshed unit, or graph schema cannot accidentally reuse the old file.

This is intentionally stronger than a timestamp or "last updated" field. The cache is addressable only through the state it claims to represent. A missing generation is a miss. A schema mismatch is stale. Corrupt metadata is corrupt. None of those conditions is permission to return whatever rows remain readable.

## Project only the hot facts

The machine aggregate is not a copy of every worktree database. It contains retained navigation symbols, their name lookup projection, retained edges, and normalized fact-to-worktree provenance. Units, documents, source text, verbose evidence records, and freshness manifests stay with their owning repositories. The navigation profile has no per-worktree occurrences or body-token postings to copy.

That narrow projection supports the catalog operations that repeatedly need symbol search and retained graph adjacency: `symbols`, `dependencies`, `path`, `impact`, and `graph`. Exact IDs, normalized display names, stable names, providers, evidence, retained edge kinds, ranges, and document identities remain sufficient for those operations.

Other reads deliberately bypass it. [`weave context`](/articles/composing-source-rich-context-without-a-second-index.md) needs the owning worktree's document identity, declaration anchor, and current source. Compact `explore` also combines semantic anchors with a bounded ripgrep pass in the selected worktree rather than pretending that the aggregate contains source bodies. An optimization should not broaden its schema until measurement shows the extra facts are both necessary and cheaper to duplicate.

When the same semantic identity appears in more than one member, its searchable names and other fields may differ across branches or worktrees. The aggregate retains compact per-source variants, reproduces each member's ranking and truncation behavior, then merges the visible result by semantic identity. Relationships receive the same per-source treatment before equivalent edges collapse. Deterministic output still reports every repository and worktree that supplied an observed fact. Deduplication does not erase a variant or its provenance.

## Publish one complete immutable generation

On an exact hit, Weave can open the aggregate after freshness succeeds without retaining every worktree graph for query fan-out. The freshness check may open each local database long enough to validate its generation marker; the hot query itself uses the aggregate. On a miss, Weave opens the healthy authoritative databases and scans their hot facts in canonical order. Bounded batches build a new projection rather than holding the complete federation in memory.

An initial generation check does not cover a worktree changing during that scan. After ingestion, the builder releases every source database handle and re-runs freshness for each worktree. If any returned generation differs from the one that selected the destination, publication aborts. The aggregate therefore proves the source set on both sides of materialization.

Builders serialize through a small process lock. A process that waited for the lock checks for the requested generation again, because another process may have completed it. Otherwise it builds a temporary bstore database, writes source records and hot facts, records final counts and metadata, closes the database, and publishes it under the generation name. Readers never share a filename with an in-progress rebuild.

Only after the published generation opens and validates can older generation files be removed. A source-generation change therefore creates a different complete database rather than mutating the file a concurrent reader already opened.

This first implementation favors complete replacement over clever incremental reconciliation. The aggregate omits worktree documents and source-serving state, and measurements need to show that full projection rebuilds are a real bottleneck before layered shards, set reconciliation, or compaction protocols earn their complexity.

## Measure the cache honestly

The first checked-in benchmark uses eight worktrees and 5,000 total symbols. It records a useful mixed result. With all eight authoritative stores already open, a bounded symbol prefix search is 19 percent slower through the aggregate. Preserving per-source variants and reproducing federation's ordering, provenance, and truncation semantics costs more than searching those warm stores directly.

Reverse edge adjacency is 3.3 to 3.9 times faster through the aggregate and allocates about 74 percent fewer bytes. Opening the query surface and then searching improves by only about 6 percent because the required Git and freshness checks dominate the fixture. An aggregate hit still avoids holding eight database handles and locks through query execution.

The aggregate is worthwhile only where it beats already-open authoritative worktrees. Current benchmarks show the strongest benefit in reverse-edge traversal and reduced open database state; symbol search can be slower. Format-5 measurements should decide whether further projection or sharding earns its complexity.

## Fall back toward authority

Cache behavior is intentionally asymmetric. A validated hit may accelerate a query. A miss may rebuild. A build lock timeout, scan failure, revalidation mismatch, corrupt cache, or publication error produces a diagnostic and restores authoritative federation for the query. If building already released a member database, that fallback re-proves freshness before reopening it.

The fallback direction matters. Weave does not serve an older aggregate because the newest one was inconvenient to build. It also never serves a cached worktree that disappeared after registration. Missing roots are excluded before aggregate selection, so a previously cached symbol cannot leak into the partial result.

Cache failure is therefore a performance condition. Repository freshness failure is a correctness condition. Keeping those categories separate makes degradation honest: the user may receive a slower complete answer, or an explicitly partial answer when a repository cannot participate, but not a fast answer that silently belongs to another generation.

## Follow one accelerated catalog query

The resulting lifecycle is compact even though each boundary is strict:

1. Select at most the requested catalog members and verify their roots.
2. Refresh every selected worktree through its local authority and collect the deterministic manifest generation.
3. Derive the complete aggregate generation from the sorted source set and schema.
4. Open and validate the immutable projection on an exact hit.
5. On a miss, open the authoritative graphs, build and validate a complete hot projection, then publish it.
6. If acceleration fails, execute against those authoritative graphs and report the cache diagnostic.

There is still no daemon and no independently updated global index. A foreground query does the authority checks, and the aggregate remains disposable state beside the catalog. That is the useful distinction: Weave caches a proven answer space, not the right to decide what is true.
