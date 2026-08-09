---
title: "Measuring Agent Research Beyond Query Latency"
date: 2026-08-07 17:54:48 -0700
last_modified_at: 2026-08-09 10:00:00 -0700
excerpt: "How Weave evaluates format-5 discovery by answer quality, model work, payload size, storage, and elapsed time."
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

A fast query is not useful if an agent still needs many searches, reads, and tokens to answer a repository question. [Weave](https://github.com/TheFellow/weave) therefore measures the complete research task.

<figure class="article-figure">
  <img src="{{ '/assets/images/articles/weave/agent-research-dogfood.svg' | relative_url }}" alt="Paired agents answer the same repository question against the same evidence rubric. The benchmark records answer quality, commands, searches, source reads, tokens, elapsed time, database size, and encoded discovery bytes. Results feed the bounded format-5 navigation design.">
  <figcaption>Measure useful evidence delivered per unit of agent work.</figcaption>
</figure>

## Score the answer first

Each task starts with a fixed repository, question, and evidence rubric. The Weave and filesystem-only arms must answer the same question from the same revision. A faster incomplete answer is a failure.

## Record the whole research path

The harness records:

- Weave commands, filesystem searches, and source reads;
- input and output tokens;
- elapsed time and tool failures;
- final answer evidence; and
- index bytes and encoded response bytes.

## Test the format-5 workflow

The current workflow is deliberately progressive:

1. `weave explore` returns a few declaration or document anchors plus diversified ripgrep hits.
2. The discovery array stays within its item limit and 12 KiB encoded ceiling.
3. The agent selects one useful target.
4. `weave context` opens bounded current source for that target.

The index does not return graph dossiers, occurrences, calls, references, or body postings. Benchmarks should test this exact workflow and report the pinned Weave commit, repository commit, prompt, limits, raw tool events, and scoring rubric.

The acceptance question is practical: does format 5 reach trustworthy source with less total work than direct rediscovery while keeping storage and payloads small?
