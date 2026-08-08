<!-- Generated from https://thefellow.github.io/articles/composing-source-rich-context-without-a-second-index/ by scripts/generate_llm_content.py; do not edit. -->

# Opening Source Context Only When It Is Useful

Source: [https://thefellow.github.io/articles/composing-source-rich-context-without-a-second-index/](https://thefellow.github.io/articles/composing-source-rich-context-without-a-second-index/)

## Pyramid summary

- **~2 words:** Selected source context
- **~8 words:** Compact discovery opens current source only after anchor selection.
- **Expanded:** How Weave separates compact discovery from exact current-source context instead of serializing complete graph dossiers for every candidate.

## Full content

**Part 4 of [Building Weave](/series/weave.md).**

The first `weave context` implementation composed definitions, references, incoming and outgoing relationships, adjacent entities, provenance, and source into one bounded dossier. `weave explore` then ranked several candidates and returned several of those dossiers at once. It was precise, but the response repeated far more graph structure than an agent needed to choose its next file.

[Weave](https://github.com/TheFellow/weave) now uses two stages. `explore` returns compact navigation choices. `context` opens current source only after the caller selects an exact semantic anchor.

```sh
weave explore how menu publication reaches persistence
weave context example.com/project/menu.Service.Publish
weave definition example.com/project/menu.Service.Publish
```

<figure class="article-figure">
  <img src="/assets/images/articles/weave/source-rich-context.svg" alt="A research phrase enters compact discovery. The navigation index contributes a few semantic anchors while bounded ripgrep contributes diversified source hits. Each result carries a path, coordinate, preview, or exact context follow-up. Only a selected semantic anchor enters context, which reads and verifies current Git-visible source under independent line and byte limits.">
  <figcaption>Discovery returns choices; context spends source and metadata only on the chosen anchor.</figcaption>
</figure>

## Keep discovery small

`weave explore` resolves up to a few ranked symbols from the navigation index and combines them with ignore-aware ripgrep hits. A semantic anchor contains its kind, stable name, declaration coordinate, provider, evidence, and an exact `weave context` command. A lexical hit contains a path, line, column, and short preview.

The array has an encoded 12 KiB ceiling in addition to the result limit. Long names and previews therefore cannot turn an apparently bounded result count into an unbounded agent payload. The application response uses the versioned `weave.query/v2` envelope.

This is intentionally less than a dossier. Discovery does not load occurrences, expand adjacent symbols, repeat repository metadata for every edge, or speculate about which complete declarations the agent will read.

## Let source search do statement-level work

The navigation profile does not produce or store occurrences, call or reference edges, fields, locals, or content-token postings. Once a package or declaration is known, current source is a cheaper and more useful place to recover that detail.

The lexical half of `explore` extracts a bounded set of useful terms from the research phrase and runs one fixed-string ripgrep operation. It respects ignore files, excludes `.git`, `vendor`, and `node_modules`, rejects files larger than 1 MiB, limits captured output, scores term overlap, and diversifies results across files before filling remaining slots. Missing ripgrep or no matches is a soft miss; semantic anchors remain available.

This does not claim that text search is semantic. The navigation index supplies compiler-backed identities and retained high-value relationships. Ripgrep supplies current statement-level evidence that is wasteful to duplicate in persistent storage.

## Read one selected declaration

`weave context TARGET` resolves one stable anchor and reads its current Git-visible file. The source loader enforces repository provenance, path containment, regular-file and UTF-8 checks, line and byte budgets, and file-race detection. A Go function or method can expand from its indexed declaration coordinate to the complete current declaration when the budget permits. Structured content uses its retained document and section coordinates.

The source file remains authoritative. Weave stores the coordinate needed to find it, not a second cached body. If the file changed, ordinary query-driven freshness runs before the read; if the file changes during the read, the loader reports that race rather than presenting mixed evidence.

## Keep graph questions separate

The split also makes the CLI easier to reason about:

1. Use `explore` when the question is still a phrase.
2. Use `context` or `definition` after one semantic anchor looks relevant.
3. Use `dependencies`, `path`, `impact`, `graph`, or an architecture check for retained navigation relationships.
4. Use current source search for statement-level callers, references, and local data flow.

The last step is a deliberate contract change. `references`, `callers`, and `callees` are no longer managed-index commands because the navigation profile does not contain the facts needed to answer them exhaustively. Providers may use compiler analysis to derive higher-level navigation, but they do not transmit the discarded statement events.

## Measure the complete handoff

On the recorded `go-modular-monolith` audit, an ordinary multi-focus `explore --json` response occupied 171,537 bytes. Progressive discovery returned 3,157 bytes. Selecting its first anchor with `context --json` returned 3,195 bytes, including 337 bytes of current source.

The improvement did not come from compressing the old dossier. It came from avoiding speculative expansion. The first response answers “where should I look?” and the second answers “show me this source.” That is a more practical boundary for both a terminal user and a coding agent.
