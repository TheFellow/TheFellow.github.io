<!-- Generated from https://thefellow.github.io/writing/ by scripts/generate_llm_content.py; do not edit. -->

# Writing

Source: [https://thefellow.github.io/writing/](https://thefellow.github.io/writing/)

## Pyramid summary

- **~2 words:** Collected writing
- **~8 words:** Articles, notes, and series together, newest writing first.
- **Expanded:** Articles, notes, and series on software architecture, developer tools, and experiments, newest first.

## Full content

Articles, notes, and series from the projects and experiments behind this site, ordered by publication date, newest first.

- **2026-09-12 · Note:** [Autonomous Semantic Porting with F#kYeah](/notes/autonomous-semantic-porting-with-fkyeah.md): How I use F#kYeah across projects to analyze, implement, validate, and review semantic ports without a human in the execution loop.
- **2026-09-12 · Article:** [Explicit Architecture, with a Go Accent](/articles/explicit-architecture-with-a-go-accent.md): What Mixology borrows from Herberto Graça's Explicit Architecture, where it deliberately differs, and what transactions, types, three interfaces, and a storage migration taught me about those choices.
- **2026-09-10 · Note:** [Building a Racing-Line Playground](/notes/building-a-racing-line-playground.md): A fun physics project in Go: turning editable roads and tyre-force limits into racing lines, ghost comparisons, and two-car experiments in overtaking and defence.
- **2026-09-03 · Note:** [Building a Persistent Merkle Trie in Go](/notes/building-a-persistent-merkle-trie-in-go.md): How canonical codecs, radix routing, structural sharing, and lazy snapshots fit together in a generic content-addressed trie.
- **2026-08-20 · Note:** [Go 1.27 Generic Methods and the Mixology Pipeline](/notes/go-1-27-generic-methods-and-the-mixology-pipeline.md): How generic methods let Mixology put typed middleware operations on the pipeline they configure.
- **2026-08-10 · Article:** [Migrating Mixology from bstore to SQLite](/articles/migrating-mixology-from-bstore-to-sqlite.md): How Mixology replaced its embedded bstore backend with SQLite while preserving transactions, typed queries, domain ownership, filtering semantics, and application errors.
- **2026-08-10 · Note:** [Retiring Weave](/notes/retiring-weave.md): What I learned from building and benchmarking a compact local code index for coding agents.
- **2026-08-05 · Article:** [Growing a Reciprocal Domain Workflow](/articles/growing-a-reciprocal-domain-workflow.md): A planned vertical-slice workshop that adds Procurement to Mixology, connects it reciprocally with Inventory, and finds the boundary between domain-owned transactional commands and processes spanning commits.
- **2026-08-05 · Article:** [Preserving Truth Through Operational Degradation](/articles/preserving-truth-through-operational-degradation.md): How explicit replacement, review states, readiness reports, and historical snapshots let a modular application degrade honestly without erasing business context.
- **2026-08-05 · Note:** [Projecting Actions Across User Interfaces](/notes/projecting-actions-across-user-interfaces.md): How Mixology projects authorization and lifecycle prerequisites once, then lets GUI and TUI render native action state without sharing their views.
- **2026-08-02 · Article:** [Turning Cross-Domain Calls into Enforced Boundaries](/articles/turning-cross-domain-calls-into-enforced-boundaries.md): A worked path from direct cross-domain orchestration to transactional retirement, owned reactions, and package rules that preserve both current operations and history.
- **2026-08-02 · Article:** [Typed Filtering over SQLite](/articles/typed-filtering-over-sqlite.md): How Mixology gives people and programs one typed filter language, then translates its safe subset into SQLite while retaining exact application semantics.
- **2026-08-01 · Article:** [Authorization Is Part of Navigation](/articles/authorization-is-part-of-navigation.md): How Mixology carries Cedar authorization through workspace discovery, dashboard summaries, row filtering, and action availability without turning the interface into a second policy engine.
- **2026-08-01 · Article:** [Bespoke Views over a Shared Application Boundary](/articles/bespoke-views-over-a-shared-application-boundary.md): What Mixology shares across CLI, Bubble Tea, and Fyne, and why each surface keeps a presentation model shaped for its own runtime instead of adopting a universal view model.
- **2026-08-01 · Article:** [Testing Native Go Desktop Applications Headlessly](/articles/testing-native-go-desktop-applications-headlessly.md): A layered testing strategy for Fyne applications, from deterministic presentation models and virtual widgets through composed lifecycles, fresh processes, race tests, and visual evidence.
- **2026-08-01 · Article:** [Using a Third Surface as an Architecture Test](/articles/using-a-third-surface-as-an-architecture-test.md): What Mixology's Fyne client revealed when a third, substantially different presentation runtime had to use the same application boundaries as its CLI and TUI.
- **2026-07-29 · Article:** [Growing Mixology with a GUI Surface](/articles/growing-mixology-with-fyne.md): A development journal for adding a retained-mode Fyne desktop client to Mixology while preserving bespoke surfaces, executable boundaries, and testable application behavior.
- **2026-07-28 · Note:** [Building a Generic RIBLT in Go](/notes/riblt-in-go.md): A step-by-step implementation of generic, rateless set reconciliation in Go, from XOR-coded cells through peeling and measured communication.
- **2026-07-28 · Article:** [Building an Application TUI Toolkit](/articles/building-an-application-tui-toolkit.md): How Mixology combines proven MVVM ideas with Bubble Tea's message loop to create a consistent, testable terminal application without inventing another framework.
- **2026-07-23 · Article:** [Building High-Quality Software](/articles/building-high-quality-software.md): A preview of eleven lessons about turning architectural intent into executable constraints, using Mixology as the worked example.
- **2026-07-23 · Series:** [Building Mixology](/series/mixology.md): An ordered path through the architecture, domain modeling, persistence, authorization, and three user interfaces of the go-modular-monolith reference application.
- **2026-04-23 · Note:** [Linux for Windows Brains](/notes/linux-for-windows-brains.md): A practical translation from familiar Windows concepts to Linux filesystems, permissions, shells, services, SSH, and containers.
- **2026-03-27 · Note:** [Porting Cedar from Go to .NET: Semantics Before Syntax](/notes/porting-cedar-semantics-from-go-to-dotnet.md): How cedar-dotnet establishes correct Cedar behavior through conformance tests, then uses benchmarks to make it fast.
- **2026-03-06 · Article:** [Making Illegal States Unrepresentable in Go](/articles/making-illegal-states-unrepresentable-in-go.md): What F#'s algebraic types teach about modeling identifiers, validated values, closed variants, and typed workflows in Go, including where Result pipelines fit.
- **2026-03-06 · Note:** [Octonions and the Standard Model in F#](/notes/octonions-and-the-standard-model-in-fsharp.md): An executable tour from non-associative octonion multiplication to a Furey-inspired eight-state particle pattern.
- **2026-03-06 · Note:** [Type-Safe Linear Algebra in F#](/notes/type-safe-linear-algebra-in-fsharp.md): Using phantom dimensions and F# operators to make invalid matrix arithmetic fail at compile time.
- **2026-02-07 · Article:** [Building a File-Backed Columnar Event Pipeline](/articles/building-a-file-backed-columnar-event-pipeline.md): How immutable Parquet batches, snapshot metadata, DuckDB, Arrow, and Protobuf form a columnar event path from storage to results.
- **2023-10-12 · Note:** [From Groups to ECDSA: Elliptic-Curve Cryptography from First Principles](/notes/elliptic-curve-cryptography-from-first-principles.md): A ground-up path to ECDSA through groups, finite fields, elliptic-curve point arithmetic, and scalar multiplication.
