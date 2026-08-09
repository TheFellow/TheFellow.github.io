<!-- Generated from https://thefellow.github.io/articles/weave-local-acceleration/ by scripts/generate_llm_content.py; do not edit. -->

# Keep Acceleration Optional

Source: [https://thefellow.github.io/articles/weave-local-acceleration/](https://thefellow.github.io/articles/weave-local-acceleration/)

## Pyramid summary

- **~2 words:** Local acceleration
- **~8 words:** Watch, sessions, and brokers reuse authoritative state.
- **Expanded:** Watch, sessions, and the transient broker reuse state without weakening freshness.

## Full content

**Part 9 of [Building Weave](/series/weave.md).**

Weave's fast paths reuse authoritative local state. They do not create a second consistency model.

![Several queries sharing one bounded local session](/assets/images/articles/weave/resident-query-session.svg)

`weave watch` is an optional foreground warmer. `weave session` gives a host an explicit framed query process. On Unix, a transient per-worktree broker can amortize startup for ordinary bounded reads and reaps itself when idle.

Every path still applies the freshness contract before answering. Maintenance and mutation commands drain resident readers before taking ownership, and callers can disable the broker when one process per command is preferable.

This is the final shape of format 5: a small disposable index, authoritative source, and optional acceleration that can always be removed without changing meaning.

[Return to the Weave project](/projects/weave.md)
