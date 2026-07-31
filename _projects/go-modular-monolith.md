---
title: "go-modular-monolith"
date: 2026-07-23 12:03:42 -0700
last_modified_at: 2026-07-30 14:00:00 -0700
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

The desktop shell reflects authorization before a user enters a workspace. Navigation and dashboard cards include only workspaces with an authorized read path, denied dashboard aggregates are omitted without masking operational failures, and Cedar continues to filter rows within each visible workspace. The native window title keeps the active persona visible throughout the session.

The persistent left navigation now opens each authorized workspace through a common list/detail layout, while create and edit operations use a standard scrolling form and action hierarchy. The TUI follows the same product-level interaction language in terminal-native form: arrows select fields, `e` or Enter begins editing, Enter accepts a value, and Escape cancels it. CLI, TUI, and GUI also open `data/mixology.db` by default, so each surface presents the same stored application state.

The package layout makes those ownership choices explicit. Domain surfaces may share application presentation contracts from `app/surfaces`, and reusable framework mechanics from the matching `pkg/toolkits` package, but they cannot import executable composition under `main`. Public models, queries, and events form the cross-domain vocabulary; authorization packages and command event publication stay within the owning domain. Architecture tests also reject novel domain package layers and catch a domain that was added without being exposed and initialized by the application root.

```text
app/
  kernel/                 shared value types and cross-cutting ports
  domains/<context>/      facade, public contracts, owned policy, internals, and surfaces
  surfaces/tui/           Mixology-wide TUI contracts and components
pkg/
  toolkits/{cli,gui,tui}/ reusable presentation mechanics
  middleware/             authorization, transactions, events, audit, and metrics
main/
  cli/                    CLI executable and composition
  gui/                    Fyne executable and composition
  tui/                    Bubble Tea root shell and workspace composition
```

The [Building High-Quality Software preview](/guides/building-high-quality-software/) follows that
thread through eleven planned lessons: enforced boundaries, constraints encoded in types, the
shared operation pipeline, transactional events, focused code generation, error contracts,
policy-based authorization, interchangeable CLI and bespoke MVVM-style TUI and GUI surfaces, an owned seam for
cross-domain features such as tags, production-shaped tests, and the discipline to stop before
simple becomes simplistic.
