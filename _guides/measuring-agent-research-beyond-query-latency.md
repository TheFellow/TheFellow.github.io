---
title: "Measuring Agent Research Beyond Query Latency"
date: 2026-08-07 17:54:48 -0700
last_modified_at: 2026-08-07 17:54:48 -0700
excerpt: "A Weave dogfood run traces menu readiness through Mixology, records every fallback, turns agent friction into product changes, and separates useful evidence from savings claims that still need a control arm."
permalink: /articles/measuring-agent-research-beyond-query-latency/
series: weave
series_order: 12
order: 16
featured: true
status: "Weave, part 12"
icon: "vial"
accent: "#22b8cf"
topics: ["Coding agents", "Developer tools", "Benchmarks"]
---

{% include series-notice.html %}

A semantic query completing in a second is not yet a useful product result. An agent can receive a fast list of opaque IDs, fail to understand it, and spend the rest of the investigation rediscovering the repository with text search and whole-file reads. Query latency looks excellent while the actual research task changes very little.

[Weave](https://github.com/TheFellow/weave) now measures the larger outcome. Its [first agent-research dogfood record](https://github.com/TheFellow/weave/blob/d975e32da1d44b7defdaf74f1648400e91cd5078/.ai/benchmarks/go-modular-monolith-agent-research.md) gave an unfamiliar agent a concrete question about [Mixology](/projects/go-modular-monolith/), required it to begin with Weave, and recorded every fallback. The run found the right architecture quickly. More importantly, it exposed exactly where the graph still made the agent work around the tool.

## Ask a repository question, not a synthetic lookup

The question crossed domain computation, shared application contracts, two presentation surfaces, publication enforcement, and tests:

> Explain how menu readiness and blocker state flow from domain computation into the GUI and TUI. Identify the central composition function, its direct callers and callees, and the tests most relevant to a behavior change.

This is a useful benchmark because no single symbol answers it. A successful investigation has to connect `AvailabilityCalculator.Readiness` to `queries.Readiness` and `Module.Readiness`, understand the shared `ReadinessReport`, `HasBlockers`, and `RequireReady` contract, then follow `ApplyReadiness` into GUI and TUI presentation. It also has to notice that `Commands.Publish` independently enforces readiness at publication time.

The agent received only the question, the repository path, and an instruction to use the installed `weave` CLI before filesystem tools. It inherited no implementation context from the parent session. It recorded every Weave command, source read, fallback search, and criticism of the tool.

<figure class="article-figure">
  <img src="{{ '/assets/images/articles/weave/agent-research-dogfood.svg' | relative_url }}" alt="An unfamiliar agent begins with a menu-readiness question and a bounded Weave exploration. Exact semantic evidence traces domain readiness through a central ApplyReadiness composition into GUI, TUI, publication enforcement, and tests. Recorded fallbacks and response size reveal friction, which feeds qualified lookup, ranked context, readable output, and future controlled benchmarks.">
  <figcaption>The benchmark follows one real question from bounded semantic evidence through targeted source confirmation. Every fallback becomes product evidence instead of disappearing from the success story.</figcaption>
</figure>

## Follow the evidence into both surfaces

The central topology came from ordinary relationship queries:

```sh
weave callers ApplyReadiness
weave callees ApplyReadiness
weave references HasBlockers
weave symbols RequireReady
```

`callers` and `callees` found the exact `ApplyReadiness` neighborhood with source locations. Symbol and reference queries then located the domain, GUI, TUI, and test seams. The agent reconstructed the readiness flow correctly:

1. `AvailabilityCalculator.Readiness` computes the domain result exposed through `queries.Readiness` and `Module.Readiness`.
2. `ReadinessReport` carries readiness and blocker state through the shared application boundary; `HasBlockers` and `RequireReady` express the two important decisions over it.
3. `ApplyReadiness` turns that shared result into presentation state used by `Presenter.loadReadiness`, `Presenter.permissionsFor`, and `ListViewModel.Update`.
4. `Commands.Publish` checks the same readiness independently, so a presentation decision cannot become the publication authority.
5. Unit, GUI, TUI, and stale-result tests provide the evidence set for a behavior change.

Most Weave queries completed in under 1.5 seconds. The remaining filesystem work was targeted: `sed` read ranges discovered through graph output, one `rg` pass validated references and tests, and `git status` confirmed worktree state. The agent reported that the graph materially reduced broad discovery.

That is a useful qualitative result, but it is not a numeric savings claim. This run had no comparable without-Weave arm. It cannot establish a percentage reduction in time, tool calls, bytes, or tokens.

## Record where the tool lost the agent

The critical part of dogfooding was preserving the friction:

- Ambiguous methods pushed the agent toward opaque graph IDs because natural names such as `AvailabilityCalculator.Readiness` did not resolve.
- A context dossier repeated a specific call and its underlying reference edge for the same endpoint.
- Variable and builtin references crowded flow relationships out of bounded context and caused truncation.
- A batch of broad context queries produced roughly 16,000 tokens. Discovery improved substantially, but context ingestion improved only moderately.
- Default impact traversal escaped through generic methods such as `Update` and `Select`, producing a noisy, truncated blast radius.

None of those problems appears in a query-latency percentile. They appear only when someone uses the output to finish a research task and counts the work the output creates downstream.

## Turn benchmark friction into product behavior

The first four findings produced direct changes to Weave. The shared resolver now accepts concise qualified names such as `AvailabilityCalculator.Readiness`, `Presenter.loadReadiness`, and `ReadinessReport.HasBlockers` as deterministic fallbacks over compiler-qualified stable names. Exact graph IDs, exact stable names, and normal provider ranking still take precedence. Ambiguity errors show candidate stable names and kinds before their internal IDs.

Context relationships now read a bounded surplus, collapse repeated edges by adjacent endpoint, and keep the most useful relationship for each one. Calls rank ahead of contracts, dependencies, authored navigation, state access, containment, and raw references. Local-variable, parameter, and language-builtin references are omitted from the bounded dossier while remaining available in exhaustive graph data. The limit applies after compaction and filtering, which stops low-value evidence from consuming the small response an agent requested.

Text output prefers stable semantic names and source paths. Inside a context dossier it also removes repeated repository and compiler-category prefixes, while JSON preserves full names and opaque IDs for exact follow-up.

`weave explore` turns a research phrase into a bounded ranked set of those same [source-rich context dossiers](/articles/composing-source-rich-context-without-a-second-index/):

```sh
weave explore how menu readiness reaches GUI and TUI
weave explore AvailabilityCalculator.Readiness --limit 6 --relationship-limit 6 --json
```

An exact entity naturally produces one dossier. A phrase becomes at most twelve useful terms plus a few mechanical suffix variants. Ordinary question words disappear, while generic scope terms such as `domain`, `GUI`, and `TUI` refine ranking rather than dominating search when more specific terms exist. Candidates accumulate explicit scores from symbol-search position, display and stable-name matches, scope matches, and kind weights. The default returns at most six entities, independently caps each dossier's occurrence, incoming, and outgoing sections at six, and divides one 64 KiB source budget across all results. Ordering is deterministic by score, stable name, and graph ID. Natural-language reasoning stays in the consuming agent. Weave supplies bounded compiler, SCIP, content, and authored evidence from its existing graph without adding an embedded model or a second persisted search database.

The noisy default impact policy remains open. `weave impact TARGET --kind calls` already supplies a narrow alternative, but changing the default requires evidence across more languages and repositories. One dogfood trace is enough to expose a problem, not enough to declare a universal traversal policy.

## Repeat the task before claiming consolidation

A second fresh agent followed menu-publishing authorization from GUI and TUI action availability through the public module, command middleware, readiness enforcement, and persistence. Its architectural account was correct and it kept the repository clean, but the route required 32 Weave commands, two filesystem searches, one source-file read, and one cleanliness check. The graph again avoided broad discovery; it did not yet provide the intended one-to-four-call research experience.

The initial phrase command failed because `explore` was still only an exact-context alias during that run. That evidence caused the command to become the phrase-to-dossier composition described above. A representative menu-publish question now returns the GUI publish boundary, `Module.Publish`, and `Commands.Publish` in one roughly two-second call on Mixology.

That post-change call is a functional check, not a post-change agent benchmark. A new implementation can show that the intended entities rank together without proving that a fresh agent now finishes the research in fewer calls. The distinction keeps a promising correction from quietly becoming an unsupported savings claim.

## Build the controlled benchmark next

A repeatable agent-facing benchmark needs two comparable arms. Both agents should begin without repository context, receive the same question and constraints, and record:

- whether the final architectural answer is correct;
- total tool calls and elapsed time;
- fallback filesystem searches;
- source files and byte ranges read;
- response bytes and estimated tokens; and
- truncation, ambiguity, and incomplete evidence.

One arm begins with Weave; the other uses the same available filesystem tools without it. Query latency remains worth recording, but only as one component. A fast graph query succeeds when it removes rediscovery while preserving answer quality, not when it merely moves that work to the next tool call.

These runs already did the job honest dogfood should do. They answered real cross-surface questions, made useful evidence visible, kept their uncontrolled design explicit, and changed the product where agents struggled. The next fresh run can now measure whether those corrections reduce the investigation itself.
