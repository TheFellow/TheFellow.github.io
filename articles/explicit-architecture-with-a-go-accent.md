<!-- Generated from https://thefellow.github.io/articles/explicit-architecture-with-a-go-accent/ by scripts/generate_llm_content.py; do not edit. -->

# Explicit Architecture, with a Go Accent

Source: [https://thefellow.github.io/articles/explicit-architecture-with-a-go-accent/](https://thefellow.github.io/articles/explicit-architecture-with-a-go-accent/)

## Pyramid summary

- **~2 words:** Architecture lineage
- **~8 words:** Comparing Explicit Architecture with Mixology’s concrete Go design choices.
- **Expanded:** What Mixology borrows from Herberto Graça's Explicit Architecture, where it deliberately differs, and what transactions, types, three interfaces, and a storage migration taught me about those choices.

## Full content

**Part 14 of [Building Mixology](/series/mixology.md).**

Retiring an ingredient is a surprisingly good architecture exercise. The catalog changes, recipes may need a replacement, physical stock still exists, published menus may become harder to serve, and accepted orders must retain what was promised. The operation also needs authorization, a transaction, and an explanation of what happened. It can begin in a terminal command, a terminal application, or a desktop window.

That is the kind of problem I built [Mixology](/projects/go-modular-monolith.md) to explore. A great deal of its inspiration came from Herberto Graça's [Explicit Architecture series][ea1], together with DDD, ports and adapters, Clean Architecture, CQRS, functional modeling, and the application frameworks I have used. Mixology is where those influences meet my preferences: concrete public APIs, small capabilities, visible wiring, native presentation models, and rules the repository can enforce.

I narrowed some of those ideas to suit one local application with strong transactional behavior. Several of the most useful boundaries became clearer only after replacing the database or adding a third user interface.

At [commit `a7c2efd`][baseline], Procurement remains planned work, and newer amendment and stock-lifecycle operations have broader CLI coverage than GUI/TUI coverage.

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

The [Fyne development journal](/articles/growing-mixology-with-fyne.md) and [third-surface audit](/articles/using-a-third-surface-as-an-architecture-test.md) supplied useful evidence. Complete selectors exposed first-page assumptions. The parity inventory found workflows absent from the TUI. Persistent clients exposed ownership of stale results, live edits, and shutdown. Those findings went back to the application or adapter that owned them.

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

Contexts that react to events also have `handlers/`. Audit and Tagging use smaller explicit profiles. The [topology test][topology] records those differences, so architectural consistency does not force an append-only audit reader to imitate a recipe editor.

I want a reader investigating ingredient retirement to find its public operation, command, policy, event, and adapters near each other. The cost is that a directory named `app/domains` contains more than pure domain code. A surface remains an outer adapter even when its path shares the domain's prefix. A DAO remains persistence implementation even when it lives below that same directory.

Go's `internal` rule provides part of the protection. Another context cannot import Ingredients' private DAO. But an Ingredients surface is inside the parent tree and Go permits that import. Mixology's [arch-lint rules][rules] reject it. Only the facade, queries, handlers, and internal implementation may consume that context's internals.

There is a useful distinction here: some bad programs fail to compile because of Go visibility or types; other imports are legal Go but fail the repository's architecture checks.

## Accept public coupling, preserve write ownership

Graça's first article describes a stricter component-decoupling target, including moving shared events out of the publishing component. It also permits read-only access to another component's data in the shared-storage case. [Explicit Architecture #1][ea1]

Mixology makes a different pair of choices. Public events stay with their owner, and collaborators read through supported query packages. Inventory's retirement handler imports `ingredients/events`; Menus can import `drinks/queries`. This is real source coupling. I accept it because the name tells a reader who owns the contract and where a compatible change must be considered.

Private writes are the stronger boundary. Handlers cannot import domain facades or command packages. Commands may emit only their own domain's events. Queries cannot import commands. The [cross-domain boundary article](/articles/turning-cross-domain-calls-into-enforced-boundaries.md) develops the rationale through retirement, while the [context map][architecture] names the actual relationships.

Business relationships can be reciprocal without requiring package cycles. Orders reads Inventory's public contracts; Inventory consumes Order events. Inventory adjustment events can affect Orders in return. Distinct query, model, event, and handler packages make those dependencies expressible without collapsing both modules into one package.

The tradeoff is deliberate. I retain compile-time navigation and an obvious contract owner, while accepting coordinated changes when that public contract evolves. Moving a module into another process would require revisiting these assumptions, especially serialization and transaction semantics.

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

The important detail is where the load happens. `LoadCommand` opens or joins the unit of work before loading trusted authorization state. The pipeline authorizes the input, invokes the command, authorizes its result, then lets transactional dispatch and success auditing finish before commit.

The [generic-methods note](/notes/go-1-27-generic-methods-and-the-mixology-pipeline.md) records how the API became a method on the configured pipeline. The current source uses Go 1.27 generic methods. The architectural point is independent of the syntax: a domain operation selects a typed execution shape, and the shared pipeline owns its surrounding behavior.

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

The [degradation article](/articles/preserving-truth-through-operational-degradation.md) explains why those outcomes differ. A replacement changes a future recipe. It does not retroactively change what a customer accepted. A published menu can become degraded while remaining published; a draft with a known blocker cannot be promoted. Domain modeling supplies the distinctions that give the boundaries work to do.

Preparation addresses a subtler problem. If Menus calculates availability before Drinks rewrites a recipe, it may compute a different answer than if it runs afterward. “They share a transaction” does not solve that ordering dependency.

For each event, the dispatcher first runs every applicable `Handling` preparation, then runs the `Handle` methods. Menus uses the event's projected stock changes and Drinks' public pure retirement rule to calculate complete resulting Menu values. Its apply step persists those prepared values without re-reading sibling state. The [prepared-menu implementation][prepared] is the useful code trace.

The barrier is **per event**. A second queued event sees the first event's completed reactions inside the transaction. It is also a programming protocol, not snapshot isolation between arbitrary handlers: a handler that re-reads changed peers while applying can reintroduce order dependence. The [regression suite][regressions] deliberately permutes relevant handler orders to test the result.

Handlers receive `HandlerContext`, which exposes the transaction, principal, and audit effects but no `AddEvent` method. Ordinary handler code therefore cannot recursively publish through its supplied context. The [context definition][context] and import restrictions work together to keep reactions bounded.

This buys one understandable success boundary: the originating write, its reactions, and the successful audit commit together. It also couples their latency and availability. One failed reaction rolls the operation back; an expensive scan lengthens a SQLite write transaction. An event has removed the source command's knowledge of its consumers, not removed the cost of coordinating them.

## Put orchestration where its lifetime is visible

A leaf reaction is too small for every workflow. Mixology's answer is explicit application composition.

`App.AmendOrders` runs a selected batch of ordinary amendment commands. `App.RetireIngredient` can combine selected amendments with retirement. [`middleware.RunWorkflow`][workflow] supplies the shared transaction and workflow correlation. Each command retains its action and domain semantics.

On managed failure, child success activities roll back with their writes. The workflow owner then records one failed activity containing attempted effects. An externally supplied transaction changes ownership: its caller remains responsible for commit, rollback, and failure recording. An audit failure is preserved alongside the business failure.

Audit consequently distinguishes changed resources, inspected participants, and domain-authored effects. It explains the attempt and its outcome. The database is not reconstructed by replaying those activities; this is not event sourcing.

The [reciprocal-workflow workshop](/articles/growing-a-reciprocal-domain-workflow.md) explores the next pressure point. Procurement is planned work involving suppliers, receipts, and potentially approvals over time. A process manager or outbox would earn its place when progress must survive separate commits, human waits, or external delivery.

Replacing the local dispatcher with a broker would therefore change the business contract. Serialization, durable delivery, idempotency, retries, and partial outcomes would need explicit designs. An outbox could atomically record an intent to deliver; it would not make remote consumers part of this SQLite transaction.

## Let the shared foundations have different jobs

[![Stage 4: The context map rests on shared value types and narrow ports, with named mechanisms, concrete wiring, and independent presentation toolkits distinguished.](/assets/diagrams/explicit-architecture/04-foundations.svg)](/assets/diagrams/explicit-architecture/04-foundations.svg)

*Stage 4. Add shared vocabulary and supporting mechanisms. [Open the SVG](/assets/diagrams/explicit-architecture/04-foundations.svg).*

Mixology's `app/kernel` contains typed entity IDs, money, measurement, quality, and tags, including a narrow tag repository port. These are shared because domain operations must agree about identity and values. Canonical stock quantities and separate display/cost units are examples where a common type protects meaning across contexts.

The practical type-system preference is modest: distinguish identifiers, validate meaningful values, and withhold capabilities that should not be present. My [illegal-states article](/articles/making-illegal-states-unrepresentable-in-go.md) develops the broader functional-modeling influence. Mixology's exported models and status values still require runtime validation.

Tagging demonstrates a different kind of sharing. Its module owns associations, while domains register target loaders and actions. The shared tag value type does not make Tagging the owner of Drinks' authorization or private data. The [tag repository port][tagport] and application registration give the cross-cutting feature an explicit seam.

`pkg` is more heterogeneous. `pkg/middleware` supplies mechanisms through configured dependencies. `pkg/store` owns a concrete persistence abstraction. Presentation toolkits own framework mechanics. Crucially, `pkg/dispatcher` contains generated imports of domain events and handlers. `pkg/authz` also assembles generated domain policy material. These are application wiring, despite their `pkg` prefix.

The `pkg` prefix therefore does not imply independence from domains. [`app.New`][composition] constructs the dispatcher and audit writer and supplies them to the pipeline through its configured boundaries. The generated dispatcher is allowed to know the receivers; the originating Ingredients command does not.

There is another deliberate compromise with a strict framework-free core: public models implement `CedarEntity`, and identifiers use Cedar identity representations. [Drink's model][drinkmodel] makes that dependency visible. Keeping policies domain-owned and evaluation centralized has been useful, but replacing Cedar would touch those contracts.

## Judge persistence boundaries by an actual replacement

The [bstore-to-SQLite migration](/articles/migrating-mixology-from-bstore-to-sqlite.md) is more informative than a hypothetical promise to swap databases.

The early application centralized database lifecycle but still used bstore transaction and query types in DAOs. The migration introduced application-owned `Store`, `Tx`, and `Query[T]` types. It preserved public operation semantics while changing the driver, file format, registration, indexes, query execution, concurrency, and error translation.

The current store uses SQLite JSON records keyed by model identity and ID, with declared expression indexes and constraints. Each context explicitly registers private row types during composition. DAOs remain concrete implementation, and domain operations still share one transaction with reactions and success auditing. See the [store implementation][store] and its [guide][storeguide].

That design has a cost. JSON records and an owned typed query layer are a particular storage strategy with particular indexing and query-planning responsibilities. They do not provide every benefit of a bespoke relational schema. What survived the migration was the public behavior and ownership boundary; substantial execution code still changed.

Filtering makes the distinction precise. The public typed expression survives while the execution adapter is database-aware. SQLite receives only safe constraints implied by the full expression. Candidate rows acquire required data such as tags, then the complete predicate evaluates them before authorized paging yields results. For `A && (B || C)`, pushing down `A` can be safe; arbitrarily choosing `B` cannot be. The [filtering article](/articles/typed-filtering-over-sqlite.md) and [SQL adapter][filter] show that contract.

The three processes may open the same local SQLite file. WAL supports the chosen reader/writer coordination; it does not permit simultaneous writers. A connection-local data-version monitor gives persistent clients coalesced invalidation hints, after which they repeat ordinary authorized queries. Those hints are neither domain events nor a durable change feed.

Revision tokens protect a separate boundary: stale intent. An editor can submit an old value even after the database serialized every write correctly. Updates and deletes therefore compare expected revisions at the store boundary, and complete tag replacements carry the expected old set. A refresh mechanism cannot substitute for either check.

## Carry policy into the experience without sharing the views

I also want the application boundary to explain what a person can do before they attempt a mutation.

Each context owns stable control IDs and action projections. Cedar denial hides a control. An authorized operation with an unmet prerequisite remains visible but disabled with a reason. Operational evaluation failure remains an error. Menus can add its readiness findings to an already-authorized Publish action.

The [navigation article](/articles/authorization-is-part-of-navigation.md) follows that policy through routes, dashboard aggregates, rows, and actions. The [action-projection note](/notes/projecting-actions-across-user-interfaces.md) describes the deliberately small shared state: ID, visibility, enabled status, and disabled reason. The command repeats authorization and invariants when it executes against current state.

This is the kind of presentation sharing I want. The [bespoke-views article](/articles/bespoke-views-over-a-shared-application-boundary.md) explains why I stop short of a universal view model. The urfave/cli CLI needs argument parsing, command dispatch, and output. The Bubble Tea TUI needs message ownership and commands. The Fyne GUI needs retained-control reconciliation, execution/publication seams, and stale-generation checks. Their common semantics do not make those interaction models interchangeable.

The [TUI toolkit article](/articles/building-an-application-tui-toolkit.md) records a separate influence: CODE Framework's shells and standard views, adapted to Bubble Tea's event loop. Toolkits share mechanics within a runtime after several domains establish the need. Domain surfaces contribute vocabulary and workflows. Architecture rules prevent toolkit-to-application imports, sibling-toolkit coupling, and a surface borrowing the wrong runtime's toolkit.

Errors cross the same boundary. A typed conflict or permission failure has one application meaning; each surface chooses its presentation. HTTP and gRPC mappings in the error package are mappings, not evidence that Mixology currently has HTTP or gRPC entrypoints.

## Read the complete map in several directions

[![Complete Mixology architecture atlas: seven domain contexts, three driving surfaces, typed operation paths, concrete infrastructure, transactional event fan-out, shared contracts, generated wiring, and executable checks.](/assets/diagrams/explicit-architecture/05-complete.svg)](/assets/diagrams/explicit-architecture/05-complete.svg)

*Stage 5. [Open the full-size SVG](/assets/diagrams/explicit-architecture/05-complete.svg) or [download the printable PDF](/assets/diagrams/explicit-architecture/05-complete.pdf).*

The complete drawing has several reading paths:

- **Outside inward:** a concrete surface reaches public application operations and domain decisions.
- **Across contexts:** public queries answer questions; owner-local events announce facts; interested contexts own reactions.
- **Through time:** a command and prepared reactions complete inside one transaction before successful audit and commit.
- **Down to foundations:** shared values, narrow ports, concrete adapters, and application wiring have different responsibilities.
- **Along the evidence strip:** types, import rules, topology, composition, regression tests, and independent clients check different claims.

The circles describe conceptual responsibility. They are not a generated import graph. Solid dependency arrows and numbered execution arrows are labeled separately, and each detailed panel links to the source it describes when the SVG is opened directly. The [diagram source and reading notes](/assets/diagrams/explicit-architecture/README.txt) identify the baseline, conventions, and regeneration command.

## Make the map answerable to evidence

The [high-quality-software series preview](/articles/building-high-quality-software.md) describes the wider teaching plan: turn important rules into executable constraints. Mixology applies that idea at several strengths.

| Claim | Evidence to inspect |
| --- | --- |
| A surface cannot bypass its own public module to import private writes | [Captured arch-lint rules][rules] |
| Contexts use the supported package vocabulary | [Topology tests][topology] |
| Every context joins the application | [Registration tests][registration] |
| Registered domain rows carry concurrency tokens | [Revision tests][revisions] |
| Retirement reactions preserve results across order changes | [Cross-domain regressions][regressions] |
| A failed selected workflow rolls back and retains correlated failure evidence | [Workflow tests][workflowtests] |
| A native client uses the real application boundary | [Headless testing strategy](/articles/testing-native-go-desktop-applications-headlessly.md) and [third-surface process tests](/articles/using-a-third-surface-as-an-architecture-test.md) |

No single check proves the diagram. Import rules cannot show that a readiness calculation preserved the right business meaning. A successful integration test cannot prevent tomorrow's surface from acquiring a new DAO dependency. Both belong in the feedback loop.

The [.NET port](/projects/modular-monolith.md) offers another comparison, with its own stated parity baseline. It asks which ideas survive a different language, persistence stack, and presentation framework. That supports treating the architecture as a set of responsibilities and contracts, while keeping language-specific mechanisms explicit.

What I borrowed most from Explicit Architecture was the habit of putting the whole application on one map and then asking whether the code tells the same story. My additions are preferences with consequences: owner-local public coupling, typed direct operations, bounded synchronous reactions, explicit workflow ownership, practical type constraints, and bespoke interfaces. Their value is visible when a replacement, a failure, or a new feature crosses a boundary and the application still explains what happened.

[ea1]: https://herbertograca.com/2017/11/16/explicit-architecture-01-ddd-hexagonal-onion-clean-cqrs-how-i-put-it-all-together/
[ea2]: https://herbertograca.com/2018/07/07/more-than-concentric-layers/
[ea3]: https://herbertograca.com/2019/06/05/reflecting-architecture-and-domain-in-code/
[drawing]: https://docs.google.com/drawings/d/1E_hx5B4czRVFVhGJbrbPDlb_JFxJC8fYB86OMzZuAhg/edit
[pdf]: https://docs.google.com/drawings/d/1E_hx5B4czRVFVhGJbrbPDlb_JFxJC8fYB86OMzZuAhg/export/pdf
[baseline]: https://github.com/TheFellow/go-modular-monolith/tree/a7c2efda8c0cd905089a27060242ff841bb0ad41
[architecture]: https://github.com/TheFellow/go-modular-monolith/blob/a7c2efda8c0cd905089a27060242ff841bb0ad41/docs/architecture.md
[rules]: https://github.com/TheFellow/go-modular-monolith/blob/a7c2efda8c0cd905089a27060242ff841bb0ad41/.arch-lint.yaml
[topology]: https://github.com/TheFellow/go-modular-monolith/blob/a7c2efda8c0cd905089a27060242ff841bb0ad41/architecture/domain_topology_test.go
[registration]: https://github.com/TheFellow/go-modular-monolith/blob/a7c2efda8c0cd905089a27060242ff841bb0ad41/architecture/domain_registration_test.go
[revisions]: https://github.com/TheFellow/go-modular-monolith/blob/a7c2efda8c0cd905089a27060242ff841bb0ad41/architecture/revision_test.go
[retire]: https://github.com/TheFellow/go-modular-monolith/blob/a7c2efda8c0cd905089a27060242ff841bb0ad41/app/domains/ingredients/delete.go
[pipeline]: https://github.com/TheFellow/go-modular-monolith/blob/a7c2efda8c0cd905089a27060242ff841bb0ad41/pkg/middleware/run.go
[dispatcher]: https://github.com/TheFellow/go-modular-monolith/blob/a7c2efda8c0cd905089a27060242ff841bb0ad41/pkg/dispatcher/dispatcher_gen.go
[prepared]: https://github.com/TheFellow/go-modular-monolith/blob/a7c2efda8c0cd905089a27060242ff841bb0ad41/app/domains/menus/handlers/prepared.go
[context]: https://github.com/TheFellow/go-modular-monolith/blob/a7c2efda8c0cd905089a27060242ff841bb0ad41/pkg/middleware/context.go
[workflow]: https://github.com/TheFellow/go-modular-monolith/blob/a7c2efda8c0cd905089a27060242ff841bb0ad41/pkg/middleware/workflow.go
[regressions]: https://github.com/TheFellow/go-modular-monolith/blob/a7c2efda8c0cd905089a27060242ff841bb0ad41/app/cross_domain_regression_test.go
[workflowtests]: https://github.com/TheFellow/go-modular-monolith/blob/a7c2efda8c0cd905089a27060242ff841bb0ad41/app/cross_domain_workflows_test.go
[tagport]: https://github.com/TheFellow/go-modular-monolith/blob/a7c2efda8c0cd905089a27060242ff841bb0ad41/app/kernel/tag/repository.go
[composition]: https://github.com/TheFellow/go-modular-monolith/blob/a7c2efda8c0cd905089a27060242ff841bb0ad41/app/app.go
[drinkmodel]: https://github.com/TheFellow/go-modular-monolith/blob/a7c2efda8c0cd905089a27060242ff841bb0ad41/app/domains/drinks/models/drink.go
[store]: https://github.com/TheFellow/go-modular-monolith/blob/a7c2efda8c0cd905089a27060242ff841bb0ad41/pkg/store/store.go
[storeguide]: https://github.com/TheFellow/go-modular-monolith/blob/a7c2efda8c0cd905089a27060242ff841bb0ad41/pkg/store/README.md
[filter]: https://github.com/TheFellow/go-modular-monolith/blob/a7c2efda8c0cd905089a27060242ff841bb0ad41/pkg/filter/sql.go
