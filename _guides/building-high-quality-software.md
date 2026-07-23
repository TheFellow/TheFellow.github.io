---
title: "Building High-Quality Software"
excerpt: "A planned ten-part written and video series using Mixology to show how simple, enforced rules produce clean architecture."
permalink: /guides/building-high-quality-software/
---

<div class="notice--series" markdown="1">
**Series status:** outline ready; written chapters and companion videos are planned. Track the source material in [GitHub issue #23](https://github.com/TheFellow/go-modular-monolith/issues/23).
</div>

This series uses the [Mixology modular monolith](https://github.com/TheFellow/go-modular-monolith) as a teaching vehicle. The goal is not to narrate every line. Each lesson isolates one principle, shows the mechanism that enforces it, and points to a small part of the repository where the idea can be tested.

## 1. Boundaries Are Walls, Not Lines

A boundary that can be crossed accidentally is only a suggestion. This lesson uses the seven rules in `.arch-lint.yaml` to show how package isolation becomes a build-time constraint, then deliberately introduces an illegal import to make the feedback loop concrete.

**Code route:** `.arch-lint.yaml` → the affected domain packages → `go tool arch-lint`.

## 2. Make Illegal States Unrepresentable

Typed entity IDs prevent identifiers from being exchanged accidentally, exhaustive switches force new variants to be handled, and a deliberately restricted `HandlerContext` makes cascading events impossible from handlers. The common thread is moving important constraints from comments and review into the compiler.

**Code route:** `app/kernel/entity/entities.go` → `pkg/middleware/context.go` → a domain handler.

## 3. One Pipeline, Every Concern

Logging, metrics, authorization, activity tracking, transactions, execution, and event dispatch surround domain operations without appearing inside domain logic. The lesson follows one command and one query through their middleware chains, including authorization against both current and resulting state.

**Code route:** `pkg/middleware/chains.go` → `pkg/middleware/authz.go` → `pkg/middleware/run.go`.

## 4. Events Carry State, Not References

Events carry the changed aggregate so independent handlers can react without reloading it. Multiple handlers prepare before any mutate state, then run inside the originating transaction; a failure rolls the entire operation back without introducing a message broker or eventual consistency.

**Code route:** `app/domains/*/events/` → `pkg/dispatcher/dispatcher_gen.go` → `app/domains/menus/handlers/ingredient-deleted.go`.

## 5. Generate the Boring Parts

Four focused generators own dispatcher routing, Cedar policy assembly, typed IDs, and error helpers. This chapter looks at the repeated structure each generator replaces and at the discipline of keeping a small generator—not hand-edited generated output—as the source of truth.

**Code route:** `pkg/dispatcher/gen` → `pkg/authz/gen` → `app/kernel/entity/gen` → `pkg/errors/gen`.

## 6. Errors Are a Contract

One typed error vocabulary maps failures to HTTP statuses, gRPC codes, CLI exit codes, and TUI presentation without leaking transport details into the domain. Generated test assertions make the same contract convenient to verify.

**Code route:** `pkg/errors/kind.go` → `pkg/errors/error.go` → `pkg/errors/gen`.

## 7. Authorization as Policy, Not Code

Cedar policy files make permission rules readable independently of Go control flow. This lesson traces a policy from a domain's `authz` directory through assembly and evaluation, then compares get semantics with list filtering and command checks against both input and output state.

**Code route:** `app/domains/*/authz/` → `pkg/authz/authorize.go` → `pkg/middleware/authz.go`.

## 8. One Binary, Every Surface

The CLI and Bubble Tea TUI call the same application operations through the same middleware. Their job is input mapping and presentation. A future HTTP or gRPC surface should be another shell around that core, not a reason to rewrite business logic.

**Code route:** a domain's `surfaces/cli/` and `surfaces/tui/` → `main/cli/cli.go`.

## 9. Test the Pipeline, Not the Plumbing

Tests use the real middleware, authorization, event dispatch, database transactions, audit tracking, and public module methods. Fast isolated fixtures make it practical to test the system that ships instead of a parallel architecture assembled from mocks.

**Code route:** `pkg/testutil/fixture.go` → representative tests under `app/domains/*/`.

## 10. The Simplest Thing That Works

The application is one binary backed by one embedded transactional database. The closing lesson inventories what is intentionally absent—service mesh, broker, orchestration—and asks what evidence would justify adding any of it without weakening the invariants already in place.

**Code route:** application bootstrap → `pkg/middleware` unit of work → bstore persistence.

## Planned format

Each finished lesson will include:

1. the architectural problem and failure mode;
2. a small repository map;
3. a code walkthrough and an experiment readers can repeat;
4. tradeoffs and the conditions under which the technique does not fit; and
5. an embedded companion video when it is available.

