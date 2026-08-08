<!-- Generated from https://thefellow.github.io/series/weave/ by scripts/generate_llm_content.py; do not edit. -->

# Building Weave

Source: [https://thefellow.github.io/series/weave/](https://thefellow.github.io/series/weave/)

## Pyramid summary

- **~2 words:** Weave series
- **~8 words:** From exhaustive semantic graphs to compact progressive source discovery.
- **Expanded:** An ordered path through Weave's move from an exhaustive semantic graph to a compact, fresh navigation index built for practical source discovery.

## Full content

Weave began by retaining a broad compiler and content graph. Repository and agent measurements showed that this made both the database and discovery responses much larger than the source evidence they were meant to reveal. The current implementation keeps a compact navigation projection, returns a few semantic anchors and ripgrep hits, and opens current source only after a caller selects a useful anchor.

This series preserves the engineering path that exposed that correction. Earlier articles describe the broad graph at the point it was built; each affected article now identifies what the format-4 navigation index retained, replaced, or removed. The stable ideas are freshness at read time, language-native adapters, explicit evidence, bounded queries, disposable local state, and measured agent outcomes. Exhaustive occurrences, statement-level call and reference storage, large multi-focus dossiers, and body-token postings are no longer the product direction.

[Explore the project](/projects/weave.md)
[View the repository](https://github.com/TheFellow/weave)

1. **Article:** [Keeping a Semantic Index Fresh Without a Daemon](/articles/keeping-a-semantic-index-fresh-without-a-daemon.md): How Weave combines Git state, provider-owned semantic units, bounded graph replacement, and manifest publication so every query observes current evidence.
2. **Article:** [Making Language Support a Process Contract](/articles/making-language-support-a-process-contract.md): How Weave keeps compiler runtimes outside its Go process while the core owns capability negotiation, bounds, validation, freshness, and atomic publication.
3. **Article:** [Making a Semantic Graph Inspectable](/articles/making-a-semantic-graph-inspectable.md): How Weave turns one bounded semantic neighborhood into deterministic DOT, reviewed contextual links, and an animated local explorer without creating a second graph model.
4. **Article:** [Opening Source Context Only When It Is Useful](/articles/composing-source-rich-context-without-a-second-index.md): How Weave separates compact discovery from exact current-source context instead of serializing complete graph dossiers for every candidate.
5. **Article:** [Caching a Federated Graph Without Weakening Freshness](/articles/caching-a-federated-graph-without-weakening-freshness.md): How Weave accelerates machine-wide symbol and graph queries with an immutable hot projection keyed by exact worktree generations while keeping every repository authoritative.
6. **Article:** [Shrinking a Semantic Graph into a Navigation Index](/articles/shrinking-a-semantic-graph-without-changing-its-meaning.md): How Weave cut a repository index by 98.38% by retaining navigation anchors and high-value relationships instead of treating every compiler event as durable product data.
7. **Article:** [Comparing Semantic Graphs Without Mutating the Worktree](/articles/comparing-semantic-graphs-without-mutating-the-worktree.md): How Weave compares exact Git revisions and dirty worktrees through the same provider pipeline, separates source changes from graph changes, and makes bounded impact and test claims with evidence.
8. **Article:** [Warming a Semantic Index Without Making the Watcher Authoritative](/articles/warming-a-semantic-index-without-making-the-watcher-authoritative.md): How Weave uses an optional foreground polling loop to coalesce edits and warm the same query-authoritative freshness pipeline without installing a daemon, hook, or second indexer.
9. **Article:** [Editing Contextual Graph Links Without Losing Source Truth](/articles/editing-contextual-graph-links-without-losing-source-truth.md): How Weave turns its local graph explorer into a source-evidence inspector and revision-guarded editor while keeping checked-in declarations, application use cases, and query-driven refresh authoritative.
10. **Article:** [Managing Compiler Adapters Without Inventing a Package Registry](/articles/managing-compiler-adapters-without-inventing-a-package-registry.md): How Weave turns an explicitly selected local adapter executable into pinned, routable automatic language support with no remote registry, ambient discovery, or hidden trust expansion.
11. **Article:** [Indexing Schemas and Build Declarations Without Executing the Repository](/articles/indexing-schemas-and-build-declarations-without-executing-the-repository.md): How Weave turns bounded source-only schemas, infrastructure, migrations, and build manifests into category-atomic graph evidence without running their tools.
12. **Article:** [Measuring Agent Research Beyond Query Latency](/articles/measuring-agent-research-beyond-query-latency.md): How paired agent research and a storage-payload audit moved Weave from large graph dossiers to compact progressive discovery without losing answer quality.
13. **Article:** [Finding Source Bodies Without Indexing Them](/articles/making-source-bodies-discoverable-without-copying-them.md): How Weave replaced broad body-token postings with bounded ripgrep discovery over current source while keeping structured document anchors in its navigation index.
14. **Article:** [Reusing Local Query State Without Installing a Daemon](/articles/serving-persistent-agent-queries-without-a-daemon.md): How Weave serves bounded reads through an explicit NDJSON session or an idle-reaping per-worktree broker while preserving one-shot freshness and maintenance paths.
15. **Article:** [Turning Cross-Repository Soaks into Indexing Contracts](/articles/turning-cross-repository-soaks-into-indexing-contracts.md): How a strict twelve-repository soak turns compiler adapter failures into bounded contracts for preparation, discovery, normalization, memory, verification, and source immutability.
