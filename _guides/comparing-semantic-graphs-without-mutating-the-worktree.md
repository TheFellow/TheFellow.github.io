---
title: "Comparing Semantic Graphs Without Mutating the Worktree"
date: 2026-08-07 13:15:28 -0700
last_modified_at: 2026-08-08 13:10:00 -0700
excerpt: "How Weave compares exact Git revisions and dirty worktrees through the same provider pipeline, separates source changes from graph changes, and makes bounded impact and test claims with evidence."
permalink: /articles/comparing-semantic-graphs-without-mutating-the-worktree/
series: weave
series_order: 7
order: 11
featured: true
status: "Weave, part 7"
icon: "compare"
accent: "#ffd43b"
topics: ["Semantic diffs", "Git", "Impact analysis"]
---

{% include series-notice.html %}

`git diff` can tell me that a file moved, a line changed, or an untracked path appeared. It cannot tell me whether a normalized symbol changed, an edge disappeared, a provider-owned public surface moved, or a test became semantically downstream of the edit. A semantic index can answer those questions about its current graph, but comparing only the current database with Git history would mix two different moments and call the result a diff.

[Weave](https://github.com/TheFellow/weave) closes that gap by building an exact graph snapshot for each side through the same configured provider pipeline. It resolves the baseline and optional head to immutable Git objects, materializes historical revisions away from the user's working tree, compares normalized facts by stable identity, and exposes four bounded views: graph, API surface, reverse impact, and affected tests.

<figure class="article-figure">
  <img src="{{ '/assets/images/articles/weave/semantic-snapshot-diff.svg' | relative_url }}" alt="A Git baseline resolves to exact commit and tree objects, enters a temporary detached worktree, and runs through the configured freshness providers to produce a normalized graph snapshot. The other side is either another isolated revision or the current dirty worktree followed by a freshness recheck. Git separately provides the authoritative source-change inventory. Stable graph identities produce added, removed, and changed facts, which feed graph, API surface, reverse-impact, and evidence-backed affected-test views.">
  <figcaption>Two exact semantic snapshots and one Git-authoritative source inventory meet at a bounded diff contract. Historical indexing never checks out the user's branch.</figcaption>
</figure>

## Keep source changes and semantic changes separate

Git is the authority for additions, deletions, modifications, copies, renames, type changes, and unresolved merges. Weave asks for the null-delimited name-status form so unusual path names remain unambiguous. An explicit `--head` produces a clean revision-to-revision inventory; omitting it compares the baseline with the index, working tree, and untracked overlay that exists now.

That inventory is useful evidence, but it is not a semantic graph delta. A comment-only edit may change a source file without changing one normalized fact. A provider upgrade may change graph evidence even when a narrow file list looks stable. A rename can preserve a stable semantic identity, while a small declaration edit can replace several symbols and relationships.

The [`weave.snapshot-diff/v1`](https://github.com/TheFellow/weave/blob/main/internal/graphdiff/diff.go) contract therefore keeps `sources` beside, not inside, the graph delta. Units, documents, retained symbols, and retained navigation edges each have independent `added`, `removed`, and `changed` collections. The schema can represent occurrence changes from richer snapshots, but managed format-4 indexes retain no occurrences. A changed record keeps both before and after values under the same stable ID.

## Index the past without checking it out here

Before indexing, Weave resolves every requested revision to exact commit and tree object IDs. Human-friendly inputs remain in the response for context, but object IDs define what was actually compared. A historical side is materialized in a temporary detached linked worktree and passed to the same automatic freshness-provider construction used for the current repository.

This matters more than teaching a second parser to read Git blobs. The configured Go, .NET, Python, Rust, C++, TypeScript, JVM, Ctags, workspace, bridge, and SCIP paths already define what Weave considers authoritative semantic evidence. A lightweight historical mapper would produce facts that look comparable while following different rules.

Temporary graph state belongs to the temporary worktree. It never enters the current worktree's database, and the caller's branch never moves. Cleanup removes both the directory and Git's linked-worktree metadata after success, provider failure, or cancellation. Tests record the worktree inventory before each failing path and require it to be identical afterward.

Historical materialization also supplies an empty `core.hooksPath`, so repository post-checkout hooks do not run merely because a diff needs the past. User-configured Git checkout filters may still execute. They remain part of the developer's local Git trust and configuration boundary, not portable source truth that Weave can safely neutralize without changing checkout semantics.

If automatic providers are unavailable, historical facts are unavailable. Weave reports that boundary instead of comparing a fresh current graph with guessed or stale baseline facts.

## Identify the graph independently of its temporary home

Freshness generations include worktree identity, which is exactly right for protecting a local database but wrong as the durable identity of a historical snapshot. Materializing the same commit in two temporary worktrees can produce two generation values even when every normalized fact is identical.

The diff contract carries both. `generation` proves the exact freshness observation used on that side. `snapshot_digest` sorts the normalized public graph and hashes it with a domain-separated schema, making equivalent semantic snapshots comparable independently of their temporary paths. Commit and tree IDs prove the Git source point; the snapshot digest proves the graph produced from it.

The current dirty side needs one more guard. Weave first refreshes and exports its graph, then asks Git for the source-change inventory, then inspects freshness again. If commit, tree, dirty state, change count, or generation moved during the operation, it asks the caller to retry. A long comparison cannot silently combine a graph from one overlay with file changes from the next.

## Bound every fact family independently

Semantic diffs can become large quickly, especially after a generated package or dependency graph changes. One global limit would let a noisy symbol family consume the response before a document or edge change appeared.

Weave sorts every fact family by stable ID and applies the limit independently to its added, removed, and changed collections. It retains one internal sentinel beyond each public limit so `truncated` is an observed fact rather than an estimate. Source changes have their own bound. The same inputs therefore produce the same prefix and the same truncation signal.

The CLI exposes that contract through `weave diff graph --base REV [--head REV]`. Plain text starts by naming both exact sides, then lists source and graph changes. JSON returns the versioned snapshot-diff result directly. The graph view also projects changed symbols and edges into a compact, stable-ID `transitions` set whose status is added, removed, or changed.

The local explorer exposes that same result through a bounded, same-origin `api/diff` endpoint. It validates revisions, edge kinds, depth, result, and edge bounds before forwarding one ordinary `diff graph` invocation through the application boundary. Its pinned d3-graphviz renderer already keys nodes and edges across animated renders, so the transition set supplies browser-ready enter, update, and exit identities without a second graph comparison implementation.

## Report API evidence without guessing compatibility

A normalized symbol name is not a cross-language compatibility classifier. Removing a public-looking method might be source-breaking, binary-breaking, both, or neither depending on language and provider semantics that the core does not own.

`weave diff api` projects provider-owned unit surface fingerprints instead. It can state exactly that a provider surface was added, removed, or changed, retain the opaque before and after fingerprints, and label the evidence `provider-surface-fingerprint`. Compatibility remains `unknown`.

That word is an important feature. A future language provider can supply a specific ABI or source-compatibility classifier, but the common graph layer does not upgrade evidence merely because a label would be convenient. If no provider-owned surface changed, the response explains that compatibility was not inferred from symbol names.

## Reuse impact traversal, then explain selected tests

Graph changes become useful when they seed the existing reverse-impact traversal. Added and changed retained symbols, navigation edges, units, and documents contribute stable IDs that exist in the head snapshot. Git-changed paths contribute current document roots. Removed facts remain visible in the graph delta, and their stable IDs can still seed relationships that survive in the head, but disconnected removed-only facts cannot be traversed through a graph where they no longer exist. The result says so diagnostically.

`weave diff impact` uses the same retained navigation edge kinds, depth bound, edge bound, ordering, and truncation behavior as ordinary impact queries. There is no second walker whose semantics can drift just because the roots came from a comparison. Statement-level call and reference changes are deliberately outside this managed snapshot contract.

`weave diff tests` is a projection of that impact result, not a new reachability claim. A selected test carries a reason and evidence. An explicit `tests` relationship keeps its edge ID and evidence. A provider-classified test symbol keeps provider evidence. Go declarations recognized through `_test.go` plus `Test`, `Benchmark`, or `Fuzz` naming are labeled syntactic. Empty or partial provider output is not promoted into a completeness promise.

## Make time an explicit part of the query

A semantic diff is not one graph with colored nodes. It is two Git identities, two freshness observations, two normalized snapshot identities, a separate source inventory, and a set of bounded projections with different evidence rules.

Keeping those pieces explicit makes the command more useful and less magical. Historical indexing reuses the real providers. Dirty comparisons detect races. Stable IDs preserve deterministic change records. API output refuses to guess. Impact reuses one traversal contract. Test selection explains why each result is present.

That fidelity has a visible cost. Historical graphs are rebuilt rather than read from a permanent snapshot cache, and the current implementation materializes complete snapshots before bounding its output. A large ref-to-ref comparison can therefore be expensive. The contract leaves room for a measured streaming comparison later without retaining temporary databases or changing what callers receive.

That is the standard Weave keeps returning to: make the evidence and its limits part of the result, then let richer interfaces build on the same honest core.
