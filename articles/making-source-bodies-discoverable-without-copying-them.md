<!-- Generated from https://thefellow.github.io/articles/making-source-bodies-discoverable-without-copying-them/ by scripts/generate_llm_content.py; do not edit. -->

# Finding Source Bodies Without Indexing Them

Source: [https://thefellow.github.io/articles/making-source-bodies-discoverable-without-copying-them/](https://thefellow.github.io/articles/making-source-bodies-discoverable-without-copying-them/)

## Pyramid summary

- **~2 words:** Current-source discovery
- **~8 words:** Format-5 anchors combine with bounded ripgrep.
- **Expanded:** How Weave format 5 combines semantic anchors with bounded ripgrep over current source.

## Full content

**Part 13 of [Building Weave](/series/weave.md).**

A declaration index cannot find a concept mentioned only in a comment or paragraph. Format 5 solves that gap without storing a second vocabulary: semantic lookup finds known entities, while ripgrep searches current source.

<figure class="article-figure">
  <img src="/assets/images/articles/weave/source-body-discovery.svg" alt="A research phrase becomes a small fixed-string term set. The format-5 navigation index supplies declaration and document anchors while one bounded ignore-aware ripgrep pass supplies current path, line, column, and preview hits. Results are diversified and bounded before exact context is opened.">
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
