---
title: "Weave"
date: 2026-08-06 22:55:00 -0700
last_modified_at: 2026-08-07 01:27:00 -0700
excerpt: "A local-first semantic index that connects compiler facts, repository structure, and documents through bounded deterministic queries."
language: "Go"
license: "MIT"
repository_url: "https://github.com/TheFellow/weave"
last_updated: 2026-08-07
series_url: "/series/weave/"
order: 5
featured: true
icon: "route"
accent: "#4dabf7"
topics: ["Code intelligence", "Developer tools", "Git"]
---

<div class="project-meta"><span>Go</span><span>Code intelligence</span><span>Git</span><span>MIT</span><span>Updated {{ page.last_updated | date: "%B %-d, %Y" }}</span></div>

[View the repository](https://github.com/TheFellow/weave){: .btn .btn--primary }
[Read the Weave series](/series/weave/){: .btn }
[Start with fresh queries](/articles/keeping-a-semantic-index-fresh-without-a-daemon/){: .btn }

Weave is a local-first, Git-aware semantic index for the knowledge encoded in a workspace. It combines language-native compiler facts with files, structured documents, sections, links, assets, routes, and metadata in one evidence-carrying graph, then exposes bounded CLI queries for people and coding agents. The index is disposable derived state. It stays beside Git instead of entering commits, requires no hosted service, and refreshes its automatic provider inventories before a query can observe stale answers.

The problem is familiar when working in a large repository. Finding a name is easy; establishing which declaration it resolves to, who calls it, which interface it implements, what package owns it, and what a change can affect requires semantic context. Coding agents repeatedly reconstruct that context with filename search, text search, and whole-file reads. Weave preserves the relationships the compiler already established and gives them a deterministic command-line interface.

```sh
weave symbols Handle --limit 20
weave definition Handle
weave callers Handle
weave path SymbolA SymbolB --kind calls --max-depth 8
weave impact --git-diff origin/main --json
weave workspace outline README.md
weave workspace backlinks docs/design.md --scope catalog
```

Every result retains its provider and evidence class. A compiler-resolved call is `exact`; a checked-in relationship may be `declared` or `generated`; a future syntax fallback must say that it is `syntactic`. Source locations, stable symbol identities, and bounded traversal make the graph useful as evidence rather than as an opaque relevance score.

The native Go provider uses `go/packages` and `go/types` for declarations, references, imports, implementations, and direct calls. Isolated adapters now carry .NET, Python, Rust, and C-family semantics across the same process contract. Roslyn, FSharp.Compiler.Service, CPython's compiler symbol table, `rust-analyzer scip`, and `scip-clang` remain the authorities for their own languages. Each adapter preserves what its producer can prove and omits stronger relationships it cannot: Python calls remain syntactic, rust-analyzer references do not become invented call edges, and C++ facts remain scoped to one selected compilation database.

An always-on workspace provider covers what does not compile. It inventories exact Git-visible paths and parses Markdown/GFM, YAML front matter, inert HTML, headings, links, images, fences, routes, topics, series, and explicit generated-from declarations. It never executes Jekyll, Liquid, Mermaid, plugins, network requests, or embedded examples. The resulting `workspace find`, `outline`, `links`, and `backlinks` queries can navigate a repository with no buildable artifact and join documentation to compiler-owned path anchors.

Language support uses an open, protoc-style process extension point. Any executable can implement the experimental [`weave.adapter/v0`](https://github.com/TheFellow/weave/blob/main/protocol/adapter/v0/README.md) request and frame contract without importing Weave's Go packages. The core owns capability negotiation, permissions, deadlines, bounds, validation, and atomic publication; the adapter owns its compiler and semantic units. A user-selected `WEAVE_ADAPTER_CONFIG` registry can give a third-party executable automatic freshness without a core change by declaring literal argv, conservative Git-visible inputs, permissions, and a timeout. Weave neither discovers registry files inside repositories nor scans `PATH` for arbitrary adapters, and invalid selected configuration fails closed. Checked-in `.weave/bridges.json` declarations separately connect exact relationships that compilers cannot see across languages, repositories, schemas, generated artifacts, and documentation. Direct SCIP import remains a bounded snapshot path whose producer output must currently be reimported when it changes.

The automatic workspace, Go, .NET, Python, Rust, C++, bridge, and explicitly registered producers own disjoint inventories of semantic units. A refresh validates complete batches, replaces each changed unit atomically, and publishes a new freshness manifest only after the graph update succeeds. The manifest includes the repository, worktree, commit, tree, branch, dirty overlay, provider and runtime identities, configuration, and unit fingerprints. Branch switches, untracked files, route or heading-surface changes, build-context changes, an interpreter or toolchain upgrade, or a new adapter policy therefore cannot leave an old automatic inventory looking current.

The same normalized graph supports local and cross-repository questions. Explicitly registered worktrees can participate in catalog queries, but each member refreshes before its database is opened. A member that cannot refresh is excluded with a diagnostic instead of silently contributing stale facts. Conventional GitHub deep links can resolve to the same repository and path identities a catalog member exposes, while the authored URL and ref remain visible. File and Git-diff impact now include incoming links and embeds, so an article or README that explains changed code can appear beside compiler-derived callers. Architecture rules evaluate the same imports, calls, dependencies, and declared bridges that interactive queries expose, with deterministic text, JSON, and SARIF output for local use and CI.

The current implementation is an early alpha with a usable Go indexing and query lifecycle, compiler-native C#, F#, Python, Rust, C, C++, and CUDA coverage, structured workspace navigation, an open process protocol and registry, graph storage and verification, Git-diff impact analysis, catalog federation, and architecture policy. The first repository-scale baseline has already changed the implementation: bounded per-unit storage transactions, candidate pruning for interface analysis, and fixed-size domain-separated Go fact identities brought a 433,523-fact Mixology index from beyond the five-minute measurement bound to 37.8 seconds. Compact identities reduced the graph from 7.54 GB to 1.11 GB, which is a substantial correction and still an explicit target for further reduction.

The same measurement kept the .NET boundary honest. A large Cedar solution exceeded the adapter's four-minute full-refresh limit, and the original .NET 9 adapter host could not evaluate FKYeah's .NET 10 F# targets. Both runs stopped without publishing a partial inventory. The follow-up moved the adapter to .NET 10, preserved the prebuilt reference outputs FSharp.Compiler.Service needs, ordered the F# project graph, and proved genuine FKYeah indexing. The large-solution bound remains visible.

The first tagged release is still ahead; its workflow is already shaped around checksummed core archives, same-version .NET adapter artifacts, and an independently installable Python wheel so packaging and runtime limitations remain visible parts of the product.

### Why it is worth exploring

- It makes freshness part of every read instead of depending on a daemon or a remembered indexing step.
- It keeps compiler truth, explicit declarations, and weaker evidence visibly distinct inside one graph.
- It treats repository topology and documentation as first-class knowledge without executing their renderers.
- It treats human output and versioned JSON as two presentations of the same bounded application behavior.
- It turns impact analysis and architecture checks into queries over the same facts used for code navigation.

Start with the [freshness walkthrough](/articles/keeping-a-semantic-index-fresh-without-a-daemon/), then read `internal/repository`, `internal/freshness`, `internal/graph`, and `internal/query` in that order. Continue through `protocol/adapter/v0`, `internal/adapter/registry.go`, and `adapters` to see five language runtimes meet the same graph boundary, then follow `internal/workspaceindex` into the non-compiling workspace graph. The [Weave series](/series/weave/) will continue outward from this lifecycle into structured content, semantic bridges, impact analysis, federation, and executable architecture policy.
