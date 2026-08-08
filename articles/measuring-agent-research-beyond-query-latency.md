<!-- Generated from https://thefellow.github.io/articles/measuring-agent-research-beyond-query-latency/ by scripts/generate_llm_content.py; do not edit. -->

# Measuring Agent Research Beyond Query Latency

Source: [https://thefellow.github.io/articles/measuring-agent-research-beyond-query-latency/](https://thefellow.github.io/articles/measuring-agent-research-beyond-query-latency/)

## Pyramid summary

- **~2 words:** Agent research dogfood
- **~8 words:** A real repository investigation measures useful evidence, fallbacks, friction, and the product corrections that follow.
- **Expanded:** A paired Weave benchmark traces menu publication through Mixology, preserves every command and answer, scores both arms 8/8, and measures how one source-rich dossier changes the investigation.

## Full content

**Part 12 of [Building Weave](/series/weave.md).**

A semantic query completing in a second is not yet a useful product result. An agent can receive a fast list of opaque IDs, fail to understand it, and spend the rest of the investigation rediscovering the repository with text search and whole-file reads. Query latency looks excellent while the actual research task changes very little.

[Weave](https://github.com/TheFellow/weave) now measures the larger outcome. Its first agent-research dogfood record gave an unfamiliar agent a concrete question about [Mixology](/projects/go-modular-monolith.md), required it to begin with Weave, and recorded every fallback. The run found the right architecture quickly. More importantly, it exposed exactly where the graph still made the agent work around the tool.

## Ask a repository question, not a synthetic lookup

The question crossed domain computation, shared application contracts, two presentation surfaces, publication enforcement, and tests:

> Explain how menu readiness and blocker state flow from domain computation into the GUI and TUI. Identify the central composition function, its direct callers and callees, and the tests most relevant to a behavior change.

This is a useful benchmark because no single symbol answers it. A successful investigation has to connect `AvailabilityCalculator.Readiness` to `queries.Readiness` and `Module.Readiness`, understand the shared `ReadinessReport`, `HasBlockers`, and `RequireReady` contract, then follow `ApplyReadiness` into GUI and TUI presentation. It also has to notice that `Commands.Publish` independently enforces readiness at publication time.

The agent received only the question, the repository path, and an instruction to use the installed `weave` CLI before filesystem tools. It inherited no implementation context from the parent session. It recorded every Weave command, source read, fallback search, and criticism of the tool.

<figure class="article-figure">
  <img src="/assets/images/articles/weave/agent-research-dogfood.svg" alt="An unfamiliar agent begins with a menu-readiness question and bounded Weave evidence. Exact semantic evidence traces domain readiness through a central ApplyReadiness composition into GUI, TUI, publication enforcement, and tests. Recorded friction drives retrieval changes, then an isolated paired benchmark gives both arms the same publication question and scores both 8 out of 8 while measuring fewer tokens, commands, searches, reads, and seconds with Weave.">
  <figcaption>The first trace turns friction into retrieval changes. The paired run then holds the question and correctness rubric constant while measuring the investigation around the answer.</figcaption>
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

`weave explore` turns a research phrase into a bounded ranked set of those same [source-rich context dossiers](/articles/composing-source-rich-context-without-a-second-index.md):

```sh
weave explore how menu readiness reaches GUI and TUI
weave explore AvailabilityCalculator.Readiness --limit 6 --relationship-limit 6 --json
```

An exact entity naturally produces one dossier. A phrase becomes at most 24 useful terms plus a few mechanical suffix variants. Ordinary question words disappear, while generic scope terms refine ranking instead of becoming broad searches when more specific terms exist. Candidate ranking combines symbol-search position, display and stable-name matches, explicit domain scope, presentation scope, and kind weights. It also diversifies methods across containers and preserves explicitly requested GUI and TUI surfaces. The default returns at most six entities, independently caps each dossier's occurrence, incoming, and outgoing sections at six, and divides one 64 KiB source budget across all results. Go function and method definitions expand to their complete parsed declarations when the budget permits. Relationship ranking uses semantic-unit and stable-path proximity after evidence kind, keeping relevant local flow ahead of distant same-named endpoints. Natural-language reasoning stays in the consuming agent. Weave supplies bounded compiler, SCIP, content, and authored evidence from its existing graph without adding an embedded model or a second persisted search database.

The noisy default impact policy remains open. `weave impact TARGET --kind calls` already supplies a narrow alternative, but changing the default requires evidence across more languages and repositories. One dogfood trace is enough to expose a problem, not enough to declare a universal traversal policy.

## Repeat the task before claiming consolidation

A second fresh agent followed menu-publishing authorization from GUI and TUI action availability through the public module, command middleware, readiness enforcement, and persistence. Its architectural account was correct and it kept the repository clean, but the route required 32 Weave commands, two filesystem searches, one source-file read, and one cleanliness check. The graph again avoided broad discovery; it did not yet provide the intended one-to-four-call research experience.

The initial phrase command failed because `explore` was still only an exact-context alias during that run. That evidence caused the command to become the phrase-to-dossier composition described above. A representative menu-publish question now returns the GUI publish boundary, `Module.Publish`, and `Commands.Publish` in one roughly two-second call on Mixology.

That post-change call was a functional check, not a post-change agent benchmark. A new implementation can show that the intended entities rank together without proving that a fresh agent now finishes the research in fewer calls. The distinction kept a promising correction from quietly becoming an unsupported savings claim while the paired harness was built.

## Hold the question and evidence standard constant

The checked-in harness creates an isolated local clone for each arm and gives both fresh agents the same read-only question: follow menu-publish authorization and enforcement from GUI and TUI action availability through `Module.Publish`, `Commands.Publish`, `RunCommand`, readiness validation, persistence, and relevant tests. A deterministic eight-item rubric checks those seams in each final answer.

The Weave arm receives a current index and an instruction to start with one `weave explore` call. The control arm places a same-named blocking executable on `PATH` and tells the agent to use ordinary repository search and source-reading tools. That prevents accidental contamination without giving one arm a different architectural question. Both clones must remain unchanged.

Every run retains its prompt, raw Codex event stream, standard error, final answer, process measurement, worktree status, and machine-readable summary. The summary counts tokens, elapsed time, command executions, successful Weave calls, filesystem searches, source reads, blocked Weave attempts, and rubric matches. A number in the report can therefore be traced back to the tool events and answer that produced it.

## Read the first paired result

The first valid paired run used Weave commit `9c756c7`, Mixology commit `7b01054`, Codex CLI 0.147.0, and one isolated clone per arm. The indexed agent made one successful `weave explore` call. Both agents produced complete answers and scored 8/8, so the efficiency comparison does not trade away the architectural result.

| Measure | With Weave | Without Weave | Reduction |
| --- | ---: | ---: | ---: |
| Correctness rubric | 8/8 | 8/8 | n/a |
| Input tokens | 167,344 | 342,080 | 51.1% |
| Output tokens | 2,816 | 3,621 | 22.2% |
| Wall time | 27.8s | 33.2s | 16.3% |
| Command executions | 5 | 8 | 37.5% |
| Filesystem searches | 1 | 4 | 75.0% |
| Source-read commands | 4 | 6 | 33.3% |

The important result is not simply that one query ran quickly. Its initial dossier supplied the GUI, TUI, module, command, readiness, persistence, and test seams while the final answer preserved the same rubric completeness as ordinary exploration. That reduced rediscovery across every recorded measure in this sample.

This is one paired sample, not a population estimate. It proves that the harness can isolate the tool, preserve correctness, retain auditable artifacts, and capture a concrete successful workload. Repeated cases across repositories and languages are still needed before treating these percentages as general expectations. That is a much stronger next position than either query latency alone or an uncontrolled success story: the measurement boundary now surrounds the agent's complete research task.
