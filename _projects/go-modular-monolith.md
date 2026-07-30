---
title: "go-modular-monolith"
date: 2026-07-23 12:03:42 -0700
last_modified_at: 2026-07-30 10:00:00 -0700
excerpt: "A Go reference application that makes modular boundaries and cross-cutting concerns executable."
language: "Go"
license: "MIT"
repository_url: "https://github.com/TheFellow/go-modular-monolith"
last_updated: 2026-07-30
guide_url: "/guides/building-high-quality-software/"
order: 10
featured: true
icon: "modules"
accent: "#63e6be"
topics: ["Architecture", "Reference app", "Cedar"]
---

<div class="project-meta"><span>Go</span><span>Software architecture</span><span>Cedar</span><span>MIT</span><span>Updated {{ page.last_updated | date: "%B %-d, %Y" }}</span></div>

[View the repository](https://github.com/TheFellow/go-modular-monolith){: .btn .btn--primary }
[Preview the tutorial series](/guides/building-high-quality-software/){: .btn }
[Read the GUI surface guide](/guides/growing-mixology-with-fyne/){: .btn }

go-modular-monolith, also called Mixology, is an opinionated reference application organized around bounded contexts for a cocktail-bar domain. It deliberately uses one binary and one embedded database, leaving the complexity budget for boundaries, types, authorization, transactions, events, and tooling that enforce the design.

The repository's central argument is that important rules should be executable. Package boundaries fail the build when they are crossed. The type system withholds capabilities that a caller should not have. Authorization, transactions, events, and audit all surround domain operations through one path, regardless of whether a request began in the CLI, Bubble Tea TUI, or Fyne desktop client.

Deleting an ingredient makes those claims concrete. The command can affect inventory, every drink that uses the ingredient, and every menu carrying those drinks. Independent event handlers prepare their work before any of them mutate state, then apply the complete change inside the originating transaction. If one handler fails, the ingredient and all of its dependent state remain untouched. No handler reaches into another domain's internals, and no message broker is required to keep the modules separate.

That balance is what makes Mixology useful as a teaching vehicle. It has enough behavior for boundaries and cross-cutting concerns to matter, while the complete application still fits in one process and its tests need no external infrastructure. The code can show the consequence of a design choice without first asking the reader to assemble a distributed system.

Adding the Fyne client also turned surface parity into an executable application contract. The audit did not merely bring the new desktop view up to the existing interfaces. It found missing TUI workflows, CLI fidelity gaps, inconsistent paging and filtering, duplicated dashboard calculations, and mutations whose domain change and complete tag set were not atomic. Shared application services and cross-surface tests now correct those behaviors for every adapter while each presentation remains bespoke.

The [Building High-Quality Software preview](/guides/building-high-quality-software/) follows that
thread through eleven planned lessons: enforced boundaries, constraints encoded in types, the
shared operation pipeline, transactional events, focused code generation, error contracts,
policy-based authorization, interchangeable CLI and bespoke MVVM-style TUI and GUI surfaces, an owned seam for
cross-domain features such as tags, production-shaped tests, and the discipline to stop before
simple becomes simplistic.
