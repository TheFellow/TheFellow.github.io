<!-- Generated from https://thefellow.github.io/articles/composing-source-rich-context-without-a-second-index/ by scripts/generate_llm_content.py; do not edit. -->

# Composing Source-Rich Context Without a Second Index

Source: [https://thefellow.github.io/articles/composing-source-rich-context-without-a-second-index/](https://thefellow.github.io/articles/composing-source-rich-context-without-a-second-index/)

## Pyramid summary

- **~2 words:** Source-rich context
- **~8 words:** One bounded dossier joins exact graph facts to current Git-visible source.
- **Expanded:** How Weave composes exact graph facts, current source excerpts, direct relationships, and repository provenance into one bounded dossier without adding embeddings or another store.

## Full content

**Part 4 of [Building Weave](/series/weave.md).**

A definition is useful when I already know the question is "where is this declared?" A caller list is useful when the question is "what invokes it?" An impact query is useful when I am planning a change. Real investigation usually begins one step earlier. I have a symbol, file, Markdown section, or route and need enough surrounding evidence to decide which question matters next.

That does not justify another index. The definitions, references, relationships, document identities, provider provenance, and current repository already exist. [Weave](https://github.com/TheFellow/weave) composes those facts with [`weave context TARGET`](https://github.com/TheFellow/weave/blob/main/.ai/prior-art/context-query/README.md), returning one bounded source-rich dossier rather than persisting a parallel retrieval model.

```sh
weave context HandleRequest
weave context README.md --context-lines 4
weave context docs/design.md#storage --json
weave context SharedType --scope catalog --repo github.com/example/service
weave context Server.Serve
```

<figure class="article-figure">
  <img src="/assets/images/articles/weave/source-rich-context.svg" alt="An exact target resolves through Weave's current normalized graph while source coordinates locate current Git-visible files in the owning worktree. One bounded context query composes the focus, definition and reference excerpts, incoming and outgoing relationships, adjacent entities, provenance, freshness, and independent truncation metadata.">
  <figcaption>The graph says what evidence to retrieve. The current owning worktree supplies source bytes. One application query composes both under explicit bounds.</figcaption>
</figure>

## Compose the graph that already exists

The context operation starts with the same heterogeneous resolver used by the other query surfaces. A target may identify a compiler symbol, package, file, document section, route, asset, or another materialized entity. Resolution must produce exactly one entity. Concise qualified names such as `Server.Serve` can match compiler stable names whose ownership is encoded as longer package, type, and method segments. Exact IDs and stable names retain precedence. If a query still matches more than one entity, the command reports candidate stable names, kinds, and graph IDs instead of guessing which result looks most relevant.

Once resolved, the operation asks the existing store for definition and reference occurrences, direct incoming edges, direct outgoing edges, and materialized entities at the other ends of those edges. Human output begins with stable names, then removes a repeated repository identity and compiler category segments such as `type` and `method` inside the dossier. JSON retains the full names and exact graph IDs. The query does not infer a relationship from nearby text or ask a model to summarize the graph. Every returned fact retains its provider and evidence class.

The result is deliberately one hop. A context dossier should help choose the next exact query, not quietly become an unbounded neighborhood walk. [`weave graph`](/articles/making-a-semantic-graph-inspectable.md) remains the right surface for exploring topology; `weave path` remains the right surface for a bounded route; `weave impact` remains the right surface for reverse reachability.

This separation keeps context useful without creating a second definition of relevance. The implementation is a composition over the normalized store, not a source database, embedding index, MCP server, or hidden LLM call.

## Read source at query time

Graph facts contain stable document identities, source ranges, and, when a provider can supply one, the indexed content hash. They do not contain a private copy of the repository. When a context result needs lines, Weave reads them from the current worktree that owns the evidence.

That distinction matters. Cached source could agree with an old range while disagreeing with the file a person is about to edit. Query-driven freshness runs before the graph read, then the source loader verifies the file again at the point of use. If the indexed hash and current SHA-256 digest disagree, the result reports changed source and withholds the excerpt. It never pairs fresh-looking lines with stale coordinates.

Line windows remain evidence, not reconstructed symbol bodies. By default the command adds two surrounding lines to an occurrence range. Human output numbers those current lines; JSON also preserves the exact indexed range and source status. A generated document can still be shown when it is Git-visible, but its `generated` evidence remains visible. An external entity with no document remains an honest graph entity with no invented source.

## Make source serving a security boundary

Reading a path stored in a database is not automatically safe. The source loader accepts only canonical repository-relative Git paths. It rejects absolute paths, parent traversal, platform-volume paths, backslashes, and anything that resolves outside the owning worktree.

The candidate must be a regular file and must be either tracked or visible as a non-ignored untracked Git path. Weave inspects the path, opens it, and verifies that the opened file is still the same file. A second identity, size, and modification-time check after reading catches replacement or mutation during the read. Symlinks, ignored files, missing paths, non-UTF-8 content, and individual files over 16 MiB produce explicit statuses without returning bytes.

These are data conditions, not excuses to guess. `unsafe-path`, `not-git-visible`, `not-regular`, `changed`, `invalid-range`, and `budget-exhausted` tell a caller why source is absent. The graph evidence and relationships can still be useful while the missing excerpt stays visible as a limitation.

## Give every section its own budget

A single global limit makes a composite response unpredictable. A symbol with many references could consume the allowance before one incoming relationship appears. Weave instead applies `--limit` independently to occurrences, incoming edges, and outgoing edges. Each section reports its own truncation.

The relationship sections read a bounded surplus before applying that limit, collapse edges that reach the same adjacent entity, and retain the most useful evidence for that endpoint. Calls come before contracts and inheritance, dependencies come before authored navigation, and raw references come last. A reference remains when it is the only useful known connection, but local variables, parameters, and language builtins are omitted from this bounded dossier because their evidence already appears in the source excerpt. They remain available through exhaustive graph data. Repeated reference facts cannot crowd a compiler-resolved call out of a small context response. Stable rank, endpoint, and edge ordering keep the selection deterministic.

Source has a separate byte budget. The default response allows 64 KiB of excerpt text. If adding surrounding lines would exceed the remaining budget, the loader first tries the exact evidence range. If even that does not fit, the excerpt reports budget exhaustion and returns no partial line. `--context-lines` and `--max-source-bytes` make both choices explicit.

```sh
weave context HandleRequest \
  --limit 24 \
  --context-lines 3 \
  --max-source-bytes 131072 \
  --json
```

The structured result uses `weave.context/v1` inside the ordinary `weave.query/v1` response. Its metadata records scope, bytes returned, freshness, partial federation, and truncation for occurrences, incoming relationships, outgoing relationships, and source. Deterministic ordering makes two equivalent dossiers compare cleanly.

## Reuse the dossier for a research phrase

An agent does not always begin with one entity. `weave explore RESEARCH PHRASE` adds bounded deterministic lexical retrieval in front of the same context composition. It first gives an exact or uniquely resolvable entity the usual single result. Otherwise it extracts up to twelve useful terms, removes ordinary question words, derives a small set of mechanical suffix variants, and treats generic scope words such as `domain`, `GUI`, and `TUI` as ranking context when more specific terms exist. Candidates accumulate explicit scores from symbol-search position, exact or partial display-name matches, stable-name matches, scope matches, and kind weights. Score, stable name, and graph ID define the complete order.

```sh
weave explore how menu readiness reaches GUI and TUI \
  --limit 6 \
  --relationship-limit 6 \
  --context-lines 1
```

The default returns at most six entities and independently caps each dossier's occurrences, incoming relationships, and outgoing relationships at six. One 64 KiB source allowance is divided across the selected entities rather than silently multiplying with the result count. Each result is still an ordinary `weave.context/v1` dossier with exact identities, current source checks, provenance, freshness, and truncation. The command adds no model, embedding store, or second persisted query engine; natural-language reasoning remains with the consuming agent.

## Carry provenance across repositories

Local context has one obvious worktree. Catalog context does not. Two repositories can contain a fact with the same stable identity, and an adjacent entity can come from a different member than the focus.

The federated store therefore records which repository and worktree supplied each symbol, occurrence, and document while it materializes the result. Source loading follows that provenance back to the owning root. It does not assume the process working directory or take an arbitrary repository path from the user.

Catalog reads still use the existing [refresh-before-open contract](/articles/keeping-a-semantic-index-fresh-without-a-daemon.md). A member that cannot refresh is excluded with a diagnostic. The context metadata marks the result partial, allowing a caller to distinguish "no relationship exists" from "one repository could not participate."

## Use the dossier to choose the next query

A practical investigation can now stay narrow:

1. Run `weave context TARGET` to resolve one entity and see its current definition, references, immediate relationships, and provenance.
2. Inspect source statuses and truncation before treating absence as evidence.
3. Follow one exact adjacent identity with another context query, or switch to `weave graph` when topology is the question.
4. Use `weave path`, `weave impact`, `weave references`, or an architecture check once the dossier reveals the precise question.

The useful feature is not a larger blob of context. It is a bounded composition whose omissions are as explicit as its facts. The graph remains the semantic authority, Git remains the source authority, and freshness joins them at query time. That gives people and coding agents enough evidence to continue without asking a new retrieval subsystem to reinterpret what the repository already knows.
