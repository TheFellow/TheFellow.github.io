<!-- Generated from https://thefellow.github.io/articles/making-source-bodies-discoverable-without-copying-them/ by scripts/generate_llm_content.py; do not edit. -->

# Making Source Bodies Discoverable Without Copying Them

Source: [https://thefellow.github.io/articles/making-source-bodies-discoverable-without-copying-them/](https://thefellow.github.io/articles/making-source-bodies-discoverable-without-copying-them/)

## Pyramid summary

- **~2 words:** Body concept discovery
- **~8 words:** Bounded lexical hints find exact content entities without copying source text.
- **Expanded:** How Weave attaches bounded provider-owned lexical terms to exact content entities, retrieves prose and unsupported files through the existing graph, and still reads current source only at query time.

## Full content

**Part 13 of [Building Weave](/series/weave.md).**

A structured-content index can know that a Markdown heading exists and still fail the question written below it. Weave already gave every document, section, code block, link, route, and asset an exact graph identity. Symbol search posted the display name of each entity. An agent asking about a concept stated only in prose could therefore miss the right section unless the author happened to repeat that concept in its heading.

Copying every source file into a second full-text database would solve a different problem by creating a second authority. [Weave](https://github.com/TheFellow/weave) instead extends the normalized entity with a bounded provider-owned lexical projection. A body concept discovers the same section, file, or code block that already carries provenance and an exact stable identity. Structured entities retain their source coordinates. A generic file keeps its exact path, and exploration finds the strongest matching line in the current file at query time. The graph never becomes the source-text authority.

<figure class="article-figure">
  <img src="/assets/images/articles/weave/source-body-discovery.svg" alt="A workspace provider reads bounded Git-visible content and attaches normalized lexical terms to exact document, section, code-block, and generic-file entities. The existing bstore token postings retrieve those identities without storing source text or inventing semantic edges. Explore ranks and diversifies the candidates. Structured entities then use the ordinary context path to return bounded definitions, while a generic file is reopened and scanned for the current line with the strongest query-term overlap.">
  <figcaption>Lexical terms make an exact entity discoverable. They do not become source, relationships, positions, or semantic evidence. The current worktree still supplies every returned line.</figcaption>
</figure>

## Put discovery hints on exact entities

Normalized graph schema 2 adds optional `search_terms` to a symbol. Each term is one lowercase normalized identifier token, sorted and unique. A term can be at most 128 bytes, and one entity can carry at most 2,048 terms. Providers must derive the set deterministically from input they own.

Those constraints make the field a compact query projection rather than an invitation to hide a document store inside every symbol. The workspace provider can say that the exact `README.md#controlled-paired-arm-proof-run` section discusses `rubric`, `tokens`, and `artifacts`. It cannot use those words to claim a call, dependency, contract, or stronger evidence class.

The public distinction matters for language adapters too. A compiler or SCIP producer remains responsible for declarations and references it can prove. An adapter may supply deterministic lexical terms for one of its own entities, but those terms never upgrade syntax into compiler truth. The protocol validates the same normalized, bounded shape before facts enter the graph.

## Extract terms at the provider boundary

Markdown has useful structure, so its extraction follows that structure:

- the document entity receives terms from front matter, title, series, topics, tags, categories, and the prelude before the first heading;
- a heading receives terms from its direct body through the next heading;
- a fenced code block receives terms from its own bounded content; and
- identical section names are diversified during exploration so generated copies do not consume the complete result bound.

The section boundary is deliberate. A parent heading does not absorb the complete nested document and become a giant duplicate candidate. Each entity remains discoverable through the text it directly owns, while ordinary containment edges preserve the hierarchy.

Evidence follows the content's origin. A document with an explicit generated-from marker, plus the conventional `llms.txt` and `llms-full.txt` aggregations, gives its document, section, occurrence, containment, and code-block facts `generated` evidence. Authored Markdown remains `syntactic`. Retrieval can therefore distinguish a canonical authored explanation from a generated copy without guessing from its path later.

The safe fallback also covers Git-visible regular UTF-8 files that are not Markdown or known assets. Files up to 2 MiB contribute bounded terms regardless of extension, making comments, configuration, scripts, and unsupported language files discoverable by exact path identity. This fallback does not invent a parsed definition or persist source coordinates. Files with NUL bytes, invalid UTF-8, asset profiles, excessive size, or content beyond the aggregate 512 MiB lexical budget retain their topology without guessed text.

## Reuse the existing inverted projection

Storage format 3 persists the term set beside the compact symbol record and emits the same bstore token postings used for display-name lookup. `symbols` and `explore` therefore retrieve an ordinary entity ID. Logical export and the disposable [machine-wide aggregate](/articles/caching-a-federated-graph-without-weakening-freshness.md) preserve the terms so local and catalog discovery have the same meaning.

There is no phrase index, stemming service, BM25 corpus, embedding store, or separate query language. Search terms widen how an entity can be found; the normalized graph still defines what was found. Exploration scores how many query terms a candidate covers and how discriminating each posting is. A term found in four entities contributes more than a truncated posting shared across hundreds. Complete coverage earns a bounded bonus only when at least three terms match and the candidate vocabulary is narrow enough to make that coverage meaningful.

Broad content pays a specificity cost proportional to the number of indexed terms, and generated content receives an additional penalty. That keeps an `llms-full.txt` aggregation containing nearly every word from defeating the smaller authored section that actually explains the question. When three or more strong content candidates belong to the same document, a modest document-scope boost keeps those related sections together instead of interleaving nearby noise from unrelated files. Normal query responses strip the potentially large internal term set because repeating hundreds of discovery tokens adds no evidence after the entity and source are known. Deterministic diagnostic export retains it.

Advancing the private and normalized schema markers makes the change explicit. An older derived index is rejected with the normal remove-and-reindex guidance. Stable entity identities and authored declarations do not migrate because they did not change. The disposable projection is rebuilt from source.

## Find the current lines without storing positions

Discovery is useful when the first result contains enough evidence to continue. [`weave explore`](/articles/composing-source-rich-context-without-a-second-index.md) already expands a Go function or method definition to its complete parsed declaration when the shared source budget permits. It now gives Markdown the same treatment. A document result returns its front matter and prelude through the first heading. A section begins at the matched heading and continues through its descendants until the next heading at the same or higher level. Front matter is masked only while the current document is parsed for heading positions, preserving line coordinates while preventing YAML from becoming accidental Markdown structure.

That expansion remains a query-time source operation. The loader rejects unsafe paths, symlinks, ignored files, changed hashes, invalid encodings, invalid ranges, and exhausted budgets exactly as it does for every other context result. If the expanded section does not fit, the response falls back to the indexed range rather than returning partial source that looks complete.

A generic file has no provider-parsed definition and the graph stores no term positions. Exploration therefore passes its normalized query terms into the context composition. The source loader reopens the current file, tokenizes each current line, scores term and mechanical suffix overlap, and anchors the excerpt at the strongest line. Normal context-line and byte budgets apply around that anchor. A stale posting can at worst lead to a current file whose concepts have moved or disappeared; it cannot make Weave return cached text or old coordinates as current evidence.

## Keep long research questions lexical

A long natural-language question should not spend its first lookup pretending the complete sentence might be a symbol name. Short inputs still take the exact resolver path, preserving the convenient one-entity result. Questions over twelve whitespace-delimited words or 512 bytes move directly to lexical retrieval.

Exploration now retains up to 32 useful terms, removes research-language stop words, and avoids giving the first surviving term the same dominant weight it receives in a short symbol-shaped query. A few mechanical variants cover common `s`, `es`, `ies`, `ed`, and `ing` endings, but variants of one term contribute only the best match instead of multiplying its score. Stable-name and path matches provide durable scope evidence for every term. Rarity, coverage, content specificity, document scope, and evidence origin refine the lexical score. Candidate kind weights keep functions, methods, types, sections, and code blocks ahead of low-value asset and URL entities; method-container, GUI/TUI, and repeated-content diversification then protect the bounded result from one prolific family.

The algorithm remains intentionally plain. It is inspectable enough to change when a real research task exposes a ranking failure, and deterministic enough for the same indexed facts and question to produce the same candidate order.

## Carry unchanged lexical units forward

Reading every generic file after every small edit would turn a useful fallback into a permanent tax. On the first index or a forced refresh, the provider builds the bounded lexical projection from the complete eligible inventory. On later refreshes it asks Git for paths changed since the previous commit and rereads only changed or new generic files. Unchanged file units carry their prior fingerprints and terms into the new manifest.

Markdown remains parsed through its structured-content path because headings, links, routes, and other surfaces can change independently. Generic files retain one unit per path. Deleted paths disappear through the same unit-replacement contract used by the rest of freshness.

## Test body discovery against complete research

The implementation returned to the paired benchmark that exposed the gap. Both agents had to explain the existing measurement argument from concepts buried in the GitHub Pages prose. Both answers scored 8/8. The Weave arm needed one `explore` call and one targeted source read; the control needed two filesystem searches and one source read. Weave used 21.3% fewer input tokens and 8.6% fewer output tokens, removed filesystem search, and finished 1.90 seconds slower. Command and source-read counts were equal.

That mixed result is more useful than a retrieval-only win. It shows that body terms can replace broad discovery without claiming that one content workload became universally faster. The final candidate returned eight coherent authored guide entities covering the paired result, benchmark question, product corrections, document premise, recorded losses, consolidation caveat, experimental controls, and supporting flow. Broad generated copies no longer displaced the focused authored sections.

A separate Mixology probe tested the generic-file path. The question about “publication lifetime independently from background work” ranked `pkg/toolkits/gui/dispatcher.go` first and anchored the dossier at the exact matching comment on lines 25–26. The file entity retained its compiler-derived `defines` relationships. Lexical fallback found the line; it did not replace the semantic facts surrounding the file.

This is the useful middle ground between filename-only navigation and a second source database. A concept in prose or an unsupported file can lead an agent to an exact graph entity, path, and current bounded excerpt. Provider ownership, bounded terms, explicit evidence, disposable storage, and query-time source verification keep that convenience inside Weave's existing truth model.
