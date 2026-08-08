<!-- Generated from https://thefellow.github.io/articles/making-source-bodies-discoverable-without-copying-them/ by scripts/generate_llm_content.py; do not edit. -->

# Finding Source Bodies Without Indexing Them

Source: [https://thefellow.github.io/articles/making-source-bodies-discoverable-without-copying-them/](https://thefellow.github.io/articles/making-source-bodies-discoverable-without-copying-them/)

## Pyramid summary

- **~2 words:** Current-source discovery
- **~8 words:** Semantic anchors and bounded ripgrep replace broad body postings.
- **Expanded:** How Weave replaced broad body-token postings with bounded ripgrep discovery over current source while keeping structured document anchors in its navigation index.

## Full content

**Part 13 of [Building Weave](/series/weave.md).**

A structured-content index can know that a heading exists and still miss a concept written only in the paragraph below it. Weave first addressed that gap by attaching body-derived search terms to graph entities and publishing them through token postings. The source text stayed outside the database, but its vocabulary still multiplied index and response cost.

The format-4 navigation index removes those broad content postings. [Weave](https://github.com/TheFellow/weave) now combines retained document and section anchors with one bounded ripgrep pass over current source. The index answers which semantic entities exist; source search answers which current lines contain the research terms.

<figure class="article-figure">
  <img src="/assets/images/articles/weave/source-body-discovery.svg" alt="A research phrase is normalized into a small set of useful fixed-string terms. Compact semantic lookup returns structured document and declaration anchors. In parallel, bounded ignore-aware ripgrep reads current Git-visible files and returns scored path, line, column, and preview hits. Results are diversified by file and combined under one item and byte budget. A selected semantic anchor can then open exact current context.">
  <figcaption>Body discovery stays in current source. The database keeps navigation anchors instead of a second full-text vocabulary.</figcaption>
</figure>

## Remove the duplicate vocabulary

The previous design allowed providers to attach thousands of normalized terms to one symbol. That made a Markdown section or unsupported source file discoverable through the same inverted index as a declaration name. It also retained a second representation of words already available in the worktree and copied those postings into machine-wide aggregate state.

The storage audit found that this was the wrong default for a disposable local tool. Name and stable-name lookup are valuable because they map human concepts onto compiler and content identities. Broad body vocabulary is different: ripgrep already searches those bytes efficiently, respects repository ignore rules, and returns the exact current line an agent needs.

Format 4 therefore clears search terms from ordinary code anchors and does not persist broad content-token postings. Structured document, section, and code-block entities remain available as anchors, with a small bounded lexical allowance where the provider needs it for their identity. Whole-body discovery no longer depends on storing every term.

## Bound the source search

`weave explore RESEARCH PHRASE` extracts normalized identifier terms, removes ordinary question words and terms shorter than four characters, and caps the search set at eight. It then invokes ripgrep with fixed-string matching, smart case, line and column output, repository ignore handling, a 1 MiB per-file ceiling, and explicit exclusions for `.git`, `vendor`, and `node_modules`.

The subprocess output is capped at 1 MiB. Lines are deduplicated, previews are trimmed and limited to 240 bytes, and results receive a simple deterministic score from term overlap in the path and line. The selection first takes the strongest hit from different files, then fills remaining positions by score. This prevents one verbose file from consuming the complete discovery bound.

If ripgrep is unavailable or finds nothing, source discovery returns an empty set rather than breaking semantic lookup. A process or parse failure other than an ordinary no-match remains visible.

## Combine pointers, not dossiers

Semantic and lexical results share a small discovery shape. A symbol result names its kind, stable identity, definition coordinate, provider, evidence, and exact next command. A source result names its path, coordinate, and preview. Neither shape includes a complete graph neighborhood or a copied file body.

The combined array is capped by item count and a 12 KiB encoded budget. An agent can choose a semantic follow-up with `weave context STABLE_NAME` or open the reported source line directly. That choice happens before Weave spends response bytes on a complete declaration.

## Keep the earlier benchmark in context

The provider-owned body-term experiment was still useful. In its paired content-research sample, both agents scored 8/8. The Weave arm used 21.3% fewer input tokens, 8.6% fewer output tokens, no filesystem searches, and the same command count, but finished 1.90 seconds slower. That result showed the value of content discovery without proving that body postings were the right implementation.

The later storage and payload audit supplied the missing cost evidence. Removing broad postings and making discovery progressive reduced the representative database from 1,034,616,832 bytes to 16,777,216 bytes and the representative first-stage response from 171,537 bytes to 3,157 bytes. The current design keeps the successful behavior, finding prose concepts, while using the worktree's existing text-search surface instead of maintaining another one.

The practical principle is that an index does not have to answer every question internally. It has to get the caller to trustworthy evidence with less work than direct rediscovery. For source-body terms, a compact semantic outline plus bounded ripgrep is the smaller and clearer composition.
