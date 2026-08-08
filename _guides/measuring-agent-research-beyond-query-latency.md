---
title: "Measuring Agent Research Beyond Query Latency"
date: 2026-08-07 17:54:48 -0700
last_modified_at: 2026-08-08 14:20:00 -0700
excerpt: "How paired agent research and a storage-payload audit moved Weave from large graph dossiers to compact progressive discovery without losing answer quality."
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

A semantic query completing in a second is not yet a useful product result. An agent can receive a fast list of opaque identities or an enormous graph response, fail to select useful source, and spend the rest of the investigation rediscovering the repository. Latency, index size, response bytes, tool calls, source reads, model tokens, and answer completeness all describe different parts of the experience.

[Weave](https://github.com/TheFellow/weave) used paired agent research to test the outcome, then used a storage and payload audit to test whether the successful behavior was practical. The combination changed the design more than either benchmark could have done alone.

<figure class="article-figure">
  <img src="{{ '/assets/images/articles/weave/agent-research-dogfood.svg' | relative_url }}" alt="A fixed repository question and evidence rubric feed paired agents with and without Weave. Their answers, tool events, searches, reads, commands, tokens, and elapsed time are retained. A second audit measures database amplification and encoded discovery bytes. The evidence leads to a compact navigation index, semantic anchors plus ripgrep hits, and exact context only after selection.">
  <figcaption>Outcome evidence says whether discovery helps; storage and payload evidence says whether its implementation is practical.</figcaption>
</figure>

## Score repository understanding

The first controlled question asked an unfamiliar agent to trace Mixology's menu publication flow through readiness, authorization, persistence, GUI and TUI surfaces, and tests. The harness fixed the repository revision, prompt, rubric, tool availability, and evidence standard. It retained the raw agent event stream, stderr, final answer, process measurements, and post-run worktree status.

Both arms scored 8/8. In that single paired code-flow sample, the Weave arm used 51.1% fewer input tokens, 37.5% fewer commands, 75% fewer filesystem searches, 33.3% fewer source reads, and 16.3% less wall time. The result showed that semantic discovery could reduce navigation work without reducing answer completeness.

A second paired question targeted concepts found in benchmark prose rather than headings. Both arms again scored 8/8. The Weave arm used 21.3% fewer input tokens, 8.6% fewer output tokens, no filesystem searches, and the same two-command count, but finished 1.90 seconds slower. Content discovery helped the evidence path without winning every metric.

These are two auditable samples, not a population estimate. They justify preserving the behavior, not freezing its first implementation.

## Record what the agent had to work around

Early dogfood exposed several forms of friction:

- ambiguous short names produced opaque choices;
- definition, reference, call, and context results repeated overlapping facts;
- variables and generic references consumed bounded relationship slots;
- one broad exploration could place roughly 16,000 tokens into context; and
- a correct second trace still used 32 Weave commands.

The first response was to rank and compact graph dossiers more carefully. That improved the original model but retained its basic assumption: discovery should serialize several complete semantic neighborhoods before the agent chose one.

## Audit the physical and encoded cost

The later audit measured a 3,019,968-byte Go repository whose format-3 database occupied 1,034,616,832 bytes. It contained 25,678 symbols, 184,826 occurrences, and 247,013 edges. The representative ordinary `explore --json` response occupied 171,537 bytes.

Only a small fraction of that response was current source. Repeated stable and opaque identities, unit and document IDs, ranges, provenance, evidence, hashes, and full edges dominated the payload. Persisting every compiler event also multiplied source bytes into storage records and indexes that agents rarely needed during first-stage discovery.

This evidence reframed the problem. The product did not need a better-compressed exhaustive dossier. It needed a smaller contract between semantic navigation and source inspection.

## Make discovery progressive

The measured format-4 implementation retained semantic anchors and high-value navigation relationships while dropping occurrences, statement-level calls and references, noisy declaration kinds, containment duplication, and broad content-token postings. Format 5 makes the same narrow shape the producer and adapter contract. `weave explore` returns at most a few semantic anchors plus diversified ripgrep hits. Each semantic anchor includes an exact `weave context` follow-up. The discovery array has a 12 KiB encoded ceiling.

The selected `context` call then reads current source for one exact anchor. It does not expand eight candidates speculatively or pretend that the graph should replace text search for statement-level investigation.

On the same repository and commit, that format-4 database occupied 16,777,216 bytes, a 98.38% reduction and 5.56 times source size. The representative first-stage response occupied 3,157 bytes, 98.16% smaller than the old response. Its selected context response occupied 3,195 bytes and included 337 bytes of source. Those measurements remain a historical baseline until format 5 is rerun on the same fixture.

## Keep the benchmark honest after the redesign

The paired 8/8 results belong to the earlier retrieval implementation. They demonstrate that graph-guided discovery can preserve evidence quality while reducing navigation work. They do not yet prove that the new compact semantic-plus-ripgrep shape preserves the same token and command improvements.

That distinction creates the next useful benchmark. Re-run the fixed questions and rubrics against progressive discovery, then compare:

1. rubric completeness and cited evidence;
2. actual input and output tokens;
3. Weave commands, filesystem searches, and source reads;
4. elapsed time and startup mode;
5. first-stage and cumulative encoded response bytes; and
6. database size and refresh cost for the tested repository.

A smaller payload is not automatically better if it makes the agent issue many blind follow-ups. A rich graph is not automatically better if most of its bytes are repeated coordinates. The acceptance boundary is practical research: preserve correct answers while reducing total discovery work and keeping the local index proportional to the source it helps navigate.
