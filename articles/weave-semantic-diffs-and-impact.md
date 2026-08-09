<!-- Generated from https://thefellow.github.io/articles/weave-semantic-diffs-and-impact/ by scripts/generate_llm_content.py; do not edit. -->

# Compare Navigation Facts Across Git States

Source: [https://thefellow.github.io/articles/weave-semantic-diffs-and-impact/](https://thefellow.github.io/articles/weave-semantic-diffs-and-impact/)

## Pyramid summary

- **~2 words:** Semantic changes
- **~8 words:** Exact Git sides produce bounded diff and impact evidence.
- **Expanded:** Semantic diff and impact compare bounded navigation evidence without mutating the worktree.

## Full content

**Part 7 of [Building Weave](/series/weave.md).**

Git changes are easier to review when file edits and navigation changes remain distinct. Weave builds exact semantic sides and reports added, removed, or changed declarations and retained relationships.

![Two Git snapshots producing a semantic diff](/assets/images/articles/weave/semantic-snapshot-diff.svg)

Historical sides use isolated immutable worktrees. The current side can include local edits, and the caller's worktree is never checked out or rewritten.

`weave impact` starts from changed files, packages, declarations, or a Git diff and traverses only relationships format 5 actually retains. Test impact therefore relies on explicit test relationships, not inferred calls or references.

Source inventory changes are reported separately from semantic changes. That keeps the evidence honest when a file moves or changes without altering the navigation profile.

[Continue to federation](/articles/weave-federated-queries.md)
