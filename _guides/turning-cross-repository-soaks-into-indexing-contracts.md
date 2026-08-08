---
title: "Turning Cross-Repository Soaks into Indexing Contracts"
date: 2026-08-08 04:04:08 -0700
last_modified_at: 2026-08-08 04:04:08 -0700
excerpt: "How a strict twelve-repository soak turns compiler adapter failures into bounded contracts for preparation, discovery, normalization, memory, verification, and source immutability."
permalink: /articles/turning-cross-repository-soaks-into-indexing-contracts/
series: weave
series_order: 15
order: 19
featured: true
status: "Weave, part 15"
icon: "matrix"
accent: "#ff922b"
topics: ["Code intelligence", "Compiler adapters", "Performance"]
---

{% include series-notice.html %}

A compiler adapter can pass every fixture and still misunderstand a repository. Real workspaces hide solutions below their checkout root, let project references pull the same assembly into a workspace twice, keep buildable projects outside the primary solution, repeat global SCIP symbols across targets, and depend on compiler caches whose contents are not part of the timed operation.

Those are not benchmark inconveniences. They are pressure on the indexing contract. [Weave](https://github.com/TheFellow/weave) therefore runs one candidate across a mixed local corpus, keeps dependency preparation outside the measurement, denies network and restore during indexing, verifies and exports every successful graph, and proves that the source repositories did not change. A failure either identifies a bounded implementation correction or remains an explicit residual.

<figure class="article-figure">
  <img src="{{ '/assets/images/articles/weave/cross-repository-indexing-soak.svg' | relative_url }}" alt="Twelve mixed-language source repositories enter isolated local clones. Dependency download, restore, and F-sharp reference builds prepare those clones before timing. A candidate Weave build performs an offline cold index, five current no-change queries, graph verification, and a full export while collecting elapsed time, peak resident memory, database size, and fact counts. Source status is compared before and after. Failures feed bounded corrections to Go package loading, dotnet project discovery, F-sharp restore policy, Rust SCIP normalization, adapter environment handling, and the benchmark harness before the complete matrix is rerun.">
  <figcaption>The corpus is an executable contract. Preparation makes the timed operation honest, every graph must verify and export, and a failure returns to the narrowest responsible boundary before the whole matrix runs again.</figcaption>
</figure>

## Make the corpus part of the test

The retained soak covers twelve repositories at pinned commits: this website, a profile repository, C# value types and Cedar authorization, two Go analyzers, F# agent workflows, a Go fluid simulation, a large Go modular monolith, a Go set-reconciliation library, Weave itself, and a Rust rigid-body project. That mix is intentionally uneven. It includes tiny and large graphs, source and documentation, nested build roots, multi-project solutions, standalone fixtures, library and executable targets, and several compiler runtimes.

The harness builds the candidate core and adapters once, then creates a detached local clone for each repository without hard links. Every clone gets its own Git-private index. The source checkout remains the authority being tested, not a scratch directory that the benchmark may quietly repair.

```sh
WEAVE_RUST_ADAPTER="$PWD/adapters/rust/target/release/weave-rust" \
WEAVE_BENCHMARK_TIMEOUT=900 \
scripts/benchmark-repositories.sh .. RESULTS \
  TheFellow.github.io TheFellow ValueTypes arch-lint cedar-dotnet enumstruct \
  fkyeah fluid go-modular-monolith go-riblt weave ai-rigidbody
```

The explicit repository list makes a diagnostic rerun small without giving the final run an easier corpus. A failure does not stop the remaining repositories. The harness records every outcome, then returns failure if any member failed. One early repository can no longer hide evidence from the rest of the matrix.

## Prepare dependencies without timing a restore

Offline indexing is meaningful only if the clone already contains the compiler inputs the adapter is allowed to use. Preparation and measurement are therefore separate phases.

For Go, the harness runs `go mod download all` in the disposable clone before the timed command. This can complete an incomplete `go.sum` inside that clone, while the actual Weave process still runs with readonly module behavior and networking denied. For .NET, every discovered C# and F# project is restored before timing, not only the projects reachable from one selected solution. F# projects are also built in advance because FSharp.Compiler.Service needs reference outputs that a restore alone does not produce.

The timed request cannot restore what preparation missed. Buildalyzer once performed an implicit F# `/restore` during design-time evaluation even though the adapter request denied it. The adapter now disables that default explicitly. A green result therefore means the requested operation stayed offline and restore-free, not merely that an unreported network path happened to succeed.

This separation also makes elapsed time interpretable. Cold index time measures provider discovery, compiler analysis, fact normalization, graph publication, and manifest publication. It does not mix those operations with package download speed.

## Treat repository shape as semantic input

The first diagnostic passes found failures that isolated fixtures did not contain:

| Pressure | Incorrect assumption | Bounded correction |
| --- | --- | --- |
| Large Go module | `go/packages.NeedDeps` was necessary to resolve dependency types | Keep repository syntax and type information, but let dependency types arrive through compiler export data without retaining recursive dependency ASTs |
| Nested .NET solution | Every recursively discovered project should join the same workspace | Select the nearest solution depth, reject ambiguity at that depth, and avoid reopening projects Roslyn already loaded through references |
| Generated C# documents | Every compiler document must be repository-contained | Diagnose and omit SDK-generated documents outside the checkout instead of aborting the repository inventory |
| Standalone F# fixtures | Restoring the selected solution prepares the whole checkout | Restore every project, prebuild F# references, and explicitly keep design-time evaluation restore-free |
| Nested Rust crate | rust-analyzer always runs from the repository root | Discover the nearest Cargo or `rust-project.json` root and rebase SCIP document paths to the repository |
| Rust library, binary, and test targets | One global SCIP symbol record appears only once | Select deterministic first-document ownership for equivalent symbol records while retaining every occurrence and relationship |
| Adapter startup | Doctor, explicit index, and automatic refresh can carry different toolchain variables | Use one bounded environment allowlist for every adapter entry point |

None of those corrections weaken graph validation. The C# adapter still rejects two equally near solutions because choosing one lexically would invent build intent. Rust still rejects conflicting descriptions of one global symbol; it collapses only equivalent producer repetition. Generated C# source remains visible as a diagnostic rather than being assigned a false repository path.

The normalization work also removed accidental scale costs. C# edge de-duplication now uses a per-project identity set instead of scanning every prior edge for every insertion. Rust builds one line index per document instead of rescanning its source from byte zero for every occurrence, and it memoizes symbol validation and stable IDs. The Go provider no longer keeps the full dependency graph's syntax resident when it emits facts only for repository packages.

## Measure publication, not only compiler startup

Each successful repository performs one cold index, five current no-change queries, `weave verify`, and a complete JSON export. The harness records elapsed time, the measured process tree's peak resident set, database bytes, and graph counts. It captures source status before preparation and compares it after the complete run.

The strict final invocation exited zero. All twelve graphs verified and exported, every source status remained unchanged, and all sixty no-change queries completed between 0.706 and 1.001 seconds on the development machine.

| Repository | Cold index | Peak RSS | Warm query range | Graph database |
| --- | ---: | ---: | ---: | ---: |
| TheFellow.github.io | 48.465 s | 310 MiB | 0.750–0.778 s | 146,608,128 bytes |
| TheFellow | 1.412 s | 20 MiB | 0.713–0.720 s | 1,048,576 bytes |
| ValueTypes | 10.100 s | 168 MiB | 0.706–0.757 s | 43,679,744 bytes |
| arch-lint | 11.456 s | 149 MiB | 0.879–0.921 s | 67,198,976 bytes |
| cedar-dotnet | 51.338 s | 520 MiB | 0.756–0.782 s | 397,537,280 bytes |
| enumstruct | 4.866 s | 106 MiB | 0.711–0.775 s | 47,013,888 bytes |
| fkyeah | 132.146 s | 1,118 MiB | 0.774–0.783 s | 418,791,424 bytes |
| fluid | 4.112 s | 135 MiB | 0.816–0.876 s | 63,754,240 bytes |
| go-modular-monolith | 82.122 s | 1,129 MiB | 0.834–1.001 s | 903,421,952 bytes |
| go-riblt | 3.832 s | 103 MiB | 0.772–0.806 s | 51,290,112 bytes |
| weave | 81.763 s | 770 MiB | 0.918–0.966 s | 655,515,648 bytes |
| ai-rigidbody | 82.406 s | 1,978 MiB | 0.708–0.768 s | 197,996,544 bytes |

These are development-machine observations, not service-level objectives. The full [retained benchmark record](https://github.com/TheFellow/weave/blob/main/.ai/benchmarks/2026-08-08-indexing-soak.md) pins the commits and environment and includes units, documents, symbols, occurrences, and edges for every graph.

The matrix closes two earlier unknowns. Cedar previously exceeded a four-minute adapter bound; it now produces 287 units, 7,629 symbols, 69,794 occurrences, and 88,135 edges in 51.338 seconds. FKYeah now produces a complete 915-unit graph, including standalone fixture projects, in 132.146 seconds without restoring inside the timed adapter request.

The Go result needs more careful interpretation. The large monolith's peak fell from roughly 2.45 GB in the adjacent diagnostic baseline to 1.13 GiB after removing recursive dependency syntax retention. Its 82.122-second cold time is slower than the earlier 37.785-second repository baseline because compiler export-data and cache conditions changed, and the provider and measurement scope are not identical. Warm queries remain below 1.01 seconds. Memory improved, but the table does not justify pretending cold performance improved in every dimension.

## Exercise the installed incremental path

The full matrix uses binaries built from the candidate worktree and proves cold publication. A separate smoke installs `./cmd/weave`, creates an isolated clone of go-riblt, indexes and verifies it, then adds one comment to `codec.go` inside that clone.

The next observation reports `dirty: true`, `change_count: 1`, and `index: refreshed 1 changed paths`. The refresh completes in 2.990 seconds at 142 MiB peak RSS, publishes a new generation, and passes `weave verify`. The original go-riblt repository remains clean.

That small result covers a different boundary from the cold table. The installed entry point can observe an ordinary dirty overlay, select the one changed path, replace the affected derived facts, publish a current manifest, and verify the result without requiring a special benchmark-only invocation. The disposable clone absorbs the deliberate edit, preserving the same source-isolation rule as dependency preparation.

## Keep the residuals in the result

All green does not mean all small. The Rust rigid-body repository peaked at 1,978 MiB while rust-analyzer produced SCIP. Weave's normalization no longer adds an occurrence-by-source-length scan, but it does not control the producer's complete working set. That boundary is now measured rather than hidden.

The matrix also does not prove every repository shape, operating system, compiler version, or warm-cache state. It proves something narrower and more useful: these pinned repositories can be prepared without mutating their sources, indexed offline by this candidate, queried through current manifests, verified structurally, and exported completely under recorded bounds.

That is enough to turn a collection of examples into a regression contract. Future provider work can rerun the same matrix and compare graph counts, storage, time, and memory without making one number the product. A faster index that drops a standalone project, mutates `go.sum`, omits repeated Rust occurrences, skips verification, or silently restores packages is a failed run.

## Let failures improve the shared boundary

The most valuable result is not twelve green rows. It is the path by which red rows changed reusable boundaries:

1. The harness made preparation, isolation, continuation, peak memory, and source immutability explicit.
2. Provider discovery learned to respect the nearest actual build root instead of assuming the checkout root is the compilation root.
3. Compiler-specific repetition became deterministic normalization only where the producer format permits it.
4. Every adapter entry point began carrying the same small toolchain environment rather than acquiring different behavior by command path.
5. Verification and export stayed mandatory after performance fixes, so reduced work could not quietly become reduced truth.

That loop belongs beside unit tests and protocol conformance. Fixtures prove narrow behavior. A cross-repository soak proves that the behaviors compose across real toolchains, graph sizes, and repository topology. Keeping both is how a language-neutral index earns the right to call its green result complete.
