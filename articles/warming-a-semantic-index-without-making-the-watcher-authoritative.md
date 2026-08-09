<!-- Generated from https://thefellow.github.io/articles/warming-a-semantic-index-without-making-the-watcher-authoritative/ by scripts/generate_llm_content.py; do not edit. -->

# Warming a Semantic Index Without Making the Watcher Authoritative

Source: [https://thefellow.github.io/articles/warming-a-semantic-index-without-making-the-watcher-authoritative/](https://thefellow.github.io/articles/warming-a-semantic-index-without-making-the-watcher-authoritative/)

## Pyramid summary

- **~2 words:** Optional watch warming
- **~8 words:** One polling loop warms the same query-authoritative freshness pipeline.
- **Expanded:** How Weave uses an optional foreground polling loop to coalesce edits and warm the same query-authoritative freshness pipeline without installing a daemon, hook, or second indexer.

## Full content

**Part 8 of [Building Weave](/series/weave.md).**

[Query-driven freshness](/articles/keeping-a-semantic-index-fresh-without-a-daemon.md) gives Weave a simple authority rule: every database-backed question proves the current Git and provider state before reading the format-5 navigation index. That rule remains correct when no background process exists. Its tradeoff is latency. The first question after an edit can inherit provider startup, normalization, and publication work.

An optional watch mode can move that work earlier, but it can also quietly damage the architecture. If filesystem events decide what is current, if the watcher owns a second incremental indexer, or if queries trust the transient broker instead of checking for themselves, the latency optimization has become a new correctness boundary.

[`weave watch`](https://github.com/TheFellow/weave) stays smaller than that. It is an optional foreground polling warmer over the same freshness manager queries already use. It owns no graph, installs no hook, starts no daemon, and publishes nothing directly.

<figure class="article-figure">
  <img src="/assets/images/articles/weave/watch-mode-warming.svg" alt="Ordinary queries and an optional foreground watch loop both enter the same query-authoritative freshness manager. The watcher periodically obtains an exact opaque Git observation token. Current observations do nothing; stale observations call the same non-forced Ensure operation. The shared per-worktree writer lock, provider pipeline, unchanged-state checks, database generation, and atomic manifest publication remain the only refresh path. Successful, refreshed, and recoverable error events are emitted without affecting authority.">
  <figcaption>The watcher changes when refresh work starts, not who decides whether the graph is current. Queries keep checking the same authoritative path.</figcaption>
</figure>

## Optimize latency without changing authority

The first invariant is almost aggressively ordinary: queries continue to call `Freshness.Ensure`. A running watcher is neither required nor consulted as proof. If it refreshed the graph just before a query, the query's check is cheap. If it stopped, failed, or never existed, the query follows exactly the same path it always did.

The watcher uses that same `Ensure(false)` operation. It cannot force a refresh that the coordinator considers unnecessary, bypass the per-worktree writer lock, write graph records itself, or publish a freshness manifest. A foreground query and the warmer may race to help, but the shared lock and second inspection inside `Ensure` ensure only one performs the work.

This also keeps failure semantics unchanged. The generation marker is invalidated before bounded storage replacement and installed only after complete graph publication. The manifest is written last. A watcher failure cannot bless a partial graph because the watcher has no alternative publication mechanism.

## Poll the exact observation, not a second file inventory

Native filesystem notifications look like the obvious implementation. They are useful hints, but a portable watcher still has to handle recursive directory discovery, atomic-save renames, editor backup files, branch and index changes, buffer overflow, finite watch counts, network filesystems, ignored paths, and linked worktrees. After handling all of that, it still needs an exact reconciliation pass.

Weave already has that pass. Repository inspection uses Git porcelain v2 with all untracked paths, hashes changed regular files, resolves shared and per-worktree Git paths correctly, and includes provider identity plus build-relevant input fingerprints in freshness. Background `git status` runs with `--no-optional-locks` so it does not take optional Git locks merely to observe state.

The freshness manager exposes an opaque observation token over repository identity, worktree identity, provider, commit, tree, branch or detached state, and the exact overlay digest. The watch loop may compare tokens for equality but does not parse them. Ignored file noise remains ignored, a branch switch is visible, an atomic rename becomes one resulting state, and linked worktrees retain separate manifests, databases, and locks without watch-specific path logic.

`Observe` is deliberately cheaper than the complete query check. It compares Git, provider, and published manifest state but does not open the graph database to verify its generation on every poll. A current observation suppresses unnecessary warmer work; it does not become proof that a reader may trust the database. The initial non-forced refresh, any stale refresh, and every ordinary query continue through `Ensure` or `Inspect`, where graph generation is verified.

Polling has a cost: every interval runs an exact Git observation, and currently changed regular files are hashed. Very large untracked worktrees may need a longer interval. That cost is explicit and configurable rather than hidden behind a native event subsystem that still requires reconciliation.

## Let one loop coalesce the edit burst

The default interval is 750 milliseconds, bounded between 50 milliseconds and five minutes. It is both the observation cadence and the edit-coalescing window. By default, startup performs one non-forced refresh and emits a ready event. `--initial=false` performs a read-only observation instead and defers warming until a poll finds stale state.

Each tick asks for one observation. A current status produces no output and no provider work. A stale status calls `Ensure(false)`. There is no worker pool. While a refresh is running, Go's ticker may collapse pending ticks into its bounded channel. That is desirable because the finished Git state subsumes the intermediate write, rename, and backup events an editor produced.

At most one refresh runs through this loop, and the ordinary worktree lock covers concurrency with other processes. A new edit that arrives during provider work is caught by the existing unchanged-state check. The attempted refresh fails rather than publishing a mixed generation, and the next observation sees the new token and retries against the resulting state.

This is a much stronger model than replaying filesystem events as commands. Events answer “something happened.” The observation answers “this is the exact state now.”

## Retry evidence, not just time

A broken provider should not run at every poll forever. After a recoverable observation or refresh failure, the watcher emits an error and associates the failure with the observation that produced it. If the same token remains, retry delay doubles from the poll interval up to a 30-second cap. Logs stay bounded and expensive failures stop hammering the machine.

A new observation is new evidence. It bypasses the old state's remaining backoff and is immediately eligible for refresh. Fixing a configuration file or changing the source does not have to wait for a retry schedule derived from a state that no longer exists.

Repository disappearance is different from a transient provider error and terminates the loop. Context cancellation is graceful. The process entry point converts interrupt and termination signals into the same context passed through observation, Git subprocesses, providers, and storage work, while the loop owns and stops its ticker on every return path.

## Make a foreground process scriptable

Human output stays quiet when nothing changes. A ready or refreshed line goes to stdout with repository identity, worktree identity, state, and changed-path count. Provider diagnostics and recoverable errors go to stderr.

`--json` emits newline-delimited `weave.watch-event/v1` records. Each invocation owns a monotonic sequence number, and event types are `ready`, `refreshed`, or `error`. A trigger distinguishes initial work, a changed observation, and a retry. Successful records carry the observed token and freshness status; error text is made valid UTF-8 and capped at 8 KiB without pretending the graph became current.

The stream is intentionally an observation surface, not a command protocol or durable log. Restarting the process restarts its sequence. Current-state polls do not create heartbeat noise. Consumers that care about the graph still ask Weave, whose query path performs its own freshness proof.

## Leave native events as an optimization layer

Polling is not declared universally faster than native notification. It is the smallest cross-platform design that preserves the existing truth boundary and handles Git state, ignored paths, atomic saves, linked worktrees, event loss, and overflow through one tested observation.

If measurements show periodic Git inspection is material at repository scale, native events can wake the same reconciliation loop earlier. They still cannot replace periodic or query-time exact checks. The watcher may reduce latency; only the freshness coordinator can establish currency.

There are two other explicit boundaries. The loop observes the provider input universe already represented by Git freshness. An explicitly imported unmanaged SCIP file remains unmanaged. Setting `WEAVE_DATABASE` also selects an unmanaged database snapshot, so watch mode is unavailable in that mode. Optional warming does not expand the system's authority merely because a process stays alive.
