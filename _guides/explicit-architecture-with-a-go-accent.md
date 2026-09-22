---
title: "Explicit Architecture, with a Go Accent"
date: 2026-09-12
last_modified_at: 2026-09-22
excerpt: "What Mixology borrows from Herberto Graça's Explicit Architecture, where it deliberately differs, and what transactions, types, three interfaces, and a storage migration taught me about those choices."
permalink: /articles/explicit-architecture-with-a-go-accent/
series: mixology
series_order: 14
order: 55
featured: true
status: "Architecture synthesis"
icon: "boundaries"
accent: "#63e6be"
topics: ["Explicit Architecture", "Go", "Modular monolith", "Design tradeoffs"]
---

{% include series-notice.html %}

Retiring an ingredient is a surprisingly good architecture exercise. The catalog changes, recipes may need a replacement, physical stock still exists, published menus may become harder to serve, and accepted orders must retain what was promised. The operation also needs authorization, a transaction, and an explanation of what happened. It can begin in a terminal command, a terminal application, or a desktop window.

That is the kind of problem I built [Mixology](/projects/go-modular-monolith/) to explore. A great deal of its inspiration came from Herberto Graça's [Explicit Architecture series][ea1], together with DDD, ports and adapters, Clean Architecture, CQRS, functional modeling, and the application frameworks I have used. Mixology is where those influences meet my preferences: concrete public APIs, small capabilities, visible wiring, native presentation models, and rules the repository can enforce.

I narrowed some of those ideas to suit one local application with strong transactional behavior. Several of the most useful boundaries became clearer only after replacing the database or adding a third user interface.

I call this arrangement **Explicit Modules**, with a Go accent: a domain-first modular monolith with clear ownership and little ceremony. The [infographic below](#explicit-modules-a-map-of-the-territory) gathers the architecture into one picture: who owns the work, how modules collaborate, and what commits together.

At [commit `0d5e64b`][baseline], Procurement remains planned work. Single and batch amendments, substitution rules, and stock disposition/history are available through all three surfaces.

## The original map, and the downloadable PDF

Graça's [first article][ea1] connects delivery mechanisms, adapters, ports, application behavior, and domain models, then slices the layers into components. It distinguishes runtime control flow from source dependencies and shows both direct application calls and a command/query bus. The diagram is a vocabulary for making choices, rather than a list of components every application must contain.

The complete graphic is still available through the **[original Google Drawing][drawing]**. Its **[direct PDF export][pdf]** downloads a one-page vector diagram. It includes the full map with driving and driven adapters, components, application and domain layers, queues, buses, search, and persistence. Open the drawing if you also want Google's other export formats.

The [second article][ea2] revisits the shared kernel. Graça places shared application/domain contracts below the component map, then separates those from general language extensions. That helps distinguish common business vocabulary from reusable programming machinery. A shared package needs an explanation stronger than “several things import it.”

The [third article][ea3] translates the maps into source organization and dependency checks. It proposes explicit namespaces for interfaces, infrastructure, components, ports, and shared code, and uses Deptrac to enforce the dependency rules. The move from a diagram to a checked structure is already part of the upstream work.

## Start with the same application behind every surface

[![Stage 1: The urfave/cli CLI, Bubble Tea TUI, and Fyne GUI enter public operations; application behavior connects to local persistence and policy evaluation.](/assets/diagrams/explicit-architecture/01-boundaries.svg)](/assets/diagrams/explicit-architecture/01-boundaries.svg)

*Stage 1. Start with ownership. [Open or download the SVG](/assets/diagrams/explicit-architecture/01-boundaries.svg).*

Mixology has three executable composition roots: `main/cli`, `main/tui`, and `main/gui`. Each constructs the application and its domain surfaces. A fourth executable, `main/seed`, creates sample data. The application has seven contexts: Ingredients, Drinks, Inventory, Menus, Orders, Audit, and Tagging.

The urfave/cli CLI parses a request and exits. The Bubble Tea TUI owns a persistent message loop. The Fyne GUI owns retained controls, callbacks, and UI-thread publication. Each enters public application operations. A persistent session remembers the selected principal, while every operation gets fresh mutable middleware state.

That is an architectural claim with observable consequences. Retiring an ingredient through the CLI must produce the same domain transition as retiring it through a desktop form. A denied operation must fail below the presentation. A presenter must not need a DAO to finish its screen.

The [Fyne development journal](/articles/growing-mixology-with-fyne/) and [third-surface audit](/articles/using-a-third-surface-as-an-architecture-test/) supplied useful evidence. Complete selectors exposed first-page assumptions. The parity inventory found workflows absent from the TUI. Persistent clients exposed ownership of stale results, live edits, and shutdown. Those findings went back to the application or adapter that owned them.

The test was especially valuable because Fyne differed from Bubble Tea. Reusing a terminal view model would have hidden some of the pressure that revealed the boundary.

## Where the choices line up, and where they differ

| Concern | Explicit Architecture reference | Mixology's concrete choice |
| --- | --- | --- |
| Delivery | Driving adapters and application ports [1][ea1] | Domain-owned urfave/cli, Bubble Tea, and Fyne adapters call public Go facades. |
| Core organization | Components crossing application/domain layers [1][ea1] | Seven contexts, with named public contracts and private implementation. |
| Calls | Direct calls or a command/query bus [1][ea1] | Typed facade calls through one configured operation pipeline. |
| Shared contracts | Shared kernel below components [2][ea2] | A small kernel plus owner-local public models, queries, and events. |
| General reuse | Separate language extensions [2][ea2] | Named packages and runtime-specific toolkits; their actual imports determine their role. |
| Source structure | UI, Core, Infrastructure namespaces [3][ea3] | Vertical domain directories include their own surface adapters and DAOs. |
| Enforcement | Dependency rules checked with Deptrac [3][ea3] | Go visibility, arch-lint, topology tests, registration tests, and behavioral tests. |

I read the common principle as making ownership and dependency choices legible.

## Package the capability vertically

[![Stage 2: A domain slice separates surface adapters, the public facade and contracts, private commands and DAO, and owned event reactions.](/assets/diagrams/explicit-architecture/02-domain-slice.svg)](/assets/diagrams/explicit-architecture/02-domain-slice.svg)

*Stage 2. Add the public and private seams within one context. [Open the SVG](/assets/diagrams/explicit-architecture/02-domain-slice.svg).*

A regular operational context has this shape:

```text
app/domains/ingredients/
  module.go                 construction and public facade
  create.go, delete.go, ...  public application operations
  models/                   domain values and public request/result types
  queries/                  supported read contracts
  events/                   facts owned by Ingredients
  authz/                    Ingredients' Cedar schema and policies
  internal/commands/        write decisions
  internal/dao/             private persistence
  surfaces/cli/             command parsing and output
  surfaces/tui/             terminal presentation
  surfaces/gui/             desktop presentation
```

Contexts that react to events also have `handlers/`. Audit and Tagging use explicit profiles; Tagging includes `handlers/` and private association persistence in `internal/dao/`. The [topology test][topology] records those differences, so architectural consistency does not force an append-only audit reader to imitate a recipe editor.

I want a reader investigating ingredient retirement to find its public operation, command, policy, event, and adapters near each other. The cost is that a directory named `app/domains` contains more than pure domain code. A surface remains an outer adapter even when its path shares the domain's prefix. A DAO remains persistence implementation even when it lives below that same directory.

Go's `internal` rule provides part of the protection. Another context cannot import Ingredients' private DAO. But an Ingredients surface is inside the parent tree and Go permits that import. Mixology's [arch-lint rules][rules] reject it. Only the facade, queries, handlers, and internal implementation may consume that context's internals.

There is a useful distinction here: some bad programs fail to compile because of Go visibility or types; other imports are legal Go but fail the repository's architecture checks.

### Follow the imports inside one module

Menus is a useful module to open up because it has the full set of public queries, private commands, event reactions, readiness calculations, models, policy, and native adapters. This diagram shows **all 24 local production import edges** at the article's baseline, after grouping its CLI, TUI, and GUI packages into one surface node. An edge from that group means at least one of those packages has the import. **Every arrow points from the importer to its dependency.**

[![Menus package dependencies. Surfaces import the facade, queries, and models. The facade imports queries, commands, DAO, events, models, and authz. Queries, commands, and handlers import the private availability helper, DAO, and models; commands and handlers also import local event contracts. Events, availability, and DAO import models, and models imports authz. Arrows point from importer to dependency.](/assets/diagrams/explicit-architecture/07-module-dependencies.svg)](/assets/diagrams/explicit-architecture/07-module-dependencies.svg)

*Inside a module: [full-size SVG](/assets/diagrams/explicit-architecture/07-module-dependencies.svg), [vector PDF](/assets/diagrams/explicit-architecture/07-module-dependencies.pdf), or [PNG](/assets/diagrams/explicit-architecture/07-module-dependencies.png).*

The convergence on `models` is intentional: commands, reads, reactions, and adapters share domain values and public types. Menus' models import its `authz` vocabulary. The facade's direct DAO dependency includes registering the private schema during construction. Its event import supplies owner-local `TagsReplaced` facts for tagged edits. These are source dependencies; their placement does not describe an operation's execution order.

The absent shortcuts matter too. Surfaces cannot import `internal`, queries and handlers cannot import commands, and handlers cannot import domain facades. The graph records actual imports, while the [architecture rules][rules] constrain imports that could be added later. Peer contracts and shared mechanisms sit outside this local view.

## Accept public coupling, preserve write ownership

Graça's first article describes a stricter component-decoupling target, including moving shared events out of the publishing component. It also permits read-only access to another component's data in the shared-storage case. [Explicit Architecture #1][ea1]

Mixology makes a different pair of choices. Public events stay with their owner, and collaborators read through supported query packages. Inventory's retirement handler imports `ingredients/events`; Menus can import `drinks/queries`. This is real source coupling. I accept it because the name tells a reader who owns the contract and where a compatible change must be considered.

Private writes are the stronger boundary. Commands cannot import domain facades, and handlers cannot import facades or command packages. Commands may emit only their own domain's events. Queries cannot import commands. The [cross-domain boundary article](/articles/turning-cross-domain-calls-into-enforced-boundaries/) develops the rationale through retirement, while the [context map][architecture] names the actual relationships.

Business relationships can be reciprocal without requiring package cycles. Orders reads Inventory's public contracts; Inventory consumes Order events. Inventory adjustment events can affect Orders in return. Distinct query, model, event, and handler packages make those dependencies expressible without collapsing both modules into one package.

The tradeoff is deliberate. I retain compile-time navigation and an obvious contract owner, while accepting coordinated changes when that public contract evolves. Moving a module into another process would require revisiting these assumptions, especially serialization and transaction semantics.

### Follow the contract owner between modules

The next diagram separates **read dependencies** from **event-contract dependencies**. Its upper panels include every cross-context public-query import from non-surface production packages and every foreign event import from domain handlers at the same baseline. Multiple package imports between the same two contexts become one read edge. The event panel keeps handler and event packages distinct.

[![Between-module source dependencies. Orders reads Menus, Drinks, Inventory, and Ingredients; Menus reads Drinks, Inventory, and Ingredients; Drinks and Inventory read Ingredients. Tagging handlers consume TagsReplaced events from all five operational contexts. Receiving handlers import the event owner's package, so dependency arrows point opposite runtime event delivery. Separate examples show operational facades importing Tagging for registration, app composing Audit and middleware, and Menus native surfaces importing the public Drinks facade.](/assets/diagrams/explicit-architecture/08-between-module-dependencies.svg)](/assets/diagrams/explicit-architecture/08-between-module-dependencies.svg)

*Between modules: [full-size SVG](/assets/diagrams/explicit-architecture/08-between-module-dependencies.svg), [vector PDF](/assets/diagrams/explicit-architecture/08-between-module-dependencies.pdf), or [PNG](/assets/diagrams/explicit-architecture/08-between-module-dependencies.png).*

| Importing context | Public query owners | Foreign event owners imported by its handlers |
| --- | --- | --- |
| Drinks | Ingredients | Ingredients |
| Inventory | Ingredients | Ingredients, Orders |
| Menus | Drinks, Ingredients, Inventory | Drinks, Ingredients, Inventory, Orders |
| Orders | Drinks, Ingredients, Inventory, Menus | Drinks, Ingredients, Inventory, Menus |
| Tagging | None | Drinks, Ingredients, Inventory, Menus, Orders |

Event delivery and source dependency point in opposite directions. An Orders event reaches Inventory at runtime, while `inventory/handlers` imports `orders/events` in source. The generated dispatcher imports both the event types and the receiving handlers. Commands know the facts they publish; the dispatcher supplies knowledge of the receivers.

Audit and Tagging have different connections. `app.New` constructs the audit writer and injects its recording function into the pipeline. Operational facades import Tagging to register domain-owned targets. Read implementations use the shared `tag.Repository` port; tagged domain edits publish owner-local facts consumed by Tagging handlers. Native surfaces also have deliberate public facade dependencies, such as Menus' GUI and TUI importing Drinks to compose their screens. The lower panel shows selected examples of these dependencies. Public model imports, other shared packages, and third-party dependencies are outside the two upper graphs.

## Use CQRS where it clarifies an operation

Mixology separates requests that observe state from operations that decide and persist a change. It keeps both over the same embedded store. Read models, filters, projections, and query packages serve the questions the application asks; private commands own mutations.

There is no command bus resolving arbitrary request types at runtime. A facade selects its handler directly. This is the actual [retirement entry point][retire], with its signature omitted:

```go
return m.pipeline.LoadCommand(ctx, authz.ActionRetire,
    func(ctx *middleware.Context) (commands.RetirementTarget, error) {
        ingredient, err := m.queries.Get(ctx, id)
        return commands.RetirementTarget{
            Ingredient: ingredient,
            Retirement: retirement,
        }, err
    },
    m.commands.Retire,
)
```

The important detail is where the load happens. `LoadCommand` claims the command transaction before loading trusted authorization state. The pipeline authorizes the input, invokes the command, authorizes its result, then lets transactional dispatch and success auditing finish before commit.

The [generic-methods note](/notes/go-1-27-generic-methods-and-the-mixology-pipeline/) records how the API became a method on the configured pipeline. The current source uses Go 1.27 generic methods. The architectural point is independent of the syntax: a domain operation selects a typed execution shape, and the shared pipeline owns its surrounding behavior.

Queries have different shapes. `Query` authorizes the returned entity. `QueryResource` authorizes a known resource before a read. `PageQuery` continues consuming until it has a page of visible entities or reaches the end. A permission denial removes a row; an evaluation or storage failure fails the query. This is a more useful contract than authorizing a route and letting every client filter its own results. The [implementation][pipeline] makes those differences explicit.

This choice keeps normal calls easy to navigate and review. It gives up the uniform runtime routing offered by a command bus. The generated **event** dispatcher serves a different purpose: routing one published fact to its interested owners.

## Make the local transaction the event contract

[![Stage 3: One command loads and authorizes state, mutates, authorizes the result, dispatches prepared leaf reactions, records success audit, and commits together.](/assets/diagrams/explicit-architecture/03-transaction.svg)](/assets/diagrams/explicit-architecture/03-transaction.svg)

*Stage 3. Add time and atomicity. Arrows here describe execution, not imports. [Open the SVG](/assets/diagrams/explicit-architecture/03-transaction.svg).*

Mixology's most distinctive choice is the combination of synchronous events, prepared reactions, and a narrow handler context.

The retirement command changes the ingredient and queues the historically named `IngredientDeleted` event. The payload expresses retirement intent, including withdrawal, reason, and optional permanent replacement. The [generated dispatcher][dispatcher] sends it to Drinks, Inventory, Menus, and Orders inside the originating transaction.

Each receiver owns a different consequence:

| Owner | Retirement responsibility |
| --- | --- |
| Drinks | Rewrite future recipes for an approved replacement, or preserve unresolved required references in `review_required`. |
| Inventory | Retain physical stock and history; distinguish discontinued stock from quarantined stock. |
| Menus | Preserve curation and publication state while calculating resulting availability. |
| Orders | Retain immutable acceptance; block affected open commitments for explicit withdrawal. |

The [degradation article](/articles/preserving-truth-through-operational-degradation/) explains why those outcomes differ. A replacement changes a future recipe. It does not retroactively change what a customer accepted. A published menu can become degraded while remaining published; a draft with a known blocker cannot be promoted. Domain modeling supplies the distinctions that give the boundaries work to do.

Preparation addresses a subtler problem. If Menus calculates availability before Drinks rewrites a recipe, it may compute a different answer than if it runs afterward. “They share a transaction” does not solve that ordering dependency.

For each event, the dispatcher first runs every applicable `Handling` preparation, then runs the `Handle` methods. Menus uses the event's projected stock changes and Drinks' public pure retirement rule to calculate complete resulting Menu values. Its apply step persists those prepared values without re-reading sibling state. The [prepared-menu implementation][prepared] is the useful code trace.

The barrier is **per event**. A second queued event sees the first event's completed reactions inside the transaction. It is also a programming protocol, not snapshot isolation between arbitrary handlers: a handler that re-reads changed peers while applying can reintroduce order dependence. The [regression suite][regressions] deliberately permutes relevant handler orders to test the result.

Handlers receive `HandlerContext`, which exposes the transaction, principal, and audit effects but no `AddEvent` method. Ordinary handler code therefore cannot recursively publish through its supplied context. The [context definition][context] and import restrictions work together to keep reactions bounded.

This buys one understandable success boundary: the originating write, its reactions, and the successful audit commit together. It also couples their latency and availability. One failed reaction rolls the operation back; an expensive scan lengthens a SQLite write transaction. An event has removed the source command's knowledge of its consumers, not removed the cost of coordinating them.

## Give each atomic operation a domain owner

A command owns one SQL transaction, its leaf reactions, and one audit activity. [The implemented contract][commandownership] rejects commands invoked from command, query, or handler contexts, including reconstructed contexts. A SQL transaction can be claimed by only one command, so passing it through a sequence of public calls cannot recreate an outer workflow.

`Orders.AmendBatch` owns an atomic selection of approved amendments. It validates and authorizes the complete selection, plans reservation changes, and emits one `OrdersAmended` event. Inventory applies reservations, Orders reconciles released shortages, and Menus prepares availability from the complete delta. Every selected amendment commits or none does.

`Ingredients.Retire` is a separate command. When accepted orders need an approved amendment before retirement, the operator submits the amendment batch and then retires the ingredient. Each has its own transaction and activity; a failed retirement leaves the approved amendments intact.

On managed failure, the command's writes and success activity roll back before a failed activity records the attempted effects. An externally supplied transaction still leaves commit, rollback, and failure recording to its caller, but permits only one command. Audit distinguishes changed resources, inspected participants, and domain-authored before/after effects. One activity includes all leaf effects; there is no workflow correlation field. These activities explain outcomes rather than reconstructing the database by replay.

The [reciprocal-workflow workshop](/articles/growing-a-reciprocal-domain-workflow/) explores the next pressure point. Procurement is planned work involving suppliers, receipts, and approvals over time. Procurement would own durable state, with separate explicit approval and receipt commands driving leaf reactions. Spanning time does not itself require generic command orchestration; delivery infrastructure needs its own demonstrated requirement.

Replacing the local dispatcher with a broker would therefore change the business contract. Serialization, durable delivery, idempotency, retries, and partial outcomes would need explicit designs. An outbox could atomically record an intent to deliver; it would not make remote consumers part of this SQLite transaction.

## Let the shared foundations have different jobs

[![Stage 4: The context map rests on shared value types and narrow ports, with named mechanisms, concrete wiring, and independent presentation toolkits distinguished.](/assets/diagrams/explicit-architecture/04-foundations.svg)](/assets/diagrams/explicit-architecture/04-foundations.svg)

*Stage 4. Add shared vocabulary and supporting mechanisms. [Open the SVG](/assets/diagrams/explicit-architecture/04-foundations.svg).*

Mixology's `app/kernel` contains typed entity IDs, money, measurement, quality, and tags, including a narrow tag repository port. These are shared because domain operations must agree about identity and values. Canonical stock quantities and separate display/cost units are examples where a common type protects meaning across contexts.

The practical type-system preference is modest: distinguish identifiers, validate meaningful values, and withhold capabilities that should not be present. My [illegal-states article](/articles/making-illegal-states-unrepresentable-in-go/) develops the broader functional-modeling influence. Mixology's exported models and status values still require runtime validation.

Tagging demonstrates a different kind of sharing. Its module owns associations, while domains register target loaders and actions. The shared tag value type does not make Tagging the owner of Drinks' authorization or private data. The [tag repository port][tagport] and application registration give the cross-cutting feature an explicit seam. A consuming command accepts `tag.Edit` through `tag.Replace(&desired, expected)` and publishes its own `TagsReplaced` event. Tagging validates the desired set, compares expected tags, and authorizes before/after state during `Handling`; `Handle` persists associations through its private DAO. A veto rolls back the domain edit and tags together. The private persistence model declares the stable `entity_tags` table name and compound constraints.

`pkg` is more heterogeneous. `pkg/middleware` supplies mechanisms through configured dependencies. `pkg/store` owns a concrete persistence abstraction. Presentation toolkits own framework mechanics. Crucially, `pkg/dispatcher` contains generated imports of domain events and handlers. `pkg/authz` also assembles generated domain policy material. These are application wiring, despite their `pkg` prefix.

The `pkg` prefix therefore does not imply independence from domains. [`app.New`][composition] constructs the dispatcher and audit writer and supplies them to the pipeline through its configured boundaries. The generated dispatcher is allowed to know the receivers; the originating Ingredients command does not.

There is another deliberate compromise with a strict framework-free core: public models implement `CedarEntity`, and identifiers use Cedar identity representations. [Drink's model][drinkmodel] makes that dependency visible. Keeping policies domain-owned and evaluation centralized has been useful, but replacing Cedar would touch those contracts.

## Judge persistence boundaries by an actual replacement

The [bstore-to-SQLite migration](/articles/migrating-mixology-from-bstore-to-sqlite/) is more informative than a hypothetical promise to swap databases.

The early application centralized database lifecycle but still used bstore transaction and query types in DAOs. The migration introduced application-owned `Store`, `Tx`, and `Query[T]` types. It preserved public operation semantics while changing the driver, file format, registration, indexes, query execution, concurrency, and error translation.

The first SQLite adapter used JSON documents. The current store uses named `STRICT` relational tables, flattened scalar columns, and ordered child tables with cascading ownership foreign keys. Declared column indexes and compound constraints follow domain access paths. Each context explicitly registers private row types during composition. DAOs remain concrete implementation, and domain operations still share one transaction with reactions and success auditing. See the [store implementation][store] and its [guide][storeguide].

The owned typed query layer still carries schema, indexing, hydration, and query-planning responsibilities. Query-plan tests verify representative indexes; scalar and aggregate tests check exact values, optional presence, revisions, and rollback. The relational revision starts with freshly seeded data and rejects the former document layout. What survived both storage changes was the public behavior and ownership boundary; substantial execution code still changed.

Filtering makes the distinction precise. The public typed expression survives while the execution adapter is database-aware. SQLite receives only safe constraints implied by the full expression. Candidate rows acquire required data such as tags, then the complete predicate evaluates them before authorized paging yields results. For `A && (B || C)`, pushing down `A` can be safe; arbitrarily choosing `B` cannot be. The [filtering article](/articles/typed-filtering-over-sqlite/) and [SQL adapter][filter] show that contract.

The three processes may open the same local SQLite file. WAL supports the chosen reader/writer coordination; it does not permit simultaneous writers. A connection-local data-version monitor gives persistent clients coalesced invalidation hints, after which they repeat ordinary authorized queries. Those hints are neither domain events nor a durable change feed.

Revision tokens protect a separate boundary: stale intent. An editor can submit an old value even after the database serialized every write correctly. Updates and deletes therefore compare expected revisions at the store boundary, and complete tag replacements carry the expected old set. A refresh mechanism cannot substitute for either check.

## Carry policy into the experience without sharing the views

I also want the application boundary to explain what a person can do before they attempt a mutation.

Each context owns stable control IDs and action projections. Cedar denial hides a control. An authorized operation with an unmet prerequisite remains visible but disabled with a reason. Operational evaluation failure remains an error. Menus can add its readiness findings to an already-authorized Publish action.

The [navigation article](/articles/authorization-is-part-of-navigation/) follows that policy through routes, dashboard aggregates, rows, and actions. The [action-projection note](/notes/projecting-actions-across-user-interfaces/) describes the deliberately small shared state: ID, visibility, enabled status, and disabled reason. The command repeats authorization and invariants when it executes against current state.

This is the kind of presentation sharing I want. The [bespoke-views article](/articles/bespoke-views-over-a-shared-application-boundary/) explains why I stop short of a universal view model. The urfave/cli CLI needs argument parsing, command dispatch, and output. The Bubble Tea TUI needs message ownership and commands. The Fyne GUI needs retained-control reconciliation, execution/publication seams, and stale-generation checks. Their common semantics do not make those interaction models interchangeable.

The [TUI toolkit article](/articles/building-an-application-tui-toolkit/) records a separate influence: CODE Framework's shells and standard views, adapted to Bubble Tea's event loop. Toolkits share mechanics within a runtime after several domains establish the need. Domain surfaces contribute vocabulary and workflows. Architecture rules prevent toolkit-to-application imports, sibling-toolkit coupling, and a surface borrowing the wrong runtime's toolkit.

Errors cross the same boundary. A typed conflict or permission failure has one application meaning; each surface chooses its presentation. HTTP and gRPC mappings in the error package are mappings, not evidence that Mixology currently has HTTP or gRPC entrypoints.

## Explicit Modules: a map of the territory

**Explicit Modules** names the two things I want a reader to find in the code: a clear owner for each capability, and visible contracts between owners. **A domain-first modular monolith** is the descriptive subtitle. The Go accent is in the implementation: concrete facades, typed direct calls, small interfaces where a capability needs one, ordinary packages, and explicit construction.

The name also leaves room for the influences. Clean and Explicit Architecture, DDD, Fubu, and Screaming Architecture all contributed to my preferences. This map brings those preferences back to the application I can inspect and run.

[![Explicit Modules, with a Go accent. Three native surfaces enter public Go operations across Ingredients, Drinks, Menus, Inventory, Orders, Audit, and Tagging. A module cutaway separates adapters, facade and pipeline, models and policy, and private commands and persistence. Public queries and owner-local events connect contexts. A command loads and authorizes, decides and authorizes its result, applies prepared leaf reactions, records success audit, and commits in one SQLite transaction. Shared vocabulary, named mechanisms, and executable checks support these boundaries.](/assets/diagrams/explicit-architecture/06-explicit-modules.svg)](/assets/diagrams/explicit-architecture/06-explicit-modules.svg)

*Open the [full-size SVG](/assets/diagrams/explicit-architecture/06-explicit-modules.svg), download the [vector PDF](/assets/diagrams/explicit-architecture/06-explicit-modules.pdf), or save the [PNG](/assets/diagrams/explicit-architecture/06-explicit-modules.png). Source links work when the SVG is opened directly.*

Read the infographic from top to bottom:

1. **The territory.** CLI, TUI, and GUI have their own interaction models. Each entrypoint builds the application and calls its public operations. Seven named contexts own the work. The green districts represent ownership; their size and neighbors do not imply dependencies. Audit and Tagging retain their smaller explicit profiles.
2. **The module boundary.** A regular context keeps its adapters, facade, models, policy, commands, and persistence together. Peers read public query contracts and consume events published by the owning context. Each receiver owns its writes. Go visibility and arch-lint make those seams enforceable.
3. **The journey of a change.** One command, its leaf reactions, and its successful audit share a local transaction. Ingredient retirement reaches Drinks, Inventory, Menus, and Orders. Every applicable preparation runs before any receiver applies its reaction for that event. Managed failure rolls back the changes before recording the failed attempt separately.

The foundations have distinct jobs: the kernel supplies shared vocabulary and narrow ports, named packages supply mechanisms, and `app.New` plus generated wiring assemble the application. Each SQL transaction admits one domain-owned command. Batch work belongs to an explicit domain command; its reactions remain leaves.

Solid blue arrows indicate calls or contract use. Dashed amber arrows indicate execution. The earlier [detailed architecture atlas](/assets/diagrams/explicit-architecture/05-complete.svg) and its [PDF](/assets/diagrams/explicit-architecture/05-complete.pdf) remain available for the infrastructure and implementation details. The [diagram source and reading notes](/assets/diagrams/explicit-architecture/README.txt) identify the pinned baseline and regeneration commands.

The companion dependency views let me check that picture against the imports: [inside Menus](#follow-the-imports-inside-one-module) and [between contexts](#follow-the-contract-owner-between-modules). In those two views, every arrow is a source dependency, including the purple event-contract arrows.

## Make the map answerable to evidence

The [high-quality-software series preview](/articles/building-high-quality-software/) describes the wider teaching plan: turn important rules into executable constraints. Mixology applies that idea at several strengths.

| Claim | Evidence to inspect |
| --- | --- |
| A surface cannot bypass its own public module to import private writes | [Captured arch-lint rules][rules] |
| Contexts use the supported package vocabulary | [Topology tests][topology] |
| Every context joins the application | [Registration tests][registration] |
| Registered domain rows carry concurrency tokens | [Revision tests][revisions] |
| Retirement reactions preserve results across order changes | [Cross-domain regressions][regressions] |
| A failed amendment batch rolls back every selection and retains attempted effects | [Command integration tests][commandtests] |
| A transaction rejects nested or sequential commands | [Transaction ownership tests][transactiontests] |
| A native client uses the real application boundary | [Headless testing strategy](/articles/testing-native-go-desktop-applications-headlessly/) and [third-surface process tests](/articles/using-a-third-surface-as-an-architecture-test/) |

No single check proves the diagram. Import rules cannot show that a readiness calculation preserved the right business meaning. A successful integration test cannot prevent tomorrow's surface from acquiring a new DAO dependency. Both belong in the feedback loop.

The [.NET port](/projects/modular-monolith/) offers another comparison, with its own stated parity baseline. It asks which ideas survive a different language, persistence stack, and presentation framework. That supports treating the architecture as a set of responsibilities and contracts, while keeping language-specific mechanisms explicit.

What I borrowed most from Explicit Architecture was the habit of putting the whole application on one map and then asking whether the code tells the same story. My additions are preferences with consequences: owner-local public coupling, typed direct operations, bounded synchronous reactions, domain-owned atomic commands, practical type constraints, and bespoke interfaces. Their value is visible when a replacement, a failure, or a new feature crosses a boundary and the application still explains what happened.

[ea1]: https://herbertograca.com/2017/11/16/explicit-architecture-01-ddd-hexagonal-onion-clean-cqrs-how-i-put-it-all-together/
[ea2]: https://herbertograca.com/2018/07/07/more-than-concentric-layers/
[ea3]: https://herbertograca.com/2019/06/05/reflecting-architecture-and-domain-in-code/
[drawing]: https://docs.google.com/drawings/d/1E_hx5B4czRVFVhGJbrbPDlb_JFxJC8fYB86OMzZuAhg/edit
[pdf]: https://docs.google.com/drawings/d/1E_hx5B4czRVFVhGJbrbPDlb_JFxJC8fYB86OMzZuAhg/export/pdf
[baseline]: https://github.com/TheFellow/go-modular-monolith/tree/0d5e64b0455f7a5c96d4afada64654a5fdbb9a2c
[architecture]: https://github.com/TheFellow/go-modular-monolith/blob/0d5e64b0455f7a5c96d4afada64654a5fdbb9a2c/docs/architecture.md
[rules]: https://github.com/TheFellow/go-modular-monolith/blob/0d5e64b0455f7a5c96d4afada64654a5fdbb9a2c/.arch-lint.yaml
[topology]: https://github.com/TheFellow/go-modular-monolith/blob/0d5e64b0455f7a5c96d4afada64654a5fdbb9a2c/architecture/domain_topology_test.go
[registration]: https://github.com/TheFellow/go-modular-monolith/blob/0d5e64b0455f7a5c96d4afada64654a5fdbb9a2c/architecture/domain_registration_test.go
[revisions]: https://github.com/TheFellow/go-modular-monolith/blob/0d5e64b0455f7a5c96d4afada64654a5fdbb9a2c/architecture/revision_test.go
[retire]: https://github.com/TheFellow/go-modular-monolith/blob/0d5e64b0455f7a5c96d4afada64654a5fdbb9a2c/app/domains/ingredients/delete.go
[pipeline]: https://github.com/TheFellow/go-modular-monolith/blob/0d5e64b0455f7a5c96d4afada64654a5fdbb9a2c/pkg/middleware/run.go
[dispatcher]: https://github.com/TheFellow/go-modular-monolith/blob/0d5e64b0455f7a5c96d4afada64654a5fdbb9a2c/pkg/dispatcher/dispatcher_gen.go
[prepared]: https://github.com/TheFellow/go-modular-monolith/blob/0d5e64b0455f7a5c96d4afada64654a5fdbb9a2c/app/domains/menus/handlers/prepared.go
[context]: https://github.com/TheFellow/go-modular-monolith/blob/0d5e64b0455f7a5c96d4afada64654a5fdbb9a2c/pkg/middleware/context.go
[commandownership]: https://github.com/TheFellow/go-modular-monolith/blob/0d5e64b0455f7a5c96d4afada64654a5fdbb9a2c/docs/transactional-workflows.md
[regressions]: https://github.com/TheFellow/go-modular-monolith/blob/0d5e64b0455f7a5c96d4afada64654a5fdbb9a2c/app/cross_domain_regression_test.go
[commandtests]: https://github.com/TheFellow/go-modular-monolith/blob/0d5e64b0455f7a5c96d4afada64654a5fdbb9a2c/app/cross_domain_workflows_test.go
[tagport]: https://github.com/TheFellow/go-modular-monolith/blob/0d5e64b0455f7a5c96d4afada64654a5fdbb9a2c/app/kernel/tag/repository.go
[composition]: https://github.com/TheFellow/go-modular-monolith/blob/0d5e64b0455f7a5c96d4afada64654a5fdbb9a2c/app/app.go
[drinkmodel]: https://github.com/TheFellow/go-modular-monolith/blob/0d5e64b0455f7a5c96d4afada64654a5fdbb9a2c/app/domains/drinks/models/drink.go
[store]: https://github.com/TheFellow/go-modular-monolith/blob/1b6a586180c116eb1231b3e108e151879881b69b/pkg/store/store.go
[storeguide]: https://github.com/TheFellow/go-modular-monolith/blob/1b6a586180c116eb1231b3e108e151879881b69b/pkg/store/README.md
[filter]: https://github.com/TheFellow/go-modular-monolith/blob/1b6a586180c116eb1231b3e108e151879881b69b/pkg/filter/sql.go
[transactiontests]: https://github.com/TheFellow/go-modular-monolith/blob/0d5e64b0455f7a5c96d4afada64654a5fdbb9a2c/pkg/middleware/command_tx_test.go
