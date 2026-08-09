---
title: "Finding Source Bodies Without Indexing Them"
date: 2026-08-07 21:13:49 -0700
last_modified_at: 2026-08-09 10:00:00 -0700
excerpt: "How Weave format 5 combines semantic anchors with bounded ripgrep over current source."
permalink: /articles/making-source-bodies-discoverable-without-copying-them/
series: weave
series_order: 13
order: 17
featured: true
status: "Weave, part 13"
icon: "search-code"
accent: "#fab005"
topics: ["Code navigation", "Search", "Performance"]
---

{% include series-notice.html %}

A declaration index cannot find a concept mentioned only in a comment or paragraph. Format 5 solves that gap without storing a second vocabulary: semantic lookup finds known entities, while ripgrep searches current source.

<figure class="article-figure">
  <img src="{{ '/assets/images/articles/weave/source-body-discovery.svg' | relative_url }}" alt="A research phrase becomes a small fixed-string term set. The format-5 navigation index supplies declaration and document anchors while one bounded ignore-aware ripgrep pass supplies current path, line, column, and preview hits. Results are diversified and bounded before exact context is opened.">
  <figcaption>Keep identities indexed and search body text where it already lives.</figcaption>
</figure>

## Keep the index semantic

Format 5 stores declaration and document names, stable identities, source ranges, and retained navigation relationships. It stores no body terms, code-block entities, generic file anchors, embeddings, or source text.

## Bound source search

`weave explore RESEARCH PHRASE`:

- removes stop words and terms shorter than four characters;
- uses at most eight fixed-string terms;
- respects repository ignore rules;
- excludes `.git`, `vendor`, and `node_modules`;
- rejects files larger than 1 MiB;
- caps ripgrep output at 1 MiB; and
- ranks and diversifies matching lines across files.

Missing ripgrep or no matches is a soft miss. Semantic lookup still works.

## Return pointers, then context

Semantic results carry an exact `weave context` follow-up. Source results carry a path, line, column, and short preview. The combined discovery array has both an item limit and a 12 KiB encoded ceiling.

The caller chooses a target before Weave opens more source. This keeps the database, search, and agent payload focused on navigation.
