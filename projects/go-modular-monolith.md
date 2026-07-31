<!-- Generated from https://thefellow.github.io/projects/go-modular-monolith/ by scripts/generate_llm_content.py; do not edit. -->

# go-modular-monolith

Source: [https://thefellow.github.io/projects/go-modular-monolith/](https://thefellow.github.io/projects/go-modular-monolith/)

## Pyramid summary

- **~2 words:** Executable architecture
- **~8 words:** A Go reference app enforcing modular boundaries and cross-cutting concerns.
- **Expanded:** A Go reference application that makes modular boundaries and cross-cutting concerns executable.

## Full content

[View the repository](https://github.com/TheFellow/go-modular-monolith)
[Preview the tutorial series](/guides/building-high-quality-software.md)
[Read the GUI surface guide](/guides/growing-mixology-with-fyne.md)

go-modular-monolith, also called Mixology, is an opinionated reference application organized around bounded contexts for a cocktail-bar domain. Its CLI, Bubble Tea TUI, and Fyne desktop client are separate composition roots over the same application and embedded database. That leaves the complexity budget for boundaries, types, authorization, transactions, events, and tooling that enforce the design.

The repository's central argument is that important rules should be executable. Package boundaries fail the build when they are crossed. The type system withholds capabilities that a caller should not have. Authorization, transactions, events, and audit all surround domain operations through one path, regardless of whether a request began in the CLI, Bubble Tea TUI, or Fyne desktop client.

Deleting an ingredient makes those claims concrete. The command can affect inventory, every drink that uses the ingredient, and every menu carrying those drinks. Independent event handlers prepare their work before any of them mutate state, then apply the complete change inside the originating transaction. If one handler fails, the ingredient and all of its dependent state remain untouched. No handler reaches into another domain's internals, and no message broker is required to keep the modules separate.

That balance is what makes Mixology useful as a teaching vehicle. It has enough behavior for boundaries and cross-cutting concerns to matter, while the complete application still fits in one process and its tests need no external infrastructure. The code can show the consequence of a design choice without first asking the reader to assemble a distributed system.

Adding the Fyne client also turned surface parity into an executable application contract. The audit did not merely bring the new desktop view up to the existing interfaces. It found missing TUI workflows, CLI fidelity gaps, inconsistent paging and filtering, duplicated dashboard calculations, and mutations whose domain change and complete tag set were not atomic. Shared application services and cross-surface tests now correct those behaviors for every adapter while each presentation remains bespoke.

The desktop shell reflects authorization before a user enters a workspace. Navigation and dashboard cards include only workspaces with an authorized read path, denied dashboard aggregates are omitted without masking operational failures, and Cedar continues to filter rows within each visible workspace. The persistent navigation keeps the active actor and role visible throughout the session.

The persistent left navigation opens each authorized workspace through a table and detail layout. Native headers resize columns and support domain ordering, tags render as compact pills, authorized row menus expose contextual operations, and detail action bars keep domain transitions beside the selected state. Create and edit operations use full-width scrolling forms, while token editors validate and normalize tags without exposing their CSV representation. The TUI follows the same product-level interaction language in terminal-native form: arrows select fields, `e` or Enter begins editing, Enter accepts a value, and Escape cancels it. CLI, TUI, and GUI also open `data/mixology.db` by default, so each surface presents the same stored application state.

The current package shape repeats the same ownership story at every level. `app/domains` contains seven bounded contexts: audit, drinks, ingredients, inventory, menus, orders, and tagging. A full operational context exposes its facade at the package root, keeps collaboration contracts in `models`, `queries`, and `events`, owns Cedar policy in `authz`, and hides commands and persistence below `internal`. Its CLI, GUI, and TUI adapters sit together below `surfaces`, so readers can follow one capability vertically without mixing presentation code into the domain's public API. Audit and tagging use smaller explicit profiles because they need fewer layers.

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
  surfaces/tui/                   Mixology-wide TUI contracts and components
pkg/
  toolkits/{cli,gui,tui}/         reusable presentation mechanics
  middleware/                     authorization, transactions, events, audit, and metrics
  {authn,authz,dispatcher,filter,store}/
main/
  {cli,gui,tui}/                  executable composition roots
  seed/                           sample-data executable
```

The boundaries are checked from several directions. Captured `arch-lint` rules apply the same restrictions to present and future domains and surfaces. Topology tests reject unrecognized peer layers, and composition tests compare the domain directories with the modules exposed by the application. Application fixtures then exercise the real embedded store, middleware, authorization, dispatch, audit, and domain handlers. Cross-surface tests mutate through one adapter and observe through another, checking shared behavior without requiring the adapters to share their implementation.

The [Building High-Quality Software preview](/guides/building-high-quality-software.md) follows that
thread through eleven planned lessons: enforced boundaries, constraints encoded in types, the
shared operation pipeline, transactional events, focused code generation, error contracts,
policy-based authorization, interchangeable CLI and bespoke MVVM-style TUI and GUI surfaces, an owned seam for
cross-domain features such as tags, production-shaped tests, and the discipline to stop before
simple becomes simplistic.
