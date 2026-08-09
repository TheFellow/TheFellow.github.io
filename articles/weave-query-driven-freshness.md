<!-- Generated from https://thefellow.github.io/articles/weave-query-driven-freshness/ by scripts/generate_llm_content.py; do not edit. -->

# Freshness Belongs on Every Weave Read

Source: [https://thefellow.github.io/articles/weave-query-driven-freshness/](https://thefellow.github.io/articles/weave-query-driven-freshness/)

## Pyramid summary

- **~2 words:** Fresh navigation
- **~8 words:** Every read proves current Git and provider state.
- **Expanded:** Every query proves that its navigation facts match the current worktree and providers.

## Full content

**Part 2 of [Building Weave](/series/weave.md).**

Weave checks freshness when a read begins. Users do not need to remember a separate indexing step, and a background process is never the authority.

![A query passing through a freshness gate](/assets/images/articles/weave/fresh-query.svg)

The gate compares current Git state, provider capabilities, configuration, and source observations with the published manifest. Changed provider units rebuild atomically before the query opens the database.

Publication matters as much as detection. A new unit and its manifest become visible together, so readers see either the previous complete generation or the next complete generation.

Caches and warm processes may reduce the cost of this check. They cannot skip it. The simple promise is that every answer describes the worktree the caller is actually using.

[Continue to language adapters](/articles/weave-language-adapters.md)
