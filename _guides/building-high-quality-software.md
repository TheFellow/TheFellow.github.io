---
title: "Building High-Quality Software"
date: 2026-07-23 12:03:42 -0700
last_modified_at: 2026-09-06
excerpt: "A preview of eleven lessons about turning architectural intent into executable constraints, using Mixology as the worked example."
permalink: /articles/building-high-quality-software/
redirect_from: /guides/building-high-quality-software/
series: mixology
series_order: 1
order: 10
featured: true
status: "Series preview"
icon: "book"
accent: "#ffa94d"
topics: ["11 lessons", "Written + video", "Go architecture"]
---

{% include series-notice.html %}

<div class="notice--series" markdown="1">
**Series status:** this is a preview of a planned written and video series. Follow its development in [GitHub issue #23](https://github.com/TheFellow/go-modular-monolith/issues/23), or [explore the application](https://github.com/TheFellow/go-modular-monolith) now.
</div>

Architecture is easy to describe after the fact. Draw a few boxes, give each one a careful name, and the dependencies all point in the right direction. The harder question is what happens on an ordinary Tuesday, when the fastest way to finish a feature is to reach across one of those boxes.

[Mixology](https://github.com/TheFellow/go-modular-monolith) is a cocktail-bar application built to examine that question. The domain is intentionally approachable: ingredients become drinks, drinks appear on menus, menus receive orders, and inventory changes as those orders are completed. The interesting part is not the cocktail bar. It is the small set of rules that lets those parts cooperate without slowly becoming one undifferentiated package.

Consider retiring an ingredient. The ingredient may be held in inventory, used by several drinks, captured in pending orders, and exposed through published menus. One command has to record that catalog decision, carry an optional permanent replacement, let each dependent domain preserve the right kind of truth, leave an audit trail, and roll everything back if any reaction fails. That is enough behavior to make the architecture real.

In Mixology, the request enters the same application pipeline whether it came from the CLI, TUI, or GUI. The ingredient module loads the current entity, Cedar authorizes the operation and any proposed replacement, and the command records the historically named `IngredientDeleted` event. Generated dispatch sends that retirement fact to Drinks, Inventory, Menus, and Orders. Drinks rewrites future recipes or marks them for review, Inventory retains stock with discontinued or quarantined eligibility, Menus prepares retained item availability, and Orders blocks open commitments only for explicit withdrawal. Acceptance remains unchanged. Every handler works through its own persistence boundary, all share the original transaction, and none can emit another event. Integration tests exercise the whole path.

That single operation contains most of the series. The lessons below pull it apart, one decision at a time.

<figure class="article-figure">
  <img src="{{ '/assets/images/articles/mixology/lesson-map.png' | relative_url }}" alt="An ordered map of eleven Mixology lessons, moving from boundaries and types through the application pipeline, events, generation, errors, authorization, surfaces, owned seams, system tests, and deliberate limits on complexity.">
  <figcaption>The series moves from constraints the repository can enforce, through shared application behavior, to evidence that the complete system preserves those decisions.</figcaption>
</figure>

## 1. A boundary should resist the shortest path

A package layout can suggest a design, but it cannot preserve one. If Drinks can import the private command code inside Ingredients, eventually some reasonable person under a reasonable deadline will do exactly that. The code will work. The boundary will not.

Mixology treats the repository's dependency rules as source code. Twelve declarations in [`.arch-lint.yaml`](https://github.com/TheFellow/go-modular-monolith/blob/main/.arch-lint.yaml) keep shared packages independent of domains, isolate concrete presentation surfaces, and protect each domain's implementation packages. The internal-access rule is an allowlist: only the domain facade, its queries, its handlers, and other packages below `internal` may import that domain's internals. Models, events, authz, surfaces, and any future public layer are denied without requiring another package-specific rule. Captured rules also make the CLI, GUI, and TUI toolkits independent, permit each domain surface to import only the matching toolkit, and keep every surface independent of `main/**` composition. Cross-domain rules keep authorization contracts private to their owner and allow a command implementation to import only its own domain's events, while public models, queries, and events remain collaboration contracts.

Import rules cover dependency direction, but they do not catch every architectural omission. Mixology also treats the domain directories as the source of truth for two repository tests. The [topology test](https://github.com/TheFellow/go-modular-monolith/blob/main/architecture/domain_topology_test.go) rejects unrecognized peer layers such as an improvised `services` or `utils` package, while allowing explicit profiles for operational, audit, and tagging domains. The [composition test](https://github.com/TheFellow/go-modular-monolith/blob/main/architecture/domain_registration_test.go) compares those directories with `app.App` and `app.New`, so a new domain cannot exist in the tree without being exposed and initialized. Neither test introduces a second registration manifest. Together with import linting, they check dependency edges, the permitted architectural vocabulary, and whether every declared module actually joins the application.

The important part is the feedback loop. Introduce an illegal import and `go tool arch-lint` fails locally and in CI. The lesson will make that failure on purpose, then trace why the rule exists. The goal is not to admire a clean dependency graph. It is to make the wrong graph difficult to create.

## 2. Let the compiler carry the rules it can

Some mistakes are too cheap to make. A `DrinkID` and a `MenuID` may have the same representation, but accepting either in the same parameter gives a bug somewhere to hide. Mixology generates distinct ID types from one [entity definition](https://github.com/TheFellow/go-modular-monolith/blob/main/app/kernel/entity/entities.go), so exchanging them accidentally is a compile error rather than a test case someone has to remember.

The more interesting example is an ability that is missing. Commands receive a full middleware context and may add domain events. Event handlers receive the narrower [`HandlerContext`](https://github.com/TheFellow/go-modular-monolith/blob/main/pkg/middleware/context.go), which exposes the transaction, principal, and audit tracking but has no `AddEvent` method. A handler can update its own domain in response to an event; it cannot start an unbounded chain of new events.

Not every business rule belongs in a type, and forcing all of them there can make a design harder to read. This lesson is about recognizing the rules that do: distinctions and capabilities the compiler can enforce continuously, at almost no cost to the next person changing the system.

## 3. Make one path through the application

Logging, metrics, authorization, transaction management, event dispatch, and audit recording apply to almost every operation. Repeating them in every handler would not make the behavior explicit. It would make the differences between handlers accidental.

Mixology composes those concerns into a shared [middleware pipeline](https://github.com/TheFellow/go-modular-monolith/blob/main/pkg/middleware/chains.go). A domain method describes the operation it needs to perform; the pipeline supplies the surrounding guarantees. Go 1.27 generic methods put that vocabulary on the configured pipeline itself. `Pipeline.Command` handles caller-supplied state, while [`Pipeline.LoadCommand`](https://github.com/TheFellow/go-modular-monolith/blob/main/pkg/middleware/run.go) loads trusted current state inside the unit of work, authorizes it, invokes the command, and authorizes the resulting resource before anything commits. `Query`, `QueryResource`, `PageQuery`, and `LoadCommandActions` make the other supported operation shapes equally explicit.

That second authorization check matters. Permission is sometimes a property of a transition, not merely an action name. A policy may allow someone to edit a draft menu without allowing the same edit to produce a published menu. Looking at both sides gives policy enough information to express that distinction while the command remains concerned with menu behavior.

The tutorial will follow a command and a query through the chain and then remove one middleware at a time. The shape of the pipeline is less important than the property it creates: every surface and every domain operation gets the same application semantics by default.

## 4. Use events to coordinate, not to escape

Events are often introduced with a broker, eventual consistency, retries, and a new set of operational problems. None of those is required to benefit from event-shaped coordination.

`IngredientDeleted` carries retirement intent, time, reason, withdrawal choice, and an optional permanent replacement with its ratio. The generated dispatcher gives that fact independently to Drinks, Inventory, Menus, and Orders. Every `Handling` runs before any `Handle` for that event. Menus prepares resulting availability using projected stock and the same public pure recipe-retirement rule as Drinks, then persists the prepared values without reading sibling writes. Permutation tests prove that the result does not depend on reaction order.

All of that work remains inside the transaction opened for the retirement. If any recipe rewrite, stock disposition change, menu availability update, or order block fails, the ingredient, dependent state, and audit record return to their previous state together. The event separates knowledge between domains without giving up immediate consistency.

This is a deliberately constrained event model. Handlers are leaf nodes, event payloads carry useful state, and delivery is in-process. The lesson will explore what those constraints buy, where fat events become uncomfortable, and which pressures would justify crossing the boundary into asynchronous messaging.

The focused guide [Turning Cross-Domain Calls into Enforced Boundaries](/articles/turning-cross-domain-calls-into-enforced-boundaries/) follows this deletion from the tempting direct-call implementation through owned reactions, transactional dispatch, package rules, and integration evidence.

## 5. Generate repetition, preserve decisions

Code generation can remove work, or it can conceal a framework no one wants to debug. The useful dividing line is whether the generated code contains decisions.

Mixology's generators handle structure: routing event types to handlers, assembling per-domain Cedar policies, producing typed entity IDs, and keeping error constructors aligned with their test assertions. The decisions remain in ordinary Go, Cedar, and a few small definitions. The generated output is intentionally plain enough to open and read.

The dispatcher makes the tradeoff visible. Its generator scans event and handler declarations, then writes a direct type switch in [`dispatcher_gen.go`](https://github.com/TheFellow/go-modular-monolith/blob/main/pkg/dispatcher/dispatcher_gen.go). There is no runtime registry to misconfigure and no reflection in the dispatch path. Adding a handler changes the declarations; regeneration produces the boring wiring.

This lesson will build one of those generators from its inputs to its output. The broader subject is not how to generate more code. It is how to identify repetition that should have one source of truth without moving the system's meaning into a template.

## 6. Treat errors as part of the application contract

`"not found"` looks adequate until a second surface needs to interpret it. Then a string quietly becomes an API, and every caller invents its own way to parse or replace it.

Mixology defines a small error vocabulary in [`pkg/errors`](https://github.com/TheFellow/go-modular-monolith/tree/main/pkg/errors). A `NotFound` error is one application fact with several possible presentations: an HTTP 404, a gRPC `NotFound` code, CLI exit code 20, or a warning style in the TUI. Domain code chooses the fact. The surface chooses how that fact appears in its protocol.

The shared payload also separates diagnostic detail from a message safe to show to a user. Generated constructors and assertions keep the common cases easy enough that developers do not fall back to matching strings.

The eventual lesson will start with a single failing lookup and carry it through each representation. Errors are control flow at the point of failure, part of the public contract at a boundary, and presentation at the edge. Keeping those roles distinct makes all three easier to reason about.

## 7. Make authorization readable on its own

Authorization hidden inside business logic has two failure modes. It is difficult to audit because the rule is scattered through control flow, and it is difficult to reuse because every new surface has to reach the same branches in the same way.

Each Mixology domain keeps its permission rules in [Cedar policies](https://github.com/TheFellow/go-modular-monolith/tree/main/app/domains/drinks/authz). Go code supplies a principal, action, and resource; Cedar decides whether the relationship is allowed. A reviewer can read what a bartender or sommelier may do without first reconstructing a command handler.

The surrounding application still has important choices to make. A denied command returns a permission error. A list query silently omits entities the principal cannot see and keeps reading until it fills a page, so a hidden item neither fails the request nor creates mysteriously short pages. Counts and cursors must describe the visible result, not leak the existence of filtered data.

This lesson will trace one policy through command authorization, a single-entity query, and a paged list. The interesting part is not merely adopting a policy language. It is defining consistent authorization semantics everywhere data enters or leaves the application.

## 8. Keep surfaces at the edge

For a detailed treatment of the TUI architecture introduced in this section, continue with [Building an Application TUI Toolkit](/articles/building-an-application-tui-toolkit/).

Mixology exposes three adapters through three executables. `main/cli` handles commands and formatted output, `main/tui` launches the persistent Bubble Tea application, and `main/gui` opens the native Fyne desktop client. Each composition root owns its framework setup, flags, process lifetime, and application bootstrap. All three call the same domain modules and enter the same pipeline.

That leaves each surface with work that genuinely belongs to it: gathering input, managing interaction state, and presenting results. Persistent TUI and GUI processes keep explicit application sessions because login survives between interactions. A CLI invocation builds its context from the current request. Neither distinction changes how a drink is created or how a menu is authorized.

The TUI makes that separation concrete with an MVVM-like design. Domain view models own typed
selection, workflow state, commands, and domain-specific rendering. The root model owns
application-wide navigation, help, status, and the outer frame. Repeated terminal mechanics such
as searchable list/detail state, loading, and pane sizing live in `pkg/toolkits/tui`; forms and dialogs keep
their own local input behavior. Reusable contracts, components, styles, and keys live in
`pkg/toolkits/tui`, where domain surfaces can use them without depending on the `main/tui` composition
root. That ownership split matters: sharing presentation machinery does
not move domain decisions into a generic base view model, while every domain does not have to
rediscover the same viewport arithmetic.

The boundary is behavioral as well as structural. Every view model returns an `Interaction`
contract declaring whether its current state captures printable text or handles the back key, so
global shortcuts do not steal keystrokes from a filter, form, or dialog. A newly selected view is
sized before its initialization command can yield a renderable result, avoiding a transient
unbounded frame. Async results carry an entity identity and are accepted only by the editor that
started them. Saving disables duplicate submission and cancellation until the result returns.
These small protocols make input, message, and viewport ownership explicit instead of depending on
event-loop timing.

That is the useful part of MVVM here, rather than a literal translation of a XAML framework:
separate the visible rendering from testable presentation logic, keep view models independent of a
concrete view, and use explicit messages for coordination. Reusable components such as the tag
editor stay narrow, while shared mechanics are extracted only after multiple views establish the
same need. This keeps one large view model from accumulating navigation, persistence, rendering,
and every command without creating a framework in anticipation of reuse. The approach follows the
separation and testability described in
[CODE Magazine's MVVM overview](https://www.codemag.com/article/1201081/Windows-Phone-7-Development-Using-MVVM-and-Unit-Testing),
while treating its warning about duplicated or oversized presentation logic as an architectural
constraint.

Filtering provides a useful test of the boundary. A human-readable expression begins at the CLI, but the accepted fields belong to each domain's typed schema. [`pkg/filter`](https://github.com/TheFellow/go-modular-monolith/tree/main/pkg/filter) validates the expression and turns it into a transport-neutral tree. Safe comparisons can be pushed into SQLite while the complete predicate remains available for exact evaluation. A future HTTP or gRPC adapter would not need to invent another filtering language inside the domain.

The implementation now exercises the same operations through three surfaces, drives the TUI through
its real Bubble Tea program, and tests the Fyne client through presenters, retained widgets, and a
composed desktop lifecycle. The [third-surface audit](/articles/using-a-third-surface-as-an-architecture-test/)
found application leaks precisely where the CLI and TUI had shared an assumption, while the
[bespoke-view boundary](/articles/bespoke-views-over-a-shared-application-boundary/) kept each runtime's
interaction model native.

## 9. Give cross-cutting features an owned seam

Tags belong to drinks, ingredients, inventory, menus, and orders, but they are not business state
owned by any one of those domains. Copying tag persistence and commands into all five modules
would make one feature five implementations. Letting a central tagging package reach into every
domain's private storage would erase the boundaries the application is meant to preserve.

Mixology splits the responsibility instead. The shared [`tag` value
type](https://github.com/TheFellow/go-modular-monolith/tree/main/app/kernel/tag) defines canonical
labels and key/value tags. The [tagging
domain](https://github.com/TheFellow/go-modular-monolith/tree/main/app/domains/tagging) owns their
polymorphic associations and the uniform add, remove, list, and replace workflows. Each operational
domain depends on the narrow [`tag.Repository`](https://github.com/TheFellow/go-modular-monolith/blob/main/app/kernel/tag/repository.go) port, registers a loader and a bulk active-ID query, and supplies its own get, tag, and untag actions. The
generic workflow can therefore load complete domain-owned state, authorize mutations, and respect
each domain's lifecycle without importing private models or persistence.

That seam has to hold on reads as well as writes. Domain DAOs hydrate tags for a candidate set in
one type-scoped query and within the same transaction, avoiding both inconsistent snapshots and an
N+1 query per result. Complete-set replacements calculate whether the change needs tag permission,
untag permission, or both. When a surface supplies a complete tag set alongside a domain mutation,
the application-level `RunTaggedMutation` validates the set first, joins or opens an outer
transaction, runs the public domain mutation, and then calls `Tags.Replace` with the same middleware
context. Both operations retain their ordinary command-pipeline authorization, audit, and entity
touch behavior. A failure in either one rolls back the domain change, tag replacement, and their
audit effects together. When it owns the transaction, `RunWorkflow` then records one correlated failed attempt outside the rollback. Successful child activities share a workflow ID. Audit distinguishes changed resources, referenced participants, and domain-authored before/after effects; effects on a failed activity are attempted, not committed. GUI/TUI editors additionally supply the tag set they originally loaded, so a concurrent tag change conflicts independently of the entity revision.

Cross-domain discovery makes the ownership choice especially visible. `tags show` finds active
entities carrying one exact tag or any value for a key, while `tags summary` aggregates active use
by tag and entity type. These queries have tagging-domain Cedar actions of their own. Granting them
intentionally reveals matching entity types and IDs without reapplying five domains' read policies;
associations retained for soft-deleted entities remain hidden because each domain decides which IDs
are active in one bulk query. The distinction is part of the contract, not an accidental shortcut.

Once hydrated, the same tags serve presentation, filtering, and policy without acquiring implicit
application meaning. A CLI filter can select `tags contains "service=dinner"`, while Cedar can grant
access with `resource.hasTag("audience")` and `resource.getTag("audience") == "sommelier"`. The
application reserves neither key; policy gives the metadata meaning where meaning is required.

This lesson will follow seeded tags through canonicalization, centralized persistence,
domain-owned hydration and lifecycle checks, Cedar authorization, and discovery and editing in
the CLI, TUI, and GUI. Cross-surface end-to-end tests assert equivalent persisted results rather
than merely similar output. The broader question is how to build a feature that crosses every
boundary while making each intentional disclosure and ownership decision explicit.

## 10. Test the system that will run

An integration test becomes expensive when the application depends on a collection of remote infrastructure. In a one-process application with an embedded database, exercising the real stack can be the default.

[`testutil.NewFixture`](https://github.com/TheFellow/go-modular-monolith/blob/main/pkg/testutil/fixture.go) creates an isolated database and constructs the production application around it. Tests call public module methods with real authorization, transactions, dispatch, handlers, audit recording, and in-memory metrics. Builders make domain setup concise, but they do not bypass the application to insert convenient rows.

The cross-domain tests create ingredients, inventory, drinks, orders, and published menus, then exercise retirement through the public module. Discontinuation retains stock and honors usable accepted reservations; explicit withdrawal quarantines stock and blocks orders. Future recipes can be rewritten while acceptance remains unchanged. Explicit amendments move reservations without changing agreed prices, and a failure in a selected batch rolls every member back while preserving one failed workflow activity. Handler-order permutations and optional-ingredient contention test the edges of that design without recreating its orchestration with mocks.

This lesson will use the same fixture at three scales: a focused permission check, a cross-domain behavior test, and an audit assertion that names every touched entity. The aim is not to argue that every test should be an integration test. It is to keep the real path fast and accessible enough that the most important guarantees can be tested together.

## 11. Spend complexity only once the problem exists

Mixology has bounded contexts, policies, events, multiple surfaces, metrics, and transactional coordination. Its CLI, TUI, and GUI can run as independent processes over one embedded SQLite database. There is no broker, service mesh, deployment orchestrator, or distributed transaction protocol.

That combination is the point. A modular monolith is not a refusal to draw boundaries. It is a way to make those boundaries useful before paying the cost of putting a network between them. A failed event handler can roll back the originating command because both share a transaction. A test can construct the entire system because the entire system fits in a process.

The closing lesson will ask what evidence would justify changing that arrangement. Independent scaling, deployment ownership, fault isolation, or durability requirements may eventually outweigh the guarantees of a local transaction. If that day comes, enforced package boundaries and explicit events provide better seams than a monolith held together by convention.

Simple does not mean unfinished. It means every piece of complexity can point to the problem that earned it.

## Where the series will go next

The finished chapters will slow these ideas down. Each will begin with a failure mode, walk a small route through the repository, and end with an experiment that changes the code so the design can push back. They will also spend time on the limits: when the technique stops fitting, what it costs, and what a different system might choose instead.

For now, the repository is the complete worked example. Start with the [ingredient retirement tests](https://github.com/TheFellow/go-modular-monolith/blob/main/app/domains/ingredients/delete_test.go), follow the event into the generated dispatcher, and see how far one ordinary operation travels without dissolving the boundaries around it.
