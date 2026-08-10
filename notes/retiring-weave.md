<!-- Generated from https://thefellow.github.io/notes/retiring-weave/ by scripts/generate_llm_content.py; do not edit. -->

# Retiring Weave

Source: [https://thefellow.github.io/notes/retiring-weave/](https://thefellow.github.io/notes/retiring-weave/)

## Pyramid summary

- **~2 words:** Retired experiment
- **~8 words:** A local code-index experiment yielded a useful benchmark.
- **Expanded:** What I learned from building and benchmarking a compact local code index for coding agents.

## Full content

Weave was an experiment in making codebase research cheaper for coding agents. I wanted a compact, local code graph and navigation index that could point an LLM toward the right declarations, relationships, and source excerpts without storing an entire abstract syntax tree or making the agent search every file. The measure that mattered was simple: fewer tokens spent finding trustworthy evidence.

The implementation grew beyond that small idea. It accumulated indexing formats, language adapters, freshness rules, graph operations, discovery dossiers, a broker, query sessions, federation, semantic diffs, and several overlapping CLI surfaces. Each capability was defensible in isolation, but together they increased the tool's conceptual and operational cost. The experiment needed evidence that this complexity bought agents a better research workflow.

## Benchmark the outcome, not the architecture

I compared Weave, CodeGraph, and ordinary source search on clean clones of Weave and a reasonably complex Go modular monolith, then checked language coverage against an F# workflow repository. Claude Sonnet answered identical repository questions under isolated tool configurations. I measured correctness, processed tokens, cost, turns, and tool calls rather than treating a successful index build as proof of usefulness.

CodeGraph materially reduced processed tokens and tool calls on broad architectural traces. Across the completed runs it processed about 3.29 million tokens with 104 tool calls, compared with Weave's 6.45 million tokens and 204 tool calls. Weave also failed one budgeted run.

The focused correctness case supplied the more important counterweight. Ordinary source search found the decisive existing test. Weave missed an archived-menu soft-delete exception and produced the wrong conclusion. CodeGraph reached the right behavior but did not surface all of the strongest evidence. Neither index covered the F# source in the third repository.

The result was not that graphs are useless or that native search always wins. It was that a graph is an optimization, not authority. Broad tracing benefits from good graph retrieval, while precise claims still need direct source and test verification.

## Stop when the experiment answers the question

I retired Weave because its surface area and maintenance cost no longer justified continuing. An existing tool performed the broad-navigation job better, and ordinary search remained stronger for the correctness boundary where confidence mattered most. More features or another index format would not change that decision without first proving a substantially smaller and more effective agent workflow.

Building Weave was still worthwhile. It clarified how aggressively retrieval output must be bounded, how dangerous confident but incomplete evidence can be, and why tool evaluations must include questions with surprising answers. Retiring it is part of the engineering result: test the premise, keep the evidence, and stop investing when the evidence points elsewhere.
