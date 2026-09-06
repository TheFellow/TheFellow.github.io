<!-- Generated from https://thefellow.github.io/articles/preserving-truth-through-operational-degradation/ by scripts/generate_llm_content.py; do not edit. -->

# Preserving Truth Through Operational Degradation

Source: [https://thefellow.github.io/articles/preserving-truth-through-operational-degradation/](https://thefellow.github.io/articles/preserving-truth-through-operational-degradation/)

## Pyramid summary

- **~2 words:** Honest degradation
- **~8 words:** Preserve history while blocking knowingly degraded state promotion.
- **Expanded:** How explicit replacement, review states, readiness reports, and historical snapshots let a modular application degrade honestly without erasing business context.

## Full content

**Part 3 of [Building Mixology](/series/mixology.md).**

Operational software rarely gets to choose between completely healthy data and deletion. Products are discontinued, stock disappears, substitutions become temporary, and decisions already in flight still need to explain what happened.

[Mixology](https://github.com/TheFellow/go-modular-monolith) uses ingredient retirement to explore that middle. An ingredient can be retired with a permanent replacement, or it can be retired without one. The difference changes future recipes, pending orders, menu publication, availability, audit records, and what each actor may inspect. The application preserves those distinctions instead of reducing them to a cascade delete.

This guide follows the modeling decisions. [Turning Cross-Domain Calls into Enforced Boundaries](/articles/turning-cross-domain-calls-into-enforced-boundaries.md) explains how the transactional dispatcher keeps their implementation modular.

## Name the business decision

Deletion describes storage. Retirement describes intent.

The Ingredients domain exposes a Retire operation with its own Cedar action and stable presentation control. The request can include a replacement ingredient and conversion ratio, a reason, and an explicit withdrawal choice. Without withdrawal, retirement discontinues future service while honoring usable existing reservations; withdrawal quarantines stock and blocks affected open orders. An absent replacement says that no approved permanent successor is currently known.

```go
type Retirement struct {
    Withdraw      bool
    Reason        string
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

An optional ingredient is the useful exception. If it retires without replacement, Drinks can remove it from the future recipe. If that would leave an empty recipe, the drink requires review rather than pretending that an empty recipe is valid. A required ingredient remains in the recipe and moves the Drink from `active` to `review_required`. Keeping the reference tells an editor what must be resolved.

The event handler also cleans substitute lists. A retired substitute is removed, a permanent replacement can take its place, and duplicates of the primary ingredient are discarded. An ID-only substitute candidate cannot express an independent ratio. A permanent replacement with a non-1 ratio affecting that candidate is rejected with the dependent drink ID until the candidate is explicitly revised. These rules prevent a mechanically valid rewrite from silently changing recipe quantities.

Temporary catalog substitutions are persisted by original and substitute IDs, with ratio, quality, disabled state, notes, and revision. Renames do not alter those identities. `Ingredients.SetSubstitution` checks update authority on the original, read authority on the substitute, and dimensional compatibility. Rule and stock changes refresh menu availability, including dependencies that appear only through those rules.

## Rewrite plans, preserve records

A replacement applies to future intent. It does not rewrite history.

Drink recipes are current product definitions, so an explicit permanent replacement updates them transactionally. Orders preserve an immutable `AcceptanceSnapshot` containing menu and drink names, agreed prices, ordered quantities and notes, preparation steps and garnish, and the chosen or omitted ingredients. A separate `Plan` describes currently approved preparation; `IngredientUsage` aggregates the quantities that Inventory reserves. Retirement does not change acceptance or silently amend the plan. Discontinuation honors usable reservations, while explicit withdrawal blocks affected open orders.

```text
retirement with replacement
  current recipe       -> rewritten to replacement
  acceptance           -> unchanged
  approved plan        -> unchanged unless explicitly amended
  discontinue          -> honor usable reservations
  withdraw             -> quarantine stock, block affected orders
```

That asymmetry is important. If the application silently changed an existing order, it would lose the ability to explain what the customer requested, what inventory commitment was made, and why fulfillment later stopped. Snapshot fields are valuable only when later catalog changes cannot reinterpret them.

Audit distinguishes changed resources in `Touches`, referenced entities in `Participants`, and domain-authored before/after explanations in `Effects`. Merely inspecting a menu does not claim its contents changed. A `WorkflowID` connects composed commands; after a managed rollback, one failed activity records attempted effects, not committed changes. The returned error preserves both the original failure and a failure to record evidence.

## Amend the approved plan explicitly

`Orders.Amend` takes the order ID, expected revision, reason, explicit replacements, and optional preparation changes for selected drink lines. It accepts only pending or blocked orders. Ratios multiply currently selected quantities; unspecified preparation retains its previously approved values. The original acceptance and agreed prices remain unchanged.

The command projects stock with its own reservations released before planning the complete amended order. That prevents an order from competing with its own existing commitment. `OrderAmended` carries before and after state. Inventory verifies the old reservation identities and quantities, releases them, and reserves the new plan; Menus prepares availability from the net change; Orders reconciles peers helped by released commitments. Failure in any reaction rolls the plan, amendment history, reservations, projections, and success audit back together.

`App.AmendOrders` validates every selected order's revision before executing any amendment, because reconciliation can legitimately advance a peer's revision within the batch. It then reloads the in-transaction token for each command. `App.RetireIngredient` can compose those selected amendments and retirement in one workflow. The operator supplies the selection and reason; the system does not infer customer consent or amend unselected orders.

## Keep physical stock after service eligibility changes

| Operation | Physical record | Fulfillment consequence |
| --- | --- | --- |
| Discontinue | Retain quantity, identity, tags, and history | No new service; honor usable accepted reservations |
| Withdraw or quarantine | Retain stock and reason | Block affected open orders |
| Release quarantine | Retain stock; restore active or discontinued state according to catalog lifecycle | Reconcile commitments without reviving a retired catalog item |
| Dispose | Subtract physical quantity and append a movement; retain the row | Reconcile shortages; zero remainder becomes disposed |

A replacement ingredient does not inherit the old ingredient's physical stock. Disposal requires a positive amount, reason, and expected revision; it rejects removing more than exists. Completion refuses quarantined stock and incomplete or mismatched reservations.

Stock and reservations persist canonical quantities, using ml for volume and each discrete unit's native identity. Display units are separate from `CostUnit`, the basis of `CostPerUnit`. Changing an ingredient from oz to ml changes presentation, not physical quantity, accepted usage, or the meaning of the price. Incompatible dimensional changes require a replacement identity.

## Recover commitments as deliberately as they are blocked

A stock correction below aggregate reservations blocks every affected open order; it does not choose winners by FIFO or priority. Replenishment, cancellation, amendment release, and quarantine release reconcile the same rule. Clearing one ingredient's blocker must not clear another.

For example, two orders reserve 2 units each against 3 on hand. Both are blocked. Cancelling one releases 2 units; the remaining commitment fits and returns to pending if no other blockers remain. The Orders cancellation handler prepares this result from projected remaining reservations before Inventory removes reservation rows.

Optional ingredients participate in planning too. An included optional is snapshotted, reserved, consumed, and costed. If a candidate would prevent fulfilling a required ingredient, the planner can backtrack and omit the optional. Its omission remains explicit in acceptance; nothing silently consumes it later. Cost estimates use a complete feasible recipe plan, skip omitted optionals, preserve unknown prices, and require compatible currencies for margins.

## Distinguish degradation from promotion

<figure class="article-figure article-figure--compact">
  <img src="/assets/images/articles/degradation/degradation-vs-promotion.png" alt="A published serviceable menu may become published but degraded while retaining history. A draft with the same blocker cannot be promoted until readiness is restored.">
  <figcaption>An existing published state may degrade honestly. A draft with a known blocker cannot use that tolerance as permission to become published.</figcaption>
</figure>

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

The CLI, Bubble Tea TUI, and Fyne GUI expose permanent replacement during retirement and menu-readiness inspection. Amendment, batch amendment, substitution administration, quarantine/release, disposal, and movement history also have CLI entrypoints. GUI/TUI historical details show accepted preparation and amendment reasons, but dedicated forms for all the newer workflows are not yet present. They share domain operations, control IDs, and the function that composes readiness into an already-authorized Publish action. They do not share views.

The graphical and terminal interfaces load readiness asynchronously because it crosses several query boundaries. Each request captures the selected menu. If selection changes before the result returns, the surface rejects the stale result rather than attaching one menu's blockers to another menu's Publish control. The TUI also keeps reads out of `View`. Historical order details use accepted names and preparation rather than resolving the current catalog as though it were the accepted order.

The CLI remains synchronous, but it presents the same report codes and severities and receives the same rich command errors. Cross-surface tests can retire through one adapter and observe the resulting state through another, proving that business behavior lives below presentation.

## Test the distinctions, not only the happy path

The most useful scenarios begin with a healthy, published menu and a pending order, then introduce change:

1. Discontinue a required ingredient without replacement. Assert recipe review, retained stock and acceptance, honored usable reservations, degraded menu, and rejected future publication. Explicit withdrawal should instead quarantine and block.
2. Retire with a compatible permanent replacement. Assert the future recipe rewrite and unchanged historical snapshot.
3. Retire an optional ingredient. Assert that the stale reference disappears; if the recipe becomes empty, assert review.
4. Offer only a temporary substitute. Assert limited availability and a publication blocker without canonical rewrite.
5. Leave stock merely low. Assert a warning that does not block publication.
6. Query readiness as different actors. Assert useful visibility for managers and no disclosure to denied roles.
7. Force a handler failure. Assert rollback across the retirement and every dependent mutation.
8. Change interface selection while readiness loads. Assert that stale results are discarded.
9. Permute retirement and cancellation handler order. Assert identical persisted results.
10. Fail the second selected amendment. Assert all plans and reservations unchanged and one failed workflow activity retained.
11. Change display units, quarantine, release, and dispose stock. Assert physical history, cost basis, and existing commitments stay coherent.
12. Race a stale stock or combined entity/tag editor with another writer. Assert conflict and no partial commit.

The [cross-domain regression tests](https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/cross_domain_regression_test.go) and [workflow tests](https://github.com/TheFellow/go-modular-monolith/blob/635c59b4101bdc614beb973cef83e8c2073a9787/app/cross_domain_workflows_test.go) make these distinctions executable. These domain-schema changes use a freshly seeded teaching database, not an invented backfill of missing historical facts.

Each case protects a semantic boundary. Together they show that consistency means more than making all tables agree. Current plans, historical records, operational availability, user-visible actions, and authorization can legitimately represent different views of the same event.

Drink and menu deletion have separate dependency guards. Active menus and historical order usage can veto drink deletion; order usage can veto menu deletion, including terminal history. Redrafting retains the prior publication timestamp. An immutable acceptance snapshot is not blanket permission to delete every referenced catalog identity.

## Preserve enough truth to recover

The important move is refusing to make deletion carry every meaning.

Retirement records a catalog lifecycle decision. Permanent replacement changes future intent. Temporary substitution describes present operations. Review state preserves unresolved work. Order snapshots preserve history. Readiness makes degradation queryable. Publish prevents knowingly promoting that degradation. Cedar limits who may see and act on the result, while audit connects the original decision to its transactional consequences.

That collection of small, explicit states creates a more realistic application. It also creates a better teaching example: the modular boundaries matter because each domain has a genuine decision to own.
