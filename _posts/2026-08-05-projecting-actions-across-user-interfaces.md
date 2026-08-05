---
title: "Projecting Actions Across User Interfaces"
date: 2026-08-05 00:00:00 -0700
last_modified_at: 2026-08-05 00:00:00 -0700
permalink: /notes/projecting-actions-across-user-interfaces/
excerpt: "How Mixology projects authorization and lifecycle prerequisites once, then lets GUI and TUI render native action state without sharing their views."
icon: "modules"
tags: ["Go", "Cedar", "Authorization", "GUI", "TUI", "Architecture"]
---

An action can be unavailable for two very different reasons. The current actor may not have permission to perform it, or the domain may not be in a state where the action makes sense. Collapsing both cases into one boolean loses information that a useful interface needs.

Menus in [Mixology](https://github.com/TheFellow/go-modular-monolith) made that distinction concrete. Publishing has its own Cedar permission, but it also requires a draft menu with publishable contents. Denial should remove Publish from the interface. An authorized draft that still needs work should keep Publish visible, disable it, and explain what must change.

Mixology now projects that meaning once for its Fyne GUI and Bubble Tea TUI while allowing both interfaces to remain native to their runtimes.

## Give each state one meaning

The shared presentation result is deliberately small:

```go
type State struct {
    ID             ID
    Visible        bool
    Enabled        bool
    DisabledReason string
}
```

The evaluator applies a strict sequence. It checks permission first. A typed permission denial produces an invisible, disabled action and skips its conditions. Any other authorization error remains an error rather than masquerading as denial. Once permission succeeds, conditions run in declaration order. The first unmet condition leaves the action visible, disables it, and supplies a reason.

That creates three outcomes with distinct meanings:

| Result | Meaning | Presentation |
| --- | --- | --- |
| Not visible | Cedar denied the operation | Omit the control and its shortcut |
| Visible, disabled | The actor is authorized, but a prerequisite is unmet | Show the control and explain what must change |
| Visible, enabled | Preflight permission and prerequisites passed | Offer the action |

Evaluation failure is a fourth outcome, but it is not action state. The surface reports it as an operational error.

## Declare permission at the right scope

Controls form groups so a domain can state a broad permission once. A menu editor can require Edit for its ordinary controls, then override Publish with the distinct Publish authorization check. An explicitly public control can remove an inherited requirement.

```go
declaration := actions.Group{
    Permission: actions.Require(canEdit),
    Controls: []actions.Control{
        {ID: nameAction},
        {
            ID:         publishAction,
            Permission: actions.Require(canPublish),
            Conditions: []actions.Condition{publishable},
        },
    },
}
```

The override matters. Treating group permission as an unconditional gate would make Publish inherit Edit even though Cedar models them as different operations. The declaration instead follows the actual capability boundary. Stable IDs also keep mapping independent of labels, translations, and control order.

## Share durable meaning, not runtime state

The projector belongs to the domain because action names and lifecycle prerequisites belong there. Its result is framework-neutral because neither Cedar nor menu lifecycle knows about Fyne widgets or Bubble Tea key bindings.

The GUI maps projected state into visible and enabled controls. The TUI maps the same state into accepted keys, contextual help, and explanatory detail text. They agree about what Publish means without sharing a universal view model.

Transient constraints stay on each side of that boundary. A dirty GUI form, an open confirmation dialog, TUI focus, and a request already in flight can temporarily suppress an action. Those facts describe the current interaction, not the domain capability, so folding them into the shared projector would couple otherwise independent runtimes.

This split also clarifies testing. Projector tests cover permission inheritance, overrides, lifecycle conditions, disabled reasons, invalid declarations, and authorization failures. GUI and TUI tests cover their native mappings and transient constraints. Lifecycle tests exercise the command itself.

## Projection guides, commands enforce

Action projection is a preflight description, not a security boundary. State can change after rendering, another request can race the current one, and callers can bypass both graphical interfaces. Publish therefore repeats Cedar authorization and menu invariants inside the normal application command pipeline.

This duplication is deliberate because the two checks answer different questions. Projection asks what the interface should honestly offer now. Command enforcement asks whether the operation may commit against current state. The first makes the product understandable; the second preserves correctness.

The resulting abstraction is narrower than a shared view model and more useful than a collection of `CanPublish` booleans. Domains project stable action meaning, a small evaluator gives that meaning consistent semantics, and every interface keeps the interaction model that fits its runtime.
