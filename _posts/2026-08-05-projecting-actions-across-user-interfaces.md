---
title: "Projecting Actions Across User Interfaces"
date: 2026-08-05 00:00:00 -0700
last_modified_at: 2026-08-06 17:40:00 -0700
permalink: /notes/projecting-actions-across-user-interfaces/
series: mixology
series_order: 12
excerpt: "How Mixology projects authorization and lifecycle prerequisites once, then lets GUI and TUI render native action state without sharing their views."
icon: "modules"
accent: "#74c0fc"
tags: ["Go", "Cedar", "Authorization", "GUI", "TUI", "Architecture"]
---

{% include series-notice.html %}

An action can be unavailable for two very different reasons. The current actor may not have permission to perform it, or the domain may not be in a state where the action makes sense. Collapsing both cases into one boolean loses information that a useful interface needs.

Menus in [Mixology](https://github.com/TheFellow/go-modular-monolith) made that distinction concrete. Publishing has its own Cedar permission, but it also requires a draft menu with publishable contents. Denial should remove Publish from the interface. An authorized draft that still needs work should keep Publish visible, disable it, and explain what must change.

Mixology now projects that meaning for its Fyne GUI and Bubble Tea TUI while allowing both interfaces to remain native to their runtimes. Drinks, Ingredients, Inventory, Menus, Orders, Audit, and Tagging each own their action declarations rather than leaving individual presenters to assemble capability checks. Menus then composes its cross-domain readiness report into the authorized Publish state.

## Give each state one meaning

<figure class="article-figure">
  <img src="{{ '/assets/images/notes/actions/action-states.png' | relative_url }}" alt="Three action presentations: permission denial omits the control, authorization with an unmet prerequisite shows a disabled Publish button and reason, and a ready action shows an enabled Publish button.">
  <figcaption>Visibility communicates permission; enabled state communicates readiness. Execution still repeats authorization and domain invariants.</figcaption>
</figure>

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

The IDs are namespaced by their owning domain, such as `drinks.create`, `menus.publish`, and `orders.complete`. A projector returns collection controls when no entity is selected, then adds row and detail controls for the concrete selected model. This gives shells and surfaces one capability vocabulary without making a presenter import another presenter's state.

## Authorize real resources

The projectors accept one shared function type:

```go
type EntityAuthorizer func(
    context.Context,
    cedar.EntityUID,
    cedar.EntityUID,
    cedar.Entity,
) error
```

The default implementation calls Mixology's in-process Cedar policy set. Keeping the boundary as a function makes the projector easy to test and permits an application to adapt a remote policy evaluator without changing the action model.

Every check uses a real entity from the policy model. Create and placement actions use the domain's defined prospective resource. Selected actions use the complete Cedar entity for that Drink, Menu, Order, or other model. Collection entry is different: when a list query authorizes and elides individual results, the list control is public because there is no collection entity to authorize. This does not make the rows public. It states that entering the catalog is allowed while the query pipeline remains responsible for which entities appear.

Audit and Tag discovery have genuine authorization resources and project them accordingly. Tagging's target actions cross ownership boundaries, so its projector resolves the target's registered Get, Tag, and Untag actions instead of guessing another domain's Cedar vocabulary.

## Share durable meaning, not runtime state

The projector belongs to the domain because action names and lifecycle prerequisites belong there. Its result is framework-neutral because neither Cedar nor menu lifecycle knows about Fyne widgets or Bubble Tea key bindings.

The GUI maps projected state into visible and enabled controls. The TUI maps the same state into accepted keys, contextual help, and explanatory detail text. They agree about what Publish means without sharing a universal view model.

Some durable conditions require more than the selected entity. Menu readiness reads Drinks, Ingredients, and Inventory and returns coded blockers and warnings. GUI and TUI request that report asynchronously, reject results for a stale selection, then call the same `ApplyReadiness` function to disable an authorized Publish action when blockers exist. Permission remains the first stage, so a denied actor never receives a visible control merely because readiness was calculated.

This two-stage composition avoids moving cross-domain reads into a synchronous projector or into Bubble Tea's `View`. The domain still owns the final action meaning, while each runtime owns request scheduling and stale-result protection.

Transient constraints stay on each side of that boundary. A dirty GUI form, an open confirmation dialog, TUI focus, and a request already in flight can temporarily suppress an action. Those facts describe the current interaction, not the domain capability, so folding them into the shared projector would couple otherwise independent runtimes.

This split also clarifies testing. Projector tests cover permission inheritance, overrides, lifecycle conditions, disabled reasons, public collection entry, real entity authorization, invalid declarations, and evaluation failures. GUI and TUI tests cover their native mappings and transient constraints. Lifecycle tests exercise the command itself.

Projection failure also has defined recovery behavior. A presenter clears the affected capability state so an earlier enabled action cannot survive an evaluator error, reports the projection error without overwriting an unrelated load error, and recomputes on the next refresh or selection. This makes failure distinct from denial and prevents stale authority from leaking across targets.

## Projection guides, commands enforce

Action projection is a preflight description, not a security boundary. State can change after rendering, another request can race the current one, and callers can bypass both graphical interfaces. Publish therefore repeats Cedar authorization and menu invariants inside the normal application command pipeline.

This duplication is deliberate because the two checks answer different questions. Projection asks what the interface should honestly offer now. Command enforcement asks whether the operation may commit against current state. The first makes the product understandable; the second preserves correctness.

The resulting abstraction is narrower than a shared view model and more useful than a collection of `CanPublish` booleans. Domains project stable action meaning, a small evaluator gives that meaning consistent semantics, and every interface keeps the interaction model that fits its runtime.
