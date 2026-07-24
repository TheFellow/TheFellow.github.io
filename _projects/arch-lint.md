---
title: "arch-lint"
excerpt: "A Go analyzer that turns architectural dependency rules into build-time checks."
language: "Go"
license: "MIT"
repository_url: "https://github.com/TheFellow/arch-lint"
last_updated: 2026-03-29
order: 30
icon: "boundaries"
accent: "#66d9e8"
topics: ["Static analysis", "Architecture"]
---

<div class="project-meta"><span>Go</span><span>Static analysis</span><span>Architecture</span><span>MIT</span><span>Updated {{ page.last_updated | date: "%B %-d, %Y" }}</span></div>

[View the repository](https://github.com/TheFellow/arch-lint){: .btn .btn--primary }

Architecture diagrams and conventions are useful, but they drift when nothing checks them. arch-lint makes package-boundary rules executable: a YAML specification selects packages, forbids dependency patterns, and records narrowly scoped exceptions or exemptions.

Glob captures move arch-lint beyond a simple deny list. Rules can express relationships such as “one module must not import another module's internals” without spelling out every module pair. The same analyzer can run as a command, through Go's `analysis` framework, or as a golangci-lint module plugin, so the constraint can live in both local feedback and CI.

### Why it is worth exploring

- It demonstrates architecture as an automatically tested property of a repository.
- Its pattern language balances broad rules with explicit, reviewable exceptions.
- It is used by the Mixology modular-monolith sample, showing the rules at work in a real codebase.

Read the configuration schema and matcher first, then see `.arch-lint.yaml` in [go-modular-monolith](https://github.com/TheFellow/go-modular-monolith) for a real rule set.
