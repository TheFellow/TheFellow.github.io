<!-- Generated from https://thefellow.github.io/articles/turning-cross-repository-soaks-into-indexing-contracts/ by scripts/generate_llm_content.py; do not edit. -->

# Turning Cross-Repository Soaks into Indexing Contracts

Source: [https://thefellow.github.io/articles/turning-cross-repository-soaks-into-indexing-contracts/](https://thefellow.github.io/articles/turning-cross-repository-soaks-into-indexing-contracts/)

## Pyramid summary

- **~2 words:** Cross-repository indexing soak
- **~8 words:** A mixed-language matrix validates the format-5 provider contract.
- **Expanded:** How Weave validates format-5 providers across real repositories without weakening bounds, freshness, or source safety.

## Full content

**Part 15 of [Building Weave](/series/weave.md).**

Small fixtures prove protocol rules. A mixed repository soak proves that the same rules survive real project layouts, toolchains, and source volumes.

<figure class="article-figure">
  <img src="/assets/images/articles/weave/cross-repository-indexing-soak.svg" alt="Mixed-language repositories enter isolated prepared clones. A format-5 Weave build indexes offline, runs bounded queries, verifies the navigation index, exports it, records time, memory, database size, and retained fact counts, and confirms that source did not change.">
  <figcaption>The soak tests the complete format-5 publication path, not only compiler startup.</figcaption>
</figure>

## Prepare outside the measurement

Dependency download, restore, and required reference builds happen before timing. The measured index run is offline and may not mutate the checkout. This separates provider work from network and package-manager variance.

## Exercise the public contract

Each repository run performs:

1. a cold format-5 index;
2. ordinary current no-change queries;
3. `weave verify`;
4. a deterministic export; and
5. a source-status comparison.

The harness records elapsed time, peak process-tree memory, database bytes, units, documents, retained symbols, and retained navigation edges. Occurrence and statement-edge counts are not part of the format-5 contract.

## Treat repository shape as input

The matrix must cover nested workspaces, multiple build systems, generated compiler documents, mixed languages, standalone fixtures, and repositories with missing optional tooling. Discovery must reject ambiguity instead of choosing a project silently.

## Keep failures explicit

A timeout, denied permission, missing toolchain, malformed adapter frame, incomplete unit inventory, or source mutation fails the run. No partial manifest is published. Unsupported repositories remain named residuals rather than disappearing from the report.

The soak succeeds when every supported provider produces the same small navigation profile reproducibly, within bounds, without changing source.
