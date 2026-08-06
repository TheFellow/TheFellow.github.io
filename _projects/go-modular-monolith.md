---
title: "go-modular-monolith"
date: 2026-07-23 12:03:42 -0700
last_modified_at: 2026-08-06 12:00:00 -0700
excerpt: "A Go reference application that makes modular boundaries and cross-cutting concerns executable."
language: "Go"
license: "MIT"
repository_url: "https://github.com/TheFellow/go-modular-monolith"
last_updated: 2026-08-05
series_url: "/series/mixology/"
order: 10
featured: true
icon: "modules"
accent: "#63e6be"
topics: ["Architecture", "Reference app", "Cedar"]
---

<div class="project-meta"><span>Go</span><span>Software architecture</span><span>Cedar</span><span>MIT</span><span>Updated {{ page.last_updated | date: "%B %-d, %Y" }}</span></div>

[View the repository](https://github.com/TheFellow/go-modular-monolith){: .btn .btn--primary }
[Start with the repository guide](https://github.com/TheFellow/go-modular-monolith#five-minute-start){: .btn }
[Read the Mixology series](/series/mixology/){: .btn }
[Read the GUI surface article](/articles/growing-mixology-with-fyne/){: .btn }

go-modular-monolith, also called Mixology, is an opinionated reference application organized around bounded contexts for a cocktail-bar domain. Its CLI, Bubble Tea TUI, and Fyne desktop client are separate composition roots over the same application and embedded database. That leaves the complexity budget for boundaries, types, authorization, transactions, events, and tooling that enforce the design.

The repository's central argument is that important rules should be executable. Package boundaries fail the build when they are crossed. The type system withholds capabilities that a caller should not have. Authorization, transactions, events, and audit all surround domain operations through one path, regardless of whether a request began in the CLI, Bubble Tea TUI, or Fyne desktop client.

Retiring an ingredient makes those claims concrete. The command may name a compatible permanent replacement, or it may admit that no replacement is known. Independent event handlers prepare their work before any of them mutate state, then update inventory, recipes, and historical orders inside the originating transaction. Menu readiness reflects the resulting state without destructively changing menu membership. A replacement rewrites future recipes. An unresolved required ingredient moves its drinks to `review_required`, blocks affected orders, and leaves published menus visible in a degraded state. If one handler fails, the complete operation rolls back. No handler reaches into another domain's internals, and no message broker is required to keep the modules separate.

That lifecycle also separates degradation from promotion. Existing published menus can honestly report that service has deteriorated, but a draft menu with a known blocker cannot be published. Menus owns the readiness report and its Cedar permission, so manager and owner surfaces can inspect precise blockers and warnings without disclosing operational details to every actor. CLI, TUI, and GUI all expose the same retirement choices and readiness decision, while their interaction and asynchronous loading remain native to each surface.

That balance is what makes Mixology useful as a teaching vehicle. It has enough behavior for boundaries and cross-cutting concerns to matter, while the complete application still fits in one process and its tests need no external infrastructure. The code can show the consequence of a design choice without first asking the reader to assemble a distributed system.

Adding the Fyne client also turned surface parity into an executable application contract. The audit did not merely bring the new desktop view up to the existing interfaces. It found missing TUI workflows, CLI fidelity gaps, inconsistent paging and filtering, duplicated dashboard calculations, and mutations whose domain change and complete tag set were not atomic. Shared application services and cross-surface tests now correct those behaviors for every adapter while each presentation remains bespoke.

The desktop shell reflects projected capabilities before a user enters a workspace. Navigation and dashboard cards consume domain-owned collection controls, denied dashboard aggregates are omitted without masking operational failures, and Cedar continues to filter rows within each visible workspace. The persistent navigation keeps the active actor and role visible throughout the session.

Action availability now follows the same cross-surface discipline. Every domain owns stable control IDs and a projector that combines Cedar decisions on real entities with durable lifecycle prerequisites. Entity-filtered catalogs expose public collection entry while their query pipelines continue to authorize and elide individual rows; Tagging resolves target actions from the owning domain's registry. Permission denial hides an action, while an unmet business condition leaves an authorized action visible and explains why it cannot run. GUI, TUI, and desktop composition consume the same framework-neutral state, then add only transient constraints such as dirty forms or requests in flight. Commands still repeat authorization and invariants when they execute, so presentation state improves guidance without becoming the security boundary.

The persistent left navigation opens each authorized workspace through a table and detail layout. Native headers resize columns and support domain ordering, tags render as compact pills, authorized row menus expose contextual operations, and detail action bars keep domain transitions beside the selected state. Create and edit operations use full-width scrolling forms, while token editors validate and normalize tags without exposing their CSV representation. The TUI follows the same product-level interaction language in terminal-native form: arrows select fields, `e` or Enter begins editing, Enter accepts a value, and Escape cancels it. CLI, TUI, and GUI also open `data/mixology.db` by default, so each surface presents the same stored application state.

The current package shape repeats the same ownership story at every level. `app/domains` contains seven bounded contexts: audit, drinks, ingredients, inventory, menus, orders, and tagging. A full operational context exposes its facade at the package root, keeps collaboration contracts in `models`, `queries`, and `events`, owns Cedar policy in `authz`, and hides commands and persistence below `internal`. Its CLI, GUI, and TUI adapters sit together below `surfaces`, so readers can follow one capability vertically without mixing presentation code into the domain's public API. Audit and tagging use smaller explicit profiles because they need fewer layers.

The repository now keeps that first code trace explicit. Its compact root guide leads from an executable through one domain surface and into the public module, then links to focused architecture, feature, entrypoint, domain-surface, and presentation-toolkit guides beside the code they describe.

Code shared by every context has a named home rather than accumulating in a generic utility package. `app/kernel` owns application value types and narrow ports. `pkg` owns transport-independent infrastructure such as authorization, dispatch, filtering, middleware, paging, storage, and telemetry. Presentation mechanics live in three application-independent `pkg/toolkits` packages. Domain surfaces may use only the toolkit for the same presentation mode, toolkits cannot import application code or each other, and no surface may import executable composition from `main`.

The three user-facing programs complete that symmetry. `main/cli`, `main/gui`, and `main/tui` each assemble the application and their domain surfaces, while `main/seed` creates representative data. This keeps framework setup, process lifetime, navigation, and cross-domain workspace composition at the edge. The application root separately proves that every declared domain is exposed and initialized, so adding a directory is not enough to add a module.

```text
app/
  kernel/                         shared value types and narrow ports
  domains/<context>/
    module.go                     public facade
    {models,queries,events}/      collaboration contracts
    authz/                        domain-owned Cedar policy
    internal/{commands,dao}/      write logic and persistence
    surfaces/{cli,gui,tui}/       bespoke presentation adapters
pkg/
  presentation/actions/           framework-neutral action state
  toolkits/{cli,gui,tui}/         reusable presentation mechanics
  middleware/                     authorization, transactions, events, audit, and metrics
  {authn,authz,dispatcher,filter,store}/
main/
  {cli,gui,tui}/                  executable composition roots
  seed/                           sample-data executable
```

The boundaries are checked from several directions. Captured `arch-lint` rules apply the same restrictions to present and future domains and surfaces. Topology tests reject unrecognized peer layers, and composition tests compare the domain directories with the modules exposed by the application. Application fixtures then exercise the real embedded store, middleware, authorization, dispatch, audit, and domain handlers. Cross-surface tests mutate through one adapter and observe through another, checking shared behavior without requiring the adapters to share their implementation.

The [Building High-Quality Software preview](/articles/building-high-quality-software/) follows that
thread through eleven planned lessons: enforced boundaries, constraints encoded in types, the
shared operation pipeline, transactional events, focused code generation, error contracts,
policy-based authorization, interchangeable CLI and bespoke MVVM-style TUI and GUI surfaces, an owned seam for
cross-domain features such as tags, production-shaped tests, and the discipline to stop before
simple becomes simplistic.
