---
title: "modular-monolith"
date: 2026-08-09 19:30:00 -0700
last_modified_at: 2026-09-06
excerpt: "An idiomatic .NET port of Mixology that preserves behavior while rebuilding the architecture for C#."
language: "C#"
license: "MIT"
repository_url: "https://github.com/TheFellow/modular-monolith"
last_updated: 2026-08-10
order: 15
icon: "modules"
accent: "#b197fc"
topics: ["Architecture", "Semantic port", "Expr", "Cedar"]
---

<div class="project-meta"><span>C#</span><span>Software architecture</span><span>Semantic port</span><span>Expr</span><span>MIT</span><span>Updated {{ page.last_updated | date: "%B %-d, %Y" }}</span></div>

[View the repository](https://github.com/TheFellow/modular-monolith){: .btn .btn--primary }
[Explore the Go reference](/projects/go-modular-monolith/){: .btn }
[Read the Mixology series](/series/mixology/){: .btn }
[Explore Expr for .NET](/projects/expr-dotnet/){: .btn }

modular-monolith is the .NET 10 port of Mixology, a stateful cocktail-bar application with seven bounded contexts, one embedded SQLite database, Cedar authorization, and independent CLI, TUI, and desktop clients. It ports a documented Go behavior baseline while rebuilding the architecture around C# and the .NET ecosystem. Its parity ledger, rather than ongoing changes in the Go repository, defines that claim. The September 2026 Go additions for order amendments and retained stock lifecycle are described in the [Go project](/projects/go-modular-monolith/) and should not be inferred to exist here.

That distinction shapes the project. The port does not reproduce Go package layouts or error conventions in C#. It uses the .NET Generic Host for configuration and lifetime, dependency injection for composition, EF Core for persistence, Terminal.Gui for the terminal application, and .NET MAUI for the desktop client. Closed domain states use explicit record hierarchies and exhaustive pattern matching. Public module facades expose deliberate collaboration contracts while commands, persistence rows, and handlers remain internal.

The shared filtering foundation now adapts [Expr for .NET](/projects/expr-dotnet/) instead of maintaining a private expression compiler. Expr supplies parsing, static checking, the public immutable AST, optimization, canonical printing, and exact VM evaluation. `Mixology.Filtering` keeps the application-specific boundary: typed domain schemas, compatibility rewrites for existing filter spellings, application errors, help examples, and conservative EF Core pushdowns. Every narrowed query still evaluates the complete compiled expression after hydrating the public filter view, so the planner can improve candidate selection without becoming the authority for filter meaning.

The repository references the [published `Expr` 0.1.0 package](https://github.com/TheFellow/modular-monolith/blob/master/Directory.Packages.props#L6) rather than a source copy. Its [filtering tests](https://github.com/TheFellow/modular-monolith/blob/master/tests/Mixology.Filtering.Tests/FilterExpressionTests.cs) exercise checked evaluation, AST rewriting, compatibility syntax, canonical output, and safe planning through that dependency, while [SQLite integration tests](https://github.com/TheFellow/modular-monolith/blob/master/tests/Mixology.Filtering.Tests/SqlitePushdownTests.cs) compare pushed and exact results. Mixology therefore supplies a downstream validation of the same package available to other .NET applications.

### Semantics before syntax

The Go application provides a behavioral specification rather than a source template. A checked parity ledger tracks domain operations, authorization, transaction behavior, event reactions, paging, filtering, telemetry, and all three presentation surfaces. Production-shaped tests then exercise those claims through the real SQLite store and composed application.

Ingredient retirement is one of the most useful examples. A permanent replacement can rewrite compatible future recipes, while an unresolved required ingredient moves affected drinks into review and blocks pending orders. Published menus remain visible but report degraded readiness. Event reactions prepare before mutation, run inside the originating transaction, and finalize derived state only after every handler has applied its work. If any step fails, the domain changes and successful audit entry roll back together.

The application boundary applies the same discipline to ordinary operations. Commands pass through serialization, logging, metrics, activity tracking, a unit of work, Cedar authorization, event dispatch, and audit recording. Reads authorize their results, and paged lists continue through hidden rows until they fill a visible page. Counts and cursors therefore describe what the current actor can actually observe. Revisioned EF Core rows use concurrency tokens that advance during `SaveChanges`; when another unit of work has already changed the row, the persistence boundary translates `DbUpdateConcurrencyException` into the same transport-neutral conflict model used by the rest of the application.

### Native surfaces, shared behavior

The CLI, Terminal.Gui TUI, and .NET MAUI desktop client share application behavior and durable state, not view models. Each surface owns its framework-specific interaction model while consuming the same public module capabilities and authorization-projected actions. Cross-process tests write through one client and observe through another, which makes the embedded database and application contract executable across every adapter.

The desktop client adds its own concurrency obligations. UI-thread publication, latest-request-wins refresh, dirty-navigation decisions, and drained shutdown are explicit MVVM state with platform-neutral view-model and XAML contract tests. CI publishes native .NET MAUI applications for Windows and macOS, exercises the UI-neutral target on Linux, and runs a dynamic race gate over the desktop concurrency primitives.

### Why it is worth exploring

- It shows how to preserve a nontrivial application's semantics without carrying source-language architecture into the target ecosystem.
- It makes module direction, transactions, authorization, event reactions, and presentation isolation executable through project references, architecture tests, generated routing, and end-to-end behavior.
- It provides parallel Go and C# implementations of the same application, making language and framework tradeoffs concrete rather than hypothetical.

The quickest route through the repository is the root README, followed by the architecture guide and semantic parity ledger. The [`Mixology.Filtering` guide](https://github.com/TheFellow/modular-monolith/blob/master/src/Mixology.Filtering/README.md) is a compact example of adapting a general language into an application-owned contract, while the source map traces the kernel, bounded contexts, toolkits, and independent composition roots.
