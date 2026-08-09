<!-- Generated from https://thefellow.github.io/articles/weave-graph-inspection-and-links/ by scripts/generate_llm_content.py; do not edit. -->

# Inspect the Graph and Author Missing Links

Source: [https://thefellow.github.io/articles/weave-graph-inspection-and-links/](https://thefellow.github.io/articles/weave-graph-inspection-and-links/)

## Pyramid summary

- **~2 words:** Inspectable navigation
- **~8 words:** Bounded graphs and checked-in links share one contract.
- **Expanded:** Bounded graph views and checked-in links make navigation facts visible and reviewable.

## Full content

**Part 5 of [Building Weave](/series/weave.md).**

Navigation facts must be easy to inspect. `weave graph` resolves a target and renders a bounded neighborhood as DOT, JSON, or an interactive local explorer.

![A bounded graph with visible evidence](/assets/images/articles/weave/inspectable-graph.svg)

Each edge carries its kind and evidence. Filters, direction, depth, and result limits keep the answer focused instead of turning the command into an unbounded graph dump.

Some useful relationships cannot be derived from source alone. `weave links` edits reviewed relationships in `.weave/bridges.json`, such as a design section documenting a handler or a schema generating a client. Writes are validated, canonical, atomic, and guarded against stale interactive editors.

Derived and authored edges then flow through the same path, graph, impact, export, and architecture queries.

[Continue to source-only declarations](/articles/weave-source-only-declarations.md)
