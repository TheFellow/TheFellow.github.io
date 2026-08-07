<!-- Generated from https://thefellow.github.io/projects/weave/ by scripts/generate_llm_content.py; do not edit. -->

# Weave

Source: [https://thefellow.github.io/projects/weave/](https://thefellow.github.io/projects/weave/)

## Pyramid summary

- **~2 words:** Semantic indexing
- **~8 words:** A Git-aware semantic index for deterministic compiler-backed code queries.
- **Expanded:** A local-first semantic index that turns compiler facts and live Git state into bounded, deterministic code queries.

## Full content

[View the repository](https://github.com/TheFellow/weave)
[Read the Weave series](/series/weave.md)
[Start with fresh queries](/articles/keeping-a-semantic-index-fresh-without-a-daemon.md)

Weave is a local-first, Git-aware semantic index for source code. It asks language-native compiler tooling for facts, normalizes them into one evidence-carrying graph, and exposes bounded CLI queries for people and coding agents. The index is disposable derived state. It stays beside Git instead of entering commits, requires no hosted service, and refreshes its automatic provider inventories before a query can observe stale answers.

The problem is familiar when working in a large repository. Finding a name is easy; establishing which declaration it resolves to, who calls it, which interface it implements, what package owns it, and what a change can affect requires semantic context. Coding agents repeatedly reconstruct that context with filename search, text search, and whole-file reads. Weave preserves the relationships the compiler already established and gives them a deterministic command-line interface.

```sh
weave symbols Handle --limit 20
weave definition Handle
weave callers Handle
weave path SymbolA SymbolB --kind calls --max-depth 8
weave impact --git-diff origin/main --json
```

Every result retains its provider and evidence class. A compiler-resolved call is `exact`; a checked-in relationship may be `declared` or `generated`; a future syntax fallback must say that it is `syntactic`. Source locations, stable symbol identities, and bounded traversal make the graph useful as evidence rather than as an opaque relevance score.

The native Go provider uses `go/packages` and `go/types` for declarations, references, imports, implementations, and direct calls. An isolated .NET adapter uses Roslyn and MSBuild for C# plus FSharp.Compiler.Service for F#. Checked-in `.weave/bridges.json` declarations connect exact relationships that compilers cannot see across languages, repositories, schemas, generated artifacts, and documentation. SCIP import provides a separate bounded snapshot path for existing compiler-backed indexers; those explicit imports must currently be repeated when their producer output changes.

The automatic Go, .NET, and bridge producers own disjoint inventories of semantic compilation units. A refresh validates complete batches, replaces each changed unit atomically, and publishes a new freshness manifest only after the graph update succeeds. The manifest includes the repository, worktree, commit, tree, branch, dirty overlay, provider identity, and unit fingerprints. Branch switches, untracked files, build-context changes, or a new adapter therefore cannot leave an old automatic inventory looking current.

The same normalized graph supports local and cross-repository questions. Explicitly registered worktrees can participate in catalog queries, but each member refreshes before its database is opened. A member that cannot refresh is excluded with a diagnostic instead of silently contributing stale facts. Architecture rules then evaluate the same imports, calls, dependencies, and declared bridges that interactive queries expose, with deterministic text, JSON, and SARIF output for local use and CI.

The current implementation is an early alpha with a usable Go indexing and query lifecycle, compiler-native C# and F# coverage through the optional adapter, graph storage and verification, Git-diff impact analysis, catalog federation, and architecture policy. The first tagged release remains ahead. The release workflow is already shaped around checksummed core archives and same-version .NET adapter artifacts so the packaging boundary is tested as part of the product rather than left as a manual follow-up.

### Why it is worth exploring

- It makes freshness part of every read instead of depending on a daemon or a remembered indexing step.
- It keeps compiler truth, explicit declarations, and weaker evidence visibly distinct inside one graph.
- It treats human output and versioned JSON as two presentations of the same bounded application behavior.
- It turns impact analysis and architecture checks into queries over the same facts used for code navigation.

Start with the [freshness walkthrough](/articles/keeping-a-semantic-index-fresh-without-a-daemon.md), then read `internal/repository`, `internal/freshness`, `internal/graph`, and `internal/query` in that order. The [Weave series](/series/weave.md) will continue outward from this lifecycle into compiler adapters, semantic bridges, impact analysis, federation, and executable architecture policy.
