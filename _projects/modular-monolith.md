---
title: "modular-monolith"
date: 2026-08-09 19:30:00 -0700
last_modified_at: 2026-08-09 19:30:00 -0700
excerpt: "An idiomatic .NET port of Mixology that preserves behavior while rebuilding the architecture for C#."
language: "C#"
license: "MIT"
repository_url: "https://github.com/TheFellow/modular-monolith"
last_updated: 2026-08-09
order: 15
icon: "modules"
accent: "#b197fc"
topics: ["Architecture", "Semantic port", "Cedar"]
---

<div class="project-meta"><span>C#</span><span>Software architecture</span><span>Semantic port</span><span>MIT</span><span>Updated {{ page.last_updated | date: "%B %-d, %Y" }}</span></div>

[View the repository](https://github.com/TheFellow/modular-monolith){: .btn .btn--primary }
[Explore the Go reference](/projects/go-modular-monolith/){: .btn }
[Read the Mixology series](/series/mixology/){: .btn }

modular-monolith is the .NET 10 port of Mixology, a stateful cocktail-bar application with seven bounded contexts, one embedded SQLite database, Cedar authorization, and independent CLI, TUI, and desktop clients. It preserves the Go application's observable behavior while rebuilding its architecture around C# and the .NET ecosystem.

That distinction shapes the project. The port does not reproduce Go package layouts or error conventions in C#. It uses the .NET Generic Host for configuration and lifetime, dependency injection for composition, EF Core for persistence, Terminal.Gui for the terminal application, and Avalonia for the desktop client. Closed domain states use explicit record hierarchies and exhaustive pattern matching. Public module facades expose deliberate collaboration contracts while commands, persistence rows, and handlers remain internal.

### Semantics before syntax

The Go application provides a behavioral specification rather than a source template. A checked parity ledger tracks domain operations, authorization, transaction behavior, event reactions, paging, filtering, telemetry, and all three presentation surfaces. Production-shaped tests then exercise those claims through the real SQLite store and composed application.

Ingredient retirement is one of the most useful examples. A permanent replacement can rewrite compatible future recipes, while an unresolved required ingredient moves affected drinks into review and blocks pending orders. Published menus remain visible but report degraded readiness. Event reactions prepare before mutation, run inside the originating transaction, and finalize derived state only after every handler has applied its work. If any step fails, the domain changes and successful audit entry roll back together.

The application boundary applies the same discipline to ordinary operations. Commands pass through serialization, logging, metrics, activity tracking, a unit of work, Cedar authorization, event dispatch, and audit recording. Reads authorize their results, and paged lists continue through hidden rows until they fill a visible page. Counts and cursors therefore describe what the current actor can actually observe.

### Native surfaces, shared behavior

The CLI, Terminal.Gui TUI, and Avalonia desktop client share application behavior and durable state, not view models. Each surface owns its framework-specific interaction model while consuming the same public module capabilities and authorization-projected actions. Cross-process tests write through one client and observe through another, which makes the embedded database and application contract executable across every adapter.

The desktop client adds its own concurrency obligations. UI-thread publication, latest-request-wins refresh, dirty-navigation decisions, and drained shutdown are explicit MVVM state with headless control tests. CI publishes native desktop applications for Linux, Windows, and macOS, executes their help paths, and runs a dynamic race gate over the desktop concurrency primitives.

### Why it is worth exploring

- It shows how to preserve a nontrivial application's semantics without carrying source-language architecture into the target ecosystem.
- It makes module direction, transactions, authorization, event reactions, and presentation isolation executable through project references, architecture tests, generated routing, and end-to-end behavior.
- It provides parallel Go and C# implementations of the same application, making language and framework tradeoffs concrete rather than hypothetical.

The quickest route through the repository is the root README, followed by the architecture guide and semantic parity ledger. The source map then traces the kernel, bounded contexts, toolkits, and independent composition roots.
