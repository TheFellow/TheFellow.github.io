<!-- Generated from https://thefellow.github.io/articles/weave-federated-queries/ by scripts/generate_llm_content.py; do not edit. -->

# Federate Fresh Worktrees

Source: [https://thefellow.github.io/articles/weave-federated-queries/](https://thefellow.github.io/articles/weave-federated-queries/)

## Pyramid summary

- **~2 words:** Federated navigation
- **~8 words:** Fresh worktrees select one disposable aggregate generation.
- **Expanded:** Cross-repository queries refresh selected worktrees before using a disposable aggregate.

## Full content

**Part 8 of [Building Weave](/series/weave.md).**

Weave can query a bounded set of cataloged repositories without making a hosted graph authoritative. Each selected worktree passes its normal freshness gate first.

![Fresh worktree generations forming a machine aggregate](/assets/images/articles/weave/machine-aggregate.svg)

The generation identities form a deterministic aggregate key. A matching immutable aggregate can answer the query quickly; otherwise Weave builds one or falls back to authoritative federation over the refreshed member databases.

Aggregates live outside Git and are safe to delete. Missing or unhealthy members are reported as partial results rather than hidden.

Source context remains repository-local. Federation helps choose the repository and target, then `weave context` reopens source under that repository's own bounds and freshness rules.

[Continue to local acceleration](/articles/weave-local-acceleration.md)
