---
title: "Shrinking a Semantic Graph into a Navigation Index"
date: 2026-08-07 12:45:59 -0700
last_modified_at: 2026-08-08 13:10:00 -0700
excerpt: "How Weave cut a repository index by 98.38% by retaining navigation anchors and high-value relationships instead of treating every compiler event as durable product data."
permalink: /articles/shrinking-a-semantic-graph-without-changing-its-meaning/
series: weave
series_order: 6
order: 10
featured: true
status: "Weave, part 6"
icon: "layers"
accent: "#22b8cf"
topics: ["Storage design", "Code navigation", "Performance"]
---

{% include series-notice.html %}

The first storage correction in Weave changed representation while preserving an exhaustive graph. Numeric identities, interned strings, and narrower records reduced one large index from 7.54 GB to 1.11 GB. That was useful engineering, but it did not answer the more important product question: why should a local navigation tool store hundreds of compiler events for every byte of source?

The later audit answered by changing the retained contract. [Weave](https://github.com/TheFellow/weave) format 4 is a navigation index, not a compiler-event archive. Compilers and adapters may still produce rich facts during analysis, but persistence keeps only the anchors and relationships that reliably move a person or agent toward the right source.

<figure class="article-figure">
  <img src="{{ '/assets/images/articles/weave/compact-storage.svg' | relative_url }}" alt="Language and content providers emit normalized facts. A format-4 navigation projection retains documents, package and declaration anchors, and high-value dependency, implementation, test, generation, documentation, link, and embed edges. It drops occurrences, calls, references, containment duplication, fields, constants, locals, and token postings. The compact database points discovery back to current source.">
  <figcaption>The decisive reduction came from narrowing the durable product contract, then compacting the representation that remained.</figcaption>
</figure>

## Measure amplification, not fact counts

The representative repository contained 3,019,968 bytes outside `.git`. Its format-3 database occupied 1,034,616,832 bytes, or 342.6 times the source size. The database held 25,678 symbols, 184,826 occurrences, and 247,013 edges. A deterministic JSON export alone was 247,371,432 bytes.

Those numbers showed that the index was duplicating statement-level evidence more expensively than the source itself. A call or reference row still needed identities, ranges, ownership, evidence, indexes, and storage overhead. Most of that data was then serialized again when an agent asked a broad discovery question.

## Retain the navigation layer

Format 4 keeps:

- units and documents needed for source identity and freshness;
- repository, content, package, type, function, method, test, and unknown provider-defined anchors;
- imports, dependencies, extension and implementation relationships, tests, generation, documentation, exposure, links, and embeds; and
- the compound name indexes used by exact and prefix navigation.

It drops occurrences, statement-level calls and references, definition and containment edges, variables, fields, constants, builtins, locals, and broad content-token postings. Declaration ranges on retained symbols remain enough for `definition` and exact `context` follow-ups. Current source and bounded ripgrep recover the lower-level detail after discovery has selected a useful area.

This is a change in meaning, and naming it matters. The earlier storage-v2 work proved that a private encoding could become smaller without changing public facts. Format 4 makes a different trade: exhaustive compiler events are no longer part of the managed query contract. Commands and edge filters now advertise only relationships the navigation projection actually retains.

## Project before publishing

Each provider still owns its analysis boundary. The storage projection runs after normalization, filters noisy symbol kinds and relationship families, clears unnecessary search terms, and publishes only the retained facts. A clean refresh compacts the closed database before installing its manifest.

This keeps adapter protocols independent from one storage experiment. A precise provider can expose richer facts to validation or future consumers without forcing every worktree database to retain them indefinitely. The local index pays for the product surface that current queries use.

## Follow the evidence back to source

The smaller index works with progressive discovery. `weave explore` returns a few semantic anchors plus diversified ripgrep hits, each with a path and source coordinate. A semantic result includes the exact `weave context` command for opening the selected declaration. The first response is bounded by both item count and encoded bytes.

This division uses each mechanism where it is strongest. Compiler-backed identities select packages, types, functions, and relationships that plain text cannot resolve reliably. Ripgrep finds statement-level words in current files cheaply. `context` reads source only for the selected anchor. The graph stops trying to be a compressed copy of the repository.

## Verify the practical result

On the same repository and commit, format 4 produced a 16,777,216-byte database with 6,269 symbols, no occurrences, and 9,535 retained edges. That is 5.56 index bytes per source byte and a 98.38% reduction from format 3. A forced refresh completed in 10.2 seconds.

The response boundary improved with it. The representative `explore --json` result fell from 171,537 bytes to 3,157 bytes. Selecting its first anchor produced a 3,195-byte `context --json` response containing 337 bytes of current source. These are controlled measurements from one repository, but they test the actual product constraints: disk amplification and useful evidence placed into an agent's context.

The lesson is simpler than another record-layout optimization. A derived local index should retain what makes navigation faster, point precisely back to source, and stay cheap enough to rebuild. Everything else has to earn its persistent cost.
