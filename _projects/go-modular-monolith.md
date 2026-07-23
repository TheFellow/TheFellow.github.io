---
title: "go-modular-monolith"
excerpt: "A Go reference application that makes modular boundaries and cross-cutting concerns executable."
language: "Go"
license: "MIT"
repository_url: "https://github.com/TheFellow/go-modular-monolith"
guide_url: "/guides/building-high-quality-software/"
---

<div class="project-meta"><span>Go</span><span>Software architecture</span><span>Cedar</span><span>MIT</span></div>

[View the repository](https://github.com/TheFellow/go-modular-monolith){: .btn .btn--primary }
[Open the guide outline](/guides/building-high-quality-software/){: .btn }

go-modular-monolith—also called Mixology—is an opinionated reference application organized around bounded contexts for a cocktail-bar domain. It deliberately uses one binary and one embedded database, leaving the complexity budget for boundaries, types, authorization, transactions, events, and tooling that enforce the design.

The repository's central argument is that important rules should be executable. arch-lint rejects forbidden package dependencies; generated dispatchers and IDs remove repetitive wiring; typed contexts prevent event handlers from emitting cascading events; Cedar policies separate authorization decisions from domain code; and shared middleware applies the same concerns to CLI and TUI surfaces.

### Why it is worth exploring

- It is a teaching vehicle whose architectural claims can be checked directly in code and tests.
- The full pipeline—commands, queries, authorization, persistence, events, audit records, and presentation surfaces—runs in integration tests without external infrastructure.
- It provides the worked example for the planned **Building High-Quality Software** written and video series.

The best entry point is the [guide outline](/guides/building-high-quality-software/), which maps each architectural idea to specific files in the repository.

