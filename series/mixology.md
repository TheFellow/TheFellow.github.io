<!-- Generated from https://thefellow.github.io/series/mixology/ by scripts/generate_llm_content.py; do not edit. -->

# Building Mixology

Source: [https://thefellow.github.io/series/mixology/](https://thefellow.github.io/series/mixology/)

## Pyramid summary

- **~2 words:** Mixology series
- **~8 words:** An ordered path through Mixology's executable application architecture.
- **Expanded:** An ordered path through the architecture, domain modeling, persistence, authorization, and three user interfaces of the go-modular-monolith reference application.

## Full content

Mixology is a Go reference application that makes modular boundaries and cross-cutting concerns executable. This series follows the application from its architectural premise through transactional domain collaboration, presentation boundaries, native desktop testing, authorization, shared action meaning, and the migration from bstore to SQLite.

The completed [.NET semantic port](/projects/modular-monolith.md) preserves that observable behavior while rebuilding the application with .NET 10, EF Core, Terminal.Gui, and .NET MAUI. It provides a parallel implementation for separating the architecture's durable ideas from the Go-specific mechanisms described throughout this series.

[Explore the project](/projects/go-modular-monolith.md)
[View the repository](https://github.com/TheFellow/go-modular-monolith)
[Explore the .NET port](/projects/modular-monolith.md)
[Present the slide deck](/talks/building-mixology.md)

1. **Article:** [Building High-Quality Software](/articles/building-high-quality-software.md): A preview of eleven lessons about turning architectural intent into executable constraints, using Mixology as the worked example.
2. **Article:** [Turning Cross-Domain Calls into Enforced Boundaries](/articles/turning-cross-domain-calls-into-enforced-boundaries.md): A worked path from direct cross-domain orchestration to transactional retirement, owned reactions, and package rules that preserve both current operations and history.
3. **Article:** [Preserving Truth Through Operational Degradation](/articles/preserving-truth-through-operational-degradation.md): How explicit replacement, review states, readiness reports, and historical snapshots let a modular application degrade honestly without erasing business context.
4. **Article:** [Growing a Reciprocal Domain Workflow](/articles/growing-a-reciprocal-domain-workflow.md): A planned vertical-slice workshop that adds Procurement to Mixology, connects it reciprocally with Inventory, and finds the boundary between transactional handlers and explicit workflows.
5. **Article:** [Building an Application TUI Toolkit](/articles/building-an-application-tui-toolkit.md): How Mixology combines proven MVVM ideas with Bubble Tea's message loop to create a consistent, testable terminal application without inventing another framework.
6. **Article:** [Growing Mixology with a GUI Surface](/articles/growing-mixology-with-fyne.md): A development journal for adding a retained-mode Fyne desktop client to Mixology while preserving bespoke surfaces, executable boundaries, and testable application behavior.
7. **Article:** [Using a Third Surface as an Architecture Test](/articles/using-a-third-surface-as-an-architecture-test.md): What Mixology's Fyne client revealed when a third, substantially different presentation runtime had to use the same application boundaries as its CLI and TUI.
8. **Article:** [Bespoke Views over a Shared Application Boundary](/articles/bespoke-views-over-a-shared-application-boundary.md): What Mixology shares across CLI, Bubble Tea, and Fyne, and why each surface keeps a presentation model shaped for its own runtime instead of adopting a universal view model.
9. **Article:** [Testing Native Go Desktop Applications Headlessly](/articles/testing-native-go-desktop-applications-headlessly.md): A layered testing strategy for Fyne applications, from deterministic presentation models and virtual widgets through composed lifecycles, fresh processes, race tests, and visual evidence.
10. **Article:** [Authorization Is Part of Navigation](/articles/authorization-is-part-of-navigation.md): How Mixology carries Cedar authorization through workspace discovery, dashboard summaries, row filtering, and action availability without turning the interface into a second policy engine.
11. **Article:** [Typed Filtering over SQLite](/articles/typed-filtering-over-sqlite.md): How Mixology gives people and programs one typed filter language, then translates its safe subset into SQLite while retaining exact application semantics.
12. **Note:** [Projecting Actions Across User Interfaces](/notes/projecting-actions-across-user-interfaces.md): How Mixology projects authorization and lifecycle prerequisites once, then lets GUI and TUI render native action state without sharing their views.
13. **Article:** [Migrating Mixology from bstore to SQLite](/articles/migrating-mixology-from-bstore-to-sqlite.md): How Mixology replaced its embedded bstore backend with SQLite while preserving transactions, typed queries, domain ownership, filtering semantics, and application errors.
