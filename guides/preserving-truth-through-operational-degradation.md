<!-- Generated from https://thefellow.github.io/guides/preserving-truth-through-operational-degradation/ by scripts/generate_llm_content.py; do not edit. -->

# Preserving Truth Through Operational Degradation

Source: [https://thefellow.github.io/guides/preserving-truth-through-operational-degradation/](https://thefellow.github.io/guides/preserving-truth-through-operational-degradation/)

## Pyramid summary

- **~2 words:** Honest degradation
- **~8 words:** Preserve history while blocking knowingly degraded state promotion.
- **Expanded:** How explicit replacement, review states, readiness reports, and historical snapshots let a modular application degrade honestly without erasing business context.

## Full content

Operational software rarely gets to choose between completely healthy data and deletion. Products are discontinued, stock disappears, substitutions become temporary, and decisions already in flight still need to explain what happened.

[Mixology](https://github.com/TheFellow/go-modular-monolith) uses ingredient retirement to explore that middle. An ingredient can be retired with a permanent replacement, or it can be retired without one. The difference changes future recipes, pending orders, menu publication, availability, audit records, and what each actor may inspect. The application preserves those distinctions instead of reducing them to a cascade delete.

This guide follows the modeling decisions. [Turning Cross-Domain Calls into Enforced Boundaries](/guides/turning-cross-domain-calls-into-enforced-boundaries.md) explains how the transactional dispatcher keeps their implementation modular.

## Name the business decision

Deletion describes storage. Retirement describes intent.

The Ingredients domain exposes a Retire operation with its own Cedar action and stable presentation control. The request can include a replacement ingredient and conversion ratio. Absence is meaningful: it says that no approved permanent replacement is currently known.

```go
type Retirement struct {
    ReplacementID IngredientID
    Ratio         float64
}
```

The command rejects malformed intent before publishing a fact. A replacement must differ from the retired ingredient, exist, remain active, share its category, and use a convertible unit. The ratio must be finite and positive. The actor must also be able to read the proposed replacement, otherwise the request could use a hidden catalog record as an oracle.

These checks deliberately stop short of claiming that category equality proves product equivalence. Herradura and Hornitos can pass structural tequila compatibility, but choosing one as the canonical replacement remains a manager's business decision. The model validates what the application can know and records who supplied the judgment.

## Keep three forms of substitution separate

Permanent replacement, temporary substitution, and removal express different facts.

| Decision | Meaning | Recipe consequence |
| --- | --- | --- |
| Permanent replacement | Use the new catalog item as future product intent | Rewrite the canonical ingredient and amount |
| Temporary substitution | Fulfill a current shortage without redefining the product | Keep the canonical recipe and report limited availability |
| No replacement | The required component has no approved successor | Preserve the unresolved reference and require review |

An optional ingredient is the useful exception. If it retires without replacement, Drinks can remove it from the future recipe because its absence does not change whether the drink is achievable. A required ingredient remains in the recipe and moves the Drink from `active` to `review_required`. Keeping the reference tells an editor what must be resolved.

The event handler also cleans substitute lists. A retired substitute is removed, a permanent replacement can take its place, and duplicates of the primary ingredient are discarded. These small rules prevent a mechanically valid rewrite from leaving contradictory recipe state.

## Rewrite plans, preserve records

A replacement applies to future intent. It does not rewrite history.

Drink recipes are current product definitions, so an explicit permanent replacement updates them transactionally. Pending Orders contain snapshots of the recipe selected when the order was placed. Those snapshots continue to name the retired ingredient and the order becomes blocked, even if the current Drink now uses its successor.

```text
retirement with replacement
  current recipe       -> rewritten to replacement
  historical snapshot  -> retains retired ingredient
  pending order        -> blocked for explicit resolution
```

That asymmetry is important. If the application silently changed an existing order, it would lose the ability to explain what the customer requested, what inventory commitment was made, and why fulfillment later stopped. Snapshot fields are valuable only when later catalog changes cannot reinterpret them.

Audit follows the same rule. The retirement entry touches the retired ingredient, the selected replacement, and every recipe or order changed by handlers. A reviewer can connect one authorized decision with its complete transactional blast radius without pretending that the event erased earlier facts.

## Distinguish degradation from promotion

An already-published menu can become degraded after an ingredient retires or inventory changes. Automatically unpublishing it would hide what operators and customers were already relying on. Automatically deleting its drinks would destroy the context needed to repair it.

Mixology therefore allows degradation in place. The Menu retains its publication status and membership, while its readiness report explains current problems. The application applies a stricter rule to promotion: a draft menu cannot be published while the system knows it has a blocker.

This produces a useful transition boundary:

```text
published + later degradation  -> remain published, report findings
draft + known degradation      -> reject Publish
draft + warnings only          -> allow Publish
```

The command checks readiness again when Publish executes. A button rendered moments earlier cannot guarantee that inventory, recipes, or authority remain unchanged.

## Make readiness a domain-owned report

Readiness is more than a boolean because repair work needs reasons. Menus owns a report containing stable codes, severity, affected Drink and Ingredient IDs, and an explanatory message.

The current findings distinguish:

- a Drink whose recipe requires review;
- a retired or missing ingredient reference;
- reliance on a temporary substitution;
- an unavailable ingredient;
- low stock.

The first four are blockers. Low stock is a warning because limited quantity does not prove that the menu is impossible to serve. This policy can evolve without teaching every interface how to reconstruct it from raw inventory.

The report is queryable independently of Publish. That gives an owner a repair queue before attempting a state transition and gives reporting or a future Analytics domain a supported source of operational meaning. The query remains under Menus ownership because publication policy belongs to Menus, even though its calculation reads Drinks, Ingredients, and Inventory.

## Treat visibility as part of the model

A readiness report can reveal more than a menu row. It names hidden ingredients, exposes shortages, and identifies recipes under review. Route access alone should not grant that information.

Menus therefore defines a separate `readiness` Cedar action. Managers and owners may query it; actors without that permission do not receive a watered-down report. The retirement command similarly authorizes both the target action and access to a proposed replacement.

The distinction continues into the interfaces:

| State | Publish presentation |
| --- | --- |
| Cedar denies Publish | Control is absent |
| Publish allowed, readiness has blocker | Control is visible, disabled, and explains why |
| Publish allowed, warnings only | Control is enabled and warnings remain inspectable |

Authorization still executes inside the command and query pipelines. Presentation state guides the user, but it is never the enforcement boundary.

## Carry the same behavior through every surface

The CLI, Bubble Tea TUI, and Fyne GUI all expose permanent replacement during retirement and menu-readiness inspection. They share domain operations, control IDs, and the function that composes readiness into an already-authorized Publish action. They do not share views.

The graphical and terminal interfaces load readiness asynchronously because it crosses several query boundaries. Each request captures the selected menu. If selection changes before the result returns, the surface rejects the stale result rather than attaching one menu's blockers to another menu's Publish control. The TUI follows the same rule for asynchronously loaded Drink names and never performs database reads during `View`.

The CLI remains synchronous, but it presents the same report codes and severities and receives the same rich command errors. Cross-surface tests can retire through one adapter and observe the resulting state through another, proving that business behavior lives below presentation.

## Test the distinctions, not only the happy path

The most useful scenarios begin with a healthy, published menu and a pending order, then introduce change:

1. Retire a required ingredient without replacement. Assert `review_required`, blocked order history, degraded published menu, and rejected future publication.
2. Retire with a compatible permanent replacement. Assert the future recipe rewrite and unchanged historical snapshot.
3. Retire an optional ingredient. Assert that the stale recipe reference disappears without forcing review.
4. Offer only a temporary substitute. Assert limited availability and a publication blocker without canonical rewrite.
5. Leave stock merely low. Assert a warning that does not block publication.
6. Query readiness as different actors. Assert useful visibility for managers and no disclosure to denied roles.
7. Force a handler failure. Assert rollback across the retirement and every dependent mutation.
8. Change interface selection while readiness loads. Assert that stale results are discarded.

Each case protects a semantic boundary. Together they show that consistency means more than making all tables agree. Current plans, historical records, operational availability, user-visible actions, and authorization can legitimately represent different views of the same event.

## Preserve enough truth to recover

The important move is refusing to make deletion carry every meaning.

Retirement records a catalog lifecycle decision. Permanent replacement changes future intent. Temporary substitution describes present operations. Review state preserves unresolved work. Order snapshots preserve history. Readiness makes degradation queryable. Publish prevents knowingly promoting that degradation. Cedar limits who may see and act on the result, while audit connects the original decision to its transactional consequences.

That collection of small, explicit states creates a more realistic application. It also creates a better teaching example: the modular boundaries matter because each domain has a genuine decision to own.
