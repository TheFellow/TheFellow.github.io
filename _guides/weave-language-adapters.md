---
title: "Language Adapters Share One Navigation Contract"
date: 2026-08-09 10:32:00 -0700
last_modified_at: 2026-08-09 10:32:00 -0700
excerpt: "Compiler-backed adapters project bounded facts into the same format-5 profile."
permalink: /articles/weave-language-adapters/
series: weave
series_order: 3
status: "Weave, part 3"
featured: true
image: /assets/images/articles/weave/adapter-contract.svg
---

{% include series-notice.html %}

Weave treats language support as a process contract. An adapter reads a bounded request and emits validated `navigation-v1` facts over framed standard input and output.

![Language tools converging on one adapter contract](/assets/images/articles/weave/adapter-contract.svg)

The boundary lets a language tool use its own compiler without moving that compiler into Weave. Weave validates framing, limits, identities, paths, source ranges, edge kinds, and the advertised capability digest before publication.

The adapter registry records explicit commands and input routing. Managed adapters add pinned artifacts and lifecycle commands, but do not invent a package registry. Cross-repository soak fixtures check the contract against real repository shapes before support is advertised.

The built-in Go provider and external adapters therefore produce the same small navigation model. Query behavior does not depend on which compiler produced the facts.

[Continue to progressive discovery](/articles/weave-progressive-discovery/){: .btn .btn--primary }
