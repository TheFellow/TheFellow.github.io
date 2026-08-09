<!-- Generated from https://thefellow.github.io/articles/weave-progressive-discovery/ by scripts/generate_llm_content.py; do not edit. -->

# Progressive Discovery Returns to Source

Source: [https://thefellow.github.io/articles/weave-progressive-discovery/](https://thefellow.github.io/articles/weave-progressive-discovery/)

## Pyramid summary

- **~2 words:** Progressive discovery
- **~8 words:** Small semantic and source pointers precede exact context.
- **Expanded:** Weave selects small semantic and text clues before opening exact source context.

## Full content

**Part 4 of [Building Weave](/series/weave.md).**

Format 5 separates finding a promising target from reading it. This keeps initial answers small while preserving direct access to authoritative source.

![Small discovery results leading to selected source](/assets/images/articles/weave/source-rich-context.svg)

`weave explore QUERY` combines declaration and document anchors with bounded, ignore-aware ripgrep results. The encoded discovery set has a hard 12 KiB budget and includes commands for the next step.

`weave context TARGET` then resolves one target and returns a bounded source excerpt. Markdown sections expand naturally, while code stays anchored to its current file and range.

Graph questions remain graph questions. Dependencies, paths, impact, and architecture use retained relationships; source wording and implementation details come from the worktree. This division is the practical center of format 5.

[Continue to graph inspection](/articles/weave-graph-inspection-and-links.md)
