<!-- Generated from https://thefellow.github.io/articles/keeping-a-semantic-index-fresh-without-a-daemon/ by scripts/generate_llm_content.py; do not edit. -->

# Keeping a Semantic Index Fresh Without a Daemon

Source: [https://thefellow.github.io/articles/keeping-a-semantic-index-fresh-without-a-daemon/](https://thefellow.github.io/articles/keeping-a-semantic-index-fresh-without-a-daemon/)

## Pyramid summary

- **~2 words:** Fresh indexes
- **~8 words:** Query-driven refresh keeps semantic evidence aligned with live Git state.
- **Expanded:** How Weave combines Git state, provider-owned semantic units, bounded graph replacement, and manifest publication so every query observes current evidence.

## Full content

**Part 1 of [Building Weave](/series/weave.md).**

A code index becomes dangerous at the moment it is convincing and wrong. A definition from the checkout before the last edit, a dependency path from the previous branch, or an impact result built with a different compiler configuration looks precise enough to trust. That makes stale semantic evidence worse than an honest text search.

[Weave](https://github.com/TheFellow/weave) makes freshness part of the read path for its automatic providers. A query inspects the current Git worktree, compares it with the last completely published semantic inventory, refreshes changed compilation units when necessary, and only then opens the graph for the requested operation. No daemon or hook is required to preserve that contract.

```text
$ weave explore how request handling reaches persistence
index: refreshed 3 changed paths

symbol  service.Handle  internal/service/handler.go:24
        next: weave context "example.com/project/service.Handle"
source  internal/api/login.go:42  service.Handle(ctx, request)
```

The refresh notice goes to stderr and the answer goes to stdout. A person sees why the first query took additional work, while a script can consume clean results or request the versioned JSON envelope. The important behavior is less visible: Weave does not open the query database until the freshness decision has completed.

<figure class="article-figure">
  <img src="/assets/images/articles/weave/fresh-query.svg" alt="A Weave query first inspects Git and compares a complete freshness manifest. A current index proceeds directly to a bounded graph query. A stale index refreshes compiler and declared-fact providers, validates and replaces complete semantic units, publishes the manifest, then runs the same query.">
  <figcaption>Freshness is a gate in front of every database-backed query. The manifest is published after the graph, so an interrupted refresh remains observably stale.</figcaption>
</figure>

## Freshness has a semantic identity

File modification times are not enough to establish that an index matches a checkout. A branch can change while files retain timestamps. A compiler or interpreter upgrade can change resolution without changing source. Build tags, target frameworks, workspace files, generated inputs, and the installed adapter can all change the facts a semantic provider emits.

Weave starts with Git's own description of the worktree. [`repository.Discover`](https://github.com/TheFellow/weave/blob/main/internal/repository/git.go) asks Git for the root, absolute Git directory, common directory, object format, remote identity, and the correct derived-data path. It does not assume that `.git` is a directory, which matters for linked worktrees. [`Repository.Inspect`](https://github.com/TheFellow/weave/blob/main/internal/repository/git.go) then records:

- the current commit and tree;
- the branch, or detached state;
- every tracked, untracked, renamed, deleted, and conflicted path in the overlay;
- a content hash for each live changed path.

That state is compared with a [freshness manifest](https://github.com/TheFellow/weave/blob/main/internal/freshness/freshness.go) containing the stable repository and worktree identities, the complete provider identity, the Git state, an overlay digest, and the provider-owned compilation-unit inventory. Each unit can contribute a semantic input fingerprint, a public-surface fingerprint, and an inventory digest.

The distinction between those fingerprints is useful. Editing a function body changes the local facts for its compilation unit. Changing an exported declaration can alter the semantic context of dependent units. Changing only the order of emitted facts should not imply a different inventory. The provider decides its smallest sound invalidation boundary, while the freshness manager decides whether the complete published result still describes the checkout.

## Every read passes through the same gate

Weave's CLI is a thin presentation layer over [`application.Local`](https://github.com/TheFellow/weave/blob/main/internal/application/application.go). Database-backed commands such as `symbols`, `explore`, `context`, `definition`, `dependencies`, `path`, `impact`, `graph`, `export`, and `verify` begin by calling `Freshness.Ensure`. `status` uses the read-only inspection path because its job is to report currency, not to change it.

The manager follows a short sequence:

1. Discover the repository and inspect the current Git state.
2. Read the last complete manifest and compare repository, worktree, Git, and provider identities.
3. Return immediately when the manifest and graph are current.
4. Otherwise acquire a repository-scoped writer lock with owner diagnostics.
5. Inspect again, because another invocation may have refreshed while this one waited.
6. Ask the semantic providers for complete replacement batches and their resulting inventories.
7. Validate and store the batches, then publish the new manifest.
8. Open the resulting database and execute the original bounded query.

The second inspection is small but important. Two shells can discover the same stale state at once. The first acquires the lock and refreshes. When the second gets the lock, it sees the completed manifest and avoids repeating the work.

Hooks and watch processes can eventually make that path warmer, but they cannot be the source of truth. Hooks can be absent, disabled, or skipped; a daemon can stop. The query remains the one moment when Weave must prove that the answer and worktree agree.

## Providers own complete semantic units

Weave normalizes facts from several semantic worlds. The always-on workspace provider inventories Git-visible paths and extracts structured document, section, link, asset, route, topic, series, and code-fence facts without executing a renderer. The native Go provider uses `go/packages` and `go/types`. The optional .NET process uses Roslyn and MSBuild for C#, and FSharp.Compiler.Service for F#. The optional Python process uses CPython's parser and compiler symbol table for exact lexical binding facts while labeling imports `declared` and calls `syntactic`. Rust-analyzer, `scip-clang`, `scip-typescript`, and `scip-java` supply compiler-resolved Rust, C/C++/CUDA, TypeScript/JavaScript, and Java/Kotlin facts through bounded process adapters. Runtime, compiler, configuration, and toolchain probes participate in freshness so an environment change cannot silently reuse an older inventory. A checked-in [relationship file](https://github.com/TheFellow/weave/blob/main/docs/declared-bridges.md) contributes reviewed connections that no single compiler can establish.

The workspace provider has a deliberately different failure boundary. Malformed, non-UTF-8, or oversized structured content retains exact file-topology facts and publishes a bounded diagnostic with the manifest, so one prose file cannot make compiler queries unavailable. A transient read or identity race still aborts the refresh. Persisting the first kind and retrying the second keeps stable source limitations distinct from an unsafe snapshot.

The [`CompositeProvider`](https://github.com/TheFellow/weave/blob/main/internal/freshness/composite.go) gives each active producer an owner name and a view of only its previous units. It rejects duplicate owners and rejects a semantic unit claimed by two providers. If an installed provider disappears, the composite result explicitly removes its former units instead of leaving their facts behind.

That ownership prevents a subtle failure. Suppose the Go provider refreshes its package inventory while the workspace and process providers are unchanged. If absence from the Go result meant global deletion, a correct Go refresh could erase structured content or facts from another language. Provider-scoped inventories make omission meaningful only inside the producer that owns the unit.

Explicit SCIP import follows a separate lifecycle. It accepts a bounded compiler-backed snapshot, preserves inventories from other SCIP producers, and replaces only the importing producer's units. It does not yet know how to rerun that producer before a query, so the user must reimport changed output. Keeping that limitation explicit is better than pretending an imported snapshot is a live provider; a future producer contract can join the freshness path once it can describe how its inputs and executable identity change.

Each returned [`graph.UnitFacts`](https://github.com/TheFellow/weave/blob/main/internal/graph/model.go) is complete for one replacement boundary. A provider can emit its unit, documents, symbols, occurrences, and edges. Validation checks ownership, stable identifiers, UTF-8, source ranges, evidence classes, edge kinds, and duplicate facts before persistent state changes. Format 4 then projects that rich provider output into retained documents, declaration anchors, and high-value navigation edges before storage. Occurrences, statement-level calls and references, and noisy declaration kinds do not become durable managed-index facts.

## Publish completeness after the graph

The graph lives in a bstore database with indexed adjacency in both directions. Replacing a semantic unit deletes the facts owned by that unit and inserts its complete new batch in one storage transaction. Readers therefore observe either the old unit or the new unit, never half of each.

Large compiler universes add another constraint. Hundreds of thousands of facts should not be held in one enormous Bolt transaction. [`ReplaceUnitsIncremental`](https://github.com/TheFellow/weave/blob/main/internal/storage/storage.go) validates the complete refresh result first, then applies bounded groups while preserving atomic replacement at unit granularity.

That introduces an interval in which several new units may be stored before the complete refresh has finished. The manifest closes the correctness gap. [`Manager.Ensure`](https://github.com/TheFellow/weave/blob/main/internal/freshness/freshness.go) writes it only after every bounded replacement succeeds and the database closes cleanly. If the process stops earlier, the old manifest cannot certify the partially updated graph. The next query observes the mismatch and deterministically reapplies the complete provider result before reading.

The ordering is the contract:

```text
validate complete result
  -> replace complete units in bounded transactions
  -> close graph database
  -> atomically publish complete manifest
  -> answer query
```

Publishing the manifest first would invert that guarantee. A crash could leave a current-looking manifest beside an incomplete graph, which is exactly the silent stale-answer state the lifecycle is designed to prevent.

## Measure the complete path

The bounded publication path came from a real failure, not an estimated future scale. Weave's first [repository-scale baseline](https://github.com/TheFellow/weave/blob/main/.ai/benchmarks/2026-08-06-repositories.md) indexed Mixology, arch-lint, cedar-dotnet, and FKYeah in isolated local clones. The original Mixology cold index exceeded the harness's 300-second bound. Its Go graph contained 165 compilation units and 433,523 document, symbol, occurrence, and edge facts, enough for a single storage transaction to consume multiple gigabytes of memory and miss the same bound.

Three corrections addressed different sources of work. A required-method index pruned concrete type and interface pairs that could not possibly match while retaining `go/types.Implements` as the final authority. Bounded transactions kept graph publication proportional to complete semantic units. Fixed-size, domain-separated SHA-256 identities replaced recursively encoded Go fact IDs.

The adjacent measured run made the first correction concrete:

| Repository | Cold index | Current empty lookup | Graph database |
| --- | ---: | ---: | ---: |
| go-modular-monolith | 37.785 s | 0.536–0.610 s | 1.11 GB |
| arch-lint | 2.610 s | 0.531–0.549 s | 16.8 MB |

The current lookup included Git inspection, manifest and provider comparison, database open, and a bounded symbol search with no match. Compact identities reduced the Mixology database from 7.54 GB to 1.11 GB, an 85.3 percent reduction. That historical result exposed the next problem rather than finishing the storage work.

The format-4 navigation projection later changed what the managed database retains. On a 3,019,968-byte Go repository, it reduced a 1,034,616,832-byte format-3 database to 16,777,216 bytes, or 5.56 times source size. A forced refresh completed in 10.2 seconds. The projection retains documents, declaration anchors, and navigation relationships while omitting occurrences, statement-level calls and references, fields, constants, locals, and broad body-token postings. Freshness still governs the complete provider inventory even though persistence is now deliberately smaller than provider output.

The unsuccessful repositories exercised the other half of the contract. Cedar's large C# solution exceeded the native adapter's four-minute full-refresh limit. FKYeah selected .NET 10 F# targets that the adapter's original .NET 9 host could not evaluate. Neither run published a manifest or a partial semantic inventory. Success became faster, while failure stayed observable and replayable.

The FKYeah result also gave the next change a precise target. The adapter now runs on .NET 10, keeps the prebuilt reference outputs FSharp.Compiler.Service requires, and indexes dependents before referenced F# projects so design-time cleanup cannot remove a dependency output before its consumers have used it. A genuine FKYeah graph now completes. The Cedar timeout remains an honest limit of the current full-refresh adapter rather than being hidden behind partial facts.

A later [twelve-repository indexing soak](/articles/turning-cross-repository-soaks-into-indexing-contracts.md) closed that Cedar result and broadened the measurement contract. Every candidate ran in an isolated prepared clone, indexed offline, answered five current no-change queries, verified, exported, and left its source status unchanged. Cedar completed in 51.338 seconds and FKYeah in 132.146 seconds. The same matrix exposed recursive Go dependency syntax retention, nested .NET and Rust project roots, repeated Rust SCIP symbols, and divergent adapter environments. Those findings belong to freshness because a provider inventory is complete only when it identifies the correct build boundary and can reproduce it under the same bounded process inputs.

An installed-binary smoke covered the incremental half of that lifecycle. One comment added inside an isolated go-riblt clone produced a dirty generation with one changed path, refreshed in 2.990 seconds at 142 MiB peak RSS, and passed `weave verify`. The original source repository remained clean. Cold completeness and ordinary edit-driven replacement therefore use the same observable publication boundary.

## Derived state follows the worktree

The detailed graph and manifest live at the location returned by `git rev-parse --git-path weave`, normally `.git/weave`. Git resolves a distinct path for each linked worktree, so a dirty overlay in one checkout does not claim freshness for another. The cross-repository catalog lives in the platform user data directory because it describes explicitly registered local worktrees rather than one repository snapshot.

This placement makes recovery direct. Source, build configuration, checked-in bridge declarations, and provider versions are authoritative; the database is not. Schema mismatch, physical corruption, or a failed verification can be reported as a rebuildable derived-state problem. Reindexing reconstructs the semantic graph without asking source control to carry opaque binary history.

The same rule applies to federation. A catalog query refreshes every selected member before opening its database. A repository that cannot refresh is excluded and reported, while healthy repositories still return bounded results with provenance. Cross-repository breadth does not weaken the local freshness contract.

## Bound the answer as well as the refresh

Current evidence can still be impractical if one broad name or highly connected symbol consumes unbounded work. Weave's queries carry result and traversal limits into the graph layer. Symbol lookup has a requested limit. Path and impact traversal bound depth, visited nodes, and examined edges. Canonical ordering makes the same graph and bounds produce the same answer, and a truncation flag tells the caller when a boundary stopped the search.

That behavior matters most for automated consumers. An agent can ask a precise question, receive exact provider and source evidence in `weave.query/v2`, and know whether the result is complete. Compact discovery also has a 12 KiB encoded ceiling, so a small result count cannot conceal an oversized payload.

The output streams preserve the same separation of concerns:

| Channel | Contents |
| --- | --- |
| stdout | Requested text result or versioned JSON envelope |
| stderr | Refresh notices, excluded catalog members, and diagnostics |
| exit status | Usage, policy, integrity, or execution outcome |

Successful empty text results stay silent. A query that finds nothing and a query that failed are therefore distinct without adding decorative output a script must discard.

## Follow the lifecycle in a checkout

The behavior is easiest to see by letting ordinary development invalidate the graph:

```sh
# Establish the first complete inventory.
weave index
weave status

# Discover compact anchors and source pointers from the current index.
weave explore how request handling reaches persistence

# After editing, adding, renaming, or deleting source, the query refreshes first.
weave context example.com/project/service.Handle --json

# Use Git itself to define a multi-file impact root.
weave impact --git-diff origin/main --limit 100
```

Switch branches or move to another linked worktree and run the same query again. The command does not need a special checkout notification. Commit, tree, branch, overlay, worktree, and provider identities already participate in freshness, so observation is enough to select or rebuild the right facts.

This is the foundation the rest of Weave can build on. Compiler precision is useful because its facts remain current. Semantic bridges are useful because their checked-in declaration participates in the same refresh. Impact and architecture policy are useful because they evaluate the same evidence a navigation query sees. Federation is useful because it refuses to gain breadth by hiding stale members.

The next parts of this series will move inside the providers and normalized graph. This first boundary is the one every later feature depends on: before Weave answers where code leads, it proves which code it is looking at.
