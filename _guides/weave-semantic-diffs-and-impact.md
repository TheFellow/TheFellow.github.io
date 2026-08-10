---
title: "Compare Navigation Facts Across Git States"
date: 2026-08-09 10:36:00 -0700
last_modified_at: 2026-08-10
excerpt: "Semantic diff and impact compare bounded navigation evidence without mutating the worktree."
permalink: /articles/weave-semantic-diffs-and-impact/
series: weave
series_order: 7
order: 7
status: "Weave, part 7"
featured: true
icon: "compare"
accent: "#ffd43b"
topics: ["Semantic diffs", "Git", "Impact analysis"]
image: /assets/images/articles/weave/semantic-snapshot-diff.svg
---

{% include series-notice.html %}

Git changes are easier to review when file edits and navigation changes remain distinct. Weave builds exact semantic sides and reports added, removed, or changed declarations and retained relationships.

![Two Git snapshots producing a semantic diff](/assets/images/articles/weave/semantic-snapshot-diff.svg)

Historical sides use isolated immutable worktrees. The current side can include local edits, and the caller's worktree is never checked out or rewritten.

`weave impact` starts from changed files, packages, declarations, or a Git diff and traverses only relationships format 5 actually retains. Test impact therefore relies on explicit test relationships, not inferred calls or references.

Source inventory changes are reported separately from semantic changes. That keeps the evidence honest when a file moves or changes without altering the navigation profile.

[Continue to federation](/articles/weave-federated-queries/){: .btn .btn--primary }
